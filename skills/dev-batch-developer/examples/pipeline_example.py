import logging
import time
import json
import sys
from typing import List, Dict, Any, Generator

# Configure structured logging to stderr (leaving stdout clean for potential piping)
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
    stream=sys.stderr
)

class MockDatabase:
    """Simulates a database for reading and writing data."""
    def __init__(self):
        self.data = [
            {"id": i, "name": f"User {i}", "email": f"user{i}@example.com" if i != 4 else "invalid-email", "score": i * 10}
            for i in range(1, 21)
        ]
        self.saved_records = []

    def fetch_users_chunked(self, chunk_size: int) -> Generator[List[Dict[str, Any]], None, None]:
        """Reader component: streams chunks to prevent OOM."""
        for i in range(0, len(self.data), chunk_size):
            yield self.data[i:i + chunk_size]

    def save_users_bulk(self, users: List[Dict[str, Any]]):
        """Writer component: commits records in bulk to optimize network usage."""
        self.saved_records.extend(users)
        logging.info(f"Successfully wrote {len(users)} records to database.")

class UserBatchProcessor:
    """Orchestrates the Reader-Processor-Writer pipeline."""
    def __init__(self, db: MockDatabase, chunk_size: int = 5):
        self.db = db
        self.chunk_size = chunk_size
        self.stats = {"read": 0, "processed": 0, "failed": 0}
        self.dlq = [] # Dead Letter Queue

    def process_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Processor component: validation and transformation of a single record."""
        # Validate email format
        if "@" not in record["email"]:
            raise ValueError(f"Invalid email: {record['email']}")
        
        # Transform record
        processed = record.copy()
        processed["score_level"] = "high" if record["score"] >= 100 else "normal"
        processed["processed_at"] = time.strftime('%Y-%m-%d %H:%M:%S')
        return processed

    def run(self):
        start_time = time.time()
        logging.info("Starting user data batch processing...")

        for chunk in self.db.fetch_users_chunked(self.chunk_size):
            write_buffer = []
            
            for record in chunk:
                self.stats["read"] += 1
                try:
                    # Record-level try-catch prevents the entire pipeline from failing
                    processed_record = self.process_record(record)
                    write_buffer.append(processed_record)
                    self.stats["processed"] += 1
                except Exception as e:
                    self.stats["failed"] += 1
                    error_entry = {"record": record, "error": str(e), "failed_at": time.time()}
                    self.dlq.append(error_entry)
                    logging.warning(f"Failed to process record ID {record['id']}: {e}")

            # Write chunk if there are valid records
            if write_buffer:
                self.db.save_users_bulk(write_buffer)

        duration = time.time() - start_time
        logging.info("Batch processing complete.")
        
        # Telemetry & Summary Log output
        summary = {
            "duration_seconds": round(duration, 3),
            "stats": self.stats,
            "dlq_records_count": len(self.dlq)
        }
        print(json.dumps(summary, indent=2)) # Print final summary to stdout

if __name__ == "__main__":
    db = MockDatabase()
    processor = UserBatchProcessor(db, chunk_size=5)
    processor.run()

---
name: dev-be-developer
description: Guides the agent in developing secure, robust, and clean backend server APIs, structuring code (DDD/MVC), and integrating databases.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **Senior Backend Engineer**. Adopt their exact mindset, priorities, and vocabulary. Do NOT spawn a subagent for this.


Develop Backend feature for: $ARGUMENTS

Follow these guidelines to design, implement, and verify backend APIs, server services, and logic.

## Step 1: Design API Contract
Before writing endpoint code, establish the API contract:
1. **HTTP Methods & URIs**: Use standard REST conventions (e.g., `GET /api/v1/users` to fetch, `POST /api/v1/users` to create).
2. **Request / Response Formats**: Always specify and validate input payloads (schemas like JSON Schema, Zod, or native structs). Use standard JSON payloads for responses.
3. **HTTP Status Codes**:
   * `200 OK` / `201 Created` / `204 No Content` for successes.
   * `400 Bad Request` / `401 Unauthorized` / `403 Forbidden` / `404 Not Found` for client errors.
   * `500 Internal Server Error` for system crashes.

## Step 2: Layered Code Structure
Organize backend code clearly based on the selected architecture pattern:

* **Domain-Driven Design (DDD) / Clean Architecture Layers**:
  * **Domain Layer**: Keep business rules and domain aggregates isolated. No dependencies on database frameworks or network libraries.
  * **Application Layer**: Map request handlers to specific use cases. Orchestrate data flows using repository interfaces.
  * **Infrastructure Layer**: Implement repository interfaces using database frameworks (SQL, ORM, etc.). Setup adapters for external HTTP clients or email senders.
  * **Interface/Presentation Layer**: Wire HTTP/GraphQL routers, controllers, and middlewares (auth, CORS, rate-limiting).

* **MVC Pattern Layers**:
  * **Model**: Represent database schema models and encapsulation of data operations.
  * **Controller**: Route execution, authenticate, validate inputs, fetch from model, and format outputs.

## Step 3: Input Validation and Error Handling
1. **Sanitize & Validate**: Never trust client inputs. Apply schema validations immediately at the presentation layer (e.g., check email format, character limits, type casting).
2. **Unified Error Handler**: Use a global error middleware/handler to catch exceptions.
3. **Structured Error Response**: Return clean error payloads to clients:
   ```json
   {
     "error": "validation_failed",
     "message": "The provided email is already registered.",
     "details": { "email": "must be unique" }
   }
   ```
4. **Structured Logging**: Write internal logs with severity levels (`INFO`, `WARN`, `ERROR`) in JSON format. Do not expose database errors or stack traces to public API clients.

## Step 4: Database & State Operations
1. **Connections**: Use connection pools (e.g., pg-pool, r2d2, sqlx pool) rather than opening a new connection per HTTP request.
2. **Transactions**: Use transactions (`BEGIN ... COMMIT / ROLLBACK`) for operations affecting multiple database tables to guarantee ACID compliance.
3. **Queries**: Avoid raw string interpolation for SQL queries to prevent SQL Injection. Always use parameterized queries (e.g., `SELECT * FROM users WHERE id = $1`).

## Step 5: Security Guardrails
1. **Authentication**: Use secure mechanisms (e.g., JWT with asymmetric keys, or session tokens in HTTP-only cookies).
2. **Passwords**: Never store passwords in plain text. Always hash them using slow hashing functions (e.g., bcrypt, argon2).
3. **Authorization**: Verify permissions on *every* request. Check resource ownership (e.g., ensure user A cannot update user B's profile).

## Step 6: Code Conventions & Documentation
Instead of hardcoded rules, you MUST apply the specific conventions based on the project's language and framework. Before writing code, consult the appropriate convention file:
- TypeScript/Node.js (Backend): [`typescript-node.md`](../../resources/conventions/typescript-node.md)
- TypeScript/React (Frontend): [`typescript-react.md`](../../resources/conventions/typescript-react.md)
- Rust: [`rust.md`](../../resources/conventions/rust.md)
- Python: [`python.md`](../../resources/conventions/python.md)
- Go: [`go.md`](../../resources/conventions/go.md)

1. **Naming Conventions**: Follow the file suffix rules defined in the convention file.
2. **Business Logic Comments**: Follow the 'Why over How' rule.
3. **Module-level README**: Every newly created module must contain a local `README.md` as mandated by the convention guidelines.

## Step 7: Verification (Definition of Done)
For every backend feature implemented:
1. Write unit tests for business logic/use cases (mocking repository adapters).
2. Write integration tests using a test database (e.g., test routers, request/response cycles).
3. Confirm the application compiles, runs, and lint checks pass cleanly.
4. Add `/health` endpoint and verify server health status.

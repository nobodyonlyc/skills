---
name: ship-mcp-build
description: Build, compile, lint, and package an MCP server from source, running tests to verify success.
---

MCP server to build: $ARGUMENTS

Gather context:

```bash
ls package.json pyproject.toml go.mod Cargo.toml 2>/dev/null
node --version 2>/dev/null; python3 --version 2>/dev/null
find . -name "*.ts" -o -name "*.py" | grep -i mcp | head -10
```

Build an MCP server following this workflow:

## 1. Design (confirm before coding)

Identify:
- **Server name** and purpose
- **Tools** to expose: for each tool, define name, description, input schema (JSON Schema), and what it returns
- **Resources** (if any): URIs the server exposes for reading
- **Prompts** (if any): reusable prompt templates
- **Runtime**: Node/TypeScript (preferred) or Python

Present the tool list to the user and confirm before implementing.

## 2. Scaffold

**TypeScript (Node):**
```
<name>/
  src/index.ts       ← server entry, tool handlers
  package.json       ← @modelcontextprotocol/sdk dependency
  tsconfig.json
```

**Python:**
```
<name>/
  server.py          ← server entry, tool handlers
  pyproject.toml     ← mcp dependency
```

## 3. Implement

- Register each tool with proper `inputSchema` (JSON Schema)
- Implement handler logic — keep handlers thin, extract logic into helper functions
- Return structured content: `{ type: "text", text: "..." }` for text, `{ type: "json", data: {...} }` for structured data
- Add error handling: catch exceptions and return `isError: true` with a clear message

## 4. Test locally

```bash
# Node: build and inspect
npm run build && node dist/index.js
# Python
python server.py
```

Use `mcp dev` or `claude mcp add` to connect and verify each tool works.

## 5. Document

Add to the project's README or CLAUDE.md:
- How to install/run the server
- Each tool: name, what it does, required inputs, example output

Don't add tools beyond what was asked. Each tool should do one thing well.

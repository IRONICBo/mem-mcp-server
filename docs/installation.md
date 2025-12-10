# Installation Instructions

### Prerequisites

Install `uv` first - [Modern Python package and project manager](https://docs.astral.sh/uv/getting-started/installation/)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Claude Code

Run in your project root directory:

```bash
claude mcp add mem-mcp --scope project -- uvx --from git+https://github.com/memovai/memov.git mem stdio $(pwd)
```

### VS Code

Create `.vscode/mcp.json` in your project root:

```json
{
  "servers": {
    "mem-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/memovai/memov.git",
        "mem",
        "stdio",
        "${workspaceFolder}"
      ]
    }
  }
}
```

### Cursor

Go to **Files > Preferences > Cursor Settings > MCP**, then add:

```json
{
  "mcpServers": {
    "mem-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/memovai/memov.git",
        "mem",
        "stdio",
        "${workspaceFolder}"
      ]
    }
  }
}
```

### With VectorDB (RAG mode)

To enable semantic search, validation, and debugging tools (`mem_sync`, `validate_commit`, `validate_recent`, `vibe_debug`, `vibe_search`), install with `[rag]` extras:

**Claude Code:**
```bash
claude mcp add mem-mcp --scope project -- uvx --from "git+https://github.com/memovai/memov.git[rag]" mem stdio $(pwd)
```

**VS Code / Cursor:** Change the `--from` argument to:
```
"git+https://github.com/memovai/memov.git[rag]"
```
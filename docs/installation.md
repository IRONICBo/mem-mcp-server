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
claude mcp add mem-mcp --scope project -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
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
        "mem-mcp-launcher",
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
        "mem-mcp-launcher",
        "stdio",
        "${workspaceFolder}"
      ]
    }
  }
}
```

### Antigravity

> **Note:** Antigravity does not support `"${workspaceFolder}"` variable. Please manually enter the absolute path to your project directory.

Go to **Settings > MCP**, then add:

```json
{
  "mcpServers": {
    "mem-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/memovai/memov.git",
        "mem-mcp-launcher",
        "stdio",
        "/absolute/path/to/your/project"
      ]
    }
  }
}
```

Replace `/absolute/path/to/your/project` with the actual absolute path to your project directory (e.g., `/Users/username/projects/my-project` on macOS/Linux or `C:\\Users\\username\\projects\\my-project` on Windows).

### With VectorDB (RAG mode)

To enable semantic search, validation, and debugging tools (`mem_sync`, `validate_commit`, `validate_recent`, `vibe_debug`, `vibe_search`), install with `[rag]` extras:

**Claude Code:**
```bash
claude mcp add mem-mcp --scope project -- uvx --from "git+https://github.com/memovai/memov.git[rag]" mem-mcp-launcher stdio $(pwd)
```

**VS Code / Cursor:** Change the `--from` argument to:
```
"git+https://github.com/memovai/memov.git[rag]"
```
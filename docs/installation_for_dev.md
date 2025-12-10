
## Installation for Contributors

### Prerequisites

- **Python 3.11+** - Required for all functionality
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** - Modern Python package and project manager

### Quick Setup

1. **Clone and install dependencies:**
   ```bash
   git clone git@github.com:memovai/memov.git
   cd memov

   # Basic version (core features only)
   uv sync

   # With VectorDB/RAG support (semantic search, validation, debugging)
   uv sync --extra rag
   ```

2. **Set up development tools:**
   ```bash
   uv pip install pre-commit
   uv run pre-commit install
   ```

3. **Optional: Link core memory package** (for advanced development):
   ```bash
   # Clone the core mem package
   cd ..
   git clone git@github.com:memovai/mem.git

   # Install as editable dependency
   cd memov
   uv pip install -e ../mem
   ```

## Testing Local Development Version

After `uv sync`, you can test your local MCP server with different clients:

### Claude Code

```bash
# Navigate to your test project directory
cd /path/to/your/test/project

# Add local dev MCP server
claude mcp add mem-mcp --scope project -- /path/to/memov/.venv/bin/mem-mcp-launcher stdio $(pwd)
```

### VS Code

Create `.vscode/mcp.json` in your test project:

```json
{
  "servers": {
    "mem-mcp": {
      "type": "stdio",
      "command": "/path/to/memov/.venv/bin/mem-mcp-launcher",
      "args": ["stdio", "${workspaceFolder}"]
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
      "command": "/path/to/memov/.venv/bin/mem-mcp-launcher",
      "args": ["stdio", "${workspaceFolder}"]
    }
  }
}
```

### Using `uv run` (Alternative)

You can also use `uv run` from the memov directory:

```bash
# From the memov project directory
uv run mem-mcp-launcher stdio /path/to/your/test/project
```

## Available Commands

The project provides two main entry points:

| Command | Purpose | Module |
|---------|---------|---------|
| `mem-mcp-server` | Server management CLI | `mem_mcp_server.cli.server_cli:main` |
| `mem-mcp-launcher` | Direct MCP runtime launcher | `mem_mcp_server.server.mcp_launcher:main` |

**Run commands without global installation:**
```bash
uv run mem-mcp-server --help
uv run mem-mcp-launcher --help
```

## Configuration and Logs

Default config directory: `~/.mem_mcp_server`

```
~/.mem_mcp_server/
└── logs/           # Server log files
```

## Installation for Contributors

### Prerequisites

- **Python 3.11+** - Required for all functionality
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** - Modern Python package and project manager

### Quick Setup

1. **Clone and install dependencies:**
   ```bash
   git clone git@github.com:memovai/memov.git
   cd memov
   uv sync
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

## Available Commands

The project provides two main entry points:

| Command | Purpose | Module |
|---------|---------|---------|
| `vit-mcp-server` | Server management CLI | `vit_mcp_server.cli.server_cli:main` |
| `vit-mcp-launcher` | Direct MCP runtime launcher | `vit_mcp_server.server.mcp_launcher:main` |

**Run commands without global installation:**
```bash
uv run vit-mcp-server --help
uv run vit-mcp-launcher --help
```

## Configuration and Logs

Default config directory: `~/.vit_mcp_server`

```
~/.vit_mcp_server/
└── logs/           # Server log files
```
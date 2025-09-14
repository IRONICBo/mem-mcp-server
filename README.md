# Mem MCP Server

Mem extends coding agents with beyond-Git memory — auto-capturing **prompts**, **agent plans**, and **code changes** as bound context.
As your **coding partner**, it accelerates debugging, shares context in real time, reuses edits, prevents agentic infinite loops, and turns history into learning.

- 💬 [Join our Discord](https://discord.gg/YCN75dTh) and dive into smarter context engineering
- 🌐 [Visit memov.im](https://memov.im) to visualize your Mem history and supercharge existing GitHub repos


<div align="center">

[![Add to VS Code](https://img.shields.io/badge/Add%20to%20VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://memov-vscode.vercel.app/)
[![Add to Cursor](https://img.shields.io/badge/Add%20to%20CURSOR-000000?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://memov-vscode.vercel.app/)

</div>

## Features

- 📒 **Context-bound memory**: Automatically track user prompts, agent plans, and code changes — independent of Git history
- 🐞 **Context-aware debugging**: Isolate faulty context and leverage it across LLMs for 5× faster fixing
- 🤝 **Team context sharing**: Real-time alignment with zero friction
- ♻️ **Change reuse**: Reapply past code edits by description to save tokens when iterating on a feature
- 🛑 **Loop guard**: Prevent runaway agent auto-generation by intervening and halting infinite loops
- 🔍 **History-driven optimization**: Use past records and failed generations as reference context to boost future outputs

## MCP Tools

These are available to MCP clients through the server:

- `set_user_context(user_prompt: str, session_id?: str)`
  - Set the exact user request at the beginning of a task. Must be called before recording changes.

- `mem_snap(files_changed: str)`
  - Create a mem snapshot tied to the previously set user prompt. Handles untracked vs modified files intelligently. Argument is a comma-separated list of relative paths.

- `clean_user_context()`
  - Clear the stored context after finishing a task to avoid leakage across interactions.

- `GET /health`
  - Returns "OK". Useful for IDE/agent readiness checks.


## Development Setup

### Prerequisites

- **Python 3.11+** - Required for all functionality
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** - Modern Python package and project manager

### Quick Setup

1. **Clone and install dependencies:**
   ```bash
   git clone git@github.com:memovai/mem-mcp-server.git
   cd mem-mcp-server
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
   cd mem-mcp-server
   pip install -e ../mem
   ```

### Available Commands

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

## Quick Start

### Start a server (HTTP)

```bash
uv run mem-mcp-server start --workspace /path/to/project --port 8080 --host 127.0.0.1
```

Output includes the MCP URL and health endpoint:
- MCP: `http://127.0.0.1:8080/mcp`
- Health: `http://127.0.0.1:8080/health`

### Check status

```bash
uv run mem-mcp-server status | cat
```

### Stop servers

- Stop a specific server:

```bash
uv run mem-mcp-server stop --workspace /path/to/project --port 8080
```

- Stop all servers for a workspace:

```bash
uv run mem-mcp-server stop --workspace /path/to/project
```

- Stop all servers on a port:

```bash
uv run mem-mcp-server stop --port 8080
```

- Stop everything:

```bash
uv run mem-mcp-server stop --all
```

## Launcher (advanced)

You can launch the MCP runtime directly with the launcher.

- HTTP mode:

```bash
uv run mem-mcp-launcher http /path/to/project --host 127.0.0.1 --port 8080
```

- stdio mode (for tools like Claude Desktop):

```bash
uv run mem-mcp-launcher stdio /path/to/project
```

Logs are written to `~/.mem_mcp_server/logs/`.

## Configuration and Logs

Default config directory: `~/.mem_mcp_server`

```
~/.mem_mcp_server/
├── servers.json    # Server registry and status
└── logs/           # Server log files
```

## Integrations

- **Cursor**:
  1. Start a server for your workspace (see Quick Start)
  2. In Cursor Settings → Extensions → MCP, add a new server with URL `http://127.0.0.1:8080/mcp`

- **Claude Desktop**:
  - Use `mem-mcp-launcher stdio /path/to/project` and configure Claude Desktop to start that script in stdio mode

## Development

### Project layout

```
mem_mcp_server/
├── __init__.py
├── globals.py                 # ~/.mem_mcp_server path
├── cli/
│   ├── __init__.py
│   └── server_cli.py          # mem-mcp-server CLI
└── server/
    ├── __init__.py
    ├── mcp_server.py          # FastMCP tools and routes
    └── mcp_launcher.py        # mem-mcp-launcher entry
```

### Setup

```bash
uv sync
```

### Lint/format (if configured)

```bash
uv run black .
uv run isort .
```

### Run tests (if present)

```bash
uv run pytest
```

## Notes on MCP tools provided

The server exposes tools like `set_user_context`, `mem_snap`, and `clean_user_context` via FastMCP, and a `/health` endpoint.

## Troubleshooting

- Port already in use: choose another port or stop the existing server.
- No servers listed by `status`: ensure you started via `mem-mcp-server start`.
- Logs: check `~/.mem_mcp_server/logs/` for the latest log.

## License

MIT License. See `LICENSE`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests where applicable
4. Open a PR

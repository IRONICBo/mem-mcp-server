<p align="center">
  <a href="https://github.com/memovai/memov">
    <img src="docs/images/memov-banner.png" width="800px" alt="MemoV - The Memory Layer for AI Coding Agents">
  </a>
</p>

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


## Installation

Please see [docs/installation.md](docs/installation.md) for detailed installation instructions.

## Installation for Contributors

Please see [docs/installation_for_dev.md](docs/installation_for_dev.md) for detailed installation instructions.

## CLI Commands

Memov provides a powerful command-line interface for managing your project memory:

### Core Commands

- `mem init` - Initialize memov in your project
- `mem track <files>` - Start tracking files
- `mem snap` - Create a snapshot of current state
- `mem history` - View all operations
- `mem show <commit>` - Show snapshot details
- `mem jump <commit>` - Restore to a specific snapshot
- `mem status` - Show working directory status

### 🔍 Semantic Search (NEW) 🪶 Lightweight

Memov now includes vector database-powered semantic search with **zero heavy dependencies**:

```bash
# Search by natural language (similarity scores shown by default)
mem search "authentication bug fix"

# Search by files
mem search "src/auth.py" --by-files

# Filter and limit results
mem search "refactor" --type snap --limit 5
```

**Features:**
- 🧠 **Semantic understanding**: Finds similar prompts even with different words
- 🎯 **File-based search**: Find all commits affecting specific files
- 🏷️ **Type filtering**: Filter by operation type (track, snap, rename, remove)
- 📊 **Rich output**: Beautiful tables with similarity scores
- ⚡ **Fast**: Sub-second search on thousands of commits
- 🪶 **Lightweight**: Only ~150MB total (no PyTorch required!)

**Embedding Options:**
- **Default** (Recommended): Built-in, ~50MB, works immediately ✨
- **FastEmbed**: ONNX Runtime, ~30MB, better quality
- **OpenAI API**: <5MB client, best quality, requires API key

See [EMBEDDING_BACKENDS.md](EMBEDDING_BACKENDS.md) for backend comparison and [SEARCH_COMMAND.md](SEARCH_COMMAND.md) for usage.

## MCP Tools

These are available to MCP clients through the server:

- `mem_snap(files_changed: str)`
  - Create a mem snapshot tied to the previously set user prompt. Handles untracked vs modified files intelligently. Argument is a comma-separated list of relative paths.

- `GET /health`
  - Returns "OK". Useful for IDE/agent readiness checks.


## License

MIT License. See `LICENSE`.

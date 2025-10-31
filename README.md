<p align="center">
  <a href="https://github.com/memovai/memov">
    <img src="docs/images/memov-banner.png" width="800px" alt="MemoV - The Memory Layer for AI Coding Agents">
  </a>
</p>

# Never forget a commit, and vibe debugging

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da?logo=discord&logoColor=white)](https://discord.gg/un54aD7Hug)
[![Twitter Follow](https://img.shields.io/twitter/follow/ssslvky?style=social)](https://x.com/ssslvky)

</div>

MemoV = Prompt + Context + CodeDiff

<p align="center">
  <img src="docs/images/readme.gif" alt="MemoV Demo" width="800px">
</p>

It gives AI coding agents a traceable memory layer beyond Git — auto-capturing **every prompt**, **agent plan**, and **code change** in a separate timeline. Work freely with AI, iterate fast, and keep your Git history clean. When you're ready, cherry-pick what matters for Git commits. Based on memory, we built an open source Aardvark: OpenAI’s agentic security researcher.

- 💬 [Join our Discord](https://discord.gg/un54aD7Hug) and dive into smarter context engineering
- 🌐 [Visit memov.ai](https://memov.ai) to visualize your coding memory and supercharge existing GitHub repos


<div align="center">

[![Add to VS Code](https://img.shields.io/badge/Add%20to%20VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://memov.ai/set-mcp)
[![Add to Cursor](https://img.shields.io/badge/Add%20to%20CURSOR-000000?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://memov.ai/set-mcp)

</div>

## Features

- 📒 **Context-bound memory**: Automatically track user GitDiffs, prompts, and agent plans — independent of Git history
- 🐞 **Vibe debugging**: Isolate faulty context and leverage it across LLMs for 5× faster fixing
- ✅ **Validation & alignment checking**: Verify AI prompts match actual code changes, detect context drift
- 🤝 **Team context sharing**: Real-time alignment with zero friction
- ♻️ **Change reuse**: Reapply past code edits by description to save tokens when iterating on a feature
- 🔍 **History-driven optimization**: Use past records and failed generations as reference context to boost future outputs


## Installation

Please see [docs/installation.md](docs/installation.md) for detailed installation instructions.

## Installation for Contributors

Please see [docs/installation_for_dev.md](docs/installation_for_dev.md) for detailed installation instructions.

## MCP Tools

These are available to MCP clients through the server:

### Core Operations

- `snap(user_prompt: str, original_response: str, agent_plan: list[str], files_changed: str)`
  - Record every user interaction with automatic file tracking. Handles untracked vs modified files intelligently.

- `mem_sync()`
  - Sync all pending operations to VectorDB for semantic search capabilities.

### Validation & Debugging (NEW)

- `validate_commit(commit_hash: str, detailed: bool = True)`
  - Validate a specific commit by comparing prompt/response with actual code changes. Detects context drift and alignment issues.

- `validate_recent(n: int = 5)`
  - Validate the N most recent commits for alignment patterns. Useful for session reviews and quality assurance.

See [DEBUGGING_VALIDATION.md](DEBUGGING_VALIDATION.md) for comprehensive documentation on validation features.

### Health Check

- `GET /health`
  - Returns "OK". Useful for IDE/agent readiness checks.


## License

MIT License. See `LICENSE`.

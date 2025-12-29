<p align="center">
  <a href="https://github.com/memovai/memov">
    <img src="docs/images/memov-banner.png" width="800px" alt="MemoV - AI 编程的记忆层">
  </a>
</p>

<p align="center">
  <a href="README.md">English</a> | <b>简体中文</b> | <a href="README_JA.md">日本語</a>
</p>

# VibeGit🤌：自动管理你的提示词、上下文和代码变化

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da?logo=discord&logoColor=white)](https://discord.gg/un54aD7Hug)
[![Twitter Follow](https://img.shields.io/twitter/follow/ssslvky?style=social)](https://x.com/ssslvky)

</div>

可追溯、Git 驱动的 AI 编程记忆层。提示词、上下文和代码差异**自动版本化** - 这就是 VibeGit!🤌

省去 1000+ 次**手动** commit，你的 .git 依然保持**干净**。

<div align="center">

| MemoV | Checkpoints |
|-------|-------------|
| 分支探索 | 线性时间线 |
| 跨会话 | 绑定会话 |
| 回滚保留所有历史 | 回滚清除历史 |
| 跳转轨迹可追踪 | 无轨迹记录 |

</div>

- 💬 [加入我们的 Discord](https://discord.gg/un54aD7Hug)，探索更智能的 vibe 工程

## 功能特性

- ⚡ **一键安装 MCP** — 适配任何 AI 编程助手
- 🧠 **完整上下文** — 每个提示词 → 代理计划 → 代码差异，实时捕获
- ⏪ **版本控制** — 分支、回滚、重放任何交互
- 🧼 **保持 Git 干净** — 影子 `.mem` 时间线，零污染 `.git`
- 🔍 **可视化界面** — 浏览你的 AI 编程历史
- 🔒 **隐私优先** — 本地存储，无数据库，零开销

## 快速开始（MCP 安装）

### 前置条件

先安装 `uv`：

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Claude Code

在项目根目录运行：

```bash
claude mcp add mem-mcp --scope project -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
```

### Codex

在项目根目录运行：

```bash
codex mcp add mem-mcp -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
```

### VS Code

在项目根目录创建 `.vscode/mcp.json`：

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

进入 **Files > Preferences > Cursor Settings > MCP**，添加：

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

### Web 界面

在对话中说 **"use mem ui"** — 在 `http://localhost:38888` 打开，包含时间线视图、分支过滤、差异查看器和一键跳转到任意快照。

### 启用向量数据库（RAG 模式）

要启用语义搜索、验证和调试工具，使用 `[rag]` 扩展安装：

**Claude Code:**
```bash
claude mcp add mem-mcp --scope project -- uvx --from "git+https://github.com/memovai/memov.git[rag]" mem-mcp-launcher stdio $(pwd)
```

**VS Code / Cursor:** 将 `--from` 参数改为：
```
"git+https://github.com/memovai/memov.git[rag]"
```

## CLI 安装（可选）

如果你想直接使用 `mem` 命令行工具（用于手动追踪、查看历史等）：

### 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/memovai/memov/main/install.sh | bash
```

或使用 wget：

```bash
wget -qO- https://raw.githubusercontent.com/memovai/memov/main/install.sh | bash
```

### 包管理器

<details>
<summary><b>Homebrew (macOS/Linux)</b></summary>

```bash
brew tap memovai/mem
brew install memov
```

</details>

<details>
<summary><b>APT (Debian/Ubuntu)</b></summary>

```bash
echo "deb [trusted=yes] https://memovai.github.io/memov/apt stable main" | sudo tee /etc/apt/sources.list.d/mem.list
sudo apt update
sudo apt install mem
```

</details>

<details>
<summary><b>YUM/DNF (Fedora/RHEL/CentOS)</b></summary>

```bash
sudo curl -o /etc/yum.repos.d/mem.repo https://memovai.github.io/memov/yum/mem.repo
sudo dnf install mem
```

</details>

<details>
<summary><b>从源码安装</b></summary>

需要 Python 3.10+ 和 [uv](https://github.com/astral-sh/uv)：

```bash
git clone https://github.com/memovai/memov.git
cd memov
uv sync
uv pip install -e .
mem --help
```

</details>

## 贡献者安装指南

请参阅 [docs/installation_for_dev.md](docs/installation_for_dev.md) 获取详细安装说明。

## MCP 工具

这些工具可通过 MCP 服务器供客户端使用：

### 核心操作

- `snap(user_prompt: str, original_response: str, agent_plan: list[str], files_changed: str)`
  - 记录每次用户交互，自动追踪文件。智能处理未追踪和已修改的文件。

- `mem_ui(port: int = 38888)`
  - 在 `http://localhost:38888` 启动 Web 界面，可视化浏览历史、查看差异和跳转到任意快照。

- `mem_history(limit: int = 20, commit_hash: str = "")`
  - 查看 memov 历史，包括提示词、响应和文件更改。

- `mem_jump(commit_hash: str)`
  - 跳转到指定快照，恢复所有追踪的文件并创建新分支。

### RAG 工具（需要 `[rag]` 扩展）

这些工具仅在使用 `[rag]` 扩展安装时可用。

- `mem_sync()`
  - 将所有待处理操作同步到向量数据库，启用语义搜索功能。

- `validate_commit(commit_hash: str, detailed: bool = True)`
  - 通过比较提示词/响应与实际代码更改来验证特定提交。检测上下文漂移和对齐问题。

- `validate_recent(n: int = 5)`
  - 验证最近 N 次提交的对齐模式。适用于会话审查和质量保证。

- `vibe_debug(query: str, error_message: str = "", stack_trace: str = "", user_logs: str = "", models: str = "", n_results: int = 5)`
  - 使用 RAG 搜索 + 多模型 LLM 比较进行调试。搜索代码历史获取相关上下文，并行查询多个 AI 模型（GPT-4、Claude、Gemini）获取多样化的调试见解。

- `vibe_search(query: str, n_results: int = 5, content_type: str = "")`
  - 快速语义搜索代码历史（提示词、响应、代理计划、代码更改），无需 LLM 分析。适合快速上下文查找。

### 健康检查

- `GET /health`
  - 返回 "OK"。用于 IDE/代理就绪检查。

## 开源协议

MIT License。详见 `LICENSE`。

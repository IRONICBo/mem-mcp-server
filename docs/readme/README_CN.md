<p align="center">
  <a href="https://github.com/memovai/memov">
    <img src="../images/memov-banner.png" width="800px" alt="MemoV - AI 编程的记忆层">
  </a>
</p>

<p align="center">
  <a href="../../README.md">English</a> | <a href="README_DE.md">Deutsch</a> | <a href="README_ES.md">Español</a> | <a href="README_FR.md">Français</a> | <a href="README_JA.md">日本語</a> | <a href="README_KO.md">한국어</a> | <a href="README_PT.md">Português</a> | <a href="README_RU.md">Русский</a> | <b>中文</b>
</p>

<h4 align="center">VibeGit🤌：自动管理你的提示词、上下文和代码变化</h4>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da?logo=discord&logoColor=white)](https://discord.gg/un54aD7Hug)
[![DeepWiki](https://img.shields.io/badge/DeepWiki-memovai%2Fmemov-blue.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNNCAxOWguNmMuNC0uMi44LS41IDEuMi0uOCAyLjItMS42IDMuNy0zLjggNC4yLTYuMyIvPjxwYXRoIGQ9Ik0xNC42IDEyLjFjLjYtLjkgMS4zLTEuOCAyLjEtMi42IDEuMS0xLjEgMi40LTEuOCAzLjgtMi4yIDEuMS0uMyAyLjItLjQgMy4zLS4zIi8+PHBhdGggZD0iTTE5LjQgNS4yYy0uOC4xLTEuNi4zLTIuMy41LS41LjItLjkuNC0xLjQuNy0uNC4zLS44LjYtMS4xIDEiLz48cGF0aCBkPSJNNiAxOGMtMS44IDAtMy0xLjUtMy0zIDAtMi4yIDEuOS0zLjUgMi44LTUgLjUtLjggMS45LTIuNyAyLjMtMy43LjYtMS4yIDEuMi0yLjQgMS42LTMuNi4xLS40LjUtLjkuOS0uOS43IDAgLjggMS4yLjggMS4zIDAgMS40LS4zIDIuOC0uNyA0LjEtLjQgMS41LTEuMSAyLjktMS44IDQuMyIvPjwvc3ZnPg==)](https://deepwiki.com/memovai/memov)
[![Twitter Follow](https://img.shields.io/twitter/follow/ssslvky?style=social)](https://x.com/ssslvky)

</div>

MemoV 是 AI 编程代理的记忆层，提供**可追溯**、**Git 驱动**的提示词、上下文和代码差异版本控制。它实现了 **VibeGit** - AI 编程会话的自动版本化，支持分支探索、回滚功能，且对标准 .git 仓库**零污染**。

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

- **一键安装 MCP** — 适配任何 AI 编程助手
- **VibeGit for Agents** — 自动追踪提示词、上下文和代码差异，无需手动提交
- **版本控制** — 分支、回滚、重放任何交互
- **保持 Git 干净** — 影子 `.mem` 时间线，零污染 `.git`
- **可视化界面** — 在对话中说 "mem ui"，访问 http://localhost:38888 查看
- **隐私优先** — 本地存储，无数据库，零开销。使用 .memignore 排除文件

## 快速开始（MCP 安装）

### 前置条件

先安装 `uv`：

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 安装 Git（如果未安装）
winget install --id Git.Git -e --source winget
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

<details>
<summary><b>VS Code</b></summary>

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

</details>

<details>
<summary><b>Cursor</b></summary>

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

</details>

<details>
<summary><b>启用向量数据库（RAG 模式）</b> 🚧 WIP</summary>

要启用语义搜索、验证和调试工具，使用 `[rag]` 扩展安装：

**Claude Code:**
```bash
claude mcp add mem-mcp --scope project -- uvx --from "git+https://github.com/memovai/memov.git[rag]" mem-mcp-launcher stdio $(pwd)
```

**VS Code / Cursor:** 将 `--from` 参数改为：
```
"git+https://github.com/memovai/memov.git[rag]"
```

</details>

### 重要提示

**添加规则** — 要在每次交互后自动保存快照，请在你的编程代理中添加规则：

- **Cursor**: Cursor Settings > Rules
- **Claude Code**: `CLAUDE.md`
- 或你的 MCP 客户端中的等效设置

示例规则：

```
After completing any interaction, always call `use mem snap` to save the snapshot.
```

## Web 界面，就说 Use mem ui🤌

在对话中说 **"use mem ui"** — 在 `http://localhost:38888` 打开，包含时间线视图、分支过滤、差异查看器和一键跳转到任意快照。

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
<summary><b>直接下载</b></summary>

下载适合你平台的最新版本：

| 平台 | 下载 |
|------|------|
| Linux x86_64 | [mem-linux-x86_64.tar.gz](https://github.com/memovai/memov/releases/latest/download/mem-linux-x86_64.tar.gz) |
| macOS Intel | [mem-macos-x86_64.tar.gz](https://github.com/memovai/memov/releases/latest/download/mem-macos-x86_64.tar.gz) |
| macOS Apple Silicon | [mem-macos-arm64.tar.gz](https://github.com/memovai/memov/releases/latest/download/mem-macos-arm64.tar.gz) |
| Windows x86_64 | [mem-windows-x86_64.exe.zip](https://github.com/memovai/memov/releases/latest/download/mem-windows-x86_64.exe.zip) |

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

请参阅 [docs/installation_for_dev.md](../installation_for_dev.md) 获取详细安装说明。

## 架构

MemoV 采用三层架构，以 MemovManager 为核心协调器，MCP Server 作为 AI 代理的适配层，以及可选的 RAG 系统用于语义搜索。

![MemoV 架构](../images/Arc.png)

<details>
<summary><b>MCP 工具</b></summary>

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

</details>

## 开源协议

MIT License。详见 `LICENSE`。

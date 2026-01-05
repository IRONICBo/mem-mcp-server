<p align="center">
  <a href="https://github.com/memovai/memov">
    <img src="../images/memov-banner.png" width="800px" alt="MemoV - AIコーディングのメモリレイヤー">
  </a>
</p>

<p align="center">
  <a href="../../README.md">English</a> | <a href="README_DE.md">Deutsch</a> | <a href="README_ES.md">Español</a> | <a href="README_FR.md">Français</a> | <b>日本語</b> | <a href="README_KO.md">한국어</a> | <a href="README_PT.md">Português</a> | <a href="README_RU.md">Русский</a> | <a href="README_CN.md">中文</a>
</p>

<h4 align="center">VibeGit🤌：プロンプト、コンテキスト、差分を自動管理</h4>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da?logo=discord&logoColor=white)](https://discord.gg/un54aD7Hug)
[![DeepWiki](https://img.shields.io/badge/DeepWiki-memovai%2Fmemov-blue.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNNCAxOWguNmMuNC0uMi44LS41IDEuMi0uOCAyLjItMS42IDMuNy0zLjggNC4yLTYuMyIvPjxwYXRoIGQ9Ik0xNC42IDEyLjFjLjYtLjkgMS4zLTEuOCAyLjEtMi42IDEuMS0xLjEgMi40LTEuOCAzLjgtMi4yIDEuMS0uMyAyLjItLjQgMy4zLS4zIi8+PHBhdGggZD0iTTE5LjQgNS4yYy0uOC4xLTEuNi4zLTIuMy41LS41LjItLjkuNC0xLjQuNy0uNC4zLS44LjYtMS4xIDEiLz48cGF0aCBkPSJNNiAxOGMtMS44IDAtMy0xLjUtMy0zIDAtMi4yIDEuOS0zLjUgMi44LTUgLjUtLjggMS45LTIuNyAyLjMtMy43LjYtMS4yIDEuMi0yLjQgMS42LTMuNi4xLS40LjUtLjkuOS0uOS43IDAgLjggMS4yLjggMS4zIDAgMS40LS4zIDIuOC0uNyA0LjEtLjQgMS41LTEuMSAyLjktMS44IDQuMyIvPjwvc3ZnPg==)](https://deepwiki.com/memovai/memov)
[![Twitter Follow](https://img.shields.io/twitter/follow/ssslvky?style=social)](https://x.com/ssslvky)

</div>

MemoVは、AIコーディングエージェントのためのメモリレイヤーです。プロンプト、コンテキスト、コード差分の**トレーサブル**で**Git駆動**のバージョン管理を提供します。**VibeGit**を実現 - AIコーディングセッションの自動バージョン管理、ブランチ探索、ロールバック機能を備え、標準の.gitリポジトリを**汚染しません**。

<div align="center">

| MemoV | Checkpoints |
|-------|-------------|
| ブランチ探索 | 線形タイムライン |
| クロスセッション | セッション限定 |
| ロールバックで全履歴保持 | ロールバックで履歴削除 |
| 全ジャンプを追跡 | 軌跡なし |

</div>

- 💬 [Discordに参加](https://discord.gg/un54aD7Hug)して、スマートなバイブエンジニアリングを探求しよう

## 機能

- **ワンクリックMCP** — あらゆるAIコーディングエージェントに対応
- **VibeGit for Agents** — プロンプト、コンテキスト、コード差分を手動コミットなしで自動追跡
- **バージョン管理** — ブランチ、ロールバック、任意のインタラクションをリプレイ
- **Gitをクリーンに保つ** — シャドウ `.mem` タイムライン、`.git` を汚染しない
- **ビジュアルUI** — チャットで「mem ui」と言うだけ、http://localhost:38888 で表示
- **プライバシーファースト** — ローカル、データベース不要、オーバーヘッドなし。.memignoreで除外

## クイックスタート（MCPインストール）

### 前提条件

まず `uv` をインストール：

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Claude Code

プロジェクトルートディレクトリで実行：

```bash
claude mcp add mem-mcp --scope project -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
```

### Codex

プロジェクトルートディレクトリで実行：

```bash
codex mcp add mem-mcp -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
```

<details>
<summary><b>VS Code</b></summary>

プロジェクトルートに `.vscode/mcp.json` を作成：

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

**Files > Preferences > Cursor Settings > MCP** に移動し、以下を追加：

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
<summary><b>VectorDB対応（RAGモード）</b> 🚧 WIP</summary>

セマンティック検索、検証、デバッグツールを有効にするには、`[rag]` エクストラでインストール：

**Claude Code:**
```bash
claude mcp add mem-mcp --scope project -- uvx --from "git+https://github.com/memovai/memov.git[rag]" mem-mcp-launcher stdio $(pwd)
```

**VS Code / Cursor:** `--from` 引数を以下に変更：
```
"git+https://github.com/memovai/memov.git[rag]"
```

</details>

### 重要なヒント

**ルールを追加** — 各インタラクション後に自動的にスナップショットを保存するには、コーディングエージェントにルールを追加：

- **Cursor**: Cursor Settings > Rules
- **Claude Code**: `CLAUDE.md`
- またはMCPクライアントの同等の設定

ルールの例：

```
After completing any interaction, always call `use mem snap` to save the snapshot.
```

## Web UI、Use mem uiと言うだけ🤌

チャットで **「use mem ui」** と言うだけ — `http://localhost:38888` でタイムラインビュー、ブランチフィルタリング、差分ビューア、任意のスナップショットへのジャンプが開きます。

## CLIインストール（オプション）

`mem` CLIツールを直接使用したい場合（手動トラッキング、履歴表示など）：

### ワンライナーインストール

```bash
curl -fsSL https://raw.githubusercontent.com/memovai/memov/main/install.sh | bash
```

またはwgetで：

```bash
wget -qO- https://raw.githubusercontent.com/memovai/memov/main/install.sh | bash
```

### パッケージマネージャー

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
<summary><b>直接ダウンロード</b></summary>

お使いのプラットフォーム用の最新リリースをダウンロード：

| プラットフォーム | ダウンロード |
|------------------|--------------|
| Linux x86_64 | [mem-linux-x86_64.tar.gz](https://github.com/memovai/memov/releases/latest/download/mem-linux-x86_64.tar.gz) |
| macOS Intel | [mem-macos-x86_64.tar.gz](https://github.com/memovai/memov/releases/latest/download/mem-macos-x86_64.tar.gz) |
| macOS Apple Silicon | [mem-macos-arm64.tar.gz](https://github.com/memovai/memov/releases/latest/download/mem-macos-arm64.tar.gz) |
| Windows x86_64 | [mem-windows-x86_64.exe.zip](https://github.com/memovai/memov/releases/latest/download/mem-windows-x86_64.exe.zip) |

</details>

<details>
<summary><b>ソースから</b></summary>

Python 3.10+ と [uv](https://github.com/astral-sh/uv) が必要：

```bash
git clone https://github.com/memovai/memov.git
cd memov
uv sync
uv pip install -e .
mem --help
```

</details>

## コントリビューター向けインストール

詳細なインストール手順は [docs/installation_for_dev.md](../installation_for_dev.md) をご覧ください。

## アーキテクチャ

MemoVは3層アーキテクチャを採用しています。MemovManagerを中央オーケストレーターとし、MCPサーバーをAIエージェントのアダプターレイヤーとして、オプションのRAGシステムでセマンティック検索を提供します。

![MemoV アーキテクチャ](../images/Arc.png)

<details>
<summary><b>MCPツール</b></summary>

### コア操作

- `snap(user_prompt: str, original_response: str, agent_plan: list[str], files_changed: str)`
  - 自動ファイル追跡で全ユーザーインタラクションを記録。未追跡vs変更済みファイルをインテリジェントに処理。

- `mem_ui(port: int = 38888)`
  - `http://localhost:38888` でWeb UIを起動。履歴の視覚的ブラウズ、差分表示、任意のスナップショットへジャンプ。

- `mem_history(limit: int = 20, commit_hash: str = "")`
  - プロンプト、レスポンス、ファイル変更を含むmemov履歴を表示。

- `mem_jump(commit_hash: str)`
  - 特定のスナップショットにジャンプし、追跡されているすべてのファイルを復元して新しいブランチを作成。

### RAGツール（`[rag]` エクストラが必要）

これらのツールは `[rag]` エクストラでインストールした場合のみ利用可能。

- `mem_sync()`
  - 保留中のすべての操作をVectorDBに同期し、セマンティック検索機能を有効化。

- `validate_commit(commit_hash: str, detailed: bool = True)`
  - プロンプト/レスポンスと実際のコード変更を比較して特定のコミットを検証。コンテキストドリフトとアラインメント問題を検出。

- `validate_recent(n: int = 5)`
  - 直近N件のコミットのアラインメントパターンを検証。セッションレビューと品質保証に有用。

- `vibe_debug(query: str, error_message: str = "", stack_trace: str = "", user_logs: str = "", models: str = "", n_results: int = 5)`
  - RAG検索 + マルチモデルLLM比較でデバッグ。コード履歴から関連コンテキストを検索し、複数のAIモデル（GPT-4、Claude、Gemini）を並列クエリして多様なデバッグインサイトを取得。

- `vibe_search(query: str, n_results: int = 5, content_type: str = "")`
  - LLM分析なしでコード履歴（プロンプト、レスポンス、エージェントプラン、コード変更）を高速セマンティック検索。クイックコンテキスト検索に最適。

### ヘルスチェック

- `GET /health`
  - "OK"を返す。IDE/エージェントの準備状況チェックに有用。

</details>

## ライセンス

MIT License。`LICENSE` を参照。

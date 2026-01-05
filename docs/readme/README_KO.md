<p align="center">
  <a href="https://github.com/memovai/memov">
    <img src="../images/memov-banner.png" width="800px" alt="MemoV - AI 코딩 에이전트를 위한 메모리 레이어">
  </a>
</p>

<p align="center">
  <a href="../../README.md">English</a> | <a href="README_DE.md">Deutsch</a> | <a href="README_ES.md">Español</a> | <a href="README_FR.md">Français</a> | <a href="README_JA.md">日本語</a> | <b>한국어</b> | <a href="README_PT.md">Português</a> | <a href="README_RU.md">Русский</a> | <a href="README_CN.md">中文</a>
</p>

<h4 align="center">VibeGit🤌: 프롬프트, 컨텍스트 및 코드 diff 자동 추적</h4>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da?logo=discord&logoColor=white)](https://discord.gg/un54aD7Hug)
[![DeepWiki](https://img.shields.io/badge/DeepWiki-memovai%2Fmemov-blue.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNNCAxOWguNmMuNC0uMi44LS41IDEuMi0uOCAyLjItMS42IDMuNy0zLjggNC4yLTYuMyIvPjxwYXRoIGQ9Ik0xNC42IDEyLjFjLjYtLjkgMS4zLTEuOCAyLjEtMi42IDEuMS0xLjEgMi40LTEuOCAzLjgtMi4yIDEuMS0uMyAyLjItLjQgMy4zLS4zIi8+PHBhdGggZD0iTTE5LjQgNS4yYy0uOC4xLTEuNi4zLTIuMy41LS41LjItLjkuNC0xLjQuNy0uNC4zLS44LjYtMS4xIDEiLz48cGF0aCBkPSJNNiAxOGMtMS44IDAtMy0xLjUtMy0zIDAtMi4yIDEuOS0zLjUgMi44LTUgLjUtLjggMS45LTIuNyAyLjMtMy43LjYtMS4yIDEuMi0yLjQgMS42LTMuNi4xLS40LjUtLjkuOS0uOS43IDAgLjggMS4yLjggMS4zIDAgMS40LS4zIDIuOC0uNyA0LjEtLjQgMS41LTEuMSAyLjktMS44IDQuMyIvPjwvc3ZnPg==)](https://deepwiki.com/memovai/memov)
[![Twitter Follow](https://img.shields.io/twitter/follow/ssslvky?style=social)](https://x.com/ssslvky)

</div>

MemoV는 AI 코딩 에이전트를 위한 메모리 레이어로, 프롬프트, 컨텍스트 및 코드 diff에 대한 **추적 가능한** **Git 기반** 버전 관리를 제공합니다. **VibeGit**을 구현합니다 - 브랜치 탐색, 롤백 기능을 갖춘 AI 코딩 세션의 자동 버전 관리와 표준 .git 저장소에 대한 **제로 오염**.

<div align="center">

| MemoV | Checkpoints |
|-------|-------------|
| 브랜치 탐색 | 선형 타임라인 |
| 크로스 세션 | 세션 한정 |
| 롤백 시 모든 기록 유지 | 롤백 시 기록 삭제 |
| 모든 점프 추적 | 궤적 없음 |

</div>

- 💬 [Discord에 참여](https://discord.gg/un54aD7Hug)하여 더 스마트한 바이브 엔지니어링을 탐험하세요

## 기능

- **원클릭 MCP** — 모든 AI 코딩 에이전트와 호환
- **에이전트용 VibeGit** — 수동 커밋 없이 프롬프트, 컨텍스트, 코드 diff 자동 추적
- **버전 관리** — 브랜치, 롤백, 모든 인터랙션 리플레이
- **Git 깨끗하게 유지** — 섀도우 `.mem` 타임라인, `.git`에 제로 오염
- **비주얼 UI** — 채팅에서 "mem ui"라고 말하면 http://localhost:38888에서 확인
- **프라이버시 우선** — 로컬, 데이터베이스 없음, 오버헤드 없음. .memignore로 제외

## 빠른 시작 (MCP 설치)

### 사전 요구 사항

먼저 `uv` 설치:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Git 설치 (설치되지 않은 경우)
winget install --id Git.Git -e --source winget
```

### Claude Code

프로젝트 루트 디렉토리에서 실행:

```bash
claude mcp add mem-mcp --scope project -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
```

### Codex

프로젝트 루트 디렉토리에서 실행:

```bash
codex mcp add mem-mcp -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
```

<details>
<summary><b>VS Code</b></summary>

프로젝트 루트에 `.vscode/mcp.json` 생성:

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

**Files > Preferences > Cursor Settings > MCP**로 이동하여 추가:

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
<summary><b>VectorDB 포함 (RAG 모드)</b> 🚧 WIP</summary>

시맨틱 검색, 검증 및 디버깅 도구를 활성화하려면 `[rag]` 추가 옵션으로 설치:

**Claude Code:**
```bash
claude mcp add mem-mcp --scope project -- uvx --from "git+https://github.com/memovai/memov.git[rag]" mem-mcp-launcher stdio $(pwd)
```

**VS Code / Cursor:** `--from` 인수를 다음으로 변경:
```
"git+https://github.com/memovai/memov.git[rag]"
```

</details>

### 중요한 팁

**규칙 추가** — 각 인터랙션 후 자동으로 스냅샷을 저장하려면 코딩 에이전트에 규칙 추가:

- **Cursor**: Cursor Settings > Rules
- **Claude Code**: `CLAUDE.md`
- 또는 MCP 클라이언트의 동등한 설정

규칙 예시:

```
After completing any interaction, always call `use mem snap` to save the snapshot.
```

## Web UI, Use mem ui라고만 말하세요🤌

채팅에서 **"use mem ui"**라고 말하면 — `http://localhost:38888`에서 타임라인 뷰, 브랜치 필터링, diff 뷰어, 모든 스냅샷으로 점프 기능이 열립니다.

## CLI 설치 (선택사항)

`mem` CLI 도구를 직접 사용하려면:

### 원라인 설치

```bash
curl -fsSL https://raw.githubusercontent.com/memovai/memov/main/install.sh | bash
```

## 아키텍처

MemoV는 MemovManager를 중앙 오케스트레이터로, MCP 서버를 AI 에이전트용 어댑터 레이어로, 시맨틱 검색을 위한 선택적 RAG 시스템으로 구성된 3계층 아키텍처를 따릅니다.

![MemoV 아키텍처](../images/Arc.png)

<details>
<summary><b>MCP 도구</b></summary>

### 핵심 작업

- `snap()` - 모든 사용자 인터랙션 기록
- `mem_ui()` - Web UI 실행
- `mem_history()` - 기록 보기
- `mem_jump()` - 스냅샷으로 점프

### RAG 도구 (`[rag]` 추가 옵션 필요)

- `mem_sync()` - VectorDB와 동기화
- `validate_commit()` - 커밋 검증
- `vibe_debug()` - RAG 검색으로 디버깅
- `vibe_search()` - 시맨틱 검색

</details>

## 라이선스

MIT 라이선스. `LICENSE` 참조.

<p align="center">
  <a href="https://github.com/memovai/memov">
    <img src="../images/memov-banner.png" width="800px" alt="MemoV - Die Speicherschicht für KI-Coding-Agenten">
  </a>
</p>

<p align="center">
  <a href="../../README.md">English</a> | <b>Deutsch</b> | <a href="README_ES.md">Español</a> | <a href="README_FR.md">Français</a> | <a href="README_JA.md">日本語</a> | <a href="README_KO.md">한국어</a> | <a href="README_PT.md">Português</a> | <a href="README_RU.md">Русский</a> | <a href="README_CN.md">中文</a>
</p>

<h4 align="center">VibeGit🤌: Automatische Verfolgung von Prompts, Kontext & Code-Diffs</h4>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da?logo=discord&logoColor=white)](https://discord.gg/un54aD7Hug)
[![DeepWiki](https://img.shields.io/badge/DeepWiki-memovai%2Fmemov-blue.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNNCAxOWguNmMuNC0uMi44LS41IDEuMi0uOCAyLjItMS42IDMuNy0zLjggNC4yLTYuMyIvPjxwYXRoIGQ9Ik0xNC42IDEyLjFjLjYtLjkgMS4zLTEuOCAyLjEtMi42IDEuMS0xLjEgMi40LTEuOCAzLjgtMi4yIDEuMS0uMyAyLjItLjQgMy4zLS4zIi8+PHBhdGggZD0iTTE5LjQgNS4yYy0uOC4xLTEuNi4zLTIuMy41LS41LjItLjkuNC0xLjQuNy0uNC4zLS44LjYtMS4xIDEiLz48cGF0aCBkPSJNNiAxOGMtMS44IDAtMy0xLjUtMy0zIDAtMi4yIDEuOS0zLjUgMi44LTUgLjUtLjggMS45LTIuNyAyLjMtMy43LjYtMS4yIDEuMi0yLjQgMS42LTMuNi4xLS40LjUtLjkuOS0uOS43IDAgLjggMS4yLjggMS4zIDAgMS40LS4zIDIuOC0uNyA0LjEtLjQgMS41LTEuMSAyLjktMS44IDQuMyIvPjwvc3ZnPg==)](https://deepwiki.com/memovai/memov)
[![Twitter Follow](https://img.shields.io/twitter/follow/ssslvky?style=social)](https://x.com/ssslvky)

</div>

MemoV ist eine Speicherschicht für KI-Coding-Agenten, die **nachverfolgbare**, **Git-gesteuerte** Versionskontrolle für Prompts, Kontext und Code-Diffs bietet. Es ermöglicht **VibeGit** - automatische Versionierung von KI-Coding-Sitzungen mit Branch-Erkundung, Rollback-Funktionen und **null Verschmutzung** des Standard-.git-Repositorys.

<div align="center">

| MemoV | Checkpoints |
|-------|-------------|
| Branch-Erkundung | Lineare Zeitachse |
| Sitzungsübergreifend | Sitzungsgebunden |
| Rollback behält alles | Rollback löscht Verlauf |
| Jeder Sprung wird verfolgt | Keine Trajektorie |

</div>

![MemoV Time](../images/ALL.png)
- 💬 [Tritt unserem Discord bei](https://discord.gg/un54aD7Hug) und tauche in smarteres Vibe-Engineering ein

## Funktionen

- **Ein-Klick-MCP** — Funktioniert mit jedem KI-Coding-Agenten
- **VibeGit für Agenten** — Automatische Verfolgung von Prompts, Kontext und Code-Diffs ohne manuelle Commits
- **Versionskontrolle** — Branch, Rollback, Replay jeder Interaktion
- **Git sauber halten** — Schatten `.mem` Zeitachse, null Verschmutzung von `.git`
- **Visuelle UI** — Sag "mem ui" im Chat, und sieh es unter http://localhost:38888
- **Privatsphäre zuerst** — Lokal, keine Datenbank, kein Overhead. Nutze .memignore zum Ausschließen


![MemoV Time](../images/one.png)
## Schnellstart (MCP-Installation)

### Voraussetzungen

Installiere zuerst `uv`:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Git installieren (falls nicht installiert)
winget install --id Git.Git -e --source winget
```

### Claude Code

Im Projektstammverzeichnis ausführen:

```bash
claude mcp add mem-mcp --scope project -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
```

### Codex

Im Projektstammverzeichnis ausführen:

```bash
codex mcp add mem-mcp -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
```

<details>
<summary><b>VS Code</b></summary>

Erstelle `.vscode/mcp.json` im Projektstamm:

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

Gehe zu **Files > Preferences > Cursor Settings > MCP** und füge hinzu:

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
<summary><b>Antigravity</b></summary>

> **Hinweis:** Antigravity unterstützt die Variable "${workspaceFolder}" nicht. Bitte gib den absoluten Pfad deines Projektverzeichnisses manuell ein.

Gehe zu **Settings > MCP** und füge hinzu:

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

Ersetze `/absolute/path/to/your/project` durch den tatsächlichen absoluten Pfad deines Projektverzeichnisses (z.B. `/Users/username/projects/my-project` unter macOS/Linux oder `C:\Users\username\projects\my-project` unter Windows).

</details>


<details>
<summary><b>Mit VectorDB (RAG-Modus)</b> 🚧 WIP</summary>

Um semantische Suche, Validierung und Debugging-Tools zu aktivieren, installiere mit `[rag]` Extras:

**Claude Code:**
```bash
claude mcp add mem-mcp --scope project -- uvx --from "git+https://github.com/memovai/memov.git[rag]" mem-mcp-launcher stdio $(pwd)
```

**VS Code / Cursor:** Ändere das `--from` Argument zu:
```
"git+https://github.com/memovai/memov.git[rag]"
```

</details>

### Wichtige Tipps

**Regel hinzufügen** — Um Snapshots nach jeder Interaktion automatisch zu speichern, füge eine Regel zu deinen Coding-Agenten hinzu:

- **Cursor**: Cursor Settings > Rules
- **Claude Code**: `CLAUDE.md`
- Oder das Äquivalent in deinem MCP-Client

Beispielregel:

```
After completing any interaction, always call `use mem snap` to save the snapshot.
```

## Web UI, Sag einfach Use mem ui🤌

Sag einfach **"use mem ui"** im Chat — öffnet unter `http://localhost:38888` mit Zeitachsenansicht, Branch-Filterung, Diff-Viewer und Sprung zu jedem Snapshot.

## CLI-Installation (Optional)

Wenn du das `mem` CLI-Tool direkt nutzen möchtest (für manuelles Tracking, Verlaufsanzeige, etc.):

### Ein-Zeilen-Installation

```bash
curl -fsSL https://raw.githubusercontent.com/memovai/memov/main/install.sh | bash
```

Oder mit wget:

```bash
wget -qO- https://raw.githubusercontent.com/memovai/memov/main/install.sh | bash
```

## Architektur

MemoV folgt einer dreistufigen Architektur mit MemovManager als zentralem Orchestrator, dem MCP-Server als Adapterschicht für KI-Agenten und einem optionalen RAG-System für semantische Suche.

![MemoV Architektur](../images/Arc.png)

<details>
<summary><b>MCP-Tools</b></summary>

### Kernoperationen

- `snap(user_prompt: str, original_response: str, agent_plan: list[str], files_changed: str)`
  - Zeichnet jede Benutzerinteraktion mit automatischer Dateiverfolgung auf.

- `mem_ui(port: int = 38888)`
  - Startet die Web-UI unter `http://localhost:38888`.

- `mem_history(limit: int = 20, commit_hash: str = "")`
  - Zeigt memov-Verlauf mit Prompts, Antworten und Dateiänderungen.

- `mem_jump(commit_hash: str)`
  - Springt zu einem bestimmten Snapshot.

### RAG-Tools (erfordert `[rag]` Extras)

- `mem_sync()` - Synchronisiert mit VectorDB
- `validate_commit()` - Validiert Commits
- `vibe_debug()` - Debugging mit RAG-Suche
- `vibe_search()` - Semantische Suche

</details>

## Lizenz

MIT-Lizenz. Siehe `LICENSE`.

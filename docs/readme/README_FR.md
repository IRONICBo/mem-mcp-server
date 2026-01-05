<p align="center">
  <a href="https://github.com/memovai/memov">
    <img src="../images/memov-banner.png" width="800px" alt="MemoV - La Couche Mémoire pour les Agents de Codage IA">
  </a>
</p>

<p align="center">
  <a href="../../README.md">English</a> | <a href="README_DE.md">Deutsch</a> | <a href="README_ES.md">Español</a> | <b>Français</b> | <a href="README_JA.md">日本語</a> | <a href="README_KO.md">한국어</a> | <a href="README_PT.md">Português</a> | <a href="README_RU.md">Русский</a> | <a href="README_CN.md">中文</a>
</p>

<h4 align="center">VibeGit🤌: Suivi automatique de vos prompts, contexte et diffs de code</h4>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da?logo=discord&logoColor=white)](https://discord.gg/un54aD7Hug)
[![DeepWiki](https://img.shields.io/badge/DeepWiki-memovai%2Fmemov-blue.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNNCAxOWguNmMuNC0uMi44LS41IDEuMi0uOCAyLjItMS42IDMuNy0zLjggNC4yLTYuMyIvPjxwYXRoIGQ9Ik0xNC42IDEyLjFjLjYtLjkgMS4zLTEuOCAyLjEtMi42IDEuMS0xLjEgMi40LTEuOCAzLjgtMi4yIDEuMS0uMyAyLjItLjQgMy4zLS4zIi8+PHBhdGggZD0iTTE5LjQgNS4yYy0uOC4xLTEuNi4zLTIuMy41LS41LjItLjkuNC0xLjQuNy0uNC4zLS44LjYtMS4xIDEiLz48cGF0aCBkPSJNNiAxOGMtMS44IDAtMy0xLjUtMy0zIDAtMi4yIDEuOS0zLjUgMi44LTUgLjUtLjggMS45LTIuNyAyLjMtMy43LjYtMS4yIDEuMi0yLjQgMS42LTMuNi4xLS40LjUtLjkuOS0uOS43IDAgLjggMS4yLjggMS4zIDAgMS40LS4zIDIuOC0uNyA0LjEtLjQgMS41LTEuMSAyLjktMS44IDQuMyIvPjwvc3ZnPg==)](https://deepwiki.com/memovai/memov)
[![Twitter Follow](https://img.shields.io/twitter/follow/ssslvky?style=social)](https://x.com/ssslvky)

</div>

MemoV est une couche mémoire pour les agents de codage IA qui fournit un contrôle de version **traçable** et **basé sur Git** pour les prompts, le contexte et les diffs de code. Il permet **VibeGit** - versioning automatique des sessions de codage IA avec exploration de branches, capacités de rollback et **zéro pollution** du dépôt .git standard.

<div align="center">

| MemoV | Checkpoints |
|-------|-------------|
| Exploration de branches | Ligne temporelle linéaire |
| Inter-sessions | Limité à la session |
| Rollback préserve tout | Rollback efface l'historique |
| Chaque saut tracé | Pas de trajectoire |

</div>

- 💬 [Rejoignez notre Discord](https://discord.gg/un54aD7Hug) et plongez dans l'ingénierie vibe plus intelligente

## Fonctionnalités

- **MCP en un clic** — Fonctionne avec tout agent de codage IA
- **VibeGit pour Agents** — Suivi automatique des prompts, contexte et diffs sans commits manuels
- **Contrôle de version** — Branchez, revenez en arrière, rejouez toute interaction
- **Gardez Git propre** — Ligne temporelle fantôme `.mem`, zéro pollution de `.git`
- **UI Visuelle** — Dites "mem ui" dans le chat, et voyez sur http://localhost:38888
- **Vie privée d'abord** — Local, pas de base de données, pas d'overhead. Utilisez .memignore pour exclure

## Démarrage Rapide (Installation MCP)

### Prérequis

Installez `uv` d'abord:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Claude Code

Exécutez dans le répertoire racine de votre projet:

```bash
claude mcp add mem-mcp --scope project -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
```

### Codex

Exécutez dans le répertoire racine de votre projet:

```bash
codex mcp add mem-mcp -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
```

<details>
<summary><b>VS Code</b></summary>

Créez `.vscode/mcp.json` à la racine de votre projet:

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

Allez dans **Files > Preferences > Cursor Settings > MCP**, puis ajoutez:

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
<summary><b>Avec VectorDB (mode RAG)</b> 🚧 WIP</summary>

Pour activer la recherche sémantique, la validation et les outils de débogage, installez avec les extras `[rag]`:

**Claude Code:**
```bash
claude mcp add mem-mcp --scope project -- uvx --from "git+https://github.com/memovai/memov.git[rag]" mem-mcp-launcher stdio $(pwd)
```

**VS Code / Cursor:** Changez l'argument `--from` en:
```
"git+https://github.com/memovai/memov.git[rag]"
```

</details>

### Conseils Importants

**Ajouter une Règle** — Pour sauvegarder automatiquement les snapshots après chaque interaction, ajoutez une règle à vos agents de codage:

- **Cursor**: Cursor Settings > Rules
- **Claude Code**: `CLAUDE.md`
- Ou l'équivalent dans votre client MCP

Exemple de règle:

```
After completing any interaction, always call `use mem snap` to save the snapshot.
```

## Web UI, Dites simplement Use mem ui🤌

Dites simplement **"use mem ui"** dans le chat — ouvre à `http://localhost:38888` avec vue chronologique, filtrage de branches, visualiseur de diffs et saut vers n'importe quel snapshot.

## Installation CLI (Optionnel)

Si vous voulez utiliser l'outil CLI `mem` directement:

### Installation en une ligne

```bash
curl -fsSL https://raw.githubusercontent.com/memovai/memov/main/install.sh | bash
```

## Architecture

MemoV suit une architecture à trois niveaux avec MemovManager comme orchestrateur central, le serveur MCP comme couche d'adaptation pour les agents IA et un système RAG optionnel pour la recherche sémantique.

![Architecture MemoV](../images/Arc.png)

<details>
<summary><b>Outils MCP</b></summary>

### Opérations Principales

- `snap()` - Enregistre chaque interaction utilisateur
- `mem_ui()` - Lance l'UI Web
- `mem_history()` - Voir l'historique
- `mem_jump()` - Sauter à un snapshot

### Outils RAG (nécessite les extras `[rag]`)

- `mem_sync()` - Synchroniser avec VectorDB
- `validate_commit()` - Valider les commits
- `vibe_debug()` - Débogage avec recherche RAG
- `vibe_search()` - Recherche sémantique

</details>

## Licence

Licence MIT. Voir `LICENSE`.

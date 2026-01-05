<p align="center">
  <a href="https://github.com/memovai/memov">
    <img src="../images/memov-banner.png" width="800px" alt="MemoV - La Capa de Memoria para Agentes de Codificación IA">
  </a>
</p>

<p align="center">
  <a href="../../README.md">English</a> | <a href="README_DE.md">Deutsch</a> | <b>Español</b> | <a href="README_FR.md">Français</a> | <a href="README_JA.md">日本語</a> | <a href="README_KO.md">한국어</a> | <a href="README_PT.md">Português</a> | <a href="README_RU.md">Русский</a> | <a href="README_CN.md">中文</a>
</p>

<h4 align="center">VibeGit🤌: Seguimiento automático de prompts, contexto y diffs de código</h4>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Discord](https://img.shields.io/badge/Discord-Join%20Server-7289da?logo=discord&logoColor=white)](https://discord.gg/un54aD7Hug)
[![DeepWiki](https://img.shields.io/badge/DeepWiki-memovai%2Fmemov-blue.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNNCAxOWguNmMuNC0uMi44LS41IDEuMi0uOCAyLjItMS42IDMuNy0zLjggNC4yLTYuMyIvPjxwYXRoIGQ9Ik0xNC42IDEyLjFjLjYtLjkgMS4zLTEuOCAyLjEtMi42IDEuMS0xLjEgMi40LTEuOCAzLjgtMi4yIDEuMS0uMyAyLjItLjQgMy4zLS4zIi8+PHBhdGggZD0iTTE5LjQgNS4yYy0uOC4xLTEuNi4zLTIuMy41LS41LjItLjkuNC0xLjQuNy0uNC4zLS44LjYtMS4xIDEiLz48cGF0aCBkPSJNNiAxOGMtMS44IDAtMy0xLjUtMy0zIDAtMi4yIDEuOS0zLjUgMi44LTUgLjUtLjggMS45LTIuNyAyLjMtMy43LjYtMS4yIDEuMi0yLjQgMS42LTMuNi4xLS40LjUtLjkuOS0uOS43IDAgLjggMS4yLjggMS4zIDAgMS40LS4zIDIuOC0uNyA0LjEtLjQgMS41LTEuMSAyLjktMS44IDQuMyIvPjwvc3ZnPg==)](https://deepwiki.com/memovai/memov)
[![Twitter Follow](https://img.shields.io/twitter/follow/ssslvky?style=social)](https://x.com/ssslvky)

</div>

MemoV es una capa de memoria para agentes de codificación IA que proporciona control de versiones **rastreable** y **basado en Git** para prompts, contexto y diffs de código. Habilita **VibeGit** - versionado automático de sesiones de codificación IA con exploración de ramas, capacidades de rollback y **cero contaminación** del repositorio .git estándar.

<div align="center">

| MemoV | Checkpoints |
|-------|-------------|
| Exploración de ramas | Línea temporal lineal |
| Entre sesiones | Limitado a sesión |
| Rollback preserva todo | Rollback borra historial |
| Cada salto rastreado | Sin trayectoria |

</div>

- 💬 [Únete a nuestro Discord](https://discord.gg/un54aD7Hug) y sumérgete en ingeniería vibe más inteligente

## Características

- **MCP de un clic** — Funciona con cualquier agente de codificación IA
- **VibeGit para Agentes** — Seguimiento automático de prompts, contexto y diffs sin commits manuales
- **Control de versiones** — Ramifica, revierte, reproduce cualquier interacción
- **Mantén Git limpio** — Línea temporal sombra `.mem`, cero contaminación en `.git`
- **UI Visual** — Di "mem ui" en el chat, y mira en http://localhost:38888
- **Privacidad primero** — Local, sin base de datos, sin overhead. Usa .memignore para excluir

## Inicio Rápido (Instalación MCP)

### Prerrequisitos

Instala `uv` primero:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Claude Code

Ejecuta en el directorio raíz de tu proyecto:

```bash
claude mcp add mem-mcp --scope project -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
```

### Codex

Ejecuta en el directorio raíz de tu proyecto:

```bash
codex mcp add mem-mcp -- uvx --from git+https://github.com/memovai/memov.git mem-mcp-launcher stdio $(pwd)
```

<details>
<summary><b>VS Code</b></summary>

Crea `.vscode/mcp.json` en la raíz de tu proyecto:

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

Ve a **Files > Preferences > Cursor Settings > MCP**, luego añade:

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
<summary><b>Con VectorDB (modo RAG)</b> 🚧 WIP</summary>

Para habilitar búsqueda semántica, validación y herramientas de depuración, instala con extras `[rag]`:

**Claude Code:**
```bash
claude mcp add mem-mcp --scope project -- uvx --from "git+https://github.com/memovai/memov.git[rag]" mem-mcp-launcher stdio $(pwd)
```

**VS Code / Cursor:** Cambia el argumento `--from` a:
```
"git+https://github.com/memovai/memov.git[rag]"
```

</details>

### Consejos Importantes

**Añadir una Regla** — Para guardar snapshots automáticamente después de cada interacción, añade una regla a tus agentes de codificación:

- **Cursor**: Cursor Settings > Rules
- **Claude Code**: `CLAUDE.md`
- O el equivalente en tu cliente MCP

Regla de ejemplo:

```
After completing any interaction, always call `use mem snap` to save the snapshot.
```

## Web UI, Solo di Use mem ui🤌

Solo di **"use mem ui"** en el chat — abre en `http://localhost:38888` con vista de línea temporal, filtrado de ramas, visor de diffs y salto a cualquier snapshot.

## Instalación CLI (Opcional)

Si quieres usar la herramienta CLI `mem` directamente:

### Instalación de una línea

```bash
curl -fsSL https://raw.githubusercontent.com/memovai/memov/main/install.sh | bash
```

## Arquitectura

MemoV sigue una arquitectura de tres niveles con MemovManager como orquestador central, el servidor MCP como capa adaptadora para agentes IA y un sistema RAG opcional para búsqueda semántica.

![Arquitectura MemoV](../images/Arc.png)

<details>
<summary><b>Herramientas MCP</b></summary>

### Operaciones Principales

- `snap()` - Registra cada interacción de usuario
- `mem_ui()` - Lanza la Web UI
- `mem_history()` - Ver historial
- `mem_jump()` - Saltar a un snapshot

### Herramientas RAG (requiere extras `[rag]`)

- `mem_sync()` - Sincronizar con VectorDB
- `validate_commit()` - Validar commits
- `vibe_debug()` - Depuración con búsqueda RAG
- `vibe_search()` - Búsqueda semántica

</details>

## Licencia

Licencia MIT. Ver `LICENSE`.

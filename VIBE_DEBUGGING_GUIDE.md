# VIBE Debugging Guide

**VIBE (Vector-Indexed Behavior Exploration) Debugging** combines RAG (Retrieval Augmented Generation) with multi-model LLM comparison to provide comprehensive code debugging insights.

## 🎯 Overview

VIBE debugging provides three powerful capabilities:

1. **RAG Search**: Semantic search through your code history to find relevant context
2. **Multi-Model Analysis**: Query multiple AI models (GPT-4, Claude, Gemini) simultaneously for diverse insights
3. **Context-Aware Debugging**: Combines error traces, logs, and historical code changes for comprehensive analysis

## 📋 Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage Methods](#usage-methods)
  - [Method 1: MCP Tools](#method-1-mcp-tools-claude-code-integration)
  - [Method 2: CLI Tool](#method-2-cli-tool)
- [Features](#features)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Installation

### 1. Install Dependencies

```bash
# Install the package with debugging support
cd /path/to/mem-mcp-server
pip install -e .

# Or install litellm separately if needed
pip install litellm
```

### 2. Configure API Keys

Set environment variables for the AI models you want to use:

```bash
# OpenAI (GPT models)
export OPENAI_API_KEY="your-openai-api-key"

# Anthropic (Claude models)
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Google (Gemini models)
export GEMINI_API_KEY="your-google-api-key"
# OR
export GOOGLE_API_KEY="your-google-api-key"

# Optional: Other providers
export COHERE_API_KEY="your-cohere-api-key"
export MISTRAL_API_KEY="your-mistral-api-key"
```

**Note**: You need at least one API key configured to use multi-model debugging.

---

## ⚙️ Setup

### 1. Initialize Memov in Your Project

```bash
cd /path/to/your/project
mem init
```

### 2. Track Files and Create Snapshots

```bash
# Track files
mem track src/main.py

# Create snapshots as you work
mem snap
```

### 3. Sync to VectorDB

**Critical**: You must sync your changes to the VectorDB for RAG search to work:

```bash
mem sync
```

This indexes your code changes, prompts, and responses for semantic search.

### 4. Verify Setup

```bash
# Using CLI
mem-debug setup

# Check VectorDB status
mem status
```

---

## 🛠️ Usage Methods

### Method 1: MCP Tools (Claude Code Integration)

If you're using Claude Code or another MCP-compatible client, VIBE debugging is available as MCP tools.

#### Tool 1: `vibe_debug` - Full Debugging Analysis

```python
# Example MCP tool call
vibe_debug(
    query="Why is the login endpoint returning 500 errors?",
    error_message="Internal Server Error: Database connection timeout",
    stack_trace="""
    File "app/routes/auth.py", line 45, in login
        user = db.query(User).filter_by(email=email).first()
    File "db/connection.py", line 23, in query
        raise TimeoutError("Database connection timeout")
    """,
    user_logs="[ERROR] Connection pool exhausted after 5.2s",
    models="gpt-4o-mini,claude-3-5-sonnet-20241022",
    n_results=5
)
```

**Parameters**:
- `query` (required): Main debug question
- `error_message` (optional): Error message text
- `stack_trace` (optional): Full stack trace
- `user_logs` (optional): Relevant log output
- `models` (optional): Comma-separated model names (default: GPT-4o-mini, Claude Sonnet, Gemini Flash)
- `n_results` (optional): Number of relevant code snippets to retrieve (default: 5)

**Returns**: Comprehensive debugging report with:
- RAG-retrieved relevant code context
- Analysis from each LLM model
- Consensus recommendations
- Specific fix suggestions

#### Tool 2: `vibe_search` - Quick RAG Search

```python
# Fast semantic search without LLM analysis
vibe_search(
    query="authentication implementation",
    n_results=10,
    content_type="agent_plan"  # or "prompt", "response", ""
)
```

**Parameters**:
- `query` (required): Search query
- `n_results` (optional): Number of results (default: 5, max: 20)
- `content_type` (optional): Filter by "prompt", "response", "agent_plan", or "" for all

---

### Method 2: CLI Tool

The `mem-debug` CLI provides standalone debugging capabilities.

#### Command 1: `search` - RAG Search

Search your code history semantically:

```bash
# Basic search
mem-debug search "authentication logic"

# With options
mem-debug search "database queries" --limit 10 --type agent_plan

# Filter by content type
mem-debug search "API error handling" --type response
```

**Options**:
- `--limit, -n`: Number of results (default: 5)
- `--type, -t`: Filter by content type (prompt, response, agent_plan)
- `--path, -p`: Project path (default: current directory)

#### Command 2: `analyze` - Multi-Model Debugging

Analyze issues using multiple AI models:

```bash
# Basic analysis
mem-debug analyze "Why is the API slow?"

# With error context
mem-debug analyze "Login fails" \
    --error "Invalid credentials" \
    --trace "$(cat error.log)"

# Custom models
mem-debug analyze "Memory leak in worker process" \
    --models "gpt-4o,claude-3-5-sonnet-20241022,gemini/gemini-1.5-pro" \
    --context 10

# With logs
mem-debug analyze "Database connection issues" \
    --logs "$(tail -n 50 app.log)"
```

**Options**:
- `--error, -e`: Error message
- `--trace, -t`: Stack trace
- `--logs, -l`: User logs
- `--models, -m`: Comma-separated model names
- `--context, -c`: Number of context snippets (default: 5)
- `--path, -p`: Project path

#### Command 3: `compare` - Side-by-Side Model Comparison

Compare responses from multiple models:

```bash
# Default models
mem-debug compare "How to optimize database queries?"

# Custom models
mem-debug compare "Best practices for error handling" \
    --models "gpt-4o,claude-3-opus-20240229,gemini/gemini-1.5-flash"
```

#### Command 4: `setup` - Check Configuration

Verify your setup:

```bash
mem-debug setup
```

This checks:
- Memov initialization
- VectorDB status
- LiteLLM installation
- API key configuration
- Available models

---

## 🎨 Features

### 1. RAG Search

**What it does**: Searches your code history using semantic similarity to find relevant:
- Previous prompts (what you asked)
- AI responses (what was done)
- Agent plans (high-level summaries)
- File changes (which files were modified)

**How it works**:
1. Your code changes are embedded into vectors using ChromaDB
2. Query is converted to a vector
3. Semantic similarity search finds the most relevant historical changes
4. Results ranked by relevance score

**Use cases**:
- "When did I implement authentication?"
- "Find all changes related to database queries"
- "Show me where error handling was added"

### 2. Multi-Model LLM Analysis

**What it does**: Queries multiple AI models in parallel for diverse debugging insights.

**Supported models**:

| Provider | Models |
|----------|--------|
| OpenAI | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-3.5-turbo` |
| Anthropic | `claude-3-5-sonnet-20241022`, `claude-3-5-haiku-20241022`, `claude-3-opus-20240229` |
| Google | `gemini/gemini-1.5-pro`, `gemini/gemini-1.5-flash`, `gemini/gemini-pro` |
| Cohere | `command-r-plus`, `command-r` |
| Mistral | `mistral/mistral-large-latest`, `mistral/mistral-medium-latest` |

**Benefits**:
- **Diverse perspectives**: Different models may identify different issues
- **Consensus building**: Common recommendations across models are likely accurate
- **Completeness**: One model might catch what another misses

### 3. Context-Aware Debugging

**What it does**: Combines multiple information sources for comprehensive analysis:

1. **Error Information**: Error messages, stack traces, exception details
2. **User Logs**: Application logs, console output, debug info
3. **Code History**: Relevant commits, file changes, previous modifications
4. **RAG Context**: Semantically similar code and issues from your history

**Workflow**:
```
Query + Error + Logs + Stack Trace
           ↓
    RAG Search (VectorDB)
           ↓
   Retrieve Relevant Context
           ↓
  Build Comprehensive Prompt
           ↓
  Query Multiple LLM Models
           ↓
 Compare & Synthesize Results
           ↓
    Actionable Recommendations
```

---

## 💡 Examples

### Example 1: Simple Error Debugging

```bash
mem-debug analyze "API endpoint returning 500" \
    --error "Internal Server Error"
```

**Output**:
```
🔍 VIBE DEBUGGING REPORT
================================================================================

Context Retrieved:
  • Relevant commits: 3
  • Error: Internal Server Error

🎯 Key Recommendations:
  1. Check database connection pool configuration
  2. Add timeout handling for database queries
  3. Implement proper error logging
  4. Add retry logic for transient failures
  5. Monitor connection pool metrics

💬 Analysis by Model:

┌─ ✓ gpt-4o-mini ────────────────────────────────────────────────────────────┐
│ Based on the context, this appears to be a database connection issue.      │
│                                                                              │
│ Root Cause:                                                                  │
│ The connection pool is likely exhausted due to:                             │
│ - Not closing connections properly                                          │
│ - Too many concurrent requests                                              │
│ - Long-running queries blocking the pool                                    │
│                                                                              │
│ Recommended Fix:                                                             │
│ ```python                                                                    │
│ # Add connection pooling config                                             │
│ from sqlalchemy.pool import QueuePool                                       │
│                                                                              │
│ engine = create_engine(                                                     │
│     DATABASE_URL,                                                           │
│     poolclass=QueuePool,                                                    │
│     pool_size=20,                                                           │
│     max_overflow=0,                                                         │
│     pool_pre_ping=True,  # Test connections before use                     │
│     pool_recycle=3600    # Recycle connections after 1 hour                │
│ )                                                                           │
│ ```                                                                         │
│                                                                              │
│ Tokens: 425 (prompt: 250, completion: 175)                                 │
└──────────────────────────────────────────────────────────────────────────┘

[Additional model responses...]
================================================================================
```

### Example 2: Performance Issue Investigation

```bash
mem-debug analyze "Database queries are slow" \
    --logs "Query took 5.2s to execute" \
    --models "gpt-4o,claude-3-5-sonnet-20241022"
```

### Example 3: Finding Historical Context

```bash
# Search for when a feature was implemented
mem-debug search "user authentication flow" --limit 10

# Find error handling patterns
mem-debug search "try catch exception" --type agent_plan

# Locate database-related changes
mem-debug search "database migration" --type response
```

### Example 4: Complex Debugging with Full Context

```bash
mem-debug analyze "Memory leak in background worker" \
    --error "MemoryError: unable to allocate array" \
    --trace "$(python -c 'import traceback; print(traceback.format_exc())')" \
    --logs "$(tail -n 100 worker.log)" \
    --models "gpt-4o,claude-3-opus-20240229" \
    --context 10
```

### Example 5: Comparing Model Responses

```bash
# Ask a general question to multiple models
mem-debug compare "What are best practices for API rate limiting?" \
    --models "gpt-4o-mini,claude-3-5-sonnet-20241022,gemini/gemini-1.5-flash"
```

---

## 🔧 Troubleshooting

### Issue: "VectorDB is empty"

**Solution**: Run `mem sync` to populate the database:
```bash
mem sync
```

### Issue: "LiteLLM not installed"

**Solution**: Install litellm:
```bash
pip install litellm
```

### Issue: "No API keys configured"

**Solution**: Set at least one API key:
```bash
export OPENAI_API_KEY="your-key"
# And/or other providers
```

### Issue: "Memov not initialized"

**Solution**: Initialize Memov in your project:
```bash
cd /path/to/your/project
mem init
```

### Issue: Model timeouts or rate limits

**Solutions**:
1. Use fewer models: `--models "gpt-4o-mini"`
2. Increase timeout: The client defaults to 60s
3. Use faster models: `gpt-4o-mini`, `claude-3-5-haiku-20241022`, `gemini-1.5-flash`
4. Check rate limits on your API accounts

### Issue: Poor search results

**Solutions**:
1. Ensure you've synced recent changes: `mem sync`
2. Increase `n_results`: `--context 10`
3. Make queries more specific: "database connection pooling" vs "database"
4. Check VectorDB has data: `mem-debug setup`

### Issue: Inconsistent model responses

**This is expected!** Different models have different strengths:
- **GPT-4**: Strong general reasoning, good for complex analysis
- **Claude**: Excellent at following instructions, detailed explanations
- **Gemini**: Fast, good at pattern recognition

Use multiple models to get diverse perspectives and identify consensus.

---

## 🎓 Best Practices

### 1. Keep VectorDB Updated

```bash
# Sync after every 3-5 changes
mem snap
mem snap
mem snap
mem sync
```

### 2. Provide Comprehensive Context

The more context you provide, the better the analysis:
```bash
mem-debug analyze "Error message" \
    --error "Full error text" \
    --trace "Complete stack trace" \
    --logs "Relevant log entries" \
    --context 10  # More context snippets
```

### 3. Use Appropriate Models

- **Fast debugging**: `gpt-4o-mini`, `claude-3-5-haiku-20241022`
- **Complex issues**: `gpt-4o`, `claude-3-5-sonnet-20241022`, `gemini-1.5-pro`
- **Cost-effective**: `gpt-4o-mini`, `gemini-1.5-flash`

### 4. Iterate on Search Queries

If initial search results aren't relevant:
```bash
# Too broad
mem-debug search "error"

# Better
mem-debug search "database connection error"

# Even more specific
mem-debug search "postgresql connection pool timeout error"
```

### 5. Compare Models for Critical Issues

For production bugs or critical issues, use multiple models:
```bash
mem-debug analyze "Production API outage" \
    --models "gpt-4o,claude-3-5-sonnet-20241022,gemini-1.5-pro" \
    --error "..." --trace "..." --logs "..."
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Query + Context                      │
│              (Error, Stack Trace, Logs, Question)               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RAG Search Layer                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  VectorDB (ChromaDB)                                      │  │
│  │  - Embedded prompts, responses, agent plans              │  │
│  │  - Semantic similarity search                            │  │
│  │  - Retrieve top-N relevant documents                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Context Builder                                │
│  Combines:                                                       │
│  - RAG search results (relevant code history)                   │
│  - Error information (messages, traces)                         │
│  - User logs (application logs, debug output)                   │
│  - Commit details (files, changes, metadata)                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Multi-Model Query Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   GPT-4o     │  │    Claude    │  │    Gemini    │         │
│  │   (OpenAI)   │  │  (Anthropic) │  │   (Google)   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                  │                  │                  │
│         └──────────────────┴──────────────────┘                 │
│                         │                                        │
│                  LiteLLM Router                                  │
│              (Parallel async queries)                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                Response Synthesizer                              │
│  - Compare model responses                                       │
│  - Extract consensus recommendations                             │
│  - Identify common themes                                        │
│  - Generate actionable insights                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Formatted Report                                │
│  - Context summary                                               │
│  - Key recommendations                                           │
│  - Individual model analyses                                     │
│  - Consensus insights                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔗 Related Documentation

- [Main README](./README.md)
- [VectorDB Implementation](./VECTORDB_IMPLEMENTATION.md)
- [VectorDB Usage](./VECTORDB_USAGE.md)
- [Debugging Validation](./DEBUGGING_VALIDATION.md)

---

## 📝 License

MIT License - See [LICENSE](./LICENSE) file for details.

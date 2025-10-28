# VIBE Debugging - README Addition

Add this section to your main README.md:

---

## 🔍 VIBE Debugging (NEW!)

**VIBE (Vector-Indexed Behavior Exploration)** combines RAG search with multi-model LLM comparison for powerful code debugging.

### Quick Example

```bash
# Search your code history
mem-debug search "authentication implementation"

# Debug with multiple AI models
mem-debug analyze "Why is login failing?" \
    --error "Invalid credentials" \
    --models "gpt-4o-mini,claude-3-5-sonnet-20241022"
```

### What You Get

🔎 **RAG Search**: Semantic search through your code history
🤖 **Multi-Model Analysis**: Query GPT-4, Claude, Gemini simultaneously
📊 **Context-Aware**: Combines errors, logs, and code history
💡 **Actionable Insights**: Specific fixes with code examples

### Features

#### 1. MCP Tools (Claude Code Integration)

```python
# Full debugging with RAG + multi-model
vibe_debug(
    query="API returning 500 errors",
    error_message="Database timeout",
    stack_trace="...",
    models="gpt-4o-mini,claude-3-5-sonnet-20241022"
)

# Quick RAG search
vibe_search(
    query="authentication",
    n_results=10
)
```

#### 2. CLI Tool

```bash
# Search
mem-debug search "query" [--limit N] [--type TYPE]

# Analyze
mem-debug analyze "question" [--error TEXT] [--trace TEXT] \
    [--logs TEXT] [--models LIST] [--context N]

# Compare models
mem-debug compare "question" [--models LIST]

# Check setup
mem-debug setup
```

### Supported Models

| Provider | Models |
|----------|--------|
| OpenAI | GPT-4o, GPT-4o-mini, GPT-4-turbo |
| Anthropic | Claude 3.5 Sonnet, Claude 3.5 Haiku |
| Google | Gemini 1.5 Pro, Gemini 1.5 Flash |
| Cohere | Command R+, Command R |
| Mistral | Mistral Large, Mistral Medium |

### Quick Start

```bash
# 1. Install
pip install -e .

# 2. Configure API keys
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"  # Optional
export GEMINI_API_KEY="your-key"    # Optional

# 3. Initialize & sync
mem init
mem sync

# 4. Start debugging
mem-debug analyze "your question"
```

### Documentation

- **📚 [Full Guide](./VIBE_DEBUGGING_GUIDE.md)** - Comprehensive documentation
- **⚡ [Quick Start](./VIBE_DEBUGGING_QUICKSTART.md)** - Get started in 5 minutes
- **🎨 [Demo Page](./vibe-debugging-demo.html)** - Interactive demo
- **📊 [Implementation](./VIBE_DEBUGGING_IMPLEMENTATION_SUMMARY.md)** - Technical details

### Example Output

```
🔍 VIBE DEBUGGING REPORT
================================================================================

Context Retrieved:
  • Relevant commits: 3
  • Error: Database connection timeout

🎯 Key Recommendations:
  1. Check database connection pool configuration
  2. Add timeout handling for database queries
  3. Implement proper error logging
  4. Add retry logic for transient failures

💬 Analysis by Model:

✓ gpt-4o-mini:
Root cause: Connection pool exhausted...
[Detailed analysis with code examples]

✓ claude-3-5-sonnet-20241022:
Database connection issues detected...
[Alternative perspective and solutions]

✓ gemini/gemini-1.5-flash:
Pattern suggests resource exhaustion...
[Third opinion and recommendations]
================================================================================
```

### Architecture

```
Query + Error → RAG Search → Context Building → Multi-Model Query → Synthesis
    ↓             ↓              ↓                    ↓               ↓
User Input    VectorDB    Error+Logs+History    GPT/Claude/Gemini  Report
```

### Use Cases

✅ Debug runtime errors and exceptions
✅ Find when features were implemented
✅ Understand legacy code
✅ Get multiple AI perspectives
✅ Compare debugging approaches
✅ Track down regression causes

### Requirements

- **VectorDB populated**: Run `mem sync` after changes
- **API keys**: At least one LLM provider configured
- **LiteLLM**: Installed via dependencies

### Tips

💡 Run `mem sync` regularly to keep RAG search updated
💡 Use multiple models for critical production bugs
💡 Provide error context for better results
💡 Start with specific queries, not broad searches

---

## Installation

```bash
# Install with VIBE debugging support
pip install -e .

# Or install litellm separately
pip install litellm
```

## Configuration

```bash
# Set API keys (at least one required for VIBE debugging)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."
```

---

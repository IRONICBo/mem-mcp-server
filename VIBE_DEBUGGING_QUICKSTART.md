# VIBE Debugging Quick Start Guide

Get started with VIBE debugging in 5 minutes! This guide will help you set up and use RAG-based debugging with multi-model LLM comparison.

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Dependencies

```bash
cd /path/to/mem-mcp-server
pip install -e .
```

This installs:
- ✅ Memov core
- ✅ ChromaDB for vector storage
- ✅ LiteLLM for multi-model querying
- ✅ CLI tools

### Step 2: Configure API Keys

Set at least one API key (you can use multiple):

```bash
# OpenAI (GPT models) - Recommended for beginners
export OPENAI_API_KEY="sk-..."

# Anthropic (Claude models)
export ANTHROPIC_API_KEY="sk-ant-..."

# Google (Gemini models)
export GEMINI_API_KEY="..."
```

**Tip**: Add these to your `~/.bashrc` or `~/.zshrc` to make them permanent.

### Step 3: Initialize Your Project

```bash
cd /path/to/your/project

# Initialize Memov
mem init

# Track some files
mem track src/*.py

# Create a snapshot
mem snap

# IMPORTANT: Sync to VectorDB for RAG search
mem sync
```

**Critical**: Always run `mem sync` after making changes. This indexes your code for RAG search.

### Step 4: Verify Setup

```bash
mem-debug setup
```

You should see:
- ✅ Memov initialized
- ✅ VectorDB populated
- ✅ LiteLLM installed
- ✅ At least one API key configured

---

## 🎯 Your First Debug Session

### Example 1: Quick Search

Search your code history using natural language:

```bash
mem-debug search "authentication implementation"
```

**Output**:
```
🔍 RAG SEARCH RESULTS
Found 3 results

[1] Relevance: 95.3%
    Commit: a1b2c3d4
    Type: agent_plan
    Files: auth.py, middleware.py
    Content: Implemented JWT authentication with refresh tokens...
```

### Example 2: Debug with Error Context

Analyze an error using multiple AI models:

```bash
mem-debug analyze "Why is login failing?" \
    --error "Invalid credentials" \
    --trace "File auth.py, line 42, in verify_password"
```

**Output**:
```
🔍 VIBE DEBUGGING REPORT

Context Retrieved:
  • Relevant commits: 3
  • Error: Invalid credentials

🎯 Key Recommendations:
  1. Check password hashing algorithm compatibility
  2. Verify database query is returning correct user
  3. Add debug logging to password verification
  4. Check for case sensitivity in email comparison

💬 Analysis by Model:

✓ gpt-4o-mini:
Based on the stack trace and context, the issue appears to be in
password verification...

✓ claude-3-5-sonnet-20241022:
The authentication failure suggests a mismatch between...

✓ gemini/gemini-1.5-flash:
Root cause likely stems from password hash verification...
```

### Example 3: Compare Model Responses

Get different perspectives on a question:

```bash
mem-debug compare "How should I structure error handling?"
```

This queries all configured models and displays their responses side-by-side.

---

## 📚 Common Use Cases

### Use Case 1: Finding When Something Was Added

```bash
mem-debug search "user authentication" --type agent_plan --limit 10
```

### Use Case 2: Debugging Production Errors

```bash
# Copy error from logs
ERROR_MSG="Database connection timeout after 30s"
STACK_TRACE=$(cat error.log)

mem-debug analyze "Production API timeout" \
    --error "$ERROR_MSG" \
    --trace "$STACK_TRACE" \
    --models "gpt-4o,claude-3-5-sonnet-20241022"
```

### Use Case 3: Understanding Legacy Code

```bash
mem-debug search "database migration logic" --type response
```

### Use Case 4: Getting Multiple Opinions

```bash
mem-debug compare "Should I use PostgreSQL or MongoDB?" \
    --models "gpt-4o,claude-3-opus-20240229,gemini-1.5-pro"
```

---

## 🔧 MCP Integration (Claude Code)

If you're using Claude Code, VIBE debugging is available as MCP tools.

### Configure MCP Server

Add to your Claude Code MCP config:

```json
{
  "mcpServers": {
    "memov": {
      "command": "mem-mcp-server",
      "args": ["--project-path", "/path/to/your/project"]
    }
  }
}
```

### Use in Claude Code

```python
# In Claude Code, call the tool
vibe_debug(
    query="Why is the API slow?",
    error_message="Timeout after 5s",
    models="gpt-4o-mini,claude-3-5-sonnet-20241022"
)

# Quick search
vibe_search(
    query="authentication",
    n_results=10
)
```

---

## 💡 Tips & Best Practices

### 1. Keep VectorDB Updated

```bash
# After every 3-5 changes
mem snap
mem snap
mem snap
mem sync  # ← Don't forget!
```

### 2. Use Appropriate Models

| Situation | Recommended Models |
|-----------|-------------------|
| Quick debugging | `gpt-4o-mini`, `claude-3-5-haiku-20241022` |
| Complex issues | `gpt-4o`, `claude-3-5-sonnet-20241022` |
| Cost-effective | `gpt-4o-mini`, `gemini-1.5-flash` |
| Production bugs | All three major models |

### 3. Provide Context

More context = better results:

```bash
# Good ✅
mem-debug analyze "Login fails" \
    --error "Invalid password" \
    --trace "$(cat stacktrace.txt)" \
    --logs "$(tail -n 50 app.log)"

# Less effective ❌
mem-debug analyze "Login fails"
```

### 4. Iterate on Queries

Start specific, not broad:

```bash
# Too broad ❌
mem-debug search "error"

# Better ✅
mem-debug search "database connection error"

# Best ✅✅
mem-debug search "postgresql connection pool timeout error"
```

---

## 🐛 Troubleshooting

### "VectorDB is empty"

```bash
# Solution: Sync your changes
mem sync
```

### "No API keys configured"

```bash
# Solution: Set at least one
export OPENAI_API_KEY="your-key"
```

### "Memov not initialized"

```bash
# Solution: Initialize in your project
cd /path/to/project
mem init
```

### Search results not relevant

```bash
# Make sure you've synced recent changes
mem sync

# Try more specific query
mem-debug search "specific feature name" --limit 10

# Check VectorDB has data
mem-debug setup
```

### Models timeout

```bash
# Use faster models
mem-debug analyze "..." --models "gpt-4o-mini"

# Or reduce context
mem-debug analyze "..." --context 3
```

---

## 🎓 Next Steps

1. **Read the Full Guide**: [VIBE_DEBUGGING_GUIDE.md](./VIBE_DEBUGGING_GUIDE.md)
2. **View Demo**: Open [vibe-debugging-demo.html](./vibe-debugging-demo.html) in your browser
3. **Try Examples**: Run the examples in this guide
4. **Explore Models**: Try different model combinations
5. **Integrate with Workflow**: Add to your debugging routine

---

## 📊 Workflow Integration

### Daily Development Workflow

```bash
# Morning: Start work
cd /path/to/project
mem-debug search "feature I'm working on"

# During development: Track changes
mem track new_file.py
mem snap

# After 3-5 changes: Sync
mem sync

# When stuck: Debug
mem-debug analyze "Why isn't this working?" \
    --error "..." \
    --trace "..."

# End of day: Final sync
mem sync
```

### Bug Investigation Workflow

```bash
# 1. Gather context
ERROR_MSG=$(tail -n 1 error.log)
STACK_TRACE=$(cat stacktrace.txt)

# 2. Search for similar issues
mem-debug search "$ERROR_MSG" --limit 10

# 3. Full analysis with multiple models
mem-debug analyze "Debug this error" \
    --error "$ERROR_MSG" \
    --trace "$STACK_TRACE" \
    --models "gpt-4o,claude-3-5-sonnet-20241022,gemini-1.5-pro"

# 4. Compare recommendations
# Review output from all 3 models

# 5. Implement fix
# Make changes...

# 6. Track the fix
mem snap
mem sync
```

---

## 🌟 Advanced Features

### Custom Model Selection

```bash
# Use specific models for different tasks
mem-debug analyze "Complex architecture question" \
    --models "gpt-4o,claude-3-opus-20240229"

mem-debug analyze "Quick bug fix" \
    --models "gpt-4o-mini"
```

### Filter by Content Type

```bash
# Search only agent plans (high-level summaries)
mem-debug search "API changes" --type agent_plan

# Search only prompts (what you asked)
mem-debug search "authentication" --type prompt

# Search only responses (what AI did)
mem-debug search "error handling" --type response
```

### Increase Context Depth

```bash
# Get more historical context (default: 5)
mem-debug analyze "Complex issue" --context 15
```

---

## 📝 Summary

**VIBE Debugging gives you:**

✅ **RAG Search**: Find relevant code using natural language
✅ **Multi-Model Analysis**: Get diverse AI perspectives
✅ **Context-Aware**: Combines errors, logs, and history
✅ **Actionable Insights**: Specific recommendations with code
✅ **Fast**: Async parallel querying
✅ **Flexible**: MCP tools + CLI

**Get started now:**

```bash
# 1. Install
pip install -e .

# 2. Configure
export OPENAI_API_KEY="your-key"

# 3. Initialize
mem init && mem sync

# 4. Debug
mem-debug analyze "your question"
```

**Happy Debugging! 🎉**

---

## 🔗 Links

- [Full Documentation](./VIBE_DEBUGGING_GUIDE.md)
- [Demo Page](./vibe-debugging-demo.html)
- [GitHub Issues](https://github.com/yourusername/mem-mcp-server/issues)
- [Main README](./README.md)

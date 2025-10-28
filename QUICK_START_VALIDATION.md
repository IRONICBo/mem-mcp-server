# Quick Start: Validation & Debugging

## 🚀 5-Minute Setup

### 1. Ensure Memov is Initialized

```bash
# In your project directory
mem init
```

### 2. Make Some Changes with AI

```python
# Example: AI modifies files
# Files: auth/middleware.py, api/routes.py

# Record with snap
snap(
    user_prompt="Add JWT authentication middleware to API",
    original_response="I've created a JWT middleware...",
    agent_plan=[
        "auth/middleware.py: Created JWT validation middleware",
        "api/routes.py: Integrated middleware into routes"
    ],
    files_changed="auth/middleware.py,api/routes.py"
)
```

### 3. Validate the Changes

```python
# Validate the most recent commit
result = validate_commit("HEAD")
```

**Expected Output:**
```
======================================================================
VALIDATION REPORT: a1b2c3d8
======================================================================

Status: ✓ ALIGNED
Alignment Score: 0.85 / 1.00

Prompt:
  Add JWT authentication middleware to API

Files Changed: 2
  [ADDED] auth/middleware.py
  [MODIFIED] api/routes.py

Expected Files (from prompt): 2
  • auth/middleware.py
  • api/routes.py

Issues (0):

Recommendations (1):
  → Consider adding test coverage for authentication logic

======================================================================
```

## 📊 Common Workflows

### Workflow 1: Post-Feature Check

```python
# 1. Implement feature with AI
# 2. Record changes
snap(user_prompt, response, agent_plan, files_changed)

# 3. Validate immediately
result = validate_commit("HEAD")

# 4. Check score
if score < 0.7:
    print("⚠ Low alignment - review unexpected changes")
```

### Workflow 2: Session Review

```python
# At end of coding session
report = validate_recent(n=10)

# Look for patterns:
# - Declining scores → context drift
# - Repeated unexpected files → systematic issue
# - Missing files → incomplete work
```

### Workflow 3: Debugging Investigation

```python
# When a bug is found
results = validate_recent(n=20)

# Find suspicious commits
for r in results:
    if r.alignment_score < 0.6:
        print(f"Check commit {r.commit_hash}")
        print(f"Issues: {r.issues}")
```

## 🎯 Understanding Scores

| Score | Meaning | Action |
|-------|---------|--------|
| 0.9-1.0 | Excellent | ✅ Continue as is |
| 0.7-0.9 | Good | ✅ Minor review recommended |
| 0.5-0.7 | Moderate | ⚠ Review unexpected changes |
| 0.0-0.5 | Poor | 🚨 Investigate immediately |

## 🔍 Key Indicators

### Green Flags (Good Alignment)
- ✅ All mentioned files were modified
- ✅ No unexpected file changes
- ✅ Clear, detailed prompt
- ✅ Agent plan present
- ✅ Reasonable change scope (1-5 files)

### Red Flags (Context Drift)
- 🚨 Many unexpected files modified
- 🚨 Mentioned files not changed
- 🚨 Vague or very short prompt
- 🚨 No agent plan provided
- 🚨 Unusually large change scope (>10 files)

## 💡 Quick Tips

### For Better Alignment

1. **Be Specific in Prompts**
   ```
   ❌ "Update the auth code"
   ✅ "Add JWT validation to auth/middleware.py"
   ```

2. **Always Provide Agent Plans**
   ```python
   agent_plan=[
       "file1.py: What changed",
       "file2.py: What changed"
   ]
   ```

3. **Break Down Large Changes**
   ```
   ❌ One commit touching 20 files
   ✅ Multiple commits, 2-5 files each
   ```

4. **Validate Regularly**
   ```python
   # After each feature
   validate_commit("HEAD")

   # End of session
   validate_recent(n=10)
   ```

## 🐛 Vibe Debugging Example

When you find a misaligned commit:

```python
# 1. Identify the problem
result = validate_commit("a1b2c3d")
# Score: 0.45, Unexpected: config.py, logger.py

# 2. Extract context
context = {
    "prompt": result.prompt,
    "unexpected_files": result.unexpected_files,
    "actual_changes": result.actual_changes
}

# 3. Query Multiple LLMs with this context
# Claude: "Why were config.py and logger.py changed?"
# GPT-4: "What could cause drift to these files?"
# Gemini: "How are these files related?"

# 4. Compare insights → 5× faster resolution
```

## 🎬 Interactive Demo

Open `vibe-debugging-demo.html` in your browser for:
- Visual workflow diagrams
- Interactive examples
- Architecture overview
- Use case demonstrations

## 📚 Full Documentation

- **Comprehensive Guide**: [DEBUGGING_VALIDATION.md](DEBUGGING_VALIDATION.md)
- **Implementation Details**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **MCP Tools Reference**: [README.md](README.md)

## ⚡ Cheat Sheet

```python
# Validate specific commit
validate_commit("a1b2c3d", detailed=True)

# Validate recent commits
validate_recent(n=5)

# Quick check (less detail)
validate_commit("HEAD", detailed=False)

# Batch review
validate_recent(n=20)  # Max 20
```

## 🆘 Troubleshooting

### "No commits found to validate"
- Ensure you've made commits with `snap()`
- Check that memov is initialized: `mem init`

### "Low alignment score but changes are correct"
- Prompt may not have mentioned files explicitly
- Add detailed agent plans
- Consider adjusting threshold (0.7 is recommended)

### "Validation error"
- Verify commit hash exists
- Check memov repository integrity
- Review logs for details

## 🎓 Learning Path

1. **Start Here**: Read this quick start
2. **Practice**: Validate a few commits
3. **Understand**: Read [DEBUGGING_VALIDATION.md](DEBUGGING_VALIDATION.md)
4. **Explore**: Open [vibe-debugging-demo.html](vibe-debugging-demo.html)
5. **Master**: Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

## 📞 Get Help

- 💬 [Discord Community](https://discord.gg/un54aD7Hug)
- 🐛 [GitHub Issues](https://github.com/memovai/memov/issues)
- 🌐 [Website](https://memov.ai)
- 🐦 [Twitter](https://x.com/ssslvky)

---

**Ready to validate?** Start with `validate_recent(n=5)` and explore your recent commits!

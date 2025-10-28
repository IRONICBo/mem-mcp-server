# Debugging & Validation Package

## Overview

The debugging package provides validation tools for MCP operations, helping you verify that AI prompts and responses align with actual code changes. This is crucial for:

- **Context Drift Detection**: Identifying when changes diverge from stated intent
- **Quality Assurance**: Ensuring changes match their descriptions
- **Debugging**: Finding root causes of issues by reviewing change history
- **Vibe Debugging**: Leveraging validation results across different LLMs for faster issue resolution

## Architecture

```
memov/debugging/
├── __init__.py          # Package exports
└── validator.py         # Core validation logic
    ├── DebugValidator   # Main validator class
    ├── ValidationResult # Result data structure
    └── FileChange       # File change representation
```

## Core Concepts

### ValidationResult

Each validation produces a structured result containing:

- **Alignment Score** (0.0-1.0): Calculated based on:
  - File overlap (expected vs actual) - 40% weight
  - Prompt quality (length/specificity) - 30% weight
  - Agent plan presence - 15% weight
  - Change size reasonableness - 15% weight

- **File Analysis**:
  - `expected_files`: Files mentioned in prompt/response
  - `actual_changes`: Files actually modified in commit
  - `unexpected_files`: Changed but not mentioned (possible drift)
  - `missing_files`: Mentioned but not changed

- **Issues & Recommendations**: Actionable insights for improvement

### Alignment Scoring

| Score Range | Meaning | Typical Characteristics |
|-------------|---------|------------------------|
| 0.9 - 1.0 | Excellent | All files match, clear prompt, reasonable scope |
| 0.7 - 0.9 | Good | Minor discrepancies, acceptable alignment |
| 0.5 - 0.7 | Moderate | Some drift, needs review |
| 0.0 - 0.5 | Poor | Significant misalignment, investigate immediately |

## MCP Tools

### 1. `validate_commit`

Validates a specific commit by comparing its metadata with actual changes.

```python
# Usage via MCP
validate_commit(
    commit_hash="a1b2c3d",  # Full or short hash
    detailed=True           # Include full details
)
```

**Output Example**:
```
======================================================================
VALIDATION REPORT: a1b2c3d8
======================================================================

Status: ✓ ALIGNED
Alignment Score: 0.85 / 1.00

Prompt:
  Add authentication middleware to API routes and create login handler

Agent Plan:
  1. auth/middleware.py: Created authentication middleware with JWT validation
  2. api/routes.py: Integrated middleware into route definitions

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

### 2. `validate_recent`

Batch validates the N most recent commits, providing aggregate statistics.

```python
# Usage via MCP
validate_recent(n=5)  # Validate last 5 commits
```

**Output Example**:
```
================================================================================
MEMOV VALIDATION REPORT
================================================================================

Total Commits Validated: 5
Aligned Commits: 4 (80.0%)
Average Alignment Score: 0.78

--------------------------------------------------------------------------------

[1] Commit: a1b2c3d8
    Aligned: ✓ Yes
    Score: 0.85
    Prompt: Add authentication middleware to API routes
    Files Changed: 2

[2] Commit: b2c3d4e5
    Aligned: ✗ No
    Score: 0.55
    Prompt: Fix login bug
    Files Changed: 5
    Unexpected: config/settings.py, utils/logger.py
    Issues (2):
      • Unexpected files modified: config/settings.py, utils/logger.py
      • Prompt is very short and may lack context
    Recommendations (2):
      → Review if these unexpected changes were intentional or indicate context drift
      → Provide more detailed prompts for better tracking

[3] Commit: c3d4e5f6
    ...

================================================================================
```

## Usage Patterns

### 1. Post-Feature Validation

After implementing a feature, validate the commit to ensure alignment:

```python
# In your AI assistant workflow
1. Complete feature implementation
2. Call snap() to record changes
3. Call validate_commit() with the commit hash
4. Review alignment score and issues
5. If score < 0.7, investigate unexpected changes
```

### 2. Session Review

At the end of a coding session:

```python
# Validate all recent work
validate_recent(n=10)

# Check for patterns:
# - Are scores declining? (context drift over time)
# - Repeated unexpected files? (systematic issue)
# - Missing files? (incomplete implementations)
```

### 3. Debugging Workflow

When investigating an issue:

```python
# Find commits related to problematic files
1. Use validate_recent() to get overview
2. Identify commits with low alignment scores
3. Use validate_commit() with detailed=True for deep dive
4. Review unexpected_files and missing_files
5. Check if context drift introduced the bug
```

### 4. Vibe Debugging Integration

The validation results can be used for cross-LLM debugging:

```python
# 1. Validate and identify misaligned commit
result = validate_commit("a1b2c3d")

# 2. Extract alignment issues
issues = {
    "alignment_score": result.alignment_score,
    "unexpected_files": result.unexpected_files,
    "missing_files": result.missing_files,
    "original_prompt": result.prompt,
    "actual_changes": result.actual_changes
}

# 3. Use these insights to query different LLMs
# - Share the misalignment context
# - Ask for analysis of what went wrong
# - Get suggestions for fixes
# - Compare responses from Claude, GPT-4, etc.
```

## Implementation Details

### File Path Extraction

The validator uses regex patterns to extract file paths from text:

```python
# Pattern 1: Standard file extensions
r"([a-zA-Z0-9_\-./]+\.[a-zA-Z0-9]+)"

# Pattern 2: Explicit references
r"(?:file|modify|update|change|create)[\s:]+([a-zA-Z0-9_\-./]+\.[a-zA-Z0-9]+)"
```

**Examples matched**:
- `auth/middleware.py`
- `src/components/Login.tsx`
- `modify api/routes.py`
- `create tests/test_auth.py`

### Change Detection

The validator compares commits using git operations:

1. Get files in target commit
2. Get files in parent commit
3. Compute set differences:
   - Added = target - parent
   - Deleted = parent - target
   - Modified = target ∩ parent

### Alignment Calculation

```python
score = (
    file_overlap_score * 0.4 +      # How well files match
    prompt_quality_score * 0.3 +     # Is prompt clear?
    agent_plan_score * 0.15 +        # Is plan present?
    change_size_score * 0.15         # Is scope reasonable?
)
```

## Best Practices

### For AI Assistants

1. **Clear Prompts**: Include specific file names in prompts
2. **Detailed Agent Plans**: List all files you intend to modify
3. **Regular Validation**: Call validate after significant changes
4. **Score Monitoring**: Track alignment scores over session
5. **Issue Response**: Address low scores immediately

### For Users

1. **Provide Context**: Give detailed prompts with file references
2. **Review Reports**: Check validation output after major changes
3. **Pattern Recognition**: Look for recurring issues (same unexpected files)
4. **Threshold Setting**: Define acceptable alignment score for your project (e.g., > 0.7)
5. **Cross-Reference**: Use validation data when debugging with multiple LLMs

## Troubleshooting

### Low Alignment Scores

**Causes**:
- Vague prompts lacking file specifics
- Agent modified more files than intended (context drift)
- Incomplete file path extraction

**Solutions**:
- Provide explicit file paths in prompts
- Review unexpected_files for patterns
- Break large changes into smaller commits

### False Positives (Unexpected Files)

**Causes**:
- File paths not mentioned in prompt text
- Reasonable but implicit dependencies

**Solutions**:
- Use detailed agent plans listing all files
- Review if unexpected files were necessary
- Adjust alignment threshold if needed

### Missing Expected Files

**Causes**:
- File mentioned but not actually changed
- Feature partially implemented
- File path extraction detected false positive

**Solutions**:
- Complete the implementation
- Update prompt to reflect actual scope
- Check if mentioned file was a reference, not a target

## Future Enhancements

Potential improvements to the validation system:

1. **Semantic Analysis**: Use embeddings to compare prompt intent with change diffs
2. **Diff-Level Validation**: Validate specific code changes, not just files
3. **Pattern Learning**: Build corpus of good/bad alignments for ML-based scoring
4. **Integration Testing**: Validate that changes work as intended
5. **Context Tracking**: Monitor context drift across entire sessions
6. **Auto-Correction**: Suggest fixes for misaligned commits
7. **LLM Comparison**: Built-in vibe debugging with multiple LLMs

## API Reference

### DebugValidator

```python
class DebugValidator:
    def __init__(self, memov_manager: MemovManager)

    def validate_commit(self, commit_hash: str) -> ValidationResult
        """Validate single commit"""

    def validate_recent_commits(self, n: int = 5) -> list[ValidationResult]
        """Validate N recent commits"""

    def generate_report(self, results: list[ValidationResult]) -> str
        """Generate human-readable report"""
```

### ValidationResult

```python
@dataclass
class ValidationResult:
    commit_hash: str
    is_aligned: bool
    alignment_score: float
    prompt: Optional[str]
    response: Optional[str]
    agent_plan: Optional[str]
    actual_changes: list[FileChange]
    expected_files: list[str]
    unexpected_files: list[str]
    missing_files: list[str]
    issues: list[str]
    recommendations: list[str]

    def to_dict(self) -> dict[str, Any]
        """Serialize to dictionary"""
```

### FileChange

```python
@dataclass
class FileChange:
    file_path: str
    change_type: str  # "added", "modified", "deleted"
    additions: int
    deletions: int
    diff: str
```

## Examples

### Example 1: Well-Aligned Commit

```
Prompt: "Add error handling to user registration in auth/register.py"
Agent Plan: ["auth/register.py: Added try-catch blocks and validation"]
Actual Changes: [auth/register.py (modified)]

Result:
  ✓ ALIGNED
  Score: 0.95
  Issues: None
```

### Example 2: Context Drift Detected

```
Prompt: "Fix typo in README"
Agent Plan: ["README.md: Corrected spelling errors"]
Actual Changes: [
    README.md (modified),
    src/config.py (modified),
    tests/test_config.py (modified)
]

Result:
  ✗ NOT ALIGNED
  Score: 0.45
  Unexpected: src/config.py, tests/test_config.py
  Issues: Unexpected files modified (context drift suspected)
  Recommendations: Review if config changes were intentional
```

### Example 3: Vague Prompt

```
Prompt: "update code"
Agent Plan: None
Actual Changes: [5 files modified]

Result:
  ✗ NOT ALIGNED
  Score: 0.30
  Issues:
    - Prompt is very short and may lack context
    - No agent plan provided
  Recommendations:
    - Provide more detailed prompts for better tracking
    - Include agent plan to document intended changes
```

## Contributing

To extend the validation system:

1. Add new validation heuristics in `validator.py`
2. Extend `ValidationResult` with additional metrics
3. Implement new MCP tools in `mcp_server.py`
4. Update scoring weights based on empirical data
5. Add pattern recognition for common drift scenarios

## License

MIT License - Same as parent project

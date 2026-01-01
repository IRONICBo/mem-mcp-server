def short_msg(val: str) -> str:
    """Shorten the message to 15 characters, adding '...' if longer."""
    if not isinstance(val, str):
        raise TypeError(f"Expected str, got {type(val)}")

    if not val:
        return ""
    return val[:15] + ("..." if len(val) > 15 else "")


def clean_windows_git_lstree_output(output: str) -> str:
    """Clean up git ls-tree output for Windows compatibility.

    Handles:
    - Windows CRLF line endings (\\r\\n)
    - Quoted paths (git quotes paths with special characters)
    - Trailing/leading whitespace
    """
    if not isinstance(output, str):
        raise TypeError(f"Expected str, got {type(output)}")

    # First remove line endings, then strip whitespace, then remove quotes
    result = output.split('\r')[0].split('\n')[0].strip().strip('"')
    return result


def split_path_parts(rel_path: str) -> list[str]:
    """Split a relative path into parts, handling both Unix and Windows separators.

    This function normalizes path separators to work cross-platform.
    Git always outputs paths with '/' but os.path.relpath uses '\\' on Windows.

    Args:
        rel_path: A relative file path (may use '/' or '\\' as separator)

    Returns:
        List of path components
    """
    # Normalize to forward slashes then split
    # This handles both Git output (/) and Windows os.path output (\\)
    return rel_path.replace("\\", "/").split("/")

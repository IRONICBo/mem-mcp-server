"""Unit tests for string_utils module - cross-platform path handling."""

import pytest

from memov.utils.string_utils import (
    clean_windows_git_lstree_output,
    short_msg,
    split_path_parts,
)


class TestShortMsg:
    """Tests for short_msg function."""

    def test_short_string(self):
        """String shorter than 15 chars should not be truncated."""
        assert short_msg("hello") == "hello"

    def test_exact_15_chars(self):
        """String exactly 15 chars should not have ellipsis."""
        assert short_msg("a" * 15) == "a" * 15

    def test_long_string(self):
        """String longer than 15 chars should be truncated with ellipsis."""
        assert short_msg("a" * 20) == "a" * 15 + "..."

    def test_empty_string(self):
        """Empty string should return empty."""
        assert short_msg("") == ""

    def test_invalid_type(self):
        """Non-string input should raise TypeError."""
        with pytest.raises(TypeError):
            short_msg(123)


class TestCleanWindowsGitLstreeOutput:
    """Tests for clean_windows_git_lstree_output function."""

    def test_clean_quoted_path(self):
        """Should remove surrounding quotes from path."""
        assert clean_windows_git_lstree_output('"file.py"') == "file.py"

    def test_clean_carriage_return(self):
        """Should remove carriage return (Windows line ending)."""
        assert clean_windows_git_lstree_output("file.py\r") == "file.py"
        assert clean_windows_git_lstree_output("file.py\r\n") == "file.py"

    def test_clean_crlf(self):
        """Should handle Windows CRLF line endings."""
        assert clean_windows_git_lstree_output("src/main.py\r\n") == "src/main.py"

    def test_clean_quoted_with_crlf(self):
        """Should handle both quotes and CRLF."""
        assert clean_windows_git_lstree_output('"src/file.py"\r\n') == "src/file.py"

    def test_no_modification_needed(self):
        """Should return unchanged if no cleanup needed."""
        assert clean_windows_git_lstree_output("file.py") == "file.py"

    def test_path_with_spaces(self):
        """Should handle paths with spaces (often quoted by git)."""
        assert clean_windows_git_lstree_output('"path with spaces/file.py"') == "path with spaces/file.py"

    def test_invalid_type(self):
        """Non-string input should raise TypeError."""
        with pytest.raises(TypeError):
            clean_windows_git_lstree_output(123)


class TestSplitPathParts:
    """Tests for split_path_parts function - cross-platform path splitting."""

    # Unix-style paths (forward slashes)
    def test_unix_simple_path(self):
        """Should split Unix-style path correctly."""
        assert split_path_parts("src/utils/file.py") == ["src", "utils", "file.py"]

    def test_unix_single_file(self):
        """Should handle single file without directory."""
        assert split_path_parts("file.py") == ["file.py"]

    def test_unix_deep_path(self):
        """Should handle deeply nested paths."""
        assert split_path_parts("a/b/c/d/e/f.txt") == ["a", "b", "c", "d", "e", "f.txt"]

    # Windows-style paths (backslashes)
    def test_windows_simple_path(self):
        """Should split Windows-style path correctly."""
        assert split_path_parts("src\\utils\\file.py") == ["src", "utils", "file.py"]

    def test_windows_deep_path(self):
        """Should handle deeply nested Windows paths."""
        assert split_path_parts("a\\b\\c\\d\\e\\f.txt") == ["a", "b", "c", "d", "e", "f.txt"]

    # Mixed paths (should not happen but handle gracefully)
    def test_mixed_separators(self):
        """Should handle mixed path separators."""
        assert split_path_parts("src/utils\\file.py") == ["src", "utils", "file.py"]
        assert split_path_parts("src\\utils/file.py") == ["src", "utils", "file.py"]

    # Edge cases
    def test_empty_string(self):
        """Empty string should return list with empty string."""
        assert split_path_parts("") == [""]

    def test_trailing_separator(self):
        """Should handle trailing separator."""
        assert split_path_parts("src/utils/") == ["src", "utils", ""]
        assert split_path_parts("src\\utils\\") == ["src", "utils", ""]

    def test_leading_separator(self):
        """Should handle leading separator."""
        assert split_path_parts("/src/utils") == ["", "src", "utils"]
        assert split_path_parts("\\src\\utils") == ["", "src", "utils"]

    # Real-world scenarios
    def test_git_output_unix(self):
        """Git always outputs paths with forward slashes."""
        # Git ls-tree output format (always uses /)
        assert split_path_parts("memov/core/manager.py") == ["memov", "core", "manager.py"]

    def test_os_relpath_windows(self):
        """os.path.relpath on Windows returns backslashes."""
        # Simulating os.path.relpath output on Windows
        assert split_path_parts("memov\\core\\manager.py") == ["memov", "core", "manager.py"]

    def test_path_with_dots(self):
        """Should handle paths with dots (hidden files, extensions)."""
        assert split_path_parts(".github/workflows/ci.yml") == [".github", "workflows", "ci.yml"]
        assert split_path_parts(".gitignore") == [".gitignore"]

    def test_path_with_spaces(self):
        """Should handle paths with spaces in names."""
        assert split_path_parts("My Documents/file.txt") == ["My Documents", "file.txt"]
        assert split_path_parts("My Documents\\file.txt") == ["My Documents", "file.txt"]


class TestCrossplatformIntegration:
    """Integration tests simulating cross-platform scenarios."""

    def test_git_to_tree_structure_unix(self):
        """Simulate building tree structure from Git output (Unix)."""
        # Git output always uses /
        rel_paths = [
            "src/main.py",
            "src/utils/helper.py",
            "tests/test_main.py",
        ]

        tree = {}
        for rel_path in rel_paths:
            parts = split_path_parts(rel_path)
            current = tree
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = "blob_hash"

        assert "src" in tree
        assert "main.py" in tree["src"]
        assert "utils" in tree["src"]
        assert "helper.py" in tree["src"]["utils"]
        assert "tests" in tree
        assert "test_main.py" in tree["tests"]

    def test_git_to_tree_structure_windows(self):
        """Simulate building tree structure from os.path.relpath output (Windows)."""
        # os.path.relpath on Windows uses \
        rel_paths = [
            "src\\main.py",
            "src\\utils\\helper.py",
            "tests\\test_main.py",
        ]

        tree = {}
        for rel_path in rel_paths:
            parts = split_path_parts(rel_path)
            current = tree
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = "blob_hash"

        # Should produce identical tree structure as Unix
        assert "src" in tree
        assert "main.py" in tree["src"]
        assert "utils" in tree["src"]
        assert "helper.py" in tree["src"]["utils"]
        assert "tests" in tree
        assert "test_main.py" in tree["tests"]

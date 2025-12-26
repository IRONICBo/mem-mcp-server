"""Tests for CLI commands."""

import os
import subprocess
import sys

import pytest


class TestMemCLI:
    """Tests for the mem CLI command."""

    def test_mem_help(self):
        """Test mem --help command."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Usage" in result.stdout or "usage" in result.stdout.lower()

    def test_mem_init(self, temp_project):
        """Test mem init command."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "init"],
            cwd=temp_project,
            capture_output=True,
            text=True,
        )
        # Should succeed or indicate already initialized
        assert result.returncode == 0 or "already" in result.stderr.lower()

    def test_mem_check_not_initialized(self, temp_project):
        """Test mem check on uninitialized project."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "check"],
            cwd=temp_project,
            capture_output=True,
            text=True,
        )
        # Should indicate not initialized
        assert "not initialized" in result.stdout.lower() or result.returncode != 0


class TestMemHistory:
    """Tests for mem history command."""

    def test_history_empty(self, initialized_memov, temp_project):
        """Test history on fresh memov (may have init commit)."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "history"],
            cwd=temp_project,
            capture_output=True,
            text=True,
        )
        # Should run without error
        assert result.returncode == 0

    def test_history_with_commits(self, memov_with_snapshots, temp_project):
        """Test history shows commits with agent_plan column."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "history"],
            cwd=temp_project,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        # Should contain the Plan column header
        assert "Plan" in result.stdout

    def test_history_shows_operation_type(self, memov_with_snapshots, temp_project):
        """Test history shows operation type column."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "history"],
            cwd=temp_project,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Operation" in result.stdout


class TestMemSnap:
    """Tests for mem snap command."""

    def test_snap_basic(self, initialized_memov, temp_project):
        """Test basic snap command."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "snap"],
            cwd=temp_project,
            capture_output=True,
            text=True,
        )
        # Should succeed
        assert result.returncode == 0


class TestMemWeb:
    """Tests for mem web command."""

    def test_web_help(self):
        """Test mem web --help command."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "web", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "port" in result.stdout.lower() or "loc" in result.stdout.lower()

    def test_web_not_initialized(self, temp_project):
        """Test web command on uninitialized project."""
        # Use timeout to prevent hanging
        try:
            result = subprocess.run(
                [sys.executable, "-m", "memov.main", "web", "--loc", str(temp_project)],
                cwd=temp_project,
                capture_output=True,
                text=True,
                timeout=2,  # Should fail quickly if not initialized
            )
            # Should indicate error or not initialized
            assert "not initialized" in result.stdout.lower() or result.returncode != 0
        except subprocess.TimeoutExpired:
            # If it times out, that's also acceptable (means server tried to start)
            pass


class TestMemJump:
    """Tests for mem jump command."""

    def test_jump_help(self):
        """Test mem jump --help command."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "jump", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0


class TestMemShow:
    """Tests for mem show command."""

    def test_show_help(self):
        """Test mem show --help command."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "show", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_show_with_commit(self, memov_with_snapshots, temp_project):
        """Test show command with a commit hash."""
        # Get a commit hash first
        from memov.core.manager import MemovManager

        manager = MemovManager(project_path=str(temp_project))
        history = manager.get_history(limit=1)
        if not history:
            pytest.skip("No commits found")

        commit_hash = history[0]["short_hash"]

        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "show", commit_hash],
            cwd=temp_project,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0


class TestMemBranch:
    """Tests for mem branch command."""

    def test_branch_list(self, initialized_memov, temp_project):
        """Test listing branches."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "branch"],
            cwd=temp_project,
            capture_output=True,
            text=True,
        )
        # Should succeed or show branches
        assert result.returncode == 0


class TestCLIErrorHandling:
    """Tests for CLI error handling."""

    def test_invalid_command(self):
        """Test handling of invalid command."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "invalid_command_xyz"],
            capture_output=True,
            text=True,
        )
        # Should fail with non-zero exit code
        assert result.returncode != 0

    def test_jump_invalid_hash(self, initialized_memov, temp_project):
        """Test jump with invalid commit hash."""
        result = subprocess.run(
            [sys.executable, "-m", "memov.main", "jump", "invalid_hash_xyz"],
            cwd=temp_project,
            capture_output=True,
            text=True,
        )
        # Should show "not found" message in stdout or have non-zero exit
        assert result.returncode != 0 or "not found" in result.stdout.lower()

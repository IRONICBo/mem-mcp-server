"""Tests for agent_plan storage and parsing."""

import pytest

from memov.core.manager import MemovManager, MemStatus


class TestAgentPlanStorage:
    """Tests for storing agent_plan in commit messages."""

    def test_snapshot_stores_agent_plan(self, initialized_memov, temp_project):
        """Test that snapshot() includes agent_plan in commit message."""
        manager = initialized_memov

        # Create snapshot with agent_plan
        status = manager.snapshot(
            prompt="Test prompt",
            response="Test response",
            agent_plan="1. Step one\n2. Step two",
            by_user=False,
        )
        assert status == MemStatus.SUCCESS

        # Get history and verify agent_plan is stored
        history = manager.get_history(limit=1)
        assert len(history) >= 1

        latest = history[0]
        assert latest["agent_plan"] == "1. Step one"  # First line only in parsed result

    def test_snapshot_empty_agent_plan(self, initialized_memov, temp_project):
        """Test snapshot with empty agent_plan."""
        manager = initialized_memov

        status = manager.snapshot(
            prompt="Test prompt",
            response="Test response",
            agent_plan="",
            by_user=False,
        )
        assert status == MemStatus.SUCCESS

        history = manager.get_history(limit=1)
        assert len(history) >= 1

    def test_snapshot_with_files_stores_agent_plan(self, initialized_memov, temp_project):
        """Test that snapshot with specific files also stores agent_plan."""
        manager = initialized_memov

        # Create a new file
        new_file = temp_project / "new_feature.py"
        new_file.write_text("def new_feature(): pass\n")

        status = manager.snapshot(
            file_paths=[str(new_file)],
            prompt="Add new feature",
            response="Added new_feature function",
            agent_plan="1. Create file\n2. Add function\n3. Test",
            by_user=False,
        )
        assert status == MemStatus.SUCCESS

        history = manager.get_history(limit=1)
        assert len(history) >= 1
        assert "agent_plan" in history[0]


class TestAgentPlanParsing:
    """Tests for parsing agent_plan from commit messages."""

    def test_get_history_includes_agent_plan(self, memov_with_snapshots):
        """Test that get_history() returns agent_plan field."""
        manager = memov_with_snapshots

        history = manager.get_history(limit=10)
        assert len(history) >= 2

        for entry in history:
            assert "agent_plan" in entry
            # agent_plan may be empty string but should exist

    def test_agent_plan_in_history_entry_structure(self, memov_with_snapshots):
        """Test the structure of history entries with agent_plan."""
        manager = memov_with_snapshots

        history = manager.get_history(limit=1)
        entry = history[0]

        # Verify all expected fields are present
        expected_fields = [
            "commit_hash",
            "short_hash",
            "operation",
            "branch",
            "is_head",
            "prompt",
            "response",
            "agent_plan",
            "files",
            "timestamp",
            "author",
        ]

        for field in expected_fields:
            assert field in entry, f"Missing field: {field}"


class TestAgentPlanCommitMessageFormat:
    """Tests for the commit message format with agent_plan."""

    def test_commit_message_contains_agent_plan_line(self, initialized_memov, temp_project):
        """Test that the raw commit message contains 'Agent Plan:' line."""
        from memov.core.git import GitManager

        manager = initialized_memov

        manager.snapshot(
            prompt="Test",
            response="Test response",
            agent_plan="Do step A, then step B",
            by_user=False,
        )

        # Get the latest commit hash
        history = manager.get_history(limit=1)
        if not history:
            pytest.skip("No commits found")

        commit_hash = history[0]["commit_hash"]

        # Get raw commit message
        message = GitManager.get_commit_message(manager.bare_repo_path, commit_hash)

        assert "Agent Plan:" in message
        assert "Do step A, then step B" in message

    def test_commit_message_format_order(self, initialized_memov, temp_project):
        """Test that commit message fields are in expected order."""
        from memov.core.git import GitManager

        manager = initialized_memov

        manager.snapshot(
            prompt="User prompt here",
            response="AI response here",
            agent_plan="Plan step 1",
            by_user=False,
        )

        history = manager.get_history(limit=1)
        if not history:
            pytest.skip("No commits found")

        commit_hash = history[0]["commit_hash"]
        message = GitManager.get_commit_message(manager.bare_repo_path, commit_hash)

        # Verify order: Prompt -> Response -> Agent Plan -> Source
        prompt_pos = message.find("Prompt:")
        response_pos = message.find("Response:")
        agent_plan_pos = message.find("Agent Plan:")
        source_pos = message.find("Source:")

        assert prompt_pos < response_pos < agent_plan_pos < source_pos


class TestAgentPlanEdgeCases:
    """Tests for edge cases in agent_plan handling."""

    def test_agent_plan_with_special_characters(self, initialized_memov, temp_project):
        """Test agent_plan with special characters."""
        manager = initialized_memov

        special_plan = "1. Use `code` formatting\n2. Handle 'quotes' and \"doubles\""
        status = manager.snapshot(
            prompt="Test",
            response="Test",
            agent_plan=special_plan,
            by_user=False,
        )
        assert status == MemStatus.SUCCESS

    def test_agent_plan_with_unicode(self, initialized_memov, temp_project):
        """Test agent_plan with unicode characters."""
        manager = initialized_memov

        unicode_plan = "1. 添加中文支持\n2. Handle emoji"
        status = manager.snapshot(
            prompt="Test unicode",
            response="OK",
            agent_plan=unicode_plan,
            by_user=False,
        )
        assert status == MemStatus.SUCCESS

        history = manager.get_history(limit=1)
        assert len(history) >= 1

    def test_agent_plan_none_value(self, initialized_memov, temp_project):
        """Test that None agent_plan is handled gracefully."""
        manager = initialized_memov

        # Snapshot without agent_plan parameter (uses default)
        status = manager.snapshot(
            prompt="Test",
            response="Test",
            by_user=False,
        )
        assert status == MemStatus.SUCCESS

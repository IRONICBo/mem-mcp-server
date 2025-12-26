"""Shared test fixtures for MemoV tests."""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_project():
    """Create a temporary project directory with git initialized."""
    temp_dir = tempfile.mkdtemp()
    project_path = Path(temp_dir) / "test_project"
    project_path.mkdir()

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=project_path, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"], cwd=project_path, capture_output=True
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"], cwd=project_path, capture_output=True
    )

    # Create a sample file
    (project_path / "test.py").write_text("print('hello')\n")

    yield project_path

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def initialized_memov(temp_project):
    """Create a temporary project with memov initialized."""
    from memov.core.manager import MemovManager

    manager = MemovManager(project_path=str(temp_project))
    manager.init()

    return manager


@pytest.fixture
def memov_with_snapshots(initialized_memov, temp_project):
    """Create a memov instance with some test snapshots."""
    manager = initialized_memov

    # Create first snapshot
    manager.snapshot(
        prompt="Add hello function",
        response="I added a hello function",
        agent_plan="1. Create hello function\n2. Test it",
        by_user=False,
    )

    # Modify file and create another snapshot
    (temp_project / "test.py").write_text("def hello():\n    print('hello')\n")
    manager.snapshot(
        prompt="Refactor to function",
        response="Refactored print to a function",
        agent_plan="1. Wrap in function\n2. Add docstring",
        by_user=False,
    )

    return manager

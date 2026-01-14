"""Benchmark tests for graph API performance.

These tests measure and compare performance of the get_history method
which is used by the /api/graph endpoint.

Run with: pytest tests/test_benchmark_graph.py -v -s
"""

import time
from pathlib import Path

import pytest


@pytest.fixture
def memov_with_many_snapshots(initialized_memov, temp_project):
    """Create a memov instance with many test snapshots for benchmarking."""
    manager = initialized_memov
    num_snapshots = 50  # Create 50 snapshots for benchmark

    for i in range(num_snapshots):
        # Create/modify files
        (temp_project / f"file_{i}.py").write_text(f"# File {i}\nprint('hello {i}')\n")

        manager.snapshot(
            prompt=f"Add file {i} with hello function",
            response=f"I added file {i} with a hello function that prints hello {i}",
            agent_plan=f"1. Create file_{i}.py\n2. Add print statement",
            by_user=False,
        )

    return manager


@pytest.fixture
def memov_with_large_history(initialized_memov, temp_project):
    """Create a memov instance with large number of snapshots for stress testing.

    Note: Creating 200+ real commits takes time. Adjust num_snapshots as needed.
    """
    manager = initialized_memov
    num_snapshots = 200  # Increase for larger tests

    for i in range(num_snapshots):
        # Create/modify files - use modulo to reuse files and reduce disk usage
        file_idx = i % 20
        (temp_project / f"file_{file_idx}.py").write_text(
            f"# File {file_idx} - version {i}\nprint('hello {i}')\n"
        )

        manager.snapshot(
            prompt=f"Update {i}: modify file_{file_idx}",
            response=f"Modified file_{file_idx} in iteration {i}",
            agent_plan=f"1. Update file_{file_idx}.py\n2. Version {i}",
            by_user=False,
        )

    return manager


@pytest.fixture(scope="module")
def memov_with_1k_history(tmp_path_factory):
    """Create a memov instance with 1000 snapshots for stress testing.

    Uses module scope to avoid recreating for each test.
    Takes about 4-5 minutes to create.
    """
    import subprocess

    from memov.core.manager import MemovManager

    # Create temp directory that persists for the module
    temp_dir = tmp_path_factory.mktemp("benchmark_1k")
    project_path = temp_dir / "test_project"
    project_path.mkdir()

    # Initialize git repo
    subprocess.run(["git", "init"], cwd=project_path, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=project_path,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=project_path,
        capture_output=True,
    )

    # Create initial file
    (project_path / "test.py").write_text("print('hello')\n")

    # Initialize memov
    manager = MemovManager(project_path=str(project_path))
    manager.init()

    num_snapshots = 1000
    print(f"\nCreating {num_snapshots} snapshots...")

    for i in range(num_snapshots):
        # Progress indicator every 100 commits
        if i % 100 == 0:
            print(f"  Progress: {i}/{num_snapshots} ({i * 100 // num_snapshots}%)")

        # Create/modify files - use modulo to reuse files and reduce disk usage
        file_idx = i % 50
        (project_path / f"file_{file_idx}.py").write_text(
            f"# File {file_idx} - version {i}\nprint('hello {i}')\n"
        )

        manager.snapshot(
            prompt=f"Update {i}: modify file_{file_idx}",
            response=f"Modified file_{file_idx} in iteration {i}",
            agent_plan=f"1. Update file_{file_idx}.py\n2. Version {i}",
            by_user=False,
        )

    print(f"  Completed: {num_snapshots} snapshots created")
    return manager, project_path


class TestGetHistoryBenchmark:
    """Benchmark tests for get_history method."""

    def test_get_history_performance_status_mode(self, memov_with_many_snapshots):
        """Benchmark get_history with diff_mode='status' (used by /api/graph)."""
        manager = memov_with_many_snapshots

        # Warm up
        manager.get_history(limit=10, diff_mode="status")

        # Benchmark
        iterations = 3
        times = []

        for _ in range(iterations):
            start = time.perf_counter()
            history = manager.get_history(limit=100, diff_mode="status")
            elapsed = time.perf_counter() - start
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"\n--- get_history(limit=100, diff_mode='status') ---")
        print(f"Commits returned: {len(history)}")
        print(f"Average time: {avg_time:.3f}s")
        print(f"Min time: {min_time:.3f}s")
        print(f"Max time: {max_time:.3f}s")

        # Performance assertion: should complete in reasonable time
        # With batch optimization, 50 commits should take < 2 seconds
        assert avg_time < 5.0, f"get_history took too long: {avg_time:.3f}s"

    def test_get_history_performance_none_mode(self, memov_with_many_snapshots):
        """Benchmark get_history with diff_mode='none' (fastest mode)."""
        manager = memov_with_many_snapshots

        # Warm up
        manager.get_history(limit=10, diff_mode="none")

        # Benchmark
        iterations = 3
        times = []

        for _ in range(iterations):
            start = time.perf_counter()
            history = manager.get_history(limit=100, diff_mode="none")
            elapsed = time.perf_counter() - start
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"\n--- get_history(limit=100, diff_mode='none') ---")
        print(f"Commits returned: {len(history)}")
        print(f"Average time: {avg_time:.3f}s")
        print(f"Min time: {min_time:.3f}s")
        print(f"Max time: {max_time:.3f}s")

        # Performance assertion: none mode should be fastest
        assert avg_time < 3.0, f"get_history (none mode) took too long: {avg_time:.3f}s"

    def test_get_history_correctness(self, memov_with_many_snapshots):
        """Verify get_history returns correct data structure."""
        manager = memov_with_many_snapshots

        history = manager.get_history(limit=10, diff_mode="status")

        assert len(history) > 0, "History should not be empty"

        # Check first entry has all required fields
        entry = history[0]
        assert "commit_hash" in entry
        assert "short_hash" in entry
        assert "operation" in entry
        assert "branch" in entry
        assert "is_head" in entry
        assert "prompt" in entry
        assert "response" in entry
        assert "agent_plan" in entry
        assert "files" in entry
        assert "timestamp" in entry
        assert "author" in entry
        assert "diff" in entry

        # Verify commit hash format
        assert len(entry["commit_hash"]) == 40
        assert len(entry["short_hash"]) == 7

        print(f"\nSample entry structure verified:")
        print(f"  commit_hash: {entry['short_hash']}")
        print(f"  operation: {entry['operation']}")
        print(f"  files count: {len(entry['files'])}")
        print(f"  has timestamp: {entry['timestamp'] is not None}")
        print(f"  has author: {entry['author'] is not None}")


class TestGraphApiBenchmark:
    """Benchmark tests for the /api/graph endpoint."""

    def test_graph_api_performance(self, memov_with_many_snapshots, temp_project):
        """Benchmark the /api/graph endpoint."""
        from fastapi.testclient import TestClient

        from memov.web.server import create_app

        app = create_app(str(temp_project))
        client = TestClient(app)

        # Warm up
        client.get("/api/graph")

        # Benchmark
        iterations = 3
        times = []

        for _ in range(iterations):
            start = time.perf_counter()
            response = client.get("/api/graph")
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            assert response.status_code == 200

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        data = response.json()

        print(f"\n--- /api/graph endpoint ---")
        print(f"Nodes returned: {len(data['nodes'])}")
        print(f"Edges returned: {len(data['edges'])}")
        print(f"Average time: {avg_time:.3f}s")
        print(f"Min time: {min_time:.3f}s")
        print(f"Max time: {max_time:.3f}s")

        # Performance assertion: graph API should complete quickly
        assert avg_time < 5.0, f"/api/graph took too long: {avg_time:.3f}s"


class Test1kBenchmark:
    """Large scale benchmark tests (1000 commits).

    Takes about 4-5 minutes to set up.
    Run with: pytest tests/test_benchmark_graph.py::Test1kBenchmark -v -s
    """

    def test_1k_history_performance(self, memov_with_1k_history):
        """Benchmark get_history with 1000 commits."""
        manager, _ = memov_with_1k_history

        # Benchmark status mode (used by /api/graph)
        iterations = 3
        times = []

        for i in range(iterations):
            start = time.perf_counter()
            history = manager.get_history(limit=1000, diff_mode="status")
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            print(f"  Iteration {i + 1}: {elapsed:.3f}s, {len(history)} commits")

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"\n=== 1K BENCHMARK: get_history(limit=1000, diff_mode='status') ===")
        print(f"Commits returned: {len(history)}")
        print(f"Average time: {avg_time:.3f}s")
        print(f"Min time: {min_time:.3f}s")
        print(f"Max time: {max_time:.3f}s")
        print(f"Throughput: {len(history) / avg_time:.1f} commits/sec")

        # Should handle 1000 commits in reasonable time with batch optimization
        assert avg_time < 30.0, f"1k history took too long: {avg_time:.3f}s"

    def test_1k_graph_api_performance(self, memov_with_1k_history):
        """Benchmark /api/graph with 1000 commits."""
        from fastapi.testclient import TestClient

        from memov.web.server import create_app

        manager, project_path = memov_with_1k_history
        app = create_app(str(project_path))
        client = TestClient(app)

        # Benchmark
        iterations = 3
        times = []

        for i in range(iterations):
            start = time.perf_counter()
            response = client.get("/api/graph")
            elapsed = time.perf_counter() - start
            times.append(elapsed)
            assert response.status_code == 200
            print(f"  Iteration {i + 1}: {elapsed:.3f}s")

        avg_time = sum(times) / len(times)
        data = response.json()

        print(f"\n=== 1K BENCHMARK: /api/graph endpoint ===")
        print(f"Nodes returned: {len(data['nodes'])}")
        print(f"Edges returned: {len(data['edges'])}")
        print(f"Average time: {avg_time:.3f}s")
        print(f"Throughput: {len(data['nodes']) / avg_time:.1f} nodes/sec")

        assert avg_time < 30.0, f"/api/graph took too long: {avg_time:.3f}s"

    def test_1k_batch_methods(self, memov_with_1k_history):
        """Benchmark batch methods with 1000 commits."""
        from memov.core.git import GitManager

        manager, _ = memov_with_1k_history
        branches = manager._load_branches()

        # Get all commits
        seen = set()
        all_commits = []
        for commit_hash in branches["branches"].values():
            commit_history = GitManager.get_commit_history(manager.bare_repo_path, commit_hash)
            for hash_id in commit_history:
                if hash_id not in seen:
                    seen.add(hash_id)
                    all_commits.append(hash_id)

        print(f"\nTotal commits found: {len(all_commits)}")

        # Benchmark batch methods
        start = time.perf_counter()
        batch_info = GitManager.get_commits_info_batch(manager.bare_repo_path, all_commits)
        info_time = time.perf_counter() - start

        start = time.perf_counter()
        batch_files = GitManager.get_files_by_commits_batch(manager.bare_repo_path, all_commits)
        files_time = time.perf_counter() - start

        start = time.perf_counter()
        batch_diff = GitManager.get_diff_status_batch(manager.bare_repo_path, all_commits)
        diff_time = time.perf_counter() - start

        total_batch_time = info_time + files_time + diff_time

        print(f"\n=== 1K BENCHMARK: Batch Methods ({len(all_commits)} commits) ===")
        print(f"get_commits_info_batch: {info_time:.3f}s ({len(batch_info)} results)")
        print(f"get_files_by_commits_batch: {files_time:.3f}s ({len(batch_files)} results)")
        print(f"get_diff_status_batch: {diff_time:.3f}s ({len(batch_diff)} results)")
        print(f"Total batch time: {total_batch_time:.3f}s")
        print(f"Throughput: {len(all_commits) / total_batch_time:.1f} commits/sec")

        # Estimate individual method time (based on 50 sample)
        sample_commits = all_commits[:50]
        start = time.perf_counter()
        for commit_hash in sample_commits:
            GitManager.get_commit_message(manager.bare_repo_path, commit_hash)
            manager._get_commit_info(commit_hash)
            GitManager.get_files_by_commit(manager.bare_repo_path, commit_hash)
            manager._get_commit_diff_status(commit_hash)
        sample_time = time.perf_counter() - start

        estimated_individual_time = sample_time * (len(all_commits) / 50)
        speedup = estimated_individual_time / total_batch_time

        print(f"\nIndividual method time (50 sampled): {sample_time:.3f}s")
        print(f"Estimated individual time ({len(all_commits)}): {estimated_individual_time:.1f}s ({estimated_individual_time / 60:.1f} min)")
        print(f"SPEEDUP: {speedup:.1f}x")


class TestLargeScaleBenchmark:
    """Large scale benchmark tests (200+ commits)."""

    def test_large_history_performance(self, memov_with_large_history):
        """Benchmark get_history with 200 commits."""
        manager = memov_with_large_history

        # Benchmark status mode (used by /api/graph)
        iterations = 3
        times = []

        for _ in range(iterations):
            start = time.perf_counter()
            history = manager.get_history(limit=500, diff_mode="status")
            elapsed = time.perf_counter() - start
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        print(f"\n--- Large Scale: get_history(limit=500, diff_mode='status') ---")
        print(f"Commits returned: {len(history)}")
        print(f"Average time: {avg_time:.3f}s")
        print(f"Min time: {min_time:.3f}s")
        print(f"Max time: {max_time:.3f}s")
        print(f"Throughput: {len(history) / avg_time:.1f} commits/sec")

        # Should handle 200 commits in reasonable time
        assert avg_time < 10.0, f"Large history took too long: {avg_time:.3f}s"

    def test_large_batch_vs_individual(self, memov_with_large_history):
        """Compare batch vs individual methods with 200 commits."""
        from memov.core.git import GitManager

        manager = memov_with_large_history
        branches = manager._load_branches()

        # Get all commits
        seen = set()
        all_commits = []
        for commit_hash in branches["branches"].values():
            commit_history = GitManager.get_commit_history(manager.bare_repo_path, commit_hash)
            for hash_id in commit_history:
                if hash_id not in seen:
                    seen.add(hash_id)
                    all_commits.append(hash_id)

        test_commits = all_commits[:200]

        # Benchmark batch method
        start = time.perf_counter()
        batch_info = GitManager.get_commits_info_batch(manager.bare_repo_path, test_commits)
        batch_files = GitManager.get_files_by_commits_batch(manager.bare_repo_path, test_commits)
        batch_diff = GitManager.get_diff_status_batch(manager.bare_repo_path, test_commits)
        batch_time = time.perf_counter() - start

        # Benchmark individual method (sample 50 commits to avoid timeout)
        sample_commits = test_commits[:50]
        start = time.perf_counter()
        for commit_hash in sample_commits:
            GitManager.get_commit_message(manager.bare_repo_path, commit_hash)
            manager._get_commit_info(commit_hash)
            GitManager.get_files_by_commit(manager.bare_repo_path, commit_hash)
            manager._get_commit_diff_status(commit_hash)
        individual_time_50 = time.perf_counter() - start

        # Extrapolate individual time to 200 commits
        individual_time_extrapolated = individual_time_50 * (200 / 50)

        speedup = individual_time_extrapolated / batch_time if batch_time > 0 else float("inf")

        print(f"\n--- Large Scale Batch vs Individual ({len(test_commits)} commits) ---")
        print(f"Batch method time (all 200): {batch_time:.3f}s")
        print(f"Individual method time (50 sampled): {individual_time_50:.3f}s")
        print(f"Individual method time (extrapolated 200): {individual_time_extrapolated:.3f}s")
        print(f"Estimated speedup: {speedup:.1f}x")
        print(f"Batch results - info: {len(batch_info)}, files: {len(batch_files)}, diff: {len(batch_diff)}")

        assert batch_time < individual_time_extrapolated, "Batch should be faster"


class TestBatchMethodsBenchmark:
    """Benchmark tests for batch git methods."""

    def test_batch_vs_individual_commits_info(self, memov_with_many_snapshots):
        """Compare batch vs individual commit info fetching."""
        from memov.core.git import GitManager

        manager = memov_with_many_snapshots
        branches = manager._load_branches()

        # Get all commits
        seen = set()
        all_commits = []
        for commit_hash in branches["branches"].values():
            commit_history = GitManager.get_commit_history(manager.bare_repo_path, commit_hash)
            for hash_id in commit_history:
                if hash_id not in seen:
                    seen.add(hash_id)
                    all_commits.append(hash_id)

        # Limit to test set
        test_commits = all_commits[:30]

        # Benchmark batch method
        start = time.perf_counter()
        batch_result = GitManager.get_commits_info_batch(manager.bare_repo_path, test_commits)
        batch_time = time.perf_counter() - start

        # Benchmark individual method
        start = time.perf_counter()
        individual_results = {}
        for commit_hash in test_commits:
            message = GitManager.get_commit_message(manager.bare_repo_path, commit_hash)
            info = manager._get_commit_info(commit_hash)
            individual_results[commit_hash] = {
                "message": message,
                "timestamp": info.get("timestamp"),
                "author": info.get("author"),
            }
        individual_time = time.perf_counter() - start

        speedup = individual_time / batch_time if batch_time > 0 else float("inf")

        print(f"\n--- Batch vs Individual Commit Info ({len(test_commits)} commits) ---")
        print(f"Batch method time: {batch_time:.3f}s")
        print(f"Individual method time: {individual_time:.3f}s")
        print(f"Speedup: {speedup:.1f}x")

        # Verify batch returns same number of results
        assert len(batch_result) == len(test_commits), "Batch should return all commits"

        # Batch should be faster
        assert batch_time < individual_time, "Batch method should be faster"

    def test_batch_diff_status(self, memov_with_many_snapshots):
        """Benchmark batch diff status fetching."""
        from memov.core.git import GitManager

        manager = memov_with_many_snapshots
        branches = manager._load_branches()

        # Get all commits
        seen = set()
        all_commits = []
        for commit_hash in branches["branches"].values():
            commit_history = GitManager.get_commit_history(manager.bare_repo_path, commit_hash)
            for hash_id in commit_history:
                if hash_id not in seen:
                    seen.add(hash_id)
                    all_commits.append(hash_id)

        test_commits = all_commits[:30]

        # Benchmark batch method
        start = time.perf_counter()
        batch_result = GitManager.get_diff_status_batch(manager.bare_repo_path, test_commits)
        batch_time = time.perf_counter() - start

        # Benchmark individual method
        start = time.perf_counter()
        individual_results = {}
        for commit_hash in test_commits:
            individual_results[commit_hash] = manager._get_commit_diff_status(commit_hash)
        individual_time = time.perf_counter() - start

        speedup = individual_time / batch_time if batch_time > 0 else float("inf")

        print(f"\n--- Batch vs Individual Diff Status ({len(test_commits)} commits) ---")
        print(f"Batch method time: {batch_time:.3f}s")
        print(f"Individual method time: {individual_time:.3f}s")
        print(f"Speedup: {speedup:.1f}x")

        # Batch should be faster
        assert batch_time < individual_time, "Batch method should be faster"

"""Tests for Web UI API endpoints."""

import pytest
from fastapi.testclient import TestClient

from memov.web.server import create_app


@pytest.fixture
def web_client(initialized_memov, temp_project):
    """Create a test client for the web API."""
    app = create_app(str(temp_project))
    return TestClient(app)


@pytest.fixture
def web_client_with_data(memov_with_snapshots, temp_project):
    """Create a test client with snapshot data."""
    app = create_app(str(temp_project))
    return TestClient(app)


class TestBranchesEndpoint:
    """Tests for /api/branches endpoint."""

    def test_get_branches_empty(self, web_client):
        """Test getting branches from fresh memov."""
        response = web_client.get("/api/branches")
        assert response.status_code == 200
        data = response.json()
        assert "current" in data
        assert "branches" in data

    def test_get_branches_with_data(self, web_client_with_data):
        """Test getting branches after snapshots."""
        response = web_client_with_data.get("/api/branches")
        assert response.status_code == 200
        data = response.json()
        assert data["current"] == "main"
        assert "main" in data["branches"]


class TestGraphEndpoint:
    """Tests for /api/graph endpoint."""

    def test_get_graph_empty(self, web_client):
        """Test getting graph from fresh memov."""
        response = web_client.get("/api/graph")
        assert response.status_code == 200
        data = response.json()
        assert "nodes" in data
        assert "edges" in data
        assert "current_branch" in data

    def test_get_graph_with_data(self, web_client_with_data):
        """Test graph contains node data including agent_plan."""
        response = web_client_with_data.get("/api/graph")
        assert response.status_code == 200
        data = response.json()

        assert len(data["nodes"]) >= 2
        assert data["current_branch"] == "main"

        # Check node structure
        node = data["nodes"][0]
        assert "id" in node
        assert "short_hash" in node
        assert "operation" in node
        assert "prompt" in node
        assert "response" in node
        assert "agent_plan" in node
        assert "files" in node

    def test_graph_edges_structure(self, web_client_with_data):
        """Test edges represent parent relationships."""
        response = web_client_with_data.get("/api/graph")
        data = response.json()

        # With 2+ commits, should have at least 1 edge
        if len(data["nodes"]) >= 2:
            assert len(data["edges"]) >= 1
            edge = data["edges"][0]
            assert "from" in edge
            assert "to" in edge


class TestCommitEndpoint:
    """Tests for /api/commit/{commit_hash} endpoint."""

    def test_get_commit_not_found(self, web_client):
        """Test 404 for non-existent commit."""
        response = web_client.get("/api/commit/nonexistent")
        assert response.status_code == 404

    def test_get_commit_by_hash(self, web_client_with_data):
        """Test getting commit details by hash."""
        # First get a valid hash from graph
        graph_response = web_client_with_data.get("/api/graph")
        nodes = graph_response.json()["nodes"]
        if not nodes:
            pytest.skip("No nodes in graph")

        commit_hash = nodes[0]["short_hash"]
        response = web_client_with_data.get(f"/api/commit/{commit_hash}")
        assert response.status_code == 200

        data = response.json()
        assert "commit_hash" in data
        assert "prompt" in data
        assert "response" in data
        assert "agent_plan" in data


class TestDiffEndpoint:
    """Tests for /api/diff/{commit_hash} endpoint."""

    def test_get_diff(self, web_client_with_data):
        """Test getting diff for a commit."""
        # Get a valid hash first
        graph_response = web_client_with_data.get("/api/graph")
        nodes = graph_response.json()["nodes"]
        if not nodes:
            pytest.skip("No nodes in graph")

        commit_hash = nodes[0]["short_hash"]
        response = web_client_with_data.get(f"/api/diff/{commit_hash}")
        assert response.status_code == 200

        data = response.json()
        assert "commit_hash" in data
        assert "diff" in data


class TestJumpEndpoint:
    """Tests for /api/jump/{commit_hash} endpoint."""

    def test_jump_to_commit(self, web_client_with_data, temp_project):
        """Test jumping to a specific commit."""
        # Get graph to find a commit to jump to
        graph_response = web_client_with_data.get("/api/graph")
        nodes = graph_response.json()["nodes"]
        if len(nodes) < 2:
            pytest.skip("Need at least 2 commits to test jump")

        # Jump to the older commit (index 1 since 0 is newest)
        target_hash = nodes[1]["short_hash"]
        response = web_client_with_data.post(f"/api/jump/{target_hash}")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert "new_branch" in data


class TestIndexPage:
    """Tests for serving the index page."""

    def test_serve_index(self, web_client):
        """Test that index.html is served at root."""
        response = web_client.get("/")
        # May be 200 or 404 depending on whether static files exist
        assert response.status_code in [200, 404]


class TestJumpParentRelationship:
    """Tests for verifying parent relationships after jump."""

    def test_snap_after_jump_has_correct_parent(
        self, web_client_with_data, temp_project, memov_with_snapshots
    ):
        """Test that a snap after jump uses jumped-to commit as parent."""
        # Get graph before jump
        graph_before = web_client_with_data.get("/api/graph").json()
        nodes = graph_before["nodes"]
        if len(nodes) < 2:
            pytest.skip("Need at least 2 commits to test jump parent")

        # Find the commit hashes - nodes[0] is newest, nodes[-1] is oldest
        # We'll jump to an older commit
        target_commit = nodes[-1]["id"]  # Jump to oldest
        newest_before_jump = nodes[0]["id"]

        # Jump to the older commit
        response = web_client_with_data.post(f"/api/jump/{target_commit}")
        assert response.status_code == 200
        assert response.json()["status"] == "success"

        # Make a change and create new snapshot
        (temp_project / "test.py").write_text("# After jump\nprint('new code')\n")
        memov_with_snapshots.snapshot(
            prompt="Change after jump",
            response="Made changes after jumping",
            by_user=False,
        )

        # Get graph after snap
        graph_after = web_client_with_data.get("/api/graph").json()

        # Find the new commit (should be on jump/1 branch)
        branches = web_client_with_data.get("/api/branches").json()
        new_branch = branches["current"]
        assert "jump" in new_branch

        # Find edges pointing to the new commit
        new_commit_tip = branches["branches"][new_branch]

        # Build parent lookup from edges
        child_to_parent = {}
        for edge in graph_after["edges"]:
            # edge: {"from": parent, "to": child}
            if edge["to"] not in child_to_parent:
                child_to_parent[edge["to"]] = edge["from"]

        # Verify the new commit's parent is the jumped-to commit
        assert (
            new_commit_tip in child_to_parent
        ), f"New commit {new_commit_tip[:7]} should have a parent edge"
        actual_parent = child_to_parent[new_commit_tip]
        assert actual_parent == target_commit, (
            f"New commit's parent should be {target_commit[:7]} (jumped-to), "
            f"but was {actual_parent[:7]}"
        )


class TestStatusEndpoint:
    """Tests for /api/status endpoint."""

    def test_status_initialized(self, web_client, temp_project):
        """Test status returns initialized=True for initialized memov."""
        response = web_client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert data["initialized"] is True
        assert data["project_path"] == str(temp_project)

    def test_status_not_initialized(self, temp_project):
        """Test status returns initialized=False for uninitialized project."""
        app = create_app(str(temp_project))
        client = TestClient(app)

        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert data["initialized"] is False
        assert data["project_path"] == str(temp_project)


class TestNotInitialized:
    """Tests for handling uninitialized memov."""

    def test_branches_not_initialized(self, temp_project):
        """Test error when memov not initialized."""
        app = create_app(str(temp_project))
        client = TestClient(app)

        response = client.get("/api/branches")
        assert response.status_code == 400
        assert "not initialized" in response.json()["detail"].lower()

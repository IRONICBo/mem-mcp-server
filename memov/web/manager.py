"""Web UI server process manager."""

import datetime
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import psutil

CONFIG_DIR = Path.home() / ".config" / "memov"
SERVERS_FILE = CONFIG_DIR / "ui_servers.json"


class UIManager:
    """Manages Web UI server processes for different projects."""

    @staticmethod
    def _ensure_config_dir():
        """Ensure config directory exists."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def load_servers() -> dict:
        """Load server registry from file."""
        UIManager._ensure_config_dir()
        if not SERVERS_FILE.exists():
            return {}
        try:
            with open(SERVERS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    @staticmethod
    def save_servers(servers: dict):
        """Save server registry to file."""
        UIManager._ensure_config_dir()
        with open(SERVERS_FILE, "w") as f:
            json.dump(servers, f, indent=2)

    @staticmethod
    def _normalize_path(project_path: str) -> str:
        """Normalize project path for consistent lookup."""
        return str(Path(project_path).resolve())

    @staticmethod
    def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
        """Check if a port is already in use."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return False
            except OSError:
                return True

    @staticmethod
    def is_process_running(pid: int) -> bool:
        """Check if a process is still running."""
        try:
            process = psutil.Process(pid)
            return process.is_running() and process.status() != psutil.STATUS_ZOMBIE
        except psutil.NoSuchProcess:
            return False

    @staticmethod
    def start(project_path: str, port: int = 38888, host: str = "127.0.0.1") -> tuple[bool, str]:
        """Start UI server for a project in background.

        Returns:
            (success, message) tuple
        """
        project_path = UIManager._normalize_path(project_path)

        # Check if project path exists
        if not os.path.exists(project_path):
            return False, f"Project path does not exist: {project_path}"

        # Check if already running for this project
        servers = UIManager.load_servers()
        if project_path in servers:
            info = servers[project_path]
            if UIManager.is_process_running(info["pid"]):
                return False, (
                    f"Server already running for {project_path}\n"
                    f"  URL: http://{info['host']}:{info['port']}\n"
                    f"  PID: {info['pid']}"
                )
            # Clean up stale entry
            del servers[project_path]

        # Check if port is in use
        if UIManager.is_port_in_use(port, host):
            return False, f"Port {port} is already in use"

        # Start server in background
        # Use python -m memov.web.launcher to start
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "memov.web.launcher",
                project_path,
                "--port",
                str(port),
                "--host",
                host,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

        # Wait a moment for server to start
        time.sleep(1.5)

        # Check if process is still running
        if process.poll() is not None:
            return False, "Server failed to start (process exited immediately)"

        # Verify by checking if port is now in use
        if not UIManager.is_port_in_use(port, host):
            # Give it another moment
            time.sleep(0.5)
            if not UIManager.is_port_in_use(port, host):
                process.terminate()
                return False, "Server failed to bind to port"

        # Save server info
        servers[project_path] = {
            "pid": process.pid,
            "port": port,
            "host": host,
            "project_path": project_path,
            "start_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "start_timestamp": datetime.datetime.now().timestamp(),
        }
        UIManager.save_servers(servers)

        return True, f"http://{host}:{port}"

    @staticmethod
    def stop(project_path: str) -> tuple[bool, str]:
        """Stop UI server for a project.

        Returns:
            (success, message) tuple
        """
        project_path = UIManager._normalize_path(project_path)
        servers = UIManager.load_servers()

        if project_path not in servers:
            return False, f"No server running for {project_path}"

        info = servers[project_path]
        pid = info["pid"]

        if not UIManager.is_process_running(pid):
            # Clean up stale entry
            del servers[project_path]
            UIManager.save_servers(servers)
            return True, "Server was not running (cleaned up stale entry)"

        try:
            process = psutil.Process(pid)
            # Terminate gracefully
            process.terminate()
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)

            # Remove from registry
            del servers[project_path]
            UIManager.save_servers(servers)
            return True, "Server stopped"

        except psutil.NoSuchProcess:
            del servers[project_path]
            UIManager.save_servers(servers)
            return True, "Server was not running"
        except Exception as e:
            return False, f"Failed to stop server: {e}"

    @staticmethod
    def status(project_path: Optional[str] = None) -> list[dict]:
        """Get status of running servers.

        Args:
            project_path: If provided, only return status for this project.
                         If None, return status for all servers.

        Returns:
            List of server status dicts
        """
        servers = UIManager.load_servers()
        result = []
        stale_keys = []

        for path, info in servers.items():
            if project_path and UIManager._normalize_path(project_path) != path:
                continue

            pid = info["pid"]
            is_running = UIManager.is_process_running(pid)

            if not is_running:
                stale_keys.append(path)
                continue

            # Calculate uptime
            start_ts = info.get("start_timestamp", 0)
            uptime_seconds = int(time.time() - start_ts) if start_ts else 0

            # Get memory usage
            try:
                process = psutil.Process(pid)
                memory_mb = process.memory_info().rss / 1024 / 1024
            except psutil.NoSuchProcess:
                memory_mb = 0

            result.append(
                {
                    "project_path": path,
                    "pid": pid,
                    "port": info["port"],
                    "host": info["host"],
                    "url": f"http://{info['host']}:{info['port']}",
                    "start_time": info.get("start_time", "unknown"),
                    "uptime_seconds": uptime_seconds,
                    "memory_mb": round(memory_mb, 1),
                    "status": "running",
                }
            )

        # Clean up stale entries
        if stale_keys:
            for key in stale_keys:
                del servers[key]
            UIManager.save_servers(servers)

        return result

    @staticmethod
    def format_uptime(seconds: int) -> str:
        """Format uptime in human readable format."""
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes}m {secs}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"

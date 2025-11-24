# Makefile for mem CLI tool
# Provides convenient commands for building, testing, and installing

.PHONY: help build install clean test dev release

help:
	@echo "Memov CLI Build Targets:"
	@echo "  make build        - Build binary for current platform"
	@echo "  make install      - Build and install system-wide"
	@echo "  make install-user - Build and install to ~/.local/bin"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make test         - Run tests"
	@echo "  make dev          - Install in development mode"
	@echo "  make release      - Create a release build"
	@echo ""
	@echo "Platform-specific builds:"
	@echo "  make build-linux  - Build for Linux (requires Docker)"
	@echo "  make build-macos  - Build for macOS"
	@echo "  make build-windows- Build for Windows (requires Wine/VM)"

# Build binary for current platform
build:
	@echo "Building mem binary..."
	@./build_binary.sh

# Build and install system-wide
install: build
	@echo "Installing to /usr/local/bin/mem..."
	@sudo cp dist/mem-* /usr/local/bin/mem
	@sudo chmod +x /usr/local/bin/mem
	@echo "Installation complete. Run 'mem --help' to verify."

# Build and install to user directory
install-user: build
	@echo "Installing to ~/.local/bin/mem..."
	@mkdir -p ~/.local/bin
	@cp dist/mem-* ~/.local/bin/mem
	@chmod +x ~/.local/bin/mem
	@echo "Installation complete."
	@echo "Make sure ~/.local/bin is in your PATH:"
	@echo "  export PATH=\"\$$HOME/.local/bin:\$$PATH\""

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build dist *.spec
	@rm -rf .pytest_cache .coverage htmlcov
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Clean complete."

# Run tests
test:
	@echo "Running tests..."
	@python3 -m pytest tests/ -v

# Install in development mode
dev:
	@echo "Installing in development mode..."
	@pip install -e ".[dev]"
	@pre-commit install
	@echo "Development setup complete."

# Create a release build with optimizations
release: clean
	@echo "Creating release build..."
	@PYINSTALLER_OPTIMIZE=1 ./build_binary.sh
	@echo "Release build complete."

# Build for Linux using Docker
build-linux:
	@echo "Building for Linux using Docker..."
	@docker run --rm -v $(PWD):/app -w /app python:3.12-slim bash -c "\
		apt-get update && apt-get install -y binutils && \
		pip install pyinstaller && \
		pip install -e . && \
		pyinstaller mem.spec --noconfirm"
	@echo "Linux build complete."

# Build for macOS (must run on macOS)
build-macos:
	@echo "Building for macOS..."
	@./build_binary.sh
	@echo "macOS build complete."

# Build for Windows (using Wine or requires Windows VM)
build-windows:
	@echo "Windows builds should be done on a Windows machine or CI/CD."
	@echo "See .github/workflows/build-binaries.yml for automated builds."

# Quick test of the built binary
test-binary:
	@echo "Testing built binary..."
	@dist/mem-* --help
	@dist/mem-* version
	@echo "Binary test passed."

# Update dependencies
update-deps:
	@echo "Updating dependencies..."
	@pip install --upgrade pip
	@pip install --upgrade -e ".[dev]"
	@echo "Dependencies updated."

#!/bin/bash
# Build script for creating mem binary locally
# Supports Linux, macOS (Intel and Apple Silicon), and Windows (via WSL or Git Bash)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detect platform
PLATFORM=$(uname -s)
ARCH=$(uname -m)

echo -e "${GREEN}Building mem binary for $PLATFORM ($ARCH)${NC}"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed${NC}"
    exit 1
fi

# Check Python version (requires 3.11+)
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]; }; then
    echo -e "${RED}Error: Python 3.11+ is required (current: $PYTHON_VERSION)${NC}"
    exit 1
fi

echo -e "${GREEN}Python version: $PYTHON_VERSION${NC}"

# Check if virtual environment exists, create if not
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -e . > /dev/null
pip install pyinstaller > /dev/null

# Clean previous build
echo -e "${YELLOW}Cleaning previous build...${NC}"
rm -rf build dist *.spec

# Build binary using the spec file or inline command
if [ -f "mem.spec" ]; then
    echo -e "${YELLOW}Building binary using mem.spec...${NC}"
    pyinstaller mem.spec --noconfirm
else
    echo -e "${YELLOW}Building binary using inline configuration...${NC}"
    pyinstaller --onefile \
        --name mem \
        --hidden-import=memov.core \
        --hidden-import=memov.utils \
        --hidden-import=memov.storage \
        --hidden-import=chromadb \
        --hidden-import=litellm \
        --collect-all chromadb \
        --collect-all litellm \
        --noconfirm \
        memov/main.py
fi

# Test the binary
echo -e "${YELLOW}Testing binary...${NC}"
chmod +x dist/mem
if dist/mem --help > /dev/null; then
    echo -e "${GREEN}Binary built successfully!${NC}"
else
    echo -e "${RED}Binary test failed${NC}"
    exit 1
fi

# Determine output filename based on platform
case "$PLATFORM" in
    Linux*)
        OUTPUT_NAME="mem-linux-$ARCH"
        ;;
    Darwin*)
        OUTPUT_NAME="mem-macos-$ARCH"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        OUTPUT_NAME="mem-windows-$ARCH.exe"
        ;;
    *)
        OUTPUT_NAME="mem-$PLATFORM-$ARCH"
        ;;
esac

# Rename binary
mv dist/mem "dist/$OUTPUT_NAME"

echo -e "${GREEN}Build complete!${NC}"
echo -e "Binary location: ${YELLOW}dist/$OUTPUT_NAME${NC}"
echo -e ""
echo -e "To install system-wide, run:"
echo -e "${YELLOW}  sudo cp dist/$OUTPUT_NAME /usr/local/bin/mem${NC}"
echo -e ""
echo -e "Or add to PATH manually:"
echo -e "${YELLOW}  export PATH=\$PATH:$(pwd)/dist${NC}"

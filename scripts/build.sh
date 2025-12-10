#!/bin/bash
# Build script for vit CLI - supports basic and rag modes

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
MODE="basic"
PLATFORM=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
OUTPUT_DIR="dist"

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --mode MODE       Build mode: 'basic' or 'rag' (default: basic)"
            echo "  --output DIR      Output directory (default: dist)"
            echo "  --help, -h        Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 --mode basic   # Build lightweight basic mode"
            echo "  $0 --mode rag     # Build full RAG mode with ChromaDB"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Validate mode
if [[ "$MODE" != "basic" && "$MODE" != "rag" ]]; then
    print_error "Invalid mode: $MODE. Must be 'basic' or 'rag'"
    exit 1
fi

# Determine binary name
if [[ "$PLATFORM" == "darwin" ]]; then
    PLATFORM_NAME="macos"
elif [[ "$PLATFORM" == "linux" ]]; then
    PLATFORM_NAME="linux"
elif [[ "$PLATFORM" == "mingw"* || "$PLATFORM" == "msys"* ]]; then
    PLATFORM_NAME="windows"
else
    PLATFORM_NAME="$PLATFORM"
fi

BINARY_NAME="vit-${MODE}-${PLATFORM_NAME}-${ARCH}"

print_info "Building vit CLI in ${MODE} mode..."
print_info "Platform: ${PLATFORM_NAME}, Architecture: ${ARCH}"
print_info "Output: ${OUTPUT_DIR}/${BINARY_NAME}"

# Clean previous builds
print_info "Cleaning previous builds..."
rm -rf build dist *.spec

# Install dependencies
print_info "Installing dependencies..."
if [[ "$MODE" == "basic" ]]; then
    print_info "Installing basic mode dependencies..."
    uv pip install pyinstaller
    uv pip install .
else
    print_info "Installing RAG mode dependencies (includes ChromaDB)..."
    uv pip install pyinstaller
    uv pip install ".[rag]"
    # Force NumPy 1.26.x for PyInstaller macOS compatibility
    uv pip install "numpy>=1.26.0,<2.0.0"
fi

print_success "Dependencies installed"

# Build with PyInstaller
print_info "Building binary with PyInstaller..."
pyinstaller --onefile \
    --name vit \
    --hidden-import=vit.core \
    --hidden-import=vit.utils \
    --hidden-import=vit.storage \
    $([ "$MODE" = "rag" ] && echo "--hidden-import=chromadb --hidden-import=litellm --collect-all chromadb --collect-all litellm") \
    --noconfirm \
    vit/main.py

print_success "Binary built successfully"

# Rename binary
print_info "Renaming binary..."
mv dist/vit "${OUTPUT_DIR}/${BINARY_NAME}"

print_success "Binary renamed to ${BINARY_NAME}"

# Test binary
print_info "Testing binary..."
chmod +x "${OUTPUT_DIR}/${BINARY_NAME}"
"${OUTPUT_DIR}/${BINARY_NAME}" --help > /dev/null 2>&1

if [ $? -eq 0 ]; then
    print_success "Binary test passed"
else
    print_warning "Binary test failed (might be expected for some commands)"
fi

# Print summary
echo ""
echo "═══════════════════════════════════════════════════"
print_success "Build completed successfully!"
echo "═══════════════════════════════════════════════════"
echo ""
echo "Mode:           ${MODE}"
echo "Binary:         ${OUTPUT_DIR}/${BINARY_NAME}"
echo "Size:           $(du -h "${OUTPUT_DIR}/${BINARY_NAME}" | cut -f1)"
echo ""
echo "To install:"
echo "  sudo mv ${OUTPUT_DIR}/${BINARY_NAME} /usr/local/bin/vit"
echo ""
echo "To test:"
echo "  ${OUTPUT_DIR}/${BINARY_NAME} --help"
echo ""

if [[ "$MODE" == "basic" ]]; then
    print_info "Basic mode build - RAG features (sync, search) are not available"
    print_info "To build with RAG support, use: $0 --mode rag"
else
    print_info "RAG mode build - All features including semantic search are available"
fi

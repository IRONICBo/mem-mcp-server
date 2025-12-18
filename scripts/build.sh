#!/bin/bash
# Build script for memov CLI - supports basic and rag modes
# Optimized for fast startup on macOS

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
MODE="basic"
PACK_MODE="onedir"  # onedir (fast startup) or onefile (single binary)
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
        --pack)
            PACK_MODE="$2"
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
            echo "  --pack PACK       Pack mode: 'onedir' (fast, recommended) or 'onefile' (single binary)"
            echo "  --output DIR      Output directory (default: dist)"
            echo "  --help, -h        Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 --mode basic              # Fast startup, lightweight"
            echo "  $0 --mode basic --pack onefile  # Single binary (slower startup)"
            echo "  $0 --mode rag                # RAG mode with ChromaDB"
            echo ""
            echo "Performance Notes:"
            echo "  - onedir mode: ~200-300ms startup (recommended)"
            echo "  - onefile mode: ~1-2s startup (needs to extract each run)"
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

if [[ "$PACK_MODE" != "onedir" && "$PACK_MODE" != "onefile" ]]; then
    print_error "Invalid pack mode: $PACK_MODE. Must be 'onedir' or 'onefile'"
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

BINARY_NAME="mem-${MODE}-${PLATFORM_NAME}-${ARCH}"

print_info "Building memov CLI in ${MODE} mode (${PACK_MODE})..."
print_info "Platform: ${PLATFORM_NAME}, Architecture: ${ARCH}"
print_info "Output: ${OUTPUT_DIR}/${BINARY_NAME}"

# Clean previous builds
print_info "Cleaning previous builds..."
rm -rf build dist

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

# Check if mem.spec exists and use it for onedir mode
if [[ "$PACK_MODE" == "onedir" && -f "mem.spec" ]]; then
    print_info "Using optimized mem.spec for onedir build..."
    if [[ "$MODE" == "rag" ]]; then
        RAG_MODE=1 pyinstaller mem.spec --noconfirm
    else
        RAG_MODE=0 pyinstaller mem.spec --noconfirm
    fi

    # The spec file creates mem-basic or mem-rag directory
    BUILT_DIR="dist/mem-${MODE}"
else
    # Fallback to inline configuration for onefile mode
    print_info "Building with inline configuration (${PACK_MODE} mode)..."

    # Common excludes for faster startup
    EXCLUDES="--exclude-module pytest --exclude-module unittest --exclude-module IPython"
    EXCLUDES="$EXCLUDES --exclude-module matplotlib --exclude-module scipy --exclude-module pandas"
    EXCLUDES="$EXCLUDES --exclude-module tkinter --exclude-module PIL --exclude-module cv2"
    EXCLUDES="$EXCLUDES --exclude-module torch --exclude-module tensorflow"

    if [[ "$PACK_MODE" == "onefile" ]]; then
        PACK_FLAG="--onefile"
    else
        PACK_FLAG="--onedir"
    fi

    pyinstaller $PACK_FLAG \
        --name mem \
        --strip \
        --hidden-import=memov.core \
        --hidden-import=memov.utils \
        --hidden-import=memov.storage \
        --hidden-import=typer \
        --hidden-import=click \
        --hidden-import=rich \
        $EXCLUDES \
        $([ "$MODE" = "rag" ] && echo "--hidden-import=chromadb --hidden-import=litellm --collect-all chromadb") \
        --noconfirm \
        memov/main.py

    BUILT_DIR="dist"
fi

print_success "Binary built successfully"

# Handle output based on pack mode
if [[ "$PACK_MODE" == "onedir" ]]; then
    # For onedir, we have a directory
    if [[ -d "dist/mem-${MODE}" ]]; then
        mv "dist/mem-${MODE}" "${OUTPUT_DIR}/${BINARY_NAME}"
    elif [[ -d "dist/mem" ]]; then
        mv "dist/mem" "${OUTPUT_DIR}/${BINARY_NAME}"
    fi
    FINAL_PATH="${OUTPUT_DIR}/${BINARY_NAME}/mem"
    chmod +x "$FINAL_PATH"

    # Create a convenience wrapper script
    cat > "${OUTPUT_DIR}/${BINARY_NAME}.sh" << 'WRAPPER'
#!/bin/bash
# Wrapper script for mem CLI
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPT_DIR/$(basename "$0" .sh)/mem" "$@"
WRAPPER
    chmod +x "${OUTPUT_DIR}/${BINARY_NAME}.sh"

    print_info "Created directory: ${OUTPUT_DIR}/${BINARY_NAME}/"
    print_info "Wrapper script: ${OUTPUT_DIR}/${BINARY_NAME}.sh"
else
    # For onefile, rename the binary
    mv dist/mem "${OUTPUT_DIR}/${BINARY_NAME}"
    chmod +x "${OUTPUT_DIR}/${BINARY_NAME}"
    FINAL_PATH="${OUTPUT_DIR}/${BINARY_NAME}"
fi

# Test binary
print_info "Testing binary..."
if "$FINAL_PATH" --help > /dev/null 2>&1; then
    print_success "Binary test passed"
else
    print_warning "Binary test failed (might be expected for some commands)"
fi

# Measure startup time
print_info "Measuring startup time..."
START_TIME=$(python3 -c "import time; print(time.time())")
"$FINAL_PATH" --help > /dev/null 2>&1
END_TIME=$(python3 -c "import time; print(time.time())")
STARTUP_MS=$(python3 -c "print(int(($END_TIME - $START_TIME) * 1000))")
print_info "Startup time: ${STARTUP_MS}ms"

# Print summary
echo ""
echo "═══════════════════════════════════════════════════"
print_success "Build completed successfully!"
echo "═══════════════════════════════════════════════════"
echo ""
echo "Mode:           ${MODE}"
echo "Pack:           ${PACK_MODE}"
echo "Startup time:   ${STARTUP_MS}ms"

if [[ "$PACK_MODE" == "onedir" ]]; then
    echo "Directory:      ${OUTPUT_DIR}/${BINARY_NAME}/"
    echo "Binary:         ${FINAL_PATH}"
    echo "Size:           $(du -sh "${OUTPUT_DIR}/${BINARY_NAME}" | cut -f1)"
    echo ""
    echo "To install:"
    echo "  sudo cp -r ${OUTPUT_DIR}/${BINARY_NAME} /usr/local/lib/"
    echo "  sudo ln -sf /usr/local/lib/${BINARY_NAME}/mem /usr/local/bin/mem"
else
    echo "Binary:         ${FINAL_PATH}"
    echo "Size:           $(du -h "${FINAL_PATH}" | cut -f1)"
    echo ""
    echo "To install:"
    echo "  sudo mv ${FINAL_PATH} /usr/local/bin/mem"
fi
echo ""
echo "To test:"
echo "  ${FINAL_PATH} --help"
echo ""

if [[ "$MODE" == "basic" ]]; then
    print_info "Basic mode build - RAG features (sync, search) are not available"
    print_info "To build with RAG support, use: $0 --mode rag"
else
    print_info "RAG mode build - All features including semantic search are available"
fi

if [[ "$PACK_MODE" == "onefile" ]]; then
    print_warning "onefile mode has slower startup (~1-2s). Use --pack onedir for faster startup."
fi

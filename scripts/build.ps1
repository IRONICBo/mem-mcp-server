# Build script for memov CLI - supports basic and rag modes (PowerShell)

param(
    [string]$Mode = "basic",
    [string]$OutputDir = "dist",
    [switch]$Help
)

# Colors
function Write-Info { Write-Host "ℹ $args" -ForegroundColor Blue }
function Write-Success { Write-Host "✓ $args" -ForegroundColor Green }
function Write-Warning { Write-Host "⚠ $args" -ForegroundColor Yellow }
function Write-Error { Write-Host "✗ $args" -ForegroundColor Red }

# Show help
if ($Help) {
    Write-Host "Usage: .\build.ps1 [OPTIONS]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Mode MODE        Build mode: 'basic' or 'rag' (default: basic)"
    Write-Host "  -OutputDir DIR    Output directory (default: dist)"
    Write-Host "  -Help             Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\build.ps1 -Mode basic   # Build lightweight basic mode"
    Write-Host "  .\build.ps1 -Mode rag     # Build full RAG mode with ChromaDB"
    exit 0
}

# Validate mode
if ($Mode -ne "basic" -and $Mode -ne "rag") {
    Write-Error "Invalid mode: $Mode. Must be 'basic' or 'rag'"
    exit 1
}

# Determine architecture
$Arch = if ([System.Environment]::Is64BitOperatingSystem) { "x86_64" } else { "x86" }
$BinaryName = "mem-$Mode-windows-$Arch.exe"

Write-Info "Building memov CLI in $Mode mode..."
Write-Info "Platform: Windows, Architecture: $Arch"
Write-Info "Output: $OutputDir\$BinaryName"

# Clean previous builds
Write-Info "Cleaning previous builds..."
Remove-Item -Path "build", "dist", "*.spec" -Recurse -Force -ErrorAction SilentlyContinue

# Install dependencies
Write-Info "Installing dependencies..."
if ($Mode -eq "basic") {
    Write-Info "Installing basic mode dependencies..."
    uv pip install pyinstaller
    uv pip install .
} else {
    Write-Info "Installing RAG mode dependencies (includes ChromaDB)..."
    uv pip install pyinstaller
    uv pip install ".[rag]"
    # Force NumPy 1.26.x for PyInstaller compatibility
    uv pip install "numpy>=1.26.0,<2.0.0"
}

Write-Success "Dependencies installed"

# Build with PyInstaller
Write-Info "Building binary with PyInstaller..."

$PyInstallerArgs = @(
    "--onefile",
    "--name", "mem",
    "--hidden-import=memov.core",
    "--hidden-import=memov.utils",
    "--hidden-import=memov.storage"
)

if ($Mode -eq "rag") {
    $PyInstallerArgs += @(
        "--hidden-import=chromadb",
        "--hidden-import=litellm",
        "--collect-all", "chromadb",
        "--collect-all", "litellm"
    )
}

$PyInstallerArgs += @("--noconfirm", "memov/main.py")

pyinstaller @PyInstallerArgs

Write-Success "Binary built successfully"

# Rename binary
Write-Info "Renaming binary..."
Move-Item "dist\mem.exe" "$OutputDir\$BinaryName" -Force

Write-Success "Binary renamed to $BinaryName"

# Test binary
Write-Info "Testing binary..."
$TestResult = & "$OutputDir\$BinaryName" --help 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Success "Binary test passed"
} else {
    Write-Warning "Binary test failed (might be expected for some commands)"
}

# Print summary
Write-Host ""
Write-Host "═══════════════════════════════════════════════════"
Write-Success "Build completed successfully!"
Write-Host "═══════════════════════════════════════════════════"
Write-Host ""
Write-Host "Mode:           $Mode"
Write-Host "Binary:         $OutputDir\$BinaryName"
Write-Host "Size:           $((Get-Item "$OutputDir\$BinaryName").Length / 1MB) MB"
Write-Host ""
Write-Host "To install:"
Write-Host "  Move $OutputDir\$BinaryName to a directory in your PATH"
Write-Host ""
Write-Host "To test:"
Write-Host "  $OutputDir\$BinaryName --help"
Write-Host ""

if ($Mode -eq "basic") {
    Write-Info "Basic mode build - RAG features (sync, search) are not available"
    Write-Info "To build with RAG support, use: .\build.ps1 -Mode rag"
} else {
    Write-Info "RAG mode build - All features including semantic search are available"
}

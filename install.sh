#!/usr/bin/env bash

# Folder Sorter CLI installer script for macOS and Linux.

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}====================================================${NC}"
echo -e "${CYAN}      Installing Folder Sorter CLI...              ${NC}"
echo -e "${CYAN}====================================================${NC}"

# Check for python3
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}Error: Python 3 is required but was not found on your system.${NC}"
    echo -e "${RED}Please install Python 3.8 or higher and try again.${NC}"
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "Found Python ${PY_VERSION}..."

INSTALL_DIR="$HOME/.folder-sorter"
BIN_DIR="$HOME/.local/bin"

echo -e "Creating environment under ${INSTALL_DIR}..."
mkdir -p "$INSTALL_DIR"

# Check if python3-venv works, if not print troubleshooting
if ! python3 -m venv "$INSTALL_DIR/venv" 2>/dev/null; then
    echo -e "${RED}Error: Failed to create a virtual environment.${NC}"
    echo -e "${YELLOW}On Debian/Ubuntu systems, you may need to run: sudo apt install python3-venv${NC}"
    exit 1
fi

# Detect installation source pathh
if [ -f "./pyproject.toml" ]; then
    echo -e "Installing from local repository directory..."
    SRC_PATH=$(pwd)
else
    echo -e "Downloading Folder Sorter source from GitHub..."
    SRC_PATH="$INSTALL_DIR/src"
    if [ -d "$SRC_PATH" ]; then
        rm -rf "$SRC_PATH"
    fi
    if ! command -v git &>/dev/null; then
        echo -e "${RED}Error: git is required to clone the source code.${NC}"
        exit 1
    fi
    git clone https://github.com/Debanjan110d/Folder-Sorter.git "$SRC_PATH"
fi

# Upgrade pip and install
echo -e "Installing package dependencies..."
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip --quiet
"$INSTALL_DIR/venv/bin/pip" install "$SRC_PATH" --quiet

# Link binary executable to ~/.local/bin
echo -e "Registering executable..."
mkdir -p "$BIN_DIR"
ln -sf "$INSTALL_DIR/venv/bin/folder-sorter" "$BIN_DIR/folder-sorter"

# Autocomplete setup
if command -v folder-sorter &>/dev/null || [ -f "$BIN_DIR/folder-sorter" ]; then
    echo -e "Setting up shell completions..."
    # Attempt to install completion for current shell, failing silently if shell cannot be determined
    "$BIN_DIR/folder-sorter" --install-completion 2>/dev/null || true
fi

echo -e "\n${GREEN}Successfully installed Folder Sorter!${NC}"
echo -e "${CYAN}====================================================${NC}"

# Verify PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}Warning: ${BIN_DIR} is not in your PATH variable.${NC}"
    echo -e "Please add the following line to your shell profile (~/.bashrc, ~/.zshrc, or ~/.bash_profile):"
    echo -e "\n    ${CYAN}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}\n"
    echo -e "Then reload your profile with: ${CYAN}source ~/.bashrc${NC} (or equivalent)"
else
    echo -e "Running diagnostics..."
    "$BIN_DIR/folder-sorter" doctor
fi

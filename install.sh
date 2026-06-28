#!/usr/bin/env bash

# Folder Sorter CLI installer script for macOS and Linux (Production Binary-Only).

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}====================================================${NC}"
echo -e "${CYAN}      Installing Folder Sorter CLI...              ${NC}"
echo -e "${CYAN}====================================================${NC}"

# Detect OS
OS_TYPE=$(uname -s)
if [ "$OS_TYPE" = "Darwin" ]; then
    ASSET_NAME="folder-sorter-macos.tar.gz"
elif [ "$OS_TYPE" = "Linux" ]; then
    ASSET_NAME="folder-sorter-linux.tar.gz"
else
    echo -e "${RED}Error: Unsupported Operating System: ${OS_TYPE}${NC}"
    exit 1
fi

# Query latest release tag from GitHub API
echo -e "Fetching latest release information..."
LATEST_RELEASE_JSON=$(curl -s https://api.github.com/repos/Debanjan110d/Folder-Sorter/releases/latest)

# Handle cases where the API call fails or rate-limited or repo has no releases yet
TAG_NAME=$(echo "$LATEST_RELEASE_JSON" | grep -o '"tag_name": "[^"]*' | grep -o '[^"]*$')

if [ -z "$TAG_NAME" ]; then
    # Fallback to a default tag if GitHub API fails
    TAG_NAME="v1.0.0"
    echo -e "${YELLOW}Warning: Could not parse tag from GitHub API. Defaulting to ${TAG_NAME}.${NC}"
fi

DOWNLOAD_URL="https://github.com/Debanjan110d/Folder-Sorter/releases/download/${TAG_NAME}/${ASSET_NAME}"

echo -e "Latest release tag found: ${GREEN}${TAG_NAME}${NC}"
echo -e "Downloading prebuilt binary from: ${CYAN}${DOWNLOAD_URL}${NC}"

# Setup temp dir for extraction
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

# Download asset
if ! curl -fsSL "$DOWNLOAD_URL" -o "$TEMP_DIR/$ASSET_NAME"; then
    echo -e "${RED}Error: Failed to download release asset from GitHub.${NC}"
    echo -e "${YELLOW}Please verify that a release exists at: https://github.com/Debanjan110d/Folder-Sorter/releases${NC}"
    exit 1
fi

# Extract binary
echo -e "Extracting binary..."
tar -xzf "$TEMP_DIR/$ASSET_NAME" -C "$TEMP_DIR"

BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

# Move executable
echo -e "Registering executable..."
mv "$TEMP_DIR/folder-sorter" "$BIN_DIR/folder-sorter"
chmod +x "$BIN_DIR/folder-sorter"

# Attempt autocomplete installation (failing silently if not supported)
"$BIN_DIR/folder-sorter" --install-completion 2>/dev/null || true

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

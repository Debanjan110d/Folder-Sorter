#!/usr/bin/env bash

# Folder Sorter CLI uninstaller script for macOS and Linux.

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}====================================================${NC}"
echo -e "${YELLOW}      Uninstalling Folder Sorter CLI...            ${NC}"
echo -e "${YELLOW}====================================================${NC}"

BIN_PATH="$HOME/.local/bin/folder-sorter"

if [ -f "$BIN_PATH" ]; then
    echo -e "Removing executable at ${BIN_PATH}..."
    rm -f "$BIN_PATH"
    echo -e "${GREEN}Removed folder-sorter executable.${NC}"
else
    echo -e "folder-sorter executable not found at ${BIN_PATH}."
fi

# Optional clean up config
echo -e "\nNote: Global configurations and history stored at ~/.folder-sorter were left untouched."
echo -e "If you want to remove them completely, run: rm -rf ~/.folder-sorter"

echo -e "\n${GREEN}Uninstall complete. Folder Sorter has been removed.${NC}"
echo -e "${YELLOW}====================================================${NC}"

# Folder Sorter CLI

A professional cross-platform Command Line Interface (CLI) tool to organize messy folders with ease.

For a detailed guide on the CLI menus, commands, config settings, and architecture, check out the [CLI Reference Guide](docs/CLI_REFERENCE.md). To see what technologies are used under the hood explained in simple English, check out [Technology Details](docs/TECH_DETAILS.md).

---

## Features

- **Smart Sorting** — Automatically categorizes files into subfolders by type (Images, Videos, Documents, etc.).
- **Pillow-Powered Image Sorting** — Analyzes images to sort them by type (JPG, PNG, WEBP, etc.) and resolution (4K, 1080p, 720p, etc.).
- **Chronological Sorting** — Groups files into subfolders by year and month.
- **Robust Undo Support** — Sequentially reverses the last sort execution, restoring files to their original directories.
- **Dry Run Support** — Preview what files would be moved before executing.
- **Recursive Sorting** — Traverse nested directories recursively, cleaning up nested files.
- **Global Config & History** — Saves files and history under `~/.folder-sorter/` so you can view configuration or undo sorts globally.
- **Doctor Check** — Run environment health and write permission diagnostics.

---

## Platform Support

```
Windows x64      ✅ Supported
Linux x64        🚧 Planned
Linux ARM64      🚧 Planned
macOS Intel      🚧 Planned
Apple Silicon    🚧 Planned
```

---

## Installation

### Windows (Recommended)

To install Folder Sorter CLI on Windows without needing Python, Git, or pip, run the following command in PowerShell (as a normal user, no administrator permissions required):

```powershell
irm https://folder-sorter.vercel.app/install.ps1 | iex
```

This command automatically downloads the latest stable Windows release, extracts the binary to `%LOCALAPPDATA%\FolderSorter\`, adds it to your user `PATH`, runs system diagnostics, and registers command autocompletions for PowerShell.

### Alternative Installation (Development Mode)

If you are developing or want to install from source:

1. Clone or navigate to the project directory.
2. Install the package in editable development mode (or standard mode):

```powershell
pip install -e .
```

*Note: Do not include the `$` symbol when typing commands into PowerShell.*

---

## How to Run & Modes of Operation

Folder Sorter can be run in two different modes depending on how you invoke it:

### 1. Interactive Menu Mode (Default)
If you run `folder-sorter` without any subcommands, it starts a persistent, beautiful interactive menu loop in your terminal:

```powershell
folder-sorter
```

This presents a colored menu of options:
- **Smart Sort**
- **Sort By Month**
- **Undo Last Sort**
- **Diagnostics Doctor**
- **Configure Mappings**

When you choose to sort, the tool prompts you to select either the **current directory** or enter a **custom folder path** (validating that the path is an actual existing directory), and walks you through recursive and dry-run preferences.

---

### 2. Command Line Subcommands (Direct Execution)
Once installed, use the `folder-sorter` command directly with subcommands from any terminal window.

### 1. Show General Help
To see all available commands and options, run:
```powershell
folder-sorter --help
```

To view the CLI version:
```powershell
folder-sorter --version
```

---

### 2. Sort Directories (`sort`)
Organize files in the target directory (defaults to the current directory `.`).

```powershell
folder-sorter sort [DIRECTORY_PATH] [OPTIONS]
```

**Options:**
- `-m, --mode [by-type|by-date]` : Specify sorting type. Defaults to `by-type`.
- `-d, --dry-run` : Preview moves in the console without modifying files.
- `-r, --recursive` : Recursively scan and sort files in subdirectories.
- `-v, --verbose` : Print every file move operation details.

**Examples:**
```powershell
# Perform a dry-run recursive sort of the current directory
folder-sorter sort --dry-run --recursive

# Sort your Downloads folder by category types
folder-sorter sort C:\Users\User\Downloads

# Sort a folder recursively by modification date
folder-sorter sort C:\Users\User\Documents --mode by-date --recursive
```

---

### 3. Undo Last Sort (`undo`)
Reverse the most recent sorting run, returning all files to their original locations.

```powershell
folder-sorter undo [OPTIONS]
```

**Options:**
- `-d, --dry-run` : Preview what files would be restored without moving them.

**Examples:**
```powershell
# Preview restoration of the last run
folder-sorter undo --dry-run

# Run the actual undo
folder-sorter undo
```

---

### 4. Diagnostics Checks (`doctor`)
Perform environment status checks, check Python and Pillow dependencies, and test file-system read/write permissions.

```powershell
folder-sorter doctor
```

---

### 5. Custom Configurations (`config`)
Manage the file extensions mapped to folders. Custom mappings are stored globally at `~/.folder-sorter/config.json`.

```powershell
# View active extension mappings
folder-sorter config show

# Add an extension to a category (e.g. add '.go' to Code category)
folder-sorter config add Code .go

# Remove an extension from a category
folder-sorter config remove Code .go
```

---

## Troubleshooting

### PATH Issues
If the command `folder-sorter` is not recognized after a successful installation:
1. **Restart your terminal:** Close all open terminal or PowerShell windows and open a new one. The path changes only load upon terminal startup.
2. **Verify User PATH environment variable:** Ensure `%LOCALAPPDATA%\FolderSorter` is listed in your User `PATH`. You can check this by running in PowerShell:
   ```powershell
   [Environment]::GetEnvironmentVariable("PATH", "User")
   ```

### Antivirus False Positives
Since the Windows executable is packaged using PyInstaller, some antivirus programs might flag it as a false positive.
- If the installer fails to download or the binary is automatically quarantined, add an exception in your antivirus settings for the installation directory:
  `%LOCALAPPDATA%\FolderSorter`

### Installation Verification
To verify the installation was successful and you have the correct version:
1. Run the version command:
   ```powershell
   folder-sorter --version
   ```
2. Check that the executable is located in your local app data folder:
   `%LOCALAPPDATA%\FolderSorter\folder-sorter.exe`

### Running Diagnostics (`doctor`)
To run a full self-diagnostic check of the environment, permissions, and dependencies, run:
```powershell
folder-sorter doctor
```
If any diagnostic checks fail, follow the suggestions printed on the screen.
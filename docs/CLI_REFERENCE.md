# 📖 Folder Sorter CLI Reference Guide

This document provides a detailed, step-by-step explanation of the menu trees, command-line arguments, config structures, and operational features of Folder Sorter.

---

## 🗺️ Execution Mode Comparison

Folder Sorter runs in two execution modes depending on how it is invoked:

1. **Interactive Menu Mode:** Triggered by running `folder-sorter` with no arguments. It stays running in a persistent loop and walks the user through sorting options via a graphical terminal interface. Recommended for casual users.
2. **Direct CLI Mode:** Triggered by passing subcommands (e.g., `folder-sorter sort [PATH]`). It executes immediately and exits. Recommended for scripts, automation, and power users.

---

## 🧩 The "Extension Thing" Explained in Plain English

### What is a File Extension?
When you look at files on your computer, they have names like `vacation.jpg`, `notes.txt`, or `program.py`. 
The letters after the final dot (`.jpg`, `.txt`, `.py`) are the **file extension**. They indicate what type of file it is (an image, a document, code, etc.).

### How Folder Sorter Uses Them
Folder Sorter uses file extensions to figure out which folder a file belongs to. It keeps a list of extensions for each folder category.

Here is a step-by-step example of how it works:
1. You have a folder with these files:
   - `photo.jpg` (extension is `.jpg`)
   - `essay.txt` (extension is `.txt`)
   - `game.zip` (extension is `.zip`)
   - `weird_file.abc` (extension is `.abc`)
2. When you run **Smart Sort**:
   - It checks `.jpg` against the category lists. It finds `.jpg` in the **Images** list $\rightarrow$ moves `photo.jpg` to `Images/` folder.
   - It finds `.txt` in the **Documents** list $\rightarrow$ moves `essay.txt` to `Documents/` folder.
   - It finds `.zip` in the **Archives** list $\rightarrow$ moves `game.zip` to `Archives/` folder.
   - It looks for `.abc` in all lists. It is **not** in any category $\rightarrow$ moves `weird_file.abc` to `Others/` folder.

### Customizing Extensions
If you work with a file extension that Folder Sorter doesn't know about, you can add it! For example, if you want Go files (`.go`) to go into the **Code** folder instead of **Others**:
1. Select option `5` (Configure Mappings) in the menu, or run:
   ```powershell
   folder-sorter config add Code .go
   ```
2. Now, any `.go` file will be sent straight to the **Code** folder instead of **Others**.

---

## 🕹️ Interactive Menu Guide

The main menu is presented as follows:

```
╭─────────────────────────────────────────────╮
│ Folder Sorter CLI                           │
│ Organize and manage messy folders with ease │
╰─────────────────────────────────────────────╯
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Option ┃ Action / Command   ┃ Description                                         ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│   1    │ Smart Sort         │ Organize files by type categories (Images, etc.)    │
│   2    │ Sort By Month      │ Organize files chronologically by Year/Month        │
│   3    │ Undo Last Sort     │ Restore files moved during the last sorting run     │
│   4    │ Doctor Check       │ Check environment health, permissions & dependencies│
│   5    │ Configure Mappings │ View or customize file extension category mappings  │
│   6    │ CLI Reference      │ Show direct non-interactive terminal commands & flags│
│   0    │ Exit Program       │ Close the folder-sorter tool                        │
└────────┴────────────────────┴─────────────────────────────────────────────────────┘
```

### Option 1: Smart Sort (Sort by Category Type)
Organizes files based on their extension categories (Images, Videos, Documents, Archives, Code, Audio, etc.).
- **Step 1: Directory Choice**
  - Choose `1` to sort the current directory you launched the CLI from.
  - Choose `2` to specify a custom folder path (e.g. `C:\Users\User\Downloads`). The path is checked for existence before proceeding.
- **Step 2: Recursive Option**
  - Prompted to choose `y/n` for sorting subdirectories recursively. Recursion skips folders created by Folder Sorter (e.g., `Images`, `Documents`, etc.) to prevent infinite loop sorting.
- **Step 3: Dry-Run Option**
  - Choose `y/n` to perform a dry run. If enabled, it lists what files would be moved without executing actual changes.
- **Action Details:**
  - Standard files are placed directly under their respective category folders (e.g. `.zip` -> `Archives/`).
  - Image files (.jpg, .png, .webp, etc.) are processed via Pillow and placed into subfolders based on file type and resolution (e.g., `Images/PNG/1080p/image.png`).

---

### Option 2: Sort By Month (Sort by Creation Date)
Groups files chronologically based on their last modified time metadata.
- **Step 1: Directory Choice** (Current vs. Custom)
- **Step 2: Recursive Option** (`y/n`)
- **Step 3: Dry-Run Option** (`y/n`)
- **Action Details:**
  - Files are moved into a nested path: `[Year]/[Month Name]/filename` (e.g. `2026/June/file.txt`).
  - Like Smart Sort, recursive execution ignores existing year-organized folders.

---

### Option 3: Undo Last Sort Operation
Reverses the moves made in the most recent sorting run, restoring files back to their exact original directories (even if they were sorted recursively from nested folders).
- **Step 1: Dry-Run Option** (`y/n`)
  - Preview which files will be moved back and where they will go.
- **Action Details:**
  - Reads the latest run ID from `history.json` and processes all related files in reverse sequence to prevent path conflicts.
  - Clears only the undone run from the history file, leaving older runs intact for sequential undos.

---

### Option 4: Doctor Check (Diagnostics Check)
Performs an audit of the application environment to ensure everything operates correctly.
- **Audited Components:**
  1. **Python Version Check:** Verifies compatibility (must be >= Python 3.8).
  2. **Operating System Check:** Identifies platform specifications.
  3. **Global App Config Folder:** Checks read/write permissions for `~/.folder-sorter/`.
  4. **History Log Integrity:** Verifies `history.json` structure and counts stored operations/runs.
  5. **Pillow Library Check:** Assures Pillow is installed for sorting images by resolution.
  6. **Current Directory Permissions:** Assures folder read/write authorization is valid.

---

### Option 5: Configure File Mappings (Config Submenu)
Customizes mapping categories. Triggers a sub-menu:

```
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Option ┃ Action           ┃ Description                                         ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│   1    │ Show Mappings    │ List current extensions grouped under each category │
│   2    │ Add Extension    │ Register a new custom extension mapping             │
│   3    │ Remove Extension │ Deregister an extension mapping from a category     │
│   0    │ Back to Menu     │ Return to the main Folder Sorter menu               │
└────────┴──────────────────┴─────────────────────────────────────────────────────┘
```

- **Show Mappings:** Prints a clean layout table showing category names alongside their configured extensions. Also shows the config file path.
- **Add Extension:** Allows adding custom file extensions (e.g., adding `.go` to the `Code` category). Input validation automatically adds a prepended dot (`.`) if omitted and avoids duplicate additions.
- **Remove Extension:** Removes a specific extension from a category, reverting sorting behavior back to the `Others` folder default for that extension.

---

### Option 6: CLI Reference Guide
Prints the complete syntax guide for direct CLI commands and options in a clean format directly on the terminal. Useful for quick command lookup without leaving the menu.

---

## 🛠️ Direct CLI Command Reference

For terminal scripts or automations, the commands bypass the menu interface:

| Command | Option Flags | Description |
| :--- | :--- | :--- |
| `folder-sorter sort [DIR]` | `--mode`, `-m`, `--dry-run`, `-d`, `--recursive`, `-r`, `--verbose`, `-v` | Sorts directory files. |
| `folder-sorter undo` | `--dry-run`, `-d` | Reverses the last sorting operation. |
| `folder-sorter doctor` | None | Runs diagnostics checks. |
| `folder-sorter config show` | None | Lists configured extensions. |
| `folder-sorter config add [CAT] [EXT]` | None | Registers an extension mapping. |
| `folder-sorter config remove [CAT] [EXT]` | None | Deregisters an extension mapping. |

---

## 📂 Architecture and Settings Files

All application state is saved under your global user directory (`~/.folder-sorter/` or `C:\Users\YourUser\.folder-sorter/`):

1. **`config.json`**
   - Stores custom category mappings.
   - Example structure:
     ```json
     {
         "categories": {
             "Images": [".jpg", ".png", ".webp"],
             "Code": [".py", ".js", ".ts"]
         }
     }
     ```
2. **`history.json`**
   - Keeps log entries of moved files sorted by unique `run_id` timestamps.
   - Example entry:
     ```json
     [
         {
             "run_id": "9a0a0df2-132d-4519-aa57-3f30ca2414eb",
             "timestamp": "2026-06-28T01:00:00",
             "source": "C:\\Downloads\\script.py",
             "destination": "C:\\Downloads\\Code\\script.py"
         }
     ]
     ```

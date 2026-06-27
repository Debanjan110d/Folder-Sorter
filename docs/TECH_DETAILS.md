# 🛠️ Under the Hood: What is Used and What is Not

This file explains the tech stack and tools used in Folder Sorter CLI in simple, straight-forward English.

---

## 🟢 What is Used (And Why)

1. **Python**
   - **What it is:** The programming language used to write the entire tool.
   - **Why:** Python has powerful, simple libraries for working with files and folders.

2. **Typer**
   - **What it is:** A helper library that builds the command line system.
   - **Why:** It reads our code and automatically creates the subcommand flags (like `--recursive` or `--dry-run`) and handles `--help` information.

3. **Rich**
   - **What it is:** A terminal formatting library.
   - **Why:** It lets us print colors, drawing boxes (panels), tables, progress bars, and loading spinners directly inside your command line terminal.

4. **Pillow**
   - **What it is:** An image processing library.
   - **Why:** When sorting images, Folder Sorter opens the image file using Pillow to check its resolution (width and height in pixels) so it can automatically sort them into 4K, 1080p, or 720p folders.

5. **JSON Files**
   - **What it is:** Standard text files used to store data (`config.json` and `history.json`).
   - **Why:** They are simple to read, easy to write, and don't require any setup. They are saved in a hidden folder inside your user home directory: `~/.folder-sorter/`.

---

## 🔴 What is NOT Used (And Why)

1. **No Databases (like MySQL or SQLite)**
   - **Why:** Databases require complex installations and setups. We only need to store configuration extension lists and a basic list of moved files. Simple JSON text files are fast, clean, and require zero setup.

2. **No Web Browsers (like HTML, CSS, or React)**
   - **Why:** This is a terminal command line interface (CLI) tool. It doesn't run in a web browser. It runs inside PowerShell, Windows Terminal, or macOS/Linux Terminal.

3. **No Cloud / Servers**
   - **Why:** Folder Sorter runs 100% locally on your computer. It does not send your files, filenames, or directories to any server on the internet. It is safe, private, and works offline.

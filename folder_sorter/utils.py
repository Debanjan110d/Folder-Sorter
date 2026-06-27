import os
import shutil
import json
from pathlib import Path
import uuid
from datetime import datetime
from rich.console import Console

console = Console()

# Unique ID generated once per CLI execution run
RUN_ID = str(uuid.uuid4())
RUN_TIMESTAMP = datetime.now().isoformat()

def get_app_dir() -> Path:
    """Get the global configuration directory for folder-sorter."""
    app_dir = Path.home() / ".folder-sorter"
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir

def get_history_file() -> Path:
    """Get the global history file path."""
    return get_app_dir() / "history.json"

def ensure_folder(path):
    """Ensure that the target folder exists."""
    os.makedirs(path, exist_ok=True)

def initialize_history():
    """Initialize the global history file if it does not exist."""
    history_file = get_history_file()
    if not history_file.exists():
        with open(history_file, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)

def save_move(source, destination):
    """Record a file move operation in the global history file under the current run_id."""
    initialize_history()
    history_file = get_history_file()
    try:
        with open(history_file, "r", encoding="utf-8") as file:
            history = json.load(file)
    except Exception:
        history = []

    history.append({
        "run_id": RUN_ID,
        "timestamp": RUN_TIMESTAMP,
        "source": str(os.path.abspath(source)),
        "destination": str(os.path.abspath(destination))
    })

    with open(history_file, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

def move_file(source, destination, dry_run=False, verbose=False):
    """Move a file from source to destination, respecting dry_run and recording history."""
    file_name = os.path.basename(source)
    final_destination = os.path.join(destination, file_name)

    if dry_run:
        console.print(f"[yellow][DRY RUN][/yellow] Would move: [cyan]{source}[/cyan] -> [magenta]{final_destination}[/magenta]")
        return True

    # If already at destination, skip
    if os.path.abspath(source) == os.path.abspath(final_destination):
        return False

    try:
        ensure_folder(destination)
        save_move(source, final_destination)
        shutil.move(source, final_destination)
        if verbose:
            console.print(f"[green]Moved:[/green] [cyan]{os.path.basename(source)}[/cyan] -> [magenta]{os.path.relpath(destination)}[/magenta]")
        return True
    except Exception as e:
        console.print(f"[bold red]Error moving {source} to {destination}: {e}[/bold red]")
        return False
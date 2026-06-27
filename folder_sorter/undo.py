import json
import os
import shutil
from rich.console import Console
from folder_sorter.utils import get_history_file

console = Console()

def undo_last_sort(dry_run=False):
    """Reverses the moves from the latest sort operation, allowing sequential undos."""
    history_file = get_history_file()
    if not history_file.exists():
        console.print("[yellow]No history found.[/yellow]")
        return

    try:
        with open(history_file, "r", encoding="utf-8") as file:
            history = json.load(file)
    except Exception as e:
        console.print(f"[bold red]Error reading history file: {e}[/bold red]")
        return

    if not history:
        console.print("[yellow]Nothing to undo.[/yellow]")
        return

    # Find the latest run_id in the history
    latest_run_id = None
    for move in reversed(history):
        if "run_id" in move:
            latest_run_id = move["run_id"]
            break

    if not latest_run_id:
        # Fallback: if no run_id is found, undo all entries in history
        moves_to_undo = history
        remaining_history = []
    else:
        moves_to_undo = [m for m in history if m.get("run_id") == latest_run_id]
        remaining_history = [m for m in history if m.get("run_id") != latest_run_id]

    if not moves_to_undo:
        console.print("[yellow]Nothing to undo for the last run.[/yellow]")
        return

    action_word = "Would restore" if dry_run else "Restored"
    success_count = 0

    # Reverse order to avoid conflicts
    for move in reversed(moves_to_undo):
        source = move["source"]
        destination = move["destination"]

        if dry_run:
            console.print(f"[yellow][DRY RUN][/yellow] Would move: [cyan]{destination}[/cyan] -> [magenta]{source}[/magenta]")
            success_count += 1
            continue

        if not os.path.exists(destination):
            console.print(f"[yellow]Skipping (file not found at sorted location):[/yellow] {destination}")
            continue

        try:
            os.makedirs(os.path.dirname(source), exist_ok=True)
            shutil.move(destination, source)
            success_count += 1
        except Exception as e:
            console.print(f"[bold red]Error restoring {destination} -> {source}: {e}[/bold red]")

    # Update history file if not a dry-run
    if not dry_run:
        try:
            with open(history_file, "w", encoding="utf-8") as file:
                json.dump(remaining_history, file, indent=4)
        except Exception as e:
            console.print(f"[bold red]Failed to update history file: {e}[/bold red]")

    console.print(f"[bold green]{action_word} {success_count} file(s).[/bold green]")
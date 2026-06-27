import os
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.progress import track

from folder_sorter.utils import move_file
from folder_sorter.sorter import collect_files

console = Console()

def sort_by_month(folder_path, recursive=False, dry_run=False, verbose=False):
    """Sort files chronologically by year and month."""
    files = collect_files(folder_path, recursive)
    if not files:
        console.print("[yellow]No files to sort.[/yellow]")
        return

    moved_count = 0
    if dry_run or verbose:
        for file_path in files:
            full_path = str(file_path)
            try:
                modified_time = os.path.getmtime(full_path)
                date = datetime.fromtimestamp(modified_time)
                year = str(date.year)
                month = date.strftime("%B")
                destination = os.path.join(folder_path, year, month)
                if move_file(full_path, destination, dry_run=dry_run, verbose=verbose):
                    moved_count += 1
            except Exception as e:
                console.print(f"[bold red]Error reading file metadata for {full_path}: {e}[/bold red]")
    else:
        for file_path in track(files, description="[cyan]Sorting files by date...[/cyan]"):
            full_path = str(file_path)
            try:
                modified_time = os.path.getmtime(full_path)
                date = datetime.fromtimestamp(modified_time)
                year = str(date.year)
                month = date.strftime("%B")
                destination = os.path.join(folder_path, year, month)
                if move_file(full_path, destination, dry_run=dry_run, verbose=verbose):
                    moved_count += 1
            except Exception as e:
                console.print(f"[bold red]Error reading file metadata for {full_path}: {e}[/bold red]")

    action_word = "Would sort" if dry_run else "Successfully sorted"
    console.print(f"[bold green]{action_word} {moved_count} file(s).[/bold green]")
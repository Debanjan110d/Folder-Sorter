import sys
import os
import platform
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from folder_sorter.utils import get_app_dir, get_history_file

console = Console()

def check_permission(path: Path) -> bool:
    """Check if the path is readable and writeable."""
    if not path.exists():
        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception:
            return False
    return os.access(path, os.R_OK) and os.access(path, os.W_OK)

def run_diagnostics():
    """Run diagnostics checks for Folder Sorter CLI environment."""
    console.print(
        Panel.fit(
            "[bold green]Folder Sorter - Diagnostic Doctor[/bold green]\n"
            "[dim]Checking environment health and configurations...[/dim]",
            border_style="green"
        )
    )

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Check Component", style="white")
    table.add_column("Result / Details", style="white")
    table.add_column("Status", justify="center")

    # 1. Python Version
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_status = "[bold green]PASS[/bold green]" if sys.version_info >= (3, 8) else "[bold red]FAIL (Requires >= 3.8)[/bold red]"
    table.add_row("Python Version", py_ver, py_status)

    # 2. Operating System
    os_name = platform.system()
    os_release = platform.release()
    if os_name == "Windows" and os_release == "10":
        try:
            if sys.getwindowsversion().build >= 22000:
                os_release = "11"
        except AttributeError:
            pass
    os_info = f"{os_name} {os_release} ({platform.machine()})"
    table.add_row("Operating System", os_info, "[bold green]PASS[/bold green]")

    # 3. Global Config Directory Path
    app_dir = get_app_dir()
    app_dir_writeable = check_permission(app_dir)
    app_dir_status = "[bold green]PASS[/bold green]" if app_dir_writeable else "[bold red]FAIL (No Write Access)[/bold red]"
    table.add_row("Global App Config Folder", f"{app_dir} (Writeable: {app_dir_writeable})", app_dir_status)

    # 4. History File Check
    history_file = get_history_file()
    history_exists = history_file.exists()
    history_ok = True
    if history_exists:
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                import json
                history_data = json.load(f)
                num_moves = len(history_data)
                # Count unique runs
                unique_runs = len(set(m.get("run_id") for m in history_data if m.get("run_id")))
                hist_detail = f"Found history.json ({num_moves} operations across {unique_runs} runs)"
        except Exception as e:
            hist_detail = f"Corrupt history.json: {e}"
            history_ok = False
    else:
        hist_detail = "No history file yet (will be created automatically)"
    
    hist_status = "[bold green]PASS[/bold green]" if history_ok else "[bold red]CORRUPT[/bold red]"
    table.add_row("History Log Status", hist_detail, hist_status)

    # 5. Pillow Dependency
    try:
        from PIL import Image
        pillow_ver = getattr(Image, "__version__", "Installed")
        pillow_detail = f"Pillow version: {pillow_ver}"
        pillow_status = "[bold green]PASS[/bold green]"
    except ImportError:
        pillow_detail = "Pillow library not installed (Needed for image sorting)"
        pillow_status = "[bold red]FAIL[/bold red]"
    table.add_row("Pillow Library Check", pillow_detail, pillow_status)

    # 6. Current Directory Permissions
    current_dir = Path.cwd()
    curr_writeable = check_permission(current_dir)
    curr_status = "[bold green]PASS[/bold green]" if curr_writeable else "[bold yellow]WARN (Read-only)[/bold yellow]"
    table.add_row("Current Dir Permissions", f"{current_dir} (Writeable: {curr_writeable})", curr_status)

    console.print(table)
    console.print()

    # Determine overall status
    failures = []
    if sys.version_info < (3, 8):
        failures.append("Python version is less than 3.8.")
    if not app_dir_writeable:
        failures.append("No write permission to global app configuration directory.")
    if not history_ok:
        failures.append("History file is corrupted.")
    if pillow_status == "[bold red]FAIL[/bold red]":
        failures.append("Pillow is not installed or importable.")

    if failures:
        console.print("[bold red]Diagnostics found some issues:[/bold red]")
        for fail in failures:
            console.print(f" - [red]{fail}[/red]")
    else:
        console.print("[bold green]All checks passed! Folder Sorter CLI is ready to go.[/bold green]")

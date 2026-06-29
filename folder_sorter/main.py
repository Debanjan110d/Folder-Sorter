import sys
import time
import json
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

# Import local modules
from folder_sorter.sorter import sort_by_type
from folder_sorter.date_sorter import sort_by_month
from folder_sorter.undo import undo_last_sort
from folder_sorter.doctor import run_diagnostics
from folder_sorter.config import load_config, save_config, get_config_file

__version__ = "1.0.3"

def parse_version(version_str: str):
    """Helper to parse semantic version string into a tuple of integers."""
    clean_str = version_str.lstrip('v').split('-')[0]
    try:
        return tuple(int(x) for x in clean_str.split('.'))
    except ValueError:
        return (0, 0, 0)

def check_for_updates():
    """Check for updates from GitHub and print instructions if a new version is available."""
    console.print("[cyan]Checking for updates...[/cyan]")
    try:
        req = urllib.request.Request(
            "https://api.github.com/repos/Debanjan110d/Folder-Sorter/releases/latest",
            headers={"User-Agent": "Folder-Sorter-CLI"}
        )
        with urllib.request.urlopen(req, timeout=4.0) as response:
            data = json.loads(response.read().decode())
            latest_tag = data.get("tag_name", "")
            if not latest_tag:
                console.print("[yellow]Could not retrieve latest release version.[/yellow]")
                return

            current_ver = parse_version(__version__)
            latest_ver = parse_version(latest_tag)

            if latest_ver > current_ver:
                console.print(f"\n[bold yellow]Update Available![/bold yellow] Version [green]{latest_tag}[/green] is available (you have [dim]{__version__}[/dim]).")
                console.print("\nTo upgrade Folder Sorter to the latest version, run:")
                console.print("[bold cyan]Windows (PowerShell):[/bold cyan]")
                console.print("  [white]irm https://folder-sorter.vercel.app/install.ps1 | iex[/white]")
                console.print("[bold cyan]macOS / Linux:[/bold cyan]")
                console.print("  [white]curl -fsSL https://folder-sorter.vercel.app/install.sh | bash[/white]\n")
            else:
                console.print(f"[green]Folder Sorter is up to date (version {__version__}).[/green]")
    except Exception as e:
        console.print(f"[bold red]Failed to check for updates:[/bold red] {e}")

app = typer.Typer(
    name="folder-sorter",
    help="A professional cross-platform CLI tool to organize folders with ease.",
    no_args_is_help=False
)

config_app = typer.Typer(help="View or edit file extensions configuration.")

console = Console()

def version_callback(value: bool):
    if value:
        console.print(f"[bold cyan]Folder Sorter CLI[/bold cyan] version [green]{__version__}[/green]")
        raise typer.Exit()

@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit."
    )
):
    """A professional cross-platform CLI tool to organize folders with ease."""
    if ctx.invoked_subcommand is None:
        interactive_menu()

def run_loading_spinner(message: str, duration: float = 1.0):
    """Display a status loading animation."""
    with console.status(f"[cyan]{message}[/cyan]", spinner="dots"):
        time.sleep(duration)

def get_target_directory() -> Optional[Path]:
    """Prompt the user to sort the current directory or specify a custom path."""
    console.print("\n[bold yellow]Target Directory Selection:[/bold yellow]")
    console.print(f"  [cyan]1.[/cyan] Current working directory ([white]{Path.cwd()}[/white])")
    console.print("  [cyan]2.[/cyan] Specify a different custom folder path")
    
    choice = Prompt.ask("Choose target option", choices=["1", "2"], default="1")
    if choice == "1":
        return Path.cwd()
    
    while True:
        path_str = Prompt.ask("\nEnter target folder path (or 0 to cancel)").strip('"')
        if path_str == "0":
            console.print("[yellow]Operation cancelled.[/yellow]")
            return None
        
        path = Path(path_str)
        if path.exists() and path.is_dir():
            return path.resolve()
        else:
            console.print("[bold red]Error: The path does not exist or is not a directory. Please try again.[/bold red]")

def interactive_menu():
    """Main interactive terminal loop for Folder Sorter."""
    while True:
        console.clear()
        console.print(
            Panel.fit(
                "[bold cyan]Folder Sorter CLI[/bold cyan]\n"
                "[green]Organize and manage messy folders with ease[/green]",
                border_style="bright_blue"
            )
        )

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", justify="center", style="cyan")
        table.add_column("Action / Command", style="white")
        table.add_column("Description", style="dim white")

        table.add_row("1", "Smart Sort", "Organize files by type categories (Images, Code, etc.)")
        table.add_row("2", "Sort By Month", "Organize files chronologically by Year/Month")
        table.add_row("3", "Undo Last Sort", "Restore files moved during the last sorting run")
        table.add_row("4", "Doctor Check", "Check environment health, permissions & dependencies")
        table.add_row("5", "Configure Mappings", "View or customize file extension category mappings")
        table.add_row("6", "CLI Reference", "Show direct non-interactive terminal commands & flags")
        table.add_row("0", "Exit Program", "Close the folder-sorter tool")

        console.print(table)

        choice = Prompt.ask("\n[bold yellow]Choose option[/bold yellow]", choices=["0", "1", "2", "3", "4", "5", "6"])

        if choice == "0":
            console.print("\n[bold red]Exiting program. Goodbye![/bold red]")
            break

        elif choice == "1":
            directory = get_target_directory()
            if not directory:
                input("\nPress Enter to continue...")
                continue
            
            recursive = Confirm.ask("Sort subdirectories recursively?", default=False)
            dry_run = Confirm.ask("Perform a dry-run first (preview changes)?", default=False)
            
            console.print()
            run_loading_spinner("Analyzing directory files...")
            sort_by_type(str(directory), recursive=recursive, dry_run=dry_run, verbose=dry_run)
            input("\nPress Enter to continue...")

        elif choice == "2":
            directory = get_target_directory()
            if not directory:
                input("\nPress Enter to continue...")
                continue
            
            recursive = Confirm.ask("Sort subdirectories recursively?", default=False)
            dry_run = Confirm.ask("Perform a dry-run first (preview changes)?", default=False)
            
            console.print()
            run_loading_spinner("Analyzing file date metadata...")
            sort_by_month(str(directory), recursive=recursive, dry_run=dry_run, verbose=dry_run)
            input("\nPress Enter to continue...")

        elif choice == "3":
            dry_run = Confirm.ask("Perform a dry-run undo (preview changes)?", default=False)
            console.print()
            run_loading_spinner("Checking history log...")
            undo_last_sort(dry_run=dry_run)
            input("\nPress Enter to continue...")

        elif choice == "4":
            console.print()
            run_loading_spinner("Running diagnostics...")
            run_diagnostics()
            input("\nPress Enter to continue...")

        elif choice == "5":
            interactive_config_menu()

        elif choice == "6":
            console.print()
            run_loading_spinner("Loading CLI Reference...")
            console.print(
                Panel(
                    "[bold cyan]Direct CLI Mode Command Reference[/bold cyan]\n\n"
                    "For automated scripts or direct terminal runs, use these subcommands:\n\n"
                    "  [green]folder-sorter sort [DIR][/green]\n"
                    "    Sort directory files directly. Options:\n"
                    "      [cyan]-m, --mode [by-type|by-date][/cyan] : Sort mode (default: by-type)\n"
                    "      [cyan]-d, --dry-run[/cyan]                 : Preview moves without moving files\n"
                    "      [cyan]-r, --recursive[/cyan]               : Sort nested subdirectories\n"
                    "      [cyan]-v, --verbose[/cyan]                 : Print detailed move logs\n\n"
                    "  [green]folder-sorter undo[/green]\n"
                    "    Reverse the last sorting execution. Options:\n"
                    "      [cyan]-d, --dry-run[/cyan]                 : Preview restores without moving files\n\n"
                    "  [green]folder-sorter doctor[/green]\n"
                    "    Run system diagnostics, dependencies & permissions verification.\n\n"
                    "  [green]folder-sorter config [show|add|remove][/green]\n"
                    "    Manage configuration file extensions mapping directly.",
                    title="Direct CLI Mode Reference Guide",
                    border_style="cyan"
                )
            )
            input("\nPress Enter to continue...")

@config_app.command(name="edit")
def config_edit():
    """Open the configuration JSON file in your default system text editor."""
    config_file = get_config_file()
    console.print(f"[bold cyan]Opening Config File:[/bold cyan] {config_file}")
    try:
        typer.launch(str(config_file))
    except Exception as e:
        console.print(f"[bold red]Failed to open config file: {e}[/bold red]")
        console.print(f"You can manually edit the file at: [white]{config_file}[/white]")

def interactive_config_menu():
    """Nested configuration settings menu loop."""
    while True:
        console.clear()
        console.print(
            Panel.fit(
                "[bold magenta]Folder Sorter Config Settings[/bold magenta]\n"
                "[dim]Manage custom file extension mappings[/dim]",
                border_style="magenta"
            )
        )

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Option", justify="center", style="magenta")
        table.add_column("Action", style="white")
        table.add_column("Description", style="dim white")

        table.add_row("1", "Show Mappings", "List current extensions grouped under each category")
        table.add_row("2", "Add Extension", "Register a new custom extension mapping (e.g. .go to Code)")
        table.add_row("3", "Remove Extension", "Deregister an extension mapping from a category")
        table.add_row("4", "Add Category", "Create a new custom category (e.g. Music, Databases)")
        table.add_row("5", "Edit Config File", "Open the config JSON file in your default system editor")
        table.add_row("0", "Back to Menu", "Return to the main Folder Sorter menu")

        console.print(table)

        choice = Prompt.ask("\n[bold yellow]Choose config option[/bold yellow]", choices=["0", "1", "2", "3", "4", "5"])

        if choice == "0":
            break

        elif choice == "1":
            console.print()
            run_loading_spinner("Loading configuration mappings...")
            config_show()
            input("\nPress Enter to continue...")

        elif choice == "2":
            config_data = load_config()
            categories = config_data.get("categories", {})
            valid_categories = list(categories.keys())
            
            console.print(f"\nAvailable Categories: [cyan]{', '.join(valid_categories)}[/cyan]")
            category = Prompt.ask("Enter category name", choices=valid_categories)
            extension = Prompt.ask("Enter extension to add (e.g. .go, .rs)")
            
            console.print()
            run_loading_spinner("Updating configuration...")
            
            if not extension.startswith("."):
                extension = f".{extension}"
            extension = extension.lower()

            for cat, ext_list in categories.items():
                if extension in ext_list:
                    console.print(f"[yellow]Extension '{extension}' is already in category '{cat}'.[/yellow]")
                    input("\nPress Enter to continue...")
                    break
            else:
                categories[category].append(extension)
                if save_config(categories):
                    console.print(f"[bold green]Added extension '{extension}' to category '{category}'.[/bold green]")
                else:
                    console.print("[bold red]Failed to save configuration.[/bold red]")
                input("\nPress Enter to continue...")

        elif choice == "3":
            config_data = load_config()
            categories = config_data.get("categories", {})
            valid_categories = list(categories.keys())
            
            console.print(f"\nAvailable Categories: [cyan]{', '.join(valid_categories)}[/cyan]")
            category = Prompt.ask("Enter category name", choices=valid_categories)
            
            ext_list = categories.get(category, [])
            if not ext_list:
                console.print(f"[yellow]Category '{category}' has no extensions to remove.[/yellow]")
                input("\nPress Enter to continue...")
                continue

            console.print(f"Current extensions in '{category}': [cyan]{', '.join(ext_list)}[/cyan]")
            extension = Prompt.ask("Enter extension to remove", choices=ext_list)
            
            console.print()
            run_loading_spinner("Updating configuration...")
            
            categories[category].remove(extension)
            if save_config(categories):
                console.print(f"[bold green]Removed extension '{extension}' from category '{category}'.[/bold green]")
            else:
                console.print("[bold red]Failed to save configuration.[/bold red]")
            input("\nPress Enter to continue...")

        elif choice == "4":
            category = Prompt.ask("\nEnter new category name (or 0 to cancel)").strip()
            if category == "0" or not category:
                console.print("[yellow]Operation cancelled.[/yellow]")
                input("\nPress Enter to continue...")
                continue

            config_data = load_config()
            categories = config_data.get("categories", {})

            matched = False
            for cat in categories.keys():
                if cat.lower() == category.lower():
                    matched = True
                    break

            if matched:
                console.print(f"[bold red]Category '{category}' already exists.[/bold red]")
            else:
                console.print()
                run_loading_spinner("Creating category...")
                categories[category] = []
                if save_config(categories):
                    console.print(f"[bold green]Successfully added new category '{category}'.[/bold green]")
                else:
                    console.print("[bold red]Failed to save configuration.[/bold red]")
            input("\nPress Enter to continue...")

        elif choice == "5":
            console.print()
            run_loading_spinner("Opening editor...")
            config_edit()
            input("\nPress Enter to continue...")

@app.command(name="sort")
def sort_command(
    directory: Path = typer.Argument(
        default=Path("."),
        help="The directory to sort. Defaults to the current directory.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True
    ),
    mode: str = typer.Option(
        "by-type",
        "--mode",
        "-m",
        help="Sorting mode: 'by-type' or 'by-date'."
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-d",
        help="Perform a dry run without moving files."
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Recursively sort subdirectories."
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed move logs."
    )
):
    """Sort files inside a directory by type or date."""
    mode = mode.lower()
    if mode not in ("by-type", "by-date"):
        console.print("[bold red]Error: Invalid mode. Use 'by-type' or 'by-date'.[/bold red]")
        raise typer.Exit(code=1)

    if mode == "by-type":
        sort_by_type(str(directory), recursive=recursive, dry_run=dry_run, verbose=verbose)
    else:
        sort_by_month(str(directory), recursive=recursive, dry_run=dry_run, verbose=verbose)

@app.command(name="undo")
def undo_command(
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-d",
        help="Perform a dry run of the undo operation."
    )
):
    """Reverse the last folder sorting operation."""
    undo_last_sort(dry_run=dry_run)

@app.command(name="doctor")
def doctor_command():
    """Verify system diagnostics and permissions."""
    run_diagnostics()

@app.command(name="update")
def update_command():
    """Check for updates and display upgrade instructions."""
    check_for_updates()

# Configuration Nested Typer
app.add_typer(config_app, name="config")

@config_app.callback(invoke_without_command=True)
def config_default(ctx: typer.Context):
    """View configurations by default when no subcommand is given."""
    if ctx.invoked_subcommand is None:
        config_show()

@config_app.command(name="show")
def config_show():
    """Show the current file extensions configuration."""
    config_data = load_config()
    categories = config_data.get("categories", {})
    
    console.print(f"[bold cyan]Config File Path:[/bold cyan] {get_config_file()}")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan")
    table.add_column("Extensions", style="white")
    
    for category, extensions in categories.items():
        table.add_row(category, ", ".join(extensions))
        
    console.print(table)

@config_app.command(name="add")
def config_add(
    category: str = typer.Argument(..., help="Category name (e.g. Images, Code, etc.)"),
    extension: str = typer.Argument(..., help="Extension to add (e.g. .mp4, .zip)")
):
    """Add a file extension to a category."""
    if not extension.startswith("."):
        extension = f".{extension}"
    extension = extension.lower()

    config_data = load_config()
    categories = config_data.get("categories", {})

    valid_categories = list(categories.keys())
    matched_category = None
    for cat in valid_categories:
        if cat.lower() == category.lower():
            matched_category = cat
            break

    if not matched_category:
        console.print(f"[bold red]Category '{category}' does not exist.[/bold red]")
        console.print(f"Valid categories are: {', '.join(valid_categories)}")
        raise typer.Exit(code=1)

    for cat, ext_list in categories.items():
        if extension in ext_list:
            console.print(f"[yellow]Extension '{extension}' is already in category '{cat}'.[/yellow]")
            return

    categories[matched_category].append(extension)
    if save_config(categories):
        console.print(f"[bold green]Added extension '{extension}' to category '{matched_category}'.[/bold green]")
    else:
        console.print("[bold red]Failed to save configuration.[/bold red]")

@config_app.command(name="remove")
def config_remove(
    category: str = typer.Argument(..., help="Category name (e.g. Images, Code, etc.)"),
    extension: str = typer.Argument(..., help="Extension to remove (e.g. .mp4, .zip)")
):
    """Remove a file extension from a category."""
    if not extension.startswith("."):
        extension = f".{extension}"
    extension = extension.lower()

    config_data = load_config()
    categories = config_data.get("categories", {})

    matched_category = None
    for cat in categories.keys():
        if cat.lower() == category.lower():
            matched_category = cat
            break

    if not matched_category:
        console.print(f"[bold red]Category '{category}' does not exist.[/bold red]")
        raise typer.Exit(code=1)

    if extension not in categories[matched_category]:
        console.print(f"[yellow]Extension '{extension}' not found in category '{matched_category}'.[/yellow]")
        return

    categories[matched_category].remove(extension)
    if save_config(categories):
        console.print(f"[bold green]Removed extension '{extension}' from category '{matched_category}'.[/bold green]")
    else:
        console.print("[bold red]Failed to save configuration.[/bold red]")

@config_app.command(name="add-category")
def config_add_category(
    category: str = typer.Argument(..., help="Name of the new category to add (e.g. Music, Databases)")
):
    """Create a new custom category."""
    config_data = load_config()
    categories = config_data.get("categories", {})

    for cat in categories.keys():
        if cat.lower() == category.lower():
            console.print(f"[bold red]Category '{cat}' already exists.[/bold red]")
            raise typer.Exit(code=1)

    categories[category] = []
    if save_config(categories):
        console.print(f"[bold green]Successfully added new category '{category}'.[/bold green]")
    else:
        console.print("[bold red]Failed to save configuration.[/bold red]")

def main():
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[bold red]Program interrupted by user.[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error:[/bold red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
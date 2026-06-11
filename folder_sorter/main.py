from folder_sorter.sorter import sort_by_type
from folder_sorter.date_sorter import sort_by_month
from folder_sorter.undo import undo_last_sort

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table


console = Console()


def show_menu():

    console.clear()

    console.print(
        Panel.fit(
            "[bold cyan]Folder Sorter[/bold cyan]\n"
            "[green]Organize your messy folders with ease[/green]",
            border_style="bright_blue"
        )
    )

    table = Table(
        show_header=True,
        header_style="bold magenta"
    )

    table.add_column("Option", justify="center", style="cyan")
    table.add_column("Action", style="white")

    table.add_row("0", "Exit Program")
    table.add_row("1", "Smart Sort")
    table.add_row("2", "Sort By Month")
    table.add_row("3", "Undo Last Sort")

    console.print(table)


def get_folder_path():

    folder = Prompt.ask(
        "\n[cyan]Folder path[/cyan]\n"
        "[dim](Enter 0 to cancel)[/dim]"
    ).strip('"')

    if folder == "0":

        console.print("\n[yellow]Operation cancelled.[/yellow]")
        input("\nPress Enter to continue...")
        return None

    return folder


def main():

    while True:

        show_menu()

        choice = Prompt.ask("\n[bold yellow]Choose option[/bold yellow]")

        if choice == "0":

            console.print("\n[bold red]Exiting program...[/bold red]")
            break

        elif choice == "1":  # Fixed: was over-indented

            folder = get_folder_path()

            if folder is None:
                continue

            sort_by_type(folder)

            console.print("\n[bold green]✓ Sorting completed[/bold green]")
            input("\nPress Enter to continue...")

        elif choice == "2":

            folder = get_folder_path()

            if folder is None:
                continue

            sort_by_month(folder)

            console.print("\n[bold green]✓ Sorting completed[/bold green]")
            input("\nPress Enter to continue...")

        elif choice == "3":

            undo_last_sort()

            console.print("\n[bold green]✓ Undo completed[/bold green]")
            input("\nPress Enter to continue...")

        else:

            console.print("\n[bold red]Invalid option.[/bold red]")
            input("\nPress Enter to continue...")


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        console.print("\n\n[bold red]Program interrupted by user.[/bold red]")

    except Exception as error:
        console.print(f"\n[bold red]Unexpected error:[/bold red] {error}")
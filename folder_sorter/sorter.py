import os
from pathlib import Path
from PIL import Image
from rich.console import Console
from rich.progress import track

from folder_sorter.categories import get_category
from folder_sorter.utils import move_file
from folder_sorter.config import IMAGE_EXTENSIONS, load_config

console = Console()

def is_year_dir(name):
    """Check if directory name matches a year (e.g., 2024)."""
    return name.isdigit() and len(name) == 4 and 1900 <= int(name) <= 2100

def collect_files(folder_path, recursive=False):
    """Collect files from folder, optionally traversing subdirectories while skipping category dirs."""
    files = []
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        return files

    config_data = load_config()
    categories = config_data.get("categories", {})
    skip_dirs = set(categories.keys()) | {"Others"}

    if recursive:
        for root, dirs, filenames in os.walk(folder_path):
            # Prune directories we don't want to walk into
            dirs[:] = [
                d for d in dirs
                if d not in skip_dirs and not is_year_dir(d)
            ]
            for filename in filenames:
                files.append(Path(root) / filename)
    else:
        for item in folder.iterdir():
            if item.is_file():
                files.append(item)
    return files

def get_image_destination(file_path):
    """Determine image destination folder automatically based on type and resolution."""
    extension = file_path.suffix.lower()

    if extension == ".gif":
        image_type = "GIFs"
    elif extension in {".jpg", ".jpeg"}:
        image_type = "JPG"
    elif extension == ".png":
        image_type = "PNG"
    elif extension == ".webp":
        image_type = "WEBP"
    elif extension == ".svg":
        image_type = "SVG"
    else:
        image_type = "Others"

    try:
        with Image.open(file_path) as img:
            width, height = img.size
        pixels = width * height

        if pixels >= 8000000:
            resolution = "4K"
        elif pixels >= 3500000:
            resolution = "1440p"
        elif pixels >= 1800000:
            resolution = "1080p"
        elif pixels >= 900000:
            resolution = "720p"
        else:
            resolution = "Below_720p"
    except Exception:
        resolution = "Unknown"

    return os.path.join(
        "Images",
        image_type,
        resolution
    )

def sort_by_type(folder_path, recursive=False, dry_run=False, verbose=False):
    """Sort files by category type."""
    files = collect_files(folder_path, recursive)
    if not files:
        console.print("[yellow]No files to sort.[/yellow]")
        return

    moved_count = 0
    if dry_run or verbose:
        for file_path in files:
            extension = file_path.suffix.lower()
            if extension in IMAGE_EXTENSIONS:
                destination = os.path.join(folder_path, get_image_destination(file_path))
            else:
                destination = os.path.join(folder_path, get_category(extension))
            
            if move_file(str(file_path), destination, dry_run=dry_run, verbose=verbose):
                moved_count += 1
    else:
        for file_path in track(files, description="[cyan]Sorting files by type...[/cyan]"):
            extension = file_path.suffix.lower()
            if extension in IMAGE_EXTENSIONS:
                destination = os.path.join(folder_path, get_image_destination(file_path))
            else:
                destination = os.path.join(folder_path, get_category(extension))
            
            if move_file(str(file_path), destination, dry_run=dry_run, verbose=verbose):
                moved_count += 1

    action_word = "Would sort" if dry_run else "Successfully sorted"
    console.print(f"[bold green]{action_word} {moved_count} file(s).[/bold green]")
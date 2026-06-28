import os
from pathlib import Path
from PIL import Image
from folder_sorter.sorter import sort_by_type, collect_files, get_image_destination

def create_test_image(path: Path, width: int, height: int):
    """Helper to create a test image using Pillow."""
    img = Image.new("RGB", (width, height), color="blue")
    img.save(path)

def test_collect_files_non_recursive(temp_workspace):
    file1 = temp_workspace / "a.txt"
    file2 = temp_workspace / "b.zip"
    sub_dir = temp_workspace / "sub"
    sub_dir.mkdir()
    file3 = sub_dir / "c.py"

    file1.write_text("txt content")
    file2.write_text("zip content")
    file3.write_text("py content")

    collected = collect_files(str(temp_workspace), recursive=False)
    # Convert Paths to names for easy assertion
    names = {p.name for p in collected}
    assert names == {"a.txt", "b.zip"}

def test_collect_files_recursive(temp_workspace):
    file1 = temp_workspace / "a.txt"
    sub_dir = temp_workspace / "sub"
    sub_dir.mkdir()
    file2 = sub_dir / "b.py"
    ignored_dir = temp_workspace / "Code" # skip category dirs
    ignored_dir.mkdir()
    file3 = ignored_dir / "c.py"

    file1.write_text("content")
    file2.write_text("content")
    file3.write_text("content")

    collected = collect_files(str(temp_workspace), recursive=True)
    names = {p.name for p in collected}
    assert "a.txt" in names
    assert "b.py" in names
    assert "c.py" not in names  # Should be ignored because Code is in SKIP_DIRS

def test_get_image_destination(temp_workspace):
    png_1080p = temp_workspace / "1080p.png"
    create_test_image(png_1080p, 1920, 1080) # 2,073,600 pixels (1080p)
    dest = get_image_destination(png_1080p)
    assert dest == os.path.join("Images", "PNG", "1080p")

    png_small = temp_workspace / "small.png"
    create_test_image(png_small, 100, 100) # 10,000 pixels (Below_720p)
    dest_small = get_image_destination(png_small)
    assert dest_small == os.path.join("Images", "PNG", "Below_720p")

def test_sort_by_type_execution(temp_workspace):
    file_txt = temp_workspace / "notes.txt"
    file_py = temp_workspace / "script.py"
    file_png = temp_workspace / "photo.png"
    
    file_txt.write_text("text")
    file_py.write_text("python")
    create_test_image(file_png, 2000, 2000) # 4,000,000 pixels (1440p)

    sort_by_type(str(temp_workspace), recursive=False, dry_run=False, verbose=True)

    assert not file_txt.exists()
    assert not file_py.exists()
    assert not file_png.exists()

    assert (temp_workspace / "Documents" / "notes.txt").exists()
    assert (temp_workspace / "Code" / "script.py").exists()
    assert (temp_workspace / "Images" / "PNG" / "1440p" / "photo.png").exists()

def test_sort_by_type_dry_run(temp_workspace):
    file_txt = temp_workspace / "notes.txt"
    file_txt.write_text("text")

    sort_by_type(str(temp_workspace), recursive=False, dry_run=True, verbose=True)

    assert file_txt.exists()
    assert not (temp_workspace / "Documents" / "notes.txt").exists()

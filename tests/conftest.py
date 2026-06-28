import pytest
import shutil
from pathlib import Path

@pytest.fixture(autouse=True)
def mock_app_dir(tmp_path, monkeypatch):
    """Fixture to mock ~/.folder-sorter globally using pytest's tmp_path."""
    test_app_dir = tmp_path / ".folder-sorter"
    test_app_dir.mkdir(parents=True, exist_ok=True)
    
    # Patch Path.home globally to point to tmp_path
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    
    # Import all modules
    import folder_sorter.config
    import folder_sorter.utils
    import folder_sorter.categories
    import folder_sorter.sorter
    import folder_sorter.date_sorter
    import folder_sorter.undo
    import folder_sorter.doctor
    import folder_sorter.main

    # Reload them in correct order to propagate the patched Path.home
    import importlib
    importlib.reload(folder_sorter.config)
    importlib.reload(folder_sorter.utils)
    importlib.reload(folder_sorter.categories)
    importlib.reload(folder_sorter.sorter)
    importlib.reload(folder_sorter.date_sorter)
    importlib.reload(folder_sorter.undo)
    importlib.reload(folder_sorter.doctor)
    importlib.reload(folder_sorter.main)
    
    yield tmp_path / ".folder-sorter"

@pytest.fixture
def temp_workspace(tmp_path):
    """Fixture providing a mock workspace directory with temporary files to sort."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace

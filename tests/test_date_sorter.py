import os
import time
from datetime import datetime
from folder_sorter.date_sorter import sort_by_month

def test_sort_by_month_execution(temp_workspace, monkeypatch):
    file1 = temp_workspace / "notes.txt"
    file2 = temp_workspace / "script.py"

    file1.write_text("notes")
    file2.write_text("script")

    # Mock getmtime to return specific timestamps
    # 1717180800 is June 1, 2024
    # 1704067200 is January 1, 2024
    def mock_getmtime(path):
        if "notes.txt" in str(path):
            return 1717180800
        return 1704067200

    monkeypatch.setattr(os.path, "getmtime", mock_getmtime)

    sort_by_month(str(temp_workspace), recursive=False, dry_run=False, verbose=True)

    assert not file1.exists()
    assert not file2.exists()

    assert (temp_workspace / "2024" / "June" / "notes.txt").exists()
    assert (temp_workspace / "2024" / "January" / "script.py").exists()

def test_sort_by_month_dry_run(temp_workspace, monkeypatch):
    file1 = temp_workspace / "notes.txt"
    file1.write_text("notes")

    monkeypatch.setattr(os.path, "getmtime", lambda path: 1717180800)

    sort_by_month(str(temp_workspace), recursive=False, dry_run=True, verbose=True)

    assert file1.exists()
    assert not (temp_workspace / "2024" / "June" / "notes.txt").exists()

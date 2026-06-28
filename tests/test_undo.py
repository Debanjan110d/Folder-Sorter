import json
from folder_sorter.sorter import sort_by_type
from folder_sorter.undo import undo_last_sort
from folder_sorter.utils import get_history_file

def test_undo_restores_files(temp_workspace):
    file1 = temp_workspace / "notes.txt"
    file2 = temp_workspace / "script.py"

    file1.write_text("text")
    file2.write_text("code")

    # Run sort
    sort_by_type(str(temp_workspace), recursive=False, dry_run=False)
    
    assert not file1.exists()
    assert not file2.exists()
    assert (temp_workspace / "Documents" / "notes.txt").exists()
    assert (temp_workspace / "Code" / "script.py").exists()

    # Verify history is saved
    history_file = get_history_file()
    assert history_file.exists()
    with open(history_file, "r") as f:
        history = json.load(f)
        assert len(history) == 2

    # Perform undo
    undo_last_sort(dry_run=False)

    # Verify files restored
    assert file1.exists()
    assert file2.exists()
    assert not (temp_workspace / "Documents" / "notes.txt").exists()
    assert not (temp_workspace / "Code" / "script.py").exists()

    # Verify history is cleared
    with open(history_file, "r") as f:
        history = json.load(f)
        assert len(history) == 0

def test_undo_dry_run(temp_workspace):
    file1 = temp_workspace / "notes.txt"
    file1.write_text("text")

    # Run sort
    sort_by_type(str(temp_workspace), recursive=False, dry_run=False)
    assert not file1.exists()

    # Run dry-run undo
    undo_last_sort(dry_run=True)

    # File should NOT be restored yet
    assert not file1.exists()
    assert (temp_workspace / "Documents" / "notes.txt").exists()

def test_sequential_undos(temp_workspace):
    file1 = temp_workspace / "notes.txt"
    file2 = temp_workspace / "script.py"

    # Step 1: Create file1 and sort it
    file1.write_text("text")
    sort_by_type(str(temp_workspace), recursive=False, dry_run=False)

    # Step 2: Create file2 and sort it (separately, so it has a different run_id)
    file2.write_text("code")
    # Need to reload or wait to guarantee a different timestamp/run_id?
    # In utils.py, RUN_ID is set once per module import.
    # To mock different runs, we can reload utils or just test that if history contains different run_ids,
    # it only undos the latest run.
    # Let's manually write a multi-run history structure to test the logic!
    history_file = get_history_file()
    with open(history_file, "r") as f:
        history = json.load(f)
        assert len(history) == 1
        run1_id = history[0]["run_id"]

    # Manually append a second run to history
    run2_id = "second-mock-run-uuid"
    history.append({
        "run_id": run2_id,
        "timestamp": "2026-06-28T22:00:00",
        "source": str(file2.resolve()),
        "destination": str((temp_workspace / "Code" / "script.py").resolve())
    })
    
    # Manually move file2 to its destination to simulate the second sort run
    (temp_workspace / "Code").mkdir(exist_ok=True)
    file2.rename(temp_workspace / "Code" / "script.py")

    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)

    # First undo should only restore run2 (script.py)
    undo_last_sort(dry_run=False)
    assert file2.exists()
    assert not file1.exists() # notes.txt is still sorted (run1)

    # Second undo should restore run1 (notes.txt)
    undo_last_sort(dry_run=False)
    assert file1.exists()

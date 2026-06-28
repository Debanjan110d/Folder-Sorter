import sys
from folder_sorter.doctor import run_diagnostics

def test_doctor_runs_cleanly(capsys):
    # Simply running diagnostics should pass without error
    run_diagnostics()
    
    captured = capsys.readouterr()
    assert "Diagnostic Doctor" in captured.out
    assert "Python Version" in captured.out
    assert "Operating System" in captured.out

def test_doctor_fails_python_check(monkeypatch, capsys):
    # Mock python version to < 3.8 using a namedtuple
    from collections import namedtuple
    VersionInfo = namedtuple('VersionInfo', ['major', 'minor', 'micro'])
    monkeypatch.setattr(sys, "version_info", VersionInfo(3, 7, 0))
    run_diagnostics()

    captured = capsys.readouterr()
    assert "FAIL" in captured.out
    assert "Python version is less than 3.8" in captured.out

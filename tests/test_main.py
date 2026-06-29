import json
import urllib.request
import typer
from typer.testing import CliRunner
from folder_sorter.main import app, __version__
from folder_sorter.config import get_config_file

runner = CliRunner()

def test_version_flag():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.stdout
    assert __version__ in result.stdout

def test_sort_help():
    result = runner.invoke(app, ["sort", "--help"])
    assert result.exit_code == 0
    assert "Sort files inside a directory" in result.stdout

def test_doctor_command():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "Diagnostic Doctor" in result.stdout

def test_config_show_command():
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "Config File Path" in result.stdout
    assert "Images" in result.stdout
    assert "Code" in result.stdout

def test_config_add_and_remove_command():
    # Verify add
    result_add = runner.invoke(app, ["config", "add", "Code", ".rs"])
    assert result_add.exit_code == 0
    assert "Added extension '.rs' to category 'Code'" in result_add.stdout

    # Verify rs was added to config file
    with open(get_config_file(), "r") as f:
        config = json.load(f)
        assert ".rs" in config["categories"]["Code"]

    # Verify duplicate add check
    result_dup = runner.invoke(app, ["config", "add", "Code", ".rs"])
    assert "already in category" in result_dup.stdout

    # Verify remove
    result_remove = runner.invoke(app, ["config", "remove", "Code", ".rs"])
    assert result_remove.exit_code == 0
    assert "Removed extension '.rs' from category 'Code'" in result_remove.stdout

    # Verify rs was removed
    with open(get_config_file(), "r") as f:
        config = json.load(f)
        assert ".rs" not in config["categories"]["Code"]

def test_config_edit_command(monkeypatch):
    launched_path = []
    
    def mock_launch(url):
        launched_path.append(url)
        return True

    monkeypatch.setattr(typer, "launch", mock_launch)

    result = runner.invoke(app, ["config", "edit"])
    assert result.exit_code == 0
    assert "Opening Config File" in result.stdout
    assert len(launched_path) == 1
    assert "config.json" in launched_path[0]

def test_update_command_already_up_to_date(monkeypatch):
    # Mock urllib response indicating the same version (0.1.0)
    class MockResponse:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def read(self):
            return json.dumps({"tag_name": "v0.1.0"}).encode()

    def mock_urlopen(req, timeout=None):
        return MockResponse()

    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen)

    result = runner.invoke(app, ["update"])
    assert result.exit_code == 0
    assert "up to date" in result.stdout

def test_update_command_newer_version(monkeypatch):
    # Mock urllib response indicating a newer version (v1.2.0)
    class MockResponse:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def read(self):
            return json.dumps({"tag_name": "v1.2.0"}).encode()

    def mock_urlopen(req, timeout=None):
        return MockResponse()

    monkeypatch.setattr(urllib.request, "urlopen", mock_urlopen)

    result = runner.invoke(app, ["update"])
    assert result.exit_code == 0
    assert "Update Available!" in result.stdout
    assert "v1.2.0" in result.stdout

def test_config_add_category_command():
    # Verify add-category
    result_add = runner.invoke(app, ["config", "add-category", "Music"])
    assert result_add.exit_code == 0
    assert "Successfully added new category 'Music'" in result_add.stdout

    # Verify duplicate add-category check
    result_dup = runner.invoke(app, ["config", "add-category", "Music"])
    assert result_dup.exit_code == 1
    assert "Category 'Music' already exists" in result_dup.stdout

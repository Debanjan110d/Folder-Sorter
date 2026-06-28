import json
from folder_sorter.config import load_config, save_config, get_config_file, DEFAULT_CONFIG

def test_load_config_creates_default():
    config_file = get_config_file()
    if config_file.exists():
        config_file.unlink()
        
    config = load_config()
    assert config_file.exists()
    assert config == DEFAULT_CONFIG

def test_save_and_load_custom_config():
    custom_categories = {
        "Images": [".jpg", ".png"],
        "Code": [".py", ".go"],
        "CustomCat": [".abc"]
    }
    
    success = save_config(custom_categories)
    assert success is True
    
    config = load_config()
    loaded_categories = config.get("categories")
    assert loaded_categories["CustomCat"] == [".abc"]
    assert "Images" in loaded_categories
    assert "Code" in loaded_categories

from folder_sorter.config import load_config

def get_category(extension):
    """Determine which category a file belongs to based on its extension."""
    extension = extension.lower()
    config_data = load_config()
    categories = config_data.get("categories", {})

    for category, extensions in categories.items():
        if extension in extensions:
            return category

    return "Others"
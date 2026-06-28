from folder_sorter.categories import get_category

def test_get_category_known_extensions():
    # Images
    assert get_category(".jpg") == "Images"
    assert get_category(".png") == "Images"
    assert get_category(".WEBP") == "Images"  # case insensitivity check

    # Videos
    assert get_category(".mp4") == "Videos"
    assert get_category(".mkv") == "Videos"

    # Audio
    assert get_category(".mp3") == "Audio"
    assert get_category(".wav") == "Audio"

    # Documents
    assert get_category(".pdf") == "Documents"
    assert get_category(".txt") == "Documents"

    # Archives
    assert get_category(".zip") == "Archives"
    assert get_category(".tar.gz") == "Others"  # suffix check (.gz would map, .tar.gz itself matches suffix .gz)
    assert get_category(".gz") == "Archives"

    # Code
    assert get_category(".py") == "Code"
    assert get_category(".js") == "Code"

def test_get_category_unknown_extension():
    assert get_category(".xyz") == "Others"
    assert get_category(".unknown") == "Others"
    assert get_category("") == "Others"

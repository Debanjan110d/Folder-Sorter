from folder_sorter.config import *

'''
Determine which category
a file belongs to
'''

def get_category(extension):

    extension = extension.lower()

    if extension in IMAGE_EXTENSIONS:
        return "Images"

    if extension in VIDEO_EXTENSIONS:
        return "Videos"

    if extension in AUDIO_EXTENSIONS:
        return "Audio"

    if extension in DOCUMENT_EXTENSIONS:
        return "Documents"

    if extension in ARCHIVE_EXTENSIONS:
        return "Archives"

    if extension in CODE_EXTENSIONS:
        return "Code"

    return "Others"
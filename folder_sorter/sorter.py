import os
from pathlib import Path

from PIL import Image

from folder_sorter.categories import get_category
from folder_sorter.utils import move_file
from folder_sorter.config import IMAGE_EXTENSIONS


'''
Determine image destination
folder automatically
'''

def get_image_destination(file_path):

    extension = file_path.suffix.lower()

    if extension == ".gif":
        image_type = "GIFs"

    elif extension in {".jpg", ".jpeg"}:
        image_type = "JPG"

    elif extension == ".png":
        image_type = "PNG"

    elif extension == ".webp":
        image_type = "WEBP"

    elif extension == ".svg":
        image_type = "SVG"

    else:
        image_type = "Others"

    try:

        with Image.open(file_path) as img:

            width, height = img.size

        pixels = width * height

        if pixels >= 8000000:
            resolution = "4K"

        elif pixels >= 3500000:
            resolution = "1440p"

        elif pixels >= 1800000:
            resolution = "1080p"

        elif pixels >= 900000:
            resolution = "720p"

        else:
            resolution = "Below_720p"

    except Exception:

        resolution = "Unknown"

    return os.path.join(
        "Images",
        image_type,
        resolution
    )


'''
Sort files by category
'''

def sort_by_type(folder_path):

    folder = Path(folder_path)

    for file_path in folder.iterdir():

        if not file_path.is_file():
            continue

        extension = file_path.suffix.lower()

        '''
        Handle images separately
        '''

        if extension in IMAGE_EXTENSIONS:

            destination = os.path.join(
                folder_path,
                get_image_destination(file_path)
            )

            move_file(
                str(file_path),
                destination
            )

            continue

        '''
        Handle all other files
        '''

        category = get_category(extension)

        destination = os.path.join(
            folder_path,
            category
        )

        move_file(
            str(file_path),
            destination
        )

    print("Sorting completed.")
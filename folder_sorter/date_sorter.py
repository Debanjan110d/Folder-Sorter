import os
from datetime import datetime

from folder_sorter.utils import move_file

'''
Sort files
by year/month
'''

def sort_by_month(folder_path):

    for item in os.listdir(folder_path):

        full_path = os.path.join(
            folder_path,
            item
        )

        if not os.path.isfile(full_path):
            continue

        modified_time = os.path.getmtime(
            full_path
        )

        date = datetime.fromtimestamp(
            modified_time
        )

        year = str(date.year)
        month = date.strftime("%B")

        destination = os.path.join(
            folder_path,
            year,
            month
        )

        move_file(
            full_path,
            destination
        )

    print("Sorting completed.")
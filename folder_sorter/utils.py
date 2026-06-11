import os
import shutil
import json

'''
History file
used for undo
'''

HISTORY_FILE = "history.json"


'''
Create destination folder
if it doesn't exist
'''

def ensure_folder(path):

    os.makedirs(
        path,
        exist_ok=True
    )


'''
Create history file
if missing
'''

def initialize_history():

    if not os.path.exists(HISTORY_FILE):

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


'''
Save move operation
for undo support
'''

def save_move(
    source,
    destination
):

    initialize_history()

    with open(
        HISTORY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        history = json.load(file)

    history.append(
        {
            "source": source,
            "destination": destination
        }
    )

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )


'''
Move file safely
and record history
'''

def move_file(
    source,
    destination
):

    ensure_folder(destination)

    file_name = os.path.basename(
        source
    )

    final_destination = os.path.join(
        destination,
        file_name
    )

    save_move(
        source,
        final_destination
    )

    shutil.move(
        source,
        final_destination
    )
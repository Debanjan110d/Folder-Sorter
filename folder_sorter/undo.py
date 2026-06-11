import json
import os
import shutil

'''
Undo the last sorting
operation
'''

def undo_last_sort():

    if not os.path.exists(
        "history.json"
    ):

        print(
            "No history found."
        )

        return

    with open(
        "history.json",
        "r",
        encoding="utf-8"
    ) as file:

        history = json.load(file)

    if not history:

        print(
            "Nothing to undo."
        )

        return

    '''
    Reverse order
    to avoid conflicts
    '''

    for move in reversed(
        history
    ):

        source = move["source"]

        destination = move[
            "destination"
        ]

        if not os.path.exists(
            destination
        ):
            continue

        os.makedirs(
            os.path.dirname(
                source
            ),
            exist_ok=True
        )

        shutil.move(
            destination,
            source
        )

    with open(
        "history.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            [],
            file,
            indent=4
        )

    print(
        "Undo completed."
    )
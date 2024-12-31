import json
import os
import re
import shutil
from os.path import basename, splitext
from typing import Any, Sequence

import click

from rmlib.io import SYNC_DIR


def get_rm_trash_files() -> list[str]:
    file_list = []
    for metadata_file in (SYNC_DIR / "xochitl").iterdir():
        if not metadata_file.match("*.metadata"):
            continue

        metadata = json.load(open(metadata_file))
        if metadata["parent"] in "trash":
            file_list.append(splitext(basename(metadata_file))[0])

    return file_list


def get_linked_files(rm_file: str) -> Sequence[os.PathLike[Any]]:
    file_list = []
    for file in (SYNC_DIR / "xochitl").iterdir():
        if not re.search(f"{rm_file}*", str(file)):
            continue

        file_list.append(file)

    return file_list


@click.command
def remove_trash():
    delete_files = {
        rm_file: get_linked_files(rm_file) for rm_file in get_rm_trash_files()
    }

    for rm_file, file_list in delete_files.items():
        print(f"Removing {rm_file}")
        for item in file_list:
            if item.is_file():
                os.remove(item)
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)

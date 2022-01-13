from pathlib import Path
from typing import List
import re


CWD = Path.cwd()
PATH = Path(CWD / "./notebooks/datasets/raw")
IS_SUFFIX = re.compile("(\.*[\w\d]+)+", re.IGNORECASE)


def add_data(path, file_suffixes: List[str]):
    given_path = Path(path)
    files_to_add=[]
    for suffix in file_suffixes:
        if IS_SUFFIX.match(suffix): 
            contents=list(given_path.glob(f"**/*{suffix}"))
            files_to_add.extend(contents)
        else:
            raise ValueError(f"\"{suffix}\" is not a valid file suffix.")
    for _ in files_to_add:
        print(_)


if __name__ == "__main__":
    add_data(PATH, ["omex", ".pdh"])

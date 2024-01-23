from datetime import datetime
from pathlib import Path

from torch import Tensor

from embedding import embed


def extract_data_from_md(
    path_string: str,
    exclude_dir: list[str],
    exclude_file: list[str],
    cache_data: dict[Path, tuple[Tensor, datetime]],
):
    md_files = get_md_files_list(path_string, exclude_dir, exclude_file)
    changed = False

    # first checking for which are deleted
    deleted_notes = set(cache_data.keys()) - set(md_files)
    if len(deleted_notes) > 0:
        changed = True
        for d in deleted_notes:
            del cache_data[d]

    # then checking for updates and new, and creating new tensor out of it
    updates_new = dict()
    for file in md_files:
        if file not in cache_data:
            updates_new[file] = "new"
        elif datetime.fromtimestamp(file.stat().st_mtime) > cache_data[file][1]:
            updates_new[file] = "update"

    if len(updates_new) > 0:
        changed = True
        # now creating embedding of new and update
        updates_new_embedding = embed([key.read_text() for key in updates_new], True)

        # then updating the cache data and returning it
        for i, key in enumerate(updates_new):
            cache_data[key] = (
                updates_new_embedding[i],
                datetime.fromtimestamp(key.stat().st_mtime),
            )

    return cache_data, changed


def get_md_files_list(
    path_string: str,
    exclude_dir: list[str],
    exclude_file: list[str],
    compare: Path | None = None,
):
    p = Path(path_string)
    if compare == None:
        compare = p
    file_list = [
        file
        for file in p.iterdir()
        if file.suffix == ".md"
        and file.is_file()
        and str(file.relative_to(compare)) not in exclude_file
    ]
    dir_list = [
        dir
        for dir in p.iterdir()
        if dir.is_dir() and str(dir.relative_to(compare)) not in exclude_dir
    ]

    for d in dir_list:
        file_list += get_md_files_list(
            str(d.absolute()), exclude_dir, exclude_file, compare
        )

    return file_list

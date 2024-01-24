from pathlib import Path
from time import perf_counter_ns


def get_all_files_in_directory(directory, excluded):
    # file_list = []  # Initialize an empty list to store file paths

    # Use Path.glob() to get all files in the directory and its subdirectories
    file_list = [
        path
        for path in Path(directory).rglob("*.md")
        if path.is_file() and not any(ed in str(path.parent) for ed in excluded)
    ]
    # and excluded not in str(path.parent)
    # for path in Path(directory).rglob("*.md"):
    #     print(
    #         str(path.parent.relative_to(directory)),
    #         any(ed in path.parent for ed in excluded),
    #     )
    #     if path.is_file():
    #         file_list.append(path)

    # Return the list of file paths
    return file_list


# Example usage:
directory_path = "/home/roopkumar/Things-I-do/my-learning-collection"
excluded = {"software-learnings/ai", "old_thoughts", "thoughts", "tips"}
start = perf_counter_ns()
files = get_all_files_in_directory(directory_path, excluded)
print((perf_counter_ns() - start) / 10**9)

# Print or process each file
for file in files:
    print(file)

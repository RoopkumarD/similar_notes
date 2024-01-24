#!/bin/env python3
import sys
import time
from pathlib import Path
from pickle import dump, load

from collect_files import extract_data_from_md
from embedding import embed, similarity

CONFIG_DIR = "/home/roopkumar/simnotesconfig"


def main(query: str):
    with open(f"{CONFIG_DIR}/config.txt", "r") as f:
        config = dict()
        for line in f.readlines():
            c = line.strip().split("=")
            if c[0] == "exclude_dir" or c[0] == "exclude_file":
                config[c[0]] = c[1].split(",")
            else:
                config[c[0]] = c[1]

    # find if there is cache data or not
    print("Finding cache data and building corpus to compare against")
    start = time.perf_counter_ns()
    cache_data = dict()
    if Path(f"{CONFIG_DIR}/cache_data.pickle").exists() == True:
        with open(f"{CONFIG_DIR}/cache_data.pickle", "rb") as f:
            cache_data = load(f)

    cache_data = extract_data_from_md(
        config["notes_dir"],
        config["exclude_dir"],
        config["exclude_file"],
        config["note_extension"],
        cache_data,
    )
    with open(f"{CONFIG_DIR}/cache_data.pickle", "wb") as f:
        dump(cache_data, f)
    print((time.perf_counter_ns() - start) / 10**9)

    if len(cache_data) == 0:
        raise Exception("You don't have any notes in md files")

    # after getting the embedding of notes
    print("Embedding the query")
    start = time.perf_counter_ns()
    query_embed = embed(query, True)
    print((time.perf_counter_ns() - start) / 10**9)

    # now getting similarity with this
    print("Finding similarity")
    start = time.perf_counter_ns()
    corpus = [cache_data[key][0] for key in cache_data]
    hit = similarity(query_embed, corpus)
    print((time.perf_counter_ns() - start) / 10**9)

    # then printing the similarity score with filename and returning
    files = list(cache_data.keys())
    print("Top files which are similar to given query:")
    print()
    for h in hit:
        print(
            f"{str(files[h['corpus_id']]).replace(config['notes_dir'], '')} with score {h['score']}"
        )
        print()

    return


if __name__ == "__main__":
    main(sys.stdin.read())

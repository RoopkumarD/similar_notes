import sys
from pathlib import Path
from pickle import HIGHEST_PROTOCOL, dump, load

from collect_files import extract_data_from_md
from embedding import embed, similarity

from . import utils

CONFIG_DIR = utils.get_config_dir()


def main():
    # getting the query
    query = ""
    if len(sys.argv) == 2:
        query = sys.argv[1]
        if utils.is_stdin_available() == True:
            print("Provide Query text from one input source only")
            return
    else:
        if utils.is_stdin_available() == True:
            query = sys.stdin.read().strip()
        else:
            print("USAGE:\nEither provide query text via stdin or args")
            print("Stdin Example: cat temp.md | simnotes")
            print('Args Example: simnotes "Query Text"')
            return

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
    cache_data = dict()
    if Path(f"{CONFIG_DIR}/cache_data.pickle").exists() == True:
        with open(f"{CONFIG_DIR}/cache_data.pickle", "rb") as f:
            cache_data = load(f)

    print("Checking for new/update and embedding it")
    cache_data, changed = extract_data_from_md(
        config["notes_dir"],
        config["exclude_dir"],
        config["exclude_file"],
        config["note_extension"],
        cache_data,
    )

    if len(cache_data) == 0:
        raise Exception("You don't have any notes in md files")

    # don't have to worry about writing as pickle won't duplicate it
    # https://docs.python.org/3/library/pickle.html#comparison-with-marshal first point
    if changed == True:
        with open(f"{CONFIG_DIR}/cache_data.pickle", "wb") as f:
            dump(cache_data, f, protocol=HIGHEST_PROTOCOL)

    # after getting the embedding of notes
    print("Embedding the query")
    query_embed = embed(query, True)

    # now getting similarity with this
    print("Finding similarity")
    corpus = [cache_data[key][0] for key in cache_data]
    hit = similarity(query_embed, corpus)

    # then printing the similarity score with filename and returning
    files = list(cache_data.keys())
    print("\n\n======================\n\n")
    print("Top files which are similar to given query:")
    print(
        "Value range from -1 to 1, where going toward 1 means note is close to query\n"
    )
    for score, id in zip(hit[0], hit[1]):
        print(f"{str(files[id]).replace(config['notes_dir'], '')} with score {score}\n")

    return

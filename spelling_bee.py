"""Contains the functions needed to run multiple word searches in parallel."""

import itertools as it
import multiprocessing as mp

# Using the enchant lib requires `brew install enchant` and a fresh install of pyenchant in the venv for this project
import enchant

from en_trie import Trie, get_trie
from memoize import memoize_prefix

en_dict = enchant.Dict("en_US")
dict_trie = get_trie()


# TODO this will likely need to be recursive, with the next level down of the trie being passed in as an arg
@memoize_prefix
def is_valid_prefix(prefix: str) -> bool:
    """Checks if the prefix will lead to a valid English word."""
    print("RAW PROCESSING")
    if dict_trie.starts_with(prefix):
        return True
    return False


def generate_letter_combos(
    user_letters: list[str], req_letter: str, rep_i: int
) -> list[str]:
    """Generates all possible letter combinations from the user input."""
    all_combos = []
    # TODO need to start with just the single letters and then for combos of increasing length, check if they're a valid prefix, and keep only those that are
    for c in list(it.product(user_letters, repeat=rep_i)):
        if dict_trie.search(word := "".join(c)) and req_letter in word:
            all_combos.append(word)

    return all_combos


def get_words(user_letters: str, req_letter: str, rep_i: int) -> list[str]:
    """Manages the process pool (1x process per length of word to be generated) and returns the results."""
    args = [(user_letters, req_letter, i) for i in range(4, rep_i + 1)]

    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(generate_letter_combos, args)

    return results


if __name__ == "__main__":  # Crucial for multiprocessing to work
    print(get_words("botlefu", "f", 8))
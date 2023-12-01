"""Implements a trie dictionary data structure."""

import pathlib
import pickle
import time

from prettytable import PrettyTable


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word) -> None:
        """Inserts a word into the Trie."""
        curr_node = self.root
        for char in word:
            if char not in curr_node.children:
                curr_node.children[char] = TrieNode()
            curr_node = curr_node.children[char]
        curr_node.is_word = True

    def search(self, word) -> bool:
        """Searches the Trie to check if the word exists in it."""
        curr_node = self.root
        for char in word:
            if not char in curr_node.children:
                return False
            curr_node = curr_node.children[char]
        if curr_node.is_word:
            return True
        return False

    def starts_with(self, prefix) -> bool:
        """Checks if the Trie contains any words that start with the prefix."""
        curr_node = self.root
        for char in prefix:
            if not char in curr_node.children:
                return False
            curr_node = curr_node.children[char]
        return True


def build_full_trie():
    """Builds a trie from the full dictionary."""
    with open("words_alpha.txt", "r") as f:
        words = f.readlines()

    trie = Trie()
    for word in words:
        trie.insert(word.strip())

    return trie


def get_trie():
    """Fetches the pickled trie if it exists, otherwise builds it and returns it."""
    PKL_DICT_PATH = pathlib.Path("en_dictionary_trie.pkl")
    if pathlib.Path(PKL_DICT_PATH).exists():
        with open(PKL_DICT_PATH, "rb") as f:
            return pickle.load(f)

    trie = build_full_trie()
    with open(PKL_DICT_PATH, "wb") as f:
        pickle.dump(trie, f)
    return trie


def performance_test() -> None:
    """Tests the performance (speed of checking if a given prefix leads to a word) of the trie vs a list."""
    trie = get_trie()
    with open("words_alpha.txt", "r") as f:
        words = f.readlines()
        words = [word.strip() for word in words]

    print("\nTesting list performance...")
    start = time.perf_counter()
    for _ in range(10_000):
        any(word.startswith("app") for word in words)
    end = time.perf_counter()
    total_list = round(end - start, 4)
    print(f"Time to search list: {total_list}")

    print("\nTesting trie performance...")
    start = time.perf_counter()
    for _ in range(10_000):
        trie.starts_with("app")
    end = time.perf_counter()
    total_trie = round(end - start, 4)
    print(f"Time to search trie: {total_trie}")

    avg = round((total_list + total_trie) / 2, 4)
    perc_diff = round(((total_list - total_trie) / avg) * 100, 2)

    comp_table = PrettyTable()
    comp_table.field_names = ["Data Structure", "Prefix Lookup Time"]
    comp_table.add_row(["List", total_list])
    comp_table.add_row(["Trie", total_trie])
    print(comp_table, "\n")
    print(f"The trie is {perc_diff}% faster than the list.\n")


if __name__ == "__main__":
    performance_test()

"""Main script for the NYT Spelling Bee game automation project."""

from prettytable import PrettyTable

import spelling_bee


def format_words(words: list[str]) -> str:
    """Formats the list of words into a PrettyTable."""
    all_words = sorted(words, key=lambda x: len(x), reverse=True)

    table = PrettyTable()
    table.field_names = ["Word", "Length"]
    for word in all_words:
        table.add_row([word, len(word)])

    return table


if __name__ == "__main__":  # Crucial for multiprocessing to work
    # Odd import placement required by pickling errors otherwise (main.py needs access to Trie, TrieNode).
    from en_trie import Trie, TrieNode

    user_letters = list(
        input("What is the letter set? (Including the required letter)\n>> ").lower()
    )
    print("\n")
    req_letter = input("What is the required letter?\n>> ").lower()

    valid_words = spelling_bee.get_words(
        user_letters=user_letters, req_letter=req_letter, rep_i=6
    )

    table = format_words(valid_words)
    print(table, "\n")

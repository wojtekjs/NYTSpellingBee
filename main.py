"""Main script for the NYT Spelling Bee game automation project."""

from prettytable import PrettyTable

import spelling_bee


def format_words(words: list[str]) -> PrettyTable:
    """Formats the list of words into a PrettyTable."""
    words = set(filter(lambda x: len(x) > 3, words))
    all_words = sorted(list(words), key=lambda x: len(x), reverse=True)

    table = PrettyTable()
    table.field_names = ["Word", "Length"]
    for word in all_words:
        table.add_row([word, len(word)])

    return table


def main() -> None:
    """Main function for the script."""
    user_letters = set(
        input("What is the letter set? (Including the required letter)\n>> ").lower()
    )
    req_letter = input("What is the required letter?\n>> ").lower()

    dict_trie = get_trie()
    valid_words = spelling_bee.get_words_sequential(
        user_letters=list(user_letters),
        req_letter=req_letter,
        dict_trie=dict_trie,
        working_prefixes=list(user_letters),
    )

    table = format_words(valid_words)
    print(table, "\n")


if __name__ == "__main__":
    # Odd import placement required by pickling errors otherwise (main.py needs access to Trie, TrieNode).
    from en_trie import Trie, TrieNode, get_trie

    main()

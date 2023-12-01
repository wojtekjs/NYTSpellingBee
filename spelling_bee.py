"""Contains the functions needed to run multiple word searches in parallel."""

from en_trie import Trie, TrieNode, get_trie


def get_words_sequential(
    user_letters: list[str],
    req_letter: str,
    *,
    max_word_len: int = 20,
    iteration: int = 1,
    working_prefixes: list[str] = [],
    valid_words: list[str] = [],
    dict_trie: Trie | None = None,
) -> list[str]:
    """Generates all possible words from the user input."""
    if iteration == max_word_len:
        return valid_words

    new_prefixes = []
    for prefix in working_prefixes:
        if req_letter in prefix and dict_trie.search(prefix):
            valid_words.append(prefix)

        for char in user_letters:
            if dict_trie.starts_with(new_prefix := prefix + char):
                new_prefixes.append(new_prefix)

    iteration += 1
    return get_words_sequential(
        user_letters=user_letters,
        req_letter=req_letter,
        max_word_len=max_word_len,
        iteration=iteration,
        working_prefixes=new_prefixes,
        valid_words=valid_words,
        dict_trie=dict_trie,
    )


if __name__ == "__main__":
    dict_trie = get_trie()
    print(
        get_words_sequential(
            "botlefu", "f", dict_trie=dict_trie, working_prefixes=list("botlefu")
        )
    )

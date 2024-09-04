import numpy as np
from collections import Counter


def meets_letter_requirements(word, letter_counts, letters_not_in_word):
    word_counter = Counter(word)
    if letters_not_in_word:
        for letter, required_count in letter_counts.items():
            if letter not in letters_not_in_word:
                if word_counter[letter] < required_count:
                    return False
            else:
                if word_counter[letter] != required_count:
                    return False
        return True

    else:
        for letter, required_count in letter_counts.items():
            if word_counter[letter] < required_count:
                return False
        return True


def meets_no_letter_requirements(word, filter_letters):
    for char in filter_letters:
        if char in word:
            return False
    return True


def meets_position_requirements(words, letters_without_position):
    """
    Filters out words that do not meet the position requirements specified in letters_without_position.

    :param words: (list of str) List of words to filter.
    :param letters_without_position: (list of str or None) List specifying required letters at certain positions.
                                     If a position is None, that position has no constraint.
    :return: (list of str) List of words that meet the position requirements.
    """
    valid_words = []

    for word in words:
        meets_requirements = True

        for i, letter in enumerate(letters_without_position):
            if letter is not None and word[i] == letter:
                meets_requirements = False
                break

        if meets_requirements:
            valid_words.append(word)

    return valid_words


def word_finder(word_length: int,
                letters_without_position: (list, np.ndarray) = None,
                letters_with_position: (list, np.ndarray) = None,
                letters_not_in_word: (list, np.ndarray) = None):
    """
    Pass only lower case without special characters and spaces

    :param word_length: (int) -- length of word that you search
    :param letters_without_position: (list, np.ndarray) -- letters that are in word but their position is unknown e.g. ["i", "g", "n"]
    :param letters_with_position: (list, np.ndarray) -- letters that position you know e.g. [None, None, "i", None, "b", None]
    :param letters_not_in_word: (list, np.ndarray) -- letters that are not in word (include letter when there
                                                      is not more than X of letter e.g. ["i", "s", "p"]
                                                      (in such configuration there are 2 "i")
    :return: list of possible words
    """

    if letters_without_position is None and letters_with_position is None:
        return "To many words..."

    if letters_with_position:
        if len(letters_with_position) != word_length:
            raise ValueError("Pattern length must match the specified word length.")

        # Read the file and create a NumPy array of words
        with open("clear_words.txt", 'r') as infile:
            words = np.array([line.strip() for line in infile])

        # Filter words based on length
        length_mask = np.vectorize(len)(words) == word_length
        filtered_words = words[length_mask]

        # Create a boolean mask for the pattern matching
        pattern = np.array(letters_with_position)
        pattern_mask = np.full(filtered_words.shape, True, dtype=bool)

        for i, char in enumerate(pattern):
            if char is not None:
                pattern_mask &= np.char.equal(np.char.array([word[i] for word in filtered_words]), char)

        valid_words = filtered_words[pattern_mask]

        # Check if valid words contain all letters_without_position
        if letters_without_position:
            letters_without_position = np.array(letters_without_position)

            all_letters = np.append(letters_with_position, letters_without_position)
            all_letters = all_letters[all_letters != np.array(None)]

            letter_counts = Counter(all_letters)

            valid_words = np.array(
                [word for word in valid_words if meets_letter_requirements(word, letter_counts, letters_not_in_word)])

            valid_words = meets_position_requirements(valid_words, letters_without_position)

        # Check if words don't contain letters they shouldn't
        if letters_not_in_word:
            filter_letters = set(letters_not_in_word)
            flat_letters_with_position = [char for char in letters_with_position if char is not None]
            if letters_with_position is not None:
                filter_letters -= set(flat_letters_with_position)
            if letters_without_position is not None:
                filter_letters -= set(letters_without_position)

            filter_letters = list(filter_letters)

            valid_words = np.array(
                [word for word in valid_words if meets_no_letter_requirements(word, filter_letters)])

        return valid_words


print(word_finder(word_length=8,
                  letters_without_position=['i', None, None, None, 't', None, None, 'g'],
                  letters_with_position=[None, None, None, 'i', None, None, 'n', None],
                  letters_not_in_word=['p', 'h', 's', 'n', 'd', 'i']))

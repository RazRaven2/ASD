def capitalize_words(text):
    """
    Capitalizes the first letter of each word in the given text.
    Raises a TypeError if the input is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    return " ".join(word.capitalize() for word in text.split())


def remove_extra_spaces(text):
    """
    Collapses repeated spaces and trims leading/trailing spaces.
    Raises a TypeError if the input is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    return " ".join(text.split())


def reverse_words(text):
    """
    Reverses the order of words in the given text.
    Raises a TypeError if the input is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    return " ".join(text.split()[::-1])

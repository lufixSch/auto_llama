import re

from auto_llama import ModelLoader
from auto_llama.exceptions import ExtrasDependenciesMissing

# Module specific dependencies
try:
    from num2words import num2words
    import nltk
    from nltk.stem import WordNetLemmatizer
except ImportError:
    raise ExtrasDependenciesMissing("text", "text")

ModelLoader.add("lemmatizer", lambda: WordNetLemmatizer())


def str_to_list(input: str | list[str]):
    """Take str or list[str] as input and return list[str]"""

    if isinstance(input, str):
        return [input]
    return input


def tokens_from_str(input: str):
    """Take str as input and split it into small parts"""

    return re.findall(r"\b\w+\b|\W+", input)


def to_lower(text: str):
    """Change all text to lower case"""

    # Match both words and non-word characters
    tokens = tokens_from_str(text)
    for i, token in enumerate(tokens):
        # Check if token is a word
        if re.match(r"^\w+$", token):
            # Check if token is not an abbreviation or constant
            if not re.match(r"^[A-Z]+$", token) and not re.match(r"^[A-Z_]+$", token):
                tokens[i] = token.lower()
    return "".join(tokens)


def merge_spaces(text: str):
    """Merge multiple spaces into a single space"""

    return re.sub(" +", " ", text)


def merge_symbols(text: str, symbol: str):
    """Merge symbols into a single symbol"""

    return re.sub(f"{symbol}+", f"{symbol}", text)


def delete_symbols(text: str, symbol: str):
    """Delete all occurences of the given symbol in the text"""

    return re.sub(f"{symbol}+", "", text)


def remove_punctuation(text: str):
    """
    Replace all sentence splitting punctuation with ', '
    and remove otherpunctuation"""

    punctuation = r"""!"#$%&'()*+-./:;<=>?@[\]^_`{|}~"""

    text = re.sub(r"([!,\-\.:;\?\|\~]) ", ", ", text)
    return text.translate(str.maketrans("", "", punctuation))


def remove_specific_pos(text: str):
    """
    In the English language, adverbs and interjections rarely provide meaningfull information.
    Removing them improves the embedding precision
    """

    # Match both words and non-word characters
    tokens = tokens_from_str(text)

    # Exclude adverbs and interjections
    excluded_tags = ["RB", "RBR", "RBS", "UH"]

    for i, token in enumerate(tokens):
        # Check if token is a word
        if re.match(r"^\w+$", token):
            # Part-of-speech tag the word
            pos = nltk.pos_tag([token])[0][1]
            # If the word's POS tag is in the excluded list, remove the word
            if pos in excluded_tags:
                tokens[i] = ""

    return "".join(tokens)


def lemmatize(text: str):
    """Reduce inflected or derived words to their base or dictionary forms."""
    return "".join([ModelLoader.get("lemmatizer").lemmatize(word) for word in tokens_from_str(text)])


def num_to_word(text: str, min_len: int = 1):
    """
    Change numbers to words to improve attention on numbers
    """

    # Match both words and non-word characters
    tokens = tokens_from_str(text)
    for i, token in enumerate(tokens):
        # Check if token is a number of length `min_len` or more
        if token.isdigit() and len(token) >= min_len:
            # 740700 will become "seven hundred and forty thousand seven hundred".
            try:
                tokens[i] = num2words(int(token)).replace(",", "")  # Remove commas from num2words.
            except ValueError:
                # catch error for super- or subscript digits
                pass

    return "".join(tokens)


def num_to_char_long(text, min_len: int = 1):
    """
    Change digits to chars and repeat every char as often as the value of the digit to improve attention on numbers
    """

    def convert_token(token):
        return "".join((chr(int(digit) + 65) * (i + 1)) for i, digit in enumerate(token[::-1]))[::-1]

    # Match both words and non-word characters
    tokens = tokens_from_str(text)
    for i, token in enumerate(tokens):
        # Check if token is a number of length `min_len` or more
        if token.isdigit() and len(token) >= min_len:
            # This is done to pay better attention to numbers (e.g. ticket numbers, thread numbers, post numbers)
            # 740700 will become HHHHHHEEEEEAAAAHHHAAA
            tokens[i] = convert_token(tokens[i])
    return "".join(tokens)


def num_to_char(text, min_len: int = 1):
    """
    Change digits to char to improve attention on numbers
    """

    # Match both words and non-word characters
    tokens = tokens_from_str(text)
    for i, token in enumerate(tokens):
        # Check if token is a number of length `min_len` or more
        if token.isdigit() and len(token) >= min_len:
            # This is done to pay better attention to numbers (e.g. ticket numbers, thread numbers, post numbers)
            # 740700 will become HEAHAA
            tokens[i] = "".join(chr(int(digit) + 65) for digit in token)
    return "".join(tokens)

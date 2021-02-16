"""Calculate the similarity between two documents."""

import math
import re
import sys

STOP_WORDS = {'a', 'an', 'the', 'of', 'for', 'and', 'or'}


def clean(doc: str) -> str:
    """
    Cleans a string for processing.

    Removes non-alphanumeric characters and extra whitespace.
    Converts to lowercase.

    Parameters:
    doc (str): String to be cleaned

    Returns:
    str: Cleaned string
    """
    # remove non-alphanumeric or space characters
    doc = re.sub(r'[^a-zA-Z0-9 ]', '', doc)
    # trim continous whitespace down to 1 space
    doc = re.sub(r'\s+', ' ', doc)
    doc = doc.lower().strip()
    return doc


def tokenize(doc: str) -> list:
    """
    Creates tokenized representation of a document string.

    Splits a string on whitespace, ignoring words that are in `STOP_WORDS`.

    Parameters:
    doc (str): String to be tokenized

    Returns:
    [str]: list of individual words
    """
    tokens = [word for word in doc.split() if word not in STOP_WORDS]
    return tokens


def frequency(tokens: list, seq_len: int = 5) -> dict:
    """
    Counts the frequency of unique sequences in a list of tokens.

    Returns a dictionary where keys are unique sequences of length
    1 to `seq_len` and values are the count of occurences of those
    sequences in the `tokens` list.

    Parameters:
    tokens (list): list of tokens parsed from a document.
    seq_len (int): (min 1) max length of sequences to count.

    Returns:
    dict: {sequence: count}
    """
    assert seq_len >= 1, 'seq_len must be at least 1.'
    seq_count = {}

    for length in range(1, seq_len + 1):
        for i in range(len(tokens) - (length - 1)):
            seq = tuple(tokens[i:i+length])
            if seq in seq_count:
                seq_count[seq] = seq_count[seq] + 1
            else:
                seq_count[seq] = 1

    return seq_count


def dot_product(tf1, tf2):
    """
    Calculates the dot product of two term frquency vectors.

    Returns the dot product of the frequencies of matching terms
    in two term frequency vectors. The term frequency vectors are
    dictionaries with the term as the key and the frequency as the value.

    Parameters:
    tf1 (dict): Term frequency vector 1 {(term, ): frequency}
    tf2 (dict): Term frequency vector 2 {(term, ): frequency}

    Returns:
    int: Dot product of the frequencies of matching terms
    """
    sum = 0.0
    for k1 in tf1:
        if k1 in tf2:
            sum = sum + (tf1[k1] * tf2[k1])
    return sum


def cosine_similarity(tf1, tf2):
    """
    Calculates the cosine similarity between two term frequency vectors.

    Returns the cosine similarity of two term frequency vectors. The term
    frequency vectors are dictionaries with the term as the key and the
    frequency as the value.

    Parameters:
    tf1 (dict): Term frequency vector 1 {(term, ): frequency}
    tf2 (dict): Term frequency vector 2 {(term, ): frequency}

    Returns:
    float: Cosine similarity of two term frequency vectors
    """
    numerator = dot_product(tf1, tf2)
    denominator = math.sqrt(dot_product(tf1, tf1)) * \
        math.sqrt(dot_product(tf2, tf2))

    return numerator / denominator


def similarity(d1, d2):
    """
    Calculate the similarity between two document strings.

    Returns the rounded cosine similarity between two documents
    after cleaning and tokenizing them.

    Parameters:
    d1 (str): Document 1
    d2 (str): Document 2

    Returns:
    float: similarity
    """
    # clean and tokenize
    d1 = tokenize(clean(d1))
    d2 = tokenize(clean(d2))

    # build token index so as to not be operating on strings
    vocab = list(set(d1 + d2))
    v1 = [vocab.index(token) for token in d1]
    v2 = [vocab.index(token) for token in d2]

    # calculate token frequency
    seq_length = 1
    f1 = frequency(v1, seq_length)
    f2 = frequency(v2, seq_length)

    return round(cosine_similarity(f1, f2), 2)


def load_doc(filename) -> str:
    """
    Opens a file and reads it in as a string.

    Parameters:
    filename (str): Path to file

    Returns:
    str: contents of file
    """
    with open(filename, 'r') as f:
        doc = f.read()
    return doc


if __name__ == '__main__':
    doc1 = doc2 = None
    if '-h' in sys.argv or '--help' in sys.argv:
        print('Calculate similarity of two documents.')
        print(f'usage: python {sys.argv[0]} [filename] [filename]')
        print('If filenames are not provided, user will be prompted', end=' ')
        print('to enter the document contents.')
    elif len(sys.argv) == 1:
        doc1 = input('Document 1: ')
        doc2 = input('Document 2: ')
    elif len(sys.argv) == 2:
        doc1 = load_doc(sys.argv[1])
        doc2 = input('Document 2: ')
    else:
        doc1 = load_doc(sys.argv[1])
        doc2 = load_doc(sys.argv[2])

    if doc1 and doc2:
        doc_sim = similarity(doc1, doc2)
        print(f'Similarity score: {doc_sim}')

"""Handler for arguments"""

from dataclasses import dataclass
from typing import Annotated

from dykes import StoreTrue, parse_args
from dykes.options import Flags, NArgs

from py_wordsearch_gen.consts import LETTERS


@dataclass
class WSArgs:
    """Word Search Generator"""

    words: Annotated[
        list[str],
        'List of words for the search.',
        NArgs(value='+'),
    ]
    size: Annotated[
        int,
        'The size of the word search grid from 5 - 50. (Default: 10)',
        NArgs('?'),
        Flags('-s', '--size'),
    ] = 10
    min_word: Annotated[
        int,
        'The minimum word length. Cannot be larger than the size of the grid. (Default: 4)',
        NArgs('?'),
        Flags('-m', '--min'),
    ] = 4
    diagonal: Annotated[StoreTrue, 'Allow words to be placed diagonally.'] = False
    reverse: Annotated[StoreTrue, 'Allow words to be placed backwards.'] = False
    answer_key: Annotated[
        StoreTrue,
        'Print the answer key ahead of the puzzle.',
        Flags('-k', '--answer-key'),
    ] = False


def get_parameters() -> tuple[bool, bool, bool, int, list[str]]:
    """
    Get the parameters for the word search

    :return: The parameters for the word search
    """
    args = parse_args(WSArgs)
    if not 5 <= (grid_size := args.size) <= 50:
        print(f'Illegal size: {grid_size}. Grid size must be between 5 and 50.')
        exit(1)
    if not 3 <= (shortest := args.min_word) <= grid_size:
        print(f'Illegal minimum word length {shortest}. Must be between 3 and {grid_size}.')
        exit(1)
    if illegal_words := [
        word
        for word in args.words
        if (len(word) < shortest or len(word) > grid_size) or any(letter not in LETTERS for letter in word.upper())
    ]:
        print('Illegal words found:')
        for word in illegal_words:
            print('Too ' + ('short: ' if len(word) < shortest else 'long:  ') + word)
        exit(1)
    words = [word.upper() for word in args.words]
    return args.answer_key, args.reverse, args.diagonal, grid_size, words

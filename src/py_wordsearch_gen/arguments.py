"""Handler for arguments"""

from dataclasses import dataclass
from typing import Annotated

from dykes import StoreTrue, parse_args
from dykes.options import Flags, NArgs

OPTIONAL = NArgs('?')

from py_wordsearch_gen.consts import LETTERS



@dataclass
class WSArgs:
    """Word Search Generator"""

    words: Annotated[
        list[str],
        'List of words for the search.',
        NArgs(value='+'),
    ]
    # size: Annotated[
    #     int,
    #     'The size of the word search grid from 5 - 50. (Default: 10)',
    #     NArgs('?'),
    #     Flags('-s', '--size'),
    # ] = 10
    width: Annotated[
        int,
        'Width of puzzle, (Default: 10)',
        OPTIONAL,
        Flags('-w', '--width')
    ] = 10
    height: Annotated[
        int,
        'Height of puzzle, If not set will be the same as the width (square puzzle.)',
        OPTIONAL,
        Flags('-t', '--height')
    ] = 0
    min_word: Annotated[
        int,
        'The minimum word length. Cannot be larger than the size of the grid. (Default: 4)',
        OPTIONAL,
        Flags('-m', '--min'),
    ] = 4
    diagonal: Annotated[StoreTrue, 'Allow words to be placed diagonally.'] = False
    reverse: Annotated[StoreTrue, 'Allow words to be placed backwards.'] = False
    answer_key: Annotated[
        StoreTrue,
        'Print the answer key ahead of the puzzle.',
        Flags('-k', '--answer-key'),
    ] = False


def get_parameters() -> tuple[bool, bool, bool, tuple[int, int], list[str]]:
    """
    Get the parameters for the word search

    :return: The parameters for the word search
    """
    args = parse_args(WSArgs)
    width = args.width
    height = args.height if args.height else width
    grid_size = (width, height)
    if not all(5 <= dimension <= 50 for dimension in grid_size):
        print(f'Illegal size: {grid_size}. Grid size must be between 5 and 50.')
        exit(1)
    if not 3 <= (shortest := args.min_word) <= min(grid_size):
        print(f'Illegal minimum word length {shortest}. Must be between 3 and {min(grid_size)}.')
        exit(1)
    if illegal_words := [
        word
        for word in args.words
        if (len(word) < shortest or len(word) > max(grid_size)) or any(letter not in LETTERS for letter in word.upper())
    ]:
        print('Illegal words found:')
        for word in illegal_words:
            print('Too ' + ('short: ' if len(word) < shortest else 'long:  ') + word)
        exit(1)
    words = [word.upper() for word in args.words]
    return args.answer_key, args.reverse, args.diagonal, grid_size, words

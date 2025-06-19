"""Handler for arguments"""

from dataclasses import dataclass
from typing import Annotated

from dykes import StoreTrue, parse_args
from dykes.options import Flags, NArgs

from py_wordsearch_gen.consts import EXCLUDED_LETTERS, LETTERS

OPTIONAL = NArgs('?')


@dataclass
class WSArgs:
    """Word Search Generator"""

    words: Annotated[
        list[str],
        'List of words for the search.',
        NArgs(value='+'),
    ]
    width: Annotated[
        int,
        'Width of puzzle, (Default: 10)',
        OPTIONAL,
        Flags('-w', '--width'),
    ] = 10
    height: Annotated[
        int,
        'Height of puzzle, If not set will be the same as the width (square puzzle.)',
        OPTIONAL,
        Flags('-t', '--height'),
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
    excluded_letters: Annotated[
        str,
        f'A list of letters to be excluded as fill. Defaults to {repr(EXCLUDED_LETTERS)}',
        Flags('-x', '--exclude'),
        NArgs('?'),
    ] = EXCLUDED_LETTERS


def get_parameters() -> tuple[bool, bool, bool, tuple[int, int], list[str], list[str]]:
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
    words = [word.upper() for word in args.words]
    if illegal_words := [
        word
        for word in words
        if (len(word) < shortest or len(word) > max(grid_size)) or any(letter not in LETTERS for letter in word)
    ]:
        print('Illegal words found:')
        for word in illegal_words:
            print('Too ' + ('short: ' if len(word) < shortest else 'long:  ') + word)
        exit(1)
    return (
        args.answer_key,
        args.reverse,
        args.diagonal,
        grid_size,
        words,
        list(args.excluded_letters.upper()) if args.excluded_letters else list(),
    )


def print_parameters(
    backwards: bool, diagonal: bool, grid_size: tuple[int, int], words: list[str], excluded_letters: list[str]
):
    """Print the parameters being used to create the search"""
    print('Welcome to the Word Search Generator')
    print('We will be creating your search with the following attributes:')
    print(f'\tThe grid will be {"x".join(map(str, grid_size))} letters.')
    print(f'\tWe will {"allow" if diagonal else "not allow"} words to be placed diagonally.')
    print(f'\tWe will {"allow" if backwards else "not allow"} words to be placed backwards.')
    if excluded_letters:
        print(f'\tThe letters {", ".join(excluded_letters)} will not be used as fill.')
    print('\tThe words we are using are:')
    for n in range(0, len(words), 5):
        print('\t\t' + ', '.join(words[n : n + 5]))

#! /usr/bin/env python3

import argparse
import copy
import sys
from argparse import Namespace
from itertools import permutations
from random import choice, randint, shuffle

LETTERS = [
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z',
]


def get_next(x: int, y: int, d: str) -> tuple[int, int]:
    """
    Get the next set of coordinates based on current location and direction

    :param x: x coordinate
    :param y: y coordinate
    :param d: direction (can be 'v', 'h', 'dd', 'du')
    :return: Next coordinates
    :raises: ValueError for unrecognized direction
    """
    match d:
        case 'v':
            return x + 1, y
        case 'h':
            return x, y + 1
        case 'du':
            return x - 1, y + 1
        case 'dd':
            return x + 1, y + 1
    raise ValueError(f'Invalid direction {d}')


def can_place(word: str, x: int, y: int, d: str, grid: list[list[str]]) -> bool:
    """
    Determine whether a word can be placed at the gine starting coordinates

    :param word: The word
    :param x: x coordinate
    :param y: y coordinate
    :param d: direction to place the word
    :param grid: The grid
    :return: True if it is possible to place the word otherwise false
    """
    nx, ny = x, y
    for c in word:
        if not (0 <= nx < len(grid) and 0 <= ny < len(grid)):
            return False
        existing = grid[nx][ny]
        if not (c == existing or existing == '.'):
            return False
        nx, ny = get_next(nx, ny, d)
    return True


def place(word: str, x: int, y: int, d: str, grid: list[list[str]]):
    """
    Update the grid by placing the word at the starting coordinates

    :param word: The word
    :param x: x coordinate
    :param y: y coordinate
    :param d: direction to place the word
    :param grid: The grid
    """
    nx, ny = x, y
    for c in word:
        grid[nx][ny] = c
        nx, ny = get_next(nx, ny, d)


def grid_as_str(grid: list[list[str]]) -> str:
    """
    Get the grid in string form for outputting

    :param grid: The grid
    :return: The grid as a string
    """
    return '\n'.join(' '.join(row) for row in grid)


def fill_grid(grid: list[list[str]]):
    """
    Fill unfilled locations in the grid with letters

    :param grid: The grid
    :return: Updated grid with all spaces filled with letters
    """
    fillers = [letter for letter in LETTERS if letter not in 'JQZX']
    for row in grid:
        for i, c in enumerate(row):
            if c == '.':
                row[i] = choice(fillers)


def get_options(size: int) -> list[tuple[int, int]]:
    """
    Get a randomized list of starting points for the words.

    :param size: Size of the grid
    :return: Randomized list of coordinates inside the grid
    """
    options = list(permutations(range(size), 2))
    shuffle(options)
    return options


def build_search(
    backwards: bool, diagonal: bool, grid_size: int, words: list[str]
) -> tuple[list[list[str]], list[str]]:
    """
    Build the search

    :param backwards: Allow words to be placed backwards
    :param diagonal: Allow words to be placed diagonally
    :param grid_size: The size of the grid
    :param words: The words to place
    :return: The word search containing only the entered words (the answer key)
    """
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    directions = ['h', 'v']
    if diagonal:
        directions.extend(['dd', 'du'])
    word_list = copy.copy(words)
    while words:
        _directions = copy.copy(directions)
        _word = choice(words)
        word = _word[::-1] if (backwards and randint(0, 1)) else _word
        while _directions:
            direction = choice(_directions)
            for x, y in get_options(grid_size):
                if can_place(word, x, y, direction, grid):
                    place(word, x, y, direction, grid)
                    break
            else:
                _directions.remove(direction)
                continue
            break
        else:
            print(f'Unable to place {repr(_word)}.')
        words.remove(_word)
    return grid, word_list


def parse_args() -> Namespace:
    """
    Parse the command line arguments

    :return: The parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        prog=sys.argv[0].rsplit('/', 1)[-1],
        description='Word Search Generator',
    )
    parser.add_argument(
        '-s',
        '--size',
        type=int,
        default=10,
        required=False,
        help='The size of the word search grid from 5 - 50. (Default: 10)',
    )
    parser.add_argument(
        '-m',
        '--min',
        type=int,
        default=4,
        required=False,
        help='The minimum word length. Cannot be larger than the size of the grid. (Default: 4)',
    )
    parser.add_argument(
        '-d',
        '--diagonal',
        action='store_true',
        help='Allow words to be placed diagonally.',
    )
    parser.add_argument(
        '-r',
        '--reverse',
        action='store_true',
        help='Allow words to be placed backwards.',
    )
    parser.add_argument(
        'words',
        nargs='+',
        help='List of words for the search.',
    )
    parser.add_argument(
        '-k', '--answer-key', action='store_true', dest='answer_key', help='Print the answer key ahead of the puzzle.'
    )
    return parser.parse_args()


def get_parameters() -> tuple[bool, bool, bool, int, list[str]]:
    """
    Get the parameters for the word search

    :return: The parameters for the word search
    """
    args = parse_args()
    if not 5 <= (grid_size := args.size) <= 50:
        print(f'Illegal size: {grid_size}. Grid size must be between 5 and 50.')
        exit(1)
    if not 3 <= (shortest := args.min) <= grid_size:
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


def output_search(answer_key: bool, grid: list[list[str]], word_list: list[str]):
    """
    Print the word search

    :param answer_key: When true, print the answer key
    :param grid: The word search grid containing just the words
    :param word_list: The list of words in the search
    """
    if answer_key:
        print('\n\n\nAnswer Key\n\n')
        print(grid_as_str(grid))
    fill_grid(grid)
    print('\n\n\nPuzzle\n\n')
    print(grid_as_str(grid))
    print('\n\nWord List\n\n')
    shuffle(word_list)
    for n in range(0, len(word_list), 5):
        print(' '.join(word_list[n : n + 5]))


def print_parameters(backwards: bool, diagonal: bool, grid_size: int, words: list[str]):
    """Print the parameters being used to create the search"""
    print('Welcome to the Word Search Generator')
    print('We will be creating your search with the following attributes:')
    print(f'\tThe grid will be {grid_size}x{grid_size} letters.')
    print(f'\tWe will {"allow" if diagonal else "not allow"} words to be placed diagonally.')
    print(f'\tWe will {"allow" if backwards else "not allow"} words to be placed backwards.')
    print('\tThe words we are using are:')
    for n in range(0, len(words), 5):
        print('\t\t' + ', '.join(words[n : n + 5]))


def main():
    answer_key, backwards, diagonal, grid_size, words = get_parameters()

    print_parameters(backwards, diagonal, grid_size, words)

    grid, word_list = build_search(backwards, diagonal, grid_size, words)

    output_search(answer_key, grid, word_list)


if __name__ == '__main__':
    main()

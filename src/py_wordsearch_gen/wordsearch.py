#! /usr/bin/env python3

import copy
from itertools import permutations
from random import choice, randint, shuffle

from py_wordsearch_gen.arguments import get_parameters, print_parameters
from py_wordsearch_gen.consts import LETTERS


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


def can_place(word: str, x: int, y: int, d: str, grid: list[list[str]], width: int, height: int) -> bool:
    """
    Determine whether a word can be placed at the gine starting coordinates

    :param word: The word
    :param x: x coordinate
    :param y: y coordinate
    :param d: direction to place the word
    :param grid: The grid
    :param width: Width of the grid
    :param height: Height of the grid
    :return: True if it is possible to place the word otherwise false
    """
    nx, ny = x, y
    for c in word:
        if not (0 <= nx < height and 0 <= ny < width):
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


def fill_grid(grid: list[list[str]], excluded_letters: list[str]):
    """
    Fill unfilled locations in the grid with letters

    :param grid: The grid
    :param excluded_letters: List of letters to not use as fill.
    :return: Updated grid with all spaces filled with letters
    """
    fillers = [letter for letter in LETTERS if letter not in excluded_letters]
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
    backwards: bool, diagonal: bool, grid_size: tuple[int, int], words: list[str]
) -> tuple[list[list[str]], list[str]]:
    """
    Build the search

    :param backwards: Allow words to be placed backwards
    :param diagonal: Allow words to be placed diagonally
    :param grid_size: The size of the grid
    :param words: The words to place
    :return: The word search containing only the entered words (the answer key)
    """
    width, height = grid_size
    grid = [['.' for _ in range(width)] for _ in range(height)]
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
            for x, y in get_options(max(grid_size)):
                if can_place(word, x, y, direction, grid, width, height):
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


def output_search(answer_key: bool, grid: list[list[str]], word_list: list[str], excluded_letters: list[str]):
    """
    Print the word search

    :param answer_key: When true, print the answer key
    :param grid: The word search grid containing just the words
    :param word_list: The list of words in the search
    """
    if answer_key:
        print('\n\n\nAnswer Key\n\n')
        print(grid_as_str(grid))
    fill_grid(grid, excluded_letters)
    print('\n\n\nPuzzle\n\n')
    print(grid_as_str(grid))
    print('\n\nWord List\n\n')
    shuffle(word_list)
    for n in range(0, len(word_list), 5):
        print(' '.join(word_list[n : n + 5]))


def main():
    answer_key, backwards, diagonal, grid_size, words, excluded_letters = get_parameters()

    print_parameters(backwards, diagonal, grid_size, words, excluded_letters)

    grid, word_list = build_search(backwards, diagonal, grid_size, words)

    output_search(answer_key, grid, word_list, excluded_letters)


if __name__ == '__main__':
    main()

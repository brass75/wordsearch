# py-wordsearch-gen - Word Search Generator

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Tests](https://github.com/brass75/wordsearch/actions/workflows/test.yml/badge.svg)](https://github.com/brass75/wordsearch/actions/workflows/test.yml)
[![Mastodon Follow](https://img.shields.io/mastodon/follow/109552736199041636?domain=https%3A%2F%2Ftwit.social&style=flat)](https://twit.social/@brass75)

py-wordsearch-gen is a word search generator, originally written to generate a word search for distribution at the PSF booth
at PyCon US 2025. It is incredibly simple to use and will generate a new word search with every run.

## Installation

Installation is easy:
```shell
pip install py-wordsearch-gen
```

# Usage

To use just run `wordsearch` from the command line.

```shell
usage: wordsearch.py [-h] [-w [WIDTH]] [-t [HEIGHT]] [-m [MIN_WORD]] [-d] [-r] [-k] [-x [EXCLUDED_LETTERS]] words [words ...]

Word Search Generator

positional arguments:
  words                 List of words for the search.

options:
  -h, --help            show this help message and exit
  -w, --width [WIDTH]   Width of puzzle, (Default: 10)
  -t, --height [HEIGHT]
                        Height of puzzle, If not set will be the same as the width (square puzzle.)
  -m, --min [MIN_WORD]  The minimum word length. Cannot be larger than the size of the grid. (Default: 4)
  -d, --diagonal        Allow words to be placed diagonally.
  -r, --reverse         Allow words to be placed backwards.
  -k, --answer-key      Print the answer key ahead of the puzzle.
  -x, --exclude [EXCLUDED_LETTERS]
                        A list of letters to be excluded as fill. Defaults to 'JQXZ'
```

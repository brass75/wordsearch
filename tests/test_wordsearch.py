import pytest

from py_wordsearch_gen import wordsearch


@pytest.fixture
def test_grid():
    yield [['.' for _ in range(5)] for _ in range(5)]


@pytest.fixture
def patches(monkeypatch):
    monkeypatch.setattr('py_wordsearch_gen.wordsearch.choice', lambda list_: list_[-1])
    monkeypatch.setattr('py_wordsearch_gen.wordsearch.shuffle', lambda list_: list_)
    monkeypatch.setattr('py_wordsearch_gen.wordsearch.randint', lambda *_, **__: 0)


class TestWordSearch:
    def test_fill_grid(self, test_grid, patches):
        wordsearch.fill_grid(test_grid)
        assert test_grid == [['Y' for _ in range(5)] for _ in range(5)]

    def test_grid_as_str(self, test_grid):
        assert (
            wordsearch.grid_as_str(test_grid)
            == """. . . . .
. . . . .
. . . . .
. . . . .
. . . . ."""
        )

    @pytest.mark.parametrize(
        'backwards, diagonal, grid_size, words, expected, output',
        [
            (
                False,
                False,
                (5, 5),
                ['GIRL', 'BOY', 'DOG'],
                (
                    [
                        ['.', 'D', 'B', 'G', '.'],
                        ['.', 'O', 'O', 'I', '.'],
                        ['.', 'G', 'Y', 'R', '.'],
                        ['.', '.', '.', 'L', '.'],
                        ['.', '.', '.', '.', '.'],
                    ],
                    ['GIRL', 'BOY', 'DOG'],
                ),
                '',
            ),
            (
                False,
                False,
                (5, 6),
                ['GIRL', 'BOY', 'DOG', 'TOOLONG'],
                (
                    [
                        ['.', 'D', 'B', 'G', '.'],
                        ['.', 'O', 'O', 'I', '.'],
                        ['.', 'G', 'Y', 'R', '.'],
                        ['.', '.', '.', 'L', '.'],
                        ['.', '.', '.', '.', '.'],
                        ['.', '.', '.', '.', '.'],
                    ],
                    ['GIRL', 'BOY', 'DOG', 'TOOLONG'],
                ),
                "Unable to place 'TOOLONG'.\n",
            ),
            (
                True,
                True,
                (5, 6),
                ['GIRL', 'BOY', 'DOG', 'CHILD'],
                (
                    [
                        ['.', '.', 'G', 'Y', 'D'],
                        ['.', 'O', 'O', 'L', 'L'],
                        ['D', 'B', 'I', 'R', '.'],
                        ['.', 'H', 'I', '.', '.'],
                        ['C', 'G', '.', '.', '.'],
                        ['.', '.', '.', '.', '.'],
                    ],
                    ['GIRL', 'BOY', 'DOG', 'CHILD'],
                ),
                '',
            ),
        ],
    )
    def test_build_search(self, monkeypatch, patches, capsys, backwards, diagonal, grid_size, words, expected, output):
        assert wordsearch.build_search(backwards, diagonal, grid_size, words) == expected
        assert capsys.readouterr().out == output

    @pytest.mark.parametrize(
        'direction, x, y, output, exception',
        [
            ('v', 5, 5, (6, 5), False),
            ('h', 5, 5, (5, 6), False),
            ('du', 4, 5, (3, 6), False),
            ('dd', 5, 4, (6, 5), False),
            ('N', 5, 5, (6, 5), True),
        ],
    )
    def test_next(self, direction, x, y, output, exception):
        if exception:
            with pytest.raises(ValueError):
                wordsearch.get_next(x, y, direction)
        else:
            assert wordsearch.get_next(x, y, direction) == output

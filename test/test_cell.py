import pytest

from src.sudoku.cell import Cell


def test_create_valid_cell_with_number():
    c = Cell("5", (1, 1))
    assert c.number() == 5
    assert len(c.maybe_numbers()) == 0
    assert c.pos() == (1, 1)


def test_create_valid_cell_with_x():
    c = Cell("x", (5, 8))
    assert c.number() is None
    assert len(c.maybe_numbers()) == 9
    assert c.maybe_numbers() == list(range(1, 10))
    assert c.pos() == (5, 8)


@pytest.mark.parametrize("row,col,block_idx", [(0, 0, 0),
                                               (1, 4, 1),
                                               (2, 6, 2),
                                               (4, 0, 3),
                                               (5, 2, 3),
                                               (3, 3, 4),
                                               (5, 6, 5),
                                               (5, 8, 5),
                                               (8, 8, 8)])
def test_get_block_idx(row, col, block_idx):
    c = Cell("x", (row, col))
    assert c.get_block_idx() == block_idx


def test_reduce_maybe_numbers_with_remaining_numbers():
    c = Cell("x", (5, 8))
    assert not c.reduce_maybe_numbers([1, 2, 7])
    assert c.maybe_numbers() == [3, 4, 5, 6, 8, 9]
    assert c.number() is None


def test_reduce_maybe_numbers_without_remaining_numbers():
    c = Cell("x", (5, 8))
    assert not c.reduce_maybe_numbers([1, 2, 7])
    assert c.reduce_maybe_numbers([3, 4, 6, 8, 9])
    assert len(c.maybe_numbers()) == 0
    assert c.number() == 5


def test_eq():
    c1 = Cell("1", (0, 1))
    c2 = Cell("2", (1, 3))
    c3 = Cell("3", (0, 1))
    assert not c1 == c2
    assert not c2 == c3
    assert c1 == c3


def test_new_fixed_number():
    c1 = Cell("X", (0, 0))
    c1.new_fixed_number(1)
    assert c1.is_number_fixed()
    assert c1.number() == 1
    assert len(c1.maybe_numbers()) == 0

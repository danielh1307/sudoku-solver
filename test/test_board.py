from src.sudoku.board import Board


def test_get_row():
    board = get_board()
    row = board.get_row(0)
    assert list(map(str, row)) == ['1', 'X', 'X', '8', '5', 'X', '4', '7', 'X']


def test_get_row_numbers():
    board = get_board()
    row = board.get_row_numbers(0)
    assert row == [1, 8, 5, 4, 7]


def test_get_col():
    board = get_board()
    col = board.get_col(2)
    assert list(map(str, col)) == ['X', 'X', 'X', 'X', '4', '1', 'X', 'X', '5']


def test_get_col_numbers():
    board = get_board()
    col = board.get_col_numbers(2)
    assert col == [4, 1, 5]


def test_get_block():
    board = get_board()
    block0 = board.get_block(0)
    block5 = board.get_block(5)
    block8 = board.get_block(8)
    assert list(map(str, block0)) == ['1', 'X', 'X', 'X', 'X', 'X', 'X', '6', 'X']
    assert list(map(str, block5)) == ['8', '1', 'X', 'X', 'X', 'X', '7', '3', 'X']
    assert list(map(str, block8)) == ['X', 'X', '3', 'X', 'X', 'X', 'X', '2', '1']


def test_get_block_numbers():
    board = get_board()
    block = board.get_block_numbers(0)
    assert block == [1, 6]


def test_get_cell():
    board = get_board()
    cell = board.get_cell((0, 8))
    assert not cell.is_number_fixed()
    assert cell.maybe_numbers() == list(range(1, 10))


def test_no_doubles():
    board = get_board()
    assert board.no_doubles((1, 2, 3))
    assert not board.no_doubles((1, 2, 3, 1))


def get_board():
    with open("../board/11.txt", "r") as board_input:
        lines = board_input.read().split("\n")

    new_lines = list(map(lambda x: x.split(","), lines))
    return Board(new_lines)

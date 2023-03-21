from src.sudoku.board import Board
import src.sudoku.board_printer as printer
import time


def get_board(sudoku_number_):
    with open("../../board/" + sudoku_number_, "r") as board_input:
        lines = board_input.read().split("\n")

    new_lines = list(map(lambda x: x.split(","), lines))
    return Board(new_lines)


def show_board(board, text):
    print("*******************************************")
    print("************ ", text, " ***************")
    printer.print_board(board)


def main(sudoku_number_):
    board = get_board(sudoku_number_)
    show_board(board, sudoku_number_)

    # Easiest solution. We are already starting with a solved board.
    if board.is_solved():
        return True

    # First we reduce the "maybe numbers". If there are already fixed numbers in the row, column or block of a cell,
    # it cannot be a "maybe number" any longer. If only one "maybe number" remains, we know this must be the fixed
    # number of that cell.
    board.reduce_maybe_numbers()
    if board.is_solved():
        show_board(board, "After maybe numbers have been reduced")
        return True

    # If a cell contains a "maybe number" which no other cell in the column, row or block contains, we can set this
    # as a fixed number.
    board.set_last_remaining_number()
    if board.is_solved():
        show_board(board, "After maybe numbers have been changed to fixed numbers")
        return True

    # Uses the backtracking algorithm, that means it tries every remaining "maybe number" until we find a valid
    # solution.
    board.solve_with_backtrack()
    if board.is_solved():
        show_board(board, "After backtrack")
        return True

    return False


if __name__ == '__main__':
    sudoku_numbers = ["11.txt", "12.txt", "44.txt", "175.txt", "evil.txt", "medium.txt"]

    for sudoku_number in sudoku_numbers:
        start_time = time.time()
        solved = main(sudoku_number)
        stop_time = time.time()
        if solved:
            print(f"It took me {stop_time - start_time}s to solve this problem")
        else:
            print(f"Unfortunately I was not able to solve this problem - tried it for {stop_time - start_time}s")

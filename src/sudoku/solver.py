from src.sudoku.board import Board
import src.sudoku.board_printer as printer
import time


def get_board():
    with open("../../board/175.txt", "r") as board_input:
        lines = board_input.read().split("\n")

    new_lines = list(map(lambda x: x.split(","), lines))
    return Board(new_lines)


def show_board(board, text):
    print("*******************************************")
    print("************ ", text, " ***************")
    printer.print_board(board)


def main():
    board = get_board()
    show_board(board, "Starting Board")
    if board.is_solved():
        return True

    board.reduce_maybe_numbers()
    if board.is_solved():
        show_board(board, "After maybe numbers have been reduced")
        return True

    board.set_last_remaining_number()
    if board.is_solved():
        show_board(board, "After maybe numbers have been changed to fixed numbers")
        return True

    board.solve_with_backtrack()
    if board.is_solved():
        show_board(board, "After backtrack")
        return True

    return False


if __name__ == '__main__':
    start_time = time.time()
    solved = main()
    stop_time = time.time()
    if solved:
        print(f"It took me {stop_time - start_time}s to solve this problem")
    else:
        print(f"Unfortunately I was not able to solve this problem - tried it for {stop_time - start_time}s")

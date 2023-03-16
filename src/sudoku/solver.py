from src.sudoku.board import Board
import src.sudoku.board_printer as printer
import time


def get_board():
    with open("../../board/44.txt", "r") as board_input:
        lines = board_input.read().split("\n")

    new_lines = list(map(lambda x: x.split(","), lines))
    return Board(new_lines)


def show_board(board, text):
    print("*******************************************")
    print("************ ", text, " ***************")
    printer.print_board(board)
    print("*******************************************")


def main():
    board = get_board()

    show_board(board, "Starting Board")
    board.reduce_maybe_numbers()
    show_board(board, "After maybe numbers have been reduced")
    board.set_last_remaining_number()
    show_board(board, "After maybe numbers have been changed to fixed numbers")


if __name__ == '__main__':
    start_time = time.time()
    main()
    stop_time = time.time()
    print(f"It took me {stop_time - start_time}s to solve this problem")

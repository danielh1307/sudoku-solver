def print_board(board):
    cells = board.get_cells()

    num_fixed, num_not_fixed = numbers_of_cells_fixed_not_fixed(cells)

    print("-----------------")
    print(f"Numbers of cells fixed: {num_fixed}")
    print(f"Numbers of cells not fixed: {num_not_fixed}\n")
    for idx, cell in enumerate(cells):
        end_str = '|'
        if (idx + 1) % 3 == 0:
            end_str = '| |'
        if (idx + 1) % 9 == 0:
            end_str = "\n"
        print(cell, end=end_str)
        if (idx + 1) % 27 == 0:
            print("---------------------")

    print()
    # for cell in cells:
    #     if not cell.is_number_fixed():
    #         print(str(cell.pos()) + ": " + str(cell.maybe_numbers()))


def numbers_of_cells_fixed_not_fixed(cells):
    numbers_of_cells_fixed = 0
    numbers_of_cells_not_fixed = 0
    for cell in cells:
        if cell.is_number_fixed():
            numbers_of_cells_fixed += 1
        else:
            numbers_of_cells_not_fixed += 1
    return numbers_of_cells_fixed, numbers_of_cells_not_fixed

from src.sudoku.cell import Cell


class Board:
    """
    An instance of class Board represents a Sudoku board.

    Parameters
    ----------
    numbers : list
        a two-dimensional array. Each value contains a row with 9 digits from 1 to 9
        (or 'x'/'X' if the number is unknown).
    """

    def __init__(self, numbers):
        if not isinstance(numbers, list):
            raise Exception("Cannot create board since no list was given")

        if not len(numbers) == 9:
            raise Exception("Cannot create board since list does not contain 9 elements")

        self._cells = []

        for row_idx, row in enumerate(numbers):
            for col_idx, number in enumerate(row):
                self._cells.append(Cell(number, (row_idx, col_idx)))

    def get_cells(self):
        return self._cells

    def get_row(self, row_idx):
        if row_idx < 0 or row_idx > 9:
            raise Exception("Invalid row index")
        return self._cells[row_idx * 9:row_idx * 9 + 9]

    def get_row_numbers(self, row_idx):
        cells = self.get_row(row_idx)
        return [x.number() for x in cells if x.is_number_fixed()]

    def get_col_numbers(self, col_idx):
        cells = self.get_col(col_idx)
        return [x.number() for x in cells if x.is_number_fixed()]

    def get_block_numbers(self, block_idx):
        cells = self.get_block(block_idx)
        return [x.number() for x in cells if x.is_number_fixed()]

    def get_col(self, col_idx):
        if col_idx < 0 or col_idx > 9:
            raise Exception("Invalid column index")
        return self._cells[col_idx::9]

    def get_block(self, block_idx):
        # TODO: there might be a more elegant way to solve this
        if block_idx < 0 or block_idx > 9:
            raise Exception("Invalid block index")
        if block_idx < 3:
            start_idx = block_idx * 3
        elif block_idx < 6:
            start_idx = 3 * 9 + (block_idx % 3) * 3
        else:
            start_idx = 6 * 9 + (block_idx % 3) * 3

        return self._cells[start_idx:start_idx + 3] \
               + self._cells[start_idx + 9:start_idx + 12] \
               + self._cells[start_idx + 18:start_idx + 21]

    def reduce_maybe_numbers(self):
        """This method reduces the maybe numbers for every cell."""
        repeat = True
        while repeat:
            # it might happen that the reduction of a maybe number leads to a new fixed number
            # if this happens, we repeat the whole process until there are no new fixed numbers any longer
            repeat = False
            for cell in self._cells:
                repeat = repeat or cell.reduce_maybe_numbers(self.get_row_numbers(cell.get_row_idx()))
                repeat = repeat or cell.reduce_maybe_numbers(self.get_col_numbers(cell.get_col_idx()))
                repeat = repeat or cell.reduce_maybe_numbers(self.get_block_numbers(cell.get_block_idx()))
            self.validate()

    def set_last_remaining_number(self):
        """This method takes the maybe numbers from every cell. If in the according row, column or block there is
        no other cell with that maybe number, the maybe number is the new fixed number. This only works if the method
        reduce_maybe_numbers() has been called previously."""
        for cell in self._cells:
            if cell.is_number_fixed():
                continue
            self.__change_maybe_number_to_fixed(cell, self.get_row(cell.get_row_idx()))
            if cell.is_number_fixed():
                continue
            self.__change_maybe_number_to_fixed(cell, self.get_col(cell.get_col_idx()))
            if cell.is_number_fixed():
                continue
            self.__change_maybe_number_to_fixed(cell, self.get_block(cell.get_block_idx()))

    def validate(self):
        for i in range(0, 9):
            if not self.no_doubles(self.get_row_numbers(i)) \
                    or not self.no_doubles(self.get_col_numbers(i)) \
                    or not self.no_doubles(self.get_block_numbers(i)):
                raise Exception("Board is not valid any more")

    def set_fixed_value_of_cell(self, cell, number):
        cell.new_fixed_number(number)
        self.validate()
        # since we have created a new fixed number, we start reducing all maybe numbers again
        self.reduce_maybe_numbers()

    def get_cell(self, pos):
        for cell in self._cells:
            if cell.pos() == pos:
                return cell

    ########################################################
    # Static methods
    ########################################################

    @staticmethod
    def no_doubles(numbers):
        return len(numbers) == len(set(numbers))

    ########################################################
    # Internal methods
    ########################################################

    def __change_maybe_number_to_fixed(self, cell, all_other_cells):
        other_maybe_numbers = []
        for other_cell in all_other_cells:
            if cell == other_cell or other_cell.is_number_fixed():
                continue
            other_maybe_numbers += other_cell.maybe_numbers()
        for maybe_number in cell.maybe_numbers():
            if maybe_number not in other_maybe_numbers:
                self.set_fixed_value_of_cell(cell, maybe_number)

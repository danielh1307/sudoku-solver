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

    def get_row(self, row_idx) -> list:
        """
        Parameters
        ----------
        row_idx
            int between 0 and 8, indicating the index of the row from 0 (upper row) to 8.

        Returns
        -------
        list
            The list of cells of the row.

        Raises
        ------
        Exception
            If the given row_idx is not between 0 and 8 (inclusive), an Exception is raised.
        """
        if row_idx < 0 or row_idx > 9:
            raise Exception("Invalid row index")
        return self[row_idx * 9:row_idx * 9 + 9]

    def get_col(self, col_idx) -> list:
        """
        Parameters
        ----------
        col_idx
            int between 0 and 8, indicating the index of the row column 0 (most left) to 8.

        Returns
        -------
        list
            The list of cells of the column.

        Raises
        ------
        Exception
            If the given col_idx is not between 0 and 8 (inclusive), an Exception is raised.
        """
        if col_idx < 0 or col_idx > 9:
            raise Exception("Invalid column index")
        return self[col_idx::9]

    def get_block(self, block_idx) -> list:
        """
        Parameters
        ----------
        block_idx
            int between 0 and 8, indicating the index of the block from 0 (upper left) to 8 (bottom right).

        Returns
        -------
        list
            The list of cells of the block.

        Raises
        ------
        Exception
            If the given col_idx is not between 0 and 8 (inclusive), an Exception is raised.
        """
        # TODO: there might be a more elegant way to solve this
        if block_idx < 0 or block_idx > 9:
            raise Exception("Invalid block index")
        if block_idx < 3:
            start_idx = block_idx * 3
        elif block_idx < 6:
            start_idx = 3 * 9 + (block_idx % 3) * 3
        else:
            start_idx = 6 * 9 + (block_idx % 3) * 3

        return self[start_idx:start_idx + 3] \
               + self[start_idx + 9:start_idx + 12] \
               + self[start_idx + 18:start_idx + 21]

    def get_row_numbers(self, row_idx, with_maybe=False) -> list:
        """
        Parameters
        ----------
        row_idx
            int between 0 and 8, indicating the index of the row from 0 (upper row) to 8.
        with_maybe
            if set to True, the "maybe numbers" are also returned, these are numbers which we are not sure if
            they are correct in that cell.

        Returns
        -------
        list
            The list of numbers in the cells of the row, including "maybe numbers" if with_maybe is set to True.

        Raises
        ------
        Exception
            If the given row_idx is not between 0 and 8 (inclusive), an Exception is raised.
        """
        cells = self.get_row(row_idx)
        if with_maybe:
            return [x.number_or_maybe_number() for x in cells if x.is_number_fixed_or_maybe_number_set()]
        return [x.number() for x in cells if x.is_number_fixed()]

    def get_col_numbers(self, col_idx, with_maybe=False) -> list:
        """
        Parameters
        ----------
        col_idx
            int between 0 and 8, indicating the index of the column from 0 (most left) to 8.
        with_maybe
            if set to True, the "maybe numbers" are also returned, these are numbers which we are not sure if
            they are correct in that cell.

        Returns
        -------
        list
            The list of numbers in the cells of the column, including "maybe numbers" if with_maybe is set to True.

        Raises
        ------
        Exception
            If the given row_idx is not between 0 and 8 (inclusive), an Exception is raised.
        """
        cells = self.get_col(col_idx)
        if with_maybe:
            return [x.number_or_maybe_number() for x in cells if x.is_number_fixed_or_maybe_number_set()]
        return [x.number() for x in cells if x.is_number_fixed()]

    def get_block_numbers(self, block_idx, with_maybe=False):
        """
        Parameters
        ----------
        block_idx
            int between 0 and 8, indicating the index of the block from 0 (upper left) to 8 (bottom right).
        with_maybe
            if set to True, the "maybe numbers" are also returned, these are numbers which we are not sure if
            they are correct in that cell.

        Returns
        -------
        list
            The list of numbers in the block of the column, including "maybe numbers" if with_maybe is set to True.

        Raises
        ------
        Exception
            If the given row_idx is not between 0 and 8 (inclusive), an Exception is raised.
        """
        cells = self.get_block(block_idx)
        if with_maybe:
            return [x.number_or_maybe_number() for x in cells if x.is_number_fixed_or_maybe_number_set()]
        return [x.number() for x in cells if x.is_number_fixed()]

    def reduce_maybe_numbers(self):
        """This method reduces the maybe numbers for every cell.
        Reducing "maybe numbers" means, we are removing every number from the list of "maybe numbers" from every cell
        which we are sure is not the correct number (because there is already a fixed number of that value in the
        same row, column or block).

        If during the reduction a new fixed number can be set (because we have removed all except one "maybe number"
        from a cell), we repeat the reduction for all cells. We do this so long until we can't set no new fixed number.
        """
        repeat = True
        while repeat:
            # it might happen that the reduction of a maybe number leads to a new fixed number
            # if this happens, we repeat the whole process until there are no new fixed numbers any longer
            repeat = False
            for cell in self:
                repeat = repeat or cell.reduce_maybe_numbers(self.get_row_numbers(cell.get_row_idx()))
                repeat = repeat or cell.reduce_maybe_numbers(self.get_col_numbers(cell.get_col_idx()))
                repeat = repeat or cell.reduce_maybe_numbers(self.get_block_numbers(cell.get_block_idx()))
            if not self.validate():
                raise Exception("Board is not valid any more")

    def set_last_remaining_number(self):
        """This method takes the maybe numbers from every cell. If in the according row, column or block there is
        no other cell with that maybe number, the maybe number is the new fixed number. This only works if the method
        reduce_maybe_numbers() has been called previously."""

        # TODO: check if we should also repeat this step if a new fixed number is set
        for cell in self:
            if cell.is_number_fixed():
                continue
            self.__change_maybe_number_to_fixed(cell, self.get_row(cell.get_row_idx()))
            if cell.is_number_fixed():
                continue
            self.__change_maybe_number_to_fixed(cell, self.get_col(cell.get_col_idx()))
            if cell.is_number_fixed():
                continue
            self.__change_maybe_number_to_fixed(cell, self.get_block(cell.get_block_idx()))

    def validate(self, with_maybe=False) -> bool:
        """
        Parameters
        ----------
        with_maybe : bool
            If set to True, the board is validated by taking a set "maybe number" (a number which we are not sure
            is the correct number for the cell) into account. If False (default), only the fixed numbers are being
            taken into account.

        Returns
        -------
        bool
            True if the board is valid, that means there are no double numbers in a row, column or block. False
            otherwise. If with_maybe is set to False and False is returned, this means the board is invalid. If
            with_maybe is True and False is returned, it means the "maybe numbers" set in the cells are not correct,
            and we can continue with other "maybe numbers".

        """
        for i in range(0, 9):
            if not self.no_doubles(self.get_row_numbers(i, with_maybe=with_maybe)) \
                    or not self.no_doubles(self.get_col_numbers(i, with_maybe=with_maybe)) \
                    or not self.no_doubles(self.get_block_numbers(i, with_maybe=with_maybe)):
                return False
        return True

    def set_fixed_value_of_cell(self, cell, number) -> None:
        """Sets a fixed number to the given cell."""
        cell.new_fixed_number(number)
        if not self.validate():
            raise Exception("Board is not valid any more")
        # since we have created a new fixed number, we start reducing all maybe numbers again
        self.reduce_maybe_numbers()

    def get_cell(self, pos) -> Cell:
        """
        Parameters
        ----------
        pos : tuple
            A position containing of a row and column index.

        Returns
        -------
        Cell
            the cell at the specified position.
        """
        for cell in self:
            if cell.pos() == pos:
                return cell

    def solve_with_backtrack(self):
        """Tries to solve the board by using the 'backtrack' algorithm, that means trying every remaining 'maybe
        numbers' until a valid board is found.

        Raises
        ------
        Exception
            If the board cannot be solved with this algorithm, an Exception is raised.
        """
        solved = self.__backtrack()
        if not solved:
            raise Exception("Could not solve the board with backtracking")
        else:
            for cell in self:
                if not cell.is_number_fixed():
                    cell.new_fixed_number(cell.maybe_number())
        self.validate()

    def __backtrack(self) -> bool:
        """
        This is the backtracking algorithm.
        It works as follows:
        - from the given board, it takes the first cell which has no fixed number. It sets the first maybe_number
            of that cell and afterwards checks if the board is still valid (with maybe).
        - if the board is still valid, it passes the board to the next recursion of that method. By doing this, each
            function always gets a valid board as input.
        - if the board is not valid with the maybe number, the function takes the next maybe number and repeats the
            step. If there are no more maybe numbers and the board is still not valid, it returns False.

        Returns
        -------
        bool
            True if the board is still valid with the next maybe number set. False otherwise.
        """

        first_cell_without_number = None
        for cell in self:
            if not cell.is_number_fixed_or_maybe_number_set():
                first_cell_without_number = cell
                break

        if not first_cell_without_number:
            # great, there are no "empty" cells any longer, and we have a valid board, so this is the solution
            return True

        while first_cell_without_number.new_maybe_number():
            if not self.validate(with_maybe=True):
                # board is not valid, so we try the next number
                continue
            # board is still valid, so we pass the board one recursion down

            if self.__backtrack():
                # tried all variations with this maybe number, trying next one ...
                return True

        # we tried all maybe numbers with this board and that cell, no solution have been found
        return False

    def is_solved(self) -> bool:
        """
        Returns
        -------
        bool
            True if the board is solved, that means we have only fixed numbers in a valid board. False otherwise.
        """
        for cell in self:
            if not cell.is_number_fixed():
                return False
        if not self.validate():
            return False
        return True

    ########################################################
    # Static methods
    ########################################################

    @staticmethod
    def no_doubles(numbers: list) -> bool:
        """
        Returns
        -------
        bool
            True if the given list does not contain a double number, False otherwise.
        """
        return len(numbers) == len(set(numbers))

    ########################################################
    # Internal methods
    ########################################################

    def __change_maybe_number_to_fixed(self, cell, all_other_cells):
        """If the given cell contains a 'maybe number' which none of the other given cells contain, this 'maybe number'
        is set to the new fixed number of that cell."""
        other_maybe_numbers = []
        for other_cell in all_other_cells:
            if cell == other_cell or other_cell.is_number_fixed():
                continue
            other_maybe_numbers += other_cell.maybe_numbers()
        for maybe_number in cell.maybe_numbers():
            if maybe_number not in other_maybe_numbers:
                self.set_fixed_value_of_cell(cell, maybe_number)

    #########################################################
    # Built-in methods
    #########################################################

    def __len__(self):
        return len(self._cells)

    def __getitem__(self,position):
        return self._cells[position]

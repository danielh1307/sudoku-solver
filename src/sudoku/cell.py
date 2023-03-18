class Cell:
    """This class represents a single cell on a Sudoku board

    Parameters
    ----------
    number : str
        the number must either represent a value between 1 and 9 or - if the number is yet unknown - a 'x' or 'X'.
    pos : tuple
        a tuple containing two values, the x- and y-coordinate of the cell.
    """

    def __init__(self, number, pos):
        if not isinstance(number, str):
            raise Exception("Cannot create cell, given input is not a String")

        if not str(number).isdigit() and not number.lower() == 'x':
            raise Exception("Cannot create cell, given input is neither a digit nor 'x'/'X'")

        if str(number).isdigit() and not int(number) in range(1, 10):
            raise Exception("Cannot create cell, given input is not an integer value between 1 and 10")

        if str(number).isdigit():
            self._number = int(number)
            self._maybe_number = None
            self._maybe_numbers = []
        else:
            self._number = None
            self._maybe_number = None
            self._maybe_numbers = list(range(1, 10))

        self._pos = pos  # TODO: validate value of pos

    def number(self) -> int:
        """
        Returns
        -------
        int
            an integer representing the fixed number of that cell. If the number is unknown yet, None is returned.
        """
        return self._number

    def maybe_number(self) -> int:
        """
        Returns
        -------
        int
            the current "maybe number" if there is one, otherwise None is returned. The "maybe number" is a number
            which we try for the cell, but we are not sure yet if it is the correct number.
        """
        return self._maybe_number

    def number_or_maybe_number(self) -> int:
        """
        Returns
        -------
        int
            if the number is set, it returns the number. If a "maybe number" is set (a number we try for the cell
            without being sure it is the correct number), we return the "maybe number".

        Raises
        ------
        Exception
            if neither number nor "maybe number" are set, an Exception is raised.
        """
        if self.number():
            return self.number()
        elif self.maybe_number():
            return self.maybe_number()
        else:
            raise Exception("There is neither a fixed nor a maybe number")

    def maybe_numbers(self) -> list:
        """
        Returns
        -------
        list
            if the number is yet unknown, the list contains the possible numbers of that cell. If the number is
            already known, an empty list is returned.
        """
        return self._maybe_numbers

    def pos(self) -> tuple:
        """
        Returns
        -------
        tuple
            the position of the cell in the board, starting from (0, 0) in the upper left corner  to (9, 9) in
            the bottom right corner.
        """
        return self._pos

    def is_number_fixed(self) -> bool:
        """
        Returns
        -------
        bool
            True if we already know the number of that cell for sure, otherwise False.
        """
        return self._number is not None

    def is_number_fixed_or_maybe_number_set(self) -> bool:
        """
        Returns
        -------
        bool
            True if we already know the number of that cell for sure OR if we have set a "maybe number", that is
            a number we are trying for that cell without being sure it is the correct number.
        """
        return self.is_number_fixed() or self._maybe_number is not None

    def reduce_maybe_numbers(self, fixed_numbers) -> bool:
        """
        This function reduces the "maybe numbers". Every number which is contained in fixed_number is removed from
        the "maybe numbers".

        Parameters
        ----------
        fixed_numbers : list
            list of numbers which are fixed; the maybe numbers are reduced by these numbers. If just one maybe number
            remains, this is the new fixed number for this cell.

        Returns
        -------
        bool
            True if the (fixed) number of a cell has been set successfully, False otherwise.

        Raises
        ------
        Exception
            if after the reduction of the maybe numbers, no maybe numbers remain, an Exception is raised. This
            happens only if we are operating on an invalid Sudoku board.
        """
        if self.is_number_fixed():
            return False
        self._maybe_numbers = list(set(self._maybe_numbers) - set(fixed_numbers))
        if len(self._maybe_numbers) == 0:
            raise Exception("No maybe numbers remain, check this")
        elif len(self._maybe_numbers) == 1:
            # we have found a new fixed number
            self.new_fixed_number(self._maybe_numbers[0])
            return True
        # if we make changes in the maybe_numbers list, we also reset the maybe_number
        self._maybe_numbers.sort()
        self._maybe_number = None
        return False

    def new_fixed_number(self, number) -> None:
        """Sets a new fixed number, the maybe numbers are being reset."""
        self._number = number
        self._maybe_number = None
        self._maybe_numbers.clear()

    def new_maybe_number(self) -> bool:
        """Sets a new maybe number. This is a number we are trying for this cell, without being sure it is the
            correct number.

        If there is no maybe number yet, the first number from maybe_numbers() is taken.
        If there already is a maybe_number, the next number from maybe_numbers() is taken.
        If there are is no available number in maybe_numbers any longer, maybe_number is set to None.

        Returns
        -------
        bool
            True if a new maybe number was set, False otherwise.

        Raises
        ------
        Exception
            if the number of the cell is already fixed, an Exception is raised when calling this method.
        """
        if self.is_number_fixed():
            raise Exception("Do not call this method if the number is already fixed")

        if not self._maybe_number:
            self._maybe_number = self._maybe_numbers[0]
            return True

        cur_maybe_number_idx = self._maybe_numbers.index(self._maybe_number)
        if cur_maybe_number_idx == len(self._maybe_numbers) - 1:
            self._maybe_number = None
            return False
        else:
            self._maybe_number = self._maybe_numbers[cur_maybe_number_idx + 1]
            return True

    def get_row_idx(self) -> int:
        """
        Returns
        -------
        int
            the row index of that cell, starting from 0 in the first row (upper row) to 8.
        """
        return self._pos[0]

    def get_col_idx(self) -> int:
        """
        Returns
        -------
        int
            the column index of that cell, starting from 0 in the first column (most left) to 8.
        """
        return self._pos[1]

    def get_block_idx(self) -> int:
        """
        Returns
        -------
        int
            the block index of that cell, starting from 0 in the first block (upper left) to 8 (bottom right).
        """
        if self.get_row_idx() < 3:
            return self.get_col_idx() // 3
        elif self.get_row_idx() < 6:
            return 3 + self.get_col_idx() // 3
        else:
            return 6 + self.get_col_idx() // 3

    def __str__(self):
        """Prints the fixed number of that cell or 'X' if the number is not yet known."""
        if self._number:
            return str(self._number)
        else:
            return 'X'

    def __eq__(self, other):
        """If two cells have the same pos (position), they are considered to be equal."""
        if not isinstance(other, Cell):
            return False
        return self._pos[0] == other.pos()[0] and self._pos[1] == other.pos()[1]

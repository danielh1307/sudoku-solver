class Cell:
    """This class represents a single cell on a Sudoku board

    Parameters
    ----------
    number : str
        the number must either represent a value between 1 and 9 or - if the number is yet unknown - a 'x' or 'X'
    pos : tuple
        a tuple containing two values, the x- and y-coordinate of the cell
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

    def number(self):
        """
        Returns
        -------
        int
            an integer representing the fixed number of that cell. If the number is unknown yet, None is returned.
        """
        return self._number

    def maybe_number(self):
        """
        Returns
        -------
        int
            the current "maybe number" if there is one, otherwise None is returned.
        """
        return self._maybe_number

    def number_or_maybe_number(self):
        if self.number():
            return self.number()
        elif self.maybe_number():
            return self.maybe_number()
        else:
            raise Exception("There is neither a fixed nor a maybe number")

    def maybe_numbers(self):
        """
        Returns
        -------
        list
            if the number is yet unknown, the array contains the possible numbers of that cell. If the number is
            already known, an empty array is returned.
        """
        return self._maybe_numbers

    def pos(self):
        """
        Returns
        -------
        tuple
            the position of the cell in the board, starting from (0, 0) to (9, 9)
        """
        return self._pos

    def is_number_fixed(self):
        return self._number is not None

    def is_number_fixed_or_maybe_number_set(self):
        return self.is_number_fixed() or self._maybe_number is not None

    def reduce_maybe_numbers(self, fixed_numbers):
        """
        This function reduces the "maybe numbers". Every number which is contained in fixed_number is removed from
        the "maybe numbers".

        Parameters
        ----------
        fixed_numbers : list
            list of numbers which are fixed, the maybe numbers are reduced by these numbers. If just one maybe number
            remains, this is the new fixed number for this cell.

        Returns
        -------
        bool
            true if the (fixed) number of a cell has changed, false otherwise
        """
        if self.is_number_fixed():
            return
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

    def new_fixed_number(self, number):
        """Sets a new fixed number, the maybe numbers are being reset."""
        self._number = number
        self._maybe_number = None
        self._maybe_numbers.clear()

    def new_maybe_number(self):
        """Sets a new maybe number.
        If there is no maybe number yet, the first number from maybe_numbers() is taken.
        If there already is a maybe_number, the next number from maybe_numbers() is taken.
        If there are is no available number in maybe_numbers any longer, maybe_number is set to None.

        Returns
        -------
        bool
            True if a new maybe number was set, False otherwise.
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

    def get_row_idx(self):
        return self._pos[0]

    def get_col_idx(self):
        return self._pos[1]

    def get_block_idx(self):
        if self.get_row_idx() < 3:
            return self.get_col_idx() // 3
        elif self.get_row_idx() < 6:
            return 3 + self.get_col_idx() // 3
        else:
            return 6 + self.get_col_idx() // 3

    def __str__(self):
        if self._number:
            return str(self._number)
        else:
            return 'X'

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        return self._pos[0] == other.pos()[0] and self._pos[1] == other.pos()[1]

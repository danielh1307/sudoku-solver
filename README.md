# sudoku-solver
A Python program which solves Sudokus

The program follows an object oriented approach. It consists of the following classes:

Cell - a Cell represents a single cell in a Sudoku board. It can have a fixed number (then we know the correct number in that cell for sure) and a list of
"maybe numbers" (numbers which are possible in that cell). It also has a single field "maybe number", which we use during the backtracking algorithm when
solving the board.

Board - a Board represents the whole board and consists of 81 objects of class Cell.

board_printer.py - this is not an own class but a helper script which outputs a board to the console.

solver.py - this is the actual solver. The board is solved in its main() method. See comments there for more information how the program actually works.

The board directory contains the "input boards". These are text files which consists of 9 rows and 9 colums, each separated by commas. If the number in 
a cell is not known, the file contains an "X".

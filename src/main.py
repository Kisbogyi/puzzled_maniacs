from sudoku import Sudoku
from solver import solve, SudokuType


def main():
    sudoku = Sudoku()
    # sudoku.set_field(0,1, 9)
    print(sudoku)
    solved_sudoku = solve(sudoku, SudokuType.Windoku)
    print(solved_sudoku)


if __name__ == "__main__":
    main()

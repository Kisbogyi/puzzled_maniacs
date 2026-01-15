from sudoku import Sudoku
from solver import SudokuSolver, SudokuType


def main():
    sudoku = Sudoku()
    # sudoku.set_field(0,1, 9)
    print(sudoku)
    ssolver = SudokuSolver()
    solved_sudoku = ssolver.solve(sudoku, SudokuType.Windoku)
    print(solved_sudoku)


if __name__ == "__main__":
    main()

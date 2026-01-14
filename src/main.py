from our_sudoku import OurSudoku
from our_solver import solve


def main():
    sudoku = OurSudoku()
    sudoku.set_field(0,1, 9)
    print(sudoku)
    solved_sudoku = solve(sudoku)
    print(solved_sudoku)


if __name__ == "__main__":
    main()

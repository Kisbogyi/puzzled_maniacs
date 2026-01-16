from sudoku import Sudoku
from solver import SudokuSolver, SudokuType
from generator import Generator, Difficulty, count_clues

def main():
    sudoku = Sudoku()
    # sudoku.set_field(0,1, 9)
    print(sudoku)
    ssolver = SudokuSolver(SudokuType.Windoku)
    solved_sudoku = ssolver.solve(sudoku)
    print(solved_sudoku)
    
    sudoku_gen = Generator(ssolver, rng=None)
    
    difficulty = Difficulty.MEDIUM
    symmetry = None  # "diagonal", "horizontal", "vertical", None
    final, target_value = sudoku_gen.generate(solved_sudoku, difficulty=difficulty, symmetry=symmetry)
    print("Final puzzle:")
    print(final)
    print("Target clues:", target_value)
    print("Final clues:", count_clues(final.board) if final else None)


if __name__ == "__main__":
    main()

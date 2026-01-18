from random import Random
from sudoku import Sudoku
from solver import SudokuSolver, SudokuType
from generator import Generator, Difficulty, count_clues
from utils import write_csv_sudoku

def main():
    ### DEFINE TYPE, DIFFICULTY AND SYMMETRY HERE
    sudoku_type = SudokuType.Windoku
    ssolver = SudokuSolver(sudoku_type)
    difficulty = Difficulty.MEDIUM
    symmetry = None  # "diagonal", "horizontal", "vertical", None

    sudoku = Sudoku()
    # sudoku.set_field(0,1, 9)
    print(sudoku)
    solved_sudoku = ssolver.solve(sudoku)
    print(solved_sudoku)
    
    sudoku_gen = Generator(ssolver, rng=None)
    
    final, target_value = sudoku_gen.generate(solved_sudoku, difficulty=difficulty, symmetry=symmetry)
    print("Final puzzle:")
    print(final)
    print(f"Type: {sudoku_type}")
    print(f"Difficulty: {difficulty}")
    print("Target clues:", target_value)
    print("Final clues:", count_clues(final.board) if final else None)
    sudokus = []
    if final is not None:
        sudokus.append(final.csv_format())

    for _ in range(3):
        s2 = Sudoku()
        ss2 = ssolver.solve(s2)
        sg2 = Generator(ssolver, rng=None)
        f2, t2 = sg2.generate(ss2, difficulty=difficulty, symmetry=symmetry)
        
        if f2 is not None:
            sudokus.append(f2.csv_format())

    write_csv_sudoku("docs/sudoku.csv", sudokus, sudoku_type, difficulty)    

if __name__ == "__main__":
    main()

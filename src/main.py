#from random import Random
import random
from sudoku import Sudoku
from solver import SudokuSolver, SudokuType
from generator import Generator, Difficulty, count_clues
from utils import write_csv_sudoku
from argparse import ArgumentParser

parser = ArgumentParser(
        description='Script for generating solvable sudokus and sudoku variants.'
        )

parser.add_argument('sudoku_type', type=str, help='type of sudoku, options are Classic, AntiKnight, Windoku, Nonconsecutive, and Center')
parser.add_argument('difficulty', type=str, help='sudoku difficulty, can be easy, medium, hard, or expert')
parser.add_argument('-s', '--symmetry', type=str, help='options are diagonal, horisontal, and vertical')

sudoku_types = {
        'classic': SudokuType.Classic,
        'antiknight': SudokuType.AntiKnight,
        'windoku': SudokuType.Windoku,
        'nonconsecutive': SudokuType.Nonconsecutive,
        'center': SudokuType.Center
        }

difficulties = {
        'easy': Difficulty.EASY,
        'medium': Difficulty.MEDIUM,
        'hard': Difficulty.HARD,
        'expert': Difficulty.EXPERT
        }

def main():
    args = parser.parse_args()

    sudoku_type = sudoku_types[args.sudoku_type.lower()]
    ssolver = SudokuSolver(sudoku_type)
    difficulty = difficulties[args.difficulty.lower()]
    symmetry = args.symmetry.lower() if args.symmetry else None

    '''
    ### DEFINE TYPE, DIFFICULTY AND SYMMETRY HERE
    ## Classic, AntiKnight, Windoku, Nonconsecutive, Center
    sudoku_type = SudokuType.Classic
    ssolver = SudokuSolver(sudoku_type)
    difficulty = Difficulty.MEDIUM
    symmetry = None  # "diagonal", "horizontal", "vertical", None
    '''

    sudoku = Sudoku()
    ### set a random field of a sudoku to a random value
    ### to get more varied generation
    row = random.randint(0,8)
    col = random.randint(0,8)
    value = random.randint(1,9)
    sudoku.set_field(row, col, value)
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
    with open("docs/generated_sudokus.txt", "a") as f:
        f.write(f"{sudoku_type}:{difficulty}\n{solved_sudoku}\n\n")


if __name__ == "__main__":
    main()

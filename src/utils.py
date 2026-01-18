from generator import Difficulty
from solver import SudokuType

def write_csv_sudoku(file_name: str, sudokus: list[str], sudoku_type: SudokuType, difficulty: Difficulty):
    with open(file_name, 'w') as out:
        for sudoku in sudokus:
            out.write(",".join(sudoku)+"\n")
    with open(f"{file_name}.typefile", 'w') as typefile:
        typefile.write(str(sudoku_type))
        typefile.write(str(difficulty))

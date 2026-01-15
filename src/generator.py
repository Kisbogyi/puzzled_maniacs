from z3 import Solver, Or, sat
from sudoku import Sudoku
from solver import SudokuSolver, SudokuType
from enum import Enum
import random

# SLOP WARNING
class Difficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    EXPERT = "EXPERT"

DIFFICULTY_CLUE_RANGES = {
    Difficulty.EASY:   (38, 49),
    Difficulty.MEDIUM: (32, 37),
    Difficulty.HARD:   (26, 31),
    Difficulty.EXPERT: (17, 25)
}

def count_clues(board):
    return sum(1 for r in range(9) for c in range(9) if board[r][c] is not None)

class Generator:
    def __init__(self, sudoku):
        self.ssudoku = SudokuSolver().solve(sudoku, SudokuType.Classic)

    def _build_solver(self, board, stype):
        solver = SudokuSolver()
        solver.known_value_constraints(Sudoku(board))
        solver.apply_type_constraints(stype)
        return solver

    def solves_uniquely(self, board, stype=SudokuType.Classic):
        s1 = self._build_solver(board, stype)
        if s1.s.check() != sat:
            return False

        m1 = s1.s.model()
        diff = [s1.matrix[r][c] != m1.eval(s1.matrix[r][c]).as_long() for r in range(9) for c in range(9)]

        s2 = Solver()
        s2.add(s1.s.assertions())
        s2.add(Or(diff))
        return s2.check() != sat

    def remove_a_cell(self, sudoku, stype=SudokuType.Classic):
        filled_cells = sudoku.get_nonempty_cells()
        random.shuffle(filled_cells)

        for (r, c) in filled_cells:
            new_board = [row[:] for row in sudoku.board]
            new_board[r][c] = None

            if self.solves_uniquely(new_board, stype):
                sudoku.board = new_board
                return sudoku
        return None

    def removal_generator(self, sudoku, target, stype=SudokuType.Classic, symmetry=None, random_seed=None):
        if random_seed is not None:
            random.seed(random_seed)

        work = Sudoku(board=[row[:] for row in sudoku.board])
        solved = SudokuSolver().solve(work, stype)
        if solved is not None:
            work = Sudoku(board=[row[:] for row in solved.board])

        def symmetric_pairs(cells):
            if symmetry is None:
                for rc in cells:
                    yield [rc]
                return

            seen = set()
            for (r, c) in cells:
                if (r, c) in seen:
                    continue
                group = {(r, c)}
                if symmetry == "diagonal":
                    group.update([(c, r), (8 - r, 8 - c)])
                elif symmetry == "horizontal":
                    group.add((8 - r, c))
                elif symmetry == "vertical":
                    group.add((r, 8 - c))

                group = {(gr, gc) for (gr, gc) in group if 0 <= gr < 9 and 0 <= gc < 9}
                for g in group:
                    seen.add(g)
                yield sorted(group)

        while True:
            current_clues = count_clues(work.board)
            if current_clues <= target:
                break

            filled = work.get_nonempty_cells()
            random.shuffle(filled)

            removed_this_round = False
            for to_remove in symmetric_pairs(filled):
                if any(work.board[r][c] is None for (r, c) in to_remove):
                    continue
                if current_clues - len(to_remove) < target:
                    continue

                trial = [row[:] for row in work.board]
                for (r, c) in to_remove:
                    trial[r][c] = None

                if self.solves_uniquely(trial, stype):
                    work.board = trial
                    removed_this_round = True
                    yield Sudoku(board=[row[:] for row in work.board])
                    break

            if not removed_this_round:
                break

        return work

if __name__ == "__main__":
    initial_board = [
        [9,8,7,4,3,5,6,1,2],
        [2,5,1,7,6,9,8,3,4],
        [6,4,3,1,8,2,5,7,9],
        [7,3,9,8,2,1,4,5,6],
        [8,6,5,9,4,3,7,2,1],
        [4,1,2,6,5,7,3,9,8],
        [1,9,4,5,7,8,2,6,3],
        [5,2,8,3,9,6,1,4,7],
        [3,7,6,2,1,4,9,8,5],
    ]

    base = Sudoku(initial_board)
    gen = Generator(base)

    start, end = DIFFICULTY_CLUE_RANGES[Difficulty.MEDIUM]
    target_value = random.randint(start, end)
    final = None
    for puzzle in gen.removal_generator(base, target=target_value, stype=SudokuType.Classic, random_seed=42):
        print(puzzle)
        print("Clues:", count_clues(puzzle.board), "Empty ratio:", puzzle.get_difficulty_rating())
        final = puzzle

    print("Final puzzle:")
    print(final)
    print("Final clues:", count_clues(final.board))
# SLOP END

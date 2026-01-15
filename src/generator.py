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
    Difficulty.EXPERT: (9, 25)
}

def count_clues(board):
    return sum(1 for r in range(9) for c in range(9) if board[r][c] is not None)

class Generator:
    def __init__(self, solver: SudokuSolver, rng=None):
        self.base_solver = solver
        self.stype = solver.type
        self.rng = rng or random.Random()

    # Rebuild a fresh solver with same constraints & type
    def _build_solver(self, board):
        ss = self.base_solver.clone_blank()
        ss.known_value_constraints(Sudoku(board))
        ss.apply_type_constraints()
        return ss

    def solves_uniquely(self, board):
        s1 = self._build_solver(board)
        if s1.s.check() != sat:
            return False

        m1 = s1.s.model()
        diff = [
            s1.matrix[r][c] != m1.eval(s1.matrix[r][c]).as_long()
            for r in range(9)
            for c in range(9)
        ]

        s2 = Solver()
        s2.add(s1.s.assertions())
        s2.add(Or(diff))

        return s2.check() != sat

    def removal_generator(self, sudoku, target, symmetry=None):
        rng = self.rng
        stype = self.stype

        work = Sudoku(board=[row[:] for row in sudoku.board])
        solved = self.base_solver.clone_blank().solve(work)
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

                seen.update(group)
                yield sorted(group)

        while True:
            current = count_clues(work.board)
            if current <= target:
                break

            filled = work.get_nonempty_cells()
            rng.shuffle(filled)

            removed_any = False

            for group in symmetric_pairs(filled):
                if any(work.board[r][c] is None for (r, c) in group):
                    continue
                if current - len(group) < target:
                    continue

                trial = [row[:] for row in work.board]
                for (r, c) in group:
                    trial[r][c] = None

                if self.solves_uniquely(trial):
                    work.board = trial
                    removed_any = True
                    yield Sudoku(board=[row[:] for row in work.board])
                    break

            if not removed_any:
                break

        return work
    
    def generate(self, base: Sudoku, difficulty: Difficulty, symmetry=None):
        start, end = DIFFICULTY_CLUE_RANGES[difficulty]
        target_value = self.rng.randint(start, end)
        final = None
        # Start from 'base' and remove down to the sampled target_value
        for puzzle in self.removal_generator(base, target=target_value, symmetry=symmetry):
            final = puzzle
        return final, target_value
# SLOP END

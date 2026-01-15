from z3 import ArithRef, Solver, Int, Distinct, And
from sudoku import Sudoku
from enum import Enum

class SudokuType(Enum):
    Classic = 1
    AntiKnight = 2
    Windoku = 3
    Nonconsecutive = 4
    Center = 5

class SudokuSolver:
    ## added stype here as argument so that it wouldn't have to be passed around
    def __init__(self, stype: SudokuType = SudokuType.Classic):
        self.type = stype

        ## this is a Z3 solver, not to be confused with a sudoku solver!
        self.s = Solver()
        self.matrix: list[list[ArithRef]] = [
            [Int(f"{x}{y}") for x in range(9)] for y in range(9)
        ]
        self.default_constraints()
        self.apply_type_constraints()
    
    # SLOP WARNING
    ## Return a new solver with the same SudokuType but fresh constraints
    def clone_blank(self) -> "SudokuSolver":
        return SudokuSolver(self.type)
    # END SLOP

    def default_constraints(self) -> None:
        # distinct numbers in every row from 1 to 9
        for i in range(9):
            self.s.add(Distinct(self.matrix[i]))
            for j in range(9):
                self.s.add(And(1 <= self.matrix[i][j], self.matrix[i][j] <= 9))

        # distinct numbers in every column
        # all numbers are from 1 to 9 so don't need that constraint again
        for row in range(9):
            column = [self.matrix[column][row] for column in range(9)]
            self.s.add(Distinct(column))

        # Distinct values in every 3 by 3 box
        for i in range(3):
            for j in range(3):
                self.s.add(
                    Distinct(
                        [self.matrix[i * 3 + x][j * 3 + y] for x in range(3) for y in range(3)]
                    )
                )

    def known_value_constraints(self, sudoku: Sudoku) -> None:
        # copy all values from board to the solver's possible values
        for x, row in enumerate(sudoku.board):
            for y, field in enumerate(row):
                if field is not None:
                    # don't use self.matrix[x][y] = field it will be bad if you try to
                    # query results
                    self.s.add(self.matrix[x][y] == field)


    def center_constraints(self) -> None:
        self.s.add(Distinct([self.matrix[i * 3 + 1][j * 3 + 1] for i in range(3) for j in range(3)]))


    def non_consecutive_constraints(self) -> None:
        for x in range(8):
            for y in range(8):
                # Two horizontally adjacent number cannot be consecutive
                self.s.add(self.matrix[x][y] != self.matrix[x][y + 1] + 1)
                self.s.add(self.matrix[x][y] != self.matrix[x][y + 1] - 1)
                # Two vertically adjacent number cannot be consecutive
                self.s.add(self.matrix[x][y] != self.matrix[x + 1][y] + 1)
                self.s.add(self.matrix[x][y] != self.matrix[x + 1][y] - 1)


    def gen_knight_jumps(self, x: int, y: int) -> list[tuple[int, int]]:
        offsets = ((1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, 2))
        output = []
        for offset in offsets:
            x_offset, y_offset = offset
            new_x = x + x_offset
            new_y = y + y_offset
            if new_x < 9 and new_x >= 0 and new_y < 9 and new_y >= 0:
                output.append((new_x, new_y))
        return output


    def knight_constraints(self) -> None:
        for x in range(9):
            for y in range(9):
                possible_jumps = self.gen_knight_jumps(x, y)
                [self.s.add(self.matrix[x][y] != self.matrix[new_x][new_y]) for new_x, new_y in possible_jumps]

    def windoku_constraints(self) -> None:
        for i in range(2):
            for j in range(2):
                self.s.add(Distinct([self.matrix[i*4+x+1][j*4+y+1] for x in range(3) for y in range(3)]))

    # SLOP WARNING
    # Helper so we can reuse type constraints outside solve()
    def apply_type_constraints(self) -> None:
        match self.type:
            case SudokuType.Center:
                self.center_constraints()
            case SudokuType.Nonconsecutive:
                self.non_consecutive_constraints()
            case SudokuType.AntiKnight:
                self.knight_constraints()
            case SudokuType.Windoku:
                self.windoku_constraints()
            case _:
                pass
    # SLOP END

    def solve(self, sudoku: Sudoku):
        """Solve the sudoku

        The function solves the sudoku with z3-solver, then returns a new Sudoku
            object as the solved sudoku

        Args:
            sudoku: The sudoku that is needs to be solved

        Returns:
            A solved sudoku
        """
        self.known_value_constraints(sudoku)
        self.apply_type_constraints()

        # TODO: apply the check weather it is solvable
        print("="*10)
        print(self.s.check())
        print("="*10)
        model = self.s.model()

        # copy the values of the solved sudoku to the object
        solved_sudoku = Sudoku()
        for x, row in enumerate(self.matrix):
            for y, field in enumerate(row):
                value = model.eval(field).as_long()
                solved_sudoku.set_field(x, y, value)

        return solved_sudoku

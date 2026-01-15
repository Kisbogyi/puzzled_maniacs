from typing import Optional


class Sudoku:
    """Sudoku game class

    Attributes:
        board: a matrix that stores the game state a field is int if it stores a value,
            if the field is empty then it is None
    """
    # I don't use [[None]*9]*9 because it will soft copy the [None]*9 
    # so if something changes it will change in all
    def __init__(self, board: list[list[int | None]] = [[None] * 9 for _ in range(9)]):
        self.board = board

    def set_field(self, x: int, y: int, value: int|None) -> None:
        """ Sets the field with the specific value

        Args:
            x: x coordinate of the field in the matrix (starts with 0)
            y: y coordinate of the field in the matrix (starts with 0)
            value: value that the field shout be ( None if remove the value)
        """
        if x >= len(self.board) or x < 0:
            raise ValueError(
                f"x: {x} is too large or small and not in board (y: {y}, value: {value})"
            )
        if y >= len(self.board[x]) or x < 0:
            raise ValueError(
                f"y: {y} is too large or small and not in board (x: {x}, value: {value})"
            )
        if value is not None and (value < 1 or value > 9):
            raise ValueError(
                f"Value: {value} is too large or too small it should be [1-9]"
            )
        self.board[x][y] = value
    
    def get_nonempty_cells(self):
        filled_cells = [(r, c) for r in range(9) for c in range(9)
            if self.board[r][c] is not None]
        return filled_cells

    # Outputs a basic difficulty rating based on the percentage of empty cells
    # Higher = more empty = more difficult
    def get_difficulty_rating(self) -> float:
        nonempty = len(self.get_nonempty_cells())
        empty_ratio = 1.0 - (nonempty / 81.0)
        return round(empty_ratio, 4)


    # Writes a BAD ascii art of the board state
    def __repr__(self) -> str:
        output = ""
        for row_index, row in enumerate(self.board):
            output += "\n"
            for el_index, el in enumerate(row):
                output += (str(el) + " ") if el else ". "
                if (el_index % 3 == 2):
                    output += "  "
            if (row_index % 3 == 2):
                output += "\n"
        return output

class Sudoku:
    """ Sudoku game class
    
    Attributes:
        board: a matrix that stores the game state a field is int if it stores a value,
            if the field is empty then it is None
    """
    # I don't use [[None]*9]*9 because it will soft copy the [None]*9 
    # so if something changes it will change in all
    board: list[list[int | None]] = [[None] * 9 for _ in range(9)]

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

    # Writes a BAD ascii art of the board state
    def __repr__(self) -> str:
        output = ""
        for row_index, row in enumerate(self.board):
            output+= "\n"
            if row_index % 3 == 0:
                output += "-"*21
                output+= "\n"
            output += "-"*21
            output += "\n"
            for column_index, field in enumerate(row):
                if column_index % 3 == 0:
                    output += "|"
                output += str(field) if field is not None else " "
                output += "|"
        output+= "\n"
        output += "-"*21
        output += "\n"
        return output

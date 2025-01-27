from datetime import datetime

class Move:
    time: datetime

    def __init__(self, from_square, to_square):
        if isinstance(from_square, Square):
            self.from_square = from_square
        elif isinstance(to_square, list):
            self.from_square = Square(from_square[0], from_square[1])
        elif isinstance(from_square, str):
            self.from_square = Square(ord(from_square[0]) - 97, int(from_square[1]) - 1)

        if isinstance(to_square, Square):
            self.to_square = to_square
        elif isinstance(to_square, list):
            self.to_square = Square(to_square[0], to_square[1])
        elif isinstance(to_square, str):
            self.to_square = Square(ord(to_square[0]) - 97, int(to_square[1]) - 1)

        self.time = datetime.now()

    staticmethod
    def from_string(string):
        return Move(string[0:2], string[2:4])

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
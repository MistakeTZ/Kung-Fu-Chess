from .move import Move

class Board:
    configuration = None

    def __init__(self, configuration=None):
        if configuration:
            self.configuration = configuration
        else:
            self.configuration = [
                ["r", "n", "b", "q", "k", "b", "n", "r"],
                ["p", "p", "p", "p", "p", "p", "p", "p"],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                ["P", "P", "P", "P", "P", "P", "P", "P"],
                ["R", "N", "B", "Q", "K", "B", "N", "R"]
            ]

    def __str__(self):
        return "\n".join([" ".join(row) for row in self.configuration])

    def is_legal_move(self, move: Move):
        fig = self.configuration[move.from_square.y][move.from_square.x]
        if fig == ".":
            return False
        return True

    def rotated_configuration(self):
        rotated_conf = [rot[::-1] for rot in list(zip(*self.configuration[::-1]))]
        return rotated_conf

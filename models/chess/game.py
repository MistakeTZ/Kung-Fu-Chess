from .board import Board
from .move import Move

class Game:
    board: Board
    moves: list

    def __init__(self, board=None, moves=None):
        self.board = board if board else Board()

        if moves:
            self.moves = moves

    def move(self, move: Move):
        if isinstance(move, str):
            move = Move.from_string(move)

        if not self.board.is_legal_move(move):
            raise Exception("Illegal move")

        self.board.configuration[move.to_square.y][
            move.to_square.x] = self.board.configuration[move.from_square.y][move.from_square.x]
        self.board.configuration[move.from_square.y][move.from_square.x] = '.'
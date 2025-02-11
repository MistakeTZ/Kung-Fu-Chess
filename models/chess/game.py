from .board import Board
from .move import Move
from enum import Enum

class Game:
    board: Board
    moves: list
    first_player: str
    second_player: str
    positions = [{"fig": None, "possible_moves": []}] * 2

    def __init__(self, board=None, first_player=None, second_player=None, moves=None):
        self.board = board if board else Board()
        self.first_player = first_player
        self.second_player = second_player

        if moves:
            self.moves = moves

    def send_configuration(self, player, row, col):
        position = self.positions[player]
        fig = position["fig"]

        if fig:
            possible_moves = position["possible_moves"]

            self.positions[player]["fig"] = None
            if [col, row] in possible_moves:
                self.move(Move(fig, [col, row]))
                if player:
                    return {"board": self.board.straight_configuration()}
                else:
                    return {"board": self.board.rotated_configuration()}
            else:
                return self.send_configuration(player, row, col)
        else:
            possible_moves = get_possible_moves(self.board.configuration, player, col, row)
            self.positions[player]["fig"] = [col, row]
            self.positions[player]["possible_moves"] = possible_moves
            return {"moves": possible_moves}

    def move(self, move: Move):
        if isinstance(move, str):
            move = Move.from_string(move)

        if not self.board.is_legal_move(move):
            raise Exception("Illegal move")

        self.board.configuration[move.to_square.y][
            move.to_square.x] = self.board.configuration[move.from_square.y][move.from_square.x]
        self.board.configuration[move.from_square.y][move.from_square.x] = '.'

class Point(Enum):
    NOT = -1
    SAME = 0
    ENEMY = 1
    FREE = 2

def get_possible_moves(board: list, player, row, col):
    if player:
        fig = board[col][row]
    else:
        fig = board[7 - col][7 - row]
    if fig == ".":
        return []
    if fig.isupper() != player:
        return []

    possible_moves = []
    match(fig.lower()):
        case "p":
            if can_go(board, player, row, col - 1) == Point.FREE:
                possible_moves.append([row, col - 1])
                if col == 6:
                    if can_go(board, player, row, col - 2) == Point.FREE:
                        possible_moves.append([row, col - 2])
            if can_go(board, player, row - 1, col - 1) == Point.ENEMY:
                possible_moves.append([row - 1, col - 1])
            if can_go(board, player, row + 1, col - 1) == Point.ENEMY:
                possible_moves.append([row + 1, col - 1])
        case "k":
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i or j:
                        if can_go(board, player, row + i, col + j).value > 0:
                            possible_moves.append([row + i, col + j])
        case "q":
            allowed = [True] * 9
            for i in range(1, 8):
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        if k or j:
                            ind = (j + 1) * 3 + k + 1
                            if not allowed[ind]:
                                continue
                            go = can_go(board, player, row + i * j, col + i * k)
                            if go.value > 0:
                                possible_moves.append([row + i * j, col + i * k])
                            if go != Point.FREE:
                                allowed[ind] = False
        case "b":
            allowed = [True] * 4
            for i in range(1, 8):
                for j in range(-1, 2, 2):
                    for k in range(-1, 2, 2):
                        ind = (j + 1) + (k + 1) // 2
                        if not allowed[ind]:
                            continue
                        go = can_go(board, player, row + i * j, col + i * k)
                        if go.value > 0:
                            possible_moves.append([row + i * j, col + i * k])
                        if go != Point.FREE:
                            allowed[ind] = False
        case "r":
            allowed = [True] * 4
            for i in range(1, 8):
                for j in range(-1, 2, 2):
                    ind = (j + 1) // 2
                    if not allowed[ind]:
                        continue
                    go = can_go(board, player, row + i * j, col)
                    if go.value > 0:
                        possible_moves.append([row + i * j, col])
                    if go != Point.FREE:
                        allowed[ind] = False
                for j in range(-1, 2, 2):
                    ind = 2 + (j + 1) // 2
                    if not allowed[ind]:
                        continue
                    go = can_go(board, player, row, col + i * j)
                    if go.value > 0:
                        possible_moves.append([row, col + i * j])
                    if go != Point.FREE:
                        allowed[ind] = False
        case "n":
            for i in range(-1, 2, 2):
                for j in range(1, 3):
                    for k in range(-1, 2, 2):
                        if can_go(board, player, row + i * j, col + k * 2 // j).value > 0:
                            possible_moves.append([row + i * j, col + k * 2 // j])
        case _:
            pass
    return possible_moves

def can_go(board, case, row, col):
    if 0 <= row < 8 and 0 <= col < 8:
        figure = board[col][row]
        if figure == ".":
            # print("free")
            return Point.FREE
        if figure.isupper() != case:
            # print("enemy")
            return Point.ENEMY
        # print("same")
        return Point.SAME
    else:
        # print("not")
        return Point.NOT

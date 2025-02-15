from .board import Board
from .move import Move
from enum import Enum
from datetime import datetime

class Game:
    board: Board
    moves: list = []
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
                fig = self.move(Move(fig, [col, row]), player)
                if fig.lower() == "k":
                    end_game = True
                else:
                    end_game = False
                    
                if player:
                    return {"board": self.board.straight_configuration(), "end_game": end_game}
                else:
                    return {"board": self.board.rotated_configuration(), "end_game": end_game}
            else:
                return self.send_configuration(player, row, col)
        else:
            is_on_time = self.check_time(row, col)
            if is_on_time:
                possible_moves = get_possible_moves(self.board.configuration, player, col, row)
                if not player:
                    possible_moves = [[7 - x, 7 - y] for x, y in possible_moves]
                self.positions[player]["fig"] = [col, row]
            else:
                possible_moves = []
                self.positions[player]["fig"] = None

            self.positions[player]["possible_moves"] = possible_moves
            return {"moves": possible_moves}

    def check_time(self, row, col):
        move_to_point = next((x for x in self.moves if x["move"].to_square.x == col and x["move"].to_square.y == row), None)
        if not move_to_point:
            return True
        delta = datetime.now() - move_to_point["time"]
        return delta.total_seconds() > 5

    def move(self, move: Move, player):
        if isinstance(move, str):
            move = Move.from_string(move)

        last_line = move.to_square.y == 0

        if not player:
            move.from_square.x = 7 - move.from_square.x
            move.to_square.x = 7 - move.to_square.x
            move.from_square.y = 7 - move.from_square.y
            move.to_square.y = 7 - move.to_square.y

        if not self.board.is_legal_move(move):
            raise Exception("Illegal move")

        self.moves.append({
            "move": move,
            "player": player,
            "time": datetime.now()
        })

        fig = self.board.configuration[move.from_square.y][move.from_square.x]
        to_fig = self.board.configuration[move.to_square.y][move.to_square.x]

        if fig.lower() == "p" and last_line:
            self.board.configuration[move.to_square.y][move.to_square.x] = fig.isupper() and "Q" or "q"
        else:
            self.board.configuration[move.to_square.y][
                move.to_square.x] = self.board.configuration[move.from_square.y][move.from_square.x]
        self.board.configuration[move.from_square.y][move.from_square.x] = '.'
        return to_fig

class Point(Enum):
    NOT = -1
    SAME = 0
    ENEMY = 1
    FREE = 2

def get_possible_moves(board: list, player, row, col):
    if not player:
        col = 7 - col
        row = 7 - row

    fig = board[col][row]
    mod = [-1, 1][player]
    
    if fig == ".":
        return []
    if fig.isupper() != player:
        return []

    possible_moves = []
    match(fig.lower()):
        case "p":
            if can_go(board, player, row, col - mod) == Point.FREE:
                possible_moves.append([row, col - mod])
                if (col == 6 and player) or (col == 1 and not player):
                    if can_go(board, player, row, col - 2 * mod) == Point.FREE:
                        possible_moves.append([row, col - 2 * mod])
            if can_go(board, player, row - 1, col - mod) == Point.ENEMY:
                possible_moves.append([row - 1, col - mod])
            if can_go(board, player, row + 1, col - mod) == Point.ENEMY:
                possible_moves.append([row + 1, col - mod])
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

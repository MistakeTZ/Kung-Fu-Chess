from .game import Game
from enum import Enum

class Point(Enum):
    NOT = -1
    SAME = 0
    ENEMY = 1
    FREE = 2

def get_possible_moves(game: Game, player, col, row):
    conf = game.board.configuration
    if player:
        fig = conf[col][row]
    else:
        fig = conf[7 - col][7 - row]
    if fig == ".":
        return []
    if fig.isupper() != player:
        return []
    mod = 1 if player else -1

    possible_moves = []
    match(fig.lower()):
        case "p":
            if can_go(conf, player, row, col - 1) == Point.FREE:
                possible_moves.append([row, col - 1])
                if col == 6:
                    if can_go(conf, player, row, col - 2) == Point.FREE:
                        possible_moves.append([row, col - 2])
            if can_go(conf, player, row - 1, col - 1) == Point.ENEMY:
                possible_moves.append([row - 1, col - 1])
            if can_go(conf, player, row + 1, col - 1) == Point.ENEMY:
                possible_moves.append([row + 1, col - 1])
        case "k":
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i or j:
                        if can_go(conf, player, row + i, col + j).value > 0:
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
                            go = can_go(conf, player, row + i * j, col + i * k)
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
                        go = can_go(conf, player, row + i * j, col + i * k)
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
                    go = can_go(conf, player, row + i * j, col)
                    if go.value > 0:
                        possible_moves.append([row + i * j, col])
                    if go != Point.FREE:
                        allowed[ind] = False
                for j in range(-1, 2, 2):
                    ind = 2 + (j + 1) // 2
                    if not allowed[ind]:
                        continue
                    go = can_go(conf, player, row, col + i * j)
                    if go.value > 0:
                        possible_moves.append([row, col + i * j])
                    if go != Point.FREE:
                        allowed[ind] = False
        case "n":
            for i in range(-1, 2, 2):
                for j in range(1, 3):
                    for k in range(-1, 2, 2):
                        if can_go(conf, player, row + i * j, col + k * 2 // j).value > 0:
                            possible_moves.append([row + i * j, col + k * 2 // j])
        case _:
            pass
    return possible_moves

def can_go(conf, case, row, col):
    # print(row, col)
    if 0 <= row < 8 and 0 <= col < 8:
        figure = conf[col][row]
        # print(figure, case)
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
    
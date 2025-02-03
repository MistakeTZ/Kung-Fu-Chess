from models.chess.game import Game
from flask import render_template, request, jsonify, Blueprint, session
from models.games import games
import uuid


simple_page = Blueprint('simple_page', __name__, template_folder='templates')

@simple_page.route('/')
def chessboard():
    if 'player_id' not in session:
        session['player_id'] = str(uuid.uuid4())
    return render_template('join.html')
    # return render_template('chessboard.html', board=game.board.rotated_configuration())

@simple_page.route('/game/<game_id>')
def game_page(game_id):
    if game_id in games:
        player = session.get('player_id')
        session["game_id"] = game_id
        game = games[game_id]
        
        if player == game['players'][0]:
            return render_template('chessboard.html', board=game['game'].board.rotated_configuration())
        elif player == game['players'][1]:
            return render_template('chessboard.html', board=game['game'].board.straight_configuration())
    return render_template('404.html'), 404

@simple_page.route('/moves')
def get_moves():
    row = int(request.args.get('row'))
    col = int(request.args.get('col'))

    if session["game_id"] in games:
        game = games[session["game_id"]]["game"]
        player = games[session["game_id"]]["players"].index(
            session["player_id"])
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
        print(row, col)

        possible_moves = []
        match(fig.lower()):
            case "p":
                possible_moves.append([row, col - 1])
                if col == 6:
                    possible_moves.append([row, col - 2])
            case "k":
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i or j:
                            possible_moves.append([row + i, col + j])
            case "q":
                for i in range(1, 8):
                    possible_moves.append([row - i, col])
                    possible_moves.append([row + i, col])
                    possible_moves.append([row, col + i])
                    possible_moves.append([row, col - i])
                    possible_moves.append([row + i, col + i])
                    possible_moves.append([row + i, col - i])
                    possible_moves.append([row - i, col + i])
                    possible_moves.append([row - i, col - i])
            case "b":
                for i in range(1, 8):
                    possible_moves.append([row + i, col + i])
                    possible_moves.append([row + i, col - i])
                    possible_moves.append([row - i, col + i])
                    possible_moves.append([row - i, col - i])
            case "r":
                for i in range(1, 8):
                    possible_moves.append([row - i, col])
                    possible_moves.append([row + i, col])
                    possible_moves.append([row, col + i])
                    possible_moves.append([row, col - i])
            case "n":
                possible_moves.append([row + 1, col - 2])
                possible_moves.append([row + 1, col + 2])
                possible_moves.append([row - 1, col - 2])
                possible_moves.append([row - 1, col + 2])
                possible_moves.append([row - 2, col + 1])
                possible_moves.append([row + 2, col + 1])
                possible_moves.append([row - 2, col - 1])
                possible_moves.append([row + 2, col - 1])
            case _:
                pass

        # Фильтруем ходы, чтобы они оставались в пределах доски
        possible_moves = [
            [r, c] for r, c in possible_moves if 0 <= r < 8 and 0 <= c < 8
        ]
    else:
        possible_moves = []

    return jsonify(possible_moves)
from models.chess.game import Game
from flask import render_template, request, jsonify, Blueprint, session
from models.games import games
from models.chess.game_logic import get_possible_moves
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
    print(row, col)

    if session["game_id"] in games:
        game = games[session["game_id"]]["game"]
        player = games[session["game_id"]]["players"].index(
            session["player_id"])
        possible_moves = get_possible_moves(game, player, col, row)

    else:
        possible_moves = []

    return jsonify(possible_moves)

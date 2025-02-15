from flask_socketio import SocketIO, Namespace
from flask import render_template, request, jsonify, Blueprint, session
from models.games import games
import uuid


def register_handlers(socketio: SocketIO):
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
        game_id = session["game_id"]

        if not game_id in games:
            return jsonify({"moves": []})

        game_dict = games[game_id]
        game = game_dict["game"]
        player = game_dict["players"].index(
            session["player_id"])

        configurations = game.send_configuration(player, col, row)
        # return jsonify(configurations)
        if "moves" in configurations:
            return jsonify(configurations)
        else:
            conf = {
                "row": 7 - row,
                "col": 7 - col,
                "board": game.board.rotated_configuration() if player else game.board.straight_configuration()
            }
            socketio.emit('move', conf, room=game_dict["players"][not player])
            return jsonify(configurations)

    return simple_page

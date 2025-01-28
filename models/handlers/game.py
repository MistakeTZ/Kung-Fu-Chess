from app import game
from flask import render_template, request, jsonify, Blueprint


simple_page = Blueprint('simple_page', __name__, template_folder='templates')

@simple_page.route('/')
def chessboard():
    return render_template('chessboard.html', board=game.board.rotated_configuration())

@simple_page.route('/moves')
def get_moves():
    row = int(request.args.get('row'))
    col = int(request.args.get('col'))
    fig = game.board.configuration[col][row]
    print(fig)

    # Пример доступных ходов (здесь должна быть ваша логика)
    possible_moves = [
        [row - 1, col], [row + 1, col],  # Пример для пешки
        [row, col - 1], [row, col + 1]   # Пример для ладьи
    ]

    # Фильтруем ходы, чтобы они оставались в пределах доски
    possible_moves = [
        [r, c] for r, c in possible_moves if 0 <= r < 8 and 0 <= c < 8
    ]

    return jsonify(possible_moves)
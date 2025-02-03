from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ваш_секретный_ключ'
socketio = SocketIO(app)
game_state = defaultdict(dict)

from new_module_test import register_multiplayer_handlers
register_multiplayer_handlers(socketio)


@socketio.on('move')
def handle_move(data):
    user_id = data['user_id']
    direction = data['direction']
    # Обновляем состояние игры
    game_state[user_id]['position'] = update_position(game_state[user_id].get('position', (0, 0)), direction)
    # Отправляем обновленное состояние всем игрокам
    emit('game_update', game_state, broadcast=True)

def update_position(position, direction):
    x, y = position
    if direction == 'up':
        y += 1
    elif direction == 'down':
        y -= 1
    elif direction == 'left':
        x -= 1
    elif direction == 'right':
        x += 1
    return x, y

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0")

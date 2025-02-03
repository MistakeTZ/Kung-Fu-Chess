# models/handlers/multiplayer.py
from flask_socketio import emit, join_room
from models.games import add_player_to_queue, create_game, player_queue

def register_multiplayer_handlers(socketio):
    @socketio.on('join')
    def handle_join_game(data):
        username = data.get('player_id')
        print(f"Пользователь {username} присоединился к игре")
        join_room(username)

    @socketio.on('find_game')
    def handle_find_game(data):
        player_id = data.get('player_id')
        queue_size = add_player_to_queue(player_id)

        if queue_size >= 2:
            # Если в очереди есть два игрока, создаем игру
            player1 = player_queue.pop(0)
            player2 = player_queue.pop(0)
            game_id = create_game(player1, player2)

            # Отправляем игрокам информацию о созданной игре
            emit('game_created', {'game_id': game_id}, room=player1, broadcast=True)
            emit('game_created', {'game_id': game_id}, room=player2, broadcast=True)

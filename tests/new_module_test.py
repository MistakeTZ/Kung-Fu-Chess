from flask_socketio import emit, send

def register_multiplayer_handlers(socketio):
    @socketio.on('message')
    def handle_message(data):
        print(f"Получено сообщение: {data}")
        send(data, broadcast=True)  # Отправляем сообщение всем подключенным клиентам

    @socketio.on('join')
    def handle_join(data):
        print(f"Пользователь {data['username']} присоединился")
        emit('user_joined', data, broadcast=True)  # Уведомляем всех о новом пользователе
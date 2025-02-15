from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = "my_secret_key"
socketio = SocketIO(app)

if __name__ == '__main__':
    from models.handlers.game import register_handlers
    simple_page = register_handlers(socketio)

    # Подклчение обработчиков
    app.register_blueprint(simple_page)
    from models.handlers.multiplayer import register_multiplayer_handlers
    register_multiplayer_handlers(socketio)

    socketio.run(app, debug=True, host="0.0.0.0")

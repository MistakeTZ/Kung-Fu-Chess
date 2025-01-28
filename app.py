from flask import Flask
from models.chess.game import Game

app = Flask(__name__)
game = Game()

if __name__ == '__main__':
    from models.handlers.game import simple_page
    app.register_blueprint(simple_page)
    app.run(debug=True)

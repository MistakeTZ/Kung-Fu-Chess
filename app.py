from flask import Flask, render_template
from models.chess.game import Game

app = Flask(__name__)
game = Game()

@app.route('/')
def chessboard():
    return render_template('chessboard.html', board=game.board.rotated_configuration())

if __name__ == '__main__':
    app.run(debug=True)

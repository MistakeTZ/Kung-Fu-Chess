from models.chess.game import Game

game = Game()

print(game.board)
game.move("a2a4")
print(game.board)
game.move("c2a5")
print(game.board)
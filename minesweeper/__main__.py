import sys

from minesweeper.controller.controller import MinesweeperController
from minesweeper.model.game_model import MinesweeperModel
from minesweeper.view.main_view import MainView


model = MinesweeperModel()
controller = MinesweeperController(model)
view = MainView(model, controller)
view.run()

sys.exit()

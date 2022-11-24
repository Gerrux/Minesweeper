from controller import MinesweeperController
from models.game_model import MinesweeperModel
from views.main_view import MainView


def main():
    model = MinesweeperModel()
    controller = MinesweeperController(model)
    view = MainView(model, controller)
    view.run()


if __name__ == '__main__':
    main()


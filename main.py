from controller import MinesweeperController
from models.game_model import MinesweeperModel
from views.game_view import MinesweeperView
from views.menu_view import MenuView


def main():
    model = MinesweeperModel()
    controller = MinesweeperController(model)
    while True:
        menu_view = MenuView(controller)
        menu_view.run()
        view = MinesweeperView(model, controller, controller.get_game_mode())
        view.run()


if __name__ == '__main__':
    main()


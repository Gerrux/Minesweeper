from .views.game_view import MinesweeperView
from .views.menu_view import MenuView


class MainView:
    def __init__(self, model, controller):
        self.current_view = None
        self.model = model
        self.controller = controller

    def switch_on_menu(self):
        self.current_view = MenuView(self.controller)
        self.current_view.run()

    def switch_on_game(self):
        self.current_view = MinesweeperView(
            self.model, self.controller, self.controller.get_game_mode()
        )
        self.current_view.run()

    def run(self):
        while True:
            match self.controller.get_view_state():
                case "menu":
                    self.switch_on_menu()
                case "game":
                    self.switch_on_game()

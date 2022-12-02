from .views.game_view import MinesweeperView
from .views.menu_view import MenuView
from .views.records_view import RecordsView


class MainView:
    __current_view = None

    def __init__(self, model, controller):

        self.model = model
        self.controller = controller

    def switch_on_menu(self):
        self.__current_view = MenuView(self.controller)
        self.__current_view.run()

    def switch_on_records(self):
        self.__current_view = RecordsView(self.controller)
        self.__current_view.run()

    def switch_on_game(self):
        self.__current_view = MinesweeperView(
            self.model, self.controller, self.controller.get_game_mode()
        )
        self.__current_view.run()

    def run(self):
        while True:
            match self.controller.get_view_state():
                case "menu":
                    self.switch_on_menu()
                case "records":
                    self.switch_on_records()
                case "game":
                    self.switch_on_game()

import time
from collections import defaultdict
import pygame

from assets.colors import SECONDARY_COLOR, PRIMARY_COLOR, WARNING_COLOR
import config as c
from .elements.button import Button
from .elements.cell import Cell
from .elements.image import Image
from .elements.rectangle import Rectangle
from .elements.text_object import TextObject
from .view import BaseView


class MinesweeperView(BaseView):
    def __init__(self, model, controller, game_mode):
        BaseView.__init__(self,
                          caption=c.CAPTION,
                          width=c.GAME_MODE[game_mode]["surface_width"],
                          height=c.GAME_MODE[game_mode]["surface_height"],
                          background_color=pygame.Color(SECONDARY_COLOR),
                          frame_rate=c.FRAME_RATE,
                          icon=pygame.image.load(c.ICON))

        self.surface_width = c.GAME_MODE[game_mode]["surface_width"]
        self.surface_height = c.GAME_MODE[game_mode]["surface_height"]

        self.cell_width = c.GAME_MODE[game_mode]["cell_width"]
        self.cell_height = c.GAME_MODE[game_mode]["cell_height"]

        self.row_count = c.GAME_MODE[game_mode]["count_cells_row"]
        self.column_count = c.GAME_MODE[game_mode]["count_cells_column"]

        self.sound_effects = {name: pygame.mixer.Sound(sound) for name, sound in c.SOUNDS.items()}
        self.sprites = {name: pygame.transform.scale(
            pygame.image.load(sprite), (self.cell_width, self.cell_height)
        ) for name, sprite in c.GAME_SPRITES.items()}
        self.font = pygame.font.Font(c.FONT, c.FONT_SIZE)
        self.message_font = pygame.font.Font(c.FONT, c.FONT_SIZE * 2)

        self.game_area_width = self.row_count * self.cell_height
        self.game_area_height = self.column_count * self.cell_width

        self.bomb_count = c.GAME_MODE[game_mode]["count_bomb"]

        self.surface = pygame.display.set_mode((self.surface_width, self.surface_height))
        self.background_color = SECONDARY_COLOR
        self.surface.fill(self.background_color)
        pygame.display.set_caption(c.CAPTION)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

        self.model = model
        self.controller = controller
        self.controller.set_view(self)

        self.clock_image = pygame.image.load(c.CLOCK)
        self.bomb_image = pygame.image.load(c.ICON)
        self.board = None
        self.timer_string = None
        self.bomb_num_string = None

        self.pause_menu_buttons = []
        self.game_time = 0
        self.create_game_area()
        self.create_timer()
        self.create_pause_button()
        self.create_bomb_info()
        self.controller.start_new_game()

        self.show_message('GET READY!', centralized=True, duration=3)
        self.start_time = pygame.time.get_ticks()
        self.game_paused = False

    def get_game_settings(self):
        return self.row_count, self.column_count, self.bomb_count

    def get_view_cell_from_objects(self, cell):
        for i in range(len(self.objects)):
            checked_object = self.objects[i]
            if type(checked_object) == Cell:
                if checked_object.x == cell.row and checked_object.y == cell.column:
                    return checked_object, i

    def sync_with_model(self):
        for row in range(self.model.row_count):
            for column in range(self.model.column_count):
                cell = self.model.get_cell(row, column)
                if cell:
                    view_cell = self.get_view_cell_from_objects(cell)
                    view_cell, cell_index_in_objects = view_cell[0], view_cell[1]
                    if self.model.is_game_over() and cell.mined:
                        view_cell.is_pressed = True
                        view_cell.normal_image = self.sprites['bomb']

                    if cell.state == 'closed' and not view_cell.is_pressed:
                        view_cell.normal_image = self.sprites['cell_surf']

                    elif cell.state == 'opened':
                        view_cell.is_pressed = True
                        view_cell.state = 'pressed'
                        view_cell.image = self.sprites['blank']
                        if cell.counter > 0:
                            warn = f'warn{cell.counter}'
                            view_cell.image = self.sprites[warn]
                        elif cell.mined:
                            view_cell.image = self.sprites['bomb_explode']

                    elif cell.state == 'flagged':
                        if self.model.is_game_over() and cell.mined:
                            view_cell.normal_image = self.sprites['bomb_block']
                        else:
                            view_cell.normal_image = self.sprites['flag']
                            view_cell.image = self.sprites['flag']

                    elif cell.state == 'questioned':
                        view_cell.normal_image = self.sprites['question']
                        view_cell.image = self.sprites['cell_surf']
                    self.objects[cell_index_in_objects] = view_cell

    def block_cell(self, row, column, block=True):
        cell = self.get_view_cell_from_objects(self.model.get_cell(row, column))
        cell, cell_index_in_objects = cell[0], cell[1]
        if not cell:
            return
        if block:
            cell.is_block = True
        else:
            cell.is_block = False
        self.objects[cell_index_in_objects] = cell

    def create_bomb_info(self):
        self.objects.append(Image(self.bomb_image,
                                  self.surface_width - 60 - 10,
                                  self.game_area_height + 30,
                                  60,
                                  60))

        self.bomb_num_string = str(self.bomb_count)

        bomb_info = TextObject(self.surface_width - 60 - 40,
                               self.game_area_height + 45, lambda:
                               self.bomb_num_string,
                               PRIMARY_COLOR, self.font)

        self.objects.append(bomb_info)

    def create_timer(self):
        self.objects.append(Image(self.clock_image,
                                  10,
                                  self.game_area_height + 30,
                                  60,
                                  60))

        timer = TextObject(60 + 20,
                           self.game_area_height + 45,
                           lambda: self.timer_string,
                           PRIMARY_COLOR,
                           self.font)
        self.objects.append(timer)

    def update_timer(self):
        self.game_time = pygame.time.get_ticks() - self.start_time

        minutes = self.game_time / 1000 / 60
        seconds = self.game_time / 1000 % 60

        if seconds < 10:
            seconds_string = "0" + str(int(seconds))
        else:
            seconds_string = str(int(seconds))

        if minutes < 10:
            minutes_string = "0" + str(int(minutes))
        else:
            minutes_string = str(int(minutes))

        self.timer_string = f"{minutes_string}:{seconds_string}"

    def update_bomb_info(self):
        self.bomb_num_string = str(self.bomb_count - self.controller.get_count_flags())

    def create_game_area(self):
        self.objects.append(Rectangle(10,
                                      10,
                                      self.game_area_width,
                                      self.game_area_height,
                                      PRIMARY_COLOR))

    def create_board(self):
        def on_check(view_cell):
            self.sound_effects["click"].play()
            view_cell.is_pressed = True
            view_cell.state = 'pressed'
            self.controller.on_left_click(view_cell.x, view_cell.y)

        def on_flagged(view_cell):
            self.sound_effects["flag"].play()
            self.controller.on_right_click(view_cell.x, view_cell.y)

        for x in range(self.row_count):
            for y in range(self.column_count):
                cell_position = pygame.Rect(x * self.cell_width + 10,
                                            y * self.cell_height + 10,
                                            self.cell_width,
                                            self.cell_height)
                cell = Cell(cell_position,
                            self.sprites["cell_surf"],
                            on_left_click=on_check,
                            on_right_click=on_flagged)
                cell.x = x
                cell.y = y
                self.objects.append(cell)
                self.mouse_handlers.append(cell.handle_mouse_event)

    def create_pause_button(self):
        def on_pause(button):
            self.game_paused = True
            self.create_pause_menu()

        pause_button = Button(self.surface_width / 2 - 60,
                              self.game_area_height + 30,
                              120,
                              60,
                              "PAUSE",
                              on_pause,
                              padding=5,
                              font=self.font,
                              centralized=True,
                              corner_radius=10)
        self.objects.append(pause_button)
        self.mouse_handlers.append(pause_button.handle_mouse_event)

    def create_pause_menu(self):
        def on_play(button):
            self.sound_effects["click"].play()
            for pause_button in self.pause_menu_buttons:
                self.objects.remove(pause_button)
                self.mouse_handlers.remove(pause_button.handle_mouse_event)
            self.pause_menu_buttons = []
            self.objects.remove(background_menu)
            self.game_paused = False
            self.mouse_handlers = buffer_mouse_handlers
            self.start_time = pygame.time.get_ticks() - self.game_time

        def on_menu(button):
            self.view_run = False

        background_menu = Rectangle(0, 0, self.surface_width, self.surface_height, pygame.Color(SECONDARY_COLOR))
        buffer_mouse_handlers = self.mouse_handlers
        self.mouse_handlers = []
        self.objects.append(background_menu)
        for i, (text, click_handler) in enumerate((('PLAY', on_play), ('MENU', on_menu))):
            b = Button(20,
                       300 + (50 + 5) * i,
                       100,
                       50,
                       text,
                       click_handler,
                       padding=5,
                       font=self.font,
                       centralized=True,
                       corner_radius=15)
            self.objects.append(b)
            self.pause_menu_buttons.append(b)
            self.mouse_handlers.append(b.handle_mouse_event)

    def update(self):
        if not self.view_run:
            return

        if not self.game_paused:
            self.update_timer()
            self.update_bomb_info()
        super().update()

        if self.model.game_over:
            self.show_game_over_message()

    def show_message(self, text, color=SECONDARY_COLOR, centralized=False, duration=c.MESSAGE_DURATION):
        message = TextObject(self.game_area_width // 2,
                             self.game_area_height // 2,
                             lambda: text, color,
                             self.message_font)
        self.draw()
        message.draw(self.surface, centralized)
        pygame.display.update()
        time.sleep(duration)

    def show_win_message(self):
        self.sound_effects["win"].set_volume(c.VOLUME_MUSIC)
        self.sound_effects["win"].play()
        self.show_message('YOU WIN!', WARNING_COLOR, centralized=True)
        self.view_run = False

    def show_game_over_message(self):
        self.sound_effects["lose"].set_volume(c.VOLUME_MUSIC)
        self.sound_effects["lose"].play()
        self.show_message('YOU LOSE!', WARNING_COLOR, centralized=True)
        self.view_run = False

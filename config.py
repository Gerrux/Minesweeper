CAPTION = "Minesweeper"
ICON = "assets/sprites/logo.png"
FONT = "assets/fonts/Retro.ttf"
FONT_SIZE = 20

FRAME_RATE = 90

MENU_BACKGROUND = "assets/sprites/menu_background.png"

GAME_MODE = {
    "easy": {
        "count_cells_row": 9,
        "count_cells_column": 9,
        "cell_width": 60,
        "cell_height": 60,
        "count_bomb": 10,
        "surface_width": 560,
        "surface_height": 650
    },
    "medium": {
        "count_cells_row": 16,
        "count_cells_column": 16,
        "cell_width": 40,
        "cell_height": 40,
        "count_bomb": 40,
        "surface_width": 660,
        "surface_height": 760
    },
    "hard": {
        "count_cells_row": 30,
        "count_cells_column": 16,
        "cell_width": 40,
        "cell_height": 40,
        "count_bomb": 99,
        "surface_width": 1220,
        "surface_height": 760
    }
}

GAME_SPRITES = {
    "cell_surf": "assets/sprites/block.png",
    "cell_surf_select": "assets/sprites/select-block.png",
    "blank": "assets/sprites/blank-block.png",
    "warn1": "assets/sprites/warn1.png",
    "warn2": "assets/sprites/warn2.png",
    "warn3": "assets/sprites/warn3.png",
    "warn4": "assets/sprites/warn4.png",
    "warn5": "assets/sprites/warn5.png",
    "warn6": "assets/sprites/warn6.png",
    "warn7": "assets/sprites/warn7.png",
    "warn8": "assets/sprites/warn8.png",
    "bomb": "assets/sprites/bomb.png",
    "bomb_block": "assets/sprites/bomb-block.png",
    "bomb_explode": "assets/sprites/bomb-explode.png",
    "flag": "assets/sprites/flag.png",
    "question": "assets/sprites/question.png",
}

CLOCK = "assets/sprites/clock.png"

VOLUME_MUSIC = 0.8
VOLUME_EFFECTS = 0.5

SOUNDS = {
    "win": "assets/sounds/win.wav",
    "lose": "assets/sounds/lose.wav",
    "click": "assets/sounds/click.wav",
    "flag": "assets/sounds/flag.wav"
}

MESSAGE_DURATION = 5

from random import randint

from models.cell_model import MinesweeperCell

MIN_ROW_COUNT = 5
MAX_ROW_COUNT = 30

MIN_COLUMN_COUNT = 5
MAX_COLUMN_COUNT = 30

MIN_MINE_COUNT = 1
MAX_MINE_COUNT = 800


class MinesweeperModel:
    def __init__(self):
        self.game_mode = None
        self.cells_table = None
        self.game_over = None
        self.first_step = None
        self.bomb_count = None
        self.row_count = None
        self.column_count = None
        self.start_game()

    def start_game(self, row_count=15, column_count=15, bomb_count=15):
        if row_count in range(MIN_ROW_COUNT, MAX_ROW_COUNT + 1):
            self.row_count = row_count

        if column_count in range(MIN_COLUMN_COUNT, MAX_COLUMN_COUNT + 1):
            self.column_count = column_count

        if bomb_count < self.row_count * self.column_count:
            if bomb_count in range(MIN_MINE_COUNT, MAX_MINE_COUNT + 1):
                self.bomb_count = bomb_count
        else:
            self.bomb_count = self.row_count * self.column_count - 1

        self.first_step = True
        self.game_over = False
        self.cells_table = []
        for row in range(self.row_count):
            cells_row = []
            for column in range(self.column_count):
                cells_row.append(MinesweeperCell(row, column))
            self.cells_table.append(cells_row)

    def get_cell(self, row, column):
        if row < 0 or column < 0 or self.row_count <= row or self.column_count <= column:
            return None

        return self.cells_table[row][column]

    def get_count_flags(self):
        return len(list(filter(lambda c: c.state == 'flagged', sum(self.cells_table, []))))

    def is_win(self):
        for row in range(self.row_count):
            for column in range(self.column_count):
                cell = self.cells_table[row][column]
                if not cell.mined and (cell.state != 'opened' and cell.state != 'flagged'):
                    return False
        if self.get_count_flags() <= self.bomb_count:
            return True

    def is_game_over(self):
        return self.game_over

    def open_cell(self, row, column):
        cell = self.get_cell(row, column)
        if not cell:
            return

        cell.open()

        if cell.mined:
            self.game_over = True
            return

        if self.first_step:
            self.first_step = False
            self.pick_bombs()

        cell.counter = self.count_mines_around_cell(row, column)
        if cell.counter == 0:
            neighbours = self.get_cell_neighbours(row, column)
            for n in neighbours:
                if n.state == 'closed':
                    self.open_cell(n.row, n.column)

    def next_cell_mark(self, row, column):
        cell = self.get_cell(row, column)
        if cell:
            cell.next_mark()

    def pick_bombs(self):
        for i in range(self.bomb_count):
            while True:
                row = randint(0, self.row_count - 1)
                column = randint(0, self.column_count - 1)
                cell = self.get_cell(row, column)
                if not cell.state == 'opened' and not cell.mined:
                    cell.mined = True
                    break

    def count_mines_around_cell(self, row, column):
        neighbours = self.get_cell_neighbours(row, column)
        return sum(1 for n in neighbours if n.mined)

    def get_cell_neighbours(self, row, column):
        neighbours = []
        for r in range(row - 1, row + 2):
            neighbours.append(self.get_cell(r, column - 1))
            if r != row:
                neighbours.append(self.get_cell(r, column))
            neighbours.append(self.get_cell(r, column + 1))

        return filter(lambda n: n is not None, neighbours)

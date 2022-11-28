class MinesweeperCell:
    # Возможные состояния игровой клетки:
    #   closed - закрыта
    #   opened - открыта
    #   flagged - помечена флажком
    #   questioned - помечена вопросительным знаком

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.state = "closed"
        self.mined = False
        self.counter = 0

    mark_sequence = ["closed", "flagged", "questioned"]

    def next_mark(self):
        if self.state in self.mark_sequence:
            state_index = self.mark_sequence.index(self.state)
            self.state = self.mark_sequence[(state_index + 1) % len(self.mark_sequence)]

    def open(self):
        if self.state != "flagged":
            self.state = "opened"

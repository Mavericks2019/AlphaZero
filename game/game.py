from common_tools.test import windows


class Board:
    def __init__(self, width=15, height=15, n=5):
        self.width = width
        self.height = height
        self.n = n
        self.states = {}

    def show_board(self):
        return windows(self.width, self.height)

    def move_to_location(self, move):
        """
        0 1 2
        3 4 5
        6 7 8
        5 = (1, 2)
        """
        h = move // self.width
        w = move % self.width
        return [h, w]

    def location_to_move(self, location):
        if len(location) != 2:
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if move not in range(self.width * self.height):
            return -1
        return move

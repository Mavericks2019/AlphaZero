from common_tools.shapes import windows
from common_tools.shapes import GRID_WIDTH
from common_tools.graphics import Point
from common_tools.graphics import Circle


class Board:
    def __init__(self, width=15, height=15, n=5, show_board=True):
        self.width = width
        self.height = height
        self.n = n
        self.states = {}
        self.players = [1, 1]  # 1:black 0:white
        self.current_player = 1
        self.availables = set([i for i in range(width * height)])
        self.show_board = show_board
        if show_board:
            self.window = windows(width, height)

    def show_board(self):
        return windows(self.width, self.height)

    def move_to_location(self, move):
        """
        0 1 2
        3 4 5
        6 7 8
        5 = (1, 2)
        6 = (2, 0)
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

    def has_a_winner(self):
        width = self.width
        height = self.height
        states = self.states
        n = self.n

        moved = list(set(range(width * height)) - set(self.availables))
        if len(moved) < self.n * 2 - 1:
            return False, -1

        for m in moved:
            h = m // width
            w = m % width
            player = states[m]

            # rows
            if (w in range(width - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n))) == 1):
                return True, player
            # cols
            if (h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * width, width))) == 1):
                return True, player
            # \
            if (w in range(width - n + 1) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width + 1), width + 1))) == 1):
                return True, player
            # /
            if (w in range(n - 1, width) and h in range(height - n + 1) and
                    len(set(states.get(i, -1) for i in range(m, m + n * (width - 1), width - 1))) == 1):
                return True, player

        return False, -1

    def game_end(self):
        """Check whether the game is ended or not"""
        win, winner = self.has_a_winner()
        if win:
            return True, winner
        elif not len(self.availables):
            return True, -1
        return False, -1

    def human_plear_move(self):
        pos = self.window.getMouse()
        x = round((pos.getX()) / GRID_WIDTH)
        y = round((pos.getY()) / GRID_WIDTH)
        if x == 0 or y == 0:
            return
        piece = Circle(Point(GRID_WIDTH * x, GRID_WIDTH * y), 16)
        if self.current_player == 1:
            piece.setFill('black')
        else:
            piece.setFill('white')
        self.current_player = -self.current_player
        piece.draw(self.window)

    def move(self, move):
        self.states[move] = self.current_player
        self.availables.remove(move)
        self.current_player = -self.current_player


class Game:
    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2

    def start(self):
        pass


class HumanPlayer:
    def __init__(self, id):
        self.id = id

    def move(self, board):
        pass


if __name__ == '__main__':
    board = Board()
    while True:
        board.human_plear_move()

from graphics import GraphWin
from graphics import Line
from graphics import Point


GRID_WIDTH = 40
COLUMN = 15
ROW = 15


def windows():
    win = GraphWin("this is a gobang game", GRID_WIDTH * COLUMN, GRID_WIDTH * ROW)
    win.setBackground("yellow")
    i1 = 0
    while i1 <= GRID_WIDTH * COLUMN:
        l = Line(Point(i1, 0), Point(i1, GRID_WIDTH * COLUMN))
        l.draw(win)
        i1 = i1 + GRID_WIDTH
    i2 = 0

    while i2 <= GRID_WIDTH * ROW:
        l = Line(Point(0, i2), Point(GRID_WIDTH * ROW, i2))
        l.draw(win)
        i2 = i2 + GRID_WIDTH
    return win


if __name__ == '__main__':
    windows()

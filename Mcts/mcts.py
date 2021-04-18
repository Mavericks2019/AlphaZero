import random


class State:
    TURNS = 10
    MOVES = [2, -2, 3, -3]

    def __init__(self, value=0, moves=None, turns=TURNS):
        if not moves:
            moves = []
        self.value = value
        self.turns = turns
        self.moves = moves
        print(self.moves)

    def next_state(self):
        next_move = random.choice([x * self.turns for x in self.MOVES])
        return State(self.value + next_move, self.moves + [next_move], self.turns - 1)

    def over(self):
        if self.turns == 0:
            return True
        return False


class TreeNode:
    def __init__(self, state, parent=None):
        self.children = {}
        self.visit_count = 0
        self.reward = 0.0
        self.children = []
        self.parent = parent

    def add_child(self, child_state):
        child = TreeNode(child_state, self)
        self.children.append(child)

    def update(self, reward):
        self.reward += reward
        self.visit_count += 1

    def fully_eapand(self):
        if len(self.children) == len(State.MOVES):
            return True
        return False


if __name__ == '__main__':
    a = State()
    while not a.over():
        a = a.next_state()
    print(a.value)

import random
from math import sqrt
from math import log


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

    def __hash__(self):
        return hash(str(self.moves))

    def __eq__(self, other):
        return hash(self) == hash(other)

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

    def fully_expand(self):
        if len(self.children) == len(State.MOVES):
            return True
        return False


def expend(node):
    tried_children = set([c.state for c in node.children])
    new_state = node.state.next_state()
    while new_state not in tried_children:
        new_state = node.state.next_state()
    node.add_child(new_state)
    return node.children[-1]


def best_child_uct(node):
    best = 0.0
    res = []
    for child in node.children:
        exploit = child.reward / child.visit_count
        explore = sqrt(2.0 * log(node.visit_count) / float(child.visit_count))
        score = exploit + explore
        if score == best:
            res.append(child)
        if score > best:
            res = [child]
            best = score
        if len(res) == 0:
            print("no best child, please check")
    return random.choice(res)


if __name__ == '__main__':
    a = State()
    while not a.over():
        a = a.next_state()

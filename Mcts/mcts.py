import random
from graphviz import Digraph
from math import sqrt
from math import log
from queue import Queue


class State:
    TURNS = 10
    MOVES = [2, -2, 3, -3]
    GOAL = 0

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

    def reward(self):
        return abs(self.value - self.GOAL)

    def node_id(self):
        return str(self)

    def node_info(self):
        return str(self)


class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
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


def uct_serach(budget, mct_tree_root):
    for i in range(int(budget)):
        if i % 10000 == 9999:
            print(f"simulation:{i}")
            print(mct_tree_root)
        front = tree_policy(mct_tree_root)
        reward = default_policy(front.state)
        backup(front, reward)
    return best_child_uct(mct_tree_root)


def tree_policy(node):
    while not node.state.over():
        if len(node.children) == 0:
            return expend(node)
        elif random.uniform(0, 1) < 0.5:
            return best_child_uct(node)
        elif node.fully_expand():
            return best_child_uct(node)
        else:
            return expend(node)


def expend(node):
    tried_children = set([c.state for c in node.children])
    new_state = node.state.next_state()
    while new_state in tried_children:
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


def default_policy(state):
    while not state.over():
        state = state.next_state()
    return state.reward()


def backup(node, reward):
    while node is not None:
        node.visit_count += 1
        node.reward += reward
        node = node.parent


def show_tree(root):
    dot = Digraph(comment="MCTS")
    q = Queue()
    q.put(root)
    while not q.empty():
        curr = q.get()
        dot.node(curr.state.node_id(), curr.state.node_info())
        if curr != root:
            dot.edge(curr.parent.state.node_id(), curr.state.node_id())
        for n in curr.children:
            q.put(n)
    with open("MCTS.dot", "w", encoding="utf-8") as w:
        w.write(dot.source)
    dot.render("serach_path", view=False)


def main():
    level = 1
    num_sim = 500
    curr = TreeNode(State())
    for le in range(level):
        curr = uct_serach(num_sim/(level + 1), curr)
    root = curr
    while root.parent:
        root = root.parent
    show_tree(root)


if __name__ == '__main__':
    main()

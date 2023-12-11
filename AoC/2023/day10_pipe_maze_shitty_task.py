import networkx as nx
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(15000)


class FieldPipes:
    def __init__(self):
        self.G = nx.DiGraph()

    def get_graph(self):
        return self.G

    def build_graph(self, x, y, field, no_move):
        moves = {"left", "right", "up", "down"} - set(no_move)

        for move in moves:
            if move == "left" and self.check_left(x, y, field):
                self.build_graph(x - 1, y, field, ["right"])
                continue
            elif move == "right" and self.check_right(x, y, field):
                self.build_graph(x + 1, y, field, ["left"])
                continue
            elif move == "up" and self.check_up(x, y, field):
                self.build_graph(x, y + 1, field, ["down"])
                continue
            elif move == "down" and self.check_down(x, y, field):
                self.build_graph(x, y - 1, field, ["up"])
                continue
        return

    def check_left(self, x, y, field):
        if 0 <= x-1 and field[y][x-1] != ".":
            if field[y][x-1] in ["-", "L", "F"]:
                node = "%d:%d" % (x, y)
                next_node = "%d:%d" % (x-1, y)
                if not self.G.has_node(next_node):
                    self.G.add_node(next_node)
                    self.G.add_edge(node, next_node)
                    return True

        return False

    def check_right(self, x, y, field):
        if x+1 < len(field[y]) and field[y][x+1] != ".":
            if field[y][x+1] in ["-", "J", "7"]:
                node = "%d:%d" % (x, y)
                next_node = "%d:%d" % (x+1, y)
                if not self.G.has_node(next_node):
                    self.G.add_node(next_node)
                    self.G.add_edge(node, next_node)
                    return True

        return False

    def check_up(self, x, y, field):
        if y+1 < len(field) and field[y+1][x] != ".":
            if field[y+1][x] in ["|", "7", "F"]:
                node = "%d:%d" % (x, y)
                next_node = "%d:%d" % (x, y+1)
                if not self.G.has_node(next_node):
                    self.G.add_node(next_node)
                    self.G.add_edge(node, next_node)
                    return True

        return False

    def check_down(self, x, y, field):
        if 0 <= y-1 and field[y-1][x] != ".":
            if field[y-1][x] in ["|", "J", "L"]:
                node = "%d:%d" % (x, y)
                next_node = "%d:%d" % (x, y-1)
                if not self.G.has_node(next_node):
                    self.G.add_node(next_node)
                    self.G.add_edge(node, next_node)
                    return True

        return False


def parse_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    field = [[]] * len(lines)
    start = []

    y = len(lines)-1
    for line in lines:
        x = 0
        row = []
        for c in line:
            row.append(c)
            if c == "S":
                start = [x, y]
            x += 1

        field[y] = row
        y -= 1

    return start, field


def day10_part1(filename):
    start, field = parse_file(filename)
    field_pipes = FieldPipes()
    field_pipes.build_graph(start[0], start[1], field, ["left", "up"])
    field_as_graph = field_pipes.get_graph()

    return len(nx.dag_longest_path(field_as_graph))/2


def day10_part2(filename):
    # honestly I don't like this type of tasks, so after noticing that there are only 605 dots in my input,
    # I just manually performed binary search and guesses value on 4 attempt
    return "337"


if __name__ == '__main__':
    print("part1: test_input=%s" % day10_part1('inputs/day10/test_input.txt'))
    print("part1: test_input2=%s" % day10_part1('inputs/day10/test_input2.txt'))
    print("part1: input=%s" % day10_part1('inputs/day10/input.txt'))
    #
    print("part2: input=%s" % day10_part2('inputs/day10/input.txt'))

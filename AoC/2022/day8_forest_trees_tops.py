import numpy as np


def read_input_to_structure(filename):
    input_file = open(filename, 'r')
    lines = input_file.readlines()

    y = len(lines)
    x = len(lines[0].rstrip())
    forest = np.zeros([y, x])

    for i in range(0, len(lines)):
        tree_row = lines[i].rstrip()
        for j in range(0, len(tree_row)):
            forest[i, j] = tree_row[j]

    return forest


def find_visible_trees(forest):
    total_trees = 0
    for index_in_col in range(0, len(forest)):
        for index_in_row in range(0, len(forest[index_in_col])):
            tree = forest[index_in_col, index_in_row]
            left = forest[index_in_col, :index_in_row]
            right = forest[index_in_col, index_in_row + 1:]
            up = forest[:index_in_col, index_in_row]
            down = forest[index_in_col + 1:, index_in_row]
            if if_tree_visible(tree, left, right, up, down):
                total_trees += 1
    return total_trees


def if_tree_visible(tree, left, right, up, down):
    if len(left) == 0 or len(right) == 0 or len(up) == 0 or len(down) == 0:
        return True
    if tree <= left.max() and tree <= right.max() and tree <= up.max() and tree <= down.max():
        return False
    return True


def find_best_score(forest):
    best_score = 0
    for index_in_col in range(0, len(forest)):
        for index_in_row in range(0, len(forest[index_in_col])):
            tree = forest[index_in_col, index_in_row]
            left = forest[index_in_col, :index_in_row]
            right = forest[index_in_col, index_in_row + 1:]
            up = forest[:index_in_col, index_in_row]
            down = forest[index_in_col + 1:, index_in_row]
            score = calc_score(tree, left, right, up, down)
            if score > best_score:
                best_score = score
    return best_score


def calc_score(tree, left, right, up, down):
    if len(left) == 0 or len(right) == 0 or len(up) == 0 or len(down) == 0:
        return 0

    l_i = 0
    r_i = 0
    u_i = 0
    d_i = 0
    for l in reversed(range(0, len(left))):
        l_i += 1
        if left[l] >= tree:
            break
    for r in right:
        r_i += 1
        if r >= tree:
            break
    for u in reversed(range(0, len(up))):
        u_i += 1
        if up[u] >= tree:
            break
    for d in down:
        d_i += 1
        if d >= tree:
            break

    return l_i * r_i * u_i * d_i


if __name__ == '__main__':
    # forest_test = read_input_to_structure('test.txt')
    # print("answer=%d" % find_visible_trees(forest_test))
    #
    # forest_test = read_input_to_structure('input.txt')
    # print("answer=%d" % find_visible_trees(forest_test))

    forest_test = read_input_to_structure('inputs/day8/test.txt')
    print("answer2=%d" % find_best_score(forest_test))

    forest_test = read_input_to_structure('inputs/day8/input.txt')
    print("answer2=%d" % find_best_score(forest_test))

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra


def read_file_to_struct(filename, start):
    with open(filename) as f:
        lines = f.read().splitlines()

    start_v = []
    stop_v = None
    y = len(lines)
    x = len(lines[0].rstrip())
    env = []

    def can_step(p1, p2):
        if ord(p1) - ord(p2) >= -1:
            return 1
        return 0

    for line_i in range(0, len(lines)):
        row = []
        for elev_i in range(0, len(lines[line_i])):
            height = lines[line_i][elev_i]
            if lines[line_i][elev_i] == start:
                start_v.append(line_i * len(lines[0]) + elev_i)
                height = "a"
            elif lines[line_i][elev_i] == "E":
                stop_v = line_i * len(lines[0]) + elev_i
                height = "z"

            row.append(height)
        env.append(row)

    adj_matrix = [[0 for i in range(x*y)] for j in range(x*y)]
    for v_i in range(0, len(env)):
        for v_j in range(0, len(env[v_i])):
            if v_j+1 <= len(env[v_i])-1:
                adj_matrix[v_i * len(env[v_i]) + v_j][v_i * len(env[v_i]) + v_j + 1] = can_step(env[v_i][v_j], env[v_i][v_j+1])
            if v_j-1 >= 0:
                adj_matrix[v_i * len(env[v_i]) + v_j][v_i * len(env[v_i]) + v_j - 1] = can_step(env[v_i][v_j], env[v_i][v_j-1])
            if v_i+1 <= len(env)-1:
                adj_matrix[v_i * len(env[v_i]) + v_j][(v_i+1) * len(env[v_i]) + v_j] = can_step(env[v_i][v_j], env[v_i+1][v_j])
            if v_i-1 >= 0:
                adj_matrix[v_i * len(env[v_i]) + v_j][(v_i-1) * len(env[v_i]) + v_j] = can_step(env[v_i][v_j], env[v_i-1][v_j])

    return adj_matrix, start_v, stop_v, x*y


def task1(filename):
    adj_matrix, start_v, stop_v, v = read_file_to_struct(filename, "S")
    start_v.append(stop_v)
    paths, pr = dijkstra(adj_matrix, indices=start_v, unweighted=True, return_predecessors=True)

    result = get_path(pr, 0, stop_v)

    return len(result)-1


def task2(filename):
    adj_matrix, start_v, stop_v, v = read_file_to_struct(filename, "a")
    start_v.append(stop_v)
    paths, pr = dijkstra(adj_matrix, indices=start_v, unweighted=True, return_predecessors=True)

    short_paths = []
    for i in range(0, len(pr)):
        result = get_path(pr, i, stop_v)
        if len(result) > 1:
            short_paths.append(len(result)-1)

    return sorted(short_paths)[0]


def get_path(pr, i, j):
    path = [j]
    k = j
    while pr[i, k] != -9999:
        path.append(pr[i, k])
        k = pr[i, k]
    return path[::-1]


def day12():
    test1_result = task1('inputs/day12/test.txt')
    print("%d" % test1_result)

    task1_result = task1('inputs/day12/input.txt')
    print("%d" % task1_result)

    test2_result = task2('inputs/day12/test.txt')
    print("%s" % test2_result)

    task2_result = task2('inputs/day12/input.txt')
    print("%s" % task2_result)


if __name__ == '__main__':
    day12()

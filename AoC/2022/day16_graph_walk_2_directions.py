import itertools
import re
from typing import List
from sympy.combinatorics import Permutation, PermutationGroup
from collections import deque
import numpy as np
from scipy.sparse.csgraph import dijkstra


class Volcano:
    index_to_tunnel = None
    tunnels = None
    tunnel_adj_matrix = None

    path_buffer = None
    weight_buffer = None
    time_left_buffer = None
    visited = None

    position = None
    elephant_visited = None
    elephant_position = None

    time_left = None

    ekephant_time_left = 26

    def __init__(self, index_to_tunnel, tunnels, tunnel_graph, time):
        self.index_to_tunnel = index_to_tunnel
        self.tunnels = tunnels
        self.tunnel_adj_matrix = tunnel_graph

        self.time_left = time
        self.path_buffer = []
        self.weight_buffer = []
        self.time_left_buffer = []
        self.visited = [0]
        self.position = 0
        self.elephant_visited = []
        self.elephant_position = 0

    def calc_next_move_for_me_n_eleph(self, valve_order, eleph_path, precision_width, precision_deep):
        if len(self.visited) == len(self.tunnel_adj_matrix):
            return 'Done'
        self.path_buffer = []
        self.weight_buffer = []
        self.calc_best_move(valve_order, [0], self.time_left, precision_width, precision_deep)
        best_weight = max(self.weight_buffer)
        best_weight_index = self.weight_buffer.index(best_weight)
        self.time_left -= (self.distance(self.position, self.path_buffer[best_weight_index][1])+1)
        self.position = self.path_buffer[best_weight_index][1]
        self.visited.append(self.position)
        next_me = self.path_buffer[best_weight_index][1]
        rate_me = self.time_left * self.get_tunnel_data(self.position)['rate']

        self.path_buffer = []
        self.weight_buffer = []
        self.calc_best_move(eleph_path, [0], self.ekephant_time_left, precision_width, precision_deep)
        best_weight = max(self.weight_buffer)
        best_weight_index = self.weight_buffer.index(best_weight)
        self.ekephant_time_left -= (self.distance(self.elephant_position, self.path_buffer[best_weight_index][1]) + 1)
        self.elephant_position = self.path_buffer[best_weight_index][1]
        self.elephant_visited.append(self.elephant_position)

        next_elep = self.path_buffer[best_weight_index][1]
        rate_elep = self.ekephant_time_left * self.get_tunnel_data(self.elephant_position)['rate']

        return next_me, rate_me, next_elep, rate_elep

    def calc_next_move(self, valve_order, precision_width, precision_deep):
        if len(self.visited) == len(self.tunnel_adj_matrix):
            return 'Done'
        self.path_buffer = []
        self.weight_buffer = []
        self.calc_best_move(valve_order, [0], self.time_left, precision_width, precision_deep)
        best_weight = max(self.weight_buffer)
        best_weight_index = self.weight_buffer.index(best_weight)
        self.time_left -= (self.distance(self.position, self.path_buffer[best_weight_index][1])+1)
        self.position = self.path_buffer[best_weight_index][1]
        self.visited.append(self.position)
        return self.path_buffer[best_weight_index][1], self.time_left * self.get_tunnel_data(self.position)['rate']

    def calc_best_move(self, valve_order, weights, time_left, precision_width, precision_deep):
        valves_max_pressure, time_to_move = self.calc_max_pressure_per_valve(valve_order, time_left)
        valves_max_pressure[valve_order[-1]] = 0
        max_pressure = sorted(valves_max_pressure, reverse=True)[:precision_width]

        if precision_deep == 0:
            self.path_buffer.append(valve_order)
            self.weight_buffer.append(sum(weights))
            self.time_left_buffer.append(time_to_move)
            return

        for m in max_pressure:
            _valve_order = valve_order.copy()
            _weights = weights.copy()
            max_pressure_index = valves_max_pressure.index(m)
            time_left = time_to_move[max_pressure_index]
            _valve_order.append(max_pressure_index)
            _weights.append(m)
            self.calc_best_move(_valve_order, _weights, time_left, precision_width, precision_deep-1)

    def calc_max_pressure_per_valve(self, valve_order, time_left):
        start = valve_order[-1]

        def get_path(pr, i, j):
            path = [j]
            k = j
            while pr[i, k] != -9999:
                path.append(pr[i, k])
                k = pr[i, k]
            return path[::-1]

        max_pressure_per_valve = [0] * len(self.tunnel_adj_matrix)
        time_spend_per_valve = [0] * len(self.tunnel_adj_matrix)
        for i in range(0, len(self.tunnel_adj_matrix)):
            if i in valve_order or i in self.visited or i in self.elephant_visited:
                max_pressure_per_valve[i] = 0
                time_spend_per_valve[i] = 0
                continue
            paths, pr = dijkstra(self.tunnel_adj_matrix, indices=[start, i], unweighted=True, return_predecessors=True)
            short_paths = []
            for j in range(0, len(pr)):
                result = get_path(pr, j, i)
                if len(result) > 1:
                    short_paths.append(len(result) - 1)
            if len(short_paths) > 0:
                shortest_path = sorted(short_paths)[0]
            else:
                shortest_path = 0
            max_pressure_per_valve[i] = self.get_tunnel_data(i)['rate'] * (time_left - shortest_path - 1)
            time_spend_per_valve[i] = time_left - shortest_path - 1
        return max_pressure_per_valve, time_spend_per_valve

    def distance(self, start, stop):
        def get_path(pr, i, j):
            path = [j]
            k = j
            while pr[i, k] != -9999:
                path.append(pr[i, k])
                k = pr[i, k]
            return path[::-1]

        paths, pr = dijkstra(self.tunnel_adj_matrix, indices=[start, stop], unweighted=True, return_predecessors=True)
        short_paths = []
        for j in range(0, len(pr)):
            result = get_path(pr, j, stop)
            if len(result) > 1:
                short_paths.append(len(result) - 1)
        if len(short_paths) > 0:
             return sorted(short_paths)[0]
        else:
            return 0

    def get_tunnel_data(self, index):
        return self.tunnels[self.index_to_tunnel[index]]

    def get_non_visited_neighbours(self, visited, node):
        neighbours = []
        for i in range(0, len(self.tunnel_adj_matrix)):
            if self.tunnel_adj_matrix[node][i] is not None and i not in visited:
                neighbours.append(i)
        return neighbours

    def search_next(self, node, visited, weights, time):
        if node not in visited:
            valve_pressure = time * self.get_tunnel_data(node)['rate']
            new_visited = visited.copy()
            new_visited.append(node)
            new_weights = weights.copy()
            new_weights.append(valve_pressure)
            neighbours = self.get_non_visited_neighbours(new_visited, node)
            if len(neighbours) == 0 and node != 0:
                self.paths.append(new_visited)
                self.weights.append(new_weights)
            else:
                for neighbour in neighbours:
                    self.search_next(neighbour, new_visited, new_weights, time-1)


def read_file_to_structure(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    pattern = re.compile("Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)")
    tunnels = dict()
    for line in lines:
        if pattern.match(line):
            m = pattern.match(line)
            tunnel, rate, leads_to = m.group(1), int(m.group(2)), m.group(3)
            leads_to = [t.strip() for t in leads_to.split(',')]
            tunnels[tunnel] = {'name': tunnel, 'rate': rate, 'leads_to': leads_to}

    index_to_tunnel = sorted(tunnels)
    adj_matrix_size = len(tunnels)
    #tunnel_graph = np.full((adj_matrix_size, adj_matrix_size), None)
    tunnel_graph =  [[0 for x in range(adj_matrix_size)] for y in range(adj_matrix_size)]
    for i in range(0, len(index_to_tunnel)):
        tunnels[index_to_tunnel[i]]['index'] = i

    for tunnel in tunnels:
        for next_tunnel in tunnels[tunnel]['leads_to']:
            # tunnel_graph[tunnels[tunnel]['index']][tunnels[next_tunnel]['index']] = tunnels[next_tunnel]['rate']
            tunnel_graph[tunnels[tunnel]['index']][tunnels[next_tunnel]['index']] = 1

    return tunnel_graph, tunnels, index_to_tunnel


def task1(filename):
    tunnel_graph, tunnels, index_to_tunnel = read_file_to_structure(filename)
    volcano = Volcano(index_to_tunnel, tunnels, tunnel_graph, 30)
    next_i = 0
    pressure = 0
    for minute in range(30):
        next_i, rate = volcano.calc_next_move([next_i], 5, 4)
        if next_i == 0:
            break
        tunnel = volcano.get_tunnel_data(next_i)
        print(tunnel['name'])
        print(rate)
        pressure += rate

    return pressure


def task2(filename):
    tunnel_graph, tunnels, index_to_tunnel = read_file_to_structure(filename)
    volcano = Volcano(index_to_tunnel, tunnels, tunnel_graph, 26)
    next_me = 0
    next_eleph = 0
    pressure = 0
    for minute in range(30):
        next_me, rate_me, next_eleph, rate_elep = volcano.calc_next_move_for_me_n_eleph([next_me], [next_eleph], 1, 4)
        if next_me == 0:
            break
        tunnel_me = volcano.get_tunnel_data(next_me)
        tunnel_eleph = volcano.get_tunnel_data(next_eleph)
        print("I move to %s, elephant goes to %s" % (tunnel_me['name'], tunnel_eleph['name']))
        print(rate_me)
        pressure += rate_elep + rate_me

    return pressure


def day16():
    # test1_result = task1('inputs/day16/test.txt')
    # print("%d" % test1_result)
    #
    # task1_result = task1('inputs/day16/input.txt')
    # print("%d" % task1_result)
    #
    test2_result = task2('inputs/day16/test.txt')
    print("%s" % test2_result)
    #
    # task2_result = task2('inputs/day16/input.txt')
    # print("%s" % task2_result)


if __name__ == '__main__':
    day16()

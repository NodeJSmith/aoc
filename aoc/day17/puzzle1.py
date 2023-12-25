import random
import time
from argparse import ArgumentParser
from collections import Counter, defaultdict
from enum import Enum
from heapq import heappop, heappush
from itertools import count
from pathlib import Path
from time import sleep
from typing import Any

import networkx as nx
import numpy as np
from networkx import DiGraph
from networkx.algorithms.shortest_paths.weighted import _weight_function

from aoc_utils import get_data, print_colored_array

parser = ArgumentParser()

parser.add_argument("--test", action="store_true")
parser.add_argument("--print", action="store_true")

args = parser.parse_args()


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


CHOICE_MAP = {
    Direction.UP: [Direction.LEFT, Direction.RIGHT, Direction.UP],
    Direction.DOWN: [Direction.LEFT, Direction.RIGHT, Direction.DOWN],
    Direction.LEFT: [Direction.UP, Direction.DOWN, Direction.LEFT],
    Direction.RIGHT: [Direction.UP, Direction.DOWN, Direction.RIGHT],
}


def point_out_of_bounds(point: tuple[int, int], data: np.ndarray):
    return point[0] < 0 or point[1] < 0 or point[0] >= len(data[0]) or point[1] >= len(data)


def get_path(curnode, parent, explored):
    path = [curnode]
    node = parent
    while node is not None:
        path.append(node)
        node = explored[node]
    return path


def get_heat_loss(
    neighbor: tuple[int, int],
    curr_node: tuple[int, int],
    explored: dict[tuple[int, int], tuple[int, int]],
    data: np.ndarray,
):
    if curr_node is None:
        return 0

    path = get_path(curr_node, explored[curr_node], explored)

    heat_loss = int(data[neighbor])

    for node in path:
        heat_loss += int(data[node])

    return heat_loss


def can_continue(parent: tuple[int, int], curr_node: tuple[int, int], proposed_node: tuple[int, int]) -> bool:
    if not parent:
        return True

    if len(set([parent, curr_node, proposed_node])) < 3:
        return False
    # Determine directions of the last two moves
    last_direction = Direction((proposed_node[1] - curr_node[1], proposed_node[0] - curr_node[0]))
    second_last_direction = Direction((curr_node[1] - parent[1], curr_node[0] - parent[0]))

    # Check if the next move continues in the same direction
    return not (last_direction == second_last_direction)


def my_astar_path(G, source, target, weight="weight", data: np.ndarray = None):
    if source not in G or target not in G:
        msg = f"Either source {source} or target {target} is not in G"
        raise nx.NodeNotFound(msg)

    push = heappush
    pop = heappop
    weight = _weight_function(G, weight)

    G_succ: dict[tuple[int, int], dict] = G._adj  # For speed-up (and works for both directed and undirected graphs)

    # The queue stores priority, node, cost to reach, and parent.
    # Uses Python heapq to keep in priority order.
    # Add a counter to the queue to prevent the underlying heap from
    # attempting to compare the nodes themselves. The hash breaks ties in the
    # priority and is guaranteed unique for all nodes in the graph.
    c = count()
    queue = [(0, next(c), source, 0, None)]

    # Maps enqueued nodes to distance of discovered paths and the
    # computed heuristics to target. We avoid computing the heuristics
    # more than once and inserting the node into the queue too many times.
    enqueued = {}
    # Maps explored nodes to parent closest to the source.
    explored = {}

    reset_cursor = False
    while queue:
        # Pop the smallest item from queue.
        _, __, curnode, dist, parent = pop(queue)

        if curnode == target:
            path = get_path(curnode, parent, explored)
            path.reverse()
            return path

        if curnode in explored:
            # Do not override the parent of starting node
            if explored[curnode] is None:
                continue

            # Skip bad paths that were enqueued before finding a better one
            enqueued_cost = enqueued[curnode]
            if enqueued_cost < dist:
                continue

        explored[curnode] = parent

        if args.print:
            time.sleep(0.1)
            path = get_path(curnode, parent, explored)

            colored_points = {k: "blue" for k in explored}
            colored_points.update({k: "red" for k in path})
            colored_points.update({curnode: "green"})

            print_colored_array(data, None, colored_points, reset_cursor=reset_cursor)
            reset_cursor = True

        for neighbor, _ in G_succ[curnode].items():
            heat_loss = get_heat_loss(neighbor, curnode, explored, data)
            if heat_loss is None:
                continue
            combined_cost = heat_loss  # + dist

            if neighbor in enqueued:
                if enqueued[neighbor] > combined_cost:
                    enqueued[neighbor] = combined_cost
            else:
                enqueued[neighbor] = combined_cost

            if can_continue(parent, curnode, neighbor):
                push(queue, (combined_cost, next(c), neighbor, combined_cost, curnode))

    raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")


def find_shortest_path(graph: DiGraph, data: np.ndarray):
    start_point = (0, 0)
    end_point = (len(data[0]) - 1, len(data) - 1)
    astar_path = my_astar_path(graph, start_point, end_point, data=data)

    for i in astar_path:
        print(i)

    if args.print:
        colored_points = {k: "red" for k in astar_path}
        print_colored_array(data, None, colored_points, reset_cursor=True)

    return len(astar_path) - 1


def convert_grid_to_graph(data: np.ndarray) -> DiGraph:
    graph = DiGraph()

    it = np.nditer(data, flags=["multi_index"])
    for x in it:
        graph.add_node(it.multi_index, weight=int(x))

    reset_cursor = False
    for i in range(len(data[0])):
        for j in range(len(data)):
            curr_node = (i, j)
            edges = []
            for direction in Direction:
                potential_edge = tuple(np.add(curr_node, direction.value))
                if not point_out_of_bounds(potential_edge, data):
                    edges.append(potential_edge)

            for edge in edges:
                weight = graph.nodes[edge]["weight"]
                graph.add_edge(curr_node, edge, weight=weight)

            # if args.print:
            #     time.sleep(0.01)
            #     colored_points = {k: "red" for k in edges}
            #     colored_points[curr_node] = "green"
            #     print_colored_array(data, None, colored_points=colored_points, reset_cursor=reset_cursor)
            #     reset_cursor = True

    return graph


def main(test: bool = None, print_: bool = None):
    if test is not None:
        args.test = test

    if print_ is not None:
        args.print = print_

    curr_dir = Path(__file__).parent.absolute()

    data = get_data(curr_dir, args.test).splitlines()
    data = np.array([list(map(int, line)) for line in data])

    graph = convert_grid_to_graph(data)

    shortest_path = find_shortest_path(graph, data)

    print(f"Shortest path: {shortest_path}")


if __name__ == "__main__":
    main(test=True, print_=True)

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
from attrs import define, field

from aoc_utils import get_data

WORKFLOWS: dict[str, "Workflow"] = {}
ACCEPT = "A"
REJECT = "R"

PATHS = []


@define
class Rule:
    attr: str
    operator: str
    value: int
    destination: str


@define
class Workflow:
    name: str
    default: str
    rules: list[Rule] = field(factory=list, repr=False)

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return self.name


curr_dir = Path(__file__).parent.absolute()

data = get_data(curr_dir, True).splitlines()
workflow_lines: list[str] = []


for line in data:
    if not line:
        break

    workflow_lines.append(line)

for line in workflow_lines:
    print(line)

    workflow_name, rest = line.replace("}", "").split("{")
    rules = rest.split(",")
    default = rules.pop(-1)
    workflow = Workflow(workflow_name, default)
    for r in rules:
        _, _dest = r.split(":")
        _attr = r[0]
        _op = r[1]
        _val = int(r[2 : r.index(":")])

        print(_attr, _op, _val, _dest)
        rule = Rule(_attr, _op, _val, _dest)
        workflow.rules.append(rule)

    WORKFLOWS[workflow_name] = workflow


graph = nx.DiGraph()
red_edges = []
black_edges = []
w_queue = [(WORKFLOWS["in"].name, 0)]
while w_queue:
    curr, layer = w_queue.pop(0)

    if curr in [ACCEPT, REJECT]:
        continue

    workflow = WORKFLOWS[curr]
    destinations = [r.destination for r in workflow.rules] + [workflow.default]
    for dest in destinations:
        graph_layer = -1 * layer
        graph.add_node(curr, layer=graph_layer)
        graph.add_node(dest, layer=(graph_layer - 1))
        graph.add_edge(curr, dest)

        if dest in WORKFLOWS:
            w_queue.append((WORKFLOWS[dest].name, layer + 1))
        else:
            w_queue.append((dest, layer + 1))


# any path that ends at R should be red
# any path that ends at A should be black


def get_colored_edges(graph: nx.DiGraph, start: str, end: str) -> list[tuple[str, str]]:
    colored_edges = []
    for path in nx.all_simple_paths(graph, start, end):
        for i in range(len(path) - 1):
            colored_edges.append((path[i], path[i + 1]))

    return colored_edges


black_edges = get_colored_edges(graph, "in", ACCEPT)
red_edges = get_colored_edges(graph, "in", REJECT)

pos = nx.multipartite_layout(graph, subset_key="layer", align="horizontal")
nx.draw_networkx_nodes(graph, pos, node_size=500)
nx.draw_networkx_labels(graph, pos)

nx.draw_networkx_edges(graph, pos, edgelist=red_edges, edge_color="r", arrows=True)
nx.draw_networkx_edges(graph, pos, edgelist=black_edges, arrows=True)
plt.show()

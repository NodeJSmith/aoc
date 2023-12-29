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
w_queue = [(WORKFLOWS["in"], 0)]
while w_queue:
    workflow, layer = w_queue.pop(0)

    for r in workflow.rules:
        if r.destination not in ["A", "R"]:
            next_dest = WORKFLOWS[r.destination]
            black_edges.append((workflow, next_dest))
            graph.add_edge(workflow, next_dest, layer=layer)
            w_queue.append((WORKFLOWS[r.destination], layer + 1))
        else:
            red_edges.append((workflow, r.destination))
            graph.add_edge(workflow, r.destination, layer=layer)

        if workflow.default not in ["A", "R"]:
            next_dest = WORKFLOWS[workflow.default]
            black_edges.append((workflow, next_dest))
            graph.add_edge(workflow, next_dest, layer=layer)
            w_queue.append((WORKFLOWS[workflow.default], layer + 1))
        else:
            red_edges.append((workflow, workflow.default))
            graph.add_edge(workflow, workflow.default, layer=layer)


for p in PATHS:
    print(p)


# any path that ends at R should be red
# any path that ends at A should be black

# red_edges = [p for p in PATHS if p[1] == "R"]
# black_edges = [p for p in PATHS if p[1] == "A"]
# edge_colours = ["black" if not edge in red_edges else "red" for edge in graph.edges()]


# edge_colours = ['black' if not edge in red_edges else 'red'
#                 for edge in G.edges()]
# black_edges = [edge for edge in G.edges() if edge not in red_edges]


pos = nx.multipartite_layout(graph, subset_key="layer", align="horizontal")
nx.draw_networkx_nodes(graph, pos, node_size=500)
nx.draw_networkx_labels(graph, pos)

nx.draw_networkx_edges(graph, pos, edgelist=red_edges, edge_color="r", arrows=True)
nx.draw_networkx_edges(graph, pos, edgelist=black_edges, arrows=True)
plt.show()

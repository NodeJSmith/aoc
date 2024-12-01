import re
from itertools import repeat
from pathlib import Path

from tqdm import tqdm

TEST = False
curr_dir = Path(__file__).parent


def get_data(test: bool = TEST):
    input_file = get_input_file(test)
    data = input_file.read_text()
    return data


def get_input_file(test: bool = TEST):
    input_file = curr_dir / "test_input" if test else curr_dir / "input"
    return input_file


def advance_node(curr_node, direction, nodes):
    if direction == "L":
        return nodes[curr_node][0]
    elif direction == "R":
        return nodes[curr_node][1]


lines = get_data().splitlines()

directions = lines[0]
lines = lines[2:]

nodes: dict[str, tuple[str, str]] = {}

for line in lines:
    node, node_tuple = line.split(" = ")
    node_tuple = tuple(re.findall(r"(\w+)", node_tuple))

    nodes[node] = node_tuple


current_nodes = [k for k in nodes if k.endswith("A")]
node_steps_map = {}
steps_taken = 0
curr_step = 0

for i in tqdm(repeat(1)):
    # while True:
    for i in range(len(current_nodes)):
        current_nodes[i] = advance_node(current_nodes[i], directions[curr_step], nodes)

    steps_taken += 1
    curr_step += 1

    if all([x.endswith("Z") for x in current_nodes]):
        break

    if curr_step == len(directions):
        curr_step = 0


print(steps_taken)

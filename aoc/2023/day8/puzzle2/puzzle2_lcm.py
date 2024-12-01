import math
import re
from pathlib import Path

import numpy as np

TEST = False
curr_dir = Path(__file__).parent


def get_data(test: bool = TEST):
    input_file = get_input_file(test)
    data = input_file.read_text()
    return data


def get_input_file(test: bool = TEST):
    input_file = curr_dir / "test_input" if test else curr_dir / "input"
    return input_file


lines = get_data().splitlines()

directions = lines[0]
lines = lines[2:]

nodes: dict[str, tuple[str, str]] = {}

for line in lines:
    node, node_tuple = line.split(" = ")
    node_tuple = tuple(re.findall(r"(\w+)", node_tuple))

    nodes[node] = node_tuple


current_nodes = [k for k in nodes if k.endswith("A")]
end_nodes = [k for k in nodes if k.endswith("Z")]
node_steps_map = {}


for curr_node in current_nodes:
    start_node = curr_node

    steps_taken = 0
    current_step = 0
    while True:
        d = directions[current_step]
        if d == "L":
            # print(f"Direction: {d}, moving from {curr_node} to {nodes[curr_node][0]}")
            curr_node = nodes[curr_node][0]
        elif d == "R":
            # print(f"Direction: {d}, moving from {curr_node} to {nodes[curr_node][1]}")
            curr_node = nodes[curr_node][1]

        # print(curr_node)
        steps_taken += 1
        current_step += 1

        if curr_node.endswith("Z"):
            break

        if current_step == len(directions):
            # print("resetting current_step to 0")
            current_step = 0

    node_steps_map[start_node] = {"final_node": curr_node, "steps_taken": steps_taken}
    # print(steps_taken)

node_steps_map = dict(sorted(node_steps_map.items(), key=lambda x: x[1]["final_node"]))

for k, v in node_steps_map.items():
    print(k, v)


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


values = [x["steps_taken"] for x in list(node_steps_map.values())]

for i in range(len(values) - 1):
    values[i + 1] = lcm(values[i], values[i + 1])

print(max(values))


print(np.lcm.reduce(values))

import re
from pathlib import Path

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


curr_node = "AAA"
target_node = "ZZZ"

print(f"starting_node: {curr_node}")
print(f"target_node: {target_node}")

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

    if curr_node == target_node:
        break

    if current_step == len(directions):
        # print("resetting current_step to 0")
        current_step = 0


print(steps_taken)

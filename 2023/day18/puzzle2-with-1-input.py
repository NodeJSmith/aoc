from pathlib import Path

import numpy as np
from aoc_utils import Direction, get_data

colored_points = {}
FILL_CHAR = " "
MOVE_MAP = {"D": Direction.DOWN, "U": Direction.UP, "L": Direction.LEFT, "R": Direction.RIGHT}


def calculate_area(vertices):
    x = np.array([vertex[0] for vertex in vertices])
    y = np.array([vertex[1] for vertex in vertices])
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def segments_to_ordered_vertices(segments):
    # Extract the first point from each segment
    # The last point of the last segment should connect back to the first point of the first segment
    vertices = [segment[0] for segment in segments]
    vertices.append(segments[-1][1])  # Adding the last vertex to close the loop
    return vertices


curr_dir = Path(__file__).parent.absolute()

data = get_data(curr_dir, False).splitlines()


moves = []
start_point = (0, 0)
total_count = 0
for line in data:
    direction, value, rest = line.split()
    end_point = tuple(np.add(start_point, np.multiply(MOVE_MAP[direction].value, int(value))))
    total_count += int(value)
    moves.append((start_point, end_point))
    start_point = end_point

vertices = segments_to_ordered_vertices(moves)
area = calculate_area(vertices)

print(area + (total_count // 2) + 1)

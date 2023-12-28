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


directions = []

for line in data:
    direction, value, rest = line.split()
    hex_color = rest.replace("(", "").replace(")", "").replace("#", "")
    actual_value = int(hex_color[:-1], 16)
    match hex_color[-1]:
        case "0":
            direction = "R"
        case "1":
            direction = "D"
        case "2":
            direction = "L"
        case "3":
            direction = "U"
        case _:
            raise ValueError(f"Invalid hex color: {hex_color}")

    directions.append((direction, actual_value, hex_color))


moves = []
start_point = (0, 0)
total_count = 0
for direction, value, hex_color in directions:
    end_point = tuple(np.add(start_point, np.multiply(MOVE_MAP[direction].value, value)))
    total_count += value
    moves.append((start_point, end_point))
    start_point = end_point

vertices = segments_to_ordered_vertices(moves)
area = calculate_area(vertices)

# have to divide total_count by 2
# some guy online explained the actual reason but i found out
# by not including total count, which was off by X
# and then by including total_count which was off by X in the other direction
# half of the total count worked, except we were still off by one
# which the guy online explained also but, again, I forgot

print(area + (total_count // 2) + 1)

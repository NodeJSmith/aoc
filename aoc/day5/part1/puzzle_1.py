from pathlib import Path
from typing import NamedTuple

TEST = False
curr_dir = Path(__file__).parent


class LookupTuple(NamedTuple):
    source_start: int
    dest_start: int
    length: int


SEED_SOIL_MAP: list[LookupTuple] = []
SOIL_FERTILIZER_MAP: list[LookupTuple] = []
FERTILIZER_WATER_MAP: list[LookupTuple] = []
WATER_LIGHT_MAP: list[LookupTuple] = []
LIGHT_TEMP_MAP: list[LookupTuple] = []
TEMP_HUMIDITY_MAP: list[LookupTuple] = []
HUMIDITY_LOCATION_MAP: list[LookupTuple] = []

STRING_TO_MAP = {
    ("seed", "soil"): SEED_SOIL_MAP,
    ("soil", "fertilizer"): SOIL_FERTILIZER_MAP,
    ("fertilizer", "water"): FERTILIZER_WATER_MAP,
    ("water", "light"): WATER_LIGHT_MAP,
    ("light", "temperature"): LIGHT_TEMP_MAP,
    ("temperature", "humidity"): TEMP_HUMIDITY_MAP,
    ("humidity", "location"): HUMIDITY_LOCATION_MAP,
}


def get_dest_value(source_value: int, lookup_key: tuple[str, str]):
    lookup_map = STRING_TO_MAP[lookup_key]
    for lookup_tuple in lookup_map:
        if source_value >= lookup_tuple.source_start and source_value < lookup_tuple.source_start + lookup_tuple.length:
            return lookup_tuple.dest_start + (source_value - lookup_tuple.source_start)
    return source_value


def process_line(line: str, entries: list[str]):
    categories = line.replace(" map:", "").split("-to-")
    source_category = categories[0]
    dest_category = categories[1]

    curr_map = STRING_TO_MAP[(source_category, dest_category)]

    for v in entries:
        parts = list(map(int, v.split()))
        dest_range_start = parts[0]
        source_range_start = parts[1]
        length = parts[2]

        curr_map.append(
            LookupTuple(
                source_start=source_range_start,
                dest_start=dest_range_start,
                length=length,
            )
        )

        # for i in range(length):
        #     curr_map[source_range_start + i] = dest_range_start + i


def get_data(test: bool = TEST):
    input_file = curr_dir / "test_input" if test else curr_dir / "input"
    data = input_file.read_text()
    return data


def get_seeds(seed_line):
    seeds = list(map(int, seed_line.replace("seeds: ", "").split()))
    return seeds


def populate_maps(lines):
    maps = {}
    curr_list = []
    key = ""
    for line in lines:
        if not line and key:
            maps[key] = curr_list
            continue
        if "map" in line:
            key = line
            maps[key] = curr_list
            curr_list = []
            continue

        if key:
            curr_list.append(line)

    maps[key] = curr_list
    print("finished parsing lines")

    for k, v in maps.items():
        process_line(line=k, entries=v)

    print("finished populating maps")


def populate_seed_path():
    seed_path: dict[int, dict[str, int]] = {seed: {"seed": seed} for seed in seeds}
    for seed in seeds:
        curr_val = seed
        for k in STRING_TO_MAP:
            curr_val = get_dest_value(curr_val, k)
            print(f"Seed: {seed} - got {curr_val} from {k[0]} to {k[1]}")
            seed_path[seed][k[1]] = curr_val

    return seed_path


lines = get_data().splitlines()


seeds = get_seeds(lines[0])
populate_maps(lines)
seed_path = populate_seed_path()


for k, v in seed_path.items():
    print("->".join(list(map(str, v.values()))))

location_vals = []
for k, v in seed_path.items():
    location_vals.append(v["location"])

print(min(location_vals))

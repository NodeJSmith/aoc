import asyncio
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

from tqdm.asyncio import tqdm

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


@lru_cache
async def get_dest_value(source_value: int, lookup_key: tuple[str, str]):
    lookup_map = STRING_TO_MAP[lookup_key]
    retval = None
    for lookup_tuple in lookup_map:
        if source_value >= lookup_tuple.source_start and source_value < lookup_tuple.source_start + lookup_tuple.length:
            retval = lookup_tuple.dest_start + (source_value - lookup_tuple.source_start)

    if not retval:
        retval = source_value

    # print(f"source_value: {source_value}, lookup_key: {lookup_key}, retval: {retval}")
    return retval


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


def get_data(test: bool = TEST):
    input_file = curr_dir / "test_input" if test else curr_dir / "input"
    data = input_file.read_text()
    return data


def get_seed_tuples(seed_line) -> list[tuple[int, int]]:
    seeds = list(map(int, seed_line.replace("seeds: ", "").split()))
    # actual_seeds: list[int] = []
    seed_tuples: list[tuple[int, int]] = []
    for i in range(0, len(seeds), 2):
        seed_start = seeds[i]
        num_seeds = seeds[i + 1]
        seed_tuples.append((seed_start, num_seeds))

    return seed_tuples


async def async_range(start, stop, step=1):
    i = start
    while i < stop:
        yield i
        i += step
        await asyncio.sleep(0)  # This allows other tasks to run


async def generate_seeds(seed_tuple: tuple[int, int]):
    seed_start, num_seeds = seed_tuple
    stop = seed_start + num_seeds
    async for seed in tqdm(async_range(seed_start, stop), total=num_seeds):
        yield seed


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


async def get_min_seed_location(seeds):
    min_seed_location: int = None
    async for seed in seeds:
        curr_val = seed
        for k in STRING_TO_MAP:
            curr_val = await get_dest_value(curr_val, k)
        if not min_seed_location or curr_val < min_seed_location:
            min_seed_location = curr_val

    return min_seed_location


async def get_min_location_by_seed_tuple(seed_tuple: tuple[int, int]):
    # print(f"Getting min location for {seed_tuple}")
    seeds = generate_seeds(seed_tuple)
    min_seed_location = await get_min_seed_location(seeds)
    print(f"Finished getting min location for {seed_tuple}: {min_seed_location}")
    return min_seed_location


async def get_min_location(seed_line):
    seed_tuples = get_seed_tuples(seed_line)
    futures = []
    for seed_tuple in seed_tuples:
        futures.append(get_min_location_by_seed_tuple(seed_tuple))
    results = await asyncio.gather(*futures)
    return min(results)


def main():
    lines = get_data().splitlines()
    seed_line = lines[0]

    populate_maps(lines)

    min_location = asyncio.run(get_min_location(seed_line))

    print(min_location)

    # min_location = get_min_seed_location(seed_tuples)

    # print(min_location)


if __name__ == "__main__":
    main()

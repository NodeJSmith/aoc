import argparse
import re
from pathlib import Path

import attrs

DAY_PART_PATTERN = re.compile("d(\d+)p(\d+)")


@attrs.define
class Args:
    test: bool


@attrs.define
class AocData:
    curr_dir: Path
    args: Args = attrs.field(init=False)

    def __attrs_post_init__(self):
        parser = argparse.ArgumentParser(description=f"Day {self.day} Part {self.part}")
        parser.add_argument(
            "--test", "-t", help="Use the test input", action="store_true"
        )

        args = parser.parse_args()
        self.args = Args(test=args.test)

    @property
    def day(self):
        return int(DAY_PART_PATTERN.match(self.curr_dir.name).group(1))

    @property
    def part(self):
        return int(DAY_PART_PATTERN.match(self.curr_dir.name).group(2))

    @property
    def test(self):
        return self.args.test

    @property
    def input_file(self):
        return self.curr_dir / ("input" if not self.test else "test_input")

    @property
    def data(self):
        return self.input_file.read_text()

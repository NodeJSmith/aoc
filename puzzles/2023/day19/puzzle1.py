import re
from collections import defaultdict
from pathlib import Path

from attrs import define, field

from aoc_utils import get_data

WORKFLOWS: dict[str, "Workflow"] = {}
RESULTS: dict[str, list["Part"]] = defaultdict(list)
ACCEPT = "A"
REJECT = "R"


@define
class Part:
    x: int = field(converter=int)
    m: int = field(converter=int)
    a: int = field(converter=int)
    s: int = field(converter=int)

    @property
    def total(self) -> int:
        return self.x + self.m + self.a + self.s


@define
class Rule:
    attr: str
    operator: str
    value: int
    destination: str

    def compare(self, item: Part) -> bool:
        if self.operator == ">":
            return item.__getattribute__(self.attr) > self.value
        if self.operator == "<":
            return item.__getattribute__(self.attr) < self.value
        if self.operator == "=":
            return item.__getattribute__(self.attr) == self.value
        if self.operator == "!":
            return item.__getattribute__(self.attr) != self.value


@define
class Workflow:
    name: str
    default: str
    rules: list[Rule] = field(factory=list)

    def run(self, item: "Part"):
        for r in self.rules:
            if r.compare(item):
                return r.destination

        return self.default


curr_dir = Path(__file__).parent.absolute()

data = get_data(curr_dir, False).splitlines()
workflow_lines: list[str] = []
part_lines: list[str] = []


parts: list[Part] = []
active_list = workflow_lines
for line in data:
    if not line:
        active_list = part_lines
        continue

    active_list.append(line)


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


for line in part_lines:
    print(line)

    x, m, a, s = re.findall(r"\d+", line)
    part = Part(x, m, a, s)
    parts.append(part)


for part in parts:
    workflow = WORKFLOWS["in"]
    while True:
        result = workflow.run(part)
        if result == ACCEPT:
            RESULTS[ACCEPT].append(part)
            break
        elif result == REJECT:
            RESULTS[REJECT].append(part)
            break
        else:
            workflow = WORKFLOWS[result]

    RESULTS[workflow.name].append(part)


total = sum(p.total for p in RESULTS[ACCEPT])
print(total)

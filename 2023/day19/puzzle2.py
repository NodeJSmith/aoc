# i get by with a little help from my friends
# https://github.com/stefanoandroni/advent-of-code/blob/master/2023/day-19/part-2/main.py

from copy import deepcopy
from pathlib import Path

from attrs import define, field

from aoc_utils import get_data

WORKFLOWS: dict[str, "Workflow"] = {}

ACCEPT = "A"
REJECT = "R"
RULE_MIN = 1
RULE_MAX = 4000


@define
class DefaultRule:
    destination: str


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
    rules: list[Rule] = field(factory=list)


curr_dir = Path(__file__).parent.absolute()

data = get_data(curr_dir, False).splitlines()
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

    workflow.rules.append(DefaultRule(default))

    WORKFLOWS[workflow_name] = workflow


def get_product(range_dict: dict[str, tuple[int, int]]) -> int:
    combo = 1
    for _, v in range_dict.items():
        start, end = v
        combo *= end - start + 1
    return combo


start_ranges = {_: (RULE_MIN, RULE_MAX) for _ in ["x", "m", "a", "s"]}


def get_combos(curr_range: dict[str, tuple[int, int]], workflow_name: str) -> int:
    total = 0

    if workflow_name == REJECT:
        return 0

    if workflow_name == ACCEPT:
        total += get_product(curr_range)
        return total

    curr_workflow = WORKFLOWS[workflow_name]

    for rule in curr_workflow.rules:
        if isinstance(rule, DefaultRule):
            total += get_combos(curr_range, rule.destination)
            continue

        attr = rule.attr
        curr_start, curr_stop = curr_range[attr]

        # does the same as below but less readable
        # accept_range = rule.range_accepted(curr_range[attr])
        if rule.operator == "<":
            # true_portion = accept_range
            true_portion = (curr_start, rule.value - 1)
            false_portion = (rule.value, curr_stop)
        else:
            # true_portion = accept_range
            true_portion = (rule.value + 1, curr_stop)
            false_portion = (curr_start, rule.value)

        assert true_portion[0] <= true_portion[-1], f"True portion is invalid: {true_portion}"
        assert false_portion[0] <= false_portion[-1], f"False portion is invalid: {false_portion}"

        # pass a copy of the range so we don't modify the original
        copy_range = deepcopy(curr_range)
        copy_range[attr] = true_portion
        total += get_combos(copy_range, rule.destination)

        # the above lines followed the true portion of the rule
        # so now we modify in place to set the false portion
        curr_range[attr] = false_portion

    print(f"Total: {total:,}")
    return total


total_combo = get_combos(start_ranges, "in")


print(total_combo)

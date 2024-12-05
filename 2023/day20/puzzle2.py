from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import ClassVar

from aoc_utils import get_data
from tqdm import tqdm

TEST = False
PRINT = False


class EnumHelper:
    @classmethod
    def names(cls):
        return [member.name for member in cls.__members__.values()]

    @classmethod
    def values(cls):
        return [member.value for member in cls.__members__.values()]


class Pulse(EnumHelper, Enum):
    LO = 0
    HI = 1


class State(EnumHelper, Enum):
    ON = 1
    OFF = 0


class ModuleType(EnumHelper, Enum):
    FLIP_FLOP = "%"
    CONJUNCTION = "&"
    BROADCASTER = "broadcaster"


def get_clean_name(name: str) -> str:
    if name[0] in ModuleType.values():
        return name[1:]
    return name


class Module:
    all_targets: ClassVar[set[str]] = set()
    targeted_by: ClassVar[dict[str, list[str]]] = defaultdict(list)

    def __init__(self, name, targets: list[str]):
        self.name = name
        self.targets = targets

        self.all_targets.update(targets)
        for target in targets:
            self.targeted_by[target].append(self.clean_name)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.targets})"

    def receive_pulse(self, input_module: str, pulse: Pulse) -> Pulse | None:
        if not PRINT:
            return
        print(f"{get_clean_name(input_module)} -{pulse.name} -> {self.clean_name}")

    @property
    def clean_name(self):
        return get_clean_name(self.name)

    @classmethod
    def create(cls, name, targets: list[str]):
        if name[0] == ModuleType.FLIP_FLOP.value:
            return FlipFlopModule(name, targets)
        if name[0] == ModuleType.CONJUNCTION.value:
            return ConjunctionModule(name, targets)
        if name == "broadcaster":
            return BroadcasterModule(name, targets)
        return Module(name, targets)


class FlipFlopModule(Module):
    def __init__(self, name, targets: list[str]):
        super().__init__(name, targets)
        self.state = State.OFF

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.targets}, {self.state})"

    def receive_pulse(self, input_module: str, pulse: Pulse) -> Pulse | None:
        super().receive_pulse(input_module, pulse)
        if pulse == Pulse.HI:
            return None

        initial_state = self.state
        self.state = State(not self.state.value)

        if initial_state == State.OFF:
            return Pulse.HI
        return Pulse.LO


class ConjunctionModule(Module):
    def __init__(self, name, targets: list[str]):
        super().__init__(name, targets)
        self.inputs: dict[str, Pulse] = {}

    def set_default_inputs(self):
        self.inputs: dict[str, Pulse] = {x: Pulse.LO for x in self.targeted_by[self.clean_name]}

    def receive_pulse(self, input_module: str, pulse: Pulse) -> Pulse:
        super().receive_pulse(input_module, pulse)
        self.inputs[input_module] = pulse

        if all(x == Pulse.HI for x in self.inputs.values()):
            return Pulse.LO

        return Pulse.HI


class BroadcasterModule(Module):
    def receive_pulse(self, input_module: str = "button", pulse: Pulse = Pulse.LO) -> Pulse:
        super().receive_pulse(input_module, pulse)
        return Pulse.LO


def get_modules():
    modules = {}
    curr_dir = Path(__file__).parent.absolute()

    data = get_data(curr_dir, TEST).splitlines()

    for line in data:
        source_module, *rest = line.split(" -> ")
        targets = rest[0].split(", ")
        module = Module.create(source_module, targets)
        modules[module.clean_name] = module

    missing_modules = Module.all_targets - set(modules.keys())

    for mm in missing_modules:
        if mm == "broadcaster":
            continue
        modules[mm] = Module.create(mm, [])

    for module in modules.values():
        if isinstance(module, ConjunctionModule):
            module.set_default_inputs()

    return modules


def generator():
    while True:
        yield


def start():
    modules = get_modules()

    broadcaster = modules.pop("broadcaster")
    pulse_count: dict[str, int] = defaultdict(int)
    i = 0
    for _ in tqdm(generator()):
        rx_count = {Pulse.LO.name: 0, Pulse.HI.name: 0}
        if PRINT:
            print(f"Press {i+1}")
        queue: list[tuple[Module, str, Pulse]] = [(broadcaster, "button", Pulse.LO)]
        while queue:
            target, input_module, pulse = queue.pop(0)
            if target.clean_name == "rx":
                rx_count[pulse.name] += 1
            pulse_count[pulse.name] += 1

            if PRINT:
                print("\t", end="")
            output_pulse = target.receive_pulse(input_module, pulse)
            if output_pulse is None:
                continue

            for target_name in target.targets:
                queue.append((modules[target_name], target.clean_name, output_pulse))

        if rx_count[Pulse.LO.name] == 1 and rx_count[Pulse.HI.name] == 0:
            print(f"Raw i: {i}")
            print(f"Press count: {i+1}")
            print(f"RX count: {rx_count}")

            break

        i += 1

        if i % 1_000_000 == 0:
            print(f"current i: {i}")


if __name__ == "__main__":
    pulse_count = start()


# 6_222_222 is too low

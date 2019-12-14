from __future__ import annotations
import argparse
import math
import re
from typing import List, Dict, NamedTuple

pattern = re.compile(r"(\d+) ([A-Z]+)")


class Chemical(NamedTuple):
    quantity: int
    name: str

    def __eq__(self, other):
        if not isinstance(other, Chemical):
            return False
        return self.name == other.name


def sol1(data: str) -> int:
    reactions: Dict[Chemical, List[Chemical]] = {}
    for line in data.split('\n'):
        if line == "":
            continue
        chemicals = pattern.findall(line)
        output_chemical = Chemical(int(chemicals[-1][0]), chemicals[-1][1])
        reactions[output_chemical] = [Chemical(int(chemical[0]), chemical[1]) for chemical in chemicals[:-1]]
    fuel = Chemical(1, 'FUEL')
    fuel_chemicals: List[Chemical] = [fuel]
    leftovers: Dict[str, int] = {}
    ores: int = 0
    while fuel_chemicals:
        chemical = fuel_chemicals.pop()
        if chemical.name == "ORE":
            ores += chemical.quantity
            continue
        chemical = update_leftovers(chemical, leftovers)
        if chemical.quantity == 0:
            continue
        new_chemical = [c for c in reactions.keys() if chemical.name == c.name][0]
        multiplier = math.ceil(chemical.quantity / new_chemical.quantity)
        leftover_q = (new_chemical.quantity * multiplier) - chemical.quantity
        if leftover_q != 0:
            leftovers[new_chemical.name] = leftover_q
        new_chemicals = [Chemical(multiplier * ch.quantity, ch.name) for ch in reactions[new_chemical]]
        for new_c in new_chemicals:
            new_c = update_leftovers(new_c, leftovers)
            if new_c.quantity == 0:
                continue
            if new_c in fuel_chemicals:
                index = fuel_chemicals.index(new_c)
                old_q = fuel_chemicals[index].quantity
                fuel_chemicals[index] = fuel_chemicals[index]._replace(quantity=old_q + new_c.quantity)
            else:
                fuel_chemicals.insert(0, new_c)
    return ores


def update_leftovers(chemical: Chemical, leftovers: Dict[str, int]):
    if chemical.name in leftovers:
        min_quantity = min(leftovers[chemical.name], chemical.quantity)
        if min_quantity == leftovers[chemical.name]:
            del leftovers[chemical.name]
        else:
            leftovers[chemical.name] -= min_quantity
        return chemical._replace(quantity=chemical.quantity - min_quantity)
    return chemical


def sol2(data: str) -> int:
    reactions: Dict[Chemical, List[Chemical]] = {}
    for line in data.split('\n'):
        if line == "":
            continue
        chemicals = pattern.findall(line)
        output_chemical = Chemical(int(chemicals[-1][0]), chemicals[-1][1])
        reactions[output_chemical] = [Chemical(int(chemical[0]), chemical[1]) for chemical in chemicals[:-1]]
    leftovers: Dict[str, int] = {}
    ores: int = 0
    fuel_counter: int = 0
    dummy_fuel_counter: int = 0
    coarse_counter: int = 10_000
    while ores < 1_000_000_000_000:
        fuel = Chemical(coarse_counter, 'FUEL')
        fuel_chemicals: List[Chemical] = [fuel]
        ores += get_amount_of_ores(fuel_chemicals, leftovers, reactions)
        dummy_fuel_counter += coarse_counter
    dummy_fuel_counter -= coarse_counter

    leftovers: Dict[str, int] = {}
    ores: int = 0

    while fuel_counter < dummy_fuel_counter:
        fuel = Chemical(coarse_counter, 'FUEL')
        fuel_chemicals: List[Chemical] = [fuel]
        ores += get_amount_of_ores(fuel_chemicals, leftovers, reactions)
        fuel_counter += coarse_counter

    while ores < 1_000_000_000_000:
        fuel = Chemical(1, 'FUEL')
        fuel_chemicals: List[Chemical] = [fuel]
        ores += get_amount_of_ores(fuel_chemicals, leftovers, reactions)
        fuel_counter += 1
    return fuel_counter - 1


def get_amount_of_ores(fuel_chemicals, leftovers, reactions):
    ores = 0
    while fuel_chemicals:
        chemical = fuel_chemicals.pop()
        if chemical.name == "ORE":
            ores += chemical.quantity
            continue
        chemical = update_leftovers(chemical, leftovers)
        if chemical.quantity == 0:
            continue
        new_chemical = [c for c in reactions.keys() if chemical.name == c.name][0]
        multiplier = math.ceil(chemical.quantity / new_chemical.quantity)
        leftover_q = (new_chemical.quantity * multiplier) - chemical.quantity
        if leftover_q != 0:
            leftovers[new_chemical.name] = leftover_q
        new_chemicals = [Chemical(multiplier * ch.quantity, ch.name) for ch in reactions[new_chemical]]
        for new_c in new_chemicals:
            new_c = update_leftovers(new_c, leftovers)
            if new_c.quantity == 0:
                continue
            if new_c in fuel_chemicals:
                index = fuel_chemicals.index(new_c)
                old_q = fuel_chemicals[index].quantity
                fuel_chemicals[index] = fuel_chemicals[index]._replace(quantity=old_q + new_c.quantity)
            else:
                fuel_chemicals.insert(0, new_c)
    return ores


def get_input(filename: str) -> str:
    with open(filename) as f:
        data = f.read()
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='input.txt')
    args = parser.parse_args()
    data = get_input(args.filename)
    print(sol1(data))
    print(sol2(data))
    return 0


if __name__ == '__main__':
    exit(main())

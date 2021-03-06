from __future__ import annotations
import argparse
import math
import re
from typing import List, Dict, Any, Optional, NamedTuple, Tuple


class Position:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def get_energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def apply_velocity(self, velocity: Velocity):
        self.x += velocity.x
        self.y += velocity.y
        self.z += velocity.z

    def apply_gravity(self, moon: Position) -> Tuple[int, int, int]:
        x = 0
        y = 0
        z = 0
        if self.x > moon.x:
            x -= 1
        elif self.x < moon.x:
            x += 1

        if self.y > moon.y:
            y -= 1
        elif self.y < moon.y:
            y += 1

        if self.z > moon.z:
            z -= 1
        elif self.z < moon.z:
            z += 1

        return x, y, z


class Velocity:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def get_energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def apply_gravity(self, x: int, y: int, z: int):
        self.x += x
        self.y += y
        self.z += z


class Moon:
    def __init__(self, position, velocity):
        self.position: Position = position
        self.velocity: Velocity = velocity

    def get_tot_energy(self) -> int:
        return self.position.get_energy() * self.velocity.get_energy()

    def apply_gravity(self, *moons: Moon):
        for moon in moons:
            x, y, z = self.position.apply_gravity(moon.position)
            self.velocity.apply_gravity(x, y, z)

    def apply_velocity(self):
        self.position.apply_velocity(self.velocity)


def sol1(data: str, steps) -> int:
    pattern = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
    moons = []
    data.strip()
    for line in data.split('\n'):
        if line == '':
            continue
        m = pattern.match(line)
        p = Position(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        moon = Moon(p, Velocity(0, 0, 0))
        moons.append(moon)

    for i in range(steps):
        for moon in moons:
            moon.apply_gravity(*moons)
        for moon in moons:
            moon.apply_velocity()
    return sum([moon.get_tot_energy() for moon in moons])


def sol2(data: str) -> int:
    pattern = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
    moons: List[Moon] = []
    data.strip()
    for line in data.split('\n'):
        if line == '':
            continue
        m = pattern.match(line)
        p = Position(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        moon = Moon(p, Velocity(0, 0, 0))
        moons.append(moon)
    x_cycle = None
    y_cycle = None
    z_cycle = None
    i = 0
    while x_cycle is None or y_cycle is None or z_cycle is None:
        for moon in moons:
            moon.apply_gravity(*moons)
        for moon in moons:
            moon.apply_velocity()
        x, y, z = False, False, False
        for moon in moons:
            if x_cycle is None and moon.velocity.x != 0:
                x = True
            if y_cycle is None and moon.velocity.y != 0:
                y = True
            if z_cycle is None and moon.velocity.z != 0:
                z = True
        if x_cycle is None and not x:
            x_cycle = i + 1
        if y_cycle is None and not y:
            y_cycle = i + 1
        if z_cycle is None and not z:
            z_cycle = i + 1
        i += 1
    return lcm([x_cycle, y_cycle, z_cycle]) * 2


def lcm(a: List[int]) -> int:
    ret = a[0]
    for i in a[1:]:
        ret = ret * i // math.gcd(ret, i)
    return ret


def get_input(filename: str) -> str:
    with open(filename) as f:
        data = f.read()
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='input.txt')
    args = parser.parse_args()
    data = get_input(args.filename)
    print(sol1(data, 1000))
    print(sol2(data))
    return 0


if __name__ == '__main__':
    exit(main())

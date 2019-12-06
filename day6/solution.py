import argparse
from typing import List, Any, Dict, Tuple


def get_input(filename: str) -> List[str]:
    with open(filename) as f:
        lines = f.readlines()
    return [line.strip() for line in lines]


class Node:
    def __init__(self, name: str, prev: Any = None):
        self.name = name
        self.prev = prev
        self.orbits_around_me = []

    def add_orbit(self, node: Any):
        self.orbits_around_me.append(node)


def fill_nodes(data: List[str]) -> Dict[str, Node]:
    nodes: Dict[str, Node] = dict()
    for orbit in data:
        obj_a, obj_b = orbit.split(")")
        if obj_a not in nodes:
            nodes[obj_a] = Node(obj_a)
        if obj_b not in nodes:
            nodes[obj_b] = Node(obj_b, nodes[obj_a])
        else:
            nodes[obj_b].prev = nodes[obj_a]
        nodes[obj_a].add_orbit(nodes[obj_b])
    return nodes


def sol1(data: List[str]) -> int:
    nodes = fill_nodes(data)
    node_list: List[Tuple[Node, int]] = [(nodes["COM"], 0)]
    retval = 0
    while node_list:
        node, val = node_list.pop(0)
        retval += val
        node_list.extend([(n, val+1) for n in node.orbits_around_me])
    return retval


def sol2(data: List[str]) -> int:
    nodes = fill_nodes(data)
    node_list: List[Tuple[Node, int]] = [(nodes["YOU"], -1)]
    while node_list:
        node, val = node_list.pop(0)
        if node.name == "SAN":
            return val - 1
        nodes.pop(node.name)
        node_list.extend([(n, val+1) for n in [node.prev] + node.orbits_around_me if n is not None and n.name in nodes])


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

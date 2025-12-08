import heapq
import sys
from collections import defaultdict
from typing import Iterable, Tuple
from heapq import nsmallest, nlargest
from itertools import combinations


def parse_input(input_: Iterable[str]) -> Iterable[Tuple[int, int, int]]:
    return ((int(x), int(y), int(z)) for x, y, z in (row.strip().split(',') for row in input_))


def dist3(p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> int:
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2


def part1(input_: Iterable[str]) -> int:
    adjacent_map = defaultdict(list)
    for _, p1, p2 in nsmallest(1000, ((dist3(p1, p2), p1, p2) for p1, p2 in combinations(parse_input(input_), 2))):
        adjacent_map[p1].append(p2)
        adjacent_map[p2].append(p1)

    sizes = []

    while adjacent_map:
        p, adjacent = adjacent_map.popitem()
        cluster = {p, *adjacent}
        queue = list(adjacent)
        while queue:
            p = queue.pop()
            for p1 in adjacent_map.pop(p):
                if p1 not in cluster:
                    cluster.add(p1)
                    queue.append(p1)
        sizes.append(len(cluster))

    s1, s2, s3 = nlargest(3, sizes)
    return s1 * s2 * s3


def part2(input_: Iterable[str]) -> int:
    edges = list((dist3(p1, p2), p1, p2) for p1, p2 in combinations(parse_input(input_), 2))
    heapq.heapify(edges)

    cluster_map = dict()

    clusters = dict()
    n_clusters = 0

    while edges:
        dist, p1, p2 = heapq.heappop(edges)
        if p1 not in cluster_map and p2 not in cluster_map:
            cluster_no = len(cluster_map)
            cluster_map[p1] = cluster_map[p2] = cluster_no
            clusters[cluster_no] = {p1, p2}
            n_clusters += 1
        elif p1 not in cluster_map:
            cluster_map[p1] = cluster_map[p2]
            clusters[cluster_map[p2]].add(p1)
        elif p2 not in cluster_map:
            cluster_map[p2] = cluster_map[p1]
            clusters[cluster_map[p1]].add(p2)
        else:
            cluster1, cluster2 = clusters[cluster_map[p1]], clusters[cluster_map[p2]]
            if cluster1 is not cluster2:
                cluster_no = cluster_map[p1]
                cluster1.update(cluster2)
                for p in cluster2:
                    cluster_map[p] = cluster_no
                n_clusters -= 1
        if n_clusters == 1 and len(cluster_map) == 1000:
            return p1[0] * p2[0]
    raise AssertionError("oops")


if __name__ == '__main__':
    input_ = tuple(sys.stdin)
    print(part1(input_))
    print(part2(input_))

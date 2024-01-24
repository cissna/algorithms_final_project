"""All of these functions should input a list of nodes and output a graph"""
import math
import random
import sys

import numpy as np
from typing import List, Tuple, Dict
from helper_functions import sum_list_of_lists, switch_coordinates_in_list_of_pairs, globe_distance

Coordinate = Tuple[float, float]
Graph = List[Dict[Coordinate, Coordinate]]


def sort_population(population: List[Graph]) -> None:
    """Sorts population and list of indices dicts in tandem"""
    # this would be in helper_functions.py, but it caused a circular import
    population.sort(key=lambda x: objective_function(x))


def arbitrary_graph(nodes: List[Coordinate], randomize=False) -> Graph:
    """Constructs the simplest, arbitrary graph from a set of nodes.
    If randomize=True, it becomes a completely random graph"""
    if randomize:
        nodes = nodes.copy()
        random.shuffle(nodes)
    d1 = {nodes[-1]: nodes[0]}
    d2 = {nodes[0]: nodes[-1]}
    for i in range(len(nodes) - 1):
        d1[nodes[i]] = nodes[i + 1]
        d2[nodes[i + 1]] = nodes[i]
    return [d1, d2]


def greedy_algorithm(nodes: List[Coordinate], first_node=True) -> Graph:
    """Starts at some node, then greedily chooses the closest node until there are none left,
    at which point the first and last nodes are connected.
    starting_node_in_middle=True is self-explanatory, if it's False, it chooses a node in one of the corners,
    dependent on which of the 4 arrangements of -/+ this tuple is in: ({-}10000000, {-}10000000)"""
    nodes = nodes.copy()
    if first_node is True:
        longs = [node[0] for node in nodes]
        lats = [node[1] for node in nodes]
        first_node = min(nodes, key=lambda x: math.dist(x, ((max(longs) + min(longs)) / 2, (max(lats) + min(lats)) / 2)))
    elif first_node is False:
        first_node = min(nodes, key=lambda x: math.dist(x, (10000000, 10000000)))
    elif first_node is None:
        print('Starting node "none" for some reason')
    else:
        if type(first_node) != tuple or len(first_node) != 2 or type(first_node[1]) not in [int, float]:
            print('starting node not a node')
    nodes.remove(first_node)
    last_node = first_node
    path1 = {}
    path2 = {}
    while nodes:
        current_node = nodes.pop(min(range(len(nodes)), key=lambda i: math.dist(nodes[i], last_node)))
        path1[last_node] = current_node
        path2[current_node] = last_node
        last_node = current_node
    path1[last_node] = first_node
    path2[first_node] = last_node
    return [path1, path2]


def objective_function(graph: Graph, use_haversine=False) -> float:  # , previous_calcs={}, hs_previous_calcs={}
    """Finds the total distance traveled of the graph.
    If lat longs are inputted & use_haversine=True, will use haversine to find distance on the globe. (Outputs KM)"""
    total_distance = 0
    if use_haversine:
        for p1, p2 in graph[0].items():
            distance = globe_distance(p1, p2)
            total_distance += distance
    else:
        for p1, p2 in graph[0].items():
            distance = math.dist(p1, p2)
            total_distance += distance
    return total_distance
    # if use_haversine:
    #     for p1, p2 in graph[0].items():
    #         if (p1, p2) in hs_previous_calcs:
    #             total_distance += hs_previous_calcs[(p1, p2)]
    #         else:
    #             distance = globe_distance(p1, p2)
    #             total_distance += distance
    #             hs_previous_calcs[(p1, p2)] = distance
    # else:
    #     for p1, p2 in graph[0].items():
    #         if (p1, p2) in previous_calcs:
    #             total_distance += previous_calcs[(p1, p2)]
    #         else:
    #             distance = math.dist(p1, p2)
    #             total_distance += distance
    #             previous_calcs[(p1, p2)] = distance
    # return total_distance


def hill_climb(graph: Graph) -> bool:
    """Inputs/outputs a list of pairs of coordinates
    if maintain_location_for_first_and_last is True, lst should be sorted"""
    unique_coords = set(graph[0])

    score_before = objective_function(graph)
    change = False
    for i, coord1 in enumerate(unique_coords):
        if not i % 100:
            print(f'{i} / {len(unique_coords)}')
        for coord2 in unique_coords - {coord1}:
            edge_to_put_back_in = switch_coordinates_in_list_of_pairs(graph, coord1, coord2)
            if (score_after := objective_function(graph)) > score_before:
                switch_coordinates_in_list_of_pairs(graph, coord1, coord2, edge_to_put_back_in)
            else:
                change = True
                score_before = score_after
    return change


def prims(nodes: List[Coordinate]) -> dict:  # where the dict is a minimum spanning tree
    """finds the minimum spanning tree"""
    unused_nodes = set(nodes)
    minimum_spanning_tree = {unused_nodes.pop(): set()}
    while unused_nodes:
        shortest = (float('inf'), (None, None))
        for node_in_MST in minimum_spanning_tree:
            for unused_node in unused_nodes:
                if (new_dist := globe_distance(node_in_MST, unused_node)) < shortest[0]:
                    shortest = (new_dist, node_in_MST, unused_node)
        new_dist, node_in_MST, unused_node = shortest
        unused_nodes.remove(unused_node)
        minimum_spanning_tree[node_in_MST].add(unused_node)
        minimum_spanning_tree[unused_node] = {node_in_MST}
    return minimum_spanning_tree


def twice_around_the_tree(nodes: List[Coordinate], start_index=0) -> Graph:
    # mst = prims(nodes)
    with open('minimum_spanning_tree.txt') as f:
        mst = eval(f.read())
    start = nodes[start_index]
    visited_init = set(start)
    path_around = []

    def recursive(node: Coordinate, path: Graph, visited: set) -> None:
        # find neighbors (subtract visited)
        neighbors = mst[node] - visited
        # base case: no neighbors
        if not neighbors:
            return
        # run recursive on each neighbor
        for edge in neighbors:
            visited.add(edge)
            path.append([node, edge])
            recursive(edge, path, visited)
            path.append([edge, node])
    recursive(start, path_around, visited_init)  # update path_around in place

    explored = set()
    new_paths = [{}, {}]
    last_item = None
    for item in sum_list_of_lists(path_around):
        if item not in explored:
            explored.add(item)
            if last_item:
                new_paths[0][last_item] = item
                new_paths[1][item] = last_item
            last_item = item
    return new_paths

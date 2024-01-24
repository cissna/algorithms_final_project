import math
import os
import random
from pyperclip import copy
from haversine import haversine
import pytz

from college_lat_longs import lat_longs
from pygame_stuff import main_pygame


def bad_graph(graph):
    """this function caused me pain and suffering"""
    if type(graph) == dict:
        graphs = [graph.copy()]
    elif type(graph) == list:
        graphs = [graph.copy() for graph in graph]
    else:
        raise TypeError('Your graph is messed up')
    for graph in graphs:
        end, current_item = graph.popitem()
        explored = {end}
        while current_item != end:
            if current_item in explored or current_item not in graph:
                return True
            explored.add(current_item)
            current_item = graph[current_item]
    return False


def sum_list_of_lists(lst):
    new = []
    for sub in lst:
        new += sub
    return new


def globe_distance(p1, p2):
    # [(-(1/69) * item[1], (1/54.6) * item[0]) for item in line]
    points = []
    for pt in [p1, p2]:
        points.append((-(1 / 69) * pt[1], (1 / 54.6) * pt[0]))
        # points.append((-pt[1], pt[0]))
    return haversine(*points)


def swap_edges(graph, node1, edge1, node2, edge2):
    """
    Inputs 2 nodes and their edges, with the goal of swapping the edges.
    The swap is simple, but if the edges are swapped on their own, the graph gets messed up because,
    although it's undirected, it's represented as two directed graphs.
    The directed graphs get reversed on one side of the swap, so it's necessary to swap the directions of each of the
    nodes on one side of the graph—as well as doing ONE of the connections backwards.
    """
    if graph[0][node1] == edge1:
        direction = 0
    elif graph[1][node1] == edge1:
        direction = 1

    nodes_to_flip = []
    current_node = node1  # so the first thing in the list will be edge1
    while current_node != edge2:
        current_node = graph[direction][current_node]
        nodes_to_flip.append(current_node)
    for node in nodes_to_flip:
        graph[direction][node], graph[1 - direction][node] = graph[1 - direction][node], graph[direction][node]

    graph[direction][node1] = edge2
    graph[1 - direction][edge2] = node1

    graph[1 - direction][node2] = edge1
    graph[direction][edge1] = node2

    # Check successful :)
    # explored0 = set()
    # explored1 = set()
    # current_node0 = node1
    # current_node1 = node1
    # while (current_node0 != node1 and current_node1 != node1) or not explored0:
    #     explored0.add(current_node0)
    #     explored1.add(current_node1)
    #     current_node0 = graph[0][current_node0]
    #     current_node1 = graph[1][current_node1]
    # if (len(explored1), len(explored0)) != (1073, 1073):
    #     print('Check Failed')



def switch_coordinates_in_list_of_pairs(graph, c1, c2, optional_c1_edge=None):
    """
    Choose an edge (two connected points), and an unrelated point.
    Find out which (of 2) point connected to that point causes the graph to remain connected
    With those two edges, swap one point from each edge with each other, but instead of swapping both sides,
    only swap the chosen edges.
    ...A -> B -> C -> D -> E...   &   ...Z -> Y -> X -> W -> V...
    to
    ...Z -> Y -> C -> D -> E...   &   ...A -> B -> X -> W -> V...
    in such a way that if you follow the path in the same direction
    A -> B -> X -> W -> V... will lead to Z before A (AKA, it will lead to Z at all
    """
    if optional_c1_edge is None:
        if graph[0][c1] == c2:
            c1_edge = graph[1][c1]
            c2_edge = graph[0][c2]
        elif graph[1][c1] == c2:
            c1_edge = graph[0][c1]
            c2_edge = graph[1][c2]
        else:
            c1_edge_direction = random.randint(0, 1)
            c1_edge = graph[c1_edge_direction][c1]
            if graph[c1_edge_direction][c1_edge] == c2:  # if the node one further than c1's edge is c2
                c2_edge = graph[c1_edge_direction][c2]
                c1_edge = graph[1 - c1_edge_direction][c1]  # needs to go in opposite direction or overlaps
            else:
                c2_edge = graph[1 - c1_edge_direction][c2]
    else:
        c1_edge = optional_c1_edge
        if graph[0][c1] == optional_c1_edge:
            c1_edge_direction = 0
        elif graph[1][c1] == optional_c1_edge:
            c1_edge_direction = 1
        else:
            raise ValueError('optional_c1_edge is not actually an edge of c1')
        c2_edge = graph[1 - c1_edge_direction][c2]

    swap_edges(graph, c1, c1_edge, c2, c2_edge)
    return c2_edge


def datetime2pst(time):
    utc_timezone = pytz.timezone('UTC')
    pst_timezone = pytz.timezone('America/Los_Angeles')
    return utc_timezone.localize(time).astimezone(pst_timezone)


def calculate_mst_weight_bfs(mst: dict) -> float:
    """Calculates the weight of the MST using BFS traversal."""
    weight = 0.0
    done = set()
    for key, values in mst.items():
        for value in values:
            if (key, value) not in done:
                weight += globe_distance(key, value)
                done.add((value, key))
    return weight


def get_files(path_name):
    return [f"{path_name}/{f}" for f in os.listdir(path_name) if os.path.isfile(os.path.join(path_name, f))]


def load_file(file_name, already_formatted=False):
    with open(file_name) as f:
        content = f.read()
    if already_formatted:
        dicts = [{tuple([float(n) for n in dict_entry.split(': ')[0].strip('()').split(', ')]):
                  tuple([float(n) for n in dict_entry.split(': ')[1].strip('()').split(', ')])
                  for dict_entry in dictionary.split('), (')}
                 for dictionary in content.strip('[]{}').split('}, {')]
        return dicts
    else:
        pairs = [[tuple([float(num) for num in tup.split(', ')])
                  for tup in pair.strip('()').split('), (')]
                 for pair in content.strip('[]').split("], [")]
        return convert_one_graph_to_another(pairs)


def convert_one_graph_to_another(graph: list):
    """Result of me using a bad type then saving a bunch of files then changing the type"""
    groph = [{}, {}]
    for p1, p2 in graph:
        groph[0][p1] = p2
        groph[1][p2] = p1
    return groph

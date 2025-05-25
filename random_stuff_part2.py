import random

import pygame_stuff
from algorithm_stuff import objective_function, arbitrary_graph
from genetic_algorithm import mutate, init
from helper_functions import convert_one_graph_to_another, load_file, bad_graph, switch_coordinates_in_list_of_pairs
from main_nvm_random import lat_longs

def convert_to_lat_long(tup):
    return (-(1/69) * tup[1], (1/54.6) * tup[0])



# population = init(load='emergency_pickles/2024-01-22 16:17:20.865700.pkl')
# population = init(300)
# graph = load_file('path_saves/well_hill_climbed.txt', True)
# for i in range(len(population[0][0])):
#     graph = population[i]
#     print(i)
#     print(bad_graph(graph[0]))
#     print(bad_graph(graph[1]))
#     print()

graph = arbitrary_graph(lat_longs, True)
c1, c2 = random.sample(lat_longs, k=2)
switch_coordinates_in_list_of_pairs(graph, c1, c2)

bad_graph(graph)
c1, c2 = random.sample(lat_longs, k=2)
switch_coordinates_in_list_of_pairs(graph, c1, c2)
print(bad_graph(graph))

# if not {(key, value) for key, value in graph[0].items()} == {(value, key) for key, value in graph[1].items()}:
#     print('uh oh')
# pygame_stuff.main_pygame(lat_longs, population[0])
# pygame_stuff.main_pygame(lat_longs, population[-1])

# print(str([{str(key): str(value) for key, value in item.items()} for item in graph]).replace("'", '"'))

import os
from college_lat_longs import lat_longs
from pygame_stuff import main_pygame
from algorithm_stuff import objective_function, hill_climb
from helper_functions import load_file, bad_graph


def mst2graph(mst):
    graph = [{}, {}]
    for key, values in mst.items():
        for value in values:
            graph[0][key] = value
            graph[1][value] = key
    return graph

path_name = 'path_saves/intermediate_GAs'
# path_name = '../algorithmsFinalProject'
files = [f for f in os.listdir(path_name) if os.path.isfile(os.path.join(path_name, f))]
# files = ['minimum_spanning_tree.txt']
for file in files:
    print(file, end=': ')
    result = load_file(f'{path_name}/{file}', already_formatted=True)
    # with open(file) as f:
    #     result = eval(f.read())
    # result = mst2graph(result)
    # hill_climb(result)
    if not bad_graph(result):
        print(objective_function(result, use_haversine=True))
    else:
        print('bad graph')
    # print(result)
    # main_pygame(lat_longs, result)
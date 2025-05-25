from algorithm_stuff import objective_function
from college_lat_longs import lat_longs
from genetic_algorithm import init
from helper_functions import bad_graph, load_file
from pygame_stuff import main_pygame

# population = init(load='emergency_pickles/2024-01-23 15:20:53.308828.pkl')
#
# for i in range(len(population)):
#     before = str(population[i])
#     bad_graph(population[i])
#     print(before == str(population[i]))

path = load_file('path_saves/greedies/55176.txt')
print(objective_function(path, use_haversine=True))
main_pygame(lat_longs, path)

path = load_file('path_saves/greedies/53125.txt')
print(objective_function(path, use_haversine=True))
main_pygame(lat_longs, path)

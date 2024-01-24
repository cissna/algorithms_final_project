import math
import os
import pickle
import random
from datetime import datetime
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
import pygame_stuff
from algorithm_stuff import arbitrary_graph, Graph, objective_function, sort_population, hill_climb
from helper_functions import get_files, load_file, sum_list_of_lists, switch_coordinates_in_list_of_pairs, bad_graph
from college_lat_longs import lat_longs


def init(size: int = None, load: str = None) -> List[Graph]:
    """Initializes the group of graphs that the GA will use.
    Notes: I have 5 different groups (as well as two more, less useful ones)
    at my disposal, but I think just taking random ones from the optimal group might be the best strategy.
    """
    if load is None:
        if size is None:
            raise ValueError('Both load and size cannot be None')
        # size__greedy_hill_climbed_fully = round(.0575 * size) * 0
        size__greedy_hill_climbed_twice = round(.1 * size)
        size__greedy_hill_climbed_fully = round(.2 * size)
        size__greedy_raw = round(.05 * size)
        size__TATT_raw = round(.05 * size)
        size__TATT_hill_climbed_once = round(.1 * size)
        include_well_hill_climbed = 1  # should be 1 or 0
        size__random = size - (size__greedy_hill_climbed_twice + size__greedy_hill_climbed_fully + size__greedy_raw +
                               size__TATT_raw + size__TATT_hill_climbed_once + include_well_hill_climbed)

        files__greedy_hill_climbed_twice = [load_file(file) for file in
                                            np.random.choice(get_files('path_saves/greedies_hilled2'),
                                                             size=size__greedy_hill_climbed_twice, replace=False)]
        files__greedy_hill_climbed_fully = [load_file(file) for file in
                                            np.random.choice(get_files('path_saves/greedies_fully_hilled'),
                                                             size=size__greedy_hill_climbed_fully, replace=False)]
        files__greedy_raw = [load_file(file) for file in
                             np.random.choice(get_files('path_saves/greedies'),
                                              size=size__greedy_raw, replace=False)]
        files__TATT_raw = [load_file(file) for file in
                           np.random.choice(get_files('path_saves/twices'),
                                            size=size__TATT_raw, replace=False)]
        files__TATT_hill_climbed_once = [load_file(file) for file in
                                         np.random.choice(get_files('path_saves/twices_hilled'),
                                                          size=size__TATT_hill_climbed_once, replace=False)]

        files__random = [arbitrary_graph(lat_longs, randomize=True) for _ in range(size__random)]
        final = sum_list_of_lists(
            [files__greedy_hill_climbed_twice, files__greedy_hill_climbed_fully, files__greedy_raw,
             files__TATT_raw, files__TATT_hill_climbed_once, files__random])
        if include_well_hill_climbed:
            final.append(load_file("path_saves/best_GAs/2024-01-22 12:09:57.447249.txt", already_formatted=True))
            # final.append(load_file('path_saves/well_hill_climbed.txt', already_formatted=True))
        return final
    with open(load, 'rb') as f:
        final = pickle.load(f)
        for i in range(len(final)):
            if bad_graph(final[i]):
                print('bad', i)
                final[i] = arbitrary_graph(lat_longs, randomize=True)
        return final


def mutate(graph: Graph) -> None:
    chance_of_more_than_one_mutation = .1
    mutation_mean = 500  # note that 2888 is roughly the maximum distance between points
    mutation_sd = 500  # these values are completely arbitrary, so it's important for SD to be very high

    list_of_points = list(graph[0].keys())
    random.shuffle(list_of_points)

    another = False
    for p1 in list_of_points.copy():
        if random.random() < chance_of_more_than_one_mutation:
            another = True
        random_distance = abs(np.random.normal(mutation_mean, mutation_sd))  # maybe dumb to do abs()
        random.shuffle(list_of_points)  # another element of randomness that will hopefully make the code go faster
        for p2 in list_of_points:
            if math.dist(p1, p2) < random_distance:
                break
        switch_coordinates_in_list_of_pairs(graph, p1, p2)
        if not another:
            break
        another = False


# needs to be updated once fixed (minimally)
def genetic_algorithm(pop_size: int) -> Graph:
    population = init(load='emergency_pickles/2024-01-23 18:59:50.413893.pkl')
    pop_size_is_odd = bool(pop_size % 2)

    death_weights = np.array([float(i ** 4) for i in range(pop_size)])
    death_weights /= sum(death_weights)
    try:
        for generation in range(76_543_210):
            sort_population(population)
            if generation % 100_000 == 99999:
                # fully hill climb top 10
                start = datetime.now()
                for i in range(len(population)):
                    if i > 20:
                        break
                    change = True
                    while change:
                        change = hill_climb(population[i])
                print('BIG', (datetime.now() - start).total_seconds())
            elif generation % 10_000 == 9999:
                print(f'{generation:,} / {76_543_210:,}')
                # hill climb top 40 once
                start = datetime.now()
                for i in range(len(population)):
                    if i > 5:  # len(population) / 30:
                        break
                    hill_climb(population[i])
                sort_population(population)
                print((datetime.now() - start).total_seconds())
                with open('path_saves/intermediate_GAs/' + str(start) + '.txt', 'w') as f:
                    f.write(str(population[0]))

            best = [item.copy() for item in population[0]]  # shallow copy not enough

            [mutate(population[i]) for i in range(pop_size)]
            sort_population(population)
            # for item in population:
            #     pygame_stuff.main_pygame(lat_longs, item)
            indexes_to_die = np.random.choice(np.arange(pop_size), size=pop_size // 2, replace=False, p=death_weights)
            for i in sorted(indexes_to_die, reverse=True):
                population.pop(i)
            population += [[subitem.copy() for subitem in item] for item in population]
            if pop_size_is_odd:
                population.pop()
            population[-1] = best  # reinsert the optimal graph back into the population, in case its mutation is bad
    except KeyboardInterrupt:
        print("ERROR")
    with open(f'emergency_pickles/{datetime.now()}.pkl', 'wb') as file:
        pickle.dump(population, file)
    sort_population(population)
    file_name = f'path_saves/best_GAs/{datetime.now()}.txt'
    with open(file_name, 'w') as f:
        f.write(str(population[0]))
    return population[0]


if __name__ == '__main__':
    output = genetic_algorithm(300)
    print(objective_function(output, use_haversine=True))
    pygame_stuff.main_pygame(lat_longs, output)

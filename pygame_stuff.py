from datetime import datetime
from time import sleep

import pygame
import sys

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
magenta = (255, 0, 144)

pt_size = 3

delay = .01

width, height = 1700, 900
used_width, used_height = width - 100, height - 100


# needs to be updated once fixed
def main_pygame(nodes: list, graph: list):
    graph = graph[1].copy()
    x = sorted([node[0] for node in nodes])
    y = sorted([node[1] for node in nodes])
    xdiff = x[-1] - x[0]
    ydiff = y[-1] - y[0]
    if xdiff == 0:
        plus_x = used_width // 2
        if ydiff == 0:
            plus_y = used_height // 2
            scalar = 1
        else:
            scalar = used_height / ydiff
            plus_y = 0
    elif ydiff == 0:
        plus_y = used_height // 2
        plus_x = 0
        scalar = used_width / xdiff
    else:
        if xdiff / used_width > ydiff / used_height:
            scalar = used_width / xdiff
            plus_x = 0
            plus_y = (used_height - ydiff * scalar) // 2
        else:
            scalar = used_height / ydiff
            plus_y = 0
            plus_x = (used_width - xdiff * scalar) // 2

    adjusted_nodes_d = {node: ((node[0] - x[0]) * scalar + plus_x + 50,
                               (node[1] - y[0]) * scalar + plus_y + 50) for node in nodes}

    # Initialize Pygame
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Traveling Salesman Visualisation")
    screen.fill(white)

    # Main game loop
    the_list = []
    while graph:
        p1, p2 = graph.popitem()
        the_list.append((p1, p2))
    while the_list:
        p1, p2 = the_list.pop()
        if pygame.QUIT in [item.type for item in pygame.event.get()]:
            break

        for node in adjusted_nodes_d.values():
            pygame.draw.circle(screen, black, (node[0], node[1]), pt_size)
        pygame.display.flip()  # Update the display

        # for key, value in graph:  # check all lines without delay
        #     draw_line(pygame, screen, red, adjusted_nodes_d[key], value)

        adjusted_p1 = adjusted_nodes_d[p1]
        adjusted_p2 = adjusted_nodes_d[p2]
        draw_line(pygame, screen, red, adjusted_p1, adjusted_p2)
        if not the_list:
            sleep(delay)
            break
        sleep(delay)
    sleep(2)

    pygame.image.save(pygame.display.get_surface(), f'/Users/isaac.cissna/Desktop/GRAH/{datetime.now()}.png')
    pygame.quit()  # Quit Pygame
    # sys.exit()


def draw_line(pygane, screem, color, p1, p2):  # perhaps change to a slow line later in time.
    pygane.draw.line(screem, color, p1, p2, width=pt_size-1)
    pygane.display.flip()  # Update the display


if __name__ == '__main__':
    main_pygame()

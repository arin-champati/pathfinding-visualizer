from queue import PriorityQueue
import pygame as pg
import board
from board import Node


def manhattan(node_1, node_2):
    point_1 = node_1.position()
    point_2 = node_2.position()
    x1, y1 = point_1
    x2, y2 = point_2
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    cost = node_1.cost()
    return cost + (dx + dy)

def reconstruct_path(start_node, current, draw):
    while (current.parent != start_node):
        current = current.parent
        current.make_path()
    
    draw()

# all of these functions will take in as the first argument
# an ambiguous function named draw(), which updates the window
def a_star(draw, grid, start_node, end_node):
	index = 0
    # min priority queue to get node with min f constant time
	open_list = PriorityQueue()
    # tradeoff with memory for speed - keep track of open nodes
	open_list_tracker = {start_node}

    # initialize node values
	open_list.put((0, index, start_node))
	start_node.f = manhattan(start_node, end_node)
	start_node.g = 0

	while not open_list.empty():
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()

		current = open_list.get()[2]
		open_list_tracker.remove(current)

		if current == end_node:
			reconstruct_path(start_node, end_node, draw)
			end_node.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = current.g + current.cost()

			if temp_g_score < neighbor.g:
				neighbor.parent = current
				neighbor.g = temp_g_score
				neighbor.f = temp_g_score + manhattan(neighbor, end_node)
				if neighbor not in open_list_tracker:
					index += 1
					open_list.put((neighbor.f, index, neighbor))
					open_list_tracker.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start_node:
			current.make_closed()

	return False

from algorithms_utils import *
from .. import constants
from constants import *

def __normal_dfs(graph, starting_point, ending_point, callback):
	size = grapthSize(graph)

	if starting_point[0] < 0 or starting_point[0] >= size[0] or starting_point[1] < 0 or starting_point[1] >= size[1]:
		return None

	mark = [[False for __ in range(size[1])] for _ in range(size[0])]
	answer = []

	def __process(current_position):
		if ending_point == current_position:
			return True

		if not isEmptyCell(graph[current_position[0]][current_position[1]]) or mark[current_position[0]][current_position[1]]:
			return False

		mark[current_position[0]][current_position[1]] = True
		if current_position != starting_point:
			callback(current_position[1], current_position[0], Colors.PATH_COLOR)

		found = False
		for element in direction:
			next_step = current_position[0] + element[0], current_position[1] + element[1]
			
			if next_step[0] < 0 or next_step[0] >= size[0] or next_step[1] < 0 or next_step[1] >= size[1]:
				continue

			found = __process(next_step)

			if found:
				answer.append(next_step)
				break

		if not found:
			callback(current_position[1], current_position[0], Colors.WHITE)
		
		mark[current_position[0]][current_position[1]] = False
		return found

	found = __process(starting_point)

	if not found:
		return None

	return answer[::-1]

def __dfs_with_bonus_point(graph, starting_point, ending_point, bonus_points, callback):
	def __process(current_position):
		pass

def __dfs_intermediate_point(graph, starting_point, ending_point, itermediate_points, callback):
	def __process(current_position):
		pass

def __dfs_with_teleport_point(graph, starting_point, ending_point, teleport_points, callback):
	size = grapthSize(graph)
	
	if starting_point[0] < 0 or starting_point[0] >= size[0] or starting_point[1] < 0 or starting_point[1] >= size[1]:
		return None

	mark = [[False for __ in range(size[1])] for _ in range(size[0])]
	answer = []

	def __process(current_position, tele = False):
		if current_position == ending_point:
			return True

		if mark[current_position[0]][current_position[1]] or not isEmptyCell(graph[current_position[0]][current_position[1]]):
			return False

		mark[current_position[0]][current_position[1]] = True
		if current_position != starting_point:
			callback(current_position[1], current_position[0], Colors.PATH_COLOR)
		found = False

		for element in direction:
			next_step = current_position[0] + element[0], current_position[1] + element[1]
			
			if next_step[0] < 0 or next_step[0] >= size[0] or next_step[1] < 0 or next_step[1] >= size[1]:
				continue
			
			if not tele and isTeleportCell(graph[next_step[0]][next_step[1]]):
				# Stuck
				# __found = False
				# print('haha')
				# for teleport in teleport_list:
				# 	__found = __process(next_step, tele = True)
				# 	if __found:
				# 		answer.append(teleport)
				# 		break
				# if __found:
				# 	break
				pass
			else:
				found = __process(next_step)

				if found:
					answer.append(next_step)
					break
		
		if not found:
			callback(current_position[1], current_position[0], Colors.WHITE)

		mark[current_position[0]][current_position[1]] = False
		
		return found

	found = __process(starting_point)

	if not found:
		return None

	return answer[::-1]

def dfs(graph, starting_point, ending_point, mode, bonus_points, intermediate_points, teleport_points, call_back):
	
	if mode == AlgorithmsMode.NORMAL:
		return __normal_dfs(graph, starting_point, ending_point, call_back)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __dfs_with_bonus_point(graph, starting_point, ending_point, bonus_points, call_back)
	
	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __dfs_intermediate_point(graph, starting_point, ending_point, intermediate_points, call_back)
	
	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __dfs_with_teleport_point(graph, starting_point, ending_point, teleport_points, call_back)

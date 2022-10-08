from algorithms_utils import *


def __normal_ucs():
	pass

def __ucs_with_bonus_point():
	pass

def __ucs_intermediate_point():
	pass

def __ucs_with_teleport_point():
	pass

def ucs(graph, mode, call_back):
	if not isValidGraph(graph):
		return None

	if mode == AlgorithmsMode.NORMAL:
		return __normal_ucs(graph, call_back)

	if mode == AlgorithmsMode.BONUS_POINT:
		return __ucs_with_bonus_point(graph, call_back)
	
	if mode == AlgorithmsMode.INTERMEDIATE_POINT:
		return __ucs_intermediate_point(graph, call_back)
	
	if mode == AlgorithmsMode.TELEPORT_POINT:
		return __ucs_with_teleport_point(graph, call_back)


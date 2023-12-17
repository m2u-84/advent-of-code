#!/usr/bin/env python3

from math import ceil, floor

map: list[str] = []
cycle_count = 1000000000

with open('input.txt', 'r') as input_file:
	for line in input_file:
		if row := line.rstrip():
			map.append(row)

column_count = len(map[0])
row_count = len(map)

directions = {
	'north': {
		'outer': range(0, column_count),
		'inner': range(0, row_count),
		'x_index': 0,
		'y_index': 1,
		'slot_offset': 1
	},
	'west': {
		'outer': range(0, row_count),
		'inner': range(0, column_count),
		'x_index': 1,
		'y_index': 0,
		'slot_offset': 1
	},
	'south': {
		'outer': range(0, column_count),
		'inner': range(row_count - 1, -1, -1),
		'x_index': 0,
		'y_index': 1,
		'slot_offset': -1
	},
	'east': {
		'outer': range(0, row_count),
		'inner': range(column_count - 1, -1, -1),
		'x_index': 1,
		'y_index': 0,
		'slot_offset': -1
	}
}

load_history: list[int] = []

for cycle in range(cycle_count):
	for direction, direction_specs in directions.items():
		match direction:
			case 'north':
				next_free_slots = [0] * column_count
			case 'west':
				next_free_slots = [0] * row_count
			case 'south':
				next_free_slots = [row_count - 1] * column_count
			case 'east':
				next_free_slots = [column_count - 1] * row_count
			case _:
				raise ValueError(f'Invalid direction: {direction}.')

		for position1 in direction_specs['outer']:
			for position2 in direction_specs['inner']:
				position = (position1, position2)

				x_position = position[direction_specs['x_index']]
				y_position = position[direction_specs['y_index']]
				char = map[y_position][x_position]

				match char:
					case '.':
						continue
					case 'O':
						map[y_position] = map[y_position][:x_position] + '.' + map[y_position][x_position + 1:]

						if direction_specs['y_index']:
							map[next_free_slots[position1]] = f'{map[next_free_slots[position1]][:x_position]}O{map[next_free_slots[position1]][x_position + 1:]}'
						else:
							map[y_position] = f'{map[y_position][:next_free_slots[position1]]}O{map[y_position][next_free_slots[position1] + 1:]}'

						next_free_slots[position1] += direction_specs['slot_offset']
					case '#':
						next_free_slots[position1] = position2 + direction_specs['slot_offset']
					case _:
						raise ValueError(f'Invalid char found: {char}.')

	load = 0

	for index, row in enumerate(map):
		for column in row:
			if column == 'O':
				load += row_count - index

	load_history.append(load)

	indices = [i for i, x in enumerate(load_history) if x == load]
	count = len(indices)

	if count > 2 and count % 2 == 1 and indices[-1] - indices[0] > 2:
		first_index = indices[-count]
		middle_index = indices[-ceil(count / 2)]
		first_sequence = load_history[first_index:middle_index]
		second_sequence = load_history[middle_index:indices[-1]]

		if first_sequence == second_sequence:
			sequence_length = len(first_sequence)
			first_result_index = int(cycle_count - floor((cycle_count - first_index) / sequence_length) * sequence_length) - 1

			print(load_history[first_result_index])

			break

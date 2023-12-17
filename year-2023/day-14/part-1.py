#!/usr/bin/env python3

rock_positions: list[list[int]] = []
next_free_slots: list[int] = []
row_count = 0

with open('input.txt', 'r') as input_file:
	for row_id, line in enumerate(input_file):
		row = line.rstrip()

		if line:
			row_count += 1

		if not row_id:
			rock_positions = [[] for _ in range(len(row))]
			next_free_slots = [0] * len(row)

		for column_id, column in enumerate(row):
			match column:
				case '.':
					continue
				case 'O':
					rock_positions[column_id].append(next_free_slots[column_id])
					next_free_slots[column_id] += 1
				case '#':
					next_free_slots[column_id] = row_id + 1
				case _:
					raise ValueError(f'Invalid char found: {column}.')

load = 0

for column in rock_positions:
	for position in column:
		load += row_count - position

print(load)

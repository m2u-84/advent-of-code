#!/usr/bin/env python3

from itertools import combinations

map: list[list[int]] = []
empty_columns: list[bool] = []

with open('input.txt', 'r') as input_file:
	for index, row in enumerate(input_file):
		if index == 0:
			empty_columns = [True] * (len(row) - 1)

		hash_positions = [i for i, char in enumerate(row) if char == '#']

		map.append(hash_positions)

		if not hash_positions:
			map.append([])

		for position in hash_positions:
			empty_columns[position] = False

for y_position, row in enumerate(map):
	offset = 0
	adjusted_row: list[int] = []

	for x_position, column in enumerate(empty_columns):
		if column == True:
			offset += 1

		if x_position in row:
			adjusted_row.append(x_position + offset)

	map[y_position] = adjusted_row

hash_coordinates: list[tuple[int, int]] = []

for y_position, row in enumerate(map):
	for x_position in row:
		hash_coordinates.append((x_position, y_position))

total_distance = 0

for combo in combinations(hash_coordinates, 2):
	distance = abs(combo[0][0] - combo[1][0]) + abs(combo[0][1] - combo[1][1])

	total_distance += distance

print(total_distance)

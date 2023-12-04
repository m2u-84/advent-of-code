#!/usr/bin/env python3

from re import finditer

sum = 0

relative_periphery_coordinates = range(-1, 2)
covered_coordinates: list[tuple[int, int]] = []

with open('input.txt', 'r') as input_file:
	for line_number, line in enumerate(input_file):
		for char_number, char in enumerate(line.rstrip()):
			if (not char.isdigit() and char != '.'):
				for relative_x in relative_periphery_coordinates:
					for relative_y in relative_periphery_coordinates:
						x = char_number + relative_x
						y = line_number + relative_y

						if (
							x >= 0 and x < 140
							and y >= 0 and y < 140
							and not (relative_x == 0 and relative_y == 0)
						):
							covered_coordinates.append((x, y))

cover_coordinates_deduplicated = set(covered_coordinates)

with open('input.txt', 'r') as input_file:
	for line_number, line in enumerate(input_file):
		for match in finditer(r'\d+', line):
			number_coordinates: list[tuple[int, int]] = []

			for x_position in range(match.start(), match.end()):
				number_coordinates.append((x_position, line_number))

			number_coordinate_set = set(number_coordinates)

			if len(number_coordinate_set.intersection(covered_coordinates)) > 0:
				sum += int(match[0])

print(sum)

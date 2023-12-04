#!/usr/bin/env python3

from functools import reduce
from re import finditer
from typing import Any

sum = 0

relative_periphery_coordinates = range(-1, 2)
coverage_gear_mapping: dict[tuple[int, int], list[int]] = {}
gear_id = 0

with open('input.txt', 'r') as input_file:
	for line_number, line in enumerate(input_file):
		for char_number, char in enumerate(line.rstrip()):
			if char == '*':
				for relative_x in relative_periphery_coordinates:
					for relative_y in relative_periphery_coordinates:
						x = char_number + relative_x
						y = line_number + relative_y

						if (
							x >= 0 and x < 140
							and y >= 0 and y < 140
							and not (relative_x == 0 and relative_y == 0)
						):
							coordinate = (x, y)

							if not coordinate in coverage_gear_mapping.keys():
								coverage_gear_mapping[coordinate] = [gear_id]
							else:
								coverage_gear_mapping[coordinate].append(gear_id)

				gear_id += 1

covered_coordinates = coverage_gear_mapping.keys()
gear_number_mapping: dict[int, list[int]] = {}
number_metadata_mapping: dict[int, dict[str, Any]] = {}

number_id = 0

with open('input.txt', 'r') as input_file:
	for line_number, line in enumerate(input_file):
		for match in finditer(r'\d+', line):
			number_coordinates: list[tuple[int, int]] = []

			for x_position in range(match.start(), match.end()):
				number_coordinates.append((x_position, line_number))

			number_metadata_mapping[number_id] = {
				'value': int(match[0]),
				'coordinates': set(number_coordinates)
			}

			number_id += 1

gear_number_mapping: dict[int, list[int]] = {}

for number, metadata in number_metadata_mapping.items():
	for number_coordinate in metadata['coordinates']:
		if number_coordinate in covered_coordinates:
			for gear in coverage_gear_mapping[number_coordinate]:
				if not gear in gear_number_mapping.keys():
					gear_number_mapping[gear] = []

				if not number in gear_number_mapping[gear]:
					gear_number_mapping[gear].append(number)

for gear, number_ids in gear_number_mapping.items():
	if len(number_ids) > 1:
		sum += reduce(
			(lambda x, y: x * y),
			map(
				lambda number_id: number_metadata_mapping[number_id]['value'],
				number_ids
			)
		)

print(sum)

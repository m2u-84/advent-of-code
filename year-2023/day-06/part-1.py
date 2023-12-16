#!/usr/bin/env python3

from functools import reduce
from math import ceil, floor, sqrt
from re import compile, fullmatch, split

line_pattern = compile(r'^(?P<category>Time|Distance):(?P<values>(?: +\d+)+)\s*$')
splitting_pattern = compile(r' +')

times: list[int] = []
distances: list[int] = []
time_distance_mapping: dict[int, int] = {}

solution_counts: list[int] = []

with open('input.txt', 'r') as input_file:
	for line in input_file:
		if match := fullmatch(line_pattern, line):
			match match['category']:
				case 'Time':
					times = list(map(int, split(splitting_pattern, match['values'].lstrip())))
				case 'Distance':
					distances = list(map(int, split(splitting_pattern, match['values'].lstrip())))
				case _:
					pass

if len(times) != len(distances):
	ValueError('Invalid input.')

time_distance_mapping = dict(zip(times, distances))

for time, distance in time_distance_mapping.items():
	min_target_distance = distance + 1

	min_pushing_time = max(ceil(time / 2 - sqrt((time / 2) ** 2 - min_target_distance)), 0)
	max_pushing_time = max(floor(time / 2 + sqrt((time / 2) ** 2 - min_target_distance)), 0)

	solution_count = max_pushing_time - min_pushing_time + 1

	solution_counts.append(solution_count)

print(reduce(lambda x, y: x * y, solution_counts))

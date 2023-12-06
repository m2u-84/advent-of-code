#!/usr/bin/env python3

from math import ceil, floor, sqrt
from re import compile, fullmatch

line_pattern = compile(r'^(?P<category>Time|Distance):(?P<values>(?: +\d+)+)\s*$')
splitting_pattern = compile(r' +')

time: int = 0
distance: int = 0

with open('input.txt', 'r') as input_file:
	for line in input_file:
		if match := fullmatch(line_pattern, line):
			match match['category']:
				case 'Time':
					time = int(match['values'].replace(' ', ''))
				case 'Distance':
					distance = int(match['values'].replace(' ', ''))
				case _:
					pass

if time < 1 or distance < 1:
	ValueError('Invalid input.')

min_target_distance = distance + 1

min_pushing_time = max(ceil(time / 2 - sqrt((time / 2) ** 2 - min_target_distance)), 0)
max_pushing_time = max(floor(time / 2 + sqrt((time / 2) ** 2 - min_target_distance)), 0)

solution_count = max_pushing_time - min_pushing_time + 1

print(solution_count)

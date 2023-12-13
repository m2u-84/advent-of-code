#!/usr/bin/env python3

from re import compile, fullmatch, Pattern
from typing import NamedTuple

class MapRow(NamedTuple):
	springs: str
	spring_pattern: Pattern[str]

def compile_spring_pattern(damage_sequences: list[int]) -> Pattern[str]:
	pattern = fr'^\.*{r'\.+'.join([f'#{{{value}}}' for value in damage_sequences])}\.*$'

	return compile(pattern)

def find_possible_placements(
	springs: str,
	spring_pattern: Pattern[str]
) -> list[str]:
	possible_placements: list[str] = []

	if springs.find('?') != -1:
		possible_placements += find_possible_placements(
			springs = springs.replace('?', '.', 1),
			spring_pattern = spring_pattern
		)

		possible_placements += find_possible_placements(
			springs = springs.replace('?', '#', 1),
			spring_pattern = spring_pattern
		)
	elif fullmatch(spring_pattern, springs):
		possible_placements.append(springs)

	return possible_placements

map: list[MapRow] = []

with open('input.txt', 'r') as input_file:
	for line in input_file:
		(springs, sequences) = line.rstrip().split()

		map.append(
			MapRow(
				springs = springs,
				spring_pattern = compile_spring_pattern(
					damage_sequences = [int(sequence) for sequence in sequences.split(',')]
				)
			)
		)

total_possible_placements = 0

for map_row in map:
	possible_placements = find_possible_placements(
		springs = map_row.springs,
		spring_pattern = map_row.spring_pattern
	)

	total_possible_placements += len(possible_placements)

print(total_possible_placements)

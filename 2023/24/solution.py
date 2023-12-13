#!/usr/bin/env python3

# Needs more optimization with some caching to achieve better runtime results.

from functools import lru_cache
from re import compile, finditer, fullmatch, Pattern
from typing import NamedTuple

damage_sequence_pattern = compile(r'#+\.')

class MapRow(NamedTuple):
	springs: str
	damaged_spring_sequence: tuple[int]

def compile_spring_pattern(damage_spring_sequence: tuple[int]) -> Pattern[str]:
	pattern = fr'^\.*{r'\.+'.join([f'#{{{value}}}' for value in damage_spring_sequence])}\.*$'

	return compile(pattern)

def find_possible_placements(
	springs: str,
	damaged_spring_sequence: tuple[int]
) -> list[str]:
	possible_placements: list[str] = []

	if springs.find('?') != -1:
		proposed_partial_damage_sequence = tuple([match.span()[1] - match.span()[0] - 1 for match in finditer(damage_sequence_pattern, springs.split('?', 1)[0])])
		actual_partial_damage_sequence = damaged_spring_sequence[0:len(proposed_partial_damage_sequence)]

		if proposed_partial_damage_sequence == actual_partial_damage_sequence:
			possible_placements += find_possible_placements(
				springs = springs.replace('?', '.', 1),
				damaged_spring_sequence = damaged_spring_sequence
			)

			possible_placements += find_possible_placements(
				springs = springs.replace('?', '#', 1),
				damaged_spring_sequence = damaged_spring_sequence
			)
	elif fullmatch(
		compile_spring_pattern(
			damage_spring_sequence = damaged_spring_sequence
		),
		springs
	):
		possible_placements.append(springs)

	return possible_placements

map: list[MapRow] = []

with open('input.txt', 'r') as input_file:
	for line in input_file:
		(springs, sequences) = line.rstrip().split()

		map.append(
			MapRow(
				springs = '?'.join([springs] * 5),
				damaged_spring_sequence = tuple([int(sequence) for sequence in sequences.split(',')] * 5)
			)
		)

total_possible_placements = 0

for map_row in map:
	print(f'Examining row {map_row.springs}…')

	possible_placements = find_possible_placements(
		springs = map_row.springs,
		damaged_spring_sequence = map_row.damaged_spring_sequence
	)

	total_possible_placements += len(possible_placements)

print(total_possible_placements)

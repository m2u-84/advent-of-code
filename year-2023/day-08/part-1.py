#!/usr/bin/env python3

from re import compile, fullmatch

def perform_transition(
	current_location: str,
	direction: str,
	transitions: dict[str, tuple[str, str]]
) -> str:
	direction_index = 0 if direction == 'L' else 1

	return transitions[current_location][direction_index]

directions_pattern = compile(r'(?P<directions>[RL]+)\s*')
transition_pattern = compile(r'(?P<key>[A-Z]{3})\s*=\s*\((?P<origin>[A-Z]{3}),\s*(?P<destination>[A-Z]{3})\)\s*')

directions: str = ''
transitions: dict[str, tuple[str, str]] = {}

with open('input.txt', 'r') as input_file:
	for line in input_file:
		if match := fullmatch(transition_pattern, line):
			if (key := match.group('key')) in transitions:
				raise ValueError('Ambiguous transitions.')

			transitions[key] = (match.group('origin'), match.group('destination'))
		elif match := fullmatch(directions_pattern, line):
			directions = match.group('directions')

location = 'AAA'
step_count = 0

while location != 'ZZZ':
	for direction in directions:
		location = perform_transition(
			current_location = location,
			direction = direction,
			transitions = transitions
		)

		step_count += 1

		if location == 'ZZZ':
			break

print(step_count)

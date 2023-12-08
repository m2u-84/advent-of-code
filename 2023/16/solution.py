#!/usr/bin/env python3

# Disclaimer: This was the first riddle for which I had a little nudge in the
# right direction. My first implementation was the brute-force approach (which
# would have run for waaay to long). So while researching whether I maybe
# misunderstood the instructions (example was a little ambiguous imho) I was
# spoilered about utilizing LCM. Stopped reading right there and then came up
# with the solution below.

from math import lcm
from re import compile, fullmatch

location_mapping: dict[str, str] = {}
a_count = 0
z_count = 0
initial_origins: list[str] = []

def translate_key(original_key: str) -> str:
	global location_mapping
	global a_count
	global z_count
	global initial_origins

	if original_key in location_mapping:
		return location_mapping[original_key]
	elif original_key.endswith('A'):
		a_count += 1

		if a_count > 9:
			raise ValueError('Too many initial origins.')

		replacement_key = f'{a_count}{a_count}A'
		location_mapping[original_key] = replacement_key

		initial_origins.append(replacement_key)

		return replacement_key
	elif original_key.endswith('Z'):
		z_count += 1

		if z_count > 9:
			raise ValueError('Too many final destinations.')

		replacement_key = f'{z_count}{z_count}Z'
		location_mapping[original_key] = replacement_key

		return replacement_key
	else:
		return original_key

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

			transitions[translate_key(original_key = key)] = (translate_key(original_key = match.group('origin')), translate_key(original_key = match.group('destination')))
		elif match := fullmatch(directions_pattern, line):
			directions = match.group('directions')

step_counts: list[int] = []

for initial_origin in initial_origins:
	current_location = initial_origin
	current_step_count = 0

	while not current_location.endswith('Z'):
		for direction in directions:
			current_location = perform_transition(
				current_location = current_location,
				direction = direction,
				transitions = transitions
			)

			current_step_count += 1

			if current_location.endswith('Z'):
				break

	step_counts.append(current_step_count)

print(lcm(*step_counts))

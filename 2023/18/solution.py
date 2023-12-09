#!/usr/bin/env python3

sum = 0

def calculate_transition_sequence(original_sequence: list[int]) -> list[int]:
	if len(original_sequence) < 2:
		raise ValueError('Sequence too short.')

	transition_sequence: list[int] = []

	for index, value in enumerate(original_sequence):
		if index == 0:
			continue

		transition_sequence.append(value - original_sequence[index - 1])

	return transition_sequence

with open('input.txt', 'r') as input_file:
	for line in input_file:
		sequence = list(
			reversed(
				list(
					map(lambda value: int(value), line.rstrip().split())
				)
			)
		)
		next_number = 0

		while any(sequence):
			next_number += sequence[-1]

			sequence = calculate_transition_sequence(
				original_sequence = sequence
			)

		sum += next_number

print(sum)

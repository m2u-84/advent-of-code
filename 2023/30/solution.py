#!/usr/bin/env python3

from re import compile, match

def calculate_hash(label: str) -> int:
	sum = 0

	for char in label:
		sum = (sum + ord(char)) * 17 % 256

	return sum

lens_addition_pattern = compile(r'^(?P<label>[a-z]+)=(?P<focal_length>[1-9])$')
lens_removal_pattern = compile(r'^(?P<label>[a-z]+)-$')

instructions: list[str] = []
boxes = list({} for _ in range(256))

with open('input.txt', 'r') as input_file:
	for line in input_file:
		instructions += line.rstrip().split(',')

for instruction in instructions:
	if lens := match(lens_addition_pattern, instruction):
		label = lens.group('label')
		box_id = calculate_hash(label = label)

		boxes[box_id][label] = int(lens.group('focal_length'))
	elif lens := match(lens_removal_pattern, instruction):
		label = lens.group('label')
		box_id = calculate_hash(label = label)

		if label in boxes[box_id]:
			del boxes[box_id][label]
	else:
		raise ValueError(f'Invalid instruction: {instruction}.')

focusing_power = 0

for box_id, box in enumerate(boxes):
	for lens_id, lens in enumerate(box):
		focusing_power += (box_id + 1) * (lens_id + 1) * box[lens]

print(focusing_power)

#!/usr/bin/env python3

sum = 0

with open('input.txt', 'r') as input_file:
	for line in input_file:
		cube_counts = {
			'red': 0,
			'green': 0,
			'blue': 0
		}

		(game_label, game_data) = line.rstrip().split(': ')

		for draw in game_data.split('; '):
			draw_parts = {}

			for part in draw.split(', '):
				(count, color) = part.split()

				if int(count) > cube_counts[color]:
					cube_counts[color] = int(count)

		sum += cube_counts['red'] * cube_counts['green'] * cube_counts['blue']

print(sum)

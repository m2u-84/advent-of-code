#!/usr/bin/env python3

max_counts = {
	'red': 12,
	'green': 13,
	'blue': 14
}

sum = 0

with open('input.txt', 'r') as input_file:
	for line in input_file:
		(game_label, game_data) = line.rstrip().split(': ')

		game_id = int(game_label.split()[1])

		valid = True

		for draw in game_data.split('; '):
			draw_parts = {}

			for part in draw.split(', '):
				(count, color) = part.split()

				draw_parts[color] = count

				if int(count) > max_counts[color]:
					valid = False

					break

		if valid:
			sum += game_id

print(sum)

#!/usr/bin/env python3

blocks: list[list[list[int]]] = []

def line_to_number(line: str) -> int:
	sum = 0
	bit = 0

	for index, char in enumerate(line):
		match char:
			case '.':
				bit = 0
			case '#':
				bit = 1
			case _:
				raise ValueError('Invalid char found.')

		sum += bit * 2 ** index

	return sum

def process_block(rows: list[str], columns: list[str]) -> list[list[int]]:
	return [
		[line_to_number(row) for row in rows],
		[line_to_number(column) for column in columns]
	]

with open('input.txt', 'r') as input_file:
	rows: list[str] = []
	columns: list[str] = []

	for line in input_file:
		if row := line.strip():
			rows.append(row)

			for index, char in enumerate(row):
				if len(columns) > index:
					columns[index] += char
				else:
					columns.append(char)
		else:
			if columns and rows:
				blocks.append(process_block(rows = rows, columns = columns))

				rows = []
				columns = []

	if columns and rows:
		blocks.append(process_block(rows = rows, columns = columns))

sum = 0

for block in blocks:
	for is_horizontal, oriented_block in enumerate(block):
		list_length = len(oriented_block)

		for index in range(1, list_length):
			sublist_length = min(index, list_length - index)

			if oriented_block[index - sublist_length:index] == list(reversed(oriented_block[index:index + sublist_length])):
				sum += index if is_horizontal else index * 100

print(sum)

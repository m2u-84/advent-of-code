#!/usr/bin/env python3

from enum import Enum

class Direction(Enum):
	NORTH = (0, -1)
	EAST = (1, 0)
	SOUTH = (0, 1)
	WEST = (-1, 0)

def calculate_move(
	map: list[str],
	origin: tuple[int, int],
	direction: Direction
) -> tuple[int, int]:
	if not (new_y_position := origin[1] + direction.value[1]) in range(len(map)):
		raise ValueError('Invalid destination coordinate.')

	if not (new_x_position := origin[0] + direction.value[0]) in range(len(map[new_y_position])):
		raise ValueError('Invalid destination coordinate.')

	return (new_x_position, new_y_position)

def determine_pipe(map: list[str], position: tuple[int, int]) -> str:
	if not (pipe := map[position[1]][position[0]]) in '|FJ-7LS':
		raise ValueError('No pipe found.')

	return pipe

def determine_new_direction(
	pipe: str,
	last_direction: Direction
) -> Direction:
	match pipe:
		case '|':
			match last_direction:
				case Direction.NORTH:
					return Direction.NORTH
				case Direction.SOUTH:
					return Direction.SOUTH
				case _:
					raise ValueError('No connection found.')
		case 'F':
			match last_direction:
				case Direction.NORTH:
					return Direction.EAST
				case Direction.WEST:
					return Direction.SOUTH
				case _:
					raise ValueError('No connection found.')
		case 'J':
			match last_direction:
				case Direction.EAST:
					return Direction.NORTH
				case Direction.SOUTH:
					return Direction.WEST
				case _:
					raise ValueError('No connection found.')
		case '-':
			match last_direction:
				case Direction.EAST:
					return Direction.EAST
				case Direction.WEST:
					return Direction.WEST
				case _:
					raise ValueError('No connection found.')
		case '7':
			match last_direction:
				case Direction.EAST:
					return Direction.SOUTH
				case Direction.NORTH:
					return Direction.WEST
				case _:
					raise ValueError('No connection found.')
		case 'L':
			match last_direction:
				case Direction.SOUTH:
					return Direction.EAST
				case Direction.WEST:
					return Direction.NORTH
				case _:
					raise ValueError('No connection found.')
		case _:
			raise ValueError('Not a pipe.')

	return path_transitions[new_pipe][last_direction]

connectors = {
	Direction.NORTH: ['|', 'F', '7'],
	Direction.EAST: ['-', 'J', '7'],
	Direction.SOUTH: ['|', 'L', 'J'],
	Direction.WEST: ['-', 'F', 'L']
}

rows: list[str] = []

with open('input.txt', 'r') as input_file:
	rows = input_file.read().splitlines()

current_position: tuple[int, int] | None = (-1, -1)
current_direction: Direction | None = None

for y_position, row in enumerate(rows):
	if (x_position := row.find('S')) != -1:
		current_position = (x_position, y_position)

		break

if not current_position:
	raise ValueError('No starting position found.')

next_pipe = 'S'

for direction in Direction:
	new_position = calculate_move(
		map = rows,
		origin = current_position,
		direction = direction
	)

	try:
		new_pipe = determine_pipe(map = rows, position = new_position)
	except:
		continue

	if new_pipe in connectors[direction]:
		current_direction = direction
		next_pipe = new_pipe

		break

if not current_direction:
	raise ValueError('No connecting pipe found.')

move_count = 1

while next_pipe != 'S':
	current_position = calculate_move(
		map = rows,
		origin = current_position,
		direction = current_direction
	)

	current_direction = determine_new_direction(
		pipe = next_pipe,
		last_direction = current_direction
	)

	next_pipe = determine_pipe(
		map = rows,
		position = calculate_move(
			map = rows,
			origin = current_position,
			direction = current_direction
		)
	)

	move_count += 1

print(int(move_count / 2))

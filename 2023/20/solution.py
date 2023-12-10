#!/usr/bin/env python3

from enum import auto, Enum

class Direction(Enum):
	NORTH = (0, -1)
	EAST = (1, 0)
	SOUTH = (0, 1)
	WEST = (-1, 0)

class HandSide(Enum):
	RIGHT = -1
	LEFT = 1

turns = {
	'F': {
		Direction.NORTH: HandSide.RIGHT,
		Direction.WEST: HandSide.LEFT
	},
	'J': {
		Direction.EAST: HandSide.LEFT,
		Direction.SOUTH: HandSide.RIGHT
	},
	'7': {
		Direction.NORTH: HandSide.LEFT,
		Direction.EAST: HandSide.RIGHT
	},
	'L': {
		Direction.SOUTH: HandSide.LEFT,
		Direction.WEST: HandSide.RIGHT
	}
}

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

def count_attached_inside_row_tiles(
	pipe_map: list[list[int]],
	position: tuple[int, int],
	area_hand_side: HandSide
) -> int:
	start_x_position = position[0]
	end_x_position = pipe_map[position[1]][pipe_map[position[1]].index(start_x_position) + area_hand_side.value]

	return start_x_position - end_x_position - 1

connectors = {
	Direction.NORTH: ['|', 'F', '7'],
	Direction.EAST: ['-', 'J', '7'],
	Direction.SOUTH: ['|', 'L', 'J'],
	Direction.WEST: ['-', 'F', 'L']
}

rows: list[str] = []
pipe_positions: list[list[int]] = []

with open('input.txt', 'r') as input_file:
	for row in input_file:
		rows.append(row.rstrip())
		pipe_positions.append([])

start_position: tuple[int, int] | None = None
start_direction: Direction | None = None

for y_position, row in enumerate(rows):
	if (x_position := row.find('S')) != -1:
		start_position = (x_position, y_position)

		break

if not start_position:
	raise ValueError('No starting position found.')

current_position = start_position
start_next_pipe = 'S'

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
		start_direction = direction
		start_next_pipe = new_pipe

		break

if not start_direction:
	raise ValueError('No connecting pipe found.')

current_direction = start_direction
next_pipe = start_next_pipe

pipe_positions[current_position[1]].append(current_position[0])

turn_hand_side_ratio = 0

while next_pipe != 'S':
	current_position = calculate_move(
		map = rows,
		origin = current_position,
		direction = current_direction
	)

	pipe_positions[current_position[1]].append(current_position[0])

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

	if next_pipe in turns:
		turn_hand_side_ratio += 1 if turns[next_pipe][current_direction] == HandSide.RIGHT else -1

for row in pipe_positions:
	row.sort()

area_hand_side = HandSide.RIGHT if turn_hand_side_ratio > 0 else HandSide.LEFT
current_position = start_position
current_direction = start_direction
next_pipe = start_next_pipe
inside_tile_count = 0

while next_pipe != 'S':
	print(current_position, current_direction, next_pipe)

	current_position = calculate_move(
		map = rows,
		origin = current_position,
		direction = current_direction
	)

	pipe_positions[current_position[1]].append(current_position[0])

	current_direction = determine_new_direction(
		pipe = next_pipe,
		last_direction = current_direction
	)

	next_position = calculate_move(
		map = rows,
		origin = current_position,
		direction = current_direction
	)

	next_pipe = determine_pipe(
		map = rows,
		position = next_position
	)

	if (
		(
			area_hand_side == HandSide.RIGHT
			and (
				(next_pipe == 'L' and current_direction == Direction.SOUTH)
				or (next_pipe == '|' and current_direction == Direction.SOUTH)
				or (next_pipe == 'F' and current_direction == Direction.WEST)
			)
		)
		or (
			area_hand_side == HandSide.LEFT
			and (
				(next_pipe == '7' and current_direction == Direction.EAST)
				or (next_pipe == '|' and current_direction == Direction.SOUTH)
				or (next_pipe == 'J' and current_direction == Direction.SOUTH)
			)
		)
	):
		inside_tile_count += count_attached_inside_row_tiles(
			pipe_map = pipe_positions,
			position = next_position,
			area_hand_side = area_hand_side
		)

print(inside_tile_count)

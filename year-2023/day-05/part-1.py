#!/usr/bin/env python3

from re import compile, fullmatch
from typing import Iterable

seed_listing_pattern = compile(r'^seeds:(?P<seed_ids>(?: \d+)+)\s*$')
block_heading_pattern = compile(r'^(?P<block_type>seed-to-soil|soil-to-fertilizer|fertilizer-to-water|water-to-light|light-to-temperature|light-to-temperature|temperature-to-humidity|humidity-to-location) map:\s*$')
mapping_pattern = compile(r'^(?P<target_range_start>\d+) (?P<source_range_start>\d+) (?P<range_length>\d+)\s*$')

seeds: list[int] = []

range_mappings: dict[str, dict[Iterable[int], int]] = {
	'seed-to-soil': {},
	'soil-to-fertilizer': {},
	'fertilizer-to-water': {},
	'water-to-light': {},
	'light-to-temperature': {},
	'light-to-temperature': {},
	'temperature-to-humidity': {},
	'humidity-to-location': {}
}

current_block: str | None = None
lowest_location_id: int | None = None

with open('input.txt', 'r') as input_file:
	for line in input_file:
		if match := fullmatch(mapping_pattern, line):
			if not current_block:
				ValueError('Mapping values outside of mapping block.')

			source_range_start = int(match['source_range_start'])
			target_range_start = int(match['target_range_start'])
			range_length = int(match['range_length'])

			range_mappings[current_block][range(source_range_start, source_range_start + range_length)] = target_range_start - source_range_start
		elif match := fullmatch(block_heading_pattern, line):
			current_block = match['block_type']
		elif match := fullmatch(seed_listing_pattern, line):
			if seeds:
				ValueError('Duplicate seed lists.')

			current_block = None

			seeds = list(map(lambda id: int(id), match['seed_ids'].strip().split(' ')))

for seed in seeds:
	last_mapping_value = seed

	for block_type, mappings in range_mappings.items():
		for value_range, difference in mappings.items():
			if last_mapping_value in value_range:
				last_mapping_value += difference

				break

	if not lowest_location_id or last_mapping_value < lowest_location_id:
		lowest_location_id = last_mapping_value

print(lowest_location_id)

#!/usr/bin/env python3

from re import compile, fullmatch, split

sum = 0

line_pattern = compile(r'^Card +\d+: (?P<own_numbers>[^\|]+?) \| (?P<winning_numbers>.+)$')
list_separator_pattern = compile(r' +')

with open('input.txt', 'r') as input_file:
	for line in input_file:
		matches = fullmatch(line_pattern, line.rstrip())

		own_numbers = set(split(list_separator_pattern, matches['own_numbers']))
		winning_numbers = set(split(list_separator_pattern, matches['winning_numbers']))

		if own_winning_numbers := own_numbers.intersection(winning_numbers):
			sum += pow(2, len(own_winning_numbers) - 1)

print(sum)

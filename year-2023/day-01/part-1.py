#!/usr/bin/env python3

from re import compile, fullmatch

line_pattern = compile(r'^[^\d]*(?P<first_digit>\d).*?(?:(?P<second_digit>\d)[^\d]*)?$')

sum = 0

with open('input.txt', 'r') as input_file:
	for line in input_file:
		if match := fullmatch(line_pattern, line.rstrip()):
			first_digit = match.group('first_digit')
			second_digit = match.group('second_digit') if match.group('second_digit') else match.group('first_digit')

			sum += int(f'{first_digit}{second_digit}')

print(sum)

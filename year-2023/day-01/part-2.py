#!/usr/bin/env python3

from re import compile, fullmatch, sub

number_mapping = {
	'one': 1,
	'two': 2,
	'three': 3,
	'four': 4,
	'five': 5,
	'six': 6,
	'seven': 7,
	'eight': 8,
	'nine': 9
}

def fix_numbers(match):
	if match:
		return f'{match.group(1)}{number_mapping[match.group(2)]}{match.group(3)}'

line_start_pattern = compile(r'^([^\d]*?)(one|two|three|four|five|six|seven|eight|nine)(.*)$')
line_end_pattern = compile(r'^(.*)(one|two|three|four|five|six|seven|eight|nine)([^\d]*?)$')
line_pattern = compile(r'^[^\d]*(?P<first_digit>\d).*?(?:(?P<second_digit>\d)[^\d]*)?$')

sum = 0

with open('input.txt', 'r') as input_file:
	for line in input_file:
		fixed_line = line.rstrip()

		fixed_line = sub(line_start_pattern, fix_numbers, fixed_line)
		fixed_line = sub(line_end_pattern, fix_numbers, fixed_line)

		if match := fullmatch(line_pattern, fixed_line):
			first_digit = match.group('first_digit')
			second_digit = match.group('second_digit') if match.group('second_digit') else match.group('first_digit')

			sum += int(f'{first_digit}{second_digit}')

print(sum)

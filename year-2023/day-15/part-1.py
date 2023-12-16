#!/usr/bin/env python3

strings: list[str] = []
total = 0

with open('input.txt', 'r') as input_file:
	for line in input_file:
		strings += line.rstrip().split(',')

for string in strings:
	sum = 0

	for char in string:
		sum = (sum + ord(char)) * 17 % 256

	total += sum

print(total)

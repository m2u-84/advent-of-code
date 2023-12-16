#!/usr/bin/env python3

from re import compile, fullmatch, split

sum = 0
cards: dict[int, int] = {}
card_ids: list[int] = []

def calculate_card_score(card_id: int):
	global sum
	global cards
	global card_ids

	if card_id in card_ids:
		sum += 1

		if matching_number_count := cards[card_id]:
			for id in range(card_id + 1, card_id + 1 + matching_number_count):
				calculate_card_score(card_id = id)

line_pattern = compile(r'^Card +(?P<card_id>\d+): (?P<own_numbers>[^\|]+?) \| (?P<winning_numbers>.+)$')
list_separator_pattern = compile(r' +')

with open('input.txt', 'r') as input_file:
	for line in input_file:
		matches = fullmatch(line_pattern, line.rstrip())

		if matches:
			own_numbers = set(split(list_separator_pattern, matches['own_numbers']))
			winning_numbers = set(split(list_separator_pattern, matches['winning_numbers']))

			own_winning_numbers = own_numbers.intersection(winning_numbers)
			cards[int(matches['card_id'])] = len(own_winning_numbers)

card_ids = cards.keys()

for card in cards:
	calculate_card_score(card_id = card)

print(sum)

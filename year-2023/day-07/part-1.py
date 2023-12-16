#!/usr/bin/env python3

from functools import cmp_to_key

hand_inventory: list[tuple[str, int]] = []

def determine_card_rank(card: str) -> int:
	match card:
		case '2':
			return 0
		case '3':
			return 1
		case '4':
			return 2
		case '5':
			return 3
		case '6':
			return 4
		case '7':
			return 5
		case '8':
			return 6
		case '9':
			return 7
		case 'T':
			return 8
		case 'J':
			return 9
		case 'Q':
			return 10
		case 'K':
			return 11
		case 'A':
			return 12
		case _:
			ValueError('Invalid card.')

def determine_hand_rank(hand: str) -> int:
	char_counts: dict[str, int] = {}

	for char in hand:
		if not char in char_counts:
			char_counts[char] = 0

		char_counts[char] += 1

	match tuple(sorted(char_counts.values(), reverse = True)):
		case (5,):            # Five of a kind
			return 6
		case (4, 1):          # Four of a kind
			return 5
		case (3, 2):          # Full house
			return 4
		case (3, 1, 1):       # Three of a kind
			return 3
		case (2, 2, 1):       # Two pair
			return 2
		case (2, 1, 1, 1):    # One pair
			return 1
		case (1, 1, 1, 1, 1): # High card
			return 0
		case _:
			ValueError('Invalid hand.')

def compare_hands(hand1: str, hand2: str) -> int:
	if hand1 != hand2:
		hand1_rank = determine_hand_rank(hand = hand1)
		hand2_rank = determine_hand_rank(hand = hand2)

		if hand1_rank < hand2_rank:
			return -1
		elif hand1_rank > hand2_rank:
			return 1
		else:
			for card_position in range(0, 5):
				card1_rank = determine_card_rank(card = hand1[card_position])
				card2_rank = determine_card_rank(card = hand2[card_position])

				if card1_rank < card2_rank:
					return -1
				elif card1_rank > card2_rank:
					return 1

	return 0

def compare_hand_bid_combos(
	hand_bid_combo1: tuple[str, int],
	hand_bid_combo2: tuple[str, int]
) -> int:
	return compare_hands(hand1 = hand_bid_combo1[0], hand2 = hand_bid_combo2[0])

with open('input.txt', 'r') as input_file:
	for line in input_file:
		(hand, bid) = line.rstrip().split(' ')
		hand_inventory.append((hand, int(bid)))

hand_inventory.sort(key = cmp_to_key(compare_hand_bid_combos))

sum = 0

for rank, card_bid_combo in enumerate(hand_inventory):
	sum += card_bid_combo[1] * (rank + 1)

print(sum)

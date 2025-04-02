import csv
import random

def round_ans(val):
    """
    Rounds numbers to nearest integer
    :param val: number to be rounded.
    :return: Rounded number (an integer)
    """
    var_rounded = (val * 2 + 1) // 2
    raw_rounded = f"{var_rounded:.0f}"
    return int(raw_rounded)

# Retrieve colours from csv file and put them in a list
file = open("gods.csv", "r")
all_gods = list(csv.reader(file, delimiter=","))
file.close()

# Remove the first row
all_gods.pop(0)

round_gods = []
round_scores = []

# Loop until we have four colours with different scores...
while len(round_gods) < 1:
    potential_god = random.choice(all_gods)

    # Get the score and check it's not a duplicate
    if potential_god[1] not in round_scores:
        round_gods.append(potential_god[2])
        round_scores.append(potential_god[0])

print(round_gods)
print(round_scores)

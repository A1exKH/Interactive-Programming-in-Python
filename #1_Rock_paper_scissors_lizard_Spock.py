# Mini-project #1 - Rock_paper_scissors_lizard_Spock

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

def num_to_name(num):
    # convert number to a name
    if num == 0:
        result = "rock"
    elif num == 1:
        result = "Spock"
    elif num == 2:
        result = "paper"
    elif num == 3:
        result = "lizard"
    elif num == 4:
        result = "scissors"
    return result

def name_to_num(name):
    # convert name to number
    if name == "rock":
        result = 0
    elif name == "Spock":
        result = 1
    elif name == "paper":
        result = 2
    elif name == "lizard":
        result = 3
    elif name == "scissors":
        result = 4
    return result

def rpsls(name):
    # convert name to player_number using name_to_num
    # compute random guess for comp_number using random.randrange()
    # compute difference of player_number and comp_number modulo five
    # use if/elif/else to determine winner
    # convert comp_number to name using num_to_name
    # print results

    player_number = name_to_num(name)
    comp_number = random.randrange(0, 5)

    print "Player chooses", name
    print "Computer chooses", num_to_name(comp_number)

    if (comp_number + 1) % 5 == player_number:
        print "Player wins!"
    elif (comp_number + 2) % 5 == player_number:
        print "Player wins!"
    elif comp_number == player_number:
        print "Player and computer tie!"
    else:
        print "Computer wins!"

    print ""

# tests
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
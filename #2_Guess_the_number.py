# Mini-project #2 - Guess the number

# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

# initialize global variables
num_range = 100

# helper function to start new game
def new_game():
    global num_range, secret_num, guesses_left
    secret_num = 0
    guesses_left = 0

    if num_range == 100:
        guesses_left = 7
    else:
        guesses_left = 10

    secret_num = random.randrange(0, num_range)
    print "New game. The range is from 0 to " + str(num_range) + "."
    print "Number of remaining guesses is " + str(guesses_left) + "\n"


# define event handlers for control panel
def range100():
    global num_range
    num_range = 100 # button that changes range to range [0,100) and restarts
    new_game()

def range1000():
    global num_range
    num_range = 1000 # button that changes range to range [0,1000) and restarts
    new_game()

def input_guess(guess):
    # main game logic
    global guesses_left, secret_num

    won = False
    print "You guessed: ",guess
    guesses_left -= 1
    print "Number of remaining guesses is ", guesses_left
    int_guess = int(guess)

    if int_guess == secret_num:
        won = True
    elif int_guess > secret_num:
        result = "Lower!"
    else:
        result = "Higher!"

    if won:
        print "That is correct!\n"
        new_game()
    elif guesses_left == 0:
        print "Game over! The secret number: "+str(secret_num)+"\n"
        new_game()
    else:
        print result

# create frame
f = simplegui.create_frame("Game: Guess the number!", 250, 250)
f.set_canvas_background('Green')

# register event handlers for control elements
f.add_button("Range is [0, 100)", range100, 100)
f.add_button("Range is [0, 1000)", range1000, 100)
f.add_input("Enter your guess", input_guess, 100)

# call new_game and start frame
new_game()
f.start()
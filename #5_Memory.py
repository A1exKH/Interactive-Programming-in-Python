# Mini-project #5 - Memory
# http://www.codeskulptor.org/#user41_J4JOApkrKv_4.py

import simplegui
import random

card_index1 = card_index2 = 0

# helper function to initialize globals
def new_game():
    global turns, deck, exposed, state
    state = 0
    deck = [i%8 for i in range(16)]
    random.shuffle(deck)
    exposed = [False for i in range(16)]
    turns = 0
    label.set_text("Turns = " + str(turns))

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global turns, state, deck, card_index1, card_index2, exposed
    player_choise = pos[0] // 50
    if state == 0:
        card_index1 = player_choise
        exposed[card_index1] = True
        state = 1
    elif state == 1:
        if not exposed[player_choise]:
            card_index2 = player_choise
            exposed[card_index2] = True
            state = 2
            turns += 1
    elif state == 2:
        if not exposed[player_choise]:
            if deck[card_index1] == deck[card_index2]:
                pass
            else:
                exposed[card_index1] = exposed[card_index2] = False
            card_index1 = player_choise
            exposed[card_index1] = True
            state = 1
    label.set_text("Turns = " + str(turns))

# cards are logically 50x100 pixels in size
def draw(canvas):
    global deck, exposed
    for card in range(len(deck)):
        if exposed[card]:
            canvas.draw_text(str(deck[card]), (10 + 50 * card, 60), 50, 'Red')
        else:
            x = 50 * card # coefficient
            canvas.draw_polygon([[0 + x, 0], [50 + x, 0], [50 + x, 100], [0 + x, 100]], 2, 'Black', 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.set_canvas_background('White')
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
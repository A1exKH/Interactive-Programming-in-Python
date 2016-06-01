# Mini-project #4 - Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
LEFT = False
RIGHT = True

#paddles
PADDLE1_POS = HEIGHT / 2.5
PADDLE2_POS = HEIGHT / 2.5
PADDLE1_VEL = PADDLE2_VEL = 0
PADDLE_VEL = 5

# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = [HALF_WIDTH, HALF_HEIGHT]
ball_vel = [0,1]

# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [HALF_WIDTH, HALF_HEIGHT]
    ball_vel[0] = -random.randrange(120,240) / 100
    if direction == True:
        ball_vel[0] *= -1
    ball_vel[1] = -random.randrange(60, 180) / 100

# define event handlers
def new_game():
    global PADDLE1_POS, PADDLE2_POS, score1, score2
    score1 = score2 = 0
    spawn_ball(0)
    PADDLE1_POS = HEIGHT / 2.5
    PADDLE2_POS = HEIGHT / 2.5

def draw(c):
    global score1, score2, PADDLE1_POS, PADDLE2_POS, ball_pos, ball_vel, PADDLE1_VEL, PADDLE2_VEL

    # draw mid line and gutters
    c.draw_line([HALF_WIDTH, 0], [HALF_WIDTH, HEIGHT], 1, "WHITE")
    c.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "WHITE")
    c.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "WHITE")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH) or ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS):
        ball_vel[0] *= -1

        if (ball_pos[0] > HALF_WIDTH):
            if (ball_pos[1] < PADDLE2_POS or ball_pos[1] > PADDLE2_POS + PAD_HEIGHT):
                score1 += 1
                spawn_ball(LEFT)
            else: ball_vel[0] += .1 * ball_vel[0]

        if (ball_pos[0] < HALF_WIDTH):
            if (ball_pos[1] < PADDLE1_POS or ball_pos[1] > PADDLE1_POS + PAD_HEIGHT):
                score2 += 1
                spawn_ball(RIGHT)
            else: ball_vel[0] += .1 * ball_vel[0]

    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] *= -1

    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "WHITE", "GREEN")

    # update paddle's vertical position, keep paddle on the screen
    if (PADDLE1_POS <= HEIGHT - PAD_HEIGHT and PADDLE1_VEL > 0) or (PADDLE1_POS >= 0 and PADDLE1_VEL < 0) :
        PADDLE1_POS += PADDLE1_VEL
    elif (PADDLE2_POS <= HEIGHT - PAD_HEIGHT and PADDLE2_VEL > 0) or (PADDLE2_POS >= 0 and PADDLE2_VEL < 0) :
        PADDLE2_POS += PADDLE2_VEL

    # draw paddles
    c.draw_polygon([[0, PADDLE1_POS], [PAD_WIDTH, PADDLE1_POS], [PAD_WIDTH, (PADDLE1_POS) + PAD_HEIGHT], [0, (PADDLE1_POS) + PAD_HEIGHT]], 1, "green", "white")
    c.draw_polygon([[WIDTH, PADDLE2_POS], [WIDTH - PAD_WIDTH, PADDLE2_POS], [WIDTH - PAD_WIDTH, PADDLE2_POS + PAD_HEIGHT], [WIDTH, PADDLE2_POS + PAD_HEIGHT]], 1, "green", "white")
    # draw scores
    c.draw_text(str(score1), [225, 100], 60, "WHITE")
    c.draw_text(str(score2), [350, 100], 60, "WHITE")

def keydown(key):
    global PADDLE1_VEL, PADDLE2_VEL, PADDLE_VEL

    #player1
    if key == simplegui.KEY_MAP["w"]:
        PADDLE1_VEL = -PADDLE_VEL
    elif key == simplegui.KEY_MAP["s"]:
        PADDLE1_VEL = PADDLE_VEL

    #player2
    if key == simplegui.KEY_MAP["down"]:
        PADDLE2_VEL = PADDLE_VEL
    elif key == simplegui.KEY_MAP["up"]:
        PADDLE2_VEL = -PADDLE_VEL

def keyup(key):
    global PADDLE1_VEL, PADDLE2_VEL, PADDLE_VEL

    #player1
    if key == simplegui.KEY_MAP["w"]:
        PADDLE1_VEL = 0
    elif key == simplegui.KEY_MAP["s"]:
        PADDLE1_VEL = 0

    #player2
    if key == simplegui.KEY_MAP["down"]:
        PADDLE2_VEL = 0
    elif key == simplegui.KEY_MAP["up"]:
        PADDLE2_VEL = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 200)

# start frame
new_game()
frame.start()
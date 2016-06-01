# Mini-project #2 - Stopwatch: The Game

import simplegui

# define global variables
interval = 100
count = 0
total_stops = 0
successful_stops = 0
stop = True

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tenth_sec = (t) % 10
    sec = int(t / 10) % 10
    minutes = int(t / 600) % 600
    ten_min = int(t / 100) % 6
    time = str(minutes) + ":" + str(ten_min) + str(sec) + "." + str(tenth_sec)
    return time

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global count, stop
    stop = False
    timer.start()

def stop():
    global total_stops, successful_stops, stop
    if stop == False :
        if count % 10 == 0 and count != 0 :
            successful_stops += 1
            total_stops += 1
        elif count != 0 :
            total_stops += 1
        stop = True
        timer.stop()

def reset():
    global count, successful_stops, stop, total_stops
    count = 0
    total_stops = 0
    successful_stops = 0
    stop = True
    timer.stop()

# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(count), (80, 125), 42, "WHITE")
    canvas.draw_text(str(successful_stops) + '/' + str(total_stops), (190, 30), 24, "BLACK")

# Create a frame
frame = simplegui.create_frame("Stopwatch game", 250, 250)
frame.set_canvas_background('GREEN')

# Register event handlers
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)

# Start the frame animation
frame.start()
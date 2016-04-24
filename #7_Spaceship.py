# Mini-project #7 - Spaceship
#http://www.codeskulptor.org/#user41_3lGCo432p0_1.py
import simplegui
import math
import random

# globals for user interface
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CANVAS = [CANVAS_WIDTH,CANVAS_HEIGHT]
CANVAS_CENTER = [CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2]
FRICTION_CONST = 0.1
ANGLE_INCR = 0.1
score = 0
lives = 3
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = []

    def draw(self,canvas):
        if self.thrust:
            thruster_img_center = (self.image_center[0] + 90, self.image_center[1])
            canvas.draw_image(self.image, thruster_img_center, self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.play()
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.rewind()

    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % CANVAS_WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % CANVAS_HEIGHT
        self.forward = angle_to_vector(self.angle)
        self.vel[0] *= (1 - FRICTION_CONST)
        self.vel[1] *= (1 - FRICTION_CONST)
        if self.thrust:
            self.vel[0] += self.forward[0]
            self.vel[1] += self.forward[1]

    def incr_vel(self):
        self.angle_vel += ANGLE_INCR

    def decr_vel(self):
        self.angle_vel -= ANGLE_INCR

    def enable_thrusters(self, flag):
        self.thrust = flag

    def shoot(self):
        global  a_missile
        missile_pos = [self.pos[0] + self.radius * self.forward[0], self.pos[1] + self.radius * self.forward[1]]
        missile_vel = [self.vel[0] + 3 * self.forward[0], self.vel[1] + 3 * self.forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[0] += self.angle_vel
        self.vel[1] += self.angle_vel
        self.angle += self.angle_vel

def draw(canvas):
    global time
    # animiate background
    time += 1
    wtime = (time / 4) % CANVAS_WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), CANVAS_CENTER, CANVAS)
    canvas.draw_image(debris_image, center, size, (wtime - CANVAS_CENTER[0], CANVAS_CENTER[1]), CANVAS)
    canvas.draw_image(debris_image, center, size, (wtime + CANVAS_CENTER[0], CANVAS_CENTER[1]), CANVAS)
    canvas.draw_text("Score: " + str(score), [50, 30], 30, "White")
    canvas.draw_text("Lives: " + str(lives), [650, 30], 30, "White")

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()

def keydown_handler(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decr_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.incr_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.enable_thrusters(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def keyup_handler(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.incr_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decr_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.enable_thrusters(False)

# timer handler that spawns a rock
def rock_spawner():
    global a_rock
    rock_pos = [random.randint(0, CANVAS_WIDTH), random.randint(0, CANVAS_HEIGHT)]
    rock_vel = [random.randint(-1, 1), random.randint(-1, 1)]
    rock_ang = random.randint(-1, 1)
    rock_ang_vel = random.randint(-1, 1) / 100 + 0.1
    a_rock = Sprite(rock_pos, rock_vel, rock_ang, rock_ang_vel, asteroid_image, asteroid_info)

# initialize frame
frame = simplegui.create_frame("Asteroids", CANVAS_WIDTH, CANVAS_HEIGHT)

# initialize ship and two sprites
my_ship = Ship(CANVAS_CENTER, [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([CANVAS_WIDTH / 3, CANVAS_HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * CANVAS_WIDTH / 3, 2 * CANVAS_HEIGHT / 3], [-1, 1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
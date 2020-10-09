"""
Land the Rocket!

You are working for NASA and need to land a rocket on Mars for them! You are
given a few controls to work with. At every iteration you can rotate the
rocket and power on the engine to give it thurst in the direction it is
pointing. Help land the rocket safely and in a timely manner!

Inputs:
    On the first turn you are given the rockets position and a list of points
    designating what the terrain looks like. For example:

    ([30, 50], [(0, 10), (10, 5), (40, 20), (60, 0), (100, 0)])
         ^                            ^
     rocket pos                terrain points

    It's given that the first point is (0, y) and the last point is (100, y),
    for some 0 <= y <= 100. Anything above y=100 is considered the ceiling;
    don't fly too high or you'll crash! The goal is to get the rocket to y=0
    with an overall velocity of less than 3. Also, you can't land on slopes,
    so it has to end up somewhere flat.

    --

    On every subsequent turn you are given the rocket's position, angle, the
    components of its velocity (in the x and y directions), and whether or not
    your rocket crashed. For example:

    ([30, 50],      10,     3,     7,     False)
         ^           ^      ^      ^        ^
    rocket pos     angle    vx     vy    crashed?

    The angle is measured in degrees. 0 corresponds to the rocket pointing
    straight up, and positive angles go to the right. The angle will be between
    -180 and 180 degrees.

    Hopefully the velocity components are self explanatory.

    If your rocket crashes then that will be its last turn. Trying to take
    another turn will result in an error. Also, the rocket will run out of gas
    and crash if you take more than 200 turns so make sure you land it quickly!
    
Run a turn:
    To get the inputs from the turn, run
    
        rocket.get_inputs()

    To perform your actions, run

        rocket.run_turn(d_angle, power)

    d_angle is the change in the angle of the rocket. It can be anywhere from
    -5 to 5 (if you put in something too large or small it will constricted to
    that range). The power can be anywhere from 0 to 5.
"""

import matplotlib.pyplot as plt
import random
import math
random.seed(4)

plt.ion()
fig, ax = plt.subplots()
sc = ax.scatter([], [], s=64, color="green")
plt.xlim(-10, 110)
plt.ylim(-10, 110)

class Map():
    def __init__(self, points=None):
        # You can change these and make your own maps.
        if(points is None):
            self.points = [(0, 10), (10, 5), (40, 20), (60, 0), (100, 0)]
        else:
            self.points = points

    def draw(self):
        x, y = zip(*self.points)
        x = [-10, 0] + list(x) + [100, 110]
        y = [100, 100] + list(y) + [100, 100]
        plt.fill_between(x, y, color='red')
        plt.fill_between([-10, 110], [110, 110], [100, 100], color='red')
        plt.fill_between([-10, 110], [0, 0], [-10, -10], color='red')
        
        fig.canvas.draw_idle()
        

def check_collision(a, b, c, d):
    denom = ((b[0] - a[0]) * (d[1] - c[1])) - ((b[1] - a[1]) * (d[0] - c[0]))
    num1 = ((a[1] - c[1]) * (d[0] - c[0])) - ((a[0] - c[0]) * (d[1] - c[1]))
    num2 = ((a[1] - c[1]) * (b[0] - a[0])) - ((a[0] - c[0]) * (b[1] - a[1]))
    if (denom == 0):
        return num1 == 0 and num2 == 0;

    r = num1 / denom
    s = num2 / denom;

    return (r >= 0 and r <= 1) and (s >= 0 and s <= 1);

class Rocket():
    def __init__(self, points=None, pos=None):
        self.map = Map(points)
        if(pos is None):
            self.pos = [30, 50]
        else:
            self.pos = pos
        self.vx = 0
        self.vy = 0
        self.angle = 0
        self.crashed = False
        self.won = False
        self.turn = 0
        self.positions = [self.pos[:]]

    def get_inputs(self):
        if turn == 0:
            return self.pos[:], [p[:] for p in self.map.points]
        else:
            return self.pos[:], self.angle, self.vx, self.vy, self.crashed

    def run_turn(self, d_angle, power):
        if self.crashed:
            raise Exception("You already crashed, you can't keep moving!")
        
        if d_angle > 5:
            d_angle = 5
        elif d_angle < -5:
            d_angle = -5
        self.angle += d_angle
        prev_pos = self.pos[:]
        self.vx += math.sin(self.angle) * power
        self.vy += math.cos(self.angle) * power - 1 # -1 for gravity
        self.pos[0] += self.vx
        self.pos[1] += self.vy
        for i in range(len(self.map.points)-1):
            if check_collision(self.map.points[i], self.map.points[i+1], self.pos, prev_pos):
                self.crashed = True
                if self.map.points[i][0] == 0 and self.map.points[i+1][0] == 0 and \
                   self.vx ** 2 + self.vy ** 2 < 3 ** 2:
                    self.won = True

                break
        self.positions.append(self.pos[:])
        
        self.turn += 1
        if self.turn == 200:
            self.crashed = True

    def draw(self):
        sc.set_offsets(self.positions)
        plt.arrow(self.pos[0], self.pos[1], self.vx, self.vy, head_width = 1.5, color="black")
        self.map.draw()

r = Rocket()
while not r.crashed:
    r.draw()
    r.run_turn(random.randint(-5, 5), random.randint(0, 5))

if r.won:
    print("Congrats, you win!")
else:
    print("Oops, you crashed!")

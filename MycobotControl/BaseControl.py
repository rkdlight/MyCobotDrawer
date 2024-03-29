from pymycobot.mycobot import MyCobot
import time

class MyCobotInterface:

    def __init__(self, port='COM5', scale=None, speed=50, plt=None):
        self.speed = speed
        if scale is None:
            self.scale = [1, 1]
        else:
            self.scale = scale
        self.init_z = 0
        self.scale = scale
        self.mc = MyCobot('COM5', 115200)
        time.sleep(0.5)
        self.mc.set_fresh_mode(0) # Execute instructions sequentially in the form of a queue.
        time.sleep(0.5)
        self.last_coords = []
        self.plt = plt

    def start(self, init_x=80, init_y=80, init_z=100):
        self.init_z = init_z
        self.mc.send_coords([init_x, init_y, init_z, -180, 0, 0], self.speed)
        self.last_coords = [init_x, init_y, init_z, -180, 0, 0]
        time.sleep(2)

    def draw_to(self, x, y, step=0):
        x = self.scale[0]*x+160
        y = self.scale[1]*y
        self.mc.send_coords([x, y, self.init_z, -180, 0, 0], self.speed)
        self.last_coords = [x, y, self.init_z, -180, 0, 0]
        if self.plt is not None:
            self.plt.scatter(x, y)
            self.plt.pause(0.05)
        time.sleep(0.5)


    def move_to(self, x, y, step=0):
        x = self.scale[0] * x+160
        y = self.scale[1] * y
        coords = self.last_coords
        coords[2] += 30
        self.mc.send_coords(coords, self.speed)
        time.sleep(2)
        coords[0] = x
        coords[1] = y
        self.mc.send_coords(coords, self.speed)
        time.sleep(2)
        coords[2] -= 30
        self.mc.send_coords(coords, self.speed)
        self.last_coords = coords
        if self.plt is not None:
            self.plt.scatter(x, y)
            self.plt.pause(0.05)
        time.sleep(2)

    @property
    def current_coords(self):
        return self.last_coords[0], self.last_coords[1]


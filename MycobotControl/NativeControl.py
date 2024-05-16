import time
from .BaseControl import BaseInterface


class NativeInterface(BaseInterface):

    def __init__(self, port='COM5', scale=None, speed=50, plt=None, up_moving=50):
        super().__init__(port, scale, speed, plt, up_moving)

    def draw_to(self, x, y):
        x = self.scale[0] * x + self.init_x
        y = self.scale[1] * y + self.init_y
        self.mc.send_coords([x, y, self.init_z, -180, 0, 0], self.speed)
        self.last_coords = [x, y, self.init_z, -180, 0, 0]
        if self.plt is not None:
            self.plt.scatter(x, y)
            self.plt.pause(0.05)
        time.sleep(1)

    def move_to(self, x, y, step=0):
        x = self.scale[0] * x + self.init_x
        y = self.scale[1] * y + self.init_y
        coords = self.last_coords
        coords[2] += 30
        self.mc.send_coords(coords, self.speed)
        time.sleep(1)
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
        time.sleep(1)

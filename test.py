import time

import matplotlib.pyplot as plt
from SVGParse.Parse import parse_svg
from MycobotControl import MyCobotInterface, PolarMyCobotInterface
from pprint import pprint


class TestInterface:

    def __init__(self, port='COM5', scale=None, speed=50, plt=None):

        if scale is None:
            self.scale = [1, 1]
        else:
            self.scale = scale

        self.init_z = 0
        self.last_coords = []
        self.x_array = []
        self.y_array = []
        self.k_array = []
        self.plt = plt

    def start(self, init_x=100, init_y=0, init_z=100):
        self.init_z = init_z
        self.x_array.append(init_x)
        self.y_array.append(init_y)
        self.last_coords = [init_x, init_y, init_z, -180, 0, 0]

    def draw_to(self, x, y, step=0):
        x = self.scale[0] * x
        y = self.scale[1] * y
        self.x_array.append(x)
        self.y_array.append(y)
        self.k_array.append(round(step, 2))
        self.last_coords = [x, y, self.init_z, -180, 0, 0]
        if self.plt is not None:
            self.plt.scatter(x, y)
            self.plt.pause(0.05)


    def move_to(self, x, y, step=0):
        x = self.scale[0] * x
        y = self.scale[1] * y
        self.k_array.append(round(step,2))
        coords = self.last_coords
        coords[0] = x
        coords[1] = y
        self.x_array.append(x)
        self.y_array.append(y)
        self.last_coords = coords
        if self.plt is not None:
            self.plt.scatter(x, y)
            self.plt.pause(0.05)



    @property
    def current_coords(self):
        return self.last_coords[0], self.last_coords[1]




if __name__ == '__main__':
    objects = parse_svg("test_curve.svg")

    # Cobot drawing
    interface = TestInterface(port="COM5", scale=[0.10, 0.10], speed=50, plt=plt)
    interface.start(160, 0, 18)
    draw_res = 50

    plt.axis([0, 200, 0, 200])

    for obj in objects:
        for element in obj:
            pprint(element)
            element.render(interface, draw_res)

    plt.show()
    # from pymycobot.mycobot import MyCobot
    # import time
    #
    # mc = MyCobot('COM5', 115200)
    # time.sleep(0.5)
    # mc.set_fresh_mode(0)
    # time.sleep(0.5)
    #
    # angles = None
    # while angles is None:
    #     angles = mc.get_servo_voltages()
    #     time.sleep(0.5)
    # print(angles)

    # Base - [0...4096]
    # Fact
    # J1 - [105...2045...3971]
    # J2 - [474...2038...3637]
    # J3 - [282...2037...3789]
    # J4 - [271...2047...3826]
    # J5 - [97...1995...3839]
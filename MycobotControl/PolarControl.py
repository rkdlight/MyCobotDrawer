from pymycobot.mycobot import MyCobot
import time
from math import atan2
from math import sqrt, sin, cos, acos, asin, pi, degrees

a1 = 131.56
a2 = 110.4
a3 = 96
a4 = 73.18
a5 = 67



class PolarMyCobotInterface:

    def __init__(self, port='COM5', scale=None):
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

    def __get_joints_angels(self, r, z=0):
        CJ4 = sqrt((z + a5) ** 2 + (r - a4) ** 2)
        J2J4 = sqrt((a1 - a5 - z) ** 2 + (r - a4) ** 2)
        cosJ3 = (a2 ** 2 + a3 ** 2 - J2J4 ** 2) / (2 * a2 * a3)

        sinCJ2J4 = (r - a4) / J2J4
        cosJ3J2J4 = (a2 ** 2 + J2J4 ** 2 - a3 ** 2) / (2 * a2 * J2J4)
        J2 = -(pi - asin(sinCJ2J4) - acos(cosJ3J2J4))
        j3sqrtreangle = pi / 2 + J2
        J3x = cos(j3sqrtreangle) * a2
        J3y = sin(j3sqrtreangle) * a2 + a1
        J5x = r
        J5y = a5 + z
        J3J5 = sqrt((J5x - J3x) ** 2 + (J5y - J3y) ** 2)
        J3 = -(pi - acos(cosJ3))
        cosJ3J4J5 = (a3 ** 2 + a4 ** 2 - J3J5 ** 2) / (2 * a3 * a4)
        J3J4J5 = acos(cosJ3J4J5)
        J4 = pi - J3J4J5

        return degrees(J2), degrees(J3), degrees(J4)
    def start(self, init_x=80, init_y=80, init_z=100):
        self.init_z = init_z
        self.mc.send_coords([init_x, init_y, init_z, -180, 0, 0], 50)
        self.last_coords = [init_x, init_y, init_z, -180, 0, 0]
        time.sleep(2)

    def draw_to(self, x, y, step=0):
        x = self.scale[0]*x+160
        y = self.scale[1]*y
        thetha = degrees(atan2(y, x))
        r = sqrt(x**2 + y**2)
        J2, J3, J4 = self.__get_joints_angels(r)
        self.mc.send_angles([thetha, J2, J3, J4, 0, 0], 50)
        self.last_coords = [x, y, self.init_z, -180, 0, 0]
        time.sleep(0.5)

    def move_to(self, x, y):
        global a5
        a5 += 30
        x = self.scale[0] * x + 160
        y = self.scale[1] * y
        thetha = degrees(atan2(y, x))

        r = sqrt(x ** 2 + y ** 2)
        J2, J3, J4 = self.__get_joints_angels(r)
        self.mc.send_angles([thetha, J2, J3, J4, 0, 0], 50)
        self.last_coords = [x, y, self.init_z, -180, 0, 0]
        time.sleep(0.5)
        a5 -= 30
        r = sqrt(x ** 2 + y ** 2)
        J2, J3, J4 = self.__get_joints_angels(r)
        self.mc.send_angles([thetha, J2, J3, J4, 0, 0], 50)
        self.last_coords = [x, y, self.init_z, -180, 0, 0]
        time.sleep(0.5)
    @property
    def current_coords(self):
        return self.last_coords[0]/self.scale[0], self.last_coords[1]/self.scale[1]
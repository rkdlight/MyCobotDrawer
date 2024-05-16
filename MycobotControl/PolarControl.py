from pprint import pprint

import time
import math
from .BaseControl import BaseInterface



class PolarInterface(BaseInterface):

    def __init__(self, port='COM5', scale=None, speed=50, plt=None, up_moving=50):
        super().__init__(port, scale, speed, plt, up_moving)
        self.q1, self.q2, self.q3, self.q4, self.q5, self.q6 = 0, 0, 0, 0, 0, 0
        self.Tm = 30.0
        self.a1 = 131.56
        self.L2 = 66.39
        self.a4 = 73.18
        self.a5 = 43.6
        self.a2 = 110.4
        self.a3 = 96
        self.PI = math.pi

    def __get_joints_angels(self, x, y, z):
        
        r = math.sqrt(x * x + y * y)
        pravka = math.acos((-self.L2 ** 2 + 2 * r ** 2) / (2 * r * r)) * 180 / self.PI


        self.q1 = (self.PI / 2 + (math.atan2(y, x) - (self.PI / 2))) * 180 / self.PI + pravka
        self.q6 = self.q1

        a13 = math.sqrt((r - self.a4) ** 2 + (self.a1 - (z + self.a5)) ** 2)
        if a13 == self.a2 + self.a3:
            self.q3 = 0
        elif a13 > self.a2 + self.a3:
            raise "Error; A13 > a2+a3"

        else:
            self.q3 = math.acos((-a13 ** 2 + self.a2 ** 2 + self.a3 ** 2) / (2 * self.a2 * self.a3)) - self.PI
        if self.q3 > 0:
            raise "Error; q3 > 0"


        corner213 = math.acos((-self.a3 ** 2 + self.a2 ** 2 + a13 ** 2) / (2 * self.a2 * a13))
        if (self.a5 + z) >= self.a1:
            self.q2 = -(self.PI / 2 - corner213 - math.acos((r - self.a4) / a13))
        else:
            self.q2 = -(self.PI / 2 - (corner213 - math.acos((r - self.a4) / a13)))
        if self.q2 > 0:
            raise "Error; q2 > 0"


        j3ang = self.PI / 2 + self.q2
        J3x = math.cos(j3ang) * self.a2
        J3y = math.sin(j3ang) * self.a2 + self.a1
        a35 = math.sqrt((r - J3x) ** 2 + ((self.a5 + z) - J3y) ** 2)
        self.q4 = self.PI - math.acos((-a35 ** 2 + self.a3 ** 2 + self.a4 ** 2) / (2 * self.a4 * self.a3))

        if self.q4 < 0:
            raise "Error; q4 < 0"

        self.q2 *= 180 / self.PI
        self.q2 = self.q2
        self.q3 *= 180 / self.PI
        self.q3 = self.q3
        self.q4 *= 180 / self.PI
        self.q4 = self.q4
        self.q5 = 0

        print("Optimal joint angles:")
        print("q1: ", self.q1)
        print("q2: ", self.q2)
        print("q3: ", self.q3)
        print("q4: ", self.q4)
        print("q5: ", self.q5)
        print("q6: ", self.q6)
        return list((self.q1, self.q2, self.q3, self.q4, self.q5, self.q6))


    def draw_to(self, x, y):
        x = self.scale[0] * x + self.init_x
        y = self.scale[1] * y + self.init_y

        angles = self.__get_joints_angels(x, y, self.init_z)

        self.mc.send_angles(angles, self.speed)

        self.last_coords = [x, y, self.init_z, -180, 0, 0]

        if self.plt is not None:
            self.plt.scatter(x, y)
            self.plt.pause(0.05)

        time.sleep(0.5)

    def move_to(self, x, y, step=0):
        x = self.scale[0] * x + self.init_x
        y = self.scale[1] * y + self.init_y
        cords = self.last_coords
        cords[2] += self.up_moving

        angles = self.__get_joints_angels(cords[0], cords[1], cords[2])
        self.mc.send_angles(angles, self.speed)
        time.sleep(2)

        cords[0] = x
        cords[1] = y

        angles = self.__get_joints_angels(cords[0], cords[1], cords[2])
        self.mc.send_angles(angles, self.speed)
        time.sleep(2)

        cords[2] -= self.up_moving
        angles = self.__get_joints_angels(cords[0], cords[1], cords[2])
        self.mc.send_angles(angles, self.speed)
        time.sleep(2)

        self.last_coords = cords
        if self.plt is not None:
            self.plt.scatter(x, y)
            self.plt.pause(0.05)
        time.sleep(2)


        

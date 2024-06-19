
import time
import math
from .BaseControlUnity import BaseInterfaceUnity



class XinInterfaceUnity(BaseInterfaceUnity):

    def __init__(self, port='COM5', scale=None, speed=50, plt=None, up_moving=50):
        super().__init__(port, scale, speed, plt, up_moving)
        self.init_z = -80
    def __get_joints_angels(self, x, y, z):
        R = [[0, 1, 0, 0],
             [1, 0, 0, 0],
             [0, 0, -1, 0],
             [0, 0, 0, 1]]
        y = -y
        # Calculate xc, yc, and r
        xc = x - (self.L6 * R[0][2])
        yc = y - (self.L6 * R[1][2])
        zc = z
        r = math.sqrt(xc ** 2 + yc ** 2)

        # Calculate theta1
        if xc <= 0 and xc < -self.L2 and yc >= -self.L2:
            theta1 = -180 + math.degrees(math.atan2(abs(xc), abs(yc))) + math.degrees(math.acos(self.L2 / r))
        elif xc <= 0 and xc < -self.L2 and yc < -self.L2:
            theta1 = 90 - math.degrees(math.atan2(abs(xc), abs(yc))) - math.degrees(math.asin(self.L2 / r))
        elif xc > 0 and xc < self.L2 and yc < 0:
            theta1 = 90 - math.degrees(math.atan2(abs(xc), abs(yc))) - math.degrees(math.asin(self.L2 / r))
        elif xc > 0 and xc > self.L2 and yc < 0:
            theta1 = math.degrees(math.atan2(abs(xc), abs(yc))) + math.degrees(math.acos(self.L2 / r))
        else:
            theta1 = -90 - math.degrees(math.atan2(abs(xc), abs(yc))) - math.degrees(math.asin(self.L2 / r))

        # Calculate theta5
        if y >= yc:
            theta5 = math.degrees(math.atan2(z - zc, yc - y))
        elif y < yc and z <= zc:
            theta5 = -math.degrees(math.atan2(y - yc, zc - z)) - 90
        else:
            theta5 = math.degrees(math.atan2(y - yc, z - zc)) + 90

        # Calculate theta6 (assuming same rotation as theta1)
        theta6 = theta1

        # Calculate q11, L11, L12, z2
        q11 = math.acos(self.L2 / r)
        L11 = r * math.sin(q11)
        L12 = L11 - self.L5
        z2 = zc

        can1 = (L12 ** 2 + z2 ** 2 + self.Ld2 ** 2 - self.Ld3 ** 2) / (2 * self.Ld2 * math.sqrt(L12 ** 2 + z2 ** 2))
        theta2 = 180 - math.degrees(math.atan2(z2, L12)) - math.degrees(math.acos(can1))

        # Calculate can2 and theta3
        can2 = (self.Ld2 ** 2 + self.Ld3 ** 2 - L12 ** 2 - z2 ** 2) / (2 * self.Ld2 * self.Ld3)
        theta3 = 180 - math.degrees(math.acos(can2))

        # Calculate theta4
        theta4 = 180 - theta2 - theta3 + 90

        # Store joint angles
        self.q1 = 180 - theta1
        if self.q1 > 180:
            self.q1 = self.q1 - 360
        elif self.q1 < -180:
            self.q1 = 360 + self.q1
        self.q2 = 90 - theta2
        self.q3 = -theta3
        self.q4 = 90 - theta4
        # self.q5 = theta5+90
        self.q5 = 0
        self.q6 = self.q1

        result = [self.q1, -self.q2, -self.q3, -self.q4, self.q5, self.q6]

        return list(map(lambda x: "{:.2f}".format(x), result))

    def draw_to(self, x, y):
        x = self.scale[0] * x + self.init_x
        y = -self.scale[1] * y + self.init_y

        angles = self.__get_joints_angels(x, y, self.init_z)
        message = ".ModRobot:" + ",".join(angles)
        self.s.sendall(message.encode("utf-8"))

        self.last_coords = [x, y, self.init_z]

        if self.plt is not None:
            self.plt.scatter(x, y)
            self.plt.pause(0.05)

        time.sleep(0.5)

    def move_to(self, x, y, step=0):
        x = self.scale[0] * x + self.init_x
        y = -self.scale[1] * y + self.init_y
        cords = self.last_coords
        cords[2] += self.up_moving

        angles = self.__get_joints_angels(cords[0], cords[1], cords[2])

        message = ".ModRobot:" + ",".join(angles)
        self.s.sendall(message.encode("utf-8"))
        time.sleep(2)

        cords[0] = x
        cords[1] = y

        angles = self.__get_joints_angels(cords[0], cords[1], cords[2])
        message = ".ModRobot:" + ",".join(angles)
        self.s.sendall(message.encode("utf-8"))
        time.sleep(2)

        cords[2] -= self.up_moving
        angles = self.__get_joints_angels(cords[0], cords[1], cords[2])
        message = ".ModRobot:" + ",".join(angles)
        self.s.sendall(message.encode("utf-8"))
        time.sleep(2)

        self.last_coords = cords
        if self.plt is not None:
            self.plt.scatter(x, y)
            self.plt.pause(0.05)
        time.sleep(2)





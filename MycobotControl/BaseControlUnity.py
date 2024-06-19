from pprint import pprint

import time
import math
from .BaseControl import BaseInterface
import socket


class BaseInterfaceUnity(BaseInterface):

    def __init__(self, port='COM5', scale=None, speed=50, plt=None, up_moving=50):
        if scale is None:
            self.scale = [1, 1]
        else:
            self.scale = scale
        self.init_z = 0
        self.init_x = 0
        self.init_y = 0
        self.last_coords = [0, 0, 0]
        self.plt = plt
        self.up_moving = up_moving
        self.q1, self.q2, self.q3, self.q4, self.q5, self.q6 = 0, 0, 0, 0, 0, 0
        self.L1 = 131.22
        self.L2 = 63.4
        self.L5 = 75.05
        self.L6 = 45.6
        self.Ld2 = 110.4
        self.Ld3 = 96
        self.PI = math.pi
        HOST = "127.0.0.1"
        PORT = 5658
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def setup(self):

        input("Установите робота в положение начала координат")
        coords = None
        message = ".GetCoords:"
        self.s.sendall(message.encode("utf-8"))
        coords = self.s.recv(1024)
        coords = coords.decode("UTF-8")
        coords = coords.split(":")[1:]
        coords = list(map(lambda x: float(x.replace(",", ".")), coords))
        print(coords)
        self.init_x = coords[0]
        self.init_y = coords[1]
        self.init_z += coords[2]
        self.last_coords =coords
        input(coords)

    def draw_to(self, x, y):
        pass

    def move_to(self, x, y, step=0):
        pass

    def __get_joints_angels(self, x, y, z):
        pass
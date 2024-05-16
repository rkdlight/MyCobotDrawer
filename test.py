import time

import matplotlib.pyplot as plt
from SVGParse.Parse import parse_svg
from MycobotControl import NativeInterface, PolarInterface, XinInterface, KeyboardControl
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
        self.k_array.append(round(step, 2))
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


def rectangle(interface, width, height):
    for i in range(0, int(height / 2), 5):
        interface.draw_to(0, i)

    for i in range(0, width, 5):
        interface.draw_to(i, int(height / 2))

    for i in range(0, height, 5):
        interface.draw_to(width, int(height / 2) - i)

    for i in range(0, width, 5):
        interface.draw_to(width - i, -int(height / 2))
    for i in range(0, int(height / 2), 5):
        interface.draw_to(0, -int(height / 2) + i)


def rectangle_points(interface, width, height):
    interface.draw_to(0, height / 2)
    time.sleep(1)
    interface.draw_to(width, height / 2)
    time.sleep(1)
    interface.draw_to(width, -height / 2)
    time.sleep(1)
    interface.draw_to(0, -height / 2)
    time.sleep(1)
    interface.draw_to(0, 0)
    time.sleep(1)


# (14.124130975316334, -79.62337168872105, -33.59389855542819, 23.21727024414925, 0, 14.124130975316334)

class Testing:

    def __init__(self, **kwargs):
        self.args = kwargs
        # self.native = NativeInterface(**self.args)
        # self.polar = PolarInterface(**self.args)
        # self.xin = XinInterface(**self.args)
        # self.native.setup()
        #
        # self.polar.init_x, self.polar.init_y, self.polar.init_z = self.native.init_x, self.native.init_y, self.native.init_z
        # self.xin.init_x, self.xin.init_y, self.xin.init_z = self.native.init_x, self.native.init_y, self.native.init_z

        self.interface = None
        self.method = None
    def start(self):
        if self.interface == None:
            interface_num = input("Начнем тестирование! Выберите какой интерефейс будет использоваться?\
            \n 1 - NativeInterface\n 2 - PolarInterface\n 3 - XinInterface\n")
            if interface_num == "1":
                self.interface = NativeInterface(**self.args)
            elif interface_num == "2":
                self.interface = PolarInterface(**self.args)
            elif interface_num == "3":
                self.interface = XinInterface(**self.args)
            else:
                self.start()
                return

            self.interface.setup()
        def svg_draw():
            objects = parse_svg("square_test.svg")
            for obj in objects:
                for element in obj:
                    pprint(element)
                    element.render(self.interface, 50)
        def rectangles():
            rectangle(self.interface,300,300)

        def rectangles_points():
            rectangle_points(self.interface,300,300)

        method_num = input("Выберите какой метод тестирования будет использоваться?\
                \n 1 - Прямоугольник по координатам углов\n 2 - Прямоугольник по точкам прямых\n 3 - Множество прямоугольников из SVG\n")

        if method_num == "1":
            self.method = rectangles
        elif method_num == "2":
            self.method = rectangles_points
        elif method_num == "3":
            self.method = svg_draw
        else:
            self.start()
            return

        strt = input("Начинаем?\n 1 - да\n 2 - нет\n")
        if strt == "1" or strt == "":
            time.sleep(10)
            self.method()
        else:
            self.start()
            return

        repeat = input("Тестируем еще?\n 1 - да\n 2 - нет\n")
        if repeat == "1" or repeat == "":
            self.start()




if __name__ == '__main__':

    # testing = Testing(port="COM5", scale=[0.2, 0.2], speed=20, plt=None)
    # testing.start()
    k = KeyboardControl(port="COM5", speed=20)
    k.start()
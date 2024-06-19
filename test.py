import time

import matplotlib.pyplot as plt
from SVGParse.Parse import parse_svg
from MycobotControl import NativeInterface, PolarInterface, XinInterface, KeyboardControl, XinInterfaceUnity, PolarInterfaceUnity
from pprint import pprint


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


if __name__ == '__main__':

    interface = XinInterface(scale=[0.08, 0.08])
    interface.setup()
    # interface.init_z -= 79
    time.sleep(10)
    objects = parse_svg("picture-svgrepo-com.svg")
    for obj in objects:
        for element in obj:
            pprint(element)
            element.render(interface, 20)
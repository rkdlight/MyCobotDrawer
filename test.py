import time

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

    ### Для того чтобы узнать какой порт использовать
    # import serial.tools.list_ports
    #
    # ports = serial.tools.list_ports.comports()
    #
    # for port in ports:
    #     print(port.device)

    interface = XinInterface(port="COM5", scale=[0.08, 0.08], speed=90)
    interface.setup()
    # interface.init_z -= 79
    # time.sleep(10)
    objects = parse_svg("svg_images/picture-svgrepo-com.svg")
    for obj in objects:
        for element in obj:
            pprint(element)
            element.render(interface, 20)
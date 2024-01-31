import matplotlib.pyplot as plt
from SVGParse.Parse import parse_svg
from MycobotControl import MyCobotInterface
from pprint import pprint


class TestInterface:

    def __init__(self, port='COM5', scale=None):
        if scale is None:
            self.scale = [1, 1]
        else:
            self.scale = scale

        self.init_z = 0
        self.last_coords = []
        self.x_array = []
        self.y_array = []

    def start(self, init_x=100, init_y=0, init_z=100):
        self.init_z = init_z
        self.x_array.append(init_x)
        self.y_array.append(init_y)
        self.last_coords = [init_x, init_y, init_z, -180, 0, 0]

    def draw_to(self, x, y):
        x = self.scale[0] * x
        y = self.scale[1] * y
        self.x_array.append(x)
        self.y_array.append(y)
        self.last_coords = [x, y, self.init_z, -180, 0, 0]


    def move_to(self, x, y):
        x = self.scale[0] * x
        y = self.scale[1] * y
        coords = self.last_coords
        coords[0] = x
        coords[1] = y
        self.x_array.append(x)
        self.y_array.append(y)
        self.last_coords = coords

    @property
    def current_coords(self):
        return self.last_coords[0]/self.scale[0], self.last_coords[1]/self.scale[1]




if __name__ == '__main__':
    objects = parse_svg("C:/Users/konop/Downloads/genetic-data-svgrepo-com.svg")
    interface = MyCobotInterface(port="COM5", scale=[0.10, 0.10])
    interface.start(150, 0, 47)

    for obj in objects:
        for element in obj:
            pprint(element)
            element.render(interface)
    #
    # # plot
    # fig, ax = plt.subplots()
    #
    # ax.scatter(interface.x_array, interface.y_array, s=1)
    #
    # plt.show()
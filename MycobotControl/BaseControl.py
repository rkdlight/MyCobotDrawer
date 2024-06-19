from pymycobot.mycobot import MyCobot
import time
import keyboard




class BaseInterface:
    def __init__(self, port='COM5', scale=None, speed=50, plt=None, up_moving=50):
        self.speed = speed
        if scale is None:
            self.scale = [1, 1]
        else:
            self.scale = scale
        self.init_z = 0
        self.mc = MyCobot(port, 115200)
        time.sleep(0.5)
        self.mc.set_fresh_mode(0) # Execute instructions sequentially in the form of a queue.
        time.sleep(0.5)
        self.last_coords = []
        self.plt = plt
        self.up_moving = up_moving

    def setup(self):
        self.mc.release_all_servos(0)

        input("Установите робота в положение начала координат")
        coords = None

        while coords is None:
            coords = self.mc.get_coords()
            time.sleep(0.2)
        self.init_x = coords[0]
        self.init_y = coords[1]
        self.init_z = coords[2]
        self.last_coords =coords
        input(coords)


    def draw_to(self, x, y):
        x = self.scale[0]*x+self.init_x
        y = self.scale[1]*y+self.init_y

        self.last_coords = [x, y, self.init_z, -180, 0, 0]

        if self.plt is not None:
            self.plt.scatter(x, y)
            self.plt.pause(0.05)
    def move_to(self, x, y, step=0):
        x = self.scale[0] * x+self.init_x
        y = self.scale[1] * y+self.init_y
        coords = self.last_coords
        coords[2] += 30

        coords[0] = x
        coords[1] = y

        coords[2] -= 30

        self.last_coords = coords

        if self.plt is not None:
            self.plt.scatter(x, y)
            self.plt.pause(0.05)

    @property
    def current_coords(self):
        return self.last_coords[0], self.last_coords[1]


class KeyboardControl(BaseInterface):
    def __init__(self, port='COM5', speed=50):
        super().__init__(port=port, speed=speed)
        coords = None

        while coords is None:
            coords = self.mc.get_coords()
            time.sleep(0.2)
        self.last_coords = [coords[0], coords[1], coords[2], -180, 0, 0]
    def start(self):
        while True:
            # Wait for the next event.
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN and event.name == 'up':
                self.last_coords[1] +=2
                self.mc.send_coords(self.last_coords, self.speed)
            elif event.event_type == keyboard.KEY_DOWN and event.name == 'down':
                self.last_coords[1] -= 2
                self.mc.send_coords(self.last_coords, self.speed)
            elif event.event_type == keyboard.KEY_DOWN and event.name == 'left':
                self.last_coords[0] -= 2
                self.mc.send_coords(self.last_coords, self.speed)
            elif event.event_type == keyboard.KEY_DOWN and event.name == 'right':
                self.last_coords[0] += 2
                self.mc.send_coords(self.last_coords, self.speed)
            elif event.event_type == keyboard.KEY_DOWN and event.name == '+':
                self.last_coords[2] += 2
                self.mc.send_coords(self.last_coords, self.speed)
            elif event.event_type == keyboard.KEY_DOWN and event.name == '-':
                self.last_coords[2] -= 2
                self.mc.send_coords(self.last_coords, self.speed)
            elif event.event_type == keyboard.KEY_DOWN and event.name == 'esc':
                break
            # time.sleep(0.5)
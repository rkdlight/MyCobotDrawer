from MycobotControl import MyCobotInterface
from math import cos, sin, radians, sqrt, degrees, acos


class Move:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def render(self, mc_interface: MyCobotInterface):
        mc_interface.move_to(round(self.x), round(self.y))


class Line:
    def __init__(self, sp_x, sp_y, ep_x, ep_y):
        self.sp_x = sp_x
        self.sp_y = sp_y
        self.ep_x = ep_x
        self.ep_y = ep_y

    def render(self, mc_interface: MyCobotInterface):

        mc_interface.draw_to(round(self.ep_x), round(self.ep_y))


class CubicCurve:
    def __init__(self, sp_x, sp_y, ep_x1, ep_y1, sp_x2, sp_y2, ep_x, ep_y):
        '''
        Cubic Curve defined by two lines ({sp_x;sp_y};{ep_x1;ep_y1}) and
        ({sp_x2;sp_y2};{ep_x;ep_y})
        :param sp_x: X coord of start point
        :param sp_y: Y coord of start point
        :param ep_x1: X coord of end of first line
        :param ep_y1: Y coord of end of first line
        :param sp_x2: X coord of start of second line
        :param sp_y2: Y coord of start of second line
        :param ep_x: X coord of end of whole curve
        :param ep_y: Y coord of end of whole curve
        '''
        self.sp_x = sp_x
        self.sp_y = sp_y
        self.ep_x1 = ep_x1
        self.ep_y1 = ep_y1
        self.sp_x2 = sp_x2
        self.sp_y2 = sp_y2
        self.ep_x = ep_x
        self.ep_y = ep_y

    def render(self, mc_interface: MyCobotInterface):

        for i in range(0, 21):
            i = i / 20
            x = (((1 - i) ** 3) * self.sp_x + 3 * ((1 - i) ** 2) * i * self.ep_x1 +
                 + 3 * (1 - i) * (i ** 2) * self.sp_x2 + i ** 3 * self.ep_x)
            y = (((1 - i) ** 3) * self.sp_y + 3 * ((1 - i) ** 2) * i * self.ep_y1 +
                 + 3 * (1 - i) * (i ** 2) * self.sp_y2 + i ** 3 * self.ep_y)

            mc_interface.draw_to(round(x), round(y))


class QuadraticCurve:
    def __init__(self, sp_x, sp_y, mp_x, mp_y, ep_x, ep_y):
        '''
        Quadratic Curve defined by two line ({sp_x;sp_y};{mp_x;mp_y}) and
        ({mp_x;mp_y};{ep_x;ep_y})
        :param sp_x: X coord of start point
        :param sp_y: Y coord of start point
        :param mp_x: X coord of middle point
        :param mp_y: Y coord of middle point
        :param ep_x: X coord of end of whole curve
        :param ep_y: Y coord of end of whole curve
        '''
        self.sp_x = sp_x
        self.sp_y = sp_y
        self.mp_x = mp_x
        self.mp_y = mp_y
        self.ep_x = ep_x
        self.ep_y = ep_y

    def render(self, mc_interface: MyCobotInterface):

        for i in range(0, 21):
            i = i / 20
            x = ((1 - i) ** 2) * self.sp_x + 2 * (1 - i) * i * self.mp_x + (i ** 2) * self.ep_x
            y = ((1 - i) ** 2) * self.sp_y + 2 * (1 - i) * i * self.mp_y + (i ** 2) * self.ep_y

            mc_interface.draw_to(round(x), round(y))


class ArcCurve:
    def __init__(self, sp_x, sp_y, x_r, y_r, rotation, arc, sweep, ep_x, ep_y):
        '''

        :param sp_x: X coord of start point
        :param sp_y: Y coord of start point
        :param x_r: radius of ellipse for X axis
        :param y_r: radius of ellipse for Y axis
        :param rotation: rotation by X axis
        :param arc:
        :param sweep:
        :param ep_x: X coord of end point
        :param ep_y: Y coord of end point
        '''
        self.sp_x = sp_x
        self.sp_y = sp_y
        self.x_r = x_r
        self.y_r = y_r
        self.rotation = rotation
        self.arc = arc
        self.sweep = sweep
        self.ep_x = ep_x
        self.ep_y = ep_y

        self._parameterize()

    def _parameterize(self):
        # Conversion from endpoint to center parameterization
        # http://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes
        if self.sp_x == self.ep_x and self.sp_y == self.ep_y:
            # This is equivalent of omitting the segment, so do nothing
            return

        if self.x_r == 0 or self.y_r == 0:
            # This should be treated as a straight line
            return

        cosr = cos(radians(self.rotation))
        sinr = sin(radians(self.rotation))
        dx = (self.sp_x - self.ep_x) / 2
        dy = (self.sp_y - self.ep_y) / 2
        x1prim = cosr * dx + sinr * dy
        x1prim_sq = x1prim * x1prim
        y1prim = -sinr * dx + cosr * dy
        y1prim_sq = y1prim * y1prim

        rx = self.x_r
        rx_sq = rx * rx
        ry = self.y_r
        ry_sq = ry * ry

        # Correct out of range radii
        radius_scale = (x1prim_sq / rx_sq) + (y1prim_sq / ry_sq)
        if radius_scale > 1:
            radius_scale = sqrt(radius_scale)
            rx *= radius_scale
            ry *= radius_scale
            rx_sq = rx * rx
            ry_sq = ry * ry
            self.radius_scale = radius_scale
        else:
            # SVG spec only scales UP
            self.radius_scale = 1

        t1 = rx_sq * y1prim_sq
        t2 = ry_sq * x1prim_sq
        c = sqrt(abs((rx_sq * ry_sq - t1 - t2) / (t1 + t2)))

        if self.arc == self.sweep:
            c = -c
        cxprim = c * rx * y1prim / ry
        cyprim = -c * ry * x1prim / rx

        self.center = complex(
            (cosr * cxprim - sinr * cyprim) + ((self.sp_x + self.ep_x) / 2),
            (sinr * cxprim + cosr * cyprim) + ((self.sp_y + self.ep_y) / 2),
        )
        self.center_x = self.center.real
        self.center_y = self.center.imag

        ux = (x1prim - cxprim) / rx
        uy = (y1prim - cyprim) / ry
        vx = (-x1prim - cxprim) / rx
        vy = (-y1prim - cyprim) / ry
        n = sqrt(ux * ux + uy * uy)
        p = ux
        theta = degrees(acos(p / n))
        if uy < 0:
            theta = -theta
        self.theta = theta % 360

        n = sqrt((ux * ux + uy * uy) * (vx * vx + vy * vy))
        p = ux * vx + uy * vy
        d = p / n
        # In certain cases the above calculation can through inaccuracies
        # become just slightly out of range, f ex -1.0000000000000002.
        if d > 1.0:
            d = 1.0
        elif d < -1.0:
            d = -1.0
        delta = degrees(acos(d))
        if (ux * vy - uy * vx) < 0:
            delta = -delta
        self.delta = delta % 360
        if not self.sweep:
            self.delta -= 360

    def point(self, pos):
        if self.sp_x == self.ep_x and self.sp_y == self.ep_y:
            # This is equivalent of omitting the segment
            return self.sp_x, self.sp_y

        if self.x_r == 0 or self.y_r == 0:
            # This should be treated as a straight line
            distance = complex(self.ep_x, self.ep_y) - complex(self.sp_x, self.sp_y)
            c_point = complex(self.sp_x, self.sp_y) + distance * pos
            return c_point.real, c_point.imag

        angle = radians(self.theta + (self.delta * pos))
        cosr = cos(radians(self.rotation))
        sinr = sin(radians(self.rotation))
        radius = complex(self.x_r, self.y_r) * self.radius_scale

        x = (
                cosr * cos(angle) * radius.real
                - sinr * sin(angle) * radius.imag
                + self.center.real
        )
        y = (
                sinr * cos(angle) * radius.real
                + cosr * sin(angle) * radius.imag
                + self.center.imag
        )
        return x, y

    def render(self, mc_interface: MyCobotInterface):

        for i in range(21):
            i = i / 20
            x, y = self.point(i)
            mc_interface.draw_to(round(x), round(y))


class Rectangle:
    def __init__(self, sp_x, sp_y, width, height, rx=None, ry=None):
        '''

        :param sp_x: X coord of start point
        :param sp_y: Y coord of start point
        :param width: Width of rectangle
        :param height: Height of rectangle
        '''
        self.sp_x = sp_x
        self.sp_y = sp_y
        self.width = width
        self.height = height
        self.rx = rx
        self.ry = ry
        if self.rx is not None and self.ry is not None:
            self.width = self.width - 2 * self.rx
            self.height = self.height - 2 * self.ry
            self.sp_x = self.sp_x + self.rx
            self.lines = [
                Line(self.sp_x, self.sp_y, self.sp_x + self.width, self.sp_y),
                ArcCurve(self.sp_x + self.width, self.sp_y, self.rx, self.ry, 0, 0, 1,
                         self.sp_x + self.width + self.rx, self.sp_y + self.ry),
                Line(self.sp_x + self.width + self.rx, self.sp_y + self.ry, self.sp_x + self.width + self.rx,
                     self.sp_y + self.ry + self.height),
                ArcCurve(self.sp_x + self.width + self.rx, self.sp_y + self.ry + self.height, self.rx, self.ry, 0,
                         1, 1, self.sp_x + self.width, self.sp_y + self.height + 2 * self.ry),
                Line(self.sp_x + self.width, self.sp_y + self.height + 2 * self.ry, self.sp_x,
                     self.sp_y + self.height + 2 * self.ry),
                ArcCurve(self.sp_x, self.sp_y + self.height + 2 * self.ry, self.rx, self.ry, 0,
                         1, 0, self.sp_x - self.rx, self.sp_y + self.height + self.ry),
                Line(self.sp_x - self.rx, self.sp_y + self.height + self.ry, self.sp_x - self.rx,
                     self.sp_y + self.ry),
                ArcCurve(self.sp_x - self.rx, self.sp_y + self.ry, self.rx, self.ry, 0,
                         0, 0, self.sp_x, self.sp_y),
            ]
        else:
            self.lines = [Line(self.sp_x, self.sp_y, self.sp_x + self.width, self.sp_y),
                          Line(self.sp_x + self.width, self.sp_y, self.sp_x + self.width, self.sp_y + height),
                          Line(self.sp_x + self.width, self.sp_y + height, self.sp_x, self.sp_y + height),
                          Line(self.sp_x, self.sp_y + height, self.sp_x, self.sp_y)]

    def render(self):
        pass


class Circle:
    def __init__(self, c_x, c_y, r):
        self.sp_x = c_x - r
        self.sp_y = c_y
        self.lines = [
            ArcCurve(self.sp_x, self.sp_y, r, r, 0, 0, 0, c_x, c_y - r),
            ArcCurve(c_x, c_y - r, r, r, 0, 0, 1, c_x + r, c_y),
            ArcCurve(c_x + r, c_y, r, r, 0, 1, 1, c_x, c_y + r),
            ArcCurve(c_x, c_y + r, r, r, 0, 1, 0, self.sp_x, self.sp_y)
        ]

    def render(self):
        pass

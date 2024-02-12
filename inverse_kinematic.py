from math import sqrt, sin, cos, acos, asin, pi, degrees

a1 = 131.56
a2 = 110.4
a3 = 96
a4 = 73.18
a5 = 105


def get_joints_angels(r, z=0):
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


if __name__ == '__main__':
    from pymycobot.mycobot import MyCobot
    import time
    mc = MyCobot('COM5', 115200)
    time.sleep(0.5)
    mc.set_fresh_mode(0)
    time.sleep(0.5)
    J2, J3, J4 = get_joints_angels(130)
    print(J2, J3, J4)

    #

    mc.sync_send_angles([0, J2, J3, J4, 0, 0], 100)
    # J2, J3, J4 = get_joints_angels(250)
    mc.sync_send_angles([0,0, 0, 0, 0, 0], 100)
    time.sleep(2)

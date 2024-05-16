from math import sqrt, sin, cos, acos, asin, pi, degrees
import numpy as np
from pprint import pprint
import socket

a1 = 131.56
a2 = 110.4
a3 = 96
a4 = 73.18
a5 = 105

DH = [
    [0, 131.22, 0, pi / 2],
    [-pi / 2, 0, -100.4, 0],
    [0, 0, 96, 0],
    [-pi / 2, 63.4, 0, pi / 2],
    [pi / 2, 75.05, 0, -pi / 2],
    [0, 45.6, 0, 0]
]


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


def dh_matrix(thetha, d, a, alpha):
    """
    Создает матрицу преобразования для пары Денавита-Хартенберга.

    :param alpha: угол поворота вокруг z-оси предыдущего звена
    :param a: перемещение вдоль z-оси предыдущего звена
    :param d: перемещение вдоль z-оси текущего звена
    :param theta: угол поворота вокруг z-оси текущего звена
    :return: матрица преобразования 4x4
    """
    cq = cos(thetha)
    sq = sin(thetha)
    ca = cos(alpha)
    sa = sin(alpha)
    A = [
        [cq, -ca * sq, sa * sq, a * cq],
        [sq, ca * cq, -sa * cq, a * sq],
        [0, sa, ca, d],
        [0, 0, 0, 1]
    ]
    return A


def forward_kinematic(Joints):
    T = []
    DH_now = DH
    for i, j in enumerate(Joints):
        DH_now[i][0] += j
    for i, dh in enumerate(DH_now):
        A = dh_matrix(*dh)
        if i == 0:
            T = A
            continue
        T = np.matmul(T, A)



    return T[0][3], T[1][3], T[2][3], T[:3, :3]


# J = [pi, pi / 2, -pi / 2, pi / 2, 0, 0]
J_start = [-pi/2, -pi/2, 0, pi/2, 0, 0]

J = [0, 0, 0, 0, 0, 0]
if __name__ == '__main__':

    j_degrees = list(map(str, map(degrees, J)))

    x, y, z, R = forward_kinematic(J)

    print(x, y, z, R)

    HOST = "127.0.0.1"
    PORT = 5658

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        message = ".ModRobot:" + ",".join(j_degrees)+",0"
        s.sendall(message.encode("utf-8"))

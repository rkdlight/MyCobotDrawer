import math

class IK:
    def __init__(self):
        # Public variables to store joint angles



        # Chain rod lengths


    def calculate_inverse_kinematics(self, ox, oy, oz):
        """
        Calculates inverse kinematics for a 6-DOF robotic arm.

        Args:
            ox (float): X-coordinate of the target point.
            oy (float): Y-coordinate of the target point.
            oz (float): Z-coordinate of the target point.

        Returns:
            list: A list containing the calculated joint angles (q1, q2, q3, q4, q5, q6) in degrees.
        """

        # Define rotation matrix R (assuming no rotation needed in this example)
        R = [[0, 1, 0, 0],
             [1, 0, 0, 0],
             [0, 0, -1, 0],
             [0, 0, 0, 1]]

        # Calculate xc, yc, and r
        xc = ox - (self.L6 * R[0][2])
        yc = oy - (self.L6 * R[1][2])
        zc = oz - self.L6 * R[2][2]
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
        if oy >= yc:
            theta5 = math.degrees(math.atan2(oz - zc, yc - oy))
        elif oy < yc and oz <= zc:
            theta5 = -math.degrees(math.atan2(oy - yc, zc - oz)) - 90
        else:
            theta5 = math.degrees(math.atan2(oy - yc, oz - zc)) + 90

        # Calculate theta6 (assuming same rotation as theta1)
        theta6 = theta1

        # Calculate q11, L11, L12, z2
        q11 = math.acos(self.L2 / r)
        L11 = r * math.sin(q11)
        L12 = L11 - self.L5
        z2 = zc - self.L6

        can1 = (L12 ** 2 + z2 ** 2 + self.Ld2 ** 2 - self.Ld3 ** 2) / (2 * self.Ld2 * math.sqrt(L12 ** 2 + z2 ** 2))
        theta2 = 180 - math.degrees(math.atan2(z2, L12)) - math.degrees(math.acos(can1))

        # Calculate can2 and theta3
        can2 = (self.Ld2 ** 2 + self.Ld3 ** 2 - L12 ** 2 - z2 ** 2) / (2 * self.Ld2 * self.Ld3)
        theta3 = 180 - math.degrees(math.acos(can2))

        # Calculate theta4
        theta4 = 180 - theta2 - theta3 + 90

        # Store joint angles
        q1 = 180-theta1
        if q1 > 180:
            q1 = q1-360
        elif q1 < -180:
            q1 = 360+q1
        q2 = 90 - theta2
        q3 = -theta3
        q4 = 90 - theta4
        # q5 = theta5+90
        q5 = 0
        q6 = q1

        # Print results (optional)
        # print("Optimal joint angles:")
        # print("q1:", q1)
        # print("q2:", q2)
        # print("q3:", q3)
        # print("q4:", q4)
        # print("q5:", q5)
        # print("q6:", q6)

        # Calculate joint velocities (assuming Tm is movement time)

        return q1, q2, q3, q4, q5, q6  # Return all calculated values
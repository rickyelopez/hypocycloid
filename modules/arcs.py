""" Finding information about arc from 3 points
    code is from: 
    https://stackoverflow.com/questions/52990094/calculate-circle-given-3-points-code-explanation
"""

from math import sqrt, acos, pi


def arc_3_point(p_1, p_2, p_3):
    """Find into about an arc from 3 points"""
    temp = p_2[0] ** 2 + p_2[1] ** 2
    b_c = (p_1[0] ** 2 + p_1[1] ** 2 - temp) / 2
    c_d = (temp - p_3[0] ** 2 - p_3[1] ** 2) / 2
    det = (p_1[0] - p_2[0]) * (p_2[1] - p_3[1]) - (p_2[0] - p_3[0]) * (p_1[1] - p_2[1])

    if abs(det) < 1.0e-10:
        return None

    # Center of circle
    c_x = (b_c * (p_2[1] - p_3[1]) - c_d * (p_1[1] - p_2[1])) / det
    c_y = ((p_1[0] - p_2[0]) * c_d - (p_2[0] - p_3[0]) * b_c) / det
    center = (c_x, c_y)
    radius = sqrt((c_x - p_1[0]) ** 2 + (c_y - p_1[1]) ** 2)

    def angles(p_1, p_2):
        sign = -1 if p_1[1] < p_2[1] else 1
        p_1[0] = p_1[0] - p_2[0]
        p_1[1] = p_1[1] - p_2[1]
        dot = p_1[0] * 1
        mag = sqrt(p_1[0]**2 + p_1[1]**2)
        return sign * acos(dot/mag) * 180 / pi

    angs = [angles(p_1, center), angles(p_3, center)]
    return (c_x, c_y), radius, angs

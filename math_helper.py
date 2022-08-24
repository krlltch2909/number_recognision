from math import sqrt


def pythagorean_theorem(dot1: list, dot2: list):
    """
    :param dot1: list with coordinates point one
    :param dot2: list with coordinates point two
    :return: distant between two points
    """
    x = dot2[0] - dot1[0]
    y = dot2[1] - dot1[1]

    rez = sqrt(x*x + y*y)
    # print(rez)
    return rez

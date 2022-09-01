import os

import cv2

from math_helper import pythagorean_theorem


class Car_Adapter:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Car_Adapter, cls).__new__(cls)
        return cls.__instance


    def find_plate(self):


# car = Car_Adapter()
# car2 = Car_Adapter()
#
# print(car, car2, car is car2)
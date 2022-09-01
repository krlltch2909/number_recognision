import os
from datetime import datetime

import cv2

from math_helper import pythagorean_theorem


class Car_Adapter:
    __instance = None

    directory_car_number = 0  # номер для папки с номерами машин
    len_of_last_frame_obgects_detected: list = []
    last_frame_numbers: list = []  # list[list[list[x, y], № folder], list[list[x, y], № folder]]

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Car_Adapter, cls).__new__(cls)
        return cls.__instance

    def find_plate(self, rez, roi_color):
        for (x, y, w, h) in rez:

            center_of_current_number = [x + w // 2, y + h // 2]

            return_rez = []

            was_written: bool = False  # переменная обозначающая была ли записанна фотография
            for i in self.last_frame_numbers:
                # cv2.line(frame, (x+w//2, y+h//2), i[0], (0, 0, 255), 5)
                if pythagorean_theorem(i[0], center_of_current_number) < 200:
                    cv2.imwrite(f'cars/detected_numbers/{i[1]}_car/{datetime.today()}.jpeg', roi_color)
                    return_rez = [center_of_current_number, i[1]]
                    was_written = True
                    break

            if was_written is False:
                os.mkdir('cars/detected_numbers/{}_car'.format(self.directory_car_number))
                cv2.imwrite(f'cars/detected_numbers/{self.directory_car_number}_car/{datetime.today()}.jpeg', roi_color)

                return_rez = [center_of_current_number, self.directory_car_number]
                self.directory_car_number += 1
            self.last_frame_numbers.append(return_rez)
            # cv2.circle(frame, (x + w // 2, y + h // 2), 5, (0, 0, 255), thickness=-1)

        while len(self.len_of_last_frame_obgects_detected) > 3:
            for i in range(self.len_of_last_frame_obgects_detected[0]):
                self.last_frame_numbers.pop(0)
            self.len_of_last_frame_obgects_detected.pop(0)

        self.len_of_last_frame_obgects_detected.append(len(rez))

 
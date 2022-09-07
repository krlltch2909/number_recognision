import os
from datetime import datetime

import cv2

from math_helper import pythagorean_theorem


class Car_Adapter:
    __instance = None

    directory_car_number = 0  # номер для папки с номерами машин
    len_of_last_frame_obgects_detected: list = []
    last_frame_numbers: list = []  # list[list[list[x, y], № folder, list[buffer]], list[list[x, y], № folder,
                                                                                             # list[buffer]]]

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Car_Adapter, cls).__new__(cls)
        return cls.__instance

    def find_plate(self, roi_color, center_of_current_number)->None:
        """
        :param roi_color: image of current car plate withdrawn from frame
        :param center_of_current_number: center of current car plate withdrawn from frame
        :return: None
        """

        return_rez = []
        was_written: bool = False  # переменная обозначающая была ли записанна фотография

        for i in self.last_frame_numbers:
            if pythagorean_theorem(i[0], center_of_current_number) < 200:
                # cv2.imwrite(f'cars/detected_numbers/{i[1]}_car/{datetime.today()}.jpeg', roi_color)
                list_of_find_numbers: list = i[2]
                list_of_find_numbers.append(roi_color)
                return_rez = [center_of_current_number, i[1], list_of_find_numbers]

                was_written = True

                if len(return_rez[2]) >= 5:
                    try:
                        os.mkdir('cars/detected_numbers/{}_car'.format(return_rez[1]))
                    except:
                        pass
                    for image_to_wright in return_rez[2]:
                        cv2.imwrite(f'cars/detected_numbers/{return_rez[1]}_car/{datetime.today()}.jpeg',
                                    image_to_wright)
                    return_rez[2].clear()
                break

        if was_written is False:
            # os.mkdir('cars/detected_numbers/{}_car'.format(self.directory_car_number))
            # cv2.imwrite(f'cars/detected_numbers/{self.directory_car_number}_car/{datetime.today()}.jpeg', roi_color)

            return_rez = [center_of_current_number, self.directory_car_number, [roi_color]]
            self.directory_car_number += 1
        self.last_frame_numbers.append(return_rez)

    def clean_metod(self, rez:list)-> None:
        """
        :param rez: list with all found images on the frame
        :return: None
        """
        while len(self.len_of_last_frame_obgects_detected) > 3:

            for i in range(self.len_of_last_frame_obgects_detected[0]):
                self.last_frame_numbers.pop(0)
            self.len_of_last_frame_obgects_detected.pop(0)

        self.len_of_last_frame_obgects_detected.append(len(rez))

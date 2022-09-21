import multiprocessing

from copy import deepcopy

import cv2

from math_helper import pythagorean_theorem


class Car_Adapter:
    __instance = None

    queue = None
    lock = multiprocessing.RLock()

    all_number = 0

    directory_car_number = 0  # номер для папки с номерами машин
    len_of_last_frame_obgects_detected: list = []
    last_frame_numbers: list = []  # list[list[list[x, y], № folder, list[buffer]], list[list[x, y], № folder,

    # list[buffer]]]

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Car_Adapter, cls).__new__(cls)
            cls.__instance.queue = kwargs['queue']
        return cls.__instance

    def get_queue(self, queue):
        self.queue = queue

    def find_plate(self, roi_color, center_of_current_number) -> None:
        """
        :param roi_color: image of current car plate withdrawn from frame
        :param center_of_current_number: center of current car plate withdrawn from frame
        :return: None
        """

        # img = cv2.resize(roi_color, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)
        # size = img.shape
        #
        # # print(size)
        # roi_color = img[40:size[0] - 25, 15:size[1] - 40]
        return_rez = []
        was_written: bool = False  # переменная обозначающая была ли записанна фотография

        for i in self.last_frame_numbers:
            if pythagorean_theorem(i[0], center_of_current_number) < 200:
                list_of_find_numbers: list = i[2]
                list_of_find_numbers.append(roi_color)
                return_rez = [center_of_current_number, i[1], list_of_find_numbers, ]

                was_written = True

                if len(return_rez[2]) >= 5:
                    self.all_number += len(return_rez[2])
                    tasks_for_work = deepcopy(return_rez)
                    return_rez[2].clear()

                    self.queue.put(tasks_for_work)

                    print(self.all_number)
                break

        if was_written is False:
            return_rez = [center_of_current_number, self.directory_car_number, [roi_color]]
            self.directory_car_number += 1

        self.last_frame_numbers.append(return_rez)

    def clean_metod(self, rez: list) -> None:
        """
        :param rez: list with all found images on the frame
        :return: None
        """
        while len(self.len_of_last_frame_obgects_detected) > 3:

            for i in range(self.len_of_last_frame_obgects_detected[0]):
                self.last_frame_numbers.pop(0)
            self.len_of_last_frame_obgects_detected.pop(0)

        self.len_of_last_frame_obgects_detected.append(len(rez))

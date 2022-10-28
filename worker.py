import os
import sqlite3
import re

import cv2

from text_reader import run_tesseract, easy_osr_reader
from text_update import compare_number

def image_processing(queue, locker) -> None:
    """
    :param queue: queue with images for recognition with tecceract
    :param locker: blocker for processes
    :return: None
    """
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    while True:
        return_rez = queue.get()

        if return_rez is not None:
            selector = str(return_rez[1]) + "_car"
            if os.path.exists(f'cars/detected_numbers/{return_rez[1]}_car') is False:
                os.mkdir(f'cars/detected_numbers/{return_rez[1]}_car')

            recognized_text = []
            for image_to_wright in return_rez[2]:
                # text = easy_osr_reader(image_to_wright)
                text = run_tesseract(image_to_wright).strip()

                text.strip()
                text = text.upper()
                text = re.sub(r"[-_/|;:,.'+ {}=]", '', text)

                number_and_image = [text, image_to_wright]
                recognized_text.append(number_and_image)

            locker.acquire()
            cursor.execute(f"SELECT MAX(image) FROM cars WHERE car_id='{selector}'")
            number = cursor.fetchone()[0]
            if number is None or number == '':
                number = 0
            else:
                number += 1

            for number_and_image in recognized_text:
                if len(number_and_image[0]) != 0 and text != 'tesseract error':
                    cv2.imwrite(f'cars/detected_numbers/{return_rez[1]}_car/{number}.jpeg',
                                number_and_image[1])
                    is_correct = compare_number(text=number_and_image[0])
                    need_add_check = False

                    if len(number_and_image[0]) > 8:
                        need_add_check = True

                    cursor.execute("INSERT INTO cars VALUES (?, ?, ?, ?, ?)",
                                   (str(return_rez[1]) + "_car", number, number_and_image[0], is_correct, need_add_check))
                    db.commit()
                    number += 1
            locker.release()

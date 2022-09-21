import os
import sqlite3
import cv2

from text_reader import run_tesseract


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
                text = run_tesseract(image_to_wright).strip()
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
                cv2.imwrite(f'cars/detected_numbers/{return_rez[1]}_car/{number}.jpeg',
                            number_and_image[1])

                # if number_and_image[0] != '' and number_and_image[0] != 'tesseract error':
                cursor.execute("INSERT INTO cars VALUES (?, ?, ?)",
                               (str(return_rez[1]) + "_car", number, number_and_image[0],))
                db.commit()
                number += 1
            locker.release()

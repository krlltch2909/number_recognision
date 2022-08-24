from datetime import datetime

import cv2
import os
from text_reader import run_tesseract, easy_osr_reader
from math_helper import pythagorean_theorem

video = cv2.VideoCapture('videos/video.mp4')
car_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
list_of_car_numbers = []


def video_reader():
    directory_car_number = 0  # номер для папки с номерами машин

    len_of_last_frame_obgects_detected: int = 0
    last_frame_numbers: list = []   # list[list[list[x, y], № folder], list[list[x, y], № folder]]

    while True:
        _, frame = video.read()

        cv2.rectangle(frame, (0, 720), (270, 600), (255, 0, 0), thickness=-1)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        rez = car_cascade.detectMultiScale(gray, scaleFactor=1.4,
                                           minSize=(20, 20),
                                           maxSize=(120, 50),
                                           minNeighbors=2,
                                           flags=cv2.CASCADE_SCALE_IMAGE)
        if len(rez) > 0:
            for (x, y, w, h) in rez:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi_color = frame[y:y + h, x:x + w]

                center_of_current_number = [x + w // 2, y + h // 2]

                return_rez = []

                was_written: bool = False  # была ли записанна фотография
                for i in last_frame_numbers:
                    # cv2.line(frame, (x+w//2, y+h//2), i[0], (0, 0, 255), 5)
                    if pythagorean_theorem(i[0], center_of_current_number) < 200:
                        cv2.imwrite(f'cars/detected_numbers/{i[1]}_car/{datetime.today()}.jpeg', roi_color)
                        return_rez = [center_of_current_number, i[1]]
                        was_written = True
                        continue

                if was_written is False:
                    os.mkdir('cars/detected_numbers/{}_car'.format(directory_car_number))
                    cv2.imwrite(f'cars/detected_numbers/{directory_car_number}_car/{datetime.today()}.jpeg', roi_color)

                    return_rez = [center_of_current_number, directory_car_number]
                    directory_car_number += 1
                last_frame_numbers.append(return_rez)
                # cv2.circle(frame, (x + w // 2, y + h // 2), 5, (0, 0, 255), thickness=-1)

            for i in range(len_of_last_frame_obgects_detected):
                last_frame_numbers.pop(0)

            len_of_last_frame_obgects_detected = len(rez)

        cv2.imshow('video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


def main():
    i = 0
    try:
        os.mkdir('cars/detected_numbers')
    except:
        pass
    video_reader()
    print(len(list_of_car_numbers))
    print("wait ...")
    # for img in list_of_car_numbers:
    #     tessertact_text = run_tesseract(img)
    #     easyosr_text = easy_osr_reader(img)
    #
    #     cv2.imshow('image' + str(i), img)
    #     # print("number = " + str(i) +
    #     #       "\t| tesseract = " + str(tessertact_text) +
    #     #       "\t| easyosr = " + str(easyosr_text)
    #     #       )
    #
    #     with open('find_numbers', "a") as file:
    #         file.write(f"number - {i}\t tesseract - {tessertact_text}\t easyosr - {easyosr_text}\n\n")
    #     i += 1

    print("end of reading text")
    # cv2.waitKey(0)


if __name__ == '__main__':
    main()

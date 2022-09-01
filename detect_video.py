import shutil
from datetime import datetime

import cv2
import os
from text_reader import run_tesseract, easy_osr_reader
from car_adapter import Car_Adapter

video = cv2.VideoCapture('videos/video5.mp4')
car_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
list_of_car_numbers = []


def video_reader():
    car_adapter = Car_Adapter()
    while True:

        _, frame = video.read()

        # cv2.rectangle(frame, (0, 720), (270, 600), (255, 0, 0), thickness=-1)
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
                car_adapter.find_plate(rez=rez, roi_color=roi_color)

        cv2.imshow('video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


def main():
    i = 0

    path_to_folder_with_car_numbers: str = r'cars/detected_numbers'
    if os.path.isdir(path_to_folder_with_car_numbers):
        shutil.rmtree(path_to_folder_with_car_numbers)
    try:
        os.mkdir(path_to_folder_with_car_numbers)
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

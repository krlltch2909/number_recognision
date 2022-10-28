import multiprocessing
import shutil
import threading

import cv2
import os
import sqlite3
import time
import datetime

from worker import image_processing
from caradapter import CarAdapter

video = cv2.VideoCapture('videos/video5.mp4')
car_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
list_of_car_numbers = []


def video_reader():
    detect_num = 0
    car_adapter = CarAdapter()


    start_time = datetime.datetime.now()

    while True:
        if datetime.datetime.now() + datetime.timedelta(seconds=1) >= start_time:
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
                    center_of_current_number = [x + w // 2, y + h // 2]
                    roi_color = frame[y:y + h, x:x + w]
                    car_adapter.find_plate(roi_color=roi_color, center_of_current_number=center_of_current_number, )

            if len(rez) > 0:
                for (x, y, w, h) in rez:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            detect_num += len(rez)
            car_adapter.clean_metod(rez=rez)
            cv2.imshow('video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("all number was detected - "+str(detect_num))
                break
            start_time = datetime.datetime.now()
    video.release()
    cv2.destroyAllWindows()


def main():
    queue = multiprocessing.Queue()
    locker = multiprocessing.Lock()

    CarAdapter(queue=queue)
    path_to_folder_with_car_numbers: str = r'cars/detected_numbers'
    if os.path.isdir(path_to_folder_with_car_numbers):
        shutil.rmtree(path_to_folder_with_car_numbers)

    try:
        os.mkdir(path_to_folder_with_car_numbers)
    except:
        pass

    processes = []
    for i in range(3):
        pr = multiprocessing.Process(target=image_processing, args=(queue, locker,), daemon=True)
        pr.start()
        processes.append(pr)
    video_reader()

    print("wait ...")

    while queue.empty() is False:
        time.sleep(1)

    print("sleep for 15 seconds")
    time.sleep(9)

    # for i in processes:
    #     i.terminate()

    print("end of reading text")


if __name__ == '__main__':
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS cars")
    db.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS cars (car_id TEXT, image INTEGER, number TEXT, is_correct BOOLEAN, need_adition_check BOOLEAN)")

    db.commit()
    main()

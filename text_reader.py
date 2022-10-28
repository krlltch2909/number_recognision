import pytesseract
import easyocr
import numpy as np
import cv2
from string import digits, ascii_uppercase, ascii_lowercase

car_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')


def run_tesseract(img) -> str:
    """
    :param img: image from which we want to read text
    :return: text which was read from image
    """
    try:
        alphanumeric = "" + digits + ascii_uppercase
        options = f' --oem 3 --psm 7 -c tessedit_char_whitelist={alphanumeric}'

        img = cv2.resize(img, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        img = cv2.medianBlur(gray, 5)
        # img = cv2.GaussianBlur(img, (5, 5), 0)
        img = cv2.dilate(img, (5, 5), iterations=3)
        # img = cv2.erode(img, (5, 5), iterations=1)

        thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        text: str = pytesseract.image_to_string(thresh, config=options)

        return text
    except:
        return 'tesseract error'


def easy_osr_reader(img) -> list:
    """
    :param img: image from which we want to read text
    :return: text which was read from image
    """

    img = cv2.resize(img, None, fx=20, fy=20, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 7)
    gray = cv2.GaussianBlur(gray, (5, 5), 5)

    cv2.imshow('gray', gray)

    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 7)
    thresh = cv2.dilate(thresh, (5, 5), iterations=5)

    # img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
    cv2.imshow('thresh_before', thresh)
    reader = easyocr.Reader(['en'], gpu=True, verbose=False)
    text = reader.readtext(thresh, detail=0, paragraph=True)
    return text[0]


def main():
    img = cv2.imread('numbers/93.jpeg')
    print('tesseract: ' + run_tesseract(img))
    # print('easy_osr ' + str(easy_osr_reader(img)))
    cv2.waitKey(0)


if __name__ == '__main__':
    main()

import pytesseract
import easyocr
import numpy as np
import cv2
from string import digits, ascii_uppercase, ascii_lowercase


def run_tesseract(img) -> str:
    """
    :param img: image from which we want to read text
    :return: text which was read from image
    """
    try:
        alphanumeric = "" + digits + ascii_uppercase
        options = f' --oem 3 --psm 7 -c tessedit_char_whitelist={alphanumeric}'

    # image_copy = img.copy()
    # image_copy = cv2.resize(image_copy, None, fx=8, fy=8, interpolation=cv2.INTER_CUBIC)
    #
    # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #
    # img = cv2.resize(gray, None, fx=10, fy=10, interpolation=cv2.INTER_CUBIC)
    #
    # img = cv2.medianBlur(img, 5)
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    # img = cv2.dilate(img, (5, 5), iterations=1)
    # img = cv2.erode(img, (5, 5), iterations=1)
    #
    # ret, thresh = cv2.threshold(img, 75, 255, cv2.THRESH_BINARY)
    #
    #
    #
    # contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(image=image_copy, contours=contours[:5], contourIdx=-1, color=(0, 0, 255), thickness=2,
    #                  lineType=cv2.LINE_AA)

    # licensePlate = None
    # text = ''
    # for c in contours[:10]:
    #
    #     (x, y, w, h) = cv2.boundingRect(c)
    #     ar = w / float(h)
    #
    #     if ar >= 4 and ar <= 5:
    #         licensePlate = thresh[y:y + h, x:x + w]
    #
    #         cv2.imshow('image', licensePlate)


    # thresh = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 3)



    # cv2.imshow('thresh', thresh)
        text: str = pytesseract.image_to_string(img, config=options)

        return text
    except:
        return 'tesseract error'


def easy_osr_reader(img) -> list:
    """
    :param img: image from which we want to read text
    :return: text which was read from image
    """

    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
    reader = easyocr.Reader(['en'], gpu=True, verbose=False)
    text = reader.readtext(img, detail=0, paragraph=True)
    return text


def main():
    img = cv2.imread('numbers/93.jpeg')
    print('tesseract: ' + run_tesseract(img))
    # print('easy_osr ' + str(easy_osr_reader(img)))
    cv2.waitKey(0)


if __name__ == '__main__':
    main()

import pytesseract
import easyocr
import cv2
from string import digits, ascii_uppercase


def run_tesseract(img) -> str:
    """
    :param img: image from which we want to read text
    :return: text which was read from image
    """

    try:
        alphanumeric = "" + digits +ascii_uppercase
        options = ' --oem 3 --psm 7 -c tessedit_char_whitelist={}'.format(alphanumeric)
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)
        #
        # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # thresh = cv
        # #
        # cv2.imshow('img', img)
        text: str = pytesseract.image_to_string(img, config=options)
        return text.strip()
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
    img = cv2.imread('numbers/img4.jpeg')
    print('tesseract ' + run_tesseract(img))
    print('easy_osr ' + str(easy_osr_reader(img)))


if __name__ == '__main__':
    main()


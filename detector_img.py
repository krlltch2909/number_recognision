import cv2

car_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')


img = cv2.imread('numbers/img3.jpeg')

img = cv2.resize(img, (100, 30))

gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
gray = cv2.GaussianBlur(gray, (7,7), 0)

rez = car_cascade.detectMultiScale(gray, 1.1, 6)

for (x,y,w,h) in rez:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_color = img[y:y+h, x:x+w]


cv2.imshow('gray', gray)
cv2.imshow('img',img)
cv2.waitKey(0)
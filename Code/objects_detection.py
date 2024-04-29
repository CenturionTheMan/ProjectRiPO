import cv2 as cv


class ObjectsDetector:
    def __init__(self):
        self.car_cascade = cv.CascadeClassifier('cv2/data/haarcascades/haarcascade_car5.xml')
        self.human_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_fullbody.xml')


    def detect_objects(self, frame):
        gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cars = self.car_cascade.detectMultiScale(gray_image, 1.4, 6)
        #humans = self.human_cascade.detectMultiScale(gray_image, 1.1, 3)

        for (x, y, w, h) in cars:
            cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        #for (x, y, w, h) in humans:
        #    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

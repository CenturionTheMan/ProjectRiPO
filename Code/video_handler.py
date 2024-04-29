import numpy as np
import cv2 as cv


class VideoHandler:
    def __init__(self, path_for_video_file: str):
        self.capture = cv.VideoCapture(path_for_video_file)

    def get_next_frame(self) -> np.ndarray:
        if not self.capture.isOpened():
            self.capture.release()
            cv.destroyAllWindows()
            return None

        ret, frame = self.capture.read()
        if ret:
            return frame
        else:
            return None


    def display_frame(self, frame):
        cv.namedWindow('Display', cv.WINDOW_GUI_EXPANDED)
        cv.imshow('Display', frame)

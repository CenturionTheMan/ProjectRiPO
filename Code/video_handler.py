import numpy as np
import cv2 as cv


class VideoHandler:
    def __init__(self, path_for_video_file: str, force_frame_size: tuple[int, int] | None = None):
        self.capture = cv.VideoCapture(path_for_video_file)
        self.frame_size = force_frame_size

    def get_next_frame(self) -> np.ndarray:
        if not self.capture.isOpened():
            self.capture.release()
            cv.destroyAllWindows()
            return None

        ret, frame = self.capture.read()
        if self.frame_size is not None:
            frame = cv.resize(frame, self.frame_size)
        if ret:
            return frame
        else:
            return None

    def display_frame(self, frame):
        cv.namedWindow('Display', cv.WINDOW_GUI_EXPANDED) # makes window resizable
        #if self.frame_size is not None:
        #    cv.resizeWindow('Display', self.frame_size)
        cv.imshow('Display', frame)

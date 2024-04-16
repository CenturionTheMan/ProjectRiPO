from cv2 import (VideoCapture, imshow, waitKey, destroyAllWindows, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS)
import numpy as np
import cv2


class VideoHandler:
    def __init__(self, path_for_video_file: str):
        self.capture = VideoCapture(path_for_video_file)

    def get_next_frame(self) -> np.ndarray:
        if not self.capture.isOpened():
            self.capture.release()
            destroyAllWindows()
            return None

        ret, frame = self.capture.read()
        if ret:
            return frame
        else:
            return None

    def display_frame(self, frame):
        imshow('Displaying image frames from video file', frame)

    def draw_line(self, frame, x1: int, y1: int, x2: int, y2: int, line_thickness: int, rgb: tuple[int, int, int]):
        cv2.line(frame, (x1, y1), (x2, y2), (rgb[2], rgb[1], rgb[0]), thickness=line_thickness)
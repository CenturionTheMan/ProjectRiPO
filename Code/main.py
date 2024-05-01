import math

import cv2

from video_handler import VideoHandler
from line_drawer import draw_parking_line
from objects_detection import ObjectsDetector

if __name__ == '__main__':
    video_handler = VideoHandler('../Videos/2024-03-30_14-15-32-back.mp4')
    objects_detector = ObjectsDetector()

    frame_size = (640, 480)

    frame = video_handler.get_next_frame(frame_size)
    height = frame.shape[0]
    width = frame.shape[1]

    while frame is not None:
        objects_detector.detect_cars_yolo5(frame)

        draw_parking_line(frame, pivot=(width * 0.15, 0), angle_deg=15, length=700, max_thickness=30, min_thickness=10, rgb=(255, 255, 255))
        draw_parking_line(frame, pivot=(width * 0.85, 0), angle_deg=-15, length=700, max_thickness=30, min_thickness=10, rgb=(255, 255, 255))

        video_handler.display_frame(frame)
        frame = video_handler.get_next_frame(frame_size)
        if cv2.waitKey(1) == 27:
            break


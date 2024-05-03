import math
import time

import cv2
import torch
from video_handler import VideoHandler
from line_drawer import draw_parking_line
from objects_detection import ObjectsDetector
import supervision as sv

if __name__ == '__main__':
    video_handler = VideoHandler('../Videos/2024-03-27_13-15-35-front.mp4')

    objects = {
        2: ((255, 0, 0), 1), # car
        7: ((255, 0, 0), 1), # truck
        0: ((0, 255, 0), 1),  # person
        11: ((0, 0, 255), 1)  # stop sign
    }
    objects_detector = ObjectsDetector(objects)

    #frame_size = (640, 480)

    frame_rate = video_handler.capture.get(cv2.CAP_PROP_FPS)
    print(frame_rate)
    frame = video_handler.get_next_frame()
    height = frame.shape[0]
    width = frame.shape[1]

    while frame is not None:
        objects_detector.detect_and_mark_objects(frame, draw_on_th_frame=3)

        # draw_parking_line(frame, pivot=(width * 0.15, 0), angle_deg=15, length=700, max_thickness=30, min_thickness=10, rgb=(255, 255, 255))
        # draw_parking_line(frame, pivot=(width * 0.85, 0), angle_deg=-15, length=700, max_thickness=30, min_thickness=10, rgb=(255, 255, 255))

        video_handler.display_frame(frame)
        frame = video_handler.get_next_frame()
        time.sleep(1 / frame_rate) # potrzebne, żeby wideo odtwarzało się z odpowiednią prędkością
        # | poszukać lepszego rozwiązania na to
        if cv2.waitKey(1) == 27:
            break

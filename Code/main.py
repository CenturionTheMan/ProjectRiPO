import math
import time

import cv2
import torch
from video_handler import VideoHandler
from line_drawer import draw_parking_line
from objects_detection import ObjectsDetector
import supervision as sv

if __name__ == '__main__':
    # torch.set_default_device("mps")

    video_handler = VideoHandler('../Videos/2024-03-30_14-15-32-back.mp4')
    objects_detector = ObjectsDetector()

    # frame_size = (640, 480)
    # frame_size = (1280, 720)

    framerate = video_handler.capture.get(cv2.CAP_PROP_FPS)
    print(framerate)
    frame = video_handler.get_next_frame()
    height = frame.shape[0]
    width = frame.shape[1]
    # można by znaleźć jakiś lepszy sposób na skalowanie, aktualnie pierwsza klatka wyświetla
    # się w oryginalnej rozdzielczości
    frame_size = (round(width * 0.5), round(height * 0.5))
    frame_number = 0
    results = None

    while frame is not None:
        if True: #frame_number % 3 == 0:
            results = objects_detector.detect_cars_yolo5(frame)
            frame_number = 0
        frame_number += 1

        for res in results:
            label = int(res[-1])
            if label == 2:  # Label for car in COCO dataset
                # Draw bounding box
                x_min, y_min, x_max, y_max, conf = map(int, res[:5])
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
            elif label == 0:
                # Draw bounding box
                x_min, y_min, x_max, y_max, conf = map(int, res[:5])
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

        # draw_parking_line(frame, pivot=(width * 0.15, 0), angle_deg=15, length=700, max_thickness=30, min_thickness=10, rgb=(255, 255, 255))
        # draw_parking_line(frame, pivot=(width * 0.85, 0), angle_deg=-15, length=700, max_thickness=30, min_thickness=10, rgb=(255, 255, 255))

        video_handler.display_frame(frame)
        frame = video_handler.get_next_frame(frame_size)
        time.sleep(1 / framerate) # potrzebne, żeby wideo odtwarzało się z odpowiednią prędkością
        # | poszukać lepszego rozwiązania na to
        if cv2.waitKey(1) == 27:
            break

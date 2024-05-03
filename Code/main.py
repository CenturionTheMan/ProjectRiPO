import math
import time

import cv2
import torch
from video_handler import VideoHandler
from line_drawer import draw_parking_line
from objects_detection import YoloObjectsDetector, draw_boxes, RoboflowObjectsDetector
import supervision as sv

if __name__ == '__main__':
    video_handler = VideoHandler('../Videos/3.mp4')

    yolo_objects = {
        2: ((0, 255, 255), 1), # car
        7: ((0, 255, 255), 1), # truck
        0: ((0, 255, 0), 1),  # person
        11: ((255, 0, 255),1) # stop sign
    }

    roboflow_objects = {
        "Speed Limit 30": ((255, 0, 255),1),
        "Speed Limit 40": ((255, 0, 255),1),
        "Speed Limit 50": ((255, 0, 255),1),
        "Speed Limit 60": ((255, 0, 255),1),
        "Speed Limit 70": ((255, 0, 255),1),
        "speed limit \"30\"": ((255, 0, 255),1),
        "speed limit \"40\"": ((255, 0, 255),1),
        "speed limit \"50\"": ((255, 0, 255),1),
        "speed limit \"60\"": ((255, 0, 255),1),
        "speed limit \"70\"": ((255, 0, 255),1),
        "speed limit \"80\"": ((255, 0, 255),1),
        "speed limit \"100\"": ((255, 0, 255),1),
        "speed limit \"110\"": ((255, 0, 255),1),
        "speed limit \"120\"": ((255, 0, 255),1),
        "speed limit \"130\"": ((255, 0, 255),1),
    }

    yolo_objects_detector = YoloObjectsDetector(yolo_objects)
    roboflow_objects_detector = RoboflowObjectsDetector(roboflow_objects)

    frame_rate = video_handler.capture.get(cv2.CAP_PROP_FPS)
    print(frame_rate)
    frame = video_handler.get_next_frame()
    height = frame.shape[0]
    width = frame.shape[1]

    while frame is not None:
        detections = yolo_objects_detector.detect_objects(frame, draw_on_th_frame=2)
        draw_boxes(frame, detections)

        detections = roboflow_objects_detector.detect_objects(frame=frame, draw_on_th_frame=3)
        draw_boxes(frame, detections)

        # draw_parking_line(frame, pivot=(width * 0.15, 0), angle_deg=15, length=700, max_thickness=30, min_thickness=10, rgb=(255, 255, 255))
        # draw_parking_line(frame, pivot=(width * 0.85, 0), angle_deg=-15, length=700, max_thickness=30, min_thickness=10, rgb=(255, 255, 255))

        video_handler.display_frame(frame)
        frame = video_handler.get_next_frame()
        time.sleep(1 / frame_rate) # potrzebne, żeby wideo odtwarzało się z odpowiednią prędkością
        # | poszukać lepszego rozwiązania na to
        if cv2.waitKey(1) == 27:
            break

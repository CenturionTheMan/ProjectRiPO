import math
import time

import cv2
from cv2 import waitKey
import torch
from video_handler import VideoHandler
from line_drawer import draw_parking_line
from objects_detection import YoloObjectsDetector, draw_boxes, RoboflowObjectsDetector
import supervision as sv

if __name__ == '__main__':
    # init objects detection
    yolo_objects = {
        2: ((0, 255, 255), 1), # car
        7: ((0, 255, 255), 1), # truck
        0: ((0, 255, 0), 1),  # person
        11: ((255, 0, 0),1) # stop sign
    }

    roboflow_objects = {
        #"30": ((255, 0, 0),1),
        #"40": ((255, 0, 0),1),
        #"50": ((255, 0, 0),1),
        #"60": ((255, 0, 0),1),
        #"70": ((255, 0, 0),1),
        "Roboty_drogowe": ((255,255, 0),1),
        "Zakaz_wyprzedzania": ((255,255, 0),1),
        #"Zakaz_zatrzymywania": ((255, 0, 0),1),
        #"koniec": ((255, 0, 255),1), - słabo działą
        "koniec_pierwszenstwa": ((255, 255, 0),1),
        "niebezpieczenstwo": ((255, 255, 0),1),
        #"pierwszenstwo": ((255, 0, 255),1),
        "prog": ((255, 255, 0),1),
        #"przejscie": ((0, 0, 255),1),
        #"stop": ((255, 0, 0),1), - detected by YOLO
        "ustap uwaga_dzieci": ((255, 255, 0),1),
        #"zakaz_wjazdu ": ((255, 0, 0),1),
        "zwierzyna": ((255, 255, 0),1),
    }

    yolo_objects_detector = YoloObjectsDetector(yolo_objects, confidence_threshold=0.77)
    roboflow_objects_detector = RoboflowObjectsDetector(roboflow_objects, confidence_threshold=0.6)

    # lines settings
    pivot_distance_from_side = 0.05
    line_angle_deg = 32
    line_length = 700
    max_thickness = 30
    min_thickness = 10
    line_color = (255, 255, 255)
    is_line = False

    # handle video
    video_handler = VideoHandler('../Videos/3.mp4', force_frame_size=None)
    frame_rate = video_handler.capture.get(cv2.CAP_PROP_FPS)
    print("frame rate: " + str(frame_rate))
    frame = video_handler.get_next_frame()
    height = frame.shape[0]
    width = frame.shape[1]

    while frame is not None:
        detections = yolo_objects_detector.detect_objects(frame, draw_on_th_frame=2)
        draw_boxes(frame, detections)

        detections = roboflow_objects_detector.detect_objects(frame, draw_on_th_frame=3)
        draw_boxes(frame, detections)

        if is_line:
            draw_parking_line(frame, pivot=(width * pivot_distance_from_side, 0), angle_deg=line_angle_deg,
                              length=line_length, max_thickness=max_thickness, min_thickness=min_thickness, rgb=line_color)
            draw_parking_line(frame, pivot=(width * (1 - pivot_distance_from_side), 0), angle_deg=-line_angle_deg,
                              length=line_length, max_thickness=max_thickness, min_thickness=min_thickness, rgb=line_color)

        video_handler.display_frame(frame)
        frame = video_handler.get_next_frame()
        time.sleep(1 / frame_rate)
        key = waitKey(1)

        if key == 27:  # ESC
            break
        elif key == 108:  # 'l' key
            is_line = not is_line
            print(f"Lines: {is_line}")
        elif key == 32:  # space
            waitKey(0)
        elif key == 100:  # 'd' key
            pivot_distance_from_side += 0.01
            print(f"pivot_distance_from_side: {pivot_distance_from_side}")
        elif key == 97:  # 'a' - key
            pivot_distance_from_side -= 0.01
            print(f"pivot_distance_from_side: {pivot_distance_from_side}")
        elif key == 119:  # 'w' key
            line_length += 10
            print(f"line_length: {line_length}")
        elif key == 115:  # 's' key
            line_length -= 10
            print(f"line_length: {line_length}")
        elif key == 120:  # x
            line_angle_deg += 1
            print(f"line_angle_deg: {line_angle_deg}")
        elif key == 122:  # z
            line_angle_deg -= 1
            print(f"line_angle_deg: {line_angle_deg}")
        if key != -1:
            print(key)

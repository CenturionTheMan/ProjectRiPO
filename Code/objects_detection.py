import yolov5
import numpy as np
import torch
import cv2
from threading import Thread
import torchvision


class ObjectsDetector:
    def __init__(self, objects_to_detect: dict[int, tuple[tuple[int, int, int], int]]):
        # load pretrained model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.model.conf = 0.10  # NMS confidence threshold
        self.model.iou = 0.45  # NMS IoU threshold
        self.model.agnostic = False  # NMS class-agnostic
        self.model.multi_label = False  # NMS multiple labels per box
        self.model.max_det = 10  # maximum number of detections per image

        if torch.cuda.is_available():
            device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            device = torch.device("mps")
        else:
            device = torch.device("cpu")
        self.model.to(device)
        print(f"mps:{next(self.model.parameters()).is_mps}")
        print(f"cuda:{next(self.model.parameters()).is_cuda}")

        self.counter = 0
        self.detected_objects = []
        self.objects_to_detect = objects_to_detect
        self.thread = None

    def detect_and_mark_objects(self, frame, draw_on_th_frame=5):
        if len(self.detected_objects) == 0:
            self.__detect_objects(frame)

        if self.counter < draw_on_th_frame:
            self.counter += 1

        if self.counter == draw_on_th_frame and (self.thread is None or not self.thread.is_alive()):
            self.counter = 0
            thread = Thread(target=self.__detect_objects, args=(frame,))
            thread.start()
        else:
            self.counter += 1

        for label, x_min, y_min, x_max, y_max, conf in self.detected_objects:
            color, thickness = self.objects_to_detect[label]
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, thickness)

    def __detect_objects(self, frame):
        results = self.model(frame)
        detections = []
        for res in results.xyxy[0]:
            label = int(res[-1])
            if label in self.objects_to_detect:
                # Draw bounding box
                x_min, y_min, x_max, y_max, conf = map(int, res[:5])
                detections.append((label, x_min, y_min, x_max, y_max, conf))
        self.detected_objects = detections
        return detections

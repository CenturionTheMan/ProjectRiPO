import numpy as np
import torch
import cv2
from threading import Thread
import torchvision
#import yolov5
from inference import get_model
import supervision as sv
from dataclasses import dataclass




@dataclass
class ObjectDetection:
    object_name: str
    bottom_left_corner: tuple[int, int]
    top_right_corner: tuple[int, int]
    color: tuple[int, int, int]
    thickness: int

def draw_boxes(frame, detections: list[ObjectDetection]):
    for detection in detections:
        cv2.rectangle(frame, detection.bottom_left_corner, detection.top_right_corner, detection.color, detection.thickness)


class YoloObjectsDetector:
    def __init__(self, objects_to_detect: dict[int, tuple[tuple[int, int, int], int]]):
        # load pretrained model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.model.conf = 0.20  # NMS confidence threshold
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
        self.detected_objects = None
        self.objects_to_detect = objects_to_detect
        self.thread = None

        self.label_decoder = {
            0: "person",
            2: "car",
            7: "truck",
            11: "stop sign",
        }

    def detect_objects(self, frame, draw_on_th_frame=5):
        if self.detected_objects is None:
            self.__detect_objects(frame)

        if self.counter < draw_on_th_frame:
            self.counter += 1

        if self.counter == draw_on_th_frame and (self.thread is None or not self.thread.is_alive()):
            self.counter = 0
            thread = Thread(target=self.__detect_objects, args=(frame,))
            thread.start()
        else:
            self.counter += 1

        return self.detected_objects

    def __detect_objects(self, frame):
        results = self.model(frame)
        detections = []
        for res in results.xyxy[0]:
            label = int(res[-1])
            if label in self.objects_to_detect:
                # Draw bounding box
                x_min, y_min, x_max, y_max, conf = map(int, res[:5])
                color, thickness = self.objects_to_detect[label]
                obj = ObjectDetection(self.label_decoder[label], (x_min, y_min), (x_max, y_max), color, thickness)
                detections.append(obj)
        self.detected_objects = detections


class SignsObjectsDetector:
    def __init__(self):
        self.model = get_model(model_id="znaki-drogowe-w-polsce/15", api_key="1UHD3uECCOTgnJZg0Lh8")
        self.model.confidence_threshold = 0.05
        self.model.iou_threshold = 0.4
        self.model.max_det = 10
        self.model.agnostic = False
        self.counter = 1
        self.detected_objects = None

    def detect_signs(self, frame, draw_on_th_frame=5):
        if self.counter % draw_on_th_frame == 1:
            results = self.model.infer(frame)
            detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))
            objects = []
            for label, cords in zip(detections.data['class_name'], detections.xyxy):
                obj = ObjectDetection(label, (int(cords[0]), int(cords[1])), (int(cords[2]), int(cords[3])), (0, 0, 255), 1)
                objects.append(obj)
            self.detected_objects = objects

        if self.counter < draw_on_th_frame - 1:
            self.counter += 1
        else:
            self.counter = 0
        return self.detected_objects

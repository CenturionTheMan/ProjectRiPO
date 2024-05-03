# import yolov5
import numpy as np
# from ultralytics import YOLO
import torch
from inference import get_model
# zainstalować też inference-gpu
import cv2


class ObjectsDetector:
    def __init__(self):
        # load pretrained model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        # self.model = YOLO('yolov5s.pt')
        self.model.conf = 0.10  # NMS confidence threshold
        self.model.iou = 0.45  # NMS IoU threshold
        self.model.agnostic = False  # NMS class-agnostic
        self.model.multi_label = False  # NMS multiple labels per box
        self.model.max_det = 10  # maximum number of detections per image

        self.model2 = get_model(model_id="znaki-drogowe-w-polsce/15", api_key="")
        self.model2.confidence_threshold = 0.1
        self.model2.iou_threshold = 0.45
        self.model2.max_det = 10
        self.model2.agnostic = False
        # print(next(self.model.parameters().is_cuda))

        if torch.cuda.is_available():
            device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            device = torch.device("mps")
        else:
            device = torch.device("cpu")
        self.model.to(device)

        print(f"mps:{next(self.model.parameters()).is_mps}")
        print(f"cuda:{next(self.model.parameters()).is_cuda}")

    def detect_cars_yolo5(self, frame, color=(255, 0, 0), thickness=2):
        results = self.model(frame)
        results2 = self.model2.infer(frame)
        return results.xyxy[0], results2
        # for res in results.xyxy[0]:
        #     label = int(res[-1])
        #     if label == 2:  # Label for car in COCO dataset
        #         # Draw bounding box
        #         x_min, y_min, x_max, y_max, conf = map(int, res[:5])
        #         cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, thickness)

# import yolov5
import numpy as np
import torch
import cv2


class ObjectsDetector:
    def __init__(self):
        # load pretrained model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.model.conf = 0.10  # NMS confidence threshold
        self.model.iou = 0.45  # NMS IoU threshold
        self.model.agnostic = False  # NMS class-agnostic
        self.model.multi_label = False  # NMS multiple labels per box
        self.model.max_det = 10  # maximum number of detections per image
        # print(next(self.model.parameters().is_cuda))

        # mps_device = torch.device("mps")
        # self.model.to(mps_device)

    def detect_cars_yolo5(self, frame, color=(255, 0, 0), thickness=2):
        results = self.model(frame)
        return results.xyxy[0]
        # for res in results.xyxy[0]:
        #     label = int(res[-1])
        #     if label == 2:  # Label for car in COCO dataset
        #         # Draw bounding box
        #         x_min, y_min, x_max, y_max, conf = map(int, res[:5])
        #         cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, thickness)


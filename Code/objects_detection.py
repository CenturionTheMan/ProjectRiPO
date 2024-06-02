import os
import torch
import cv2
import time
from inference import get_model
import supervision as sv
from dataclasses import dataclass
from user_settings import get_current_settings
from playsound import playsound


@dataclass
class ObjectDetection:
    object_name: str
    confidence_percent: float
    top_left_corner: tuple[int, int]
    bottom_right_corner: tuple[int, int]
    color: tuple[int, int, int]
    thickness: int


def draw_boxes(frame, detections: list[ObjectDetection]):
    for detection in detections:
        cv2.rectangle(frame, detection.top_left_corner, detection.bottom_right_corner, detection.color,
                      detection.thickness)
        name = detection.object_name.replace("-", " ").replace("_", " ").lower()
        cv2.putText(frame, f"[{name}] - {detection.confidence_percent}%",
                    (detection.top_left_corner[0], detection.top_left_corner[1] - detection.thickness * 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    detection.color, detection.thickness, cv2.LINE_AA)
        # print(detection.object_name)


class YoloObjectsDetector:
    def __init__(self, confidence_threshold: float = 0.5):
        # load pretrained model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.model.conf = confidence_threshold  # NMS confidence threshold
        self.model.iou = 0.5  # NMS IoU threshold
        self.model.agnostic = False  # NMS class-agnostic
        self.model.multi_label = False  # NMS multiple labels per box
        self.model.max_det = 20  # maximum number of detections per image

        self.last_played = time.time()

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

        self.label_decoder = {
            0: "person",
            2: "car",
            7: "truck",
            11: "stop sign",
        }
        self.all_labels = [0, 2, 7, 11]

    def detect_objects(self, frame, objects_to_detect: dict[int, tuple[tuple[int, int, int], int]], draw_on_th_frame=5):
        if self.detected_objects is None:
            self.__detect_objects(frame, objects_to_detect)
            return self.detected_objects

        if self.counter < draw_on_th_frame:
            self.counter += 1
        else:
            self.counter = 0
            self.__detect_objects(frame, objects_to_detect)
        return self.detected_objects

    def __detect_objects(self, frame, objects_to_detect):
        settings = get_current_settings()

        label_dict = {
            0: settings.people_alert_type,
            2: settings.cars_alert_type,
            7: settings.cars_alert_type,
            11: settings.stop_signs_alert_type
        }

        # select which objects to play sound for and which to return for drawing bounding boxes
        box_labels = []
        sound_labels = []
        for label in self.all_labels:
            alert_type = label_dict[label]
            if alert_type == "box":
                box_labels.append(label)
            elif alert_type == "sound":
                sound_labels.append(label)

        results = self.model(frame)
        detections = []
        for res in results.xyxy[0]:
            label = int(res[-1])
            if label in objects_to_detect:
                if label in box_labels:
                    x_min, y_min, x_max, y_max = map(int, res[:4])
                    conf = float(res[4])
                    color, thickness = objects_to_detect[label]
                    color = (color[2], color[1], color[0])
                    obj = ObjectDetection(self.label_decoder[label], round(conf * 100, 0), (x_min, y_min),
                                          (x_max, y_max), color, thickness)
                    detections.append(obj)
                elif label in sound_labels:
                    current_time = time.time()
                    if current_time - self.last_played >= 0.4:
                        playsound("sounds/alert.mp3", block=False)
                        self.last_played = current_time
        self.detected_objects = detections


class RoboflowObjectsDetector:
    def __init__(self, model_name: str, confidence_threshold: float = 0.5):
        # trafficsigndetection-vwdix/10 - cross walks really good - https://universe.roboflow.com/trafficsign-bzwfa/trafficsigndetection-vwdix/model/10
        # "kaggle-datasets-for-traffic/2" - speed limit detection - https://universe.roboflow.com/school-0ljld/kaggle-datasets-for-traffic/model/2
        # "kaggle-datasets-for-traffic/2" - jako tako daje rade wykrywac ostrzegawcze
        self.model = get_model(model_id=model_name, api_key=os.getenv("ROBOFLOW_KEY"))
        self.model.confidence_threshold = confidence_threshold  # does not work??
        self.confidence_threshold = confidence_threshold
        self.model.iou_threshold = 0.4
        self.model.max_det = 10
        self.model.agnostic = False
        self.counter = 1
        self.detected_objects = None

        self.last_played = time.time()

    def detect_objects(self, frame, objects_to_detect: dict[str, tuple[tuple[int, int, int], int]], draw_on_th_frame=5):
        if self.detected_objects is None:
            self.__detect_object(frame, objects_to_detect)
            return self.detected_objects

        if self.counter < draw_on_th_frame:
            self.counter += 1
        else:
            self.counter = 0
            self.__detect_object(frame, objects_to_detect)
        return self.detected_objects

    def __detect_object(self, frame, objects_to_detect):
        settings = get_current_settings()
        results = self.model.infer(frame)
        detections = sv.Detections.from_inference(results[0].dict(by_alias=True, exclude_none=True))
        objects = []
        for label, cords, conf in zip(detections.data['class_name'], detections.xyxy, detections.confidence):
            # print(f'[{round(conf, 2)}] {label}')
            if label in objects_to_detect and conf > self.confidence_threshold:
                if settings.warning_signs_alert_type == "box":
                    color, thickness = objects_to_detect[label]
                    color = (color[2], color[1], color[0])
                    obj = ObjectDetection(label, round(conf * 100, 0), (int(cords[0]), int(cords[1])),
                                          (int(cords[2]), int(cords[3])), color, thickness)
                    objects.append(obj)
                elif settings.warning_signs_alert_type == "sound":
                    current_time = time.time()
                    if current_time - self.last_played >= 0.4:
                        playsound("sounds/alert.mp3", block=False)
                        self.last_played = current_time
        self.detected_objects = objects

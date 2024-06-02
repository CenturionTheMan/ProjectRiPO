import numpy as np
import cv2 as cv
from objects_detection import YoloObjectsDetector, draw_boxes, RoboflowObjectsDetector
import time
import cv2
from cv2 import waitKey
from line_drawer import draw_parking_line
from user_settings import get_current_settings
from threading import Thread


class VideoHandler:
    def __init__(self, root, force_frame_size: tuple[int, int] | None = None):
        self.__root = root
        self.__capture = None
        self.__frame_size = force_frame_size
        self.__is_stop_requested = False
        self.video_playing = False

    def __dispose_capture(self):
        if self.__capture is not None:
            self.__capture.release()
            cv.destroyAllWindows()
            self.__capture = None
            self.video_playing = False

    def __get_next_frame(self) -> np.ndarray | None:
        if self.__capture is None:
            return None

        if not self.__capture.isOpened():
            self.__dispose_capture()
            return None

        ret, frame = self.__capture.read()
        if self.__frame_size is not None:
            frame = cv.resize(frame, self.__frame_size)
        if ret:
            return frame
        else:
            return None

    def __display_frame(self, frame):
        cv.namedWindow('Display', cv.WINDOW_GUI_EXPANDED)  # makes window resizable
        if self.__frame_size is not None:
            cv.resizeWindow('Display', self.__frame_size)
        cv.imshow('Display', frame)
        root_x = self.__root.winfo_x()
        root_y = self.__root.winfo_y()
        _, _, video_width, _ = cv.getWindowImageRect('Display')
        video_x = root_x - video_width
        cv.moveWindow('Display', video_x, root_y)

    def play_video_on_new_thread(self, path_for_video_file: str) -> Thread:
        """
        Will start playing video on new thread
        
        Args:
            path_for_video_file: Path for video file
            
        Returns:
            thread object
        """
        t = Thread(target=self.play_video, args=(path_for_video_file,))
        t.start()
        return t

    def stop_video(self) -> None:
        """
        Method will stop currently playing video
        """
        self.__is_stop_requested = True

    def play_video(self, path_for_video_file: str) -> None:
        """
        Method will play video on current thread
        
        Args:
            path_for_video_file: path for video
        """
        self.__is_stop_requested = False
        self.video_playing = True
        if path_for_video_file == "0":
            self.__capture = cv.VideoCapture(0)
        else:
            self.__capture = cv.VideoCapture(path_for_video_file)

        # init objects detection
        yolo_objects_detector = YoloObjectsDetector(confidence_threshold=0.7)
        roboflow_objects_detector = RoboflowObjectsDetector(
            model_name="znaki-drogowe-w-polsce/15", confidence_threshold=0.6)

        # init video
        frame_rate = self.__capture.get(cv2.CAP_PROP_FPS)
        print("frame rate: " + str(frame_rate))
        frame = self.__get_next_frame()
        if frame is None:
            raise Exception("Can not find video at given path ...")

        width = frame.shape[1]

        while frame is not None and self.__is_stop_requested is False:
            # measure frame start time
            start_time = time.time()

            # get config for object detection
            yolo_objects, roboflow_objects = get_detection_objects_config()

            # detect objects
            detections = yolo_objects_detector.detect_objects(frame, yolo_objects, draw_on_th_frame=2)
            draw_boxes(frame, detections)

            detections = roboflow_objects_detector.detect_objects(frame, roboflow_objects, draw_on_th_frame=3)
            draw_boxes(frame, detections)

            # get config for lines
            pivot_distance_from_side, line_angle_deg, line_length, max_thickness, min_thickness, line_color, is_line = get_lines_config()
            if is_line:
                draw_parking_line(frame, pivot=(width * pivot_distance_from_side, 0), angle_deg=line_angle_deg,
                                  length=line_length, max_thickness=max_thickness, min_thickness=min_thickness,
                                  rgb=line_color)
                draw_parking_line(frame, pivot=(width * (1 - pivot_distance_from_side), 0), angle_deg=-line_angle_deg,
                                  length=line_length, max_thickness=max_thickness, min_thickness=min_thickness,
                                  rgb=line_color)

            # display frame and get next one
            self.__display_frame(frame)
            frame = self.__get_next_frame()

            # handle constant frame rate
            elapsed_time = time.time() - start_time
            delay_time = max(1, int((1 / frame_rate - elapsed_time) * 1000))  # Calculate delay time in milliseconds
            key = waitKey(delay_time)

            if key == 27:  # ESC
                break
        self.__dispose_capture()


def get_detection_objects_config():
    settings = get_current_settings()

    yolo_objects = {
        2: (settings.detection_color_cars, settings.detection_thickness_cars),  # car
        7: (settings.detection_color_cars, settings.detection_thickness_cars),  # truck
        0: (settings.detection_color_people, settings.detection_thickness_people),  # person
        11: (settings.detection_color_stop_signs, settings.detection_thickness_stop_signs)  # stop sign
    }

    roboflow_objects = {
        "Roboty_drogowe": (settings.detection_color_warning_signs, settings.detection_thickness_warning_signs),
        "koniec_pierwszenstwa": (settings.detection_color_warning_signs, settings.detection_thickness_warning_signs),
        "niebezpieczenstwo": (settings.detection_color_warning_signs, settings.detection_thickness_warning_signs),
        "prog": (settings.detection_color_warning_signs, settings.detection_thickness_warning_signs),
        "ustap": (settings.detection_color_warning_signs, settings.detection_thickness_warning_signs),
        "uwaga_dzieci": (settings.detection_color_warning_signs, settings.detection_thickness_warning_signs),
        "zwierzyna": (settings.detection_color_warning_signs, settings.detection_thickness_warning_signs),
    }
    return yolo_objects, roboflow_objects


def get_lines_config():
    s = get_current_settings()
    return s.lines_pivot_distance_from_edge, s.lines_angle, s.lines_length, s.lines_max_thickness, s.lines_min_thickness, s.lines_color, s.lines_is_on

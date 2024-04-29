import math

from cv2 import waitKey

from video_handler import VideoHandler
from line_drawer import draw_parking_line
from objects_detection import ObjectsDetector

if __name__ == '__main__':
    video_handler = VideoHandler('../Videos/2024-03-30_14-15-32-back.mp4')
    objects_detector = ObjectsDetector()

    frame = video_handler.get_next_frame()
    height = frame.shape[0]
    width = frame.shape[1]
    while frame is not None:
        objects_detector.detect_objects(frame)

        draw_parking_line(frame, pivot=(width * 0.2, 0), angle_deg=-10, length=700, line_thickness=20, rgb=(255, 255, 255))
        draw_parking_line(frame, pivot=(width * 0.8, 0), angle_deg=10, length=700, line_thickness=20, rgb=(255, 255, 255))

        video_handler.display_frame(frame)
        frame = video_handler.get_next_frame()
        if waitKey(1) == 27:
            break


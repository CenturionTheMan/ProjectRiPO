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
    pivot_distance_from_side = 0.05
    line_angle_deg = 32
    line_length = 700
    max_thckness = 30
    min_thickness = 10
    line_color = (255, 255, 255)
    while frame is not None:
        objects_detector.detect_objects(frame)

        draw_parking_line(frame, pivot=(width * pivot_distance_from_side, 0), angle_deg=line_angle_deg,
                          length=line_length, max_thickness=max_thckness, min_thickness=min_thickness, rgb=line_color)
        draw_parking_line(frame, pivot=(width * (1 - pivot_distance_from_side), 0), angle_deg=-line_angle_deg,
                          length=line_length, max_thickness=max_thckness, min_thickness=min_thickness, rgb=line_color)

        video_handler.display_frame(frame)
        frame = video_handler.get_next_frame()
        key = waitKey(1)
        # if key != -1:
        #     print(key)
        if key == 27:  # ESC
            break
        elif key == 32:  # space
            waitKey(0)
        elif key == 3:  # right arrow
            pivot_distance_from_side += 0.01
            print(f"pivot_distance_from_side: {pivot_distance_from_side}")
        elif key == 2:  # left arrow
            pivot_distance_from_side -= 0.01
            print(f"pivot_distance_from_side: {pivot_distance_from_side}")
        elif key == 0:  # up arrow
            line_length += 10
            print(f"line_length: {line_length}")
        elif key == 1:  # down arrow
            line_length -= 10
            print(f"line_length: {line_length}")
        elif key == 120:  # x
            line_angle_deg += 1
            print(f"line_angle_deg: {line_angle_deg}")
        elif key == 122:  # z
            line_angle_deg -= 1
            print(f"line_angle_deg: {line_angle_deg}")

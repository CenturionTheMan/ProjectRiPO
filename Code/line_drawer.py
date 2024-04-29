from math import *
import cv2 as cv


def draw_line_on_frame(frame, x1: int, y1: int, x2: int, y2: int, line_thickness: int, rgb: tuple[int, int, int]):
    cv.line(frame, (x1, y1), (x2, y2), (rgb[2], rgb[1], rgb[0]), thickness=line_thickness)


def draw_parking_line(frame, pivot: tuple[any, any], angle_deg, length, line_thickness, rgb: tuple[int, int, int]):
    const = pi/2
    radians = -angle_deg * (pi / 180)
    height = frame.shape[0]
    x2 = pivot[0] + length * cos(radians + const)
    y2 = pivot[1] + length * sin(radians + const)
    draw_line_on_frame(frame, int(pivot[0]), height - (pivot[1]), int(x2), height - int(y2), int(line_thickness), rgb)
from math import *
import cv2 as cv
import numpy as np


def draw_line_on_frame(frame, x1: int, y1: int, x2: int, y2: int, max_thickness: int, min_thickness: int,
                       rgb: tuple[int, int, int]):
    """
    Draws a line on the given frame with specified coordinates, maximum and minimum thickness, and color.

    Args:
    - frame: The image frame on which the line will be drawn.
    - x1, y1: The coordinates of the starting point of the line.
    - x2, y2: The coordinates of the ending point of the line.
    - max_thickness: The maximum thickness of the line.
    - min_thickness: The minimum thickness of the line.
    - rgb: The color of the line in RGB format.

    """
    # Convert RGB to BGR format
    color = (rgb[2], rgb[1], rgb[0])

    # Calculate line length
    line_length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Define the number of segments for the line
    num_segments = 20

    # Calculate the incremental change for perspective
    for i in range(num_segments):
        weight = i / num_segments
        x_start = int(x1 * (1 - weight) + x2 * weight)
        y_start = int(y1 * (1 - weight) + y2 * weight)
        x_end = int(x1 * (1 - (weight + 1 / num_segments)) + x2 * (weight + 1 / num_segments))
        y_end = int(y1 * (1 - (weight + 1 / num_segments)) + y2 * (weight + 1 / num_segments))

        # Calculate thickness based on distance from the viewer
        thickness = int(max_thickness * (1 - i / num_segments)) + int(min_thickness * (i / num_segments))
        thickness = max(min_thickness, min(thickness, max_thickness))

        start_point = (x_start, y_start)
        end_point = (x_end, y_end)
        cv.line(frame, start_point, end_point, color, thickness=thickness)


def draw_parking_line(frame, pivot: tuple[any, any], angle_deg, length, max_thickness: int, min_thickness: int, rgb: tuple[int, int, int]):
    const = pi/2
    radians = -angle_deg * (pi / 180)
    height = frame.shape[0]
    x2 = pivot[0] + length * cos(radians + const)
    y2 = pivot[1] + length * sin(radians + const)
    draw_line_on_frame(frame, int(pivot[0]), height - (pivot[1]), int(x2), height - int(y2), max_thickness, min_thickness, rgb)
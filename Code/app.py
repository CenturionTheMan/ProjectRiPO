from cv2 import waitKey

from video_handler import VideoHandler

if __name__ == '__main__':
    video_handler = VideoHandler('../Videos/2024-03-30_14-15-32-back.mp4')

    frame = video_handler.get_next_frame()
    height = frame.shape[0]
    width = frame.shape[1]
    while frame is not None:
        video_handler.draw_line(frame, 0, 0, height, width, 2, (255, 0, 0))
        video_handler.display_frame(frame)
        frame = video_handler.get_next_frame()
        if waitKey(25) == 27:
            break


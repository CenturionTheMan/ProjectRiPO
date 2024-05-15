from user_settings import get_current_settings
from threading import Thread
from video_handler import VideoHandler

if __name__ == '__main__':
    user_settings = get_current_settings()
    video_handler = VideoHandler(force_frame_size=None)
    t = video_handler.run_video_on_new_thread("../Videos/3.mp4")
    t.join()

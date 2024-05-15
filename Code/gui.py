from tkinter import *
from tkinter import ttk
from video_handler import VideoHandler
from tkinter.filedialog import askopenfilename
from user_settings import save_settings_to_json_file, read_settings_from_json_file, get_current_settings

# TODO
# 1. lunching chosen video
# 2. settings editing
# 3. saving settings


class Gui:
    def __init__(self):
        self.root = Tk()
        self.file_name_label = StringVar(value="Chosen video: None")
        self.file_name = None
        self.video_handler = VideoHandler(force_frame_size=None)

        self.__setup_grid()

    def __setup_grid(self):
        frm = ttk.Frame(self.root, padding=10, height=300, width=300)
        frm.grid()
        ttk.Label(frm, textvariable=self.file_name_label).grid(column=0, row=0)
        ttk.Button(frm, text="Choose video to play", command=self.__show_open_file_dialog).grid(column=0, row=1)
        ttk.Button(frm, text="Play video", command=self.__play_video).grid(column=0, row=2)
        ttk.Button(frm, text="Stop video", command=self.video_handler.stop_video).grid(column=1, row=2)
        ttk.Button(frm, text="Save settings to file", command=self.__save_settings_to_file).grid(column=0, row=3)
        ttk.Button(frm, text="Read settings from file", command=self.__read_settings_from_file).grid(column=1, row=3)
        ttk.Button(frm, text="Quit", command=self.root.destroy).grid(column=1, row=4)

    def __read_settings_from_file(self):
        read_settings_from_json_file('app_settings.json')

    def __save_settings_to_file(self):
        s = get_current_settings()
        save_settings_to_json_file(s, 'app_settings.json')


    def __play_video(self):
        self.video_handler.play_video_on_new_thread(self.file_name)

    def __show_open_file_dialog(self):
        name = askopenfilename(filetypes=[("MP4", '.mp4')])
        self.file_name_label.set("Chosen video: " + name)
        self.file_name = name

    def run_gui(self):
        self.root.mainloop()

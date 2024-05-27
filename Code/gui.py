from tkinter import *
from tkinter import ttk
from video_handler import VideoHandler
from tkinter.filedialog import askopenfilename
from user_settings import save_settings_to_json_file, read_settings_from_json_file, get_current_settings
from time import sleep


# TODO
# 1. lunching chosen video
# 2. settings editing
# 3. saving settings


class Gui:
    def __init__(self):
        self.root = Tk()
        self.root.title("Camera app")
        self.root.resizable(False, False)
        self.file_name_label = StringVar(value="Chosen video: None")
        self.file_name = None
        self.video_handler = VideoHandler(force_frame_size=None, root=self.root)

        self.root.eval('tk::PlaceWindow . center')

        self.settings_window = None
        self.playback_window = None

        self.root.bind("<Configure>", self.move_settings_window)
        # self.root.bind("<Configure>", self.move_playback_control_window)

        self.__setup_grid()

    def __setup_grid(self):
        frm = ttk.Frame(self.root, padding=10, height=300, width=300)
        frm.grid()
        ttk.Label(frm, textvariable=self.file_name_label).grid(column=0, row=0, columnspan=2)
        ttk.Button(frm, text="Choose video to play", command=self.__show_open_file_dialog).grid(column=0, row=1,
                                                                                                columnspan=2,
                                                                                                sticky='nesw')
        self.play_button = ttk.Button(frm, text="Play video", command=self.__play_video)
        self.play_button.state(['disabled'])
        self.play_button.grid(column=0, row=2, sticky='nesw')
        self.stop_button = ttk.Button(frm, text="Stop video", command=self.__stop_video)
        self.stop_button.state(['disabled'])
        self.stop_button.grid(column=1, row=2, sticky='nesw')
        ttk.Button(frm, text="Save settings to file", command=self.__save_settings_to_file).grid(column=0, row=3,
                                                                                                 sticky='nesw')
        ttk.Button(frm, text="Read settings from file", command=self.__read_settings_from_file).grid(column=1, row=3,
                                                                                                     sticky='nesw')
        ttk.Button(frm, text="Settings", command=self.__open_settings_window).grid(column=0, row=4, columnspan=2,
                                                                                   sticky='nesw')
        ttk.Button(frm, text="Quit", command=self.__quit).grid(column=0, row=5, columnspan=2, sticky='nesw')

    def __open_settings_window(self):
        if self.settings_window is not None:
            self.settings_window.destroy()
            self.settings_window = None
            return
        self.settings_window = Toplevel(self.root)
        self.settings_window.title("Settings")
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        width = self.root.winfo_width()
        self.settings_window.geometry(f"300x300+{x + width}+{y}")
        self.settings_window.resizable(False, False)
        self.settings_window.overrideredirect(True)
        label = Label(self.settings_window, text="Settings")
        label.pack()

    def move_settings_window(self, event):
        try:
            if self.settings_window is not None:
                x = self.root.winfo_x()
                y = self.root.winfo_y()
                width = self.root.winfo_width()
                self.settings_window.geometry(f"+{x + width}+{y}")
        except NameError:
            pass

    # def __open_playback_control_window(self):
    #     if self.playback_window is not None:
    #         self.playback_window.destroy()
    #         self.playback_window = None
    #         return
    #     self.playback_window = Toplevel(self.root)
    #     self.playback_window.title("Playback control")
    #     x = self.root.winfo_x()
    #     y = self.root.winfo_y()
    #     height = self.root.winfo_height()
    #     self.playback_window.geometry(f"300x300+{x}+{y+height+30}")
    #     self.playback_window.resizable(False, False)
    #     self.playback_window.overrideredirect(True)
    #     label = Label(self.playback_window, text="Playback control")
    #     label.pack()

    # def move_playback_control_window(self, event):
    #     try:
    #         if self.playback_window is not None:
    #             x = self.root.winfo_x()
    #             y = self.root.winfo_y()
    #             height = self.root.winfo_height()
    #             self.playback_window.geometry(f"+{x}+{y+height+30}")
    #     except NameError:
    #         pass

    def __read_settings_from_file(self):
        read_settings_from_json_file('app_settings.json')

    def __save_settings_to_file(self):
        s = get_current_settings()
        save_settings_to_json_file(s, 'app_settings.json')

    def __play_video(self):
        self.video_handler.play_video_on_new_thread(self.file_name)
        # self.__open_playback_control_window()
        self.play_button.state(['disabled'])
        self.stop_button.state(['!disabled'])

    def __stop_video(self):
        self.video_handler.stop_video()
        # self.__open_playback_control_window()
        self.play_button.state(['!disabled'])
        self.stop_button.state(['disabled'])

    def __quit(self):
        self.video_handler.stop_video()
        sleep(0.5)
        self.root.destroy()

    def __show_open_file_dialog(self):
        name = askopenfilename(filetypes=[("MP4", '.mp4')])
        if name == "" or name is None:
            return
        display_name = name.split("/")[-1]
        self.file_name_label.set("Chosen video: " + display_name)
        self.file_name = name
        self.play_button.state(['!disabled'])

    def run_gui(self):
        self.root.mainloop()

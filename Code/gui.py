import os.path
from tkinter import *
from tkinter import ttk, messagebox, colorchooser
from video_handler import VideoHandler
from tkinter.filedialog import askopenfilename
from user_settings import save_settings_to_json_file, read_settings_from_json_file, get_current_settings
from time import sleep


# TODO
# 1. launching chosen video
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

        # self.root.geometry("300x300")
        self.settings_window = None
        self.playback_window = None

        self.root.bind("<Configure>", self.move_settings_window)

        if os.path.isfile('app_settings.json'):
            if os.stat('app_settings.json').st_size == 0:
                save_settings_to_json_file(get_current_settings(), 'app_settings.json')
            else:
                read_settings_from_json_file('app_settings.json')
        else:
            save_settings_to_json_file(get_current_settings(), 'app_settings.json')

        self.linesOn = IntVar(value=0)
        if get_current_settings().lines_is_on:
            self.linesOn.set(1)

        self.car_thickness = IntVar(value=get_current_settings().detection_thickness_cars)

        self.line_min_thickness = IntVar(value=get_current_settings().lines_min_thickness)
        self.line_max_thickness = IntVar(value=get_current_settings().lines_max_thickness)

        self.line_angle = IntVar(value=get_current_settings().lines_angle)
        self.line_length = IntVar(value=get_current_settings().lines_length)
        self.line_pivot_distance = IntVar(value=int(get_current_settings().lines_pivot_distance_from_edge * 100))


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

        ttk.Button(frm, text="Settings", command=self.__open_settings_window).grid(column=0, row=4, columnspan=2,
                                                                                   sticky='nesw')
        ttk.Button(frm, text="Quit", command=self.__quit).grid(column=0, row=5, columnspan=2, sticky='nesw')

    def __open_settings_window(self):
        if self.settings_window is not None:
            self.settings_window.destroy()
            self.settings_window = None
            return
        settings_win = self.settings_window = Toplevel(self.root)
        settings_win.title("Settings")
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        width = self.root.winfo_width()
        settings_win.geometry(f"+{x + width}+{y}")
        settings_win.resizable(False, False)
        settings_win.overrideredirect(True)

        settings_frm = ttk.Frame(settings_win, padding=10, height=300, width=300)
        settings_frm.grid()

        label = Label(settings_frm, text="Settings")
        label.grid(column=0, row=0, columnspan=2, sticky='nesw')

        settings = get_current_settings()

        (ttk.Button(settings_frm, text="Set car detection color",
                    command=lambda: self.__set_color("Car detection color", settings.detection_color_cars))
         .grid(column=0, row=1, columnspan=2, sticky='nesw'))
        (ttk.Button(settings_frm, text="Set people detection color",
                    command=lambda: self.__set_color("People detection color", settings.detection_color_people))
         .grid(column=0, row=2, columnspan=2, sticky='nesw'))
        (ttk.Button(settings_frm, text="Set warning sign detection color",
                    command=lambda: self.__set_color("Warning sign detection color",
                                                     settings.detection_color_warning_signs))
         .grid(column=0, row=3, columnspan=2, sticky='nesw'))
        (ttk.Button(settings_frm, text="Set stop sign detection color",
                    command=lambda: self.__set_color("Stop sign detection color",
                                                     settings.detection_color_stop_signs))
         .grid(column=0, row=4, columnspan=2, sticky='nesw'))

        self.car_thickness_label = Label(settings_frm, text=f"Car Detection thickness: {settings.detection_thickness_cars}")
        self.car_thickness_label.grid(column=0, row=5, columnspan=2, sticky='nesw')

        (ttk.Scale(settings_frm, from_=1, to=6, orient=HORIZONTAL, variable=self.car_thickness,
                   command=lambda value: self.__update_thickness("cars", value))
        .grid(
            column=0, row=6, columnspan=2, sticky='nesw'))

        ttk.Checkbutton(settings_frm, text="Draw parking lines", variable=self.linesOn, command=self.__draw_parking_lines).grid(column=0, row=7, sticky='nesw')

        ttk.Button(settings_frm, text="Set line color", command=lambda: self.__set_color("Line color", settings.lines_color)).grid(column=1, row=7, sticky='nesw')

        self.line_min_thickness_label = Label(settings_frm, text=f"Line minimum thickness: {settings.lines_min_thickness}")
        self.line_min_thickness_label.grid(column=0, row=8, columnspan=2, sticky='nesw')

        (ttk.Scale(settings_frm, from_=5, to=30, orient=HORIZONTAL, variable=self.line_min_thickness,
                   command=lambda value: self.__update_thickness("line_min", value))
        .grid(
            column=0, row=9, columnspan=2, sticky='nesw'))

        self.line_max_thickness_label = Label(settings_frm, text=f"Line minimum thickness: {settings.lines_max_thickness}")
        self.line_max_thickness_label.grid(column=0, row=10, columnspan=2, sticky='nesw')

        (ttk.Scale(settings_frm, from_=30, to=70, orient=HORIZONTAL, variable=self.line_max_thickness,
                   command=lambda value: self.__update_thickness("line_max", value))
        .grid(
            column=0, row=11, columnspan=2, sticky='nesw'))

        self.line_angle_label = Label(settings_frm, text=f"Line angle: {settings.lines_angle}")
        self.line_angle_label.grid(column=0, row=12, columnspan=2, sticky='nesw')

        (ttk.Scale(settings_frm, from_=1, to=80, orient=HORIZONTAL, variable=self.line_angle,
                   command=lambda value: self.__set_line("angle", value))
        .grid(
            column=0, row=13, columnspan=2, sticky='nesw'))

        self.line_length_label = Label(settings_frm, text=f"Line length: {settings.lines_length}")
        self.line_length_label.grid(column=0, row=14, columnspan=2, sticky='nesw')

        (ttk.Scale(settings_frm, from_=400, to=900, orient=HORIZONTAL, variable=self.line_length,
                   command=lambda value: self.__set_line("length", value))
        .grid(
            column=0, row=15, columnspan=2, sticky='nesw'))

        self.line_pivot_label = Label(settings_frm, text=f"Line pivot distance: {int(settings.lines_pivot_distance_from_edge * 100)}")
        self.line_pivot_label.grid(column=0, row=16, columnspan=2, sticky='nesw')

        (ttk.Scale(settings_frm, from_=0, to=50, orient=HORIZONTAL, variable=self.line_pivot_distance,
                   command=lambda value: self.__set_line("pivot_distance", value))
        .grid(
            column=0, row=17, columnspan=2, sticky='nesw'))

        self.car_combo = ttk.Combobox(settings_frm, values=["none", "box", "sound"], state="readonly")
        self.car_combo.grid(column=0, row=18, columnspan=2, sticky='nesw')
        self.car_combo.bind("<<ComboboxSelected>>", lambda event: self.__set_combo(event, "cars", self.car_combo.get()))


        (ttk.Button(settings_frm, text="Save settings to file", command=self.__save_settings_to_file)
         .grid(column=0, row=20, columnspan=1, sticky='nesw'))
        (ttk.Button(settings_frm, text="Read settings from file", command=self.__read_settings_from_file)
         .grid(column=1, row=20, columnspan=1, sticky='nesw'))

    def move_settings_window(self, event):
        try:
            if self.settings_window is not None:
                x = self.root.winfo_x()
                y = self.root.winfo_y()
                width = self.root.winfo_width()
                self.settings_window.geometry(f"+{x + width}+{y}")
        except NameError:
            pass

    def __set_color(self, window_title, color_variable: list[int, int, int]):
        color = colorchooser.askcolor(title=window_title)
        # print(color)
        color_variable[:] = (color[0][0], color[0][1], color[0][2])

    def __update_thickness(self, of: str, value: int):
        settings = get_current_settings()
        int_value = int(float(value))
        if of == "cars":
            settings.detection_thickness_cars = int_value
            self.car_thickness_label.config(text=f"Car Detection thickness: {int_value}")
            self.car_thickness.set(int_value)
        elif of == "people":
            settings.detection_thickness_people = int_value
        elif of == "warning_signs":
            settings.detection_thickness_warning_signs = int_value
        elif of == "stop_signs":
            settings.detection_thickness_stop_signs = int_value
        elif of == "line_min":
            settings.lines_min_thickness = int_value
            self.line_min_thickness_label.config(text=f"Line minimum thickness: {int_value}")
            self.line_min_thickness.set(int_value)
        elif of == "line_max":
            settings.lines_max_thickness = int_value
            self.line_max_thickness_label.config(text=f"Line maximum thickness: {int_value}")
            self.line_max_thickness.set(int_value)


    def __draw_parking_lines(self):
        settings = get_current_settings()

        if self.linesOn.get() == 1:
            settings.lines_is_on = True
        else:
            settings.lines_is_on = False

    def __set_line(self, what: str, value: int):
        settings = get_current_settings()
        value = int(float(value))
        if what == "angle":
            settings.lines_angle = value
            self.line_angle_label.config(text=f"Line angle: {value}")
            self.line_angle.set(value)
        elif what == "length":
            settings.lines_length = value
            self.line_length_label.config(text=f"Line length: {value}")
            self.line_length.set(value)
        elif what == "pivot_distance":
            self.line_pivot_distance.set(value)
            self.line_pivot_label.config(text=f"Line pivot distance: {value}")
            value = value / 100
            settings.lines_pivot_distance_from_edge = value


    def __set_combo(self, event, type: str, value: str):
        settings = get_current_settings()
        if type == "cars":
            print(value)
            settings.cars_alert_type = value

    def __read_settings_from_file(self):
        if read_settings_from_json_file('app_settings.json'):
            messagebox.showinfo("Success", "Settings loaded successfully")
        else:
            messagebox.showerror("Error", "Settings could not be loaded")

    def __save_settings_to_file(self):
        s = get_current_settings()
        if save_settings_to_json_file(s, 'app_settings.json'):
            messagebox.showinfo("Success", "Settings saved successfully")
        else:
            messagebox.showerror("Error", "Settings could not be saved")


    def __play_video(self):
        if self.video_handler.video_playing:
            return

        self.video_handler.play_video_on_new_thread(self.file_name)

    def __stop_video(self):
        if not self.video_handler.video_playing:
            return

        self.video_handler.stop_video()

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
        self.stop_button.state(['!disabled'])

    def run_gui(self):
        self.root.mainloop()

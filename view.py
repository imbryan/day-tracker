import tkinter as tk
from tkinter import ttk  # More native looking widgets
from tkinter.messagebox import showinfo
import datetime


class View(tk.Tk):

    PAD = 10
    BUTTON_WIDTH = 15

    def __init__(self, controller):
        super().__init__()  # Call Tk constructor
        self.controller = controller

        self.title("Day Tracker")

        self.date = datetime.datetime.now()
        self.current_day = tk.StringVar()
        self.current_day.set(f'{self.date.month} / {self.date.day} / {self.date.year}')

        # make this better
        self.cat_var = tk.StringVar()
        self.val_var = tk.StringVar()

        self._make_main_frame()
        self._make_buttons()
        self._make_entries()
        self._make_extras()

    def main(self):
        self.mainloop()

    def _make_main_frame(self):
        self.main_frame = ttk.Frame(self)
        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(padx=self.PAD, pady=self.PAD)  # Put padding around main frame

    def _make_buttons(self):
        frame = ttk.Frame(self.main_frame)

        left_frame = ttk.Frame(frame)
        middle_frame = ttk.Frame(frame)
        right_frame = ttk.Frame(frame)

        caption_prev = "Previous Day"
        prev_day_button = ttk.Button(left_frame, text=caption_prev, width=self.BUTTON_WIDTH, command=
        (lambda button=caption_prev: self.controller.on_nav_button_click(caption_prev))
                                     )
        prev_day_button.pack(expand=True)

        caption_prev_month = "Previous Month"
        prev_month_button = ttk.Button(left_frame, text=caption_prev_month, width=self.BUTTON_WIDTH,command=
        (lambda button=caption_prev_month: self.controller.on_nav_button_click(caption_prev_month))
                                     )
        prev_month_button.pack(expand=True)

        caption_prev_year = "Previous Year"
        prev_year_button = ttk.Button(left_frame, text=caption_prev_year, width=self.BUTTON_WIDTH, command=
        (lambda button=caption_prev_year: self.controller.on_nav_button_click(caption_prev_year))
                                     )
        prev_year_button.pack(expand=True)

        current_day_label = ttk.Label(middle_frame, font=(None, 15), textvariable=self.current_day)
        current_day_label.pack(expand=True, padx=(self.PAD, self.PAD))

        caption_next = "Next Day"
        next_day_button = ttk.Button(right_frame, text=caption_next, width=self.BUTTON_WIDTH,command=
        (lambda button=caption_next: self.controller.on_nav_button_click(caption_next))
                             )
        next_day_button.pack(expand=True)

        caption_next_month = "Next Month"
        next_month_button = ttk.Button(right_frame, text=caption_next_month, width=self.BUTTON_WIDTH,command=
        (lambda button=caption_next_month: self.controller.on_nav_button_click(caption_next_month))
                                     )
        next_month_button.pack(expand=True)

        caption_next_year = "Next Year"
        next_year_button = ttk.Button(right_frame, text=caption_next_year, width=self.BUTTON_WIDTH,command=
        (lambda button=caption_next_year: self.controller.on_nav_button_click(caption_next_year))
                                     )
        next_year_button.pack(expand=True)

        caption_today = "Today"
        today_button = ttk.Button(middle_frame, text=caption_today, command =
        (lambda button=caption_today: self.controller.on_nav_button_click(caption_today))
                                  )
        today_button.pack(side="bottom",expand=True)

        left_frame.pack(side="left")
        middle_frame.pack(side="left")
        right_frame.pack(side="left")
        frame.pack(side="top")

    def _make_entries(self):
        frame = ttk.Frame(self.main_frame)
        top_frame = ttk.Frame(frame)
        bottom_frame = ttk.Frame(frame)

        cat_label = ttk.Label(top_frame, text="Lookup category", width=17, justify="center")
        cat_label.pack(side="left",expand=True, padx=(self.PAD, self.PAD))

        cat_entry = ttk.Entry(top_frame, textvariable=self.cat_var)
        cat_entry.pack(side="left",expand=True, padx=(self.PAD, self.PAD))

        caption_lookup = "Lookup"
        lookup_button = ttk.Button(top_frame, text=caption_lookup, command =
        (lambda button=caption_lookup: self.controller.entry_button_click(caption_lookup))
                                   )
        lookup_button.pack(side="left",expand=True)

        val_label = ttk.Label(bottom_frame, text="View/change value", width=17, justify="center")
        val_label.pack(side="left", expand=True, padx=(self.PAD, self.PAD))

        val_entry = ttk.Entry(bottom_frame, textvariable=self.val_var)
        val_entry.pack(side="left", padx=(self.PAD, self.PAD))

        caption_update = "Update"
        update_button = ttk.Button(bottom_frame, text=caption_update, command=
        (lambda button=caption_update: self.controller.entry_button_click(caption_update))
                                   )
        update_button.pack(side="left", expand=True)

        top_frame.pack(side="top")
        bottom_frame.pack(side="bottom")
        frame.pack(side="top", pady=(self.PAD,self.PAD))

    def _make_extras(self):
        frame = ttk.Frame(self.main_frame)

        caption_help = "Help"
        help_button = ttk.Button(frame, text=caption_help, command=
        (lambda button=caption_help: self.controller.message_button_click(caption_help)))
        help_button.pack(side="left", expand=True)

        frame.pack(side="top")

    @staticmethod
    def popup_window(title, message):
        showinfo(title, message)



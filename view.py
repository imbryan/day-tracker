import tkinter as tk
from tkinter import ttk  # More native looking widgets
from tkinter.messagebox import showinfo
import datetime


class View(tk.Tk):

    PAD = 10
    BUTTON_WIDTH = 15

    def __init__(self, controller, db):
        super().__init__()  # Call Tk constructor
        self.controller = controller
        self.db = db

        self.title("Day Tracker")

        self.date = datetime.datetime.now()
        self.current_day = tk.StringVar()
        self.current_day.set(f'{self.date.month} / {self.date.day} / {self.date.year}')

        self.remind_var = tk.IntVar()

        # make this better
        self.cat_var = tk.StringVar()
        self.val_var = tk.StringVar()

        self.reminders = self.controller.check_reminders()

        self._make_main_frame()
        self._make_buttons()
        self._make_entries()
        self._make_extras()

        self.remind(self.reminders)

    def main(self):
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()

        right = int(self.winfo_screenwidth()/2 - width/2)
        down = int(self.winfo_screenheight()/2 - height/2)

        self.geometry(f'+{right}+{down}')

        self.mainloop()

    def remind(self, list):
        new_list = []
        for item in list:
            if self.db.read_database(self.db.conn, "data", "Entries",
                                     f"WHERE category_name = \"{item}\" and year = {self.date.year} and month = {self.date.month} and day = {self.date.day}",
                                     "int", "one") is None:
                new_list.append(item)

        try:
            if new_list:

                top = tk.Toplevel(self)
                top.wm_geometry("250x175")
                top.title("Reminder")

                msg = "You need to fill in today's values for:\n\n"

                for item in new_list:
                    msg+=(item+"\n")

                message = tk.Message(top, text=msg, pady=(self.PAD))
                message.pack(expand=True)

                button = tk.Button(top, text="Dismiss", pady=(self.PAD), command=lambda: self.destroy_top(top))
                button.pack(expand=True)

                self.cat_var.set(new_list[0])

                top.lift(self)
        except: pass

    def destroy_top(self, top):
        top.destroy()
        self.lift()

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
        bottom_frame.pack(side="top")
        frame.pack(side="top", pady=(self.PAD,self.PAD))

    def _make_extras(self):
        frame = ttk.Frame(self.main_frame)

        top_frame = ttk.Frame(frame)
        bottom_frame = ttk.Frame(frame)

        caption_remind = "Toggle reminder\nfor category"
        reminder_button = ttk.Checkbutton(top_frame, text=caption_remind, variable=self.remind_var, onvalue=1, offvalue=0, command=
        (lambda checkbutton=caption_remind: self.controller.message_button_click(caption_remind))
                          )
        reminder_button.pack(side="left", expand=True, padx=self.PAD/2)

        caption_sum_month = "Sum values (month)"
        sum_month_button = ttk.Button(top_frame, text=caption_sum_month, command=
        (lambda button=caption_sum_month: self.controller.message_button_click(caption_sum_month)))
        sum_month_button.pack(side="left", expand=True, padx=self.PAD/2)

        caption_sum_year = "Sum values (year)"
        sum_year_button = ttk.Button(top_frame, text=caption_sum_year, command=
        (lambda button=caption_sum_year: self.controller.message_button_click(caption_sum_year)))
        sum_year_button.pack(side="left", expand=True)

        caption_help = "Help"
        help_button = ttk.Button(bottom_frame, text=caption_help, command=
        (lambda button=caption_help: self.controller.message_button_click(caption_help)))
        help_button.pack(side="left", expand=True, padx=self.PAD, pady=(self.PAD,))

        caption_exit = "Exit"
        exit_button = ttk.Button(bottom_frame, text=caption_exit, command=self.destroy)
        exit_button.pack(side="left", expand=True, pady=(self.PAD,))

        top_frame.pack(side="top")
        bottom_frame.pack(side="top")
        frame.pack(side="top")

    @staticmethod
    def popup_window(title, message):
        showinfo(title, message)

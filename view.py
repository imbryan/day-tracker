import tkinter as tk
from tkinter import ttk  # More native looking widgets
from tkinter.messagebox import showinfo, askyesno
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

        # Data manipulation variables
        self.cat_var = tk.StringVar()
        self.val_var = tk.StringVar()
        self.des_var = tk.StringVar()

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

    # Method to trigger reminder for incomplete entries
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

                msg = "You need to fill in this day's values for:\n\n"

                for item in new_list:
                    msg+=(item+"\n")

                message = tk.Message(top, text=msg, pady=(self.PAD))
                message.pack(expand=True)

                button = tk.Button(top, text="Dismiss", pady=(self.PAD), command=lambda: self.destroy_top(top))
                button.pack(expand=True)

                self.cat_var.set(new_list[0])
                self.des_var.set(self.controller.get_description(new_list[0]))
                self.remind_var.set(1)

                top.lift(self)
        except: pass

    def destroy_top(self, top):
        top.destroy()
        self.lift()

    def _make_main_frame(self):
        self.main_frame = ttk.Frame(self)
        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(padx=self.PAD, pady=self.PAD)  # Put padding around main frame

    # Buttons for navigating dates
    def _make_buttons(self):
        frame = ttk.Frame(self.main_frame)

        left_frame = ttk.Frame(frame)
        middle_frame = ttk.Frame(frame)
        right_frame = ttk.Frame(frame)

        # Left frame widgets
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

        # Middle frame widgets
        current_day_label = ttk.Label(middle_frame, font=(None, 15), textvariable=self.current_day)
        current_day_label.pack(expand=True, side="top", padx=(self.PAD, self.PAD))

        caption_today = "Today"
        today_button = ttk.Button(middle_frame, text=caption_today, command=
        (lambda button=caption_today: self.controller.on_nav_button_click(caption_today))
                                  )
        today_button.pack(side="top", expand=True)

        # Reset button
        caption_reset = "Reset form"
        reset_button = ttk.Button(middle_frame, text=caption_reset, command=
        (lambda button=caption_reset: self.controller.on_nav_button_click(caption_reset))
                                  )
        reset_button.pack(side="top", expand=True)

        # Right frame widgets
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

        left_frame.pack(side="left")
        middle_frame.pack(side="left")
        right_frame.pack(side="left")
        frame.pack(side="top")

    # Buttons for data manipulation
    def _make_entries(self):
        frame = ttk.Frame(self.main_frame)
        top_frame = ttk.Frame(frame)
        bottom_frame = ttk.Frame(frame)
        des_frame = ttk.Frame(frame)

        # Description frame widgets
        des_label = ttk.Label(des_frame, text="Category description", width=20, justify="center")
        des_label.pack(side="left", expand=True, padx=(0, self.PAD/5))

        des_entry = ttk.Entry(des_frame, textvariable=self.des_var)
        des_entry.pack(side="left", padx=(self.PAD, self.PAD))

        caption_des = "Set"
        des_button = ttk.Button(des_frame, text=caption_des, command =
        (lambda button=caption_des: self.controller.entry_button_click(caption_des))
                                )
        des_button.pack(side="left",expand=True)

        # Top frame widgets
        cat_label = ttk.Label(top_frame, text="Lookup category", width=17, justify="center")
        cat_label.pack(side="left",expand=True, padx=(self.PAD, self.PAD))

        cat_entry = ttk.Entry(top_frame, textvariable=self.cat_var)
        cat_entry.pack(side="left",expand=True, padx=(self.PAD, self.PAD))

        caption_lookup = "Lookup"
        lookup_button = ttk.Button(top_frame, text=caption_lookup, command =
        (lambda button=caption_lookup: self.controller.entry_button_click(caption_lookup))
                                   )
        lookup_button.pack(side="left",expand=True)

        # Bottom frame widgets
        val_label = ttk.Label(bottom_frame, text="View/change value", width=17, justify="center")
        val_label.pack(side="left", expand=True, padx=(self.PAD, self.PAD))

        val_entry = ttk.Entry(bottom_frame, textvariable=self.val_var)
        val_entry.pack(side="left", padx=(self.PAD, self.PAD))

        caption_update = "Update"
        update_button = ttk.Button(bottom_frame, text=caption_update, command=
        (lambda button=caption_update: self.controller.entry_button_click(caption_update))
                                   )
        update_button.pack(side="left", expand=True)

        des_frame.pack(side="top", pady=(0,self.PAD/2))
        top_frame.pack(side="top", pady=(0,self.PAD/4))
        bottom_frame.pack(side="top")
        frame.pack(side="top", pady=(self.PAD,self.PAD))

    # Extras buttons
    def _make_extras(self):
        frame = ttk.Frame(self.main_frame)

        top_top_frame = ttk.Frame(frame)
        top_frame = ttk.Frame(frame)
        middle_frame = ttk.Frame(frame)
        bottom_frame = ttk.Frame(frame)

        # Top top frame widgets
        caption_entries = "Entries for this day"
        entries_button = ttk.Button(top_top_frame, text=caption_entries, command=
        (lambda button=caption_entries: self.controller.message_button_click(caption_entries))
                                    )
        entries_button.pack(side="left", expand=True, padx=(0,self.PAD/2))

        caption_check_remind = "Check reminders"
        check_remind_button = ttk.Button(top_top_frame, text=caption_check_remind, command=
        (lambda button=caption_check_remind: self.remind(self.controller.check_reminders()))
                                         )
        check_remind_button.pack(side="left", expand=True)

        # Top frame widgets
        caption_categories = "List of categories"
        categories_button = ttk.Button(top_frame, text=caption_categories, command=
        (lambda button=caption_categories: self.controller.message_button_click(caption_categories))
                                       )
        categories_button.pack(side="left", expand=True, padx=(0,self.PAD/2))

        caption_delete = "Delete category"
        delete_button = ttk.Button(top_frame, text=caption_delete, command=
        (lambda button=caption_delete: self.delete_cat())
                                   )
        delete_button.pack(side="left", expand=True)

        # Middle frame widgets
        caption_sum_month = "Sum (month)"
        sum_month_button = ttk.Button(middle_frame, text=caption_sum_month, command=
        (lambda button=caption_sum_month: self.controller.message_button_click(caption_sum_month)))
        sum_month_button.pack(side="left", expand=True, padx=(0,self.PAD/2))

        caption_sum_year = "Sum (year)"
        sum_year_button = ttk.Button(middle_frame, text=caption_sum_year, command=
        (lambda button=caption_sum_year: self.controller.message_button_click(caption_sum_year)))
        sum_year_button.pack(side="left", expand=True)

        caption_average_month = "Average (month)"
        average_month_button = ttk.Button(middle_frame, text=caption_average_month, command=
        (lambda button=caption_average_month: self.controller.message_button_click(caption_average_month)))
        average_month_button.pack(side="left", expand=True)

        caption_average_year = "Average (year)"
        average_year_button = ttk.Button(middle_frame, text=caption_average_year, command=
        (lambda button=caption_average_year: self.controller.message_button_click(caption_average_year)))
        average_year_button.pack(side="left", expand=True)

        # Bottom frame widgets
        caption_help = "Help"
        help_button = ttk.Button(bottom_frame, text=caption_help, command=
        (lambda button=caption_help: self.controller.message_button_click(caption_help)))
        help_button.pack(side="left", expand=True, padx=(0,self.PAD/2))

        caption_exit = "Exit"
        exit_button = ttk.Button(bottom_frame, text=caption_exit, command=self.destroy)
        exit_button.pack(side="left", expand=True)

        caption_remind = "Toggle reminder for category"
        reminder_button = ttk.Checkbutton(frame, text=caption_remind, variable=self.remind_var, onvalue=1,
                                          offvalue=0, command=
                                          (lambda checkbutton=caption_remind: self.controller.message_button_click(
                                              caption_remind))
                                          )
        reminder_button.pack(side="top", expand=True, pady=(0,self.PAD/2))

        top_top_frame.pack(side="top", pady=(0,self.PAD/2))
        top_frame.pack(side="top", pady=(0,self.PAD/2))
        middle_frame.pack(side="top", pady=(0,self.PAD/2))
        bottom_frame.pack(side="top", pady=(0,self.PAD/2))
        frame.pack(side="top")

    @staticmethod
    def popup_window(title, message):
        showinfo(title, message)

    def delete_cat(self):
        cat = self.cat_var.get().lower()
        response = None
        if cat is not "":
            response = askyesno("WARNING",
                 f"Are you sure you want to delete \"{cat}\"?\nALL of its entries will be permanently deleted.")
        if response:
            self.db.write_database(self.db.conn, "delete", "Entries", "category_name",
                                   f"\"{cat}\"")
            self.db.write_database(self.db.conn, "delete", "Categories", "name",
                                   f"\"{cat}\"")
            self.db.write_database(self.db.conn, "delete", "Reminders", "category_name",
                                   f"\"{cat}\"")
            self.db.conn.commit()

            self.cat_var.set("")
            self.val_var.set("")
            self.remind_var.set(0)
            self.des_var.set("")

import tkinter as tk
from tkinter import ttk, OptionMenu  # More native looking widgets
from tkinter.messagebox import showinfo, askyesno
from tkinter.simpledialog import askstring
import datetime
import model
from sqlalchemy import or_


class View(tk.Tk):

    PAD = 10
    BUTTON_WIDTH = 15

    def __init__(self, controller, db):
        super().__init__()  # Call Tk constructor
        self.controller = controller
        # self.db = db  # ! Deprecated
        self.session = db  # NOTE "db" -> SQLAlchemy session object

        self.title("Day Tracker")

        self.date = datetime.datetime.now()
        self.current_day = tk.StringVar()
        self.current_day.set(f'{self.date.month} / {self.date.day} / {self.date.year}')

        self.remind_var = tk.IntVar()

        # Data manipulation variables
        self.cat_var = tk.StringVar()
        self.val_var = tk.StringVar()
        self.des_var = tk.StringVar()

        self.backup_var = tk.StringVar()

        self.reminders = self.controller.check_reminders()

        self._make_main_frame()
        self._make_buttons()
        self.entries_frame = None
        self.entries_frame = self._make_entries(self.date)
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
            # if self.db.read_database(self.db.conn, "data", "Entries",
            #                          f"WHERE category_name = \"{item}\" and year = {self.date.year} and month = {self.date.month} and day = {self.date.day}",
            #                          "int", "one") is None:  # ! Deprecated
            check_todays_entry = self.session.query(model.Entry)\
                .join(model.Category, or_(model.Category.id==model.Entry.category_id, model.Category.name == model.Entry.category_name))\
                    .filter(
                        or_(model.Category.name == item, model.Entry.category_name == item),
                        model.Entry.year==self.date.year, 
                        model.Entry.month==self.date.month, 
                        model.Entry.day==self.date.day,
                    ).first()
            if not check_todays_entry or check_todays_entry.data in (None, ''):
                new_list.append(item)

        try:
            if new_list:

                top = tk.Toplevel(self)
                # top.wm_geometry("250x175")
                top.title("Reminder")

                msg = "You need to fill in this day's values for:\n\n"

                for item in new_list:
                    msg+=(item+"\n")

                message = tk.Message(top, text=msg)
                message.pack(expand=True, pady=(self.PAD), padx=(self.PAD))

                button = tk.Button(top, text="Dismiss", command=lambda: self.destroy_top(top))
                button.pack(expand=True, pady=(self.PAD))

                self.cat_var.set(new_list[0])
                self.des_var.set(self.controller.get_description(new_list[0]))
                self.remind_var.set(1)

                top.lift(self)
        except: pass

    def backup(self):
        top = tk.Toplevel(self)
        top.title("Backup")

        backup_label = ttk.Label(top, text="Name this backup")
        backup_label.pack(expand=True, side="left", pady=(self.PAD*2.5))

        backup_entry = ttk.Entry(top, textvariable=self.backup_var)
        backup_entry.pack(expand=True, side="left")

        backup_button = ttk.Button(top, text="Backup", command=lambda: self.controller.backup(top))
        backup_button.pack(expand=True, side="left")

    def create_category(self):
        top = tk.Toplevel(self)
        self.new_cat_name_var = tk.StringVar()
        top.title="New Category"

        category_label = ttk.Label(top, text="Category Name")
        category_label.pack(expand=True, side="left", padx=(self.PAD,0), pady=(self.PAD*2.5))

        category_name = ttk.Entry(top, textvariable=self.new_cat_name_var)
        category_name.pack(expand=True, side="left")

        self.new_cat_type_var = tk.StringVar()
        options_list = ['Number', 'Text', 'Time']
        category_menu = OptionMenu(top, self.new_cat_type_var, *options_list)
        category_menu.pack(expand=True, side="left")

        category_create_button = ttk.Button(top, text="Submit", command=lambda: self.controller.create_category(top))
        category_create_button.pack(expand=True, side="left", padx=(self.PAD/2,self.PAD))

    def toggle_reminder(self):
        top = tk.Toplevel(self)
        self.toggle_reminder_var = tk.StringVar()
        top.title = "Reminder"

        reminder_label = ttk.Label(top, text="Category Name")
        reminder_label.pack(expand=True, side="left", padx=(self.PAD,0), pady=(self.PAD*2.5))

        reminder_entry = ttk.Entry(top, textvariable=self.toggle_reminder_var)
        reminder_entry.pack(expand=True, side="left")

        reminder_toggle_button = ttk.Button(top, text="Submit", command=lambda: self.controller.toggle_reminder(top))
        reminder_toggle_button.pack(expand=True, side="left", padx=(self.PAD/2, self.PAD))

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

        # TODO: Go-to-date button

        # Reset button  # ! Deprecated -- UI Refresh
        # caption_reset = "Reset form"
        # reset_button = ttk.Button(middle_frame, text=caption_reset, command=
        # (lambda button=caption_reset: self.controller.on_nav_button_click(caption_reset))
        #                           )
        # reset_button.pack(side="top", expand=True)

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
    def _make_entries(self, current_date):
        frame = self.entries_frame or ttk.Frame(self.main_frame)
        # Clear frame
        for widget in frame.winfo_children():
            widget.destroy()
        # Get enabled categories
        categories = self.session.query(model.Category).filter_by(enabled=True).all()
        for category in categories:
            category_frame = ttk.Frame(frame)
            category_frame.category_id = category.id
            category_frame.entry_text_var = tk.StringVar()
            temp_caption_var = "Disable"

            category_label_var = ttk.Label(category_frame, text=category.name, width=20, justify="center")
            category_label_var.pack(side="left", expand=True)
            category_frame.label_var = category_label_var

            category_entry_var = ttk.Entry(category_frame, textvariable=category_frame.entry_text_var)
            category_entry_var.pack(side="left", expand=True, padx=(0, self.PAD/5))
            category_frame.entry_var = category_entry_var

            # ! I Give Up, Gonna Try Something Else.
            # category_disable_button = ttk.Button(category_frame, text=temp_caption_var,command=
            # (lambda: self.controller.disable_cat(category_frame.category_id,category_frame)))
            # category_disable_button.pack(side="left", expand=True, padx=(self.PAD/5, 0))
            ####

            category_frame.pack(side="top", pady=(0,self.PAD/2))
            
        # ! Below is deprecated - UI Refresh
        # top_frame = ttk.Frame(frame)
        # bottom_frame = ttk.Frame(frame)
        # des_frame = ttk.Frame(frame)

        # # Description frame widgets
        # des_label = ttk.Label(des_frame, text="Category description", width=20, justify="center")
        # des_label.pack(side="left", expand=True, padx=(0, self.PAD/5))

        # des_entry = ttk.Entry(des_frame, textvariable=self.des_var)
        # des_entry.pack(side="left", padx=(self.PAD, self.PAD))

        # caption_des = "Set"
        # des_button = ttk.Button(des_frame, text=caption_des, command =
        # (lambda button=caption_des: self.controller.entry_button_click(caption_des))
        #                         )
        # des_button.pack(side="left",expand=True)

        # # Top frame widgets
        # cat_label = ttk.Label(top_frame, text="Lookup category", width=17, justify="center")
        # cat_label.pack(side="left",expand=True, padx=(self.PAD, self.PAD))

        # cat_entry = ttk.Entry(top_frame, textvariable=self.cat_var)
        # cat_entry.pack(side="left",expand=True, padx=(self.PAD, self.PAD))

        # caption_lookup = "Lookup"
        # lookup_button = ttk.Button(top_frame, text=caption_lookup, command =
        # (lambda button=caption_lookup: self.controller.entry_button_click(caption_lookup))
        #                            )
        # lookup_button.pack(side="left",expand=True)

        # # Bottom frame widgets
        # val_label = ttk.Label(bottom_frame, text="View/change value", width=17, justify="center")
        # val_label.pack(side="left", expand=True, padx=(self.PAD, self.PAD))

        # val_entry = ttk.Entry(bottom_frame, textvariable=self.val_var)
        # val_entry.pack(side="left", padx=(self.PAD, self.PAD))

        # caption_update = "Update"
        # update_button = ttk.Button(bottom_frame, text=caption_update, command=
        # (lambda button=caption_update: self.controller.entry_button_click(caption_update))
        #                            )
        # update_button.pack(side="left", expand=True)

        # des_frame.pack(side="top", pady=(0,self.PAD/2))
        # top_frame.pack(side="top", pady=(0,self.PAD/4))
        # bottom_frame.pack(side="top")
        ####################
        

        frame.pack(side="top", pady=(self.PAD,self.PAD))
        for widget in frame.winfo_children():
            if isinstance(widget, ttk.Frame) == False:
                continue
            entry_for_current_date = self.session.query(model.Entry).filter(
                model.Entry.year==current_date.year,
                model.Entry.month==current_date.month,
                model.Entry.day==current_date.day,
                model.Entry.category_id==widget.category_id
            ).first()
            if entry_for_current_date:
                widget.entry_text_var.set(entry_for_current_date.data)
        return frame

    # Extras buttons
    def _make_extras(self):
        frame = ttk.Frame(self.main_frame)

        top_top_frame = ttk.Frame(frame) # ! Changed in UI Refresh
        top_frame = ttk.Frame(frame)
        middle_frame = ttk.Frame(frame)
        bottom_frame = ttk.Frame(frame)

        # Top top frame widgets
        # ! Deprecated -- UI Refresh
        # caption_entries = "Entries for this day"
        # entries_button = ttk.Button(top_top_frame, text=caption_entries, command=
        # (lambda button=caption_entries: self.controller.message_button_click(caption_entries))
        #                             )
        # entries_button.pack(side="left", expand=True, padx=(0,self.PAD/2))

        caption_create_category = "Create Category"
        create_category_button = ttk.Button(top_top_frame, text=caption_create_category, command=
        (lambda button=caption_create_category: self.create_category()))
        create_category_button.pack(side="left", expand=True, padx=(0,self.PAD/2))

        ttk.Button(top_top_frame, text="Save All", command=(lambda button="Save All": self.controller.entry_button_click("Save All"))).pack(side="top", expand=True)

        # Top frame widgets
        caption_categories = "All Categories"
        categories_button = ttk.Button(top_frame, text=caption_categories, command=
        (lambda button=caption_categories: self.controller.message_button_click(caption_categories))
                                       )
        categories_button.pack(side="left", expand=True, padx=(0,self.PAD/2))

        caption_toggle_category = "Show/Hide Category"
        toggle_cat_button = ttk.Button(top_frame, text=caption_toggle_category, command=self.controller.toggle_cat)
        toggle_cat_button.pack(side="left", expand=True, padx=(0,self.PAD/2))

        caption_check_remind = "Reminders"
        check_remind_button = ttk.Button(top_frame, text=caption_check_remind, command=
        (lambda button=caption_check_remind: self.remind(self.controller.check_reminders()))
                                         )
        check_remind_button.pack(side="left", expand=True, padx=(0,self.PAD/2))

        caption_toggle_remind = "Toggle Reminder"
        toggle_remind_button = ttk.Button(top_frame, text=caption_toggle_remind, command=
        (lambda button=caption_toggle_remind: self.toggle_reminder()))
        toggle_remind_button.pack(side="left", expand=True)


        # caption_delete = "Delete category"  # ! Deprecated -- UI Refresh
        # delete_button = ttk.Button(top_frame, text=caption_delete, command=
        # (lambda button=caption_delete: self.delete_cat())
        #                            )
        # delete_button.pack(side="left", expand=True)

        # TODO - Function buttons are broken as of UI Refresh
        # Middle frame widgets
        # caption_sum_month = "Sum (month)"
        # sum_month_button = ttk.Button(middle_frame, text=caption_sum_month, command=
        # (lambda button=caption_sum_month: self.controller.message_button_click(caption_sum_month)))
        # sum_month_button.pack(side="left", expand=True, padx=(0,self.PAD/2))

        # caption_sum_year = "Sum (year)"
        # sum_year_button = ttk.Button(middle_frame, text=caption_sum_year, command=
        # (lambda button=caption_sum_year: self.controller.message_button_click(caption_sum_year)))
        # sum_year_button.pack(side="left", expand=True)

        # caption_average_month = "Average (month)"
        # average_month_button = ttk.Button(middle_frame, text=caption_average_month, command=
        # (lambda button=caption_average_month: self.controller.message_button_click(caption_average_month)))
        # average_month_button.pack(side="left", expand=True)

        # caption_average_year = "Average (year)"
        # average_year_button = ttk.Button(middle_frame, text=caption_average_year, command=
        # (lambda button=caption_average_year: self.controller.message_button_click(caption_average_year)))
        # average_year_button.pack(side="left", expand=True)
        ### end 



        # Bottom frame widgets
        caption_help = "Help"
        help_button = ttk.Button(bottom_frame, text=caption_help, command=
        (lambda button=caption_help: self.controller.message_button_click(caption_help)))
        help_button.pack(side="left", expand=True, padx=(0,self.PAD/2))

        caption_backup = "Create Backup"
        backup_button = ttk.Button(bottom_frame, text=caption_backup, command=
        (lambda button=caption_backup: self.backup()))
        backup_button.pack(side="left", expand=True, padx=(0,self.PAD/2))

        caption_exit = "Exit"
        exit_button = ttk.Button(bottom_frame, text=caption_exit, command=self.destroy)
        exit_button.pack(side="left", expand=True)

        # Reminder Toggle  # ! Deprecated -- UI Refresh
        # caption_remind = "Toggle reminder for category"
        # reminder_button = ttk.Checkbutton(frame, text=caption_remind, variable=self.remind_var, onvalue=1,
        #                                   offvalue=0, command=
        #                                   (lambda checkbutton=caption_remind: self.controller.message_button_click(
        #                                       caption_remind))
        #                                   )
        # reminder_button.pack(side="top", expand=True, pady=(0,self.PAD/2))

        top_top_frame.pack(side="top", pady=(0,self.PAD/2)) # ! Changed in UI Refresh
        top_frame.pack(side="top", pady=(0,self.PAD/2))
        middle_frame.pack(side="top", pady=(0,self.PAD/2))
        bottom_frame.pack(side="top", pady=(0,self.PAD/2))
        frame.pack(side="top")

    @staticmethod
    def popup_window(title, message):
        showinfo(title, message)

    @staticmethod
    def input_window(title, message):
        return askstring(title, message)

    def delete_cat(self):
        cat = self.cat_var.get().lower()
        response = None
        if cat != "":
            response = askyesno("WARNING",
                 f"Are you sure you want to delete \"{cat}\"?\nALL of its entries will be permanently deleted.")
        if response:
            # self.db.write_database(self.db.conn, "delete", "Entries", "category_name",
            #                        f"\"{cat}\"")
            # self.db.write_database(self.db.conn, "delete", "Categories", "name",
            #                        f"\"{cat}\"")
            # self.db.write_database(self.db.conn, "delete", "Reminders", "category_name",
            #                        f"\"{cat}\"")
            # self.db.conn.commit()  # ! Deprecated
            to_delete_cat = self.session.query(model.Category).filter_by(name=cat).first()
            self.session.query(model.Entry)\
                .filter(or_(model.Entry.category_id==to_delete_cat.id, model.Entry.category_name == to_delete_cat.name)).delete()
            self.session.query(model.Reminder)\
                .filter(or_(model.Reminder.category_id == to_delete_cat.id, model.Reminder.category_name == to_delete_cat.name)).delete()
            self.session.query(model.Category).filter_by(name=cat).delete()
            self.session.commit()

            self.cat_var.set("")
            self.val_var.set("")
            self.remind_var.set(0)
            self.des_var.set("")

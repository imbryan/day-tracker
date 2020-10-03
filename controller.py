from datetime import datetime, timedelta
from dateutil import relativedelta
from model import Category, Entry
from view import View
import tkinter as tk
from database import Database


class Controller:
    def __init__(self):
        self.db = Database()
        self.view = View(self, self.db)

    def main(self):
        self.view.main()

    # Buttons for navigating dates
    def on_nav_button_click(self, caption):
        if caption == "Previous Day":
            self.view.date -= timedelta(days=1)
        elif caption == "Previous Month":
            self.view.date -= relativedelta.relativedelta(months=1)
        elif caption == "Previous Year":
            self.view.date -= relativedelta.relativedelta(years=1)
        elif caption == "Next Day":
            self.view.date += timedelta(days=1)
        elif caption == "Next Month":
            self.view.date += relativedelta.relativedelta(months=1)
        elif caption == "Next Year":
            self.view.date += relativedelta.relativedelta(years=1)
        elif caption == "Today":
            self.view.date = datetime.now()
        elif caption == "Reset form":
            self.view.cat_var.set("")
            self.view.val_var.set("")
            self.view.des_var.set("")
            self.view.remind_var.set(0)
            pass

        val = self.get_value(self.view.cat_var.get().lower(), self.view.date)
        if val is not None:
            self.view.val_var.set(val)
        else:
            self.view.val_var.set("")
        if self.get_reminder_status(self.view.cat_var.get().lower()) is not None:
            self.view.remind_var.set(1)
        else:
            self.view.remind_var.set(0)
        des = self.get_description(self.view.cat_var.get().lower())
        if des is not None:
            self.view.des_var.set(des)
        else:
            self.view.des_var.set("")

        self.view.current_day.set(f'{self.view.date.month} / {self.view.date.day} / {self.view.date.year}')
        # print(f'{caption} has been pressed')

    # Buttons for data manipulation
    def entry_button_click(self,caption):
        if caption == "Lookup":
            # If there is a category typed in
            if self.view.cat_var.get().lower() is not '':
                data = self.db.read_database(self.db.conn, "data", "Entries",
                                             "WHERE category_name = \"{}\" and year = {} and month = {} {}".format(
                                                 self.view.cat_var.get().lower(), self.view.date.year, self.view.date.month,
                                                 'and day = ' + str(self.view.date.day)), "string",
                                             "one")

                if data is None:  # Empty entry
                    self.view.val_var.set('')
                    self.view.popup_window("Alert", "No value found for this day")
                else:             # Entry exists
                    self.view.val_var.set(data[0])
                    self.view.des_var.set(self.get_description(self.view.cat_var.get().lower()))

            # Pull reminder info for queried category
            try:
                if self.db.exists(self.db.conn, "Reminders", "category_name", f"\"{self.view.cat_var.get().lower()}\""):
                    self.view.remind_var.set(1)

            except Exception as e:
                self.view.remind_var.set(0)
        elif caption == "Update":
            try:
                # If there is input
                if self.view.cat_var.get() is not '' and self.view.val_var.get() is not '':
                    if self.db.read_database(self.db.conn, "data", "Entries",
                                            "WHERE category_name = \"{}\" and year = {} and month = {} and day = {}".format(
                                                    self.view.cat_var.get().lower(), self.view.date.year, self.view.date.month, self.view.date.day), "string", "one") is None:
                         self.db.write_database(self.db.conn, "insert", "Entries", "category_name, year, month, day, data",
                                              "\"{}\", {}, {}, {}, \"{}\"".format(self.view.cat_var.get().lower(), self.view.date.year, self.view.date.month, self.view.date.day,
                                                                                  self.view.val_var.get().lower()))
                    else:
                        self.db.write_database(self.db.conn, "update", "Entries", "data = {}".format(self.view.val_var.get().lower()),
                                          "WHERE category_name = \"{}\" and year = {} and month = {} and day = {}".format(
                                              self.view.cat_var.get().lower(), self.view.date.year, self.view.date.month, self.view.date.day))

                    # Inserts category into database if it is novel
                    cat_type = "string"
                    if self.view.cat_var.get().isnumeric():
                        cat_type = "float"
                    self.db.write_database(self.db.conn, "insert","Categories","name, type, description", f"\"{self.view.cat_var.get().lower()}\", \"{cat_type}\", \"\"")

                    # Updates entry
                    self.db.conn.commit()
                    self.view.popup_window("Success", f"Entry has been updated to {self.view.val_var.get()}")
                else: raise Exception("Missing input in fields")
            except Exception as e: self.view.popup_window("Error", e)
        elif caption == "Set":
            if self.view.cat_var.get() is not '':
                self.set_description(self.view.des_var.get(), self.view.cat_var.get().lower())
                self.view.popup_window("Alert", f"Category description has been set to\n\"{self.view.des_var.get()}\"")

    # Extras buttons
    def message_button_click(self, caption):
        if caption=="Help":
            self.view.popup_window("Help",
                          "This program shows you one day's entry at a time.\n\n"
                          "In the middle text box, type in a \"category\" of data whose entry you would like to create or view.\n"
                          "The lower text box will be used to enter a corresponding data value (pressing \"Lookup\" above will make the lower box show any existing value)\n\n"
                          "You can enter any combination of Category and Data value, press \"Update\",\n"
                          "and it will write (or overwrite) the entry for the selected day."
                                   )
        elif caption=="Sum values (month)":
            if self.view.cat_var.get() is not '':  # if there is valid input
                try:
                    data_set = self.db.read_database(self.db.conn, "data", "Entries",
                                          f"WHERE category_name = \"{self.view.cat_var.get().lower()}\" and year = {self.view.date.year} and month = {self.view.date.month}", "int", "all")

                    sum = 0
                    for data in data_set:
                        sum+=int(data[0])

                    self.view.popup_window("Result", f"Sum of \"{self.view.cat_var.get()}\" values for {self.view.date.month}-{self.view.date.year}:\n\n{sum}")
                except Exception as e: self.view.popup_window("Error", e)
        elif caption=="Sum values (year)":
            if self.view.cat_var.get() is not '':  # if there is valid input
                try:
                    data_set = self.db.read_database(self.db.conn, "data", "Entries",
                                          f"WHERE category_name = \"{self.view.cat_var.get().lower()}\" and year = {self.view.date.year}", "int", "all")

                    sum = 0
                    for data in data_set:
                        sum+=int(data[0])

                    self.view.popup_window("Result", f"Sum of \"{self.view.cat_var.get()}\" values for {self.view.date.year}:\n\n{sum}")
                except Exception as e: self.view.popup_window("Error", e)
        elif caption == "Toggle reminder for category":
            boolean = self.view.remind_var.get()
            if boolean == 1 and self.view.cat_var.get().lower() is not '':
                self.db.write_database(self.db.conn, "insert", "Reminders", "category_name", f"\"{self.view.cat_var.get().lower()}\"")
                self.db.conn.commit()
            elif boolean == 0 and self.view.cat_var.get().lower() is not '':
                self.db.write_database(self.db.conn, "delete", "Reminders", "category_name",
                                       f"\"{self.view.cat_var.get().lower()}\"")
                self.db.conn.commit()
            elif boolean == 1 and self.view.cat_var.get().lower() is '':
                self.view.remind_var.set(0)

        elif caption == "List of categories":
            message = ''
            cats = self.db.read_database(self.db.conn, "name", "Categories", None, "string", "all")
            for cat in cats:
                message+=cat[0]+'\n'

            self.view.popup_window("Categories", message)
        elif caption == "Entries for this day":
            message = ''
            entries = self.db.read_database(self.db.conn, "category_name, data", "Entries",
                                            f"WHERE year = {self.view.date.year} and month = {self.view.date.month} and day = {self.view.date.day}",
                                            "string", "all")
            for name, data in entries:
                message+=f"{name}: {data}\n"

            self.view.popup_window("Entries for this day", message)

    # Get value for a category
    def get_value(self, cat, date):
        data = self.db.read_database(self.db.conn, "data", "Entries", f"WHERE category_name = \"{cat}\" and year = {date.year} and month = {date.month} and day = {date.day}", "string", "one")

        return data

    # Checks db for set reminders
    def check_reminders(self):
        data_set = self.db.read_database(self.db.conn, "category_name", "Reminders", None, "string", "all")
        list = []

        try:
            for data in data_set:
                list.append(data[0])
        except Exception as e:
            print(e)
            return None

        return list

    # Get reminder status for a category
    def get_reminder_status(self, cat):
        data = self.db.read_database(self.db.conn, "id", "Reminders", f"WHERE category_name = \"{cat}\"", "int", "one")

        return data

    # Get description from db
    def get_description(self, cat):
        data = self.db.read_database(self.db.conn, "description", "Categories", f"WHERE name = \"{cat}\"", "string", "one")

        return data

    # Set description to db
    def set_description(self, desc, cat):
        self.db.write_database(self.db.conn, "update", "Categories", f"description = \"{desc}\"", f"WHERE name = \"{cat}\"")
        self.db.conn.commit()


if __name__ == '__main__':
    tracker = Controller()
    tracker.main()

from datetime import datetime, timedelta
from dateutil import relativedelta
from model import Category, Entry
from view import View
import tkinter as tk
from database import Database


class Controller:
    def __init__(self):
        self.db = Database()
        self.view = View(self)

    def main(self):
        self.view.main()

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

        self.view.cat_var.set("")
        self.view.val_var.set("")

        self.view.current_day.set(f'{self.view.date.month} / {self.view.date.day} / {self.view.date.year}')
        # print(f'{caption} has been pressed')

    def entry_button_click(self,caption):
        if caption == "Lookup":
            data = self.db.read_database(self.db.conn, "data", "Entries",
                                         "WHERE category_name = \"{}\" and year = {} and month = {} {}".format(
                                             self.view.cat_var.get().lower(), self.view.date.year, self.view.date.month,
                                             'and day = ' + str(self.view.date.day)), "string",
                                         "one")

            if data is None:
                self.view.popup_window("Alert", "No value found for this day")
            else:
                self.view.val_var.set(data[0])
        elif caption == "Update":
            try:
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

                self.db.conn.commit()
                self.view.popup_window("Success", "Entry has been updated")
            except Exception as e: self.view.popup_window("Error", e)

    def message_button_click(self, caption):
        if caption=="Help":
            self.view.popup_window("Help",
                          "This program shows you one day's entry at a time.\n\n"
                          "In the upper text box, type in a \"category\" of data whose entry you would like to create or view.\n"
                          "The lower text box will be used to enter a corresponding data value (pressing \"Lookup\" above will make the lower box show any existing value)\n\n"
                          "You can enter any combination of Category and Data value, press \"Update\",\n"
                          "and it will write (or overwrite) the entry for the selected day."
                                   )


if __name__ == '__main__':
    tracker = Controller()
    tracker.main()

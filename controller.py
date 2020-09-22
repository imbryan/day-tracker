from datetime import datetime, timedelta
from dateutil import relativedelta
from model import Category, Entry
from view import View
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

        self.view.current_day.set(f'{self.view.date.month} / {self.view.date.day} / {self.view.date.year}')
        # print(f'{caption} has been pressed')


if __name__ == '__main__':
    tracker = Controller()
    tracker.main()

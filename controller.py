from model import Category, Entry
from view import View


class Controller:
    def __init__(self):
        self.view = View(self)

    def main(self):
        self.view.main()


if __name__ == '__main__':
    tracker = Controller()
    tracker.main()

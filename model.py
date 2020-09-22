class Category:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Entry:
    def __init__(self, cat_name, year, month, day, data):
        self.category_name = cat_name
        self.year = year
        self.month = month
        self.day = day
        self.data = data

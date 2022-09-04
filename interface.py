from model import Category, Entry
from database import Database
import datetime

# ! This is a deprecated interface
# ! It was once the main interface but is now obsolete with respect to current features


class Interface:
    @staticmethod
    def main():
        db = Database()

        choose = '0'
        while choose != 'q':
            try:
                choose = input("[e]nter/update data, [v]iew data, or [q]uit: ").lower()

                if choose == 'e':
                    choose = input("Create [c]ategory or create/update [e]ntry: ").lower()
                    if choose == 'c':
                        cat_name = input("Enter category name: ").lower()
                        cat_type = input("Is the [n]umerical or [t]ext? ").lower()

                        if cat_type == 'n': cat_type = 'float'
                        elif cat_type == 't': cat_type = 'string'
                        else: raise Exception("Invalid option")

                        cat = Category(cat_name, cat_type)
                        db.write_database(db.conn, "insert", "Categories", "name, type", "\"{}\", \"{}\"".format(cat.name, cat.type))  # Write to database
                        print("Category {} has been created".format(cat.name))

                        db.conn.commit()

                    elif choose == 'e':
                        cat_choice = input("Create entry under which category? ")
                        cat = Category(cat_choice, db.read_database(db.conn, "type", "Categories", "WHERE name = \"{}\"".format(cat_choice), "string", "one")) # Read category (make sure it exists)

                        entry_data = str(input("Enter data for today's entry: "))

                        date = datetime.datetime.now()

                        if db.read_database(db.conn, "data", "Entries", "WHERE category_name = \"{}\" and year = {} and month = {} and day = {}".format(cat.name, date.year, date.month, date.day), "string", "one") is None:
                            db.write_database(db.conn, "insert", "Entries", "category_name, year, month, day, data", "\"{}\", {}, {}, {}, \"{}\"".format(cat.name, date.year, date.month, date.day, entry_data))
                        else:
                            db.write_database(db.conn, "update", "Entries", "data = {}".format(entry_data), "WHERE category_name = \"{}\" and year = {} and month = {} and day = {}".format(cat.name, date.year, date.month, date.day))
                            print("Today's entry for {} has been updated".format(cat.name.capitalize()))
                        db.conn.commit()
                elif choose == 'v':
                    date = input("[t]oday, [o]ther day, [m]onth: ").lower()

                    one_flag = True
                    one_string = 'one'
                    day_string = 'and day = '

                    if date == 't':
                        date = datetime.datetime.today()
                    elif date == 'o':
                        raw_date = input("Enter date as YYYY-MM-DD: ")
                        date = datetime.date(year=int(raw_date[0:4]), month=int(raw_date[5:7].strip("0")), day=int(raw_date[8:10]))
                    elif date == 'm':
                        one_flag = False
                        raw_date = input("Enter date as YYYY-MM: ")
                        date = datetime.date(year=int(raw_date[0:4]), month=int(raw_date[5:7].strip("0")), day=1)

                    cat_choice = input("View data for which category? ").lower()
                    cat_type = db.read_database(db.conn, "type", "Categories", "WHERE name = \"{}\"".format(cat_choice), "string", "one")

                    if not one_flag:
                        one_string = 'all'
                        day_string = ''
                    else:
                        day_string += str(date.day)
                    entry_data = db.read_database(db.conn, "data", "Entries",
                                                   "WHERE category_name = \"{}\" and year = {} and month = {} {}".format(
                                                       cat_choice, date.year, date.month, day_string), cat_type, one_string)

                    if entry_data is not None:
                        if one_flag:
                            print(
                                "{}'s entry for {} is {}".format(date.strftime('%Y-%m-%d'), cat_choice.capitalize(), entry_data))
                        else:
                            sum = 0
                            print("{}'s entries for {}".format(date.strftime('%Y-%m'), cat_choice.capitalize()))
                            for entry in entry_data:
                                if entry[0].isnumeric():
                                    sum +=int (entry[0])
                                print("{}".format(entry[0]))
                            if sum > 0:
                                print("Total: {}".format(sum))

                elif choose == 'q':
                    print('Goodbye')

            except Exception as e: print(e)


if __name__ == '__main__':
    Interface.main()

import sqlite3 as lite
import datetime


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


def main():
    # Connect to database
    database = "tracker.db"
    conn = lite.connect(database)

    create_table(conn, "Categories", "id integer PRIMARY KEY, name text, type text, UNIQUE(name)")
    create_table(conn, "Entries", "id integer PRIMARY KEY, category_name text, year integer, month integer, day integer, data text")

    # User interface

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
                    write_database(conn, "insert", "Categories", "name, type", "\"{}\", \"{}\"".format(cat.name, cat.type))  # Write to database
                    print("Category {} has been created".format(cat.name))

                    conn.commit()

                elif choose == 'e':
                    cat_choice = input("Create entry under which category? ")
                    cat = Category(cat_choice, read_database(conn, "type", "Categories", "WHERE name = \"{}\"".format(cat_choice), "string", "one")) # Read category (make sure it exists)

                    entry_data = str(input("Enter data for today's entry: "))

                    date = datetime.datetime.now()

                    if read_database(conn, "data", "Entries", "WHERE category_name = \"{}\" and year = {} and month = {} and day = {}".format(cat.name, date.year, date.month, date.day), "string", "one") is None:
                        write_database(conn, "insert", "Entries", "category_name, year, month, day, data", "\"{}\", {}, {}, {}, \"{}\"".format(cat.name, date.year, date.month, date.day, entry_data))
                    else:
                        write_database(conn, "update", "Entries", "data = {}".format(entry_data), "WHERE category_name = \"{}\" and year = {} and month = {} and day = {}".format(cat.name, date.year, date.month, date.day))
                        print("Today's entry for {} has been updated".format(cat.name.capitalize()))
                    conn.commit()
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
                cat_type = read_database(conn, "type", "Categories", "WHERE name = \"{}\"".format(cat_choice), "string", "one")

                if not one_flag:
                    one_string = 'all'
                    day_string = ''
                else:
                    day_string += str(date.day)
                entry_data = read_database(conn, "data", "Entries",
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


def create_table(connect, table_name, args):
    if args is None: args = ""
    c = connect.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS {} ( {} );""".format(table_name, args))


def read_database(connect, select, table, args, datatype, mode):
    if args is None: args = ""
    c = connect.cursor()
    statement = """SELECT {} FROM {} {};""".format(select, table, args)
    c.execute(statement)

    temp = None
    if mode == "one":
        temp = c.fetchone()
    elif mode == "all":
        temp = c.fetchall()

    if temp is not None and mode == "one":
        if datatype == "int":
            temp = int(temp[0])
        elif datatype == "float":
            temp = float(temp[0])
        elif datatype == "string":
            temp = str(temp[0])

    return temp


def write_database(connect, mode, table, args1, args2):
    if args1 is None: args1 = ""
    if args2 is None: args2 = ""
    c = connect.cursor()

    statement = ""

    if mode == "update":
        statement = """UPDATE {} SET {} {};""".format(table, args1, args2)
    elif mode == "insert":
        statement = """INSERT OR IGNORE INTO {}({}) VALUES({});""".format(table, args1, args2)

    c.execute(statement)


if __name__ == "__main__":
    main()
import sqlite3 as lite


class Database:
    def __init__(self):
        # Connect to database
        self.database = "tracker.db"
        self.conn = lite.connect(self.database)

        self.create_table(self.conn, "Categories", "id integer PRIMARY KEY, name text, type text, UNIQUE(name)")
        self.create_table(self.conn, "Entries", "id integer PRIMARY KEY, category_name text, year integer, month integer, day integer, data text")
        self.create_table(self.conn, "Reminders", "id integer PRIMARY KEY, category_name text, UNIQUE(category_name)")

    def create_table(self, connect, table_name, args):
        if args is None: args = ""
        c = connect.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS {} ( {} );""".format(table_name, args))

    def read_database(self, connect, select, table, args, datatype, mode):
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

    def write_database(self, connect, mode, table, args1, args2):
        if args1 is None: args1 = ""
        if args2 is None: args2 = ""
        c = connect.cursor()

        statement = ""

        if mode == "update":
            statement = """UPDATE {} SET {} {};""".format(table, args1, args2)
        elif mode == "insert":
            statement = """INSERT OR IGNORE INTO {}({}) VALUES({});""".format(table, args1, args2)
        elif mode == "delete":
            statement = """DELETE FROM {} WHERE {} = {};""".format(table, args1, args2)

        c.execute(statement)

    def count(self, connect, table):
        c = connect.cursor()
        statement = """SELECT COUNT(*) FROM {};""".format(table)
        c.execute(statement)
        return c.fetchone()[0]

    def exists(self, connect, table, key, value):
        c = connect.cursor()
        statement = """SELECT * FROM {} WHERE {} = {};""".format(table, key, value)
        c.execute(statement)
        return c.fetchone()[0]

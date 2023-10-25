import os
import model
from datetime import datetime, timedelta
from dateutil import relativedelta
import time
from view import View
from database import session, DB_FILENAME
from setup import add_missing_columns_from_sqlalchemy_migration, add_missing_columns_from_updates, populate_reminders_category_ids, populate_entries_category_ids
from shutil import copyfile
from sqlalchemy import or_
from sqlalchemy.orm import load_only


class Controller:
    def __init__(self):
        # self.db = Database() # ! Deprecated
        self.session = session
        self.db_name = DB_FILENAME

        # Checks if setup scripts are needed
        try:
            # Checking for SQLAlchemy Migration changes
            self.session.query(model.Reminder).filter(model.Reminder.category_id==1).all()
            self.session.query(model.Entry).filter(model.Entry.category_id==1).all()
            
        except:
            print('Complying with SQLAlchemy Migration changes')
            add_missing_columns_from_sqlalchemy_migration(self.session)
        try:
            # Checking for update changes
            self.session.query(model.Category).filter(model.Category.enabled==True).first()
        except:
            print('Complying with update changes')
            add_missing_columns_from_updates(self.session)
        # Checking for NULL category_id fields
        check_reminders = self.session.query(model.Reminder).filter(model.Reminder.category_id==None).all()
        if check_reminders:
            print(f'{len(check_reminders)} legacy reminders detected')
            populate_reminders_category_ids(self.session, check_reminders)
        check_entries = self.session.query(model.Entry).filter(model.Entry.category_id==None).all()
        if check_entries:
            print(f'{len(check_entries)} legacy entries detected')
            populate_entries_category_ids(self.session, check_entries)
        ### passed all checks ###

        self.view = View(self, self.session)

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
        # elif caption == "Reset form":
        #     self.view.cat_var.set("")
        #     self.view.val_var.set("")
        #     self.view.des_var.set("")
        #     self.view.remind_var.set(0)
        #     pass

        # ! Below is deprecated - UI Refresh
        # val = self.get_value(self.view.cat_var.get().lower(), self.view.date)
        # print(f'get_value {self.view.cat_var.get().lower()} {val}')
        # if val is not None:
        #     self.view.val_var.set(val)
        # else:
        #     self.view.val_var.set("")
        if self.get_reminder_status(self.view.cat_var.get().lower()) is not None:
            self.view.remind_var.set(1)
        else:
            self.view.remind_var.set(0)
        # des = self.get_description(self.view.cat_var.get().lower())
        # if des is not None:
        #     self.view.des_var.set(des)
        # else:
        #     self.view.des_var.set("")
        # ! end deprecation
        self.view.entries_frame = self.view._make_entries(self.view.date)

        self.view.current_day.set(f'{self.view.date.month} / {self.view.date.day} / {self.view.date.year}')
        # print(f'{caption} has been pressed')

    # Buttons for data manipulation
    def entry_button_click(self,caption):
        if caption == "Lookup":
            # If there is a category typed in
            category_input = self.view.cat_var.get().lower()
            if category_input != '':
                # data = self.db.read_database(self.db.conn, "data", "Entries",
                #                              "WHERE category_name = \"{}\" and year = {} and month = {} {}".format(
                #                                  self.view.cat_var.get().lower(), self.view.date.year, self.view.date.month,
                #                                  'and day = ' + str(self.view.date.day)), "string",
                #                              "one")  # ! Deprecated
                entry = self.session.query(model.Entry).join(model.Category, model.Category.id==model.Entry.category_id)\
                    .filter(
                        model.Category.name == category_input,
                        model.Entry.year==self.view.date.year, 
                        model.Entry.month==self.view.date.month, 
                        model.Entry.day==self.view.date.day
                    ).first()
                if entry is None:  # Empty entry
                    self.view.val_var.set('')
                    self.view.popup_window("Alert", "No value found for this day")
                else:             # Entry exists
                    # self.view.val_var.set(data[0])  # ! Deprecated
                    self.view.val_var.set(entry.data)
                    self.view.des_var.set(self.get_description(self.view.cat_var.get().lower()))

            # Pull reminder info for queried category 
            try:
                reminder = self.session.query(model.Reminder).join(model.Category, model.Category.id == model.Reminder.category_id)\
                    .filter(
                        model.Category.name == self.view.cat_var.get().lower()
                    ).first()
                # if self.db.exists(self.db.conn, "Reminders", "category_name", f"\"{self.view.cat_var.get().lower()}\""):  # ! Deprecated
                if reminder:
                    self.view.remind_var.set(1)

            except Exception as e:
                self.view.remind_var.set(0)
        elif caption == "Update":
            try:
                # If there is input
                if self.view.cat_var.get() != '' and self.view.val_var.get() != '':
                    # if self.db.read_database(self.db.conn, "data", "Entries",  # ! Deprecated
                    #                         "WHERE category_name = \"{}\" and year = {} and month = {} and day = {}".format(
                    #                                 self.view.cat_var.get().lower(), self.view.date.year, self.view.date.month, self.view.date.day), "string", "one") is None:
                    #      self.db.write_database(self.db.conn, "insert", "Entries", "category_name, year, month, day, data",
                    #                           "\"{}\", {}, {}, {}, \"{}\"".format(self.view.cat_var.get().lower(), self.view.date.year, self.view.date.month, self.view.date.day,
                    #                                                               self.view.val_var.get().lower()))
                    # else:
                    #     self.db.write_database(self.db.conn, "update", "Entries", "data = {}".format(self.view.val_var.get().lower()),
                    #                       "WHERE category_name = \"{}\" and year = {} and month = {} and day = {}".format(
                    #                           self.view.cat_var.get().lower(), self.view.date.year, self.view.date.month, self.view.date.day))
                    self.set_cat_value(self.view.cat_var.get().lower(), self.view.date, self.view.val_var.get().lower())

                    # Inserts category into database if it is novel 
                    # cat_type = "string"  # ! Deprecated
                    # if self.view.cat_var.get().isnumeric():
                    #     cat_type = "float"
                    # self.db.write_database(self.db.conn, "insert","Categories","name, type, description", f"\"{self.view.cat_var.get().lower()}\", \"{cat_type}\", \"\"")

                    # Updates entry  
                    # self.db.conn.commit()  # ! Deprecated
                    self.view.popup_window("Success", f"Entry has been updated to {self.view.val_var.get()}")
                else: raise Exception("Missing input in fields")
            except Exception as e: self.view.popup_window("Error", e)
        elif caption == "Set":
            if self.view.cat_var.get() != '':
                self.set_description(self.view.des_var.get(), self.view.cat_var.get().lower())
                self.view.popup_window("Alert", f"Category description has been set to\n\"{self.view.des_var.get()}\"")
        elif caption == "Save All":
            for widget in self.view.entries_frame.winfo_children():
                if getattr(widget, 'category_id', None):
                    self.set_cat_value(widget.category_id, self.view.date, widget.entry_text_var.get())
            self.view.popup_window("Success", "All entries have been updated.")

    def toggle_cat(self):
        name = View.input_window("Categories", "Which category would you like to toggle?")
        if name:
            category = self.session.query(model.Category).filter(model.Category.name.ilike(name)).first()
        else:
            category = None
        if category:
            category.enabled = not category.enabled
            self.session.commit()
            info_text = 'shown' if category.enabled else 'hidden'
            View.popup_window("Success", f"Category \"{category.name}\" is now {info_text}.")
            self.view.entries_frame = self.view._make_entries(current_date=self.view.date)
        elif name:
            View.popup_window("Alert", f"Category \"{name}\" was not found.")


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
        elif caption=="Sum (month)":
            if self.view.cat_var.get() != '':  # if there is valid input
                try:
                    # data_set = self.db.read_database(self.db.conn, "data", "Entries",  # ! Deprecated
                    #                       f"WHERE category_name = \"{self.view.cat_var.get().lower()}\" and year = {self.view.date.year} and month = {self.view.date.month}", "int", "all")
                    data_set = self.session.query(model.Entry).join(model.Category, model.Category.id==model.Entry.category_id)\
                        .filter(
                            model.Category.name==self.view.cat_var.get().lower(),
                            model.Entry.year==self.view.date.year, 
                            model.Entry.month==self.view.date.month
                        ).options(load_only('data')).all()

                    sum = 0
                    for entry in data_set:
                        sum+=int(getattr(entry, 'data', 0))

                    self.view.popup_window("Result", f"Sum of \"{self.view.cat_var.get()}\" values for {self.view.date.month}-{self.view.date.year}:\n\n{sum}")
                except Exception as e: self.view.popup_window("Error", e)
        elif caption=="Sum (year)":
            if self.view.cat_var.get() != '':  # if there is valid input
                try:
                    # data_set = self.db.read_database(self.db.conn, "data", "Entries",  # ! Deprecated
                    #                       f"WHERE category_name = \"{self.view.cat_var.get().lower()}\" and year = {self.view.date.year}", "int", "all")
                    data_set = self.session.query(model.Entry).join(model.Category, model.Category.id==model.Entry.category_id)\
                        .filter(
                            model.Category.name==self.view.cat_var.get().lower(),
                            model.Entry.year==self.view.date.year
                        ).options(load_only('data')).all()
                    sum = 0
                    for entry in data_set:
                        sum+=int(getattr(entry, 'data', 0))

                    self.view.popup_window("Result", f"Sum of \"{self.view.cat_var.get()}\" values for {self.view.date.year}:\n\n{sum}")
                except Exception as e: self.view.popup_window("Error", e)
        elif caption=="Average (month)":
            if self.view.cat_var.get() != '':
                try:
                    # data_set = self.db.read_database(self.db.conn, "data", "Entries",  # ! Deprecated
                    #                                  f"WHERE category_name = \"{self.view.cat_var.get().lower()}\" and year = {self.view.date.year} and month = {self.view.date.month}",
                    #                                  "int", "all")
                    data_set = self.session.query(model.Entry).join(model.Category, model.Category.id==model.Entry.category_id)\
                        .filter(
                            model.Category.name==self.view.cat_var.get().lower(),
                            model.Entry.year==self.view.date.year, 
                            model.Entry.month==self.view.date.month
                        ).options(load_only('data')).all()
                    sum = 0
                    use_date = self.view.date
                    if datetime.now().date() > use_date.date():
                        # Calculate whole month if it's already past
                        use_date = use_date.replace(day=1,month=use_date.month+1) - timedelta(days=1)
                    count = (use_date - use_date.replace(day=1)).days + 1
                    for entry in data_set:
                        sum += int(getattr(entry, 'data', 0))

                    average = round(sum / count, 2)

                    self.view.popup_window("Result",
                                       f"Average of \"{self.view.cat_var.get()}\" values for {self.view.date.month}-{self.view.date.year}:\n\n{average} (given {count} days)")
                except Exception as e:
                    self.view.popup_window("Error", e)
        elif caption=="Average (year)":
            if self.view.cat_var.get() != '':
                try:
                    # data_set = self.db.read_database(self.db.conn, "data", "Entries",  # ! Deprecated
                    #                                  f"WHERE category_name = \"{self.view.cat_var.get().lower()}\" and year = {self.view.date.year}",
                    #                                  "int", "all")
                    data_set = self.session.query(model.Entry).join(model.Category, model.Category.id==model.Entry.category_id)\
                        .filter(
                            model.Category.name==self.view.cat_var.get().lower(),
                            model.Entry.year==self.view.date.year
                        ).options(load_only('data')).all()

                    sum = 0
                    use_date = self.view.date
                    if datetime.now().year > use_date.year:  
                        # Calculate whole year if it's already past
                        use_date = use_date.replace(day=1,month=1,year=use_date.year+1) - timedelta(days=1)
                    count = (use_date - use_date.replace(month=1, day=1)).days + 1
                    for entry in data_set:
                        sum += int(getattr(entry, 'data', 0))

                    average = round(sum / count, 2)

                    self.view.popup_window(
                        "Result",
                        f"Average of \"{self.view.cat_var.get()}\" values for {self.view.date.year}:\n\n{average} (given {count} days)"
                    )
                except Exception as e:
                    self.view.popup_window("Error", e)
        # elif caption == "Toggle reminder for category":  # ! Deprecated -- UI Refresh
        #     boolean = self.view.remind_var.get()
        #     category = self.session.query(model.Category).filter(
        #         or_(model.Category.name == self.view.cat_var.get().lower(), model.Category.id == self.view.cat_var.get().lower())
        #     ).first()
        #     if boolean == 1 and category:
        #         # self.db.write_database(self.db.conn, "insert", "Reminders", "category_name", f"\"{self.view.cat_var.get().lower()}\"")  # ! Deprecated
        #         # self.db.conn.commit()
        #         self.session.add(model.Reminder(category_id=category.id))
        #         self.session.commit()
        #     elif boolean == 0 and category:
        #         # self.db.write_database(self.db.conn, "delete", "Reminders", "category_name",  # ! Deprecated
        #         #                        f"\"{self.view.cat_var.get().lower()}\"")
        #         # self.db.conn.commit()
        #         self.session.delete(category.reminder)
        #         self.session.commit()
        #     elif boolean == 1 and self.view.cat_var.get().lower() == '':
        #         self.view.remind_var.set(0)

        elif caption == "All Categories":
            message = ''
            # cats = self.db.read_database(self.db.conn, "name", "Categories", None, "string", "all")  # ! Deprecated
            cats = self.session.query(model.Category).options(load_only('name')).all()
            for cat in cats:
                message+=f'{cat.name}\n'

            self.view.popup_window("Categories", message)
        # elif caption == "Entries for this day": # ! Deprecated -- UI Refresh
        #     message = ''
        #     # entries = self.db.read_database(self.db.conn, "category_name, data", "Entries",  # ! Deprecated
        #     #                                 f"WHERE year = {self.view.date.year} and month = {self.view.date.month} and day = {self.view.date.day}",
        #     #                                 "string", "all")
        #     entries = self.session.query(model.Entry).filter_by(year=self.view.date.year, month=self.view.date.month, day=self.view.date.day).all()
        #     for entry in entries:
        #         message+=f"{entry.category.name}: {entry.data}\n"

        #     self.view.popup_window("Entries for this day", message)

    # Get value for a category
    def get_value(self, cat, date):
        # data = self.db.read_database(self.db.conn, "data", "Entries", f"WHERE category_name = \"{cat}\" and year = {date.year} and month = {date.month} and day = {date.day}", "string", "one")  # ! Deprecated
        entry = self.session.query(model.Entry)\
            .join(model.Category, model.Category.id==model.Entry.category_id)\
            .filter(
                model.Category.name==cat,
                model.Entry.year==date.year,
                model.Entry.month==date.month, 
                model.Entry.day==date.day,
            ).options(load_only('data'))
        entry = entry.first()
        if entry:
            return entry.data
        return None

    # Sets value for a category, date. Creates if not exists
    def set_cat_value(self, cat_id_or_name, date, value):
        category = self.session.query(model.Category).filter(or_(model.Category.name==cat_id_or_name, model.Category.id==cat_id_or_name)).first()
        if not category:
            # You wouldn't be passing an ID if the category didn't exist
            if value.isnumeric():
                category_type = 'float'
            else:
                category_type = 'string'
            try:
                time.strptime(value, '%H:%M')
                category_type = 'time'
            except: pass
            category = model.Category(name=cat_id_or_name, type=category_type)
            self.session.add(category)
        current_entry = self.session.query(model.Entry).join(model.Category, model.Category.id==model.Entry.category_id)\
            .filter(
                or_(model.Category.name==cat_id_or_name, model.Category.id==cat_id_or_name),
                model.Entry.year==date.year, 
                model.Entry.month==date.month,
                model.Entry.day==date.day
            ).first()
        if current_entry:
            current_entry.data = value
        else:
            new_entry = model.Entry(year=date.year, month=date.month, day=date.day, category_id=category.id, data=value)
            self.session.add(new_entry)
        self.session.commit()


    # Checks db for set reminders
    def check_reminders(self):
        # data_set = self.db.read_database(self.db.conn, "category_name", "Reminders", None, "string", "all")  # ! Deprecated
        data_set = self.session.query(model.Reminder).all()
        list = []

        try:
            for data in data_set:
                # list.append(data[0])  # ! Deprecated
                list.append(data.category.name)
        except Exception as e:
            print(e)
            return None

        return list

    # Get reminder status for a category
    def get_reminder_status(self, cat):
        # data = self.db.read_database(self.db.conn, "id", "Reminders", f"WHERE category_name = \"{cat}\"", "int", "one")  # ! Deprecated
        reminder = self.session.query(model.Reminder).join(model.Category, model.Category.id==model.Reminder.category_id)\
            .filter(model.Category.name==cat).options(load_only('id')).first()
        if reminder:
            return True
        return None

    # Get description from db
    def get_description(self, cat):
        # data = self.db.read_database(self.db.conn, "description", "Categories", f"WHERE name = \"{cat}\"", "string", "one")  # ! Deprecated
        category = self.session.query(model.Category).filter_by(name=cat).options(load_only('description')).first()
        if category:
            return category.description
        return ''

    # Set description to db
    def set_description(self, desc, cat):
        # self.db.write_database(self.db.conn, "update", "Categories", f"description = \"{desc}\"", f"WHERE name = \"{cat}\"")
        # self.db.conn.commit()  # ! Deprecated
        self.session.query(model.Category).filter(or_(model.Category.name==cat, model.Category.id==cat)).update(
            {'description': desc}
        )
        self.session.commit()

    # Create db backup
    def backup(self, top):
        name = self.view.backup_var.get()

        try:
            if name == "": raise Exception("No name entered")
            if not os.path.exists('backups'):
                os.makedirs('backups')
            if os.path.exists(f"backups/{name}.db"): raise Exception("File already exists")

            copyfile(self.db_name, f"backups/{name}.db")
            top.destroy()
            self.view.popup_window("Success", f"Backup created at \"backups/{name}.db\"")
        except Exception as e:
            self.view.popup_window("Error", e)


if __name__ == '__main__':
    tracker = Controller()
    tracker.main()

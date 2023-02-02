import model

### NOTE: These are helper functions that seek to repair issues that arise from updates ###


def add_missing_columns_from_sqlalchemy_migration(session):
    # session => The SQLAlchemy DB session object
    try:
        session.execute("ALTER TABLE Reminders ADD COLUMN category_id integer")
    except:
        print("Reminders.category_id already exists")
    try:
        session.execute("ALTER TABLE Entries ADD COLUMN category_id integer")
    except:
        print("Entries.category_id already exists")
    session.commit()
    print('SETUP: added missing columns from SQLAlchemy migration')


def populate_reminders_category_ids(session, reminders):
    count = 0
    for reminder in reminders:
        category = session.query(model.Category).filter_by(name=reminder.category_name).first()
        if category:
            reminder.category_id = category.id
            count += 1
        else:
            print(f'Could not update reminder (category "{reminder.category_name}" not found)')
    session.commit()
    print(f'{count} reminders fixed')


def populate_entries_category_ids(session, entries):
    count = 0
    for entry in entries:
        category = session.query(model.Category).filter_by(name=entry.category_name).first()
        if category:
            entry.category_id = category.id
            count += 1
        else:
            print(f'Could not update entry (category "{entry.category_name}" not found)')
    session.commit()
    print(f'{count} entries fixed')

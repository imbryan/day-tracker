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
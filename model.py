from database import Base, session
import datetime
from sqlalchemy import Column, Integer, Text, ForeignKey, BigInteger, or_
from sqlalchemy.orm import relationship, load_only
from sqlalchemy.ext.hybrid import hybrid_property


# NOTE: tables and columns will follow naming convention established in legacy db connection
# ... for the sake of backwards compatibility

class Category(Base):
    __tablename__ = 'Categories'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    type = Column(Text)
    description = Column(Text)

    reminder = relationship("Reminder", uselist=False, back_populates="category")


class Entry(Base):
    __tablename__ = 'Entries'

    id = Column(BigInteger, primary_key=True)
    category_name = Column(Text)  # ! Legacy field
    category_id = Column(Integer, ForeignKey('Categories.id'))  # NOTE supercedes category_name
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    data = Column(Text)

    category = relationship("Category")

    @property
    def date(self):
        return datetime.date(self.year, self.month, self.day)

    @hybrid_property
    def category_name_from_any(self):
        category = session.query(Category)\
            .join(Entry, or_(Entry.category_name==Category.name, Entry.category_id==Category.id))\
                .options(load_only('name')).first()
        if category:
            return category.name
        return None


class Reminder(Base):
    __tablename__ = 'Reminders'

    id = Column(Integer, primary_key=True)
    category_name = Column(Text)  # ! Legacy field
    category_id = Column(Integer, ForeignKey('Categories.id'))  # NOTE supercedes category_name

    category = relationship("Category", uselist=False, back_populates="reminder")

    @hybrid_property
    def category_name_from_any(self):
        category = session.query(Category)\
            .join(Reminder, or_(Reminder.category_name==Category.name, Reminder.category_id==Category.id))\
                .options(load_only('name')).first()
        if category:
            return category.name
        return None


# ! Pre-SQLAlchemy model schema below

# class Category:
#     def __init__(self, name, type):
#         self.name = name
#         self.type = type


# class Entry:
#     def __init__(self, cat_name, year, month, day, data):
#         self.category_name = cat_name
#         self.year = year
#         self.month = month
#         self.day = day
#         self.data = data

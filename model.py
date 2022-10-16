from database import Base, session
import datetime
from sqlalchemy import Column, Integer, Text, ForeignKey, BigInteger, or_, case, func, select
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

    # TODO debug
    @hybrid_property
    def category_name_from_any(self):
        if self.category_id:
            return self.category.name
        return self.category_name

    @category_name_from_any.expression
    def category_name_from_any(cls):
        q = session.query(Category).with_entities(Category.name)\
            .filter(or_(cls.category_id==Category.id, cls.category_name==Category.name))
        print('q', q)
        return q


class Reminder(Base):
    __tablename__ = 'Reminders'

    id = Column(Integer, primary_key=True)
    category_name = Column(Text)  # ! Legacy field
    category_id = Column(Integer, ForeignKey('Categories.id'))  # NOTE supercedes category_name

    category = relationship("Category", uselist=False, back_populates="reminder")

    # TODO debug
    @hybrid_property
    def category_name_from_any(self):
        if self.category_id:
            return self.category.name
        return self.category_name

    @category_name_from_any.expression
    def category_name_from_any(cls):
        return session.query(Category).with_entities(Category.name)\
            .filter(or_(cls.category_id==Category.id, cls.category_name==Category.name))


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

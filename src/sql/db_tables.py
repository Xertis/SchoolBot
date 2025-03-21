from sqlalchemy.ext.declarative import declarative_base
from src.utils.env import Constants
from sqlalchemy import (create_engine,
                        Column, Integer,
                        Text, TIMESTAMP,
                        ForeignKey, Float,
                        DECIMAL)

engine = create_engine(Constants.DB_PATH)
Base = declarative_base()


class phone_numbers(Base):
    __tablename__ = "phone_numbers"

    id = Column(Integer, primary_key=True)
    number = Column(Text)
    owner = Column(Text)


class events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("images.id"))
    title = Column(Text)
    text = Column(Text)
    time = Column(TIMESTAMP)


class admins(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)


class images(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)


class meal_plan(Base):
    __tablename__ = "meal_plan"
    id = Column(Integer, primary_key=True)
    meal = Column(Text)
    category = Column(Text)
    recipe = Column(Text)
    dish = Column(Text)
    grams = Column(Float)
    price = Column(DECIMAL)
    date = Column(TIMESTAMP)



Base.metadata.create_all(engine)

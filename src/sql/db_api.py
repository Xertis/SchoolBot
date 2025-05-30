from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.utils.env import Constants

from src.sql.queries.db_events import DB_events
from src.sql.queries.db_phone_numbers import DB_phone_numbers
from src.sql.queries.db_images import DB_images
from src.sql.queries.db_admins import DB_admins
from src.sql.queries.db_meal_plan import DB_meal_plan
from src.sql.queries.db_lessons_schedule import DB_lesson_schedule

engine = create_engine(Constants.DB_PATH)


class DB:
    def __init__(self):
        self.session = sessionmaker(bind=engine)()

        self.events = DB_events(self.session)
        self.numbers = DB_phone_numbers(self.session)
        self.images = DB_images(self.session)
        self.admins = DB_admins(self.session)
        self.meal = DB_meal_plan(self.session)
        self.lessons = DB_lesson_schedule(self.session)

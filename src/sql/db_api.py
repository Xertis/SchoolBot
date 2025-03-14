from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.utils.env import Constants

from src.sql.queries.db_events import DB_events
from src.sql.queries.db_phone_numbers import DB_phone_numbers
from src.sql.queries.db_images import DB_images
from src.sql.queries.db_admins import DB_admins

engine = create_engine(Constants.DB_PATH)


class DB:
    def __init__(self) -> None:
        self.session = sessionmaker(bind=engine)()

        self.events = DB_events(self.session)
        self.numbers = DB_phone_numbers(self.session)
        self.images = DB_images(self.session)
        self.admins = DB_admins(self.session)

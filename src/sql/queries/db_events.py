from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.utils.env import Constants
from src.sql.db_tables import events
from datetime import datetime as dt

engine = create_engine(Constants.DB_PATH)


class DB_events:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, title: str, text: str, time: dt, image: int) -> events:
        data = events(text=text)
        data.title = title
        data.time = time
        data.image_id = image
        self.session.add(data)
        self.session.commit()
        return data

    def get_all(self) -> list[events]:
        data = self.session.query(events).all()
        return data
    
    def get_by_date(self, date: dt.date) -> list[events]:
        return self.session.query(events).filter(
            func.date(events.time) == date
        ).all()
    
    def get_older(self, time: dt) -> list[events]:
        return self.session.query(events).filter(
            events.time < time
        ).all()

    def get_by_id(self, id: int) -> events:
        return self.session.query(events).filter(
            events.id == id
        ).one_or_none()

    def delete_by_id(self, id: int) -> None:
        data = self.session.query(events).filter(
            events.id == id).one_or_none()

        if data:
            self.session.delete(data)
            self.session.commit()

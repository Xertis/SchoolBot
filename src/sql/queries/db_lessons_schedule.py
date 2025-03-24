import re
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import Session
from src.utils.env import Constants
from src.sql.db_tables import lesson_schedule

engine = create_engine(Constants.DB_PATH)


class DB_lesson_schedule:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def __sort_by_class(data):
        def extract_number(school_class):
            match = re.search(r'\d+', school_class)
            return int(match.group(0)) if match else 0

        return sorted(data, key=lambda x: extract_number(x.school_class), reverse=True)

    def add(self, 
            weekday=str,
            school_class=str,
            lesson=str,
            lesson_number=int
        ) -> lesson_schedule:
        data = lesson_schedule()
        data.weekday = weekday
        data.school_class = school_class
        data.lesson = lesson
        data.lesson_number = lesson_number

        self.session.add(data)
        self.session.commit()
        return data

    def get_all(self) -> list[lesson_schedule]:
        data = self.session.query(lesson_schedule).order_by(desc(lesson_schedule.school_class)).all()
        return data

    def get_by_id(self, id: int) -> lesson_schedule:
        data = self.session.query(lesson_schedule).filter(
            lesson_schedule.id == id).one_or_none()
        return data
    
    def get_by_weekday(self, weekday: str) -> list[lesson_schedule]:
        data = self.session.query(lesson_schedule).filter(
            lesson_schedule.weekday == weekday).order_by(desc(lesson_schedule.school_class)).all()

        return DB_lesson_schedule.__sort_by_class(data)

    def delete_by_id(self, id: int) -> None:
        data = self.session.query(lesson_schedule).filter(
            lesson_schedule.id == id).one_or_none()

        if data:
            self.session.delete(data)
            self.session.commit()

    def delete_all(self) -> None:
        self.session.query(lesson_schedule).delete()
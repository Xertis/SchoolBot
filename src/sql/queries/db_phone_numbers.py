from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from constants import DB_PATH
from src.sql.db_tables import phone_numbers

engine = create_engine(DB_PATH)


class DB_phone_numbers:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, text: str) -> phone_numbers:
        data = phone_numbers(text=text)
        self.session.add(data)
        self.session.commit()
        return data
    
    def get_all(self) -> list[phone_numbers]:
        data = self.session.query(phone_numbers).all()
        return data

    def get_by_id(self, id: int) -> phone_numbers:
        data = self.session.query(phone_numbers).filter(
            phone_numbers.id == id).one_or_none()
        return data

    def delete_by_id(self, id: int) -> None:
        data = self.session.query(phone_numbers).filter(
            phone_numbers.id == id).one_or_none()

        if data:
            self.session.delete(data)
            self.session.commit()

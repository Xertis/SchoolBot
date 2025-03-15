from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.utils.env import Constants
from src.sql.db_tables import images
from datetime import datetime as dt

engine = create_engine(Constants.DB_PATH)


class DB_images:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, id=None) -> images:
        data = images(id=id)
        self.session.add(data)
        self.session.commit()
        return data

    def get_all(self) -> list[images]:
        data = self.session.query(images).all()
        return data

    def get_by_id(self, id: int) -> images:
        data = self.session.query(images).filter(
            images.id == id).one_or_none()
        return data

    def delete_by_id(self, id: int) -> None:
        data = self.session.query(images).filter(
            images.id == id).one_or_none()

        if data:
            self.session.delete(data)
            self.session.commit()

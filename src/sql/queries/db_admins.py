from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.utils.env import Constants
from src.sql.db_tables import admins
from datetime import datetime as dt

engine = create_engine(Constants.DB_PATH)


class DB_admins:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, tg_id: str) -> admins:
        data = admins(tg_id=tg_id)
        self.session.add(data)
        self.session.commit()
        return data

    def delete(self, tg_id: str) -> None:
        data = self.session.query(admins).filter(
            admins.tg_id == tg_id).one_or_none()

        if data:
            self.session.delete(data)
            self.session.commit()

    def has(self, tg_id: str) -> None:
        data = self.session.query(admins).filter(
            admins.tg_id == tg_id).one_or_none()

        if data:
            return True

        return False

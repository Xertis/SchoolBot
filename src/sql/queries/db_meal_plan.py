from sqlalchemy import create_engine, desc
from sqlalchemy.orm import Session
from src.utils.env import Constants
from src.sql.db_tables import meal_plan
from datetime import datetime as dt

engine = create_engine(Constants.DB_PATH)


class DB_meal_plan:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, 
            meal: str, 
            category: str, 
            recipe: str, 
            dish: str,
            grams: float,
            price: float,
            date: dt
        ) -> meal_plan:
        data = meal_plan()
        data.meal = meal
        data.category = category
        data.recipe = recipe
        data.dish = dish
        data.grams = grams
        data.price = price
        data.date = date
        self.session.add(data)
        self.session.commit()
        return data

    def get_all(self) -> list[meal_plan]:
        data = self.session.query(meal_plan).order_by(desc(meal_plan.date)).all()
        return data

    def get_by_id(self, id: int) -> meal_plan:
        data = self.session.query(meal_plan).filter(
            meal_plan.id == id).one_or_none()
        return data

    def get_older(self, date: dt) -> list[meal_plan]:
        return self.session.query(meal_plan).filter(
            meal_plan.date < date
        ).all()

    def delete_by_id(self, id: int) -> None:
        data = self.session.query(meal_plan).filter(
            meal_plan.id == id).one_or_none()

        if data:
            self.session.delete(data)
            self.session.commit()

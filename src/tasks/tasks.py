import logging
from datetime import datetime as dt
from datetime import timedelta
from src.sql.db_api import DB

db = DB()

def EventsCleaner():
    current_time = dt.now()
    events = db.events.get_older(current_time)

    for event in events:
        if current_time - event.time > timedelta(days=3):
            db.session.delete(event)
            db.images.delete_by_id(event.image_id)

    db.session.commit()


def MealCleaner():
    current_time = dt.now()
    meals = db.meal.get_older(current_time)

    for meal in meals:
        if current_time - meal.date > timedelta(days=3):
            print("Делит")
            db.session.delete(meal)

    db.session.commit()
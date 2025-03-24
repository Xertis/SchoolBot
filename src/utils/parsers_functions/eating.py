import io
import pandas as pd
from aiogram.utils.markdown import hbold, hunderline

EXPECTED_COLUMNS = ['Прием пищи', 'Раздел', '№ рец.', 'Блюдо', 'Выход, г', 'Цена', 'Калорийность', 'Белки', 'Жиры', 'Углеводы']


class eating_parser:
    @staticmethod
    def find_header_row(file_path):
        for i in range(25):
            df = pd.read_excel(file_path, header=i, nrows=1)
            if all(col in df.columns for col in EXPECTED_COLUMNS):
                return i
        return None

    @staticmethod
    def parse(file_path_or_content, date=None, is_path=True):
        eating_data = {}
        date = date if date else "2025-01-01"
        eating_data[date] = {}

        try:
            if not is_path:
                file_buffer = io.BytesIO(file_path_or_content)
                df = pd.read_excel(file_buffer, header=0)

            header_row = eating_parser.find_header_row(file_path_or_content)
            if header_row is None:
                raise ValueError("Заголовки столбцов не найдены в файле.")

            df = pd.read_excel(file_path_or_content, header=header_row)

            if not all(col in df.columns for col in EXPECTED_COLUMNS):
                raise ValueError(f"Столбцы в файле не соответствуют ожидаемым. Ожидаемые столбцы: {EXPECTED_COLUMNS}, полученные: {df.columns.tolist()}")

            current_meal = None
            current_price = None

            for index, row in df.iterrows():
                if pd.notna(row['Прием пищи']):
                    current_meal = row['Прием пищи']
                    eating_data[date][current_meal] = {'блюда': [], 'цена': None}

                if pd.notna(row['Цена']):
                    current_price = row['Цена']
                    if current_meal:
                        eating_data[date][current_meal]['цена'] = current_price

                dish_data = {
                    'Раздел': row['Раздел'] if pd.notna(row['Раздел']) else None,
                    '№ рец.': row['№ рец.'] if pd.notna(row['№ рец.']) else None,
                    'Блюдо': row['Блюдо'] if pd.notna(row['Блюдо']) else None,
                    'Выход, г': row['Выход, г'] if pd.notna(row['Выход, г']) else None,
                    'Калорийность': row['Калорийность'] if pd.notna(row['Калорийность']) else None,
                    'Белки': row['Белки'] if pd.notna(row['Белки']) else None,
                    'Жиры': row['Жиры'] if pd.notna(row['Жиры']) else None,
                    'Углеводы': row['Углеводы'] if pd.notna(row['Углеводы']) else None,
                }
                if current_meal:
                    eating_data[date][current_meal]['блюда'].append(dish_data)

        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return False

        return eating_data
    
    @staticmethod
    def parse_from_db(meals):
        eating_data = {}

        for meal in meals:
            meal_date = meal.date.strftime("%Y-%m-%d")

            if meal_date not in eating_data:
                eating_data[meal_date] = {}

            if meal.meal not in eating_data[meal_date]:
                eating_data[meal_date][meal.meal] = {'блюда': [], 'цена': None}

            dish_data = {
                'Раздел': meal.category,
                '№ рец.': meal.recipe,
                'Блюдо': meal.dish,
                'Выход, г': meal.grams,
                'Калорийность': None,
                'Белки': None,
                'Жиры': None,
                'Углеводы': None
            }
            eating_data[meal_date][meal.meal]['блюда'].append(dish_data)

            if meal.price is not None:
                eating_data[meal_date][meal.meal]['цена'] = float(meal.price)

        return eating_data

    @staticmethod
    def to_str(eating):
        result = ''

        for date, eating_data in eating.items():
            result += hunderline(f"Дата: {date}\n\n")
            for meal, data in eating_data.items():
                dishes = data['блюда']
                price = data['цена']
                result += hbold(f"🍽 {meal}:\n")
                for dish in dishes:
                    if dish["Раздел"] or dish['Блюдо']:
                        category = dish['Раздел'] if dish['Раздел'] else 'Общее'
                        dish_name = dish['Блюдо'] if dish['Блюдо'] else category
                        grams = dish['Выход, г'] if dish['Выход, г'] else '>0'
                        result += f"  - {dish_name} | ({category}, {grams} г.)\n"
                if price:
                    result += f"  💰 Цена: {price} руб.\n"
                result += "\n"
            result += "\n\n"
        return result

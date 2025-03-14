import csv
from src.utils.loader import LOADER
from aiogram.utils.markdown import hbold, hunderline

class eating_parser:
    @staticmethod
    def parse(file_path):
        eating_data = []

        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=',')
                for row in reader:
                    eating_data.append({
                        'День': row['День'],
                        'Название блюда': row['Название блюда'],
                        'Время приёма': row['Время приёма'],
                        'Цена': float(row['Цена']),
                        'Тип приёма пищи': row['Тип приёма пищи']
                    })
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")

        return eating_data
    
    @staticmethod
    def to_str(eating_data, time):
        table = [f"Дата последнего обновления питания: {time}"]

        for meal in eating_data:
            current_day = meal['День']
            table.append(f"\n{hunderline(current_day)}:\n")

            table.append(
                f"{hbold(meal['Тип приёма пищи'])}: {meal['Название блюда']}\n"
                f"⏰ {meal['Время приёма']} | 💰 {meal['Цена']} руб.\n"
            )

        return "\n".join(table)
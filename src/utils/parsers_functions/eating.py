import csv
import io
from aiogram.utils.markdown import hbold, hunderline


class eating_parser:
    @staticmethod
    def parse(file_path_or_content, is_path=True):
        eating_data = []

        try:
            file = None

            if is_path:
                file = open(file_path_or_content, mode='r', encoding='utf-8')
            else:
                file = io.StringIO(file_path_or_content)

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
            return False

        return eating_data

    @staticmethod
    def to_str(eating_data, time):
        table = [f"Дата последнего обновления питания: {time}"]
        i = 0
        while i < len(eating_data):
            current_day = eating_data[i]['День']
            table.append(f"\n{hunderline(current_day)}:\n")
            while i < len(
                    eating_data) and eating_data[i]['День'] == current_day:
                table.append(
                    f"{hbold(eating_data[i]['Тип приёма пищи'])}: {eating_data[i]['Название блюда']}\n"
                    f"⏰ {eating_data[i]['Время приёма']} | 💰 {eating_data[i]['Цена']} руб.\n")

                i += 1

        return "\n".join(table)

import io
import pandas as pd
from aiogram.utils.markdown import hbold, hunderline

get_digits = lambda x: ''.join([char for char in x if char.isdigit()])[:2]


class lessons_parser:
    @staticmethod
    def clean_class_name(class_name):
        if pd.isna(class_name) or class_name == " ":
            return None

        class_name = str(class_name).strip()
        digits = get_digits(class_name)
        first_letter = next((char.lower() for char in class_name if char.isalpha()), "")

        if not digits or not first_letter:
            return ''

        return f"{digits}{first_letter}"
    
    @staticmethod
    def clean_schedule(schedule):
        for day in schedule:
            for class_name in schedule[day]:

                schedule[day][class_name] = [teacher for teacher in schedule[day][class_name] if teacher]
        return schedule

    @staticmethod
    def parse(excel_file, is_path=True):
        try:
            if not is_path:
                file_buffer = io.BytesIO(excel_file)
                df = pd.read_excel(file_buffer, sheet_name="Расписание для учителей")
            else:
                df = pd.read_excel(excel_file, sheet_name="Расписание для учителей")

            schedule = {
                "Пн": {},
                "Вт": {},
                "Ср": {},
                "Чт": {},
                "Пт": {}
            }

            for index, row in df.iloc[2:].iterrows():
                teacher_name = row.iloc[0]
                if pd.isna(teacher_name):
                    continue


                for day_index, day in enumerate(["Пн", "Вт", "Ср", "Чт", "Пт"]):
                    start_col = 1 + day_index * 8

                    for lesson_index in range(8):
                        class_name = row.iloc[start_col + lesson_index]
                        cleaned_class_name = lessons_parser.clean_class_name(class_name)
                        if not cleaned_class_name:
                            continue

                        if cleaned_class_name not in schedule[day]:
                            schedule[day][cleaned_class_name] = [""] * 10

                        if schedule[day][cleaned_class_name][lesson_index]:
                            schedule[day][cleaned_class_name][lesson_index] += f"/{teacher_name}"
                        else:
                            schedule[day][cleaned_class_name][lesson_index] = teacher_name

            return lessons_parser.clean_schedule(schedule)
        except:
            return False
        
    @staticmethod
    def parse_from_db(lessons):
        schedule = {
            "Пн": {},
            "Вт": {},
            "Ср": {},
            "Чт": {},
            "Пт": {}
        }

        for lesson in lessons:
            weekday = lesson.weekday
            school_class = lesson.school_class
            number = lesson.lesson_number

            if school_class not in schedule[weekday]:
                schedule[weekday][school_class] = [""] * 10

            schedule[weekday][school_class][number] = lesson.lesson

        return schedule
    
    @staticmethod
    def to_str(lessons: dict, split_sign: str=''):
        res = ''

        for weekday, classes in lessons.items():
            if not classes:
                continue

            res += hunderline(f"{weekday}:\n\n")
            for school_class, class_lessons in classes.items():
                if int(get_digits(school_class)) < 5:
                    continue

                res += hbold(f"{school_class}:\n")
                for num, lesson in enumerate(class_lessons):
                    if lesson:
                        res += f"   {num}. {lesson}\n"
                res += "\n"
                res += split_sign
        if not res:
            return "😕 Расписание не найдено"

        return res        

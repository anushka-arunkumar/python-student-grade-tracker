import json
import re
from tabulate import tabulate

GRADE_RANGES = {
    "A": (90, 101),
    "B": (80, 90),
    "C": (70, 80),
    "D": (60, 70),
    "F": (0, 60),
}


def get_students():
    try:
        # with open("data/students.json", "r") as file:
        with open("data/invalid_student_data.json", "r") as file:
            return validate_student(json.load(file))
    except FileNotFoundError:
        print(f"Error: students.json not found")
        return []


def validate_student(student_list):
    valid_student_data = []
    valid_student_ids = set()
    for student in student_list:

        student_id = student["student_id"]
        if student_id in valid_student_ids:
            print(f"duplicate data received for student id {student_id}")
            continue

        is_id_valid = validate_id(student_id)
        if not is_id_valid:
            print(f"invalid id received for student {student}")
            continue

        is_name_valid = validate_name(student["name"])
        if not is_name_valid:
            print(f"invalid name received for student id {student['student_id']}")
            continue

        are_scores_valid = validate_scores(student["scores"])
        if not are_scores_valid:
            print(f"invalid score/s received for student id {student['student_id']}")
            continue

        valid_student_data.append(student)
        valid_student_ids.add(student_id)

    return valid_student_data


def validate_id(student_id):
    valid_id_pattern = r"^S\d{3}$"
    return student_id is not None and bool(re.match(valid_id_pattern, student_id))


def validate_name(name):
    name = name.strip()
    if not name:
        return False
    return all(char.isalpha() or char.isspace() for char in name)


def validate_scores(scores_dict):
    if not scores_dict:
        return False
    return all(
        score is not None and isinstance(score, (int, float)) and 0 <= score <= 100
        for score in scores_dict.values()
    )


def calculate_metrics(student_list):
    processed_students = []
    for student in student_list:

        total = sum(student["scores"].values())
        percentage = total / 5

        # this is a dictionary comprehension
        # it creates a new dictionary by looping over the scores dictionary
        subjects_grade = {
            subject: {"score": score, "grade": get_grade(score)}
            for subject, score in student["scores"].items()
        }

        processed_students.append(
            {
                **student,
                "scores": subjects_grade,
                "total": total,
                "percentage": percentage,
                "grade": get_grade(percentage),
            }
        )

    return get_rank(processed_students)


def get_grade(percentage):
    for grade, (low, high) in GRADE_RANGES.items():
        if low <= percentage < high:
            return grade


def get_rank(processed_students):
    students_sorted_by_percentage = sorted(
        processed_students, key=lambda student: student["percentage"], reverse=True
    )
    for index, student in enumerate(students_sorted_by_percentage):
        student["rank"] = index + 1
    return students_sorted_by_percentage


def generate_report_card(processed_students):
    headers = ["Subject", "Marks", "Grade"]
    for student in processed_students:
        data = []
        with open(
            f"report_cards/{student['student_id']}_{student['name'].replace(' ', '_')}.txt",
            "w",
        ) as file_obj:
            file_obj.write("=== Student Report Card ===\n\n")
            file_obj.write(f"Student ID: {student['student_id']}\n")
            file_obj.write(f"Name: {student['name']}\n\n")
            for subject, score in student["scores"].items():
                data.append([subject, score["score"], score["grade"]])
            file_obj.write(
                tabulate(
                    data,
                    headers=headers,
                    tablefmt="grid",
                    numalign="center",
                    stralign="center",
                )
            )
            file_obj.write(f"\n\nTotal: {student['total']}/500\n")
            file_obj.write(f"Percentage: {student['percentage']:.2f}%\n")
            file_obj.write(f"Grade: {student['grade']}\n")
            file_obj.write(f"Rank: {student['rank']}/{len(processed_students)}")
        print(f"report card generated for student_id {student['student_id']}")


students_list = get_students()
if not students_list:
    print("Student data is not available for processing")
else:
    processed_students = calculate_metrics(students_list)
    generate_report_card(processed_students)
    print(students_list)

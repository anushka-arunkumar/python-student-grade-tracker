from students_data import students
from students_extra import additional_students

percentage_ranges = {
    "A": (90, 100),
    "B": (80, 89),
    "C": (70, 79),
    "D": (60, 69),
    "F": (0, 59),
}


def add_students():
    students.extend(additional_students)


def calculate_metrics():
    for student in students:
        student["total"] = sum(student["scores"].values())
        percentage = student["total"] / 5
        student["percentage"] = percentage
        student["grade"] = get_grade(percentage)
    return get_rank()


def get_grade(percentage):
    for grade, (low, high) in percentage_ranges.items():
        if low <= percentage <= high:
            return grade

def get_rank():
    students_sorted_by_percentage = sorted(students, key = lambda student: student['percentage'])
    for index, student in enumerate(students_sorted_by_percentage):
        student["rank"] = f"{index + 1}/{len(students_sorted_by_percentage)}"
    return students_sorted_by_percentage

# add_students()
results = calculate_metrics()
print(results)

# {
#         "student_id": "S101",
#         "name": "Alice Johnson",
#         "scores": {
#             "Math": 92,
#             "Science": 88,
#             "English": 95,
#             "History": 85,
#             "Geography": 90,
#         },
#     }

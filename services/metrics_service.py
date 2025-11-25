from utils.helpers import GRADE_RANGES


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

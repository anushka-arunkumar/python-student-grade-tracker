import json
from .validators import validate_id, validate_name, validate_subjects, validate_scores


def load_students():
    """Reads students.json and returns list of valid students."""
    try:
        with open("data/students.json", "r") as file:
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
            print(f"Duplicate data received for student ID {student_id}")
            continue

        is_id_valid = validate_id(student_id)
        if not is_id_valid:
            print(f"Invalid ID received for student {student}")
            continue

        is_name_valid = validate_name(student["name"])
        if not is_name_valid:
            print(f"Invalid name received for student {student['student_id']}")
            continue

        are_subjects_valid = validate_subjects(student["scores"])
        if not are_subjects_valid:
            continue

        are_scores_valid = validate_scores(student["scores"])
        if not are_scores_valid:
            print(f"Invalid score/s received for student {student['student_id']}")
            continue

        valid_student_data.append(student)
        valid_student_ids.add(student_id)

    return valid_student_data

def find_by_student_id(student_id, processed_students):
    if not student_id:
        return None

    student_id = student_id.strip().upper()

    return next(
        (
            student
            for student in processed_students
            if student["student_id"] == student_id
        ),
        None,
    )


def find_by_name(name, processed_students):
    if not name:
        return None

    name = name.strip().lower()

    return next(
        (student for student in processed_students if student["name"].lower() == name),
        None,
    )


def filter_by_grade(grade, processed_students):
    if not grade:
        return []

    grade = grade.strip().upper()

    return [student for student in processed_students if student["grade"] == grade]


def get_top_n_students(n, processed_students):
    if not n or n <= 0:
        return []

    return processed_students[:n]

import pprint


def find_by_student_id(student_id, processed_students):
    """
    Returns the student dictionary that matches the given student_id.

    Returns:
        dict | None: The matching student if found, else None.

    :param student_id (str): ID of the student to search for.
    :param processed_students (list[dict]): List of student records.
    """

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
    """
    Returns the student dictionary that matches the given student name.

    :param name (str): name of the student to search for.
    :param processed_students (list[dict]): List of student records.

    Returns:
        dict | None: The matching student if found, else None.
    """

    if not name:
        return None

    name = name.strip().lower()

    return next(
        (student for student in processed_students if student["name"].lower() == name),
        None,
    )


def filter_by_grade(grade, processed_students):
    """
    Filter and return all students who have the specified grade.

    :param grade (str): The grade to filter by (e.g., "A", "B", "C", "D", "F").
    :param processed_students (list[dict]): List of student records.

    Returns:
        list of students with the specified grade | []: when no students with specified grade found
    """

    if not grade:
        return []

    grade = grade.strip().upper()

    return [student for student in processed_students if student["grade"] == grade]


def get_top_n_students(n, processed_students):
    for student in processed_students[:n]:
        pprint.pprint(student)

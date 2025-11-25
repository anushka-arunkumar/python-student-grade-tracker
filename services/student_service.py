import pprint


def find_by_student_id(student_id, processed_students):
    return next(
        (
            student
            for student in processed_students
            if student["student_id"] == student_id
        ),
        None,
    )


def find_by_name(name, processed_students):
    return next(
        (
            student
            for student in processed_students
            if student["name"].lower() == name.lower()
        ),
        None,
    )


def filter_by_grade(grade, processed_students):
    student_list = list(
        filter(lambda student: student["grade"] == grade, processed_students)
    )
    if not student_list:
        print(f"None of the students scored a {grade} grade")
        return
    pprint.pprint(student_list)


def get_top_n_students(n, processed_students):
    for student in processed_students[:n]:
        pprint.pprint(student)

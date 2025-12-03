from .metrics_service import calculate_metrics


def update_student(student_id, students_list, updated_data):
    student_id = student_id.strip().upper()

    idx = next(
        (
            index
            for index, student in enumerate(students_list)
            if student["student_id"] == student_id
        ),
        None,
    )

    if idx is None:
        return None, None

    student = students_list[idx]

    for key, value in updated_data.items():
        if key == "scores":
            for sub, new_score in value.items():
                if sub in student["scores"]:
                    student["scores"][sub] = new_score
        else:
            student[key] = value

    students_list[idx] = student

    updated_processed_students = calculate_metrics(students_list)

    return students_list, updated_processed_students


def delete_student(student_id, students_list):
    idx = next(
        (
            index
            for index, student in enumerate(students_list)
            if student["student_id"].upper() == student_id
        ),
        None,
    )

    if idx is None:
        return None, None

    del students_list[idx]

    updated_processed_students = calculate_metrics(students_list)

    return students_list, updated_processed_students

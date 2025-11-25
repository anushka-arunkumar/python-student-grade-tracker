from utils.helpers import SUBJECTS
from .metrics_service import calculate_metrics
from utils.validators import validate_name, validate_score
from ui.display import show_student


def update_student(student_id, students_list):
    index = next(
        index
        for index, student in enumerate(students_list)
        if student["student_id"] == student_id
    )
    student_to_update = students_list[index]

    show_student(student_to_update)

    updated_student, changes = get_updated_details(student_to_update)

    if changes:
        print("\nYou are about to update the following fields:\n")
        for field in changes:
            old_val = changes[field]["old"]
            new_val = changes[field]["new"]
            print(f"{field}: {old_val} -> {new_val}")
    else:
        print("\nNo changes detected. Nothing to update.")
        return None, None

    confirm = input("\nConfirm update? (y/n): ").lower()
    if confirm not in ["yes", "y"]:
        print("Update cancelled")
        return None, None
    students_list[index] = updated_student
    print(f"\nStudent {student_id} updated successfully!")
    print("Recalculating metrics....")

    updated_processed_students = calculate_metrics(students_list)
    print("Update complete!")

    return students_list, updated_processed_students


def get_updated_details(student):
    updated_student = {
        "student_id": student["student_id"],
        "name": student["name"],
        "scores": {},
    }
    changes = {}

    while True:
        new_name = input(
            f"Enter new name (press Enter to keep '{student["name"]}'): "
        ).strip()

        if not new_name:
            break
        if validate_name(new_name):
            updated_student["name"] = new_name
            changes["name"] = {"old": student["name"], "new": new_name}
            break
        print("Invalid name. Please try again")

    for subject in SUBJECTS:
        old_score = student["scores"][subject]

        while True:
            new_score = input(
                f"Enter new {subject} score (press Enter to keep {old_score}):"
            ).strip()

            if new_score:
                if validate_score(new_score):
                    updated_student["scores"][subject] = int(new_score)
                    changes[subject] = {
                        "old": old_score,
                        "new": int(new_score),
                    }
                    break
                else:
                    print("Invalid score. Please try again")
            else:
                updated_student["scores"][subject] = old_score
                break

    return updated_student, changes


def delete_student(student_id, students_list):
    confirmation = input(
        f"Do you really want to delete student {student_id} ? (yes/no) "
    ).lower()
    if confirmation not in ["yes", "y"]:
        return None, None
    updated_students_list = [
        student for student in students_list if student["student_id"] != student_id
    ]
    updated_processed_students = calculate_metrics(updated_students_list)
    print(f"\nTotal number of students before deletion: {len(students_list)}\n")
    print(f"Student {student_id} was successfully deleted\n")
    print(f"Total number of students post deletion: {len(updated_students_list)}\n")
    return updated_students_list, updated_processed_students

import os
from tabulate import tabulate
from services.student_service import find_by_student_id


def generate_report_card(student_id, processed_students):

    student = find_by_student_id(student_id, processed_students)

    if not student:
        print(f"\nStudent '{student_id}' not found. Cannot generate report card.\n")
        return

    base_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "report_cards"
    )
    os.makedirs(base_dir, exist_ok=True)
    file_path = os.path.join(
        base_dir,
        f"{student["student_id"]}_{student["name"].replace(" ", "_")}.txt",
    )

    table_data = [
        [subject, details["score"], details["grade"]]
        for subject, details in student["scores"].items()
    ]

    summary_text = (
        f"Report Card for {student['name']} ({student['student_id']})\n\n"
        f"Total Score: {student['total']}\n"
        f"Percentage: {student['percentage']}\n"
        f"Final Grade: {student['grade']}\n"
        f"Class Rank: {student['rank']}\n"
    )

    with open(file_path, "w") as file:
        file.write(summary_text)
        file.write("\nSubject Scores:\n\n")
        file.write(
            tabulate(
                table_data,
                headers=["Subject", "Score", "Grade"],
                tablefmt="grid",
                numalign="center",
                stralign="center",
            )
        )

    print(f"\nReport card generated successfully:")
    print(f"File: {file_path}\n")

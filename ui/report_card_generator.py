from services.student_service import find_by_student_id
from tabulate import tabulate


def generate_report_card(student_id, processed_students):

    student = find_by_student_id(student_id, processed_students)
    if not student:
        print(f"Student {student_id} not found")
        return

    headers = ["Subject", "Marks", "Grade"]
    data = []
    with open(
        f"data/report_cards/{student['student_id']}_{student['name'].replace(' ', '_')}.txt",
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
    print(f"Report card generated for student {student['student_id']}")

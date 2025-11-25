from services.student_service import (
    find_by_student_id,
    find_by_name,
    get_top_n_students,
    filter_by_grade,
)
from services.statistics_service import get_class_statistics
from services.update_delete_service import update_student, delete_student
from services.metrics_service import calculate_metrics
from utils.file_io import load_students
from ui.display import *
from ui.report_card_generator import generate_report_card


def get_user_choice():
    print("\n==== Features Menu ====\n")
    print("1. Search student by ID")
    print("2. Search student by name")
    print("3. Filter by grade")
    print("4. Show top N students")
    print("5. Generate report card for individual student")
    print("6. Class statistics")
    print("7. Subject wise analysis")
    print("8. View all students")
    print("9. Update student by ID")
    print("10. Delete student by ID\n")
    while True:
        choice = input("Choose an option: ")
        if choice.isdigit() and 1 <= int(choice) <= 10:
            return int(choice)
        print("Invalid input. Please enter a number between 1 and 10.")


def advanced_features(user_choice, processed_students, students_list):
    match user_choice:

        case 1:
            student_id = input("Enter student ID: ")
            student = find_by_student_id(student_id, processed_students)
            (print(student) if student else print(f"Student {student_id} not found"))
            return None, None

        case 2:
            name = input("Enter a name: ")
            student = find_by_name(name, processed_students)
            print(student) if student else print(f"Student with name {name} not found")
            return None, None

        case 3:
            while True:
                grade = input("Enter the grade (A/B/C/D/F) to filter by: ").upper()
                if grade in ["A", "B", "C", "D", "F"]:
                    break
                print("Invalid grade")
            filter_by_grade(grade, processed_students)
            return None, None

        case 4:
            while True:
                n = input("Enter the number of top-ranked students you want to view: ")
                if n.isdigit() and int(n) in range(1, len(processed_students) + 1):
                    break
                print(
                    f"Invalid input. Enter a number between 1 to {len(processed_students)}"
                )
            get_top_n_students(int(n), processed_students)
            return None, None

        case 5:
            student_id = input("Enter student ID for generating report card: ")
            generate_report_card(student_id, processed_students)
            return None, None

        case 6:
            get_class_statistics(processed_students)
            return None, None

        case 7:
            show_subject_analysis(processed_students)
            return None, None

        case 8:
            show_students_list(processed_students)
            return None, None

        case 9:
            student_id = input("Enter the Student ID you want to update: ")
            if not find_by_student_id(student_id, processed_students):
                print(f"Student ID {student_id} not found. Please try again")
                return None, None
            return update_student(student_id, students_list)

        case 10:
            student_id = input("Enter the Student ID you want to delete: ")
            if not find_by_student_id(student_id, processed_students):
                print(f"Student ID {student_id} not found. Please try again")
                return None, None
            return delete_student(student_id, students_list)

        case _:
            print("Invalid choice. Enter a number between 1 to 10")
            return None, None


def run_app():
    """Main UI loop (replaces main())."""
    students_list = load_students()
    if not students_list:
        print("Student data is not available for processing")
    else:
        processed_students = calculate_metrics(students_list)
        while True:
            user_choice = get_user_choice()

            updated_students_list, updated_processed_students = advanced_features(
                user_choice, processed_students, students_list
            )

            if updated_students_list and updated_processed_students:
                students_list = updated_students_list
                processed_students = updated_processed_students

            conti = input("Do you want to continue exploring ? (yes/no) ").lower()
            if conti not in ["yes", "y"]:
                break

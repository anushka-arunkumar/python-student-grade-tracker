from services.student_service import (
    find_by_student_id,
    find_by_name,
    get_top_n_students,
    filter_by_grade,
)
from services.statistics_service import (
    get_per_subject_avg,
    get_min_max_score_per_subject,
    get_easiest_hardest_subject,
    get_class_statistics,
)
from services.update_delete_service import update_student, delete_student
from services.metrics_service import calculate_metrics
from utils.file_io import load_students
from utils.config import GRADES
from utils.validators import validate_id, validate_name, validate_score
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
            student_id = input("Enter student ID: ").strip().upper()
            if validate_id(student_id):
                student = find_by_student_id(student_id, processed_students)
                show_student_search_result(student, student_id)
            else:
                print("Invalid student ID")
            return None, None

        case 2:
            name = input("Enter student name: ").strip().lower()
            if validate_name(name):
                student = find_by_name(name, processed_students)
                show_student_search_by_name(student, name)
            else:
                print("Invalid name")
            return None, None

        case 3:
            grade = input("Enter the grade (A/B/C/D/F) to filter by: ").strip().upper()
            if grade in GRADES:
                students = filter_by_grade(grade, processed_students)
                show_students_by_grade(students, grade)
            else:
                print("Invalid grade")
            return None, None

        case 4:
            n = input("Enter the number of top-ranked students to view: ")
            if not n.isdigit():
                print("Invalid input. Please enter a positive number.")
                return None, None

            n = int(n)
            if n < 1 or n > len(processed_students):
                print(
                    f"Invalid range. Enter a number between 1 and {len(processed_students)}."
                )
                return None, None

            students = get_top_n_students(n, processed_students)
            show_top_n_students(students, n)
            return None, None

        case 5:
            student_id = input("Enter student ID for generating report card: ")
            generate_report_card(student_id, processed_students)
            return None, None

        case 6:
            stats = get_class_statistics(processed_students)
            show_class_statistics(stats)
            return None, None

        case 7:
            averages = get_per_subject_avg(processed_students, SUBJECTS)
            min_max = get_min_max_score_per_subject(processed_students, SUBJECTS)
            easiest_hardest = get_easiest_hardest_subject(processed_students, SUBJECTS)

            show_subject_averages(averages)
            show_subject_min_max(min_max)
            show_easiest_hardest_subject(easiest_hardest)

            return None, None

        case 8:
            show_students_list(processed_students)
            return None, None

        case 9:
            student_id = input("Enter the student ID to update: ").strip().upper()

            if not validate_id(student_id):
                print("Invalid student ID format")
                return None, None

            student = find_by_student_id(student_id, processed_students)
            if not student:
                print(f"Student '{student_id}' does not exist")
                return None, None

            print("\nEnter new values (leave blank to keep existing):\n")

            updated_data = {}

            # Name
            new_name = input(f"Name ({student['name']}): ").strip()
            if new_name:
                updated_data["name"] = new_name

            # Scores (per subject)
            new_scores = {}
            for subject, details in student["scores"].items():
                curr_score = details["score"]
                new_val = input(f"{subject} Score ({curr_score}): ").strip()

                if new_val:
                    if not validate_score(new_val):
                        print(f"Invalid score for {subject}. Update skipped.")
                        continue

                    score = int(new_val)
                    new_scores[subject] = score

            if new_scores:
                updated_data["scores"] = new_scores

            if not updated_data:
                print("\nNo changes entered. Nothing updated\n")
                return None, None

            updated_students_list, updated_processed_students = update_student(
                student_id, students_list, updated_data
            )
            show_update_result(
                find_by_student_id(student_id, updated_processed_students), student_id
            )
            return updated_students_list, updated_processed_students

        case 10:
            student_id = input("Enter student ID to delete: ").strip().upper()

            if not validate_id(student_id):
                print("Invalid student ID format")
                return None, None

            updated_students_list, updated_processed_students = delete_student(
                student_id, students_list
            )

            if updated_students_list is None:
                show_delete_result(student_id, False)
                return None, None

            show_delete_result(student_id, True)

            return updated_students_list, updated_processed_students

        case _:
            print("Invalid choice. Enter a number between 1 to 10")
            return None, None


def run_app():

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

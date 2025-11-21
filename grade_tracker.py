import json
import re
import pprint
import statistics
from tabulate import tabulate
from collections import Counter

GRADE_RANGES = {
    "A": (90, 101),
    "B": (80, 90),
    "C": (70, 80),
    "D": (60, 70),
    "F": (0, 60),
}

SUBJECTS = ["Math", "Science", "English", "History", "Geography"]


def get_students():
    try:
        with open("data/students.json", "r") as file:
            # with open("data/invalid_student_data.json", "r") as file:
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
            print(f"duplicate data received for student id {student_id}")
            continue

        is_id_valid = validate_id(student_id)
        if not is_id_valid:
            print(f"invalid id received for student {student}")
            continue

        is_name_valid = validate_name(student["name"])
        if not is_name_valid:
            print(f"invalid name received for student id {student['student_id']}")
            continue

        are_subjects_valid = validate_subjects(student["scores"])
        if not are_subjects_valid:
            continue

        are_scores_valid = validate_scores(student["scores"])
        if not are_scores_valid:
            print(f"invalid score/s received for student id {student['student_id']}")
            continue

        valid_student_data.append(student)
        valid_student_ids.add(student_id)

    return valid_student_data


def validate_id(student_id):
    valid_id_pattern = r"^S\d{3}$"
    return student_id is not None and bool(re.match(valid_id_pattern, student_id))


def validate_name(name):
    name = name.strip()
    if not name:
        return False
    return all(char.isalpha() or char.isspace() for char in name)


def validate_subjects(scores_dict):
    if len(scores_dict) != len(SUBJECTS):
        print("incorrect number of subjects")
        return False
    if set(scores_dict.keys()) != set(SUBJECTS):
        print("missing or extra subjects")
        return False
    return True


def validate_scores(scores_dict):
    if not scores_dict:
        return False
    return all(
        score is not None and isinstance(score, (int, float)) and 0 <= score <= 100
        for score in scores_dict.values()
    )


def calculate_metrics(student_list):
    processed_students = []
    for student in student_list:

        total = sum(student["scores"].values())
        percentage = total / 5

        # this is a dictionary comprehension
        # it creates a new dictionary by looping over the scores dictionary
        subjects_grade = {
            subject: {"score": score, "grade": get_grade(score)}
            for subject, score in student["scores"].items()
        }

        processed_students.append(
            {
                **student,
                "scores": subjects_grade,
                "total": total,
                "percentage": percentage,
                "grade": get_grade(percentage),
            }
        )

    return get_rank(processed_students)


def get_grade(percentage):
    for grade, (low, high) in GRADE_RANGES.items():
        if low <= percentage < high:
            return grade


def get_rank(processed_students):
    students_sorted_by_percentage = sorted(
        processed_students, key=lambda student: student["percentage"], reverse=True
    )
    for index, student in enumerate(students_sorted_by_percentage):
        student["rank"] = index + 1
    return students_sorted_by_percentage


def view_all_students(processed_students):
    print("\n==== ALL STUDENTS ====\n")
    for student in processed_students:
        pprint.pprint(student)


def generate_report_card(student_id, processed_students):

    student = find_by_student_id(student_id, processed_students)
    if not student:
        print(f"Student with id {student_id} not found")
        return

    headers = ["Subject", "Marks", "Grade"]
    data = []
    with open(
        f"report_cards/{student['student_id']}_{student['name'].replace(' ', '_')}.txt",
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
    print(f"report card generated for student_id {student['student_id']}")


def get_user_choice():
    print("==== Features Menu ====\n")
    print("1. Search student by ID")
    print("2. Search student by name")
    print("3. Filter by grade")
    print("4. Show top N students")
    print("5. Generate report card for individual student")
    print("6. Class statistics")
    print("7. Subject wise analysis")
    print("8. View all students\n")
    while True:
        choice = input("Choose an option: ")
        if choice.isdigit() and 1 <= int(choice) <= 8:
            return int(choice)
        print("Invalid input. Please enter a number between 1 and 8.")


def advanced_features(user_choice, processed_students):
    match user_choice:

        case 1:
            student_id = input("Enter a student id: ")
            student = find_by_student_id(student_id, processed_students)
            (
                print(student)
                if student
                else print(f"Student with id {student_id} not found")
            )

        case 2:
            name = input("Enter a name: ")
            student = find_by_name(name, processed_students)
            print(student) if student else print(f"Student with name {name} not found")

        case 3:
            while True:
                grade = input("Enter the grade (A/B/C/D/F) to filter by: ").upper()
                if grade in ["A", "B", "C", "D", "F"]:
                    break
                print("Invalid grade")
            filter_by_grade(grade, processed_students)

        case 4:
            while True:
                n = input("Enter the number of top-ranked students you want to view: ")
                if n.isdigit() and int(n) in range(1, len(processed_students) + 1):
                    break
                print(
                    f"Invalid input. Enter a number between 1 to {len(processed_students)}"
                )
            get_top_n_students(int(n), processed_students)

        case 5:
            student_id = input("Enter student id for generating report card: ")
            generate_report_card(student_id, processed_students)

        case 6:
            get_class_statistics(processed_students)

        case 7:
            subject_wise_analysis(processed_students)

        case 8:
            view_all_students(processed_students)

        case _:
            print("Invalid choice. Enter a number between 1 to 8")


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


def get_top_n_students(n, processed_students):
    for student in processed_students[:n]:
        pprint.pprint(student)


def filter_by_grade(grade, processed_students):
    student_list = list(
        filter(lambda student: student["grade"] == grade, processed_students)
    )
    if not student_list:
        print(f"None of the students scored a {grade} grade")
        return
    pprint.pprint(student_list)


def get_class_statistics(processed_students):

    class_avg_percentage = get_class_avg_percentage(processed_students)
    pass_cnt, fail_cnt = get_pass_fail_counts(processed_students)
    grade_distribution = get_grade_distribution(processed_students)

    print("==== Class Statistics ====\n")
    print(f"Class average percentage: {class_avg_percentage:.2f}%\n")

    cnt_header = ["Result", "Count"]
    cnt_data = [["Pass", pass_cnt], ["Fail", fail_cnt]]
    print("Pass/Fail Count:")
    print(
        tabulate(
            cnt_data,
            headers=cnt_header,
            tablefmt="grid",
            stralign="center",
            numalign="center",
        ),
        "\n",
    )

    grd_header = ["Grade", "Count"]
    grd_data = []
    for grade, cnt in grade_distribution.items():
        grd_data.append([grade, cnt])
    print("Grade Distribution:")
    print(
        tabulate(
            grd_data,
            headers=grd_header,
            tablefmt="grid",
            stralign="center",
            numalign="center",
        )
    )


def get_class_avg_percentage(processed_students):
    percentage_list = [student["percentage"] for student in processed_students]
    return round(statistics.mean(percentage_list), 2)


def get_pass_fail_counts(processed_students):
    # pass/fail count (passing: 40% in each subject and 50% overall)
    pass_cnt = sum(
        1
        for student in processed_students
        if student["percentage"] >= 50
        and all(score["score"] >= 40 for score in student["scores"].values())
    )
    fail_cnt = len(processed_students) - pass_cnt
    return pass_cnt, fail_cnt


def get_grade_distribution(processed_students):
    return Counter(student["grade"] for student in processed_students)


def subject_wise_analysis(processed_students):
    print("\n==== Subject Wise Analysis ====\n")

    print("Average score for each subject: \n")
    pprint.pprint(get_per_subject_avg(processed_students))
    print()

    print("Highest and lowest score per subject: \n")
    pprint.pprint(get_min_max_score_per_sub(processed_students))
    print()


# Subject with best class performance


def get_per_subject_avg(processed_students):
    per_sub_avg = {}
    for subject in SUBJECTS:
        scores_list = [
            student["scores"][subject]["score"] for student in processed_students
        ]
        per_sub_avg[subject] = round(statistics.mean(scores_list), 2)
    return per_sub_avg


def get_min_max_score_per_sub(processed_students):
    min_max_scores = {}
    for subject in SUBJECTS:
        scores = [student["scores"][subject]["score"] for student in processed_students]
        min_max_scores[subject] = {
            "min_score": min(scores),
            "min_scorer": [
                s["name"]
                for s in processed_students
                if s["scores"][subject]["score"] == min(scores)
            ],
            "max_score": max(scores),
            "max_scorer": [
                s["name"]
                for s in processed_students
                if s["scores"][subject]["score"] == max(scores)
            ],
        }
    return min_max_scores


students_list = get_students()
if not students_list:
    print("Student data is not available for processing")
else:
    processed_students = calculate_metrics(students_list)
    while True:
        user_choice = get_user_choice()
        advanced_features(user_choice, processed_students)
        conti = input("Do you want to continue exploring ? (yes/no) ").lower()
        if conti not in ["yes", "y"]:
            break


# Update Student

# Create update_student() function
# Find student by ID
# Allow updating name and scores
# Recalculate metrics after update

# Delete Student

# Create delete_student() function
# Find student by ID
# Ask for confirmation
# Remove from list
# Recalculate ranks
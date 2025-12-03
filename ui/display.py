from utils.config import SUBJECTS
from pprint import pprint


def show_student_search_result(student, student_id):
    if student:
        print("\n=== Student Found ===\n")
        pprint(student)
    else:
        print(f"\nStudent with ID '{student_id}' not found")


def show_student_search_by_name(student, student_name):
    if student:
        print("\n=== Student Found ===\n")
        pprint(student)
    else:
        print(f"\nStudent with name '{student_name}' not found")


def show_students_by_grade(students, grade):
    print(f"\n=== Students with Grade '{grade}' ===\n")

    if not students:
        print(f"Students with grade {grade} not found\n")
        return

    for student in students:
        pprint(student)
    print()


def show_top_n_students(students, n):
    if not students:
        print(f"\nNo results. Unable to show top {n} students.\n")
        return

    print(f"\n=== Top {n} Students ===\n")
    for student in students:
        pprint(student)
        print()


def show_student(student):
    print(f"\nCurrent details for student {student['student_id']}:")
    print(f"Name: {student['name']}")
    for subject in SUBJECTS:
        print(f"{subject}: {student['scores'][subject]}")


def show_students_list(students):
    print("\n==== ALL STUDENTS ====\n")
    for student in students:
        pprint(student)


def show_class_statistics(stats):
    print("\n======= CLASS STATISTICS =======\n")
    print(f"Class Average Percentage : {stats["average_percentage"]}%")
    print(f"Pass Count               : {stats["pass_count"]}")
    print(f"Fail Count               : {stats["fail_count"]}")
    print("\nGrade Distribution:")

    for grade, count in stats["grade_distribution"].items():
        print(f"  {grade} : {count}")

    print()


def show_subject_averages(averages):
    print("\n==== Subject-wise Averages ====\n")
    for subject, average in averages.items():
        print(f"{subject:12}: {average}")
    print()


def show_subject_min_max(stats):
    print("\n==== Subject Min/Max Scores ====\n")
    for subject, min_max in stats.items():
        print(f"{subject:12}: Min = {min_max['min']}, Max = {min_max['max']}")
    print()


def show_easiest_hardest_subject(result):
    print("\n==== Easiest / Hardest Subject ====\n")

    easiest = result["easiest"]
    hardest = result["hardest"]

    print(f"Easiest Subject : {easiest['subject']} (Avg {easiest['average']})")
    print(f"Hardest Subject : {hardest['subject']} (Avg {hardest['average']})")

    print()


def show_update_result(student, student_id):
    if not student:
        print(f"\nStudent '{student_id}' not found. Update failed\n")
    else:
        print("\nStudent updated successfully:\n")
        pprint(student)
        print()


def show_delete_result(student_id, success):
    if success:
        print(f"\nStudent '{student_id}' deleted successfully\n")
    else:
        print(f"\nStudent '{student_id}' not found. Nothing deleted\n")

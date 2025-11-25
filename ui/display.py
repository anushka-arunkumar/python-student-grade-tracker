from utils.helpers import SUBJECTS
from services.statistics_service import (
    get_class_avg_percentage,
    get_pass_fail_counts,
    get_grade_distribution,
    get_min_max_score_per_sub,
    get_per_subject_avg,
    get_easiest_hardest_subject
)
from pprint import pprint
from tabulate import tabulate


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

    class_avg_percentage = get_class_avg_percentage(stats)
    pass_cnt, fail_cnt = get_pass_fail_counts(stats)
    grade_distribution = get_grade_distribution(stats)

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


def show_subject_analysis(data):
    print("\n==== Subject Wise Analysis ====\n")

    print("Average score for each subject: \n")
    pprint(get_per_subject_avg(data))
    print()

    print("Highest and lowest score per subject: \n")
    pprint(get_min_max_score_per_sub(data))
    print()

    print("Easiest subject (highest avg) and hardest subject (lowest avg): \n")
    subjects = get_easiest_hardest_subject(data)
    pprint(subjects)
    print()

import pprint
import statistics
from tabulate import tabulate
from collections import Counter
from utils.helpers import SUBJECTS


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

    print("Easiest subject (highest avg) and hardest subject (lowest avg): \n")
    subjects = get_easiest_hardest_subject(processed_students)
    pprint.pprint(subjects)
    print()


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
        min_score = min(scores)
        max_score = max(scores)
        min_max_scores[subject] = {
            "min_score": min_score,
            "min_scorer": [
                s["name"]
                for s in processed_students
                if s["scores"][subject]["score"] == min_score
            ],
            "max_score": max_score,
            "max_scorer": [
                s["name"]
                for s in processed_students
                if s["scores"][subject]["score"] == max_score
            ],
        }
    return min_max_scores


def get_easiest_hardest_subject(processed_students):

    # Identify easiest subject (highest avg) and hardest subject (lowest avg)
    subjects = {}
    avg = get_per_subject_avg(processed_students)
    easiest_subject = max(avg, key=avg.get)
    hardest_subject = min(avg, key=avg.get)
    subjects["easiest_subject"] = {
        "subject": easiest_subject,
        "average": avg[easiest_subject],
    }
    subjects["hardest_subject"] = {
        "subject": hardest_subject,
        "average": avg[hardest_subject],
    }
    return subjects

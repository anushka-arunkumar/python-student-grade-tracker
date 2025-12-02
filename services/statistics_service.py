from collections import Counter
from utils.config import PASSING_PERCENTAGE, PASSING_SUBJECT_SCORE


def get_class_statistics(processed_students):

    avg_percentage = get_class_avg_percentage(processed_students)
    pass_cnt, fail_cnt = get_pass_fail_counts(processed_students)
    grade_distribution = get_grade_distribution(processed_students)

    return {
        "average_percentage": avg_percentage,
        "pass_count": pass_cnt,
        "fail_count": fail_cnt,
        "grade_distribution": grade_distribution,
    }


def get_class_avg_percentage(processed_students):
    if not processed_students:
        return 0.0

    total_percentage = sum(student["percentage"] for student in processed_students)
    return round(total_percentage / len(processed_students), 2)


def get_pass_fail_counts(processed_students):
    pass_cnt = sum(
        1
        for student in processed_students
        if student["percentage"] >= PASSING_PERCENTAGE
        and all(
            score["score"] >= PASSING_SUBJECT_SCORE
            for score in student["scores"].values()
        )
    )
    fail_cnt = len(processed_students) - pass_cnt
    return pass_cnt, fail_cnt


def get_grade_distribution(processed_students):
    return Counter(student["grade"] for student in processed_students)


def get_per_subject_avg(processed_students, subjects):
    """
    Returns a dict: {subject: average_score}
    """
    if not processed_students:
        return {subject: 0 for subject in subjects}

    averages = {}

    for subject in subjects:
        scores = [student["scores"][subject]["score"] for student in processed_students]
        averages[subject] = round(sum(scores) / len(scores), 2)

    return averages


def get_min_max_score_per_subject(processed_students, subjects):
    """
    Returns a dict:
    {
        subject: {"min": X, "max": Y}
    }
    """
    results = {}

    for subject in subjects:
        scores = [student["scores"][subject]["score"] for student in processed_students]
        results[subject] = {"min": min(scores), "max": max(scores)}

    return results


def get_easiest_hardest_subject(processed_students, subjects):
    """
    Returns:
    {
        "easiest": {"subject": S, "average": A},
        "hardest": {"subject": S, "average": A}
    }
    """
    averages = get_per_subject_avg(processed_students, subjects)
    easiest = max(averages, key=averages.get)
    hardest = min(averages, key=averages.get)
    return {
        "easiest": {"subject": easiest, "average": averages[easiest]},
        "hardest": {"subject": hardest, "average": averages[hardest]},
    }

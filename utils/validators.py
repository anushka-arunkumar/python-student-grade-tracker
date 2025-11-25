import re
from .helpers import SUBJECTS


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
        print("Incorrect number of subjects")
        return False
    if set(scores_dict.keys()) != set(SUBJECTS):
        print("Missing or extra subjects")
        return False
    return True


def validate_scores(scores_dict):
    if not scores_dict:
        return False
    return all(
        score is not None and isinstance(score, (int, float)) and 0 <= score <= 100
        for score in scores_dict.values()
    )


def validate_score(score):
    return score.isdigit() and 0 <= int(score) <= 100

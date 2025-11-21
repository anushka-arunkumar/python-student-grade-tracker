import json
import statistics
from collections import defaultdict, Counter
from tabulate import tabulate

with open("data/processed_students.json", "r") as file:
    processed_students = json.load(file)

max_min_scores = {}
for subject in ["Math", "Science", "English", "History", "Geography"]:
    scores_list = [student["scores"][subject]["score"] for student in processed_students]
    max_min_scores[subject] = {"max": max(scores_list), "min": min(scores_list)}

print(max_min_scores)

# print(Counter(student["grade"] for student in processed_students))

# groups = defaultdict(list)
# for student in processed_students:
#     groups[student["grade"]].append(student["student_id"])

# headers = ["grade", "student count"]
# data = []

# for grade, stud_id in groups.items():
#     data.append([grade, len(stud_id)])

# print(tabulate(data, headers=headers))

# print(type(groups), groups)

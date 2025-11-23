import json
import statistics
from collections import defaultdict, Counter
from tabulate import tabulate
import pprint

with open("data/processed_students.json", "r") as file:
    processed_students = json.load(file)

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

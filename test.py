s =[
    {
        "student_id": "S101",
        "name": "Alice Johnson",
        "scores": {
            "Math": 92,
            "Science": 88,
            "English": 95,
            "History": 85,
            "Geography": 90,
        },
        "total": 450,
        "percentage": 90.0,
        "grade": "A",
    },
    {
        "student_id": "S102",
        "name": "Brian Smith",
        "scores": {
            "Math": 45,
            "Science": 52,
            "English": 48,
            "History": 39,
            "Geography": 50,
        },
        "total": 234,
        "percentage": 46.8,
        "grade": "F",
    },
    {
        "student_id": "S103",
        "name": "Catherine Lee",
        "scores": {
            "Math": 88,
            "Science": 91,
            "English": 87,
            "History": 90,
            "Geography": 85,
        },
        "total": 441,
        "percentage": 88.2,
        "grade": "B",
    },
    {
        "student_id": "S104",
        "name": "David Kumar",
        "scores": {
            "Math": 33,
            "Science": 40,
            "English": 28,
            "History": 36,
            "Geography": 41,
        },
        "total": 178,
        "percentage": 35.6,
        "grade": "F",
    },
    {
        "student_id": "S105",
        "name": "Emma Wilson",
        "scores": {
            "Math": 72,
            "Science": 65,
            "English": 70,
            "History": 55,
            "Geography": 68,
        },
        "total": 330,
        "percentage": 66.0,
        "grade": "D",
    },
]
new_s = sorted(s, key = lambda student: student['percentage'], reverse = True)
# print(new_s)
for index, student in enumerate(new_s):
    print(type(index))
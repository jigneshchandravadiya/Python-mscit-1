def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


students = []

# Ask number of students
n = int(input("How many sutdent ? "))

for i in range(n):
    print("\nEnter details of Student", i + 1)

    roll_no = int(input("Enter Roll No: "))
    name = input("Enter Name: ")

    python = int(input("Enter Python marks: "))
    linux = int(input("Enter Linux marks: "))
    ds = int(input("Enter DS marks: "))
    networking = int(input("Enter Networking marks: "))
    computer = int(input("Enter Computer Programming marks: "))

    # Calculate total and percentage
    total = python + linux + ds + networking + computer
    percentage = total / 5

    # Calculate grade
    grade = get_grade(percentage)

    # Create dictionary
    student = {
        "roll_no": roll_no,
        "name": name,
        "python": python,
        "linux": linux,
        "ds": ds,
        "networking": networking,
        "computer": computer,
        "total": total,
        "percentage": percentage,
        "grade": grade
    }

    students.append(student)


# Sort by total marks (highest first)
students.sort(key=lambda x: x["total"], reverse=True)


# Assign ranks
rank = 1

for i in range(len(students)):

    if i > 0 and students[i]["total"] != students[i - 1]["total"]:
        rank = i + 1

    students[i]["rank"] = rank


# Display result
print("\n========== STUDENT RESULT ==========")

for student in students:
    print("\nRoll No    :", student["roll_no"])
    print("Name       :", student["name"])
    print("Total      :", student["total"])
    print("Percentage :", student["percentage"], "%")
    print("Grade      :", student["grade"])
    print("Rank       :", student["rank"])
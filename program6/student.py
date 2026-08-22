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


def get_students():

    students = []

    n = int(input("How many students? "))

    for i in range(n):

        print("\nEnter details of Student", i + 1)

        roll_no = int(input("Enter Roll No: "))
        name = input("Enter Name: ")

        python = int(input("Enter Python marks: "))
        linux = int(input("Enter Linux marks: "))
        ds = int(input("Enter DS marks: "))
        networking = int(input("Enter Networking marks: "))
        computer = int(input("Enter Computer Programming marks: "))

        total = python + linux + ds + networking + computer

        percentage = total / 5

        grade = get_grade(percentage)

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

    students.sort(
        key=lambda x: x["total"],
        reverse=True
    )

    return students

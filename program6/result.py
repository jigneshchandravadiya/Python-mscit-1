def display_students(students):

    print("\n")
    print("=" * 80)
    print("                    STUDENT RESULT")
    print("=" * 80)

    for student in students:

        print("      \n       Roll No    :", student["roll_no"])
        print("|---------------------------|")
        print("      Name       :", student["name"])
        print("|---------------------------|")
        print("      Python     :", student["python"])
        print("|---------------------------|")
        print("      Linux      :", student["linux"])
        print("|---------------------------|")
        print("      DS         :", student["ds"])
        print("|---------------------------|")
        print("      Networking :", student["networking"])
        print("|---------------------------|")
        print("      Computer   :", student["computer"])
        print("|---------------------------|")
        print("      Total      :", student["total"])
        print("|---------------------------|")
        print("      Percentage :", student["percentage"], "%")
        print("|---------------------------|")
        print("      Grade      :", student["grade"])
        print("|---------------------------|")
        print("      Rank       :", student["rank"])
        print("|---------------------------|")      

        print("-" * 80)

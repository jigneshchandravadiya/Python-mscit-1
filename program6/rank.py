def get_rank(students):

    rank = 1

    for i in range(len(students)):

        if i > 0 and students[i]["total"] != students[i - 1]["total"]:
            rank = i + 1

        students[i]["rank"] = rank

    return students

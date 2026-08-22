from student import get_students
from rank import get_rank
from result import display_students


# Get student details
students = get_students()

# Calculate rank
students = get_rank(students)

# Display final result
display_students(students)

from Clases.Error import *
from Clases.Inputs_check import *

class Grade:
    def __init__(self, grade_value=None, date_of_grade=None, student_id=None, subject_id=None, id=0, grade=None, description=None, date_of_award=None, course_id=None):
        if not NumberCheck(str(id), decimal=False, negative=False):
            raise IDValueError
        self.id = id

        # Support both old and new parameter names
        self.grade_value = grade_value if grade_value is not None else grade
        if self.grade_value is not None and (not isinstance(self.grade_value, int) or self.grade_value < 1 or self.grade_value > 5):
            raise GradeValueError

        self.description = description
        if self.description and not StringCheck(self.description, 25):
            raise DescriptionValueError

        self.date_of_grade = date_of_grade if date_of_grade is not None else date_of_award
        if self.date_of_grade and not isinstance(self.date_of_grade, str):
            raise DateFormatError

        self.student_id = student_id
        self.subject_id = subject_id
        self.course_id = course_id

        if self.course_id and not NumberCheck(str(self.course_id), decimal=False, negative=False):
            raise IDValueError
        if self.student_id and not NumberCheck(str(self.student_id), decimal=False, negative=False):
            raise IDValueError
        if self.subject_id and not NumberCheck(str(self.subject_id), decimal=False, negative=False):
            raise IDValueError

    def __str__(self):
        return f"ID: {self.id}, Grade: {self.grade}, Date: {self.date_of_award}, Course ID: {self.course_id}"
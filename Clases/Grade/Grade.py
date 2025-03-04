from Clases.Error import *
from Clases.Inputs_check import *

class Grade:
    def __init__(self, grade, description, date_of_award, course_id, id=0):
        if not NumberCheck(str(id), decimal=False, negative=False):
            raise IDValueError
        self.id = id

        if not isinstance(grade, int) or grade < 1 or grade > 5:
            raise GradeValueError
        self.grade = grade

        if description and not StringCheck(description, 25):
            raise DescriptionValueError
        self.description = description

        if not isinstance(date_of_award, str):
            raise DateFormatError
        self.date_of_award = date_of_award

        if not NumberCheck(str(course_id), decimal=False, negative=False):
            raise IDValueError
        self.course_id = course_id

    def __str__(self):
        return f"ID: {self.id}, Grade: {self.grade}, Date: {self.date_of_award}, Course ID: {self.course_id}"
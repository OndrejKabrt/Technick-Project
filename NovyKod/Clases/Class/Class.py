from Clases.Error import *
from Clases.Inputs_check import *

class Class:
    def __init__(self, name, grade, number_of_class, year_of_entry, active, class_teacher_id=None, id=0):

        if not NumberCheck(str(id), decimal=False, negative=False):
            raise IDValueError
        self.id = id

        if not StringCheck(name, 10):
            raise ClassNameValueError
        self.name = name

        if not isinstance(grade, int) or grade < 1 or grade > 4:
            raise GradeValueError
        self.grade = grade

        if not isinstance(number_of_class, int) or number_of_class < 0:
            raise NumberOfClassValueError
        self.number_of_class = number_of_class

        if not StringCheck(year_of_entry, 10, r"\+\-\\_"):
            raise DateFormatError
        self.year_of_entry = year_of_entry

        if not isinstance(active, bool):
            raise TypeError
        self.active = active

        if class_teacher_id and not NumberCheck(str(class_teacher_id), decimal=False, negative=False):
            raise IDValueError
        self.class_teacher_id = class_teacher_id

    def __str__(self):
        return f"ID: {self.id}, Class: {self.name}, Grade: {self.grade}, Active: {'Yes' if self.active else 'No'}"
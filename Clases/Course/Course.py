from Clases.Error import *
from Clases.Inputs_check import *

class Course:
    def __init__(self, course_name, number_of_theor_hours, number_of_practic_hours, student_id, teacher_id, subject_id, id=0):
        if not NumberCheck(str(id), decimal=False, negative=False):
            raise IDValueError
        self.id = id

        if not StringCheck(course_name, 40):
            raise CourseNameValueError
        self.course_name = course_name

        if not isinstance(number_of_theor_hours, int) or number_of_theor_hours < 0:
            raise TeorHoursValueError
        self.number_of_theor_hours = number_of_theor_hours

        if not isinstance(number_of_practic_hours, int) or number_of_practic_hours < 0:
            raise PractHoursValueError
        self.number_of_practic_hours = number_of_practic_hours

        if not NumberCheck(str(student_id), decimal=False, negative=False):
            raise IDValueError
        self.student_id = student_id

        if not NumberCheck(str(teacher_id), decimal=False, negative=False):
            raise IDValueError
        self.teacher_id = teacher_id

        if not NumberCheck(str(subject_id), decimal=False, negative=False):
            raise IDValueError
        self.subject_id = subject_id

    def __str__(self):
        return f"ID: {self.id}, Course: {self.course_name}, Theory: {self.number_of_theor_hours}h, Practice: {self.number_of_practic_hours}h"
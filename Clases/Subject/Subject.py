from Clases.Error import *
from Clases.Inputs_check import *

class Subject:
    def __init__(self, subject_name, subject_description=None, id=0):
        if not NumberCheck(str(id), decimal=False, negative=False):
            raise IDValueError
        self.id = id

        if not StringCheck(subject_name, 30):
            raise SubjectNameValueError
        self.subject_name = subject_name

        if subject_description and not StringCheck(subject_description, 50):
            raise DescriptionValueError
        self.subject_description = subject_description

    def __str__(self):
        return f"ID: {self.id}, Subject: {self.subject_name}, Description: {self.subject_description}"
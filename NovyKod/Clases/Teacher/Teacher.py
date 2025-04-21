from Clases.Error import *
from Clases.Inputs_check import *

class Teacher:
    def __init__(self, first_name, last_name, teacher_username, teacher_password, email, phone_number, id=0):
        if not NumberCheck(str(id), decimal=False, negative=False):
            raise IDValueError
        self.id = id

        if not StringCheck(first_name, 20):
            raise NameValueError
        self.first_name = first_name

        if not StringCheck(last_name, 20):
            raise LastNameValueError
        self.last_name = last_name

        if not StringCheck(teacher_username, 20):
            raise UserNameValueError
        self.teacher_username = teacher_username

        if not StringCheck(teacher_password, 25):
            raise UserPasswordValueError
        self.teacher_password = teacher_password

        if not StringCheck(email, 30) or '@' not in email:
            raise EmailValueError
        self.email = email

        if not StringCheck(phone_number, 13):
            raise PhoneNumberValueError
        self.phone_number = phone_number

    def __str__(self):
        return f"ID: {self.id}, {self.first_name} {self.last_name}, Username: {self.teacher_username}, Email: {self.email}"
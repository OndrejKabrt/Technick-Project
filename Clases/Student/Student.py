from Clases.Error import *
from Clases.Inputs_check import *


class Student:
    def __init__(self, first_name, last_name, user_name, user_password, number_in_class_order, is_student, id = 0):

        if not NumberCheck(str(id), decimal = False, negative=False):
            raise IDValueError
        self.id = id

        if not StringCheck(first_name, 20):
            raise NameValueError
        self.first_name = first_name

        if not StringCheck(last_name, 20):
            raise LastNameValueError
        self.last_name = last_name

        if not StringCheck(user_name, 20):
            raise UserNameValueError
        self.user_name = user_name

        if not StringCheck(user_password, 20):
            raise UserPasswordValueError
        self.user_password = user_password

        if not isinstance(is_student, bool):
            raise TypeError
        self.is_student = is_student

        if not NumberCheck(str(number_in_class_order), decimal = False, negative=False):
            raise OrderNumberValueError
        self.number_in_class_order = number_in_class_order

    def __str__(self):
        return f" {self.number_in_class_order}, Jmeno: {self.first_name} {self.last_name}, Uzivatel {self.user_name} {self.user_password}, Student: {'Ano' if self.is_student else 'Ne'}"
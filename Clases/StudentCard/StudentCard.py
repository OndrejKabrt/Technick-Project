from Clases.Error import *
from Clases.Inputs_check import *

class StudentCard:
    def __init__(self, town, street, descriptive_number, zip_code, email, date_of_birth, phone_number, student_id, id=0):
        if not NumberCheck(str(id), decimal=False, negative=False):
            raise IDValueError
        self.id = id

        if not StringCheck(town, 15):
            raise TownValueError
        self.town = town

        if not StringCheck(street, 20):
            raise StreetValueError
        self.street = street

        if not StringCheck(descriptive_number, 10):
            raise DescriptiveNumberValueError
        self.descriptive_number = descriptive_number

        if not StringCheck(zip_code, 6):
            raise ZipCodeValueError
        self.zip_code = zip_code

        if not StringCheck(email, 30) or '@' not in email:
            raise EmailValueError
        self.email = email

        if not isinstance(date_of_birth, str):  # Assuming date comes as string
            raise DateFormatError
        self.date_of_birth = date_of_birth

        if not StringCheck(phone_number, 13):
            raise PhoneNumberValueError
        self.phone_number = phone_number

        if not NumberCheck(str(student_id), decimal=False, negative=False):
            raise IDValueError
        self.student_id = student_id

    def __str__(self):
        return f"ID: {self.id}, Student ID: {self.student_id}, {self.town}, {self.street} {self.descriptive_number}"
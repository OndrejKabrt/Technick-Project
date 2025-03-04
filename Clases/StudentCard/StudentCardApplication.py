from Clases.Error import *
from Clases.StudentCard import StudentCard
from Clases.StudentCard.StudentCardDAO import StudentCardDAO


class StudentCardApplication:
    def __init__(self, table_user_interface):
        self.table_user_interface = table_user_interface
        self.studentCardDAO = StudentCardDAO(self)

    def insertStudentCard(self):
        town = self.table_user_interface.process_input("Město: ")
        street = self.table_user_interface.process_input("Ulice: ")
        descriptive_number = self.table_user_interface.process_input("Číslo popisné: ")
        zip_code = self.table_user_interface.process_input("PSČ: ")
        email = self.table_user_interface.process_input("Email: ")
        date_of_birth = self.table_user_interface.process_input("Datum narození (YYYY-MM-DD): ")
        phone_number = self.table_user_interface.process_input("Telefonní číslo: ")
        student_id = self.table_user_interface.process_input("ID studenta: ")

        try:
            student_card = StudentCard(town, street, descriptive_number, zip_code,email, date_of_birth, phone_number, student_id)
            self.studentCardDAO.save(student_card)
            self.table_user_interface.print_message("Karta studenta byla úspěšně přidána.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při spojení s databází.")
        except ValueError as e:
            self.table_user_interface.print_message(str(e))

    def findStudentCard(self):
        student_id = self.table_user_interface.process_input("Zadejte ID studenta: ")
        try:
            card = self.studentCardDAO.find_by_student_id(student_id)
            if card:
                print(card)
            else:
                self.table_user_interface.print_message("Karta studenta nebyla nalezena.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při hledání karty studenta.")


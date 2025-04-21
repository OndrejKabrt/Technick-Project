from Clases.Error import *
from Clases.Teacher.Teacher import Teacher
from Clases.Teacher.TeacherDAO import TeacherDAO

class TeacherApplication:
    def __init__(self, table_user_interface):
        self.table_user_interface = table_user_interface
        self.teacherDAO = TeacherDAO(self)

    def insertTeacher(self):
        first_name = self.table_user_interface.process_input("Jméno učitele: ")
        last_name = self.table_user_interface.process_input("Příjmení učitele: ")
        username = self.table_user_interface.process_input("Uživatelské jméno: ")
        password = "Zada_se_samo"
        email = self.table_user_interface.process_input("Email: ")
        phone_number = self.table_user_interface.process_input("Telefonní číslo: ")

        try:
            teacher = Teacher(first_name, last_name, username, password, email, phone_number)
            self.teacherDAO.save(teacher)
            self.table_user_interface.print_message("Učitel byl úspěšně přidán.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při spojení s databází.")
        except ValueError as e:
            self.table_user_interface.print_message(str(e))

    def deleteTeacher(self):
        username = self.table_user_interface.process_input("Zadejte username učitele pro smazání: ")
        try:
            self.teacherDAO.delete(username)
            self.table_user_interface.print_message("Učitel byl smazán.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při spojení s databází.")

    def listTeachers(self):
        try:
            teachers = self.teacherDAO.select_all()
            for teacher in teachers:
                print(teacher)
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání učitelů.")

    def getTeachersCertificates(self):
        try:
            certificates = self.teacherDAO.get_teachers_certificates()
            for cert in certificates:
                print(f"Učitel: {cert[0]}, Certifikát: {cert[1]}")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání certifikátů učitelů.")

    def addCertificateToTeacher(self):
        username = self.table_user_interface.process_input("Username učitele: ")
        certificate_name = self.table_user_interface.process_input("Název certifikátu: ")
        valid_since = self.table_user_interface.process_input("Platný od (YYYY-MM-DD): ")

        try:
            self.teacherDAO.add_certificate(username, certificate_name, valid_since)
            self.table_user_interface.print_message("Certifikát byl úspěšně přidán učiteli.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při přidávání certifikátu učiteli.")
from pyodbc import DatabaseError
from Clases.Error import *
from Clases.Student.Student import Student
from Clases.Student.StudentDAO import StudentDAO


class StudentApplication:
    def __init__(self, table_user_interface):
        self.table_user_interface = table_user_interface
        self.studentDAO = StudentDAO(self)

    def insertStudent(self):
        first_name = self.table_user_interface.process_input("Jméno studenta: ")
        last_name = self.table_user_interface.process_input("Příjmení studenta: ")
        user_name = self.table_user_interface.process_input("Uživatelské jméno: ")
        user_password = "ZadaSeSamo"
        number_in_class_order = 1
        is_student = True
        try:
            s = Student(first_name, last_name, user_name, user_password, number_in_class_order, is_student)
        except NameValueError:
            self.table_user_interface.print_message("Neplatné jméno: Jméno musí obsahovat sadu 20 písmen.")
        except LastNameValueError:
            self.table_user_interface.print_message("Neplatné přijmení: Přijmení musí obsahovat sadu 20 písmen.")
        except UserNameValueError:
            self.table_user_interface.print_message("Neplatné uživatelské jméno: username musí obsahovat sadu 20 písmen.")
        else:
            try:
                self.studentDAO.save(s)
                self.table_user_interface.print_message("Student byl uložen.")
            except DatabaseError:
                self.table_user_interface.print_message("Něco se pokazilo, při projení s databází.")

    def deleteStudent(self):
        user_name = self.table_user_interface.process_input("Zadejte username studenta, kterého si přejete smazat.")
        if (0 > len(user_name) <= 20):
            try:
                self.studentDAO.delete(user_name)
                self.table_user_interface.print_message("Student byl smazán.")
            except DatabaseError:
                self.table_user_interface.print_message("Něco se pokazilo, při projení s databází.")
        else:
            self.table_user_interface.print_message("Vstupní data nejsou ve správném formátu.")

    def listStudents(self):
        try:
            list = self.studentDAO.select_all()
            for student in list:
                self.table_user_interface.print_message(student)
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání studentů.")

    def listActiveStudents(self):
        try:
            active_students = self.studentDAO.get_active_students()
            for student in active_students:
                print(f"Jméno: {student[0]}, Příjmení: {student[1]}, Třída: {student[2]}")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání aktivních studentů.")

    def changeStudentClass(self):
        first_name = self.table_user_interface.process_input("Jméno studenta: ")
        last_name = self.table_user_interface.process_input("Příjmení studenta: ")
        previous_class = self.table_user_interface.process_input("Současná třída: ")
        new_class = self.table_user_interface.process_input("Nová třída: ")

        try:
            self.studentDAO.change_student_class(first_name, last_name, previous_class, new_class)
            self.table_user_interface.print_message("Třída studenta byla úspěšně změněna.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při změně třídy studenta.")

    def getStudentsInClass(self):
        class_name = self.table_user_interface.process_input("Název třídy: ")
        grade = self.table_user_interface.process_input("Ročník: ")

        try:
            students = self.studentDAO.get_students_in_class(class_name, grade)
            for student in students:
                print(student)
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání studentů třídy.")

    def setPreviousStudent(self):
        first_name = self.table_user_interface.process_input("Jméno studenta: ")
        last_name = self.table_user_interface.process_input("Příjmení studenta: ")
        class_name = self.table_user_interface.process_input("Název třídy: ")

        try:
            self.studentDAO.set_previous_student(first_name, last_name, class_name)
            self.table_user_interface.print_message("Student byl úspěšně označen jako bývalý student.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při označování bývalého studenta.")


















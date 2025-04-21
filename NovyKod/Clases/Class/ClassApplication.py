from pyodbc import DatabaseError
from Clases.Class.ClassDAO import ClassDAO
from Clases.Error import *
from Clases.Class.Class import Class


class ClassApplication:
    def __init__(self, table_user_interface):
        self.table_user_interface = table_user_interface
        self.classDAO = ClassDAO(self)

    def insertClass(self):
        name = self.table_user_interface.process_input("Název třídy: ")
        grade = self.table_user_interface.process_input("Ročník: ")
        number_of_class = self.table_user_interface.process_input("Číslo třídy: ")
        year_of_entry = self.table_user_interface.process_input("Rok nástupu: ")
        class_teacher_id = self.table_user_interface.process_input("ID třídního učitele: ")

        try:
            class_obj = Class(name, grade, number_of_class, year_of_entry, True, class_teacher_id)
            self.classDAO.save(class_obj)
            self.table_user_interface.print_message("Třída byla úspěšně přidána.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při spojení s databází.")
        except ValueError as e:
            self.table_user_interface.print_message(str(e))

    def listClasses(self):
        try:
            classes = self.classDAO.select_all()
            for class_obj in classes:
                self.table_user_interface.print_message(class_obj)
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání tříd.")

    def getStudentsCount(self):
        try:
            counts = self.classDAO.get_students_count()
            for count in counts:
                print(f"Třída: {count[0]}, Číslo učebny: {count[1]}, Počet studentů: {count[2]}")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání počtu studentů.")

    def setClassPreviousStudents(self):
        class_name = self.table_user_interface.process_input("Název třídy: ")

        try:
            self.classDAO.set_class_previous_students(class_name)
            self.table_user_interface.print_message("Studenti byli úspěšně označeni jako bývalí studenti.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při označování bývalých studentů.")



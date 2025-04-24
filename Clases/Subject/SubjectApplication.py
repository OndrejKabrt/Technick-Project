from Clases.Error import *
from Clases.Subject.Subject import Subject
from Clases.Subject.SubjectDAO import SubjectDAO


class SubjectApplication:
    def __init__(self, table_user_interface):
        self.table_user_interface = table_user_interface
        self.subjectDAO = SubjectDAO(self)

    def insertSubject(self):
        subject_name = self.table_user_interface.process_input("Název předmětu: ")
        subject_description = self.table_user_interface.process_input("Popis předmětu: ")

        try:
            subject = Subject(subject_name, subject_description)
            self.subjectDAO.save(subject)
            self.table_user_interface.print_message("Předmět byl úspěšně přidán.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při spojení s databází.")
        except ValueError as e:
            self.table_user_interface.print_message(str(e))

    def listSubjects(self):
        try:
            subjects = self.subjectDAO.select_all()
            for subject in subjects:
                print(subject)
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání předmětů.")

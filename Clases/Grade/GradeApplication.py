from Clases.Error import *
from Clases.Grade import Grade
from Clases.Grade.GradeDAO import GradeDAO


class GradeApplication:
    def __init__(self, table_user_interface):
        self.table_user_interface = table_user_interface
        self.gradeDAO = GradeDAO(self)

    def insertGrade(self):
        grade_value = self.table_user_interface.process_input("Známka: ")
        description = self.table_user_interface.process_input("Popis: ")
        date_of_award = self.table_user_interface.process_input("Datum udělení (YYYY-MM-DD): ")
        course_id = self.table_user_interface.process_input("ID kurzu: ")

        try:
            grade = Grade(grade_value, description, date_of_award, course_id)
            self.gradeDAO.save(grade)
            self.table_user_interface.print_message("Známka byla úspěšně přidána.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při spojení s databází.")
        except ValueError as e:
            self.table_user_interface.print_message(str(e))

    def listCourseGrades(self):
        course_id = self.table_user_interface.process_input("Zadejte ID kurzu: ")
        try:
            grades = self.gradeDAO.select_by_course(course_id)
            for grade in grades:
                print(grade)
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání známek.")
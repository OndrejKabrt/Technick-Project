from Clases.Course.CourseDAO import CourseDAO
from Clases.Error import *
from Clases.Course.Course import Course


class CourseApplication:
    def __init__(self, table_user_interface):
        self.table_user_interface = table_user_interface
        self.courseDAO = CourseDAO(self)

    def insertCourse(self):
        course_name = self.table_user_interface.process_input("Název kurzu: ")
        theory_hours = self.table_user_interface.process_input("Počet teoretických hodin: ")
        practice_hours = self.table_user_interface.process_input("Počet praktických hodin: ")
        student_id = self.table_user_interface.process_input("ID studenta: ")
        teacher_id = self.table_user_interface.process_input("ID učitele: ")
        subject_id = self.table_user_interface.process_input("ID předmětu: ")

        try:
            course = Course(course_name, theory_hours, practice_hours,student_id, teacher_id, subject_id)
            self.courseDAO.save(course)
            self.table_user_interface.print_message("Kurz byl úspěšně přidán.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při spojení s databází.")
        except ValueError as e:
            self.table_user_interface.print_message(str(e))

    def listStudentCourses(self):
        student_id = self.table_user_interface.process_input("Zadejte ID studenta: ")
        try:
            courses = self.courseDAO.select_by_student(student_id)
            for course in courses:
                print(course)
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání kurzů.")

    def getCourseStudents(self):
        try:
            students = self.courseDAO.get_course_students()
            for student in students:
                print(f"Kurz: {student[0]}, Student: {student[1]}")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání studentů kurzu.")

    def getCoursesAndTeachers(self):
        try:
            courses = self.courseDAO.get_courses_and_teachers()
            for course in courses:
                print(f"Předmět: {course[0]}, Učitel: {course[1]}")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání kurzů a učitelů.")

    def getStudentsInCourse(self):
        course_name = self.table_user_interface.process_input("Název kurzu: ")

        try:
            students = self.courseDAO.get_students_in_course(course_name)
            for student in students:
                print(student)
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání studentů kurzu.")


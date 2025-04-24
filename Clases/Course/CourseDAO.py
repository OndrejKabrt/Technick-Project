from Clases.Course.Course import Course
from Clases.DatabaseSingleton import DatabaseSingleton
from Clases.Error import DatabaseError

class CourseDAO:
    def __init__(self, table_application):
        self.table_application = table_application

    def save(self, course):
        sql = "INSERT INTO Course (course_name, number_of_theor_hours, number_of_practic_hours, Student_ID, Teacher_ID, Subject_ID) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (course.course_name,course.number_of_theor_hours,course.number_of_practic_hours,course.student_id,course.teacher_id,course.subject_id)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Failed to save course: {str(e)}")
        finally:
            cursor.close()

    def select_by_student(self, student_id):
        sql = "SELECT id, course_name, number_of_theor_hours, number_of_practic_hours, Student_ID, Teacher_ID, Subject_ID FROM Course WHERE Student_ID = %s"
        values = (student_id,)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            rows = cursor.fetchall()
            courses = []
            for row in rows:
                course = Course(course_name=row[1],number_of_theor_hours=row[2],number_of_practic_hours=row[3],student_id=row[4],teacher_id=row[5],subject_id=row[6],id=row[0])
                courses.append(course)
            return courses
        except Exception as e:
            raise DatabaseError(f"Failed to fetch courses: {str(e)}")
        finally:
            cursor.close()

    def get_course_students(self):
        """Implementace view course_students"""
        sql = "SELECT course_name, Student FROM course_students"
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Failed to get course students: {str(e)}")
        finally:
            cursor.close()

    def get_courses_and_teachers(self):
        """Implementace view courses_and_teachers"""
        sql = "SELECT subject_name, Teacher FROM courses_and_teachers"
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Failed to get courses and teachers: {str(e)}")
        finally:
            cursor.close()

    def get_students_in_course(self, course_name):
        """Implementace procedury students_in_course"""
        sql = "CALL students_in_course(%s)"
        values = (course_name,)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            return cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Failed to get students in course: {str(e)}")
        finally:
            cursor.close()
from Clases.DatabaseSingleton import DatabaseSingleton
from Clases.Student.Student import Student
from Clases.Error import *


class StudentDAO:
    def __init__(self, table_application):
        self.table_application = table_application

    def save(self, student):
        sql = "INSERT INTO Student (first_name, last_name, user_name, user_password, number_in_class_order, is_student) VALUES (%s, %s, %s, %s, %s, %s);"
        is_student_bit = 1 if student.is_student else 0
        values = (student.first_name, student.last_name, student.user_name, student.user_password, student.number_in_class_order, is_student_bit)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to save student: {str(e)}")
        finally:
            cursor.close()

    def delete(self, user_name):
        sql = "DELETE FROM Student WHERE user_name = %s;"
        values = (user_name,)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute("START TRANSACTION;")
            cursor.execute(sql, values)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Failed to delete student: {str(e)}")
        finally:
            cursor.close()

    def select_all(self):
        sql = "select * from student_list;"
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            students = []
            for row in rows:
                is_student_bool = bool(row[6])
                student = Student(first_name=row[1], last_name=row[2], user_name=row[3], user_password=row[4], number_in_class_order=row[5], is_student=is_student_bool, id=row[0])
                students.append(student)
            return students
        except Exception as e:
            raise DatabaseError(f"Failed to fetch students: {str(e)}")
        finally:
            cursor.close()

    def update(self, student):
        sql = "UPDATE Student SET first_name = %s, last_name = %s, user_name = %s, user_password = %s, number_in_class_order = %s, is_student = %s WHERE id = %s;"
        is_student_bit = 1 if student.is_student else 0
        values = (student.first_name, student.last_name, student.user_name, student.user_password, student.number_in_class_order, is_student_bit, student.id)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute("START TRANSACTION;")
            cursor.execute(sql, values)
            affected_rows = cursor.rowcount
            conn.commit()
            return affected_rows > 0
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Failed to update student: {str(e)}")
        finally:
            cursor.close()

    def find_by_username(self, username):
        sql = "SELECT id, first_name, last_name, user_name, user_password, number_in_class_order, is_student FROM Student WHERE user_name = %s;"
        values = (username,)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            row = cursor.fetchone()
            if row:
                is_student = bool(row[6])
                return Student(first_name=row[1], last_name=row[2], user_name=row[3], user_password=row[4], number_in_class_order=row[5], is_student=is_student, id=row[0])
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to find student: {str(e)}")
        finally:
            cursor.close()

    def get_active_students(self):
        """Implements the view list_of_active_students"""
        sql = "SELECT first_name, last_name, name FROM list_of_active_students;"
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch active students: {str(e)}")
        finally:
            cursor.close()

    def change_student_class(self, first_name, last_name, previous_class, new_class):
        """Implements the stored procedure student_class_change"""
        sql = "CALL student_class_change(%s, %s, %s, %s);"
        values = (first_name, last_name, previous_class, new_class)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Failed to change student class: {str(e)}")
        finally:
            cursor.close()

    def get_students_in_class(self, class_name, grade):
        """Implements the stored procedure students_in_class"""
        sql = "CALL students_in_class(%s, %s);"
        values = (class_name, grade)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            return cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Failed to get students in class: {str(e)}")
        finally:
            cursor.close()

    def set_previous_student(self, first_name, last_name, class_name):
        """Implements the stored procedure set_previous_student_by_name"""
        sql = "CALL set_previous_student_by_name(%s, %s, %s);"
        values = (first_name, last_name, class_name)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Failed to set previous student: {str(e)}")
        finally:
            cursor.close()

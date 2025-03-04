from Clases.DatabaseSingleton import DatabaseSingleton
from Clases.Error import DatabaseError
from Clases.Teacher import Teacher

class TeacherDAO:
    def __init__(self, table_application):
        self.table_application = table_application

    def save(self, teacher):
        sql = "INSERT INTO Teacher (first_name, last_name, teacher_username, teacher_password, email, phone_number) VALUES (?, ?, ?, ?, ?, ?)"
        values = (teacher.first_name,teacher.last_name,teacher.teacher_username,teacher.teacher_password,teacher.email,teacher.phone_number)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")
            cursor.execute(sql, values)
            cursor.execute("COMMIT TRANSACTION")
            return cursor.rowcount > 0
        except Exception as e:
            cursor.execute("ROLLBACK TRANSACTION")
            raise DatabaseError(f"Failed to save teacher: {str(e)}")
        finally:
            cursor.close()

    def delete(self, teacher_username):
        sql = "DELETE FROM Teacher WHERE teacher_username = ?"
        values = (teacher_username,)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")
            cursor.execute(sql, values)
            affected_rows = cursor.rowcount
            cursor.execute("COMMIT TRANSACTION")
            return affected_rows > 0
        except Exception as e:
            cursor.execute("ROLLBACK TRANSACTION")
            raise DatabaseError(f"Failed to delete teacher: {str(e)}")
        finally:
            cursor.close()

    def select_all(self):
        sql = "SELECT id, first_name, last_name, teacher_username, teacher_password, email, phone_number FROM Teacher"

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            teachers = []
            for row in rows:
                teacher = Teacher(first_name=row[1],last_name=row[2],teacher_username=row[3],teacher_password=row[4],email=row[5],phone_number=row[6],id=row[0])
                teachers.append(teacher)
            return teachers
        except Exception as e:
            raise DatabaseError(f"Failed to fetch teachers: {str(e)}")
        finally:
            cursor.close()

    def get_teachers_certificates(self):
        """Implementace view teachers_certificate"""
        sql = "SELECT Teacher, certificate_name FROM teachers_certificate"
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Failed to get teachers certificates: {str(e)}")
        finally:
            cursor.close()

    def add_certificate(self, username, certificate_name, valid_since):
        """Implementace procedury add_certificate_to_teacher"""
        sql = "EXEC add_certificate_to_teacher @username_of_teacher=?, @name_of_certificate=?, @valide_since=?"
        values = (username, certificate_name, valid_since)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            cursor.commit()
            return True
        except Exception as e:
            raise DatabaseError(f"Failed to add certificate to teacher: {str(e)}")
        finally:
            cursor.close()
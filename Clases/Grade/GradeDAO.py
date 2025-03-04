from Clases.Grade import Grade
from Clases.DatabaseSingleton import DatabaseSingleton
from Clases.Error import DatabaseError

class GradeDAO:
    def __init__(self, table_application):
        self.table_application = table_application

    def save(self, grade):
        sql = "INSERT INTO Grade (grade, description, date_of_award, Course_ID) VALUES (?, ?, ?, ?)"
        values = (grade.grade,grade.description,grade.date_of_award,grade.course_id)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")
            cursor.execute(sql, values)
            cursor.execute("COMMIT TRANSACTION")
            return cursor.rowcount > 0
        except Exception as e:
            cursor.execute("ROLLBACK TRANSACTION")
            raise DatabaseError(f"Failed to save grade: {str(e)}")
        finally:
            cursor.close()

    def select_by_course(self, course_id):
        sql = "SELECT id, grade, description, date_of_award, Course_ID FROM Grade WHERE Course_ID = ?"
        values = (course_id,)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            rows = cursor.fetchall()
            grades = []
            for row in rows:
                g = Grade(grade=row[1],description=row[2],date_of_award=row[3],course_id=row[4],id=row[0])
                grades.append(g)
            return grades
        except Exception as e:
            raise DatabaseError(f"Failed to fetch grades: {str(e)}")
        finally:
            cursor.close()
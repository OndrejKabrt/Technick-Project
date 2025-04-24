from Clases.Grade.Grade import Grade
from Clases.DatabaseSingleton import DatabaseSingleton
from Clases.Error import DatabaseError

class GradeDAO:
    def __init__(self, table_application):
        self.table_application = table_application

    def save(self, grade):
        sql = "INSERT INTO Grade (grade, description, date_of_award, Course_ID) VALUES (%s, %s, %s, %s)"
        values = (grade.grade_value, grade.description, grade.date_of_grade, grade.course_id)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Failed to save grade: {str(e)}")
        finally:
            cursor.close()

    def select_by_student(self, student_id):
        sql = """SELECT g.id, g.grade, g.description, g.date_of_award, g.Course_ID
                FROM Grade g
                JOIN Course c ON g.Course_ID = c.id
                WHERE c.Student_ID = %s"""
        values = (student_id,)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            rows = cursor.fetchall()
            grades = []
            for row in rows:
                g = Grade(grade=row[1], description=row[2], date_of_award=row[3], course_id=row[4], id=row[0])
                grades.append(g)
            return grades
        except Exception as e:
            raise DatabaseError(f"Failed to fetch grades: {str(e)}")
        finally:
            cursor.close()
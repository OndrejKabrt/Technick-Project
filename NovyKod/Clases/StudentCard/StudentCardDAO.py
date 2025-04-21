from Clases.DatabaseSingleton import DatabaseSingleton
from Clases.Error import DatabaseError
from Clases.StudentCard.StudentCard import StudentCard


class StudentCardDAO:
    def __init__(self, table_application):
        self.table_application = table_application

    def save(self, student_card):
        sql = "INSERT INTO Student_Card (town, street, descriptive_number, zip_code, email, date_of_birth, phone_number, Student_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (student_card.town,student_card.street,student_card.descriptive_number,student_card.zip_code,student_card.email,student_card.date_of_birth,student_card.phone_number,student_card.student_id)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Failed to save student card: {str(e)}")
        finally:
            cursor.close()

    def find_by_student_id(self, student_id):
        sql = "SELECT id, town, street, descriptive_number, zip_code, email, date_of_birth, phone_number, Student_ID FROM Student_Card WHERE Student_ID = %s"
        values = (student_id,)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            row = cursor.fetchone()
            if row:
                return StudentCard(town=row[1],street=row[2],descriptive_number=row[3],zip_code=row[4],email=row[5],date_of_birth=row[6],phone_number=row[7],student_id=row[8],id=row[0])
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to find student card: {str(e)}")
        finally:
            cursor.close()
from Clases.DatabaseSingleton import DatabaseSingleton
from Clases.Error import DatabaseError
from Clases.Subject import Subject


class SubjectDAO:
    def __init__(self, table_application):
        self.table_application = table_application

    def save(self, subject):
        sql = "INSERT INTO Subject (subject_name, subject_description) VALUES (?, ?)"
        values = (subject.subject_name, subject.subject_description)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")
            cursor.execute(sql, values)
            cursor.execute("COMMIT TRANSACTION")
            return cursor.rowcount > 0
        except Exception as e:
            cursor.execute("ROLLBACK TRANSACTION")
            raise DatabaseError(f"Failed to save subject: {str(e)}")
        finally:
            cursor.close()

    def select_all(self):
        sql = "SELECT id, subject_name, subject_description FROM Subject"

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            subjects = []
            for row in rows:
                subject = Subject(subject_name=row[1],subject_description=row[2],id=row[0])
                subjects.append(subject)
            return subjects
        except Exception as e:
            raise DatabaseError(f"Failed to fetch subjects: {str(e)}")
        finally:
            cursor.close()
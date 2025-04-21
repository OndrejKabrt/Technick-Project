from Clases.DatabaseSingleton import DatabaseSingleton
from Clases.Error import DatabaseError
from Clases.Class.Class import Class
import logging

class ClassDAO:
    def __init__(self, table_application):
        self.table_application = table_application

    def save(self, c):
        sql = "INSERT INTO Class (name, grade, number_of_class, year_of_entry, active, Class_Teacher_ID) VALUES (%s, %s, %s, %s, %s, %s)"
        active_bit = 1 if c.active else 0
        values = (c.name,c.grade,c.number_of_class,c.year_of_entry,active_bit,c.class_teacher_id)
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Failed to save class: {str(e)}")
        finally:
            cursor.close()

    def select_all(self):
        sql = "SELECT * from class_list"
        logging.debug(f'Executing SQL: {sql}')

        conn = None
        cursor = None
        try:
            conn = DatabaseSingleton()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            classes = []
            for row in rows:
                class_obj = Class(
                    name=row[1],
                    grade=row[2],
                    number_of_class=row[3],
                    year_of_entry=row[4],
                    active=bool(row[5]),
                    class_teacher_id=row[6],
                    id=row[0]
                )
                classes.append(class_obj)
            return classes
            
        except Exception as e:
            logging.error(f'Error in select_all: {str(e)}')
            raise DatabaseError(f"Failed to fetch classes: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            DatabaseSingleton.close_conn(conn)


    def get_students_count(self):
        """Implementace view count_of_class_students"""
        sql = "SELECT name, number_of_class, Pocet_Studentu FROM count_of_class_students"
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Failed to get class students count: {str(e)}")
        finally:
            cursor.close()


    def set_class_previous_students(self, class_name):
        """Implementace procedury set_previous_students_by_class"""
        sql = "CALL set_previous_students_by_class(%s)"
        values = (class_name,)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Failed to set previous students by class: {str(e)}")
        finally:
            cursor.close()

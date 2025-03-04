from Clases.DatabaseSingleton import DatabaseSingleton
from Clases.Student.Student import Student


class StudentDAO:
    def __init__(self, table_application):
        self.table_application = table_application


    def save(self, a):
        sql = "INSERT INTO Student (first_name, last_name, user_name, user_password, number_in_class_order, is_student) VALUES (?, ? , ? , ? , ?, 1);"
        values = (a.first_name, a.last_name, a.user_name, a.user_password, a.number)
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute("START TRANSACTION;")
            cursor.execute(sql, values)
        except Exception as e:
            print(e)
            cursor.execute("ROLLBACK;")
        else:
            cursor.execute("COMMIT;")
        finally:
            cursor.close()

    def delete(self, user_name):
        sql = "DELETE FROM Student WHERE user_name = ?;"
        values = user_name
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute("START TRANSACTION;")
            cursor.execute(sql, values)
        except Exception as e:
            print(e)
            cursor.execute("ROLLBACK;")
        else:
            cursor.execute("COMMIT;")
        finally:
            cursor.close()

    def select_all(self):
        sql = "SELECT * FROM Student;"
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            print(e)
        else:
            list = []
            for i in result:
                s = Student(i[0], i[1], i[2], i[3], i[4], i[5])
                list.append(s)
            if (len(list) > 0):
                return list
        finally:
            cursor.close()



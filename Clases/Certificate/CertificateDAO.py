from Clases.DatabaseSingleton import DatabaseSingleton
from Clases.Error import DatabaseError
from Clases.Certificate import Certificate

class CertificateDAO:
    def __init__(self, table_application):
        self.table_application = table_application

    def save(self, certificate):
        sql = "INSERT INTO Certificate (certificate_name, issuing_organization, description) VALUES (?, ?, ?)"
        values = (
            certificate.certificate_name,
            certificate.issuing_organization,
            certificate.description
        )

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")
            cursor.execute(sql, values)
            cursor.execute("COMMIT TRANSACTION")
            return cursor.rowcount > 0
        except Exception as e:
            cursor.execute("ROLLBACK TRANSACTION")
            raise DatabaseError(f"Failed to save certificate: {str(e)}")
        finally:
            cursor.close()

    def select_all(self):
        sql = "SELECT id, certificate_name, issuing_organization, description FROM Certificate"

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            certificates = []
            for row in rows:
                c = Certificate(certificate_name=row[1],issuing_organization=row[2],description=row[3],id=row[0])
                certificates.append(c)
            return certificates
        except Exception as e:
            raise DatabaseError(f"Failed to fetch certificates: {str(e)}")
        finally:
            cursor.close()
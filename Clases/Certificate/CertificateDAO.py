from Clases.DatabaseSingleton import DatabaseSingleton
from Clases.Certificate.Certificate import Certificate
from Clases.Error import *

class CertificateDAO:
    def __init__(self, table_application):
        self.table_application = table_application

    def save(self, certificate):
        """Inserts a new certificate into the database."""
        sql = "INSERT INTO certificate (certificate_name, issuing_organization, description) VALUES (%s, %s, %s)"
        values = (certificate.certificate_name, certificate.issuing_organization, certificate.description)

        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, values)
            conn.commit()  # Explicit commit for MySQL
            return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseError(f"Failed to save certificate: {str(e)}")
        finally:
            cursor.close()

    def select_all(self):
        """Retrieves all certificates from the database."""
        sql = "SELECT id, certificate_name, issuing_organization, description FROM certificate"
        conn = DatabaseSingleton()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            certificates = [Certificate(certificate_name=row[1], issuing_organization=row[2], description=row[3], id=row[0]) for row in rows]
            return certificates
        except Exception as e:
            raise DatabaseError(f"Failed to fetch certificates: {str(e)}")
        finally:
            cursor.close()
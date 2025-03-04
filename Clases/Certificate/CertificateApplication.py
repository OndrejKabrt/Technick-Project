from Clases.Certificate.CertificateDAO import CertificateDAO
from Clases.Error import *
from Clases.Certificate import Certificate


class CertificateApplication:
    def __init__(self, table_user_interface):
        self.table_user_interface = table_user_interface
        self.certificateDAO = CertificateDAO(self)

    def insertCertificate(self):
        certificate_name = self.table_user_interface.process_input("Název certifikátu: ")
        issuing_org = self.table_user_interface.process_input("Vydávající organizace: ")
        description = self.table_user_interface.process_input("Popis: ")

        try:
            certificate = Certificate(certificate_name, issuing_org, description)
            self.certificateDAO.save(certificate)
            self.table_user_interface.print_message("Certifikát byl úspěšně přidán.")
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při spojení s databází.")
        except ValueError as e:
            self.table_user_interface.print_message(str(e))

    def listCertificates(self):
        try:
            certificates = self.certificateDAO.select_all()
            for certificate in certificates:
                print(certificate)
        except DatabaseError:
            self.table_user_interface.print_message("Něco se pokazilo při načítání certifikátů.")
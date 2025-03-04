from Clases.Error import *
from Clases.Inputs_check import *


class Certificate:
    def __init__(self, certificate_name, issuing_organization=None, description=None, id=0):
        if not NumberCheck(str(id), decimal=False, negative=False):
            raise IDValueError
        self.id = id

        if not StringCheck(certificate_name, 80):
            raise CertificateNameValueError
        self.certificate_name = certificate_name

        if issuing_organization and not StringCheck(issuing_organization, 50):
            raise OrganizationValueError
        self.issuing_organization = issuing_organization

        if description and not StringCheck(description, 80):
            raise DescriptionValueError
        self.description = description

    def __str__(self):
        return f"ID: {self.id}, Certificate: {self.certificate_name}, Issuer: {self.issuing_organization}"
#Some of those errors may be created for specific object, but they may be used somewhere else

#global errors
class IDValueError(Exception):
    pass
class DatabaseError(Exception):
    pass

#errors for Student
class NameValueError(Exception):
    pass
class LastNameValueError(Exception):
    pass
class RegistryDateValueError(Exception):
    pass
class UserNameValueError(Exception):
    pass
class UserPasswordValueError(Exception):
    pass
class OrderNumberValueError(Exception):
    pass
class StudentBoolValueError(Exception):
    pass


#errors for teacher
class EmailValueError(Exception):
    pass
class PhoneNumberValueError(Exception):
    pass

#errors for subject
class SubjectNameValueError(Exception):
    pass
class DescriptionValueError(Exception):
    pass

#errors for Class
class ClassNameValueError(Exception):
    pass
class GradeValueError(Exception):
    pass
class NumberOfClassValueError(Exception):
    pass
class DateFormatError(Exception):
    pass

#errors for class StudentCard
class TownValueError(Exception):
    pass
class StreetValueError(Exception):
    pass
class DescriptiveNumberValueError(Exception):
    pass
class ZipCodeValueError(Exception):
    pass

#errors for Course
class CourseNameValueError(Exception):
    pass
class TeorHoursValueError(Exception):
    pass
class PractHoursValueError(Exception):
    pass

#errors for Certificate
class CertificateNameValueError(Exception):
    pass
class OrganizationValueError(Exception):
    pass














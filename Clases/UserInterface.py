from Clases.Student.StudentInterface import StudentInterface
from Clases.Certificate.CertificateInterface import CertificateInterface
from Clases.Class.ClassInterface import ClassInterface
from Clases.Course.CourseInterface import CourseInterface
from Clases.Grade.GradeInterface import GradeInterface
from Clases.StudentCard.StudentCardInterface import StudentCardInterface
from Clases.Subject.SubjectInterface import SubjectInterface
from Clases.Teacher.TeacherInterface import TeacherInterface


class UserInterface:

    def __init__(self):
        self.isrunning = True
        self.table_user_interface = [
            StudentInterface(self),
            CertificateInterface(self),
            ClassInterface(self),
            CourseInterface(self),
            GradeInterface(self),
            StudentCardInterface(self),
            SubjectInterface(self),
            TeacherInterface(self)
        ]

    def run(self):
        while self.isrunning:
            self.menu_input()

    def print_line(self, symbol="="):
        print(symbol * 50)

    def print_message(self, message):
        self.print_line()
        print(message)

    def new_input(self,message):
        self.print_line()
        new_input = None
        while (new_input == None):
            new_input = input(f"{message}: ").strip()
            if (len(new_input) < 1):
                print("Neplatné zadání musíte zadat nějaký text")
                new_input = None
        return new_input

    def menu_input(self):
        commands = [
            ("Správa Studentů", self.table_user_interface[0].menu_input),
            ("Úprava Certifikátů", self.table_user_interface[1].menu_input),
            ("Úprava Tříd", self.table_user_interface[2].menu_input),
            ("Úprava Kurzů", self.table_user_interface[3].menu_input),
            ("Úprava známek", self.table_user_interface[4].menu_input),
            ("Úprava Studentských karet", self.table_user_interface[5].menu_input),
            ("Úprava Předmětů", self.table_user_interface[6].menu_input),
            ("Správa Učitelů", self.table_user_interface[7].menu_input),
            ("Ukončit program", self.terminate),
        ]

        self.print_line()
        print("Vyberte operaci:")
        num = 0
        for label, action in commands:
            num += 1
            print("\t" + str(num) + ". " + label)

        choosen_num = None
        while (choosen_num == None):
            choosen_num = input("Zadejte číslo příkazu (1-" + str(len(commands)) + "): ").strip()
            try:
                choosen_num = int(choosen_num)
                if (not 0 < choosen_num <= len(commands)):
                    raise Exception()
            except:
                print("Neplatné zadání musíte zadat číslo mezi 1 až " + str(len(commands)))
                choosen_num = None

        commands[choosen_num - 1][1]()
    
    def terminate(self):
        self.isrunning = False
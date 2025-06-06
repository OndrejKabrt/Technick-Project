from Clases.Student.StudentApplication import StudentApplication


class StudentInterface:
    def __init__(self, interface):
        self.is_running = True
        self.interface = interface
        self.student_application = StudentApplication(self)

    def run(self):
        self.is_running = True
        while self.is_running:
            self.menu_input()

    def print_message(self, message):
        self.interface.print_line()
        print(message)

    def menu_input(self):
        commands = [
            ("Vložit", self.student_application.insertStudent),
            ("Smazat", self.student_application.deleteStudent),
            ("Seznam všech studentů", self.student_application.listStudents),
            ("Seznam aktivních studentů", self.student_application.listActiveStudents),
            ("Změna třídy studenta", self.student_application.changeStudentClass),
            ("Vypsání studentů jedné třídy", self.student_application.getStudentsInClass),
            ("Vyřazení studenta", self.student_application.setPreviousStudent),
            ("Zpět", self.terminate)
        ]

        self.interface.print_line()
        print("Vyberte operaci:")
        number = 0
        for label, action in commands:
            number = number + 1
            print(f"{number}. {label}")

        choosen_number = None
        while choosen_number is None:
            choosen_number = input("Zadejte číslo příkazu (1-" + str(len(commands)) + "): ").strip()
            try:
                choosen_num = int(choosen_number)
                if not 0 < choosen_num <= len(commands):
                    raise Exception()
            except:
                print("Neplatné zadání musíte zadat číslo mezi 1 až " + str(len(commands)))
                choosen_number = None

        commands[choosen_num - 1][1]()
        if self.is_running:
            self.run()

    def terminate(self):
        self.is_running = False

    def process_input(self, message):
        return self.interface.new_input(message)
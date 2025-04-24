from Clases.Teacher.TeacherApplication import TeacherApplication

class TeacherInterface:
    def __init__(self, interface):
        self.is_running = True
        self.interface = interface
        self.teacher_application = TeacherApplication(self)

    def run(self):
        self.is_running = True
        while self.is_running:
            self.menu_input()

    def print_message(self, message):
        self.interface.print_line()
        print(message)

    def menu_input(self):
        commands = [
            ("Vložit", self.teacher_application.insertTeacher),
            ("Smazat", self.teacher_application.deleteTeacher),
            ("List teachers", self.teacher_application.listTeachers),
            ("Get teachers certificates", self.teacher_application.getTeachersCertificates),
            ("Add certificate to teacher", self.teacher_application.addCertificateToTeacher),
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
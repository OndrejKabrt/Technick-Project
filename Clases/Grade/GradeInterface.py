from Clases.Grade.GradeApplication import GradeApplication

class GradeInterface:
    def __init__(self, interface):
        self.is_running = True
        self.interface = interface
        self.grade_application = GradeApplication(self)

    def run(self):
        self.is_running = True
        while self.is_running:
            self.menu_input()

    def print_message(self, message):
        self.interface.print_line()
        print(message)

    def menu_input(self):
        commands = [
            ("Vložit", self.grade_application.insertGrade),
            ("List course grades", self.grade_application.listCourseGrades),
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
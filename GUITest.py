import dearpygui.dearpygui as dpg
from Clases.Certificate.CertificateApplication import CertificateApplication


class CertificateGUI:
    def __init__(self):
        self.certificate_application = CertificateApplication(self)

        # Inicializace DearPyGui
        dpg.create_context()
        dpg.create_viewport(title="Certificate Management", width=800, height=600)
        dpg.setup_dearpygui()

        # Nastaveni barev a tematu
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [89, 149, 253])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [119, 169, 255])
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [59, 129, 233])
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, [35, 44, 59])
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, [45, 60, 90])
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, [45, 60, 90])
                dpg.add_theme_color(dpg.mvThemeCol_Text, [240, 240, 240])
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 6)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 6)

        dpg.bind_theme(global_theme)

        # Vytvoreni hlavniho okna
        with dpg.window(label="Certificate Management", tag="main_window"):
            with dpg.group(horizontal=False):
                # Nadpis
                dpg.add_spacer(height=15)
                dpg.add_text("Certificate Management System", color=[255, 255, 255])
                dpg.add_text("Select an option to proceed", color=[180, 180, 180])
                dpg.add_separator()
                dpg.add_spacer(height=20)

                # Tlacitka pro akce v kontejneru
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=150)
                    with dpg.group(horizontal=False):
                        dpg.add_button(label="Insert Certificate",
                                       callback=self.certificate_application.insertCertificate,
                                       width=300, height=40)
                        dpg.add_spacer(height=10)
                        dpg.add_button(label="List All Certificates", callback=self.list_certificates,
                                       width=300, height=40)
                        dpg.add_spacer(height=10)
                        dpg.add_button(label="Exit", callback=lambda: dpg.stop_dearpygui(),
                                       width=300, height=40)

        # Okno pro zobrazeni seznamu certifikatu
        with dpg.window(label="Certificate List", show=False, tag="certificate_list_window",
                        width=700, height=500, pos=[50, 50], no_close=True):
            with dpg.group(horizontal=False, tag="certificate_list_container"):
                dpg.add_text("List of Certificates", color=[255, 255, 255])
                dpg.add_separator()

                # Tabulka bude pridana dynamicky

                dpg.add_spacer(height=10)
                dpg.add_button(label="Close",
                               callback=lambda: dpg.configure_item("certificate_list_window", show=False),
                               width=120, height=30)

        # Pro dialogy a zpravy
        with dpg.window(label="Information", show=False, tag="dialog_window", modal=True,
                        width=500, height=250, pos=[100, 100], no_resize=True):
            with dpg.group(horizontal=False):
                dpg.add_spacer(height=15)
                dpg.add_text("", tag="dialog_message", wrap=480)
                dpg.add_spacer(height=20)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=180)
                    dpg.add_button(label="OK", callback=lambda: dpg.configure_item("dialog_window", show=False),
                                   width=140, height=35)

        # Pro vstupni dialog
        with dpg.window(label="Input Required", show=False, tag="input_window", modal=True,
                        width=500, height=250, pos=[100, 100], no_resize=True):
            with dpg.group(horizontal=False):
                dpg.add_spacer(height=15)
                dpg.add_text("", tag="input_message", wrap=480)
                dpg.add_spacer(height=10)
                dpg.add_input_text(tag="input_value", width=460, height=30)
                dpg.add_spacer(height=20)
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=120)
                    dpg.add_button(label="OK", callback=self._on_input_submit, width=140, height=35)
                    dpg.add_spacer(width=10)
                    dpg.add_button(label="Cancel", callback=lambda: dpg.configure_item("input_window", show=False),
                                   width=140, height=35)

        # Promenna pro ulozeni vstupu
        self.input_result = None
        self.input_submitted = False

    def run(self):
        # Centrovani oken na obrazovce
        dpg.set_viewport_resize_callback(self._center_main_window)

        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)

        self._center_main_window(None, None, None)

        dpg.start_dearpygui()
        dpg.destroy_context()

    def list_certificates(self):
        # Ziskani seznamu certifikatu - predpokladame, ze tato metoda ted vraci seznam objektu
        certificates = self.certificate_application.listCertificates()

        # Pokud metoda nic nevraci nebo vraci None, zobrazime zpravu
        if certificates is None or certificates == 0:
            self.print_message("No certificates found.")
            return

        # Odstranime existujici tabulku, pokud existuje
        if dpg.does_item_exist("certificate_table"):
            dpg.delete_item("certificate_table")

        # Vytvorime novou tabulku pro certifikaty
        with dpg.table(tag="certificate_table", parent="certificate_list_container", header_row=True,
                       borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True,
                       scrollY=True, height=350, width=650):

            # Predpokladame strukturu certifikatu - muzete upravit dle skutecnych atributu
            dpg.add_table_column(label="ID")
            dpg.add_table_column(label="Name")
            dpg.add_table_column(label="Expiration Date")
            dpg.add_table_column(label="Status")

            # Pridani radku pro kazdy certifikat
            for cert in range(len(certificates)):
                with dpg.table_row():
                    # Tyto atributy upravte podle skutecne struktury vaseho objektu certifikatu
                    dpg.add_text(str(getattr(cert, 'id', certificates[cert].id)))
                    dpg.add_text(str(getattr(cert, 'name', certificates[cert].certificate_name)))
                    dpg.add_text(str(getattr(cert, 'expiration_date', certificates[cert].issuing_organization)))
                    dpg.add_text(str(getattr(cert, 'status', certificates[cert].description)))

        # Centrovani a zobrazeni okna se seznamem
        self._center_dialog("certificate_list_window")
        dpg.configure_item("certificate_list_window", show=True)

    def _center_main_window(self, sender, app_data, user_data):
        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()

        # Centrovani hlavniho okna
        dpg.configure_item("main_window", width=viewport_width, height=viewport_height)

    def print_message(self, message):
        # Nastaveni zpravy a centrovani dialogu
        dpg.set_value("dialog_message", message)
        self._center_dialog("dialog_window")
        dpg.configure_item("dialog_window", show=True)

    def process_input(self, message):
        # Nastaveni zpravy a centrovani dialogu
        dpg.set_value("input_message", message)
        dpg.set_value("input_value", "")
        self._center_dialog("input_window")

        # Zobrazeni dialogu
        dpg.configure_item("input_window", show=True)

        # Reset flagu
        self.input_submitted = False

        # Cekani na vstup (blokujici)
        while not self.input_submitted and dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()

        # Vraceni vysledku
        return self.input_result if self.input_submitted else None

    def _center_dialog(self, dialog_tag):
        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()

        dialog_width = dpg.get_item_width(dialog_tag)
        dialog_height = dpg.get_item_height(dialog_tag)

        pos_x = (viewport_width - dialog_width) // 2
        pos_y = (viewport_height - dialog_height) // 2

        dpg.configure_item(dialog_tag, pos=[pos_x, pos_y])

    def _on_input_submit(self):
        self.input_result = dpg.get_value("input_value")
        self.input_submitted = True
        dpg.configure_item("input_window", show=False)

    def print_line(self):
        # V GUI tuto funkci nepotrebujeme, ale implementujeme ji pro kompatibilitu
        pass


if __name__ == "__main__":
    app = CertificateGUI()
    app.run()
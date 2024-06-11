import ttkbootstrap as tb
from ttkbootstrap import *
from fractions import Fraction

# Styles
THEME_WINDOW = "morph"
TITLE_WINDOW = "Desglose P65"
THEME_LABEL_TITLE = "dark"
FRAME_DESGLOSE = "primary"
ENTRY_STYLE = "info"
MAIN_FRAME_STYLE = "dark"
WIDTH_LABELS_FRAME_DESGLOSE = 7

FONT_COLOR_LETTERS = "#01204E"
FONT_LETTERS = ("Arial", 11, "bold")


class App(tb.Window):
    def __init__(self):
        super().__init__(themename=THEME_WINDOW)
        self.fila_cantidad = 2
        self.title(TITLE_WINDOW)
        self.geometry("1350x700+0+0")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # El menú no se debe expandir
        self.grid_columnconfigure(1, weight=1)  # El canvas debe ocupar todo el espacio restante

        # Crear un Canvas para scroll
        self.canvas = Canvas(self, background="red")
        self.canvas.grid(row=0, column=1, columnspan=2, sticky="nsew")

        # Añadir el scrollbar al canvas
        self.scrollbar = tb.Scrollbar(self, orient="vertical", command=self.canvas.yview, bootstyle="dark-round")
        self.scrollbar.grid(row=0, column=2, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Crear el frame dentro del canvas
        self.main_frame = Frame(self.canvas, bootstyle="info", padding=10)
        self.main_frame_id = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        # Ajustar el tamaño del canvas al contenido
        self.main_frame.bind("<Configure>", self.on_frame_configure)

        # Centrando horizontalmente el main_frame en el Canvas
        self.center_frame_horizontally_in_canvas()

        # Diccionarios para almacenar distintos datos
        self.alto_values = {}
        self.ancho_values = {}
        self.results = {}
        self.labels = {}

        self.starting_app()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def center_frame_horizontally_in_canvas(self):
        # Método para centrar horizontalmente el frame en el canvas
        canvas_width = self.canvas.winfo_width()
        frame_width = self.main_frame.winfo_reqwidth()

        # Centrando horizontalmente el main_frame en el canvas
        self.canvas.coords(self.main_frame_id, (canvas_width - frame_width) / 2, 0)

        # Vinculando el evento de redimensionamiento del canvas para re-centrar horizontalmente el main_frame
        self.canvas.bind("<Configure>", self.update_frame_horizontal_position)

    def update_frame_horizontal_position(self, event):
        # Recalcular la posición horizontal del frame cada vez que el canvas cambia de tamaño
        canvas_width = event.width
        frame_width = self.main_frame.winfo_reqwidth()

        # Mantener la coordenada y original (0) y centrar solo horizontalmente
        self.canvas.coords(self.main_frame_id, (canvas_width - frame_width) / 2, 0)

    def starting_app(self):
        self.text_title()
        self.painting_frame()
        self.buttons()

    def text_title(self):
        title = tb.Label(self.main_frame, bootstyle="secondary", text="Desglose P65", font=FONT_LETTERS,
                         anchor="center",
                         width=20, foreground=FONT_COLOR_LETTERS)
        title.grid(row=0, column=0, pady=10)

    def painting_frame(self):
        num = 1
        for row in range(1, self.fila_cantidad):
            for column in range(0, 4):
                self.frame_desglose_static(num, row, column)
                num += 1

    def frame_desglose_static(self, num, row, column):
        frame_desglose = Frame(self.main_frame, bootstyle=FRAME_DESGLOSE, padding=10)
        frame_desglose.grid(row=row, column=column, padx=5, pady=5)

        numero_label = tb.Label(frame_desglose, text="Nº", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE,
                                font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        numero_label.grid(row=0, column=0)

        numero_desglose = tb.Entry(frame_desglose, justify="center", font=FONT_LETTERS, width=3,
                                   bootstyle=ENTRY_STYLE, foreground=FONT_COLOR_LETTERS)
        numero_desglose.insert(0, num)
        numero_desglose.grid(row=0, column=1)

        ancho_label = tb.Label(frame_desglose, text="Ancho", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE,
                               font=FONT_LETTERS,
                               foreground=FONT_COLOR_LETTERS)
        ancho_label.grid(row=1, column=0, pady=2)

        alto_label = tb.Label(frame_desglose, bootstyle="secondary", text="Alto", anchor="center",
                              width=WIDTH_LABELS_FRAME_DESGLOSE,
                              font=FONT_LETTERS,
                              foreground=FONT_COLOR_LETTERS)
        alto_label.grid(row=1, column=1, pady=2)

        # Crear entries
        self.create_ancho_values(frame_desglose, 'ancho', num)
        self.create_alto_values(frame_desglose, 'alto', num)

        # Riel y Cabezal
        riel_cabezal = tb.Label(frame_desglose, text="RC", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE,
                                padding=2, font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS, bootstyle="secondary")
        riel_cabezal.grid(row=3, column=0, padx=5, pady=1)
        # Ruleta
        ruleta = tb.Label(frame_desglose, text="Ruleta", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE,
                          padding=2, font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        ruleta.grid(row=4, column=0, padx=5, pady=1)

        # Lateral
        lateral = tb.Label(frame_desglose, text="Lateral", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE,
                           padding=2, font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        lateral.grid(row=5, column=0, padx=5, pady=1)

        # Jamba
        jamba = tb.Label(frame_desglose, text="Jamba", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE,
                         padding=2, font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        jamba.grid(row=6, column=0, padx=5, pady=1)

        # Cristal Ancho
        cristal_ancho = tb.Label(frame_desglose, text="C.AN", anchor="center",
                                 width=WIDTH_LABELS_FRAME_DESGLOSE,
                                 padding=2, font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        cristal_ancho.grid(row=7, column=0, padx=5, pady=1)

        # Cristal Largo
        cristal_alto = tb.Label(frame_desglose, text="C.AL", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE,
                                padding=2, font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        cristal_alto.grid(row=8, column=0, padx=5, pady=1)

        # Results
        self.labels[f'desglose_{num}'] = {}
        # Riel y cabezal
        rc = tb.Label(frame_desglose, text="", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE, padding=2,
                      font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        rc.grid(row=3, column=1, padx=5, pady=1)
        self.labels[f'desglose_{num}']['Riel y Cabezal'] = rc

        # Ruleta
        r = tb.Label(frame_desglose, text="", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE, padding=2,
                     font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        r.grid(row=4, column=1, padx=5, pady=1)
        self.labels[f'desglose_{num}']['Ruleta'] = r

        # Lateral
        l = tb.Label(frame_desglose, text="", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE, padding=2,
                     font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        l.grid(row=5, column=1, padx=5, pady=1)
        self.labels[f'desglose_{num}']['Lateral'] = l

        # Jamba
        j = tb.Label(frame_desglose, text="", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE, padding=2,
                     font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        j.grid(row=6, column=1, padx=5, pady=1)
        self.labels[f'desglose_{num}']['Jamba'] = j

        # Cristal Ancho
        can = tb.Label(frame_desglose, text="", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE, padding=2,
                       font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        can.grid(row=7, column=1, padx=5, pady=1)
        self.labels[f'desglose_{num}']['Cristal Ancho'] = can

        # Cristal Alto
        cal = tb.Label(frame_desglose, text="", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE, padding=2,
                       font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        cal.grid(row=8, column=1, padx=5, pady=1)
        self.labels[f'desglose_{num}']['Cristal Alto'] = cal

    def create_ancho_values(self, frame, entry_type, num):
        entry = tb.Entry(frame, justify="center", font=FONT_LETTERS, width=7, bootstyle=ENTRY_STYLE,
                         foreground=FONT_COLOR_LETTERS)
        entry.grid(row=2, column=0, pady=5)
        self.ancho_values[f'{entry_type}_{num}'] = entry

    def create_alto_values(self, frame, entry_type, num):
        entry = tb.Entry(frame, justify="center", font=FONT_LETTERS, width=7, bootstyle=ENTRY_STYLE,
                         foreground=FONT_COLOR_LETTERS)
        entry.grid(row=2, column=1, pady=5)
        self.alto_values[f'{entry_type}_{num}'] = entry

    def update_data(self):
        # Pasando datos a diccionario interno
        ancho_values = {}
        for key, entry in self.ancho_values.items():
            ancho_values[key] = entry.get()

        # Pasando datos a diccionario interno
        alto_values = {}
        for key, entry in self.alto_values.items():
            alto_values[key] = entry.get()

        # Sumar los valores correspondientes
        num = 1
        for i in range(1, len(alto_values) + 1):
            clave_ancho = f"ancho_{i}"
            clave_alto = f"alto_{i}"
            # Obtener los valores correspondientes
            valor_ancho = str(ancho_values.get(clave_ancho, 0))
            valor_alto = str(alto_values.get(clave_alto, 0))
            self.mixto_math(valor_ancho, valor_alto, num)
            num += 1

        # Actualizar las etiquetas con los nuevos valores
        for num, values in self.results.items():
            for key, value in values.items():
                self.labels[num][key].config(text=value)


    def mixto_math(self, ancho, alto, num):
        # La f al final de la variable significa fraction
        ancho_f = sum(Fraction(s) for s in ancho.split())
        alto_f = sum(Fraction(s) for s in alto.split())

        # Riel y Cabezal
        resto_rc = "1 3/8"
        resto_rc_f = sum(Fraction(s) for s in resto_rc.split())
        rc = ancho_f - resto_rc_f
        rc = self.decimal_to_fraction_inches(rc)

        # Ruleta
        resto_r = "1 1/8"
        resto_r_f = sum(Fraction(s) for s in resto_r.split())
        r = (ancho_f - resto_r_f) / 2
        r = self.decimal_to_fraction_inches(r)

        # Lateral
        resto_l = "1/8"
        resto_l_f = sum(Fraction(s) for s in resto_l.split())
        l = alto_f - resto_l_f
        l = self.decimal_to_fraction_inches(l)

        # Jamba
        resto_j = "2 1/8"
        resto_j_f = sum(Fraction(s) for s in resto_j.split())
        j = alto_f - resto_j_f
        j = self.decimal_to_fraction_inches(j)

        # Cristal ancho
        resto_can = "6 1/2"
        resto_can_f = sum(Fraction(s) for s in resto_can.split())
        can = (ancho_f - resto_can_f) / 2
        can = self.decimal_to_fraction_inches(can)
        print(ancho)
        # Cristal alto
        cal = alto_f - 5
        cal = self.decimal_to_fraction_inches(cal)
        self.results[f'desglose_{num}'] = {
            "Riel y Cabezal": rc,
            "Ruleta": r,
            "Lateral": l,
            "Jamba": j,
            "Cristal Ancho": can,
            "Cristal Alto": cal
        }

    def buttons(self):
        agregar_fila = tb.Button(self, text="+", command=self.sum_fila, bootstyle="info")
        agregar_fila.grid(row=3, column=3)
        calculate_button = tb.Button(self, text="Obtener Valores", command=self.update_data, bootstyle="success")
        calculate_button.grid(row=3, column=1, pady=10)

    def sum_fila(self):
        # Guardar los valores actuales de los entries antes de agregar nuevas filas
        current_values_ancho = {key: entry.get() for key, entry in self.ancho_values.items()}
        current_values_alto = {key: entry.get() for key, entry in self.alto_values.items()}

        self.fila_cantidad += 1
        self.painting_frame()

        # Restaurar los valores de los entries existentes
        for key, value in current_values_ancho.items():
            self.ancho_values[key].delete(0, END)
            self.ancho_values[key].insert(0, value)

        for key, value in current_values_alto.items():
            self.alto_values[key].delete(0, END)
            self.alto_values[key].insert(0, value)

        self.update_data()

    @staticmethod
    def decimal_to_fraction_inches(value):
        # Separar la parte entera y la parte decimal
        whole_part = int(value)
        decimal_part = value - whole_part

        # Redondear la parte decimal a la fracción más cercana de 1/16
        fraction_part = round(decimal_part * 16) / 16
        fraction_part = Fraction(fraction_part).limit_denominator(16)

        # Combinar la parte entera con la fracción
        if fraction_part.numerator == 0:
            return f"{whole_part}"
        elif whole_part == 0:
            return f"{fraction_part}"
        else:
            return f"{whole_part} {fraction_part}"


if __name__ == "__main__":
    app = App()
    app.mainloop()

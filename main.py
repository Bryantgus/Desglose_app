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

        # Crear el frame dentro del canvas
        self.main_frame = Frame(self, bootstyle="info", padding=10)
        self.main_frame.grid(row=0, column=0, columnspan=3)

        # Diccionarios que almacena los valores que cambiaran de cada frame
        self.ancho_entry = {}
        self.alto_entry = {}
        self.num_entry = {}
        self.labels_results = {}
        # Dicionarios que almacenan los datos de los frames
        self.ancho_values = {}
        self.alto_values = {}
        self.results = {}
        self.starting_app()

        self.actual_label = 1

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
        for row in range(1, 3):
            for column in range(0, 4):
                self.frame_desglose(num, row, column)
                num += 1

    def buttons(self):
        calculate_button = tb.Button(self, text="Obtener Valores", command=self.get_values_entrys(),
                                     bootstyle="dark")
        calculate_button.grid(row=1, column=1)
        next_page = tb.Button(self, text=">", command=lambda: self.pagination(">"), bootstyle="dark")
        next_page.grid(row=1, column=2)
        back_page = tb.Button(self, text="<", command=lambda: self.pagination("<"), bootstyle="dark")
        back_page.grid(row=1, column=0)

    def frame_desglose(self, num, row, column):
        frame_desglose = Frame(self.main_frame, bootstyle=FRAME_DESGLOSE, padding=10)
        frame_desglose.grid(row=row, column=column, padx=5, pady=5)

        numero_label = tb.Label(frame_desglose, text="Nº", anchor="center",
                                width=WIDTH_LABELS_FRAME_DESGLOSE,
                                font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        numero_label.grid(row=0, column=0)

        numero_desglose = tb.Entry(frame_desglose, justify="center", font=FONT_LETTERS, width=3,
                                   bootstyle=ENTRY_STYLE, foreground=FONT_COLOR_LETTERS)
        numero_desglose.grid(row=0, column=1)
        self.num_entry[f"entry_{num}"] = numero_desglose

        numero_desglose.insert(0, num)

        ancho_label = tb.Label(frame_desglose, text="Ancho", anchor="center",
                               width=WIDTH_LABELS_FRAME_DESGLOSE,
                               font=FONT_LETTERS,
                               foreground=FONT_COLOR_LETTERS)
        ancho_label.grid(row=1, column=0, pady=2)

        alto_label = tb.Label(frame_desglose, bootstyle="secondary", text="Alto", anchor="center",
                              width=WIDTH_LABELS_FRAME_DESGLOSE,
                              font=FONT_LETTERS,
                              foreground=FONT_COLOR_LETTERS)
        alto_label.grid(row=1, column=1, pady=2)

        # Crear entries
        ancho_entry = tb.Entry(frame_desglose, justify="center", font=FONT_LETTERS, width=7,
                               bootstyle=ENTRY_STYLE,
                               foreground=FONT_COLOR_LETTERS)
        ancho_entry.grid(row=2, column=0, pady=5)
        self.ancho_entry[f'ancho_{num}'] = ancho_entry

        alto_entry = tb.Entry(frame_desglose, justify="center", font=FONT_LETTERS, width=7, bootstyle=ENTRY_STYLE,
                              foreground=FONT_COLOR_LETTERS)
        alto_entry.grid(row=2, column=1, pady=5)
        self.alto_entry[f'alto_{num}'] = alto_entry

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

        self.labels_results[f'desglose_{num}'] = {}
        # Riel y cabezal
        rc = tb.Label(frame_desglose, text="", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE, padding=2,
                      font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        rc.grid(row=3, column=1, padx=5, pady=1)
        self.labels_results[f'desglose_{num}']['Riel y Cabezal'] = rc

        # Ruleta
        r = tb.Label(frame_desglose, text="", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE, padding=2,
                     font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        r.grid(row=4, column=1, padx=5, pady=1)
        self.labels_results[f'desglose_{num}']['Ruleta'] = r

        # Lateral
        l = tb.Label(frame_desglose, text="", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE, padding=2,
                     font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        l.grid(row=5, column=1, padx=5, pady=1)
        self.labels_results[f'desglose_{num}']['Lateral'] = l

        # Jamba
        j = tb.Label(frame_desglose, text="", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE, padding=2,
                     font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        j.grid(row=6, column=1, padx=5, pady=1)
        self.labels_results[f'desglose_{num}']['Jamba'] = j

        # Cristal Ancho
        can = tb.Label(frame_desglose, text="", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE, padding=2,
                       font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        can.grid(row=7, column=1, padx=5, pady=1)
        self.labels_results[f'desglose_{num}']['Cristal Ancho'] = can

        # Cristal Alto
        cal = tb.Label(frame_desglose, text="", anchor="center", width=WIDTH_LABELS_FRAME_DESGLOSE, padding=2,
                       font=FONT_LETTERS, foreground=FONT_COLOR_LETTERS)
        cal.grid(row=8, column=1, padx=5, pady=1)
        self.labels_results[f'desglose_{num}']['Cristal Alto'] = cal

    def get_values_entrys(self):
        self.actual_label = int(self.num_entry[f"entry_1"].get())
        # Pasando datos a diccionario interno
        ancho_values = {}
        num1 = 1
        for key, entry in self.ancho_entry.items():
            ancho_values[key] = entry.get()
            num1 += 1
        # Pasando datos a diccionario interno
        alto_values = {}
        num2 = 1
        for key, entry in self.alto_entry.items():
            alto_values[key] = entry.get()
            num2 += 1

        for i in range(self.actual_label, self.actual_label + 8):
            clave_ancho = f"ancho_{i}"
            clave_alto = f"alto_{i}"
            # Obtener los valores correspondientes
            valor_ancho = str(ancho_values.get(clave_ancho, 0))
            valor_alto = str(alto_values.get(clave_alto, 0))
            self.mixto_math(valor_ancho, valor_alto, i)



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
        self.results[f'desglose_{num + 8}'] = {
            "Riel y Cabezal": None,
            "Ruleta": None,
            "Lateral": None,
            "Jamba": None,
            "Cristal Ancho": None,
            "Cristal Alto": None
        }

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

    def pagination(self, next_or_previous):
        # Guardando datos de los entrys ancho y alto
        actual_label = self.actual_label
        for key in self.ancho_entry:
            self.ancho_values[f'ancho_{actual_label}'] = self.ancho_entry[key].get()
            actual_label += 1
        actual_label = self.actual_label
        for key in self.alto_entry:
            self.alto_values[f'alto_{actual_label}'] = self.alto_entry[key].get()
            actual_label += 1
        # Guardando datos de los labels results
        # actual_label = self.actual_label
        # for a in range(1, 9):
            # self.results[f'desglose_{actual_label}']["Riel y Cabezal"] = self.labels_results[f'desglose_{a}']["Riel y Cabezal"].get()
            #
            # actual_label += 1

        if next_or_previous == "<":
            if self.actual_label != 1:
                self.actual_label -= 8
        else:
            self.actual_label += 8

        num = self.actual_label
        # Actualizando el número de desgloses
        for a in range(1, 9):
            self.num_entry[f'entry_{a}'].delete(0, tk.END)
            self.num_entry[f'entry_{a}'].insert(0, num)

            # Verificar si es la primera vez que se visita este rango de labels
            if f'ancho_{num}' not in self.ancho_values:
                # Primera vez: asignar valores nulos
                self.ancho_entry[f'ancho_{a}'].delete(0, tk.END)
                self.ancho_entry[f'ancho_{a}'].insert(0, "")
                self.alto_entry[f'alto_{a}'].delete(0, tk.END)
                self.alto_entry[f'alto_{a}'].insert(0, "")
            else:
                # Ya visitado: cargar los valores almacenados
                self.ancho_entry[f'ancho_{a}'].delete(0, tk.END)
                self.ancho_entry[f'ancho_{a}'].insert(0, self.ancho_values[f'ancho_{num}'])
                self.alto_entry[f'alto_{a}'].delete(0, tk.END)
                self.alto_entry[f'alto_{a}'].insert(0, self.alto_values[f'alto_{num}'])
            num += 1

        # Después de actualizar los campos de entrada, llamar a get_values_entrys para recalcular y actualizar los resultados
        self.get_values_entrys()


if __name__ == "__main__":
    app = App()
    app.mainloop()

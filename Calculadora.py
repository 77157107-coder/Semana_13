"""
calculadora.py
Calculadora básica con GUI - Semana 13
"""
import tkinter as tk
from tkinter import messagebox
import re


class Calculadora:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Calculadora - Semana 13")
        self.ventana.geometry("340x480")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#1e1e1e")

        self._crear_display()
        self._crear_botones()
        self._configurar_atajos()

        self.display.focus_set()

    # ------------------------------------------------------------------
    def _crear_display(self):
        self.display = tk.Entry(
            self.ventana, font=("Arial", 24), justify="right",
            bd=0, bg="#ffffff", fg="#000000", insertbackground="#000000"
        )
        self.display.grid(
            row=0, column=0, columnspan=4,
            sticky="nsew", padx=8, pady=8, ipady=12
        )
        self.display.configure(takefocus=1)

    def _crear_botones(self):
        # Botones con * y / para que coincidan con lo que se escribe en el display
        botones = [
            ('C',  '⌫',  '(',  ')'),
            ('7',  '8',  '9',  '/'),
            ('4',  '5',  '6',  '*'),
            ('1',  '2',  '3',  '-'),
            ('0',  '.',  '=',  '+'),
        ]
        colores = {
            'operador': ('#ff9500', 'white'),
            'funcion':  ('#a5a5a5', 'black'),
            'numero':   ('#333333', 'white'),
        }

        for i, fila in enumerate(botones):
            for j, texto in enumerate(fila):
                if texto in '/*-+=':
                    bg, fg = colores['operador']
                elif texto in ('C', '⌫', '(', ')'):
                    bg, fg = colores['funcion']
                else:
                    bg, fg = colores['numero']

                tk.Button(
                    self.ventana, text=texto,
                    font=("Arial", 16, "bold"),
                    bg=bg, fg=fg, bd=0,
                    activebackground="#555555",
                    width=4, height=2,
                    command=lambda t=texto: self.click(t),
                    takefocus=1
                ).grid(row=i + 1, column=j, padx=3, pady=3, sticky="nsew")

        for i in range(6):
            self.ventana.rowconfigure(i, weight=1)
        for j in range(4):
            self.ventana.columnconfigure(j, weight=1)

    # ------------------------------------------------------------------
    def _configurar_atajos(self):
        self.ventana.bind("<Return>",    lambda e: self.click("="))
        self.ventana.bind("<KP_Enter>",  lambda e: self.click("="))
        self.ventana.bind("<BackSpace>", lambda e: self.click("⌫"))
        self.ventana.bind("<Escape>",    lambda e: self.click("C"))
        self.ventana.bind("<Delete>",    lambda e: self.click("C"))
        self.ventana.bind("<Key>",       self._on_key)

    def _on_key(self, event):
        if event.char in "0123456789+-*/().":
            self.click(event.char)

    # ------------------------------------------------------------------
    def click(self, valor):
        actual = self.display.get()

        if valor == 'C':
            self._set_texto("")
        elif valor == '⌫':
            self._set_texto(actual[:-1])
        elif valor == '=':
            self._calcular(actual)
        else:
            self._set_texto(actual + valor)

    def _calcular(self, expresion):
        if not expresion.strip():
            return

        # Validación 1: solo caracteres permitidos
        if not re.fullmatch(r"[0-9+\-*/(). ]+", expresion):
            messagebox.showerror("Error", "Expresión inválida")
            self._set_texto("")
            return

        # Validación 2: rechazar operadores consecutivos (++, --, **, //, etc.)
        # Esto hace que "++" Y "6++3" fallen (Python evaluaría "6++3" como 9)
        if re.search(r"[+\-*/]{2,}", expresion):
            messagebox.showerror(
                "Error", "Expresión inválida: operadores consecutivos"
            )
            self._set_texto("")
            return

        try:
            resultado = eval(expresion, {"__builtins__": {}}, {})

            # Formateo: entero si aplica, si no máximo 3 decimales
            if isinstance(resultado, float):
                if resultado.is_integer():
                    resultado = int(resultado)
                else:
                    resultado = round(resultado, 3)

            self._set_texto(str(resultado))
        except ZeroDivisionError:
            messagebox.showerror("Error", "No se puede dividir por 0")
            self._set_texto("")
        except Exception:
            messagebox.showerror("Error", "Expresión inválida")
            self._set_texto("")

    def _set_texto(self, texto):
        self.display.delete(0, tk.END)
        self.display.insert(0, texto)
        self.display.xview_moveto(1)
        self.display.update_idletasks()

    # ------------------------------------------------------------------
    def run(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    Calculadora().run()

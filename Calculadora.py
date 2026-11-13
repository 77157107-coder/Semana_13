"""
calculadora.py
Calculadora básica con GUI - Semana 13
Botones con esquinas redondeadas (Canvas).
"""
import tkinter as tk
from tkinter import messagebox
import re


# ----------------------------------------------------------------------
#  Botón con esquinas redondeadas dibujado sobre un Canvas
# ----------------------------------------------------------------------
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, bg, fg,
                 w=68, h=56, radius=14,
                 font=("Arial", 16, "bold"), parent_bg="#1e1e1e"):
        super().__init__(parent, width=w, height=h, bg=parent_bg,
                         highlightthickness=0, bd=0, takefocus=1)
        self.command  = command
        self.label    = text          # 'label' evita choque con tk.Canvas.text
        self.bg_color = bg
        self.fg_color = fg
        self.radius   = radius
        self.font     = font
        self.btn_w    = w
        self.btn_h    = h

        self._draw()
        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Return>",   lambda e: self.command())
        self.bind("<space>",    lambda e: self.command())
        self.bind("<Enter>",    self._hover_in)
        self.bind("<Leave>",    self._hover_out)

    def _draw(self, hover=False):
        self.delete("all")
        w, h, r = self.btn_w, self.btn_h, self.radius
        bg = self._lighten(self.bg_color) if hover else self.bg_color

        self.create_oval(0,      0,      2*r, 2*r, fill=bg, outline=bg)
        self.create_oval(w-2*r,  0,      w,   2*r, fill=bg, outline=bg)
        self.create_oval(0,      h-2*r,  2*r, h,   fill=bg, outline=bg)
        self.create_oval(w-2*r,  h-2*r,  w,   h,   fill=bg, outline=bg)
        self.create_rectangle(r, 0, w-r, h,   fill=bg, outline=bg)
        self.create_rectangle(0, r, w,   h-r, fill=bg, outline=bg)
        self.create_text(w//2, h//2, text=self.label,
                         fill=self.fg_color, font=self.font)

    def _lighten(self, hex_color):
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"#{min(255,r+30):02x}{min(255,g+30):02x}{min(255,b+30):02x}"

    def _hover_in(self, _):
        self._draw(hover=True)

    def _hover_out(self, _):
        self._draw(hover=False)


# ----------------------------------------------------------------------
class Calculadora:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Calculadora - Semana 13")
        self.ventana.geometry("400x580")        # ← más ancho y alto
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

                RoundedButton(
                    self.ventana, text=texto,
                    command=lambda t=texto: self.click(t),
                    bg=bg, fg=fg,
                    parent_bg="#1e1e1e"
                ).grid(row=i + 1, column=j, padx=4, pady=4)

        # Que las celdas se repartan el espacio sobrante (centra los botones)
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

        if not re.fullmatch(r"[0-9+\-*/(). ]+", expresion):
            messagebox.showerror("Error", "Expresión inválida")
            self._set_texto("")
            return

        if re.search(r"[+\-*/]{2,}", expresion):
            messagebox.showerror(
                "Error", "Expresión inválida: operadores consecutivos"
            )
            self._set_texto("")
            return

        try:
            resultado = eval(expresion, {"__builtins__": {}}, {})

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

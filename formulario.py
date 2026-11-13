"""
formulario.py
Formulario de registro con validación - Semana 13
Fondo azul metálico.
"""
import tkinter as tk
from tkinter import messagebox
import re


class FormularioRegistro:
    # Paleta: azul metálico + colores de retroalimentación
    COLOR_VENTANA = "#3d5a80"   # azul metálico
    COLOR_TEXTO   = "#ffffff"   # texto claro sobre azul
    COLOR_OK      = "#d4edda"   # verde claro
    COLOR_ERROR   = "#f8d7da"   # rojo claro
    COLOR_FONDO   = "#ffffff"   # blanco de los Entry

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registro de Usuario - Semana 13")
        self.root.geometry("560x680")
        self.root.configure(bg=self.COLOR_VENTANA)

        self.nombre       = tk.StringVar()
        self.email        = tk.StringVar()
        self.password     = tk.StringVar()
        self.confirm_pass = tk.StringVar()
        self.edad         = tk.StringVar()
        self.genero       = tk.StringVar(value="")
        self.acepto       = tk.BooleanVar()

        self.entries = {}
        self.crear_widgets()
        self.configurar_atajos()

        self.entries["nombre"].focus_set()

    # ------------------------------------------------------------------
    def crear_widgets(self):
        frame = tk.Frame(self.root, padx=25, pady=20, bg=self.COLOR_VENTANA)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame, text="Registro de Usuario",
            font=("Arial", 18, "bold"),
            bg=self.COLOR_VENTANA, fg=self.COLOR_TEXTO
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        campos = [
            ("Nombre completo *:",      "nombre",       False),
            ("Email *:",                "email",        False),
            ("Contraseña *:",           "password",     True),
            ("Confirmar contraseña *:", "confirm_pass", True),
            ("Edad *:",                 "edad",         False),
        ]

        for i, (label, key, oculto) in enumerate(campos, start=1):
            tk.Label(
                frame, text=label, anchor="e",
                font=("Arial", 10),
                bg=self.COLOR_VENTANA, fg=self.COLOR_TEXTO
            ).grid(row=i, column=0, sticky="e", pady=6, padx=(0, 10))

            entry = tk.Entry(
                frame, textvariable=getattr(self, key), width=35,
                show="*" if oculto else "", font=("Arial", 10),
                relief="solid", bd=1, bg=self.COLOR_FONDO
            )
            entry.grid(row=i, column=1, pady=6, sticky="w", ipady=4)
            entry.bind("<KeyRelease>",
                       lambda e, k=key: self._reset_color(k))
            self.entries[key] = entry

        # Género
        tk.Label(
            frame, text="Género *:", anchor="e",
            font=("Arial", 10),
            bg=self.COLOR_VENTANA, fg=self.COLOR_TEXTO
        ).grid(row=6, column=0, sticky="e", pady=6, padx=(0, 10))

        genero_frame = tk.Frame(frame, bg=self.COLOR_VENTANA)
        genero_frame.grid(row=6, column=1, sticky="w")
        for opcion in ["Masculino", "Femenino", "Otro"]:
            tk.Radiobutton(
                genero_frame, text=opcion, variable=self.genero,
                value=opcion,
                bg=self.COLOR_VENTANA, fg=self.COLOR_TEXTO,
                activebackground=self.COLOR_VENTANA,
                activeforeground=self.COLOR_TEXTO,
                selectcolor=self.COLOR_VENTANA,
                takefocus=1
            ).pack(side="left", padx=5)

        # Checkbox
        tk.Checkbutton(
            frame, text="Acepto los términos y condiciones *",
            variable=self.acepto,
            bg=self.COLOR_VENTANA, fg=self.COLOR_TEXTO,
            activebackground=self.COLOR_VENTANA,
            activeforeground=self.COLOR_TEXTO,
            selectcolor=self.COLOR_VENTANA,
            takefocus=1
        ).grid(row=7, column=0, columnspan=2, pady=12)

        tk.Label(
            frame, text="* Campos obligatorios",
            font=("Arial", 8, "italic"),
            fg="#cfd8dc", bg=self.COLOR_VENTANA
        ).grid(row=8, column=0, columnspan=2, pady=(0, 10))

        # Botones
        btn_frame = tk.Frame(frame, bg=self.COLOR_VENTANA)
        btn_frame.grid(row=9, column=0, columnspan=2, pady=10)
        tk.Button(
            btn_frame, text="Registrar", command=self.validar,
            width=15, bg="#4CAF50", fg="white",
            font=("Arial", 10, "bold"), takefocus=1
        ).pack(side="left", padx=10)
        tk.Button(
            btn_frame, text="Limpiar", command=self.limpiar,
            width=15, font=("Arial", 10), takefocus=1
        ).pack(side="left", padx=10)

    # ------------------------------------------------------------------
    def configurar_atajos(self):
        self.root.bind("<Return>",   lambda e: self.validar())
        self.root.bind("<KP_Enter>", lambda e: self.validar())
        self.root.bind("<Escape>",   lambda e: self.limpiar())

    def _marcar(self, key, ok):
        self.entries[key].configure(
            bg=self.COLOR_OK if ok else self.COLOR_ERROR
        )

    def _reset_color(self, key):
        self.entries[key].configure(bg=self.COLOR_FONDO)

    def _limpiar_marcas(self):
        for entry in self.entries.values():
            entry.configure(bg=self.COLOR_FONDO)

    # ------------------------------------------------------------------
    def validar(self):
        errores = []
        self._limpiar_marcas()

        if not self.nombre.get().strip():
            errores.append("• El nombre es obligatorio")
            self._marcar("nombre", False)
        else:
            self._marcar("nombre", True)

        email = self.email.get().strip()
        patron_email = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"
        if not re.match(patron_email, email):
            errores.append("• Email inválido (ej: usuario@dominio.com)")
            self._marcar("email", False)
        else:
            self._marcar("email", True)

        pwd = self.password.get()
        if len(pwd) < 8:
            errores.append("• La contraseña debe tener mínimo 8 caracteres")
            self._marcar("password", False)
        else:
            self._marcar("password", True)

        confirm = self.confirm_pass.get()
        if not confirm:
            errores.append("• Debe confirmar la contraseña")
            self._marcar("confirm_pass", False)
        elif pwd != confirm:
            errores.append("• Las contraseñas no coinciden")
            self._marcar("confirm_pass", False)
        else:
            self._marcar("confirm_pass", True)

        try:
            edad = int(self.edad.get())
            if not (15 <= edad <= 99):
                errores.append("• La edad debe estar entre 15 y 99")
                self._marcar("edad", False)
            else:
                self._marcar("edad", True)
        except ValueError:
            errores.append("• La edad debe ser un número")
            self._marcar("edad", False)

        if not self.genero.get():
            errores.append("• Seleccione un género")

        if not self.acepto.get():
            errores.append("• Debe aceptar los términos")

        if errores:
            messagebox.showerror(
                "Errores de validación",
                "Corrija lo siguiente:\n\n" + "\n".join(errores)
            )
        else:
            messagebox.showinfo(
                "Registro exitoso",
                f"¡Bienvenido/a, {self.nombre.get()}!\n"
                f"Email: {self.email.get()}\n"
                f"Edad: {self.edad.get()}\n"
                f"Género: {self.genero.get()}"
            )
            self.limpiar()

    def limpiar(self):
        for var in [self.nombre, self.email, self.password,
                    self.confirm_pass, self.edad, self.genero]:
            var.set("")
        self.acepto.set(False)
        self._limpiar_marcas()
        self.entries["nombre"].focus_set()


if __name__ == "__main__":
    app = FormularioRegistro()
    app.root.mainloop()
    
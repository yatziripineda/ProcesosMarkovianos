import tkinter as tk
from tkinter import messagebox, simpledialog, PhotoImage, Menu
import numpy as np
from scipy.optimize import linprog
import tkinter.font as tkfont
from tkinter import ttk



# Clase principal de la aplicación
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Procesos de Decisión de Markov")
        self.root.geometry("1000x800")
        self.root.configure(bg="#DCDAD6")
        self.min = True   # o False, según convenga por defecto


        # --- Estilos ttk ---
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TLabelFrame', background='#DCDAD6', borderwidth=2, relief='groove')
        self.style.configure('TButton', font=('Helvetica', 18), padding=6)
        self.style.configure('Header.TLabel', font=('Arial', 20, 'bold'), background='#DCDAD6')
        self.style.configure('Status.TLabel', relief='sunken', anchor='w')

        # --- Fuente para título ---
        self.title_font = tkfont.Font(family="Arial", size=24, weight="bold")

        

        # --- Barra de estado ---
        self.status_var = tk.StringVar(value="Listo")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, style='Status.TLabel')
        status_bar.pack(side='bottom', fill='x')

        self.inicio()
           

    def inicio(self):
        # Limpia todo
        for widget in self.root.winfo_children():
            if not isinstance(widget, ttk.Label):  # preserva la barra de estado
                widget.destroy()

        # --- Encabezado con ícono y título ---
        header = ttk.Frame(self.root, padding=10, style='TFrame')
        header.pack(fill='x')
        try:
            icon = PhotoImage(file="icon.png")
            lbl_icon = ttk.Label(header, image=icon, background='#f5cac3')
            lbl_icon.image = icon
            lbl_icon.pack(side='left', padx=5)
        except Exception:
            pass  # si falta el icono, simplemente no lo muestra
        lbl_title = ttk.Label(header,
                              text="Procesos Estocásticos: Markovianos de Decisión",
                              style='Header.TLabel')
        lbl_title.pack(side='top', padx=20)

        # --- Sección: Lectura de datos ---
        data_frame = ttk.LabelFrame(self.root, text="Lectura de datos", padding=10)
        data_frame.pack(padx=20, pady=10, fill='x')
        ttk.Button(data_frame, text="Leer datos", width=40, command=self.abrir_lectura_datos)\
            .pack(side='left', padx=5, pady=5)
        ttk.Button(data_frame, text="Mostrar datos", width=40, command=self.mostrar_datos_ingresados)\
            .pack(side='left', padx=5, pady=5)
            
        # --- Sección: Ejercicios prueba ---
        data_frame = ttk.LabelFrame(self.root, text="Ejercicios prueb", padding=10)
        data_frame.pack(padx=20, pady=10, fill='x')
        ttk.Button(data_frame, text="Cargar ejemplo", width=25, command=self.cargar_ejemplo_datos)\
            .pack(side='left', padx=5, pady=5)
        ttk.Button(data_frame, text="Ejemplo de tarea_1", width=25, command=self.cargar_ejemplo_datos_Tarea1)\
            .pack(side='left', padx=5, pady=5)
        ttk.Button(data_frame, text="Ejemplo de tarea_2", width=25, command=self.cargar_ejemplo_datos_Tarea)\
            .pack(side='left', padx=5, pady=5)

        # --- Sección: Algoritmos disponibles ---
        algo_frame = ttk.LabelFrame(self.root, text="Algoritmos", padding=10)
        algo_frame.pack(padx=20, pady=10, fill='x')
        ttk.Button(algo_frame,
                   text="Enumeración exhaustiva",
                   width=25,
                   command=self.pedir_politicas)\
            .pack(side='top', fill='x', pady=3)
        ttk.Button(algo_frame,
                   text="Mejoramiento de políticas",
                   width=25,
                   command=self.metodo_mejoramiento_politicas)\
            .pack(side='top', fill='x', pady=3)
        ttk.Button(algo_frame,
                   text="Programación Lineal (PPL)",
                   width=25,
                   command=self.resolver_ppl)\
            .pack(side='top', fill='x', pady=3)
        ttk.Button(algo_frame,
                   text="Mejoramiento de políticas con descuento",
                   width=25,
                   command=self.metodo_mejoramiento_con_descuentos)\
            .pack(side='top', fill='x', pady=3)  
            
        ttk.Button(algo_frame,

                   text="Método de Aproximaciones Sucesivas",
                   width=25,
                   command=self.metodo_aproximaciones_sucesivas)\
            .pack(side='top', fill='x', pady=3)
        
        # --- Botón de salir destacado ---
        exit_btn = ttk.Button(self.root, text="Salir", width=30, command=self.root.quit)
        exit_btn.pack(pady=20)

        # Actualiza barra de estado
        self.status_var.set("Vista de inicio cargada")



    def abrir_lectura_datos(self):
        # Borrar la pantalla actual
        for widget in self.root.winfo_children():
            widget.destroy()

        # 2) header
        header = ttk.Frame(self.root, padding=10)
        header.pack(fill='x')
        ttk.Label(header, text="Ingreso de datos", style='Header.TLabel').pack()

        # 3) cuadro de inputs
        input_frame = ttk.LabelFrame(self.root, text="Parámetros de lectura", padding=10)
        input_frame.pack(padx=20, pady=10, fill='x')
        ttk.Label(input_frame, text="Número de estados:").grid(row=0, column=0, sticky='w')
        self.entry_estados = ttk.Entry(input_frame)
        self.entry_estados.grid(row=0, column=1, sticky='ew', pady=5)
        ttk.Label(input_frame, text="Número de decisiones:").grid(row=1, column=0, sticky='w')
        self.entry_decisiones = ttk.Entry(input_frame)
        self.entry_decisiones.grid(row=1, column=1, sticky='ew', pady=5)
        input_frame.columnconfigure(1, weight=1)

        
        
        # botones centrados
        btn_frame = ttk.Frame(self.root, padding=50)
        btn_frame.pack(fill='x')
        inner = ttk.Frame(btn_frame)
        inner.pack()

        ttk.Button(
            inner,
            text="Continuar",
            style='Azul.TButton',
            command= self.iniciar_llenado
        ).pack(side='left', padx=10)
        ttk.Button(
            inner,
            text="Volver al menú",
            style='Azul.TButton',
            command=self.inicio
        ).pack(side='left', padx=10)

        # 5) actualiza estado
        self.status_var.set("Ingrese estados y decisiones")
    

    def iniciar_llenado(self):
        
        # Validamos las entradas
        try:
            self.n_estados = int(self.entry_estados.get()) #Se llama al dato que guarda el numero de estados que se guardo en self.entry_estados
            self.n_decisiones = int(self.entry_decisiones.get())
            if self.n_estados <= 0 or self.n_decisiones <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores enteros positivos.")
            return

        # Inicializamos la matriz tridimensional Pij[k][i][j]
        self.Pij = [[[0.0 for _ in range(self.n_estados)] for _ in range(self.n_estados)] for _ in range(self.n_decisiones)]
        
        #EJEMPLO: self.Pij = [
                                #[ [0.0, 0.0], [0.0, 0.0] ],  # Pij para decisión 0
                                #[ [0.0, 0.0], [0.0, 0.0] ],  # Pij para decisión 1
                                #[ [0.0, 0.0], [0.0, 0.0] ]   # Pij para decisión 2
                            #]
                            
                            
        # Inicializamos la matriz de costos Cik[k][i]
        self.Cik = [[0.0 for _ in range(self.n_estados)] for _ in range(self.n_decisiones)]

        self.k_actual = 0  # Empezamos por la decisión 0
        self.llenar_decision(self.k_actual)



    def llenar_decision(self, k):
        # Limpiamos la pantalla
        for widget in self.root.winfo_children():
            widget.destroy()

        # Etiqueta con número de decisión (estilo)
        tk.Label(
            self.root,
            text=f"Decisión {k + 1} de {self.n_decisiones}, matriz Pij:",
            font=("Arial", 30, "bold")
            ,bg= '#DCDAD6'
        ).pack(pady=30)

        self.entry_pij = []  # Lista de listas de Entry para probabilidades
        self.entry_cik = []  # Lista de Entry para costos

        frame = tk.Frame(self.root,bg= '#DCDAD6')
        frame.pack(padx=20, pady=10)

        # Encabezado: columnas con estados destino (estilo)
        tk.Label(
            frame,
            text="Estado Inicial \\ Destino",
            font=("Helvetica", 12, "bold"),
            bg= '#DCDAD6'
        ).grid(row=0, column=0, padx=5, pady=5)

        for j in range(self.n_estados):
            tk.Label(
                frame,
                text=f"{j}",
                font=("Helvetica", 12),
                bg= '#DCDAD6'
            ).grid(row=0, column=j + 1, padx=15, pady=5)

        tk.Label(
            frame,
            text="Costo",
            font=("Helvetica", 12, "bold"),
            bg= '#DCDAD6'
        ).grid(row=0, column=self.n_estados + 3, padx=5, pady=5)

        # Sección para ingresar Pij y Cik
        for i in range(self.n_estados):
            fila = []
            fila_fisica = i + 1

            tk.Label(
                frame,
                text=f"{i}",
                font=("Helvetica", 12),
                bg= '#DCDAD6'
            ).grid(row=fila_fisica, column=0, padx=5, pady=5)

            for j in range(self.n_estados):
                e = tk.Entry(
                    frame,
                    width=5,
                    bd=2,
                    relief="ridge",
                    justify="center"
                )
                e.grid(row=fila_fisica, column=j + 1, padx=2, pady=2)
                fila.append(e)
            self.entry_pij.append(fila)

            tk.Label(
                frame,
                text=f"C_{i}{k + 1}",
                font=("Helvetica", 12),
                bg= '#DCDAD6'
            ).grid(row=fila_fisica, column=self.n_estados + 2, padx=5, pady=5)

            e_costo = tk.Entry(
                frame,
                width=6,
                bd=2,
                relief="ridge",
                justify="center"
            )
            e_costo.grid(row=fila_fisica, column=self.n_estados + 3, padx=2, pady=2)
            self.entry_cik.append(e_costo)
        
        # botones centrados
        btn_frame = ttk.Frame(self.root, padding=50)
        btn_frame.pack(fill='x')
        inner = ttk.Frame(btn_frame)
        inner.pack()

        ttk.Button(
            inner,
            text="Corregir datos",
            style='Azul.TButton',
            command= self.guardar_decision
        ).pack(side='left', padx=10)
        ttk.Button(
            inner,
            text="Volver al menú",
            style='Azul.TButton',
            command=self.inicio
        ).pack(side='left', padx=10)


    def guardar_decision(self):
        # Guardamos lo ingresado para esta decisión
        for i in range(self.n_estados):
            vector = []
            suma = 0.0
            for j in range(self.n_estados):
                try:
                    val = float(self.entry_pij[i][j].get())#Obtención del valor pij de una fila
                    if val < 0 or val > 1:
                        raise ValueError
                    vector.append(val)
                    suma += val
                except ValueError:
                    messagebox.showerror("Error", f"Probabilidad inválida en estado {i}, destino {j}")
                    return

            if not all(v == 0 for v in vector) and round(suma, 6) != 1.0:
                tk.messagebox.showerror("Error", f"La suma de probabilidades de estado {i} no es 1")
                return

            self.Pij[self.k_actual][i] = vector

            try:
                costo = float(self.entry_cik[i].get())
                self.Cik[self.k_actual][i] = costo
            except ValueError:
                messagebox.showerror("Error", f"Costo inválido en estado {i}")
                return

        self.k_actual += 1
        if self.k_actual < self.n_decisiones:
            self.llenar_decision(self.k_actual)
        else:
            messagebox.showinfo("Éxito", "¡Todos los datos fueron ingresados correctamente!")
            print("\nMatriz tridimensional Pij (decisión x estado x estado):")
            for k in range(self.n_decisiones):
                print(f"Decisión {k}:")
                for fila in self.Pij[k]:
                    print(fila)

            print("\nMatriz de costos Cik (decisión x estado):")
            for k in range(self.n_decisiones):
                print(f"Decisión {k}: {self.Cik[k]}")

            self.inicio()
            
    def pedir_politicas(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Número de políticas a ingresar:").pack(pady=10)
        self.entry_num_pols = tk.Entry(self.root)
        self.entry_num_pols.pack(pady=5)

        btn_siguiente = tk.Button(self.root, text="Continuar", command=self.ingresar_politicas)
        btn_siguiente.pack(pady=10)
        
        # Botón para volver al inicio
        btn_volver = tk.Button(self.root, text="Volver al menú", command=self.inicio)
        btn_volver.pack()
        
    def ingresar_politicas(self):
        try:
            self.num_politicas = int(self.entry_num_pols.get())
            if self.num_politicas <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número entero positivo.")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        self.politicas_entries = []  # Será una lista de listas (matriz) de Entry

        tk.Label(self.root, text="Escribe cada política ").pack(pady=30)

        frame = tk.Frame(self.root)
        frame.pack()
    
        for i in range(self.num_politicas):
            fila = []  # Lista para la política i
            tk.Label(frame, text=f"Política #{i+1}:").grid(row=i, column=0, padx=5, pady=5)
            for j in range(self.n_estados):
                entry = tk.Entry(frame, width=5)
                entry.grid(row=i, column=j + 1, padx=2, pady=2)
                fila.append(entry)
            self.politicas_entries.append(fila)
            
        # Botón para Calcular política óptima
        btn_calcular = tk.Button(self.root, text="Calcular política óptima", command=self.evaluar_politicas_usuario)
        btn_calcular.pack(pady=10)
        
        
        
        # Botón para volver al inicio
        btn_volver = tk.Button(self.root, text="Volver al menú", command=self.inicio)
        btn_volver.pack()

    
    def cargar_ejemplo_datos(self):
        self.n_estados = 4
        self.n_decisiones = 3

        self.Pij = [
            [  # Decisión 1
                [0.0, 0.875, 0.0625, 0.0625],  # Estado 0
                [0.0, 0.75, 0.125, 0.125],     # Estado 1
                [0.0, 0.0, 0.5, 0.5],          # Estado 2
                [0.0, 0.0, 0.0, 0.0]           # Estado 3 (inviable)
            ],
            [  # Decisión 2
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0]
            ],
            [  # Decisión 3
                [0, 0, 0, 0],
                [1, 0, 0, 0],
                [1, 0, 0, 0],
                [1, 0, 0, 0]
            ]
        ]

        self.Cik = [
            [0, 1000, 3000, 0],    
            [0, 0, 4000, 0],
            [0, 6000, 6000, 6000]
        ]
        messagebox.showinfo("Datos cargados", "Se cargaron los datos de ejemplo correctamente.\nPuedes ejecutar los algoritmos.")
    

    def cargar_ejemplo_datos_Tarea1(self):
        self.n_estados = 2
        self.n_decisiones = 2

        self.Pij = [
            [  # Decisión 1
                [0.875, 0.125],  # Estado 0
                [0.875, 0.125]     # Estado 1
            ],
            [  # Decisión 2
                [0.125, 0.875],
                [0.125, 0.875]
            ]
        ]

        self.Cik = [
            [75, 0],    # Decisión 1
            [14, 14],    # Decisión 2
        ]
        messagebox.showinfo("Datos cargados del ejemplo_Tarea", "Se cargaron los datos de ejemplo correctamente.\nPuedes ejecutar los algoritmos.")

    def cargar_ejemplo_datos_Tarea(self):
        # 1) Número de estados y decisiones
        self.n_estados = 3
        self.n_decisiones = 3

        # 2) Probabilidades de transición Pij[decisión][estado][estado_siguiente]
        self.Pij = [
            [  # Decisión 0: Radio
                [0.4, 0.5, 0.1],   # Estado 0 (Regular)
                [0.1, 0.7, 0.2],   # Estado 1 (Bueno)
                [0.1, 0.2, 0.7]    # Estado 2 (Excelente)
            ],
            [  # Decisión 1: TV
                [0.7, 0.2, 0.1],
                [0.3, 0.6, 0.1],
                [0.1, 0.7, 0.2]
            ],
            [  # Decisión 2: Periódico
                [0.2, 0.5, 0.3],
                [0.0, 0.7, 0.3],
                [0.0, 0.2, 0.8]
            ]
        ]

        # 3) Ingresos inmediatos Cik[decisión][estado] (en miles de dólares)
        self.Cik = [
            [280, 250, 220],    # Radio: ingresos en estados 0,1,2
            [220, 110, -130],   # TV
            [258, 255, 300]     # Periódico
        ]

        # 4) Confirmación al usuario
        messagebox.showinfo(
            "Datos cargados de la práctica",
            "Se cargaron los datos de la práctica correctamente.\nAhora puedes ejecutar los algoritmos."
        )


    def mostrar_datos_ingresados(self):
        # limpiar pantalla
        self.root.configure(bg="#DCDAD6")
        for widget in self.root.winfo_children():
            widget.destroy()

        # encabezado
        tk.Label(
            self.root,
            text="Datos ingresados",
            font=("Arial", 16),
            fg="black",
            bg="#DCDAD6"
        ).pack(pady=10)

        # resumen parámetros
        tk.Label(
            self.root,
            text=f"Número de estados: {self.n_estados}",
            font=("Arial", 16),
            fg="black",
            bg="#DCDAD6"
        ).pack()
        tk.Label(
            self.root,
            text=f"Número de decisiones: {self.n_decisiones}",
            font=("Arial", 16),
            fg="black",
            bg="#DCDAD6"
        ).pack(pady=5)

        # contenedor scrollable
        container = tk.Frame(self.root, bg="#DCDAD6")
        container.pack(fill='both', expand=True, padx=20, pady=10)
        canvas = tk.Canvas(container, bg="#DCDAD6", highlightthickness=0)
        vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scrollable = tk.Frame(canvas, bg="#DCDAD6")
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable, anchor="nw")

        # mostrar matriz Pij
        for k in range(self.n_decisiones):
            tk.Label(
                scrollable,
                text=f"Matriz de transición Pij para decisión {k+1}:",
                font=("Arial", 16),
                fg="black",
                bg="#DCDAD6"
            ).pack(anchor='w', pady=(10, 2))
            for i in range(self.n_estados):
                fila = f"Estado {i} → {self.Pij[k][i]}"
                tk.Label(
                    scrollable,
                    text=fila,
                    font=("Arial", 16),
                    fg="black",
                    bg="#DCDAD6"
                ).pack(anchor='w')

        # mostrar matriz de costos
        tk.Label(
            scrollable,
            text="Matriz de costos Cik:",
            font=("Arial", 16),
            fg="black",
            bg="#DCDAD6"
        ).pack(anchor='w', pady=(10, 2))
        for k in range(self.n_decisiones):
            fila = f"Decisión {k+1} → {self.Cik[k]}"
            tk.Label(
                scrollable,
                text=fila,
                font=("Arial", 16),
                fg="black",
                bg="#DCDAD6"
            ).pack(anchor='w')

        # botones centrados
        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(fill='x')
        inner = ttk.Frame(btn_frame)
        inner.pack()

        ttk.Button(
            inner,
            text="Corregir datos",
            style='Azul.TButton',
            command=lambda: self.llenar_decision(0)
        ).pack(side='left', padx=5)
        
        ttk.Button(
            inner,
            text="Volver al menú",
            style='Azul.TButton',
            command=self.inicio
        ).pack(side='left', padx=5)

    def evaluar_politicas_usuario(self):
        # Validación de políticas (sin cambios)
        self.politicas_usuario = []
        for i, fila in enumerate(self.politicas_entries):
            try:
                valores = [int(entry.get()) for entry in fila]
                if len(valores) != self.n_estados:
                    raise ValueError
                if any(d < 1 or d > self.n_decisiones for d in valores):
                    raise ValueError
                self.politicas_usuario.append(valores)
            except ValueError:
                messagebox.showerror("Error", f"Política #{i+1} inválida.")
                return

        # --- Cálculo de mínimo y máximo ---
        mejor_politica_min = None
        mejor_politica_max = None
        mejor_valor_min = float("inf")
        mejor_valor_max = float("-inf")

        for politica in self.politicas_usuario:
            P = np.array([self.Pij[politica[i]-1][i] for i in range(self.n_estados)])
            C = np.array([self.Cik[politica[i]-1][i] for i in range(self.n_estados)])
            A = P.T.copy()
            for j in range(self.n_estados):
                A[j][j] -= 1
            A[-1] = np.ones(self.n_estados)
            b = np.zeros(self.n_estados); b[-1] = 1
            try:
                pi = np.linalg.solve(A, b)
                costo_esp = float(np.dot(pi, C))
                # Minimizar
                if costo_esp < mejor_valor_min:
                    mejor_valor_min = costo_esp
                    mejor_politica_min = politica.copy()
                # Maximizar
                if costo_esp > mejor_valor_max:
                    mejor_valor_max = costo_esp
                    mejor_politica_max = politica.copy()
            except np.linalg.LinAlgError:
                pass

        # --- INTERFAZ CON ESTILO Y SCROLLABLE ---
        self.root.configure(bg="#DCDAD6")
        for widget in self.root.winfo_children():
            widget.destroy()

        # Encabezado
        tk.Label(
            self.root,
            text="Resultados por política",
            font=('Arial', 22, 'bold'),
            fg="black",
            bg="#DCDAD6"
        ).pack(pady=10)

        # Contenedor scrollable
        container = tk.Frame(self.root, bg="#DCDAD6")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        canvas = tk.Canvas(container, bg="#DCDAD6", highlightthickness=0)
        vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scrollable = tk.Frame(canvas, bg="#DCDAD6")
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable, anchor="nw")

        # Mostrar cada política y sus resultados
        for idx, politica in enumerate(self.politicas_usuario):
            tk.Label(
                scrollable,
                text=f"Política #{idx+1}: {politica}",
                font=("Arial", 18, 'bold'),
                fg="#2a9d8f",
                bg="#DCDAD6"
            ).pack(anchor="w", pady=(10, 2))

            # Vector π
            P = np.array([self.Pij[politica[i]-1][i] for i in range(self.n_estados)])
            C = np.array([self.Cik[politica[i]-1][i] for i in range(self.n_estados)])
            A = P.T.copy()
            for j in range(self.n_estados):
                A[j][j] -= 1
            A[-1] = np.ones(self.n_estados)
            b = np.zeros(self.n_estados); b[-1] = 1

            try:
                pi = np.linalg.solve(A, b)
                pi_texto = "[" + ", ".join(f"{x:.4f}" for x in pi) + "]"
                tk.Label(
                    scrollable,
                    text=f"π = {pi_texto}",
                    font=("Arial", 16),
                    fg="black",
                    bg="#DCDAD6"
                ).pack(anchor="w", pady=2)
                costo_esp = float(np.dot(pi, C))
                tk.Label(
                    scrollable,
                    text=f"Costo esperado: {costo_esp:.4f}",
                    font=("Arial", 14, "italic"),
                    fg="#588157",
                    bg="#DCDAD6"
                ).pack(anchor="w", pady=2)
            except np.linalg.LinAlgError:
                tk.Label(
                    scrollable,
                    text="Sistema sin solución",
                    font=("Arial", 16),
                    fg="black",
                    bg="#DCDAD6"
                ).pack(anchor="w", pady=2)

        # --- Funciones internas para mostrar diálogo óptimo ---
        def mostrar_optimo_min():
            if mejor_politica_min is None:
                messagebox.showwarning("Atención", "No se encontró política óptima para minimizar.")
            else:
                messagebox.showinfo(
                    "Óptimo (Minimizar)",
                    f"Política: {mejor_politica_min}\nCosto: {mejor_valor_min:.4f}"
                )

        def mostrar_optimo_max():
            if mejor_politica_max is None:
                messagebox.showwarning("Atención", "No se encontró política óptima para maximizar.")
            else:
                messagebox.showinfo(
                    "Óptimo (Maximizar)",
                    f"Política: {mejor_politica_max}\nCosto: {mejor_valor_max:.4f}"
                )

        # Botones centrales con padding y centrados
        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(fill="x")
        inner = ttk.Frame(btn_frame)
        inner.pack()

        ttk.Button(
            inner,
            text="Óptimo Min",
            style='Azul.TButton',
            command=mostrar_optimo_min
        ).pack(side="left", padx=5)
        ttk.Button(
            inner,
            text="Óptimo Max",
            style='Azul.TButton',
            command=mostrar_optimo_max
        ).pack(side="left", padx=5)
        ttk.Button(
            inner,
            text="Volver al menú",
            style='Azul.TButton',
            command=self.inicio
        ).pack(side='left', padx=5)

##############################################################################################################################################
    def metodo_mejoramiento_politicas(self):
        # Paso 0: política inicial
        entrada = simpledialog.askstring(
            "Política inicial",
            f"Escribe la política inicial R de {self.n_estados} valores (1 a {self.n_decisiones}, separados por espacio):"
        )
        if not entrada:
            return
        try:
            politica = list(map(int, entrada.strip().split()))
            if len(politica) != self.n_estados or any(d < 1 or d > self.n_decisiones for d in politica):
                raise ValueError
        except ValueError:
            # mostrar error en pantalla
            self.root.configure(bg="#DCDAD6")
            for w in self.root.winfo_children(): w.destroy()
            tk.Label(self.root,
                    text="Política inicial inválida.",
                    font=("Arial", 16, "bold"),
                    fg="red",
                    bg="#DCDAD6").pack(pady=20)
            ttk.Button(self.root,
                    text="Volver al menú",
                    style='Azul.TButton',
                    command=self.inicio).pack(pady=10)
            return

        # preparar interfaz scrollable
        self.root.configure(bg="#DCDAD6")
        for w in self.root.winfo_children(): w.destroy()
        ttk.Label(self.root,
                text="Mejoramiento de políticas",
                font=("Arial", 16, "bold"),
                foreground="black",
                background="#DCDAD6").pack(pady=10)

        container = tk.Frame(self.root, bg="#DCDAD6")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        canvas = tk.Canvas(container, bg="#DCDAD6", highlightthickness=0)
        vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        scrollable = tk.Frame(canvas, bg="#DCDAD6")
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable, anchor="nw")

        # variables para el bucle
        n = self.n_estados
        m = n - 1
        decisiones = self.n_decisiones
        iteracion = 0

        while True:
            iteracion += 1

            # construir P, C, A, b
            P = np.array([self.Pij[pol - 1][i] for i, pol in enumerate(politica)])
            C = np.array([self.Cik[pol - 1][i] for i, pol in enumerate(politica)])
            A = np.zeros((n+1, n+1))
            b = np.zeros(n+1)
            for i in range(n):
                if i < m:
                    A[i,i] = 1 - P[i,i]
                for j in range(m):
                    if j != i and P[i,j] != 0:
                        A[i,j] = -P[i,j]
                A[i,-1] = 1
                b[i] = C[i]
            A[n,m] = 1
            b[n] = 0

            # mostrar sistema
            sys_text = f"Iteración {iteracion} – Sistema:\n"
            for i in range(n):
                terms = []
                if i < m and 1-P[i,i] != 0:
                    terms.append(f"{round(1-P[i,i],3)}·V{i}")
                for j in range(m):
                    if j!=i and P[i,j]!=0:
                        terms.append(f"-{round(P[i,j],3)}·V{j}")
                terms.append("+ g")
                rhs = round(C[i],3)
                sys_text += " + ".join(terms) + f" = {rhs}\n"
            sys_text += f"V{m} = 0"
            tk.Label(scrollable,
                    text=sys_text,
                    font=("Arial", 16),
                    fg="black",
                    bg="#DCDAD6",
                    justify="left").pack(anchor="w", pady=5)

            # resolver
            try:
                x = np.linalg.solve(A, b)
            except np.linalg.LinAlgError:
                tk.Label(scrollable,
                        text=f"Sistema sin solución en iteración {iteracion}.",
                        font=("Arial", 16),
                        fg="red",
                        bg="#DCDAD6").pack(anchor="w", pady=5)
                break

            # mostrar solución
            sol_text = f"Solución (Iter {iteracion}):\n"
            for idx in range(n):
                sol_text += f"V{idx} = {round(x[idx],6)}\n"
            sol_text += f"g = {round(x[-1],6)}"
            tk.Label(scrollable,
                    text=sol_text,
                    font=("Arial", 16),
                    fg="black",
                    bg="#DCDAD6",
                    justify="left").pack(anchor="w", pady=5)

            V = x[:n]; g = x[-1]

            # dentro de metodo_mejoramiento_politicas, reemplaza la parte de “mejora de política” por esto:

            # mejora de política
            detalle = f"Detalle mejora (Iter {iteracion}):\n"
            nueva = []
            for i in range(n):
                # obtenemos las acciones posibles en el estado i
                acciones = [
                    k for k in range(decisiones)
                    if any(abs(self.Pij[k][i][j]) > 1e-6 for j in range(n))
                    or abs(self.Cik[k][i]) > 1e-6
                ]
                mejor_val = None
                mejor_k = None
                for k in acciones:
                    ci = round(self.Cik[k][i], 2)
                    vi = round(V[i], 2)  # done: redondear V[i] para claridad
                    # done: construir términos de la suma P_ij * V_j
                    terms = " + ".join(
                        f"{round(self.Pij[k][i][j], 2)}·V{j}"
                        for j in range(n)
                        if abs(self.Pij[k][i][j]) > 1e-6
                    )
                    # done: formar la ecuación como cadena
                    equation = f"{ci} + ({terms}) - {vi}"
                    # calculamos el valor numérico
                    valor = ci + sum(self.Pij[k][i][j] * V[j] for j in range(n)) - V[i]
                    # done: añadir al texto tanto la ecuación como el resultado
                    detalle += f"Estado {i}, k={k+1}: {equation} = {round(valor, 2)}\n"
                    # buscamos la mejor acción
                    if mejor_val is None or valor < mejor_val:
                        mejor_val, mejor_k = valor, k+1
                nueva.append(mejor_k)
                detalle += f"→ Mejor decisión: k={mejor_k}\n"
            # mostramos todo el detalle en pantalla
            tk.Label(
                scrollable,
                text=detalle,
                font=("Arial", 16),
                fg="black",
                bg="#DCDAD6",
                justify="left"
            ).pack(anchor="w", pady=5)


            # política mejorada
            pol_text = f"Política nueva (Iter {iteracion}): {nueva}"
            tk.Label(scrollable,
                    text=pol_text,
                    font=("Arial", 16, "bold"),
                    fg="#2a9d8f",
                    bg="#DCDAD6").pack(anchor="w", pady=5)

            # convergencia
            if nueva == politica:
                conv = f"No cambió en iteración {iteracion}. Termina."
                tk.Label(scrollable,
                        text=conv,
                        font=("Arial", 16, "italic"),
                        fg="#e76f51",
                        bg="#DCDAD6").pack(anchor="w", pady=10)
                break
            politica = nueva

        # botón para regresar
        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame,
                text="Volver al menú",
                style='Azul.TButton',
                command=self.inicio).pack(pady=10)


################################################################################################################################################################################################

    def resolver_ppl(self):
        #Pregunta si minimizar o maximizar
        modo = simpledialog.askstring("Modo de optimización", "¿Deseas minimizar o maximizar?\n(Escribe: min o max)")
        if not modo or modo.lower() not in ["min", "max"]:
            messagebox.showerror("Error", "Opción inválida. Debes escribir 'min' o 'max'.")
            return
#---------------
        for widget in self.root.winfo_children():
            widget.destroy()

        #Pregunta si minimizar o maximizar
        modo = simpledialog.askstring("Modo de optimización", "¿Deseas minimizar o maximizar?\n(Escribe: min o max)")
        if not modo or modo.lower() not in ["min", "max"]:
            messagebox.showerror("Error", "Opción inválida. Debes escribir 'min' o 'max'.")
            return
#---------------


        tk.Label(self.root, text="Resolviendo con Programación Lineal", font=("Arial", 16)).pack(pady=10)

        #Iniciaización de variables
        n = self.n_estados
        m = self.n_decisiones
        total_vars = n * m

        C = []      # Costos Cik
        A_eq = []   # Matriz de restricciones de igualdad
        b_eq = []   # Vector del lado derecho
        bounds = [(0, None)] * total_vars  # y_ik ≥ 0

        # Función objetivo C:según modo
        for i in range(n):
            for k in range(m):
                c = self.Cik[k][i]
                C.append(c if modo.lower() == "min" else -c)
#_________

        # Restricción 1: suma de todas las y_ik = 1
        A_eq.append([1.0] * total_vars)
        b_eq.append(1.0)

        # Demás restricciones -> para cada estado j
        for j in range(n):
            fila = [0.0] * total_vars
            for i in range(n):
                for k in range(m):
                    index = i * m + k
                    pij = self.Pij[k][i][j]
                    if i == j:
                        fila[index] += -1 + pij
                    else:
                        fila[index] += pij
            A_eq.append(fila)
            b_eq.append(0.0)
#-----------------
        # Mostrar modelo de programación lineal (PPL)
        tk.Label(self.root, text="Modelo de Programación Lineal", font=("Arial", 14, "bold")).pack(pady=5)
        frame_modelo = tk.Frame(self.root)
        frame_modelo.pack(pady=5)

        # Función objetivo
        z_texto = f"{'Max' if modo.lower() == 'max' else 'Min'} z = "
        for i in range(n):
            for k in range(m):
                coef = round(self.Cik[k][i], 2)
                z_texto += f"{coef}·y_{i}{k} + "
        z_texto = z_texto[:-3]
        tk.Label(frame_modelo, text=z_texto, font=("Courier", 10), anchor="w", justify="left").pack(anchor="w")

        # Restricción de suma total de probabilidades
        rest1 = "∑ y_ik = 1 → " + " + ".join([f"y_{i}{k}" for i in range(n) for k in range(m)])
        tk.Label(frame_modelo, text=rest1, font=("Courier", 10), anchor="w", justify="left").pack(anchor="w")

        # Restricciones de balance (omitiendo último estado)
        for j in range(n - 1):  # IMPORTANTE: solo hasta n-1
            lhs = ""
            for i in range(n):
                for k in range(m):
                    pij = self.Pij[k][i][j]
                    if pij != 0:
                        coef = round(pij, 3)
                        lhs += f"{coef}·y_{i}{k} + "
            lhs = lhs[:-3] if lhs else "0"
            ecuacion = f"Estado {j}: {lhs} = y_{j}*"
            tk.Label(frame_modelo, text=ecuacion, font=("Courier", 10), anchor="w", justify="left").pack(anchor="w")

<<<<<<< Updated upstream
        
=======
        # Si se desea maximizar, se multiplica por -1 para convertirlo en minimización
        if modo.lower() == "maximizar":
            C = [-c for c in C]
        #------
>>>>>>> Stashed changes
#---------------------
        # Resolver con scipy.optimize.linprog
        resultado = linprog(C, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')


        if resultado.success:
            y_vars = resultado.x
            costo_optimo = resultado.fun
            #Corrige el resultado para que no sea negativo si max
<<<<<<< Updated upstream
            if modo.lower() == "max":
=======
            if modo.lower() == "maximizar":
>>>>>>> Stashed changes
                costo_optimo *= -1
            #----
            # Mostrar el costo óptimo
            tk.Label(self.root, text=f"Costo óptimo total: {round(costo_optimo, 4)}", font=("Arial", 14)).pack(pady=10)

            # Mostrar valores de las variables básicas
            frame = tk.Frame(self.root)
            frame.pack()
            tk.Label(frame, text="Valor de las variables  (y_ik):", font=("Arial", 12, "bold")).pack()

            texto = ""
            politica_optima = []

            for i in range(n):
                mejor_k = -1
<<<<<<< Updated upstream
                mayor_yik = -1
=======
                valor = None
>>>>>>> Stashed changes
                fila = f"Estado {i}: "
                for k in range(m):
                    idx = i * m + k
                    y_val = round(y_vars[idx], 4)
                    fila += f" y_{i}{k}={y_val}   "
<<<<<<< Updated upstream
                    if y_val > mayor_yik:
                        mayor_yik = y_val
=======
                    if mejor_k == -1:
                        mejor_k = k
                        valor = y_val
                    elif (modo.lower() == "minimizar" and y_val > valor) or (modo.lower() == "maximizar" and y_val > valor):
                        valor = y_val
>>>>>>> Stashed changes
                        mejor_k = k
                politica_optima.append(mejor_k + 1)
                texto += fila + "\n"


            tk.Label(frame, text=texto, font=("Courier", 10), justify="left", anchor="w").pack()

            # Mostrar política óptima
            poli_txt = ", ".join([str(p) for p in politica_optima])
            tk.Label(self.root, text=f"Política óptima : [{poli_txt}]", font=("Arial", 14, "bold")).pack(pady=10)
        else:
            tk.Label(self.root, text="No se pudo encontrar una solución", fg="red", font=("Arial", 14)).pack()

        # Botón para volver
        tk.Button(self.root, text="Volver al menú", command=self.inicio).pack(pady=10)

        
############################################################################################################################################
    def metodo_mejoramiento_con_descuentos(self):
        # --- Paso 0: Política inicial ---
        entrada = simpledialog.askstring(
            "Política inicial",
            f"Escribe la política inicial R de {self.n_estados} valores (1 a {self.n_decisiones}, separados por espacio):"

        )
        if not entrada:
            return
        try:
            politica = list(map(int, entrada.strip().split()))
            if len(politica) != self.n_estados or any(d < 1 or d > self.n_decisiones for d in politica):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Política inicial inválida.")
            return

<<<<<<< Updated upstream
        # Preguntar si se desea minimizar o maximizar
        modo = simpledialog.askstring("Modo", "¿Deseas minimizar o maximizar?\n(Escribe: minimizar o maximizar)")
        if not modo or modo.lower() not in ["min", "max"]:
            messagebox.showerror("Error", "Modo inválido. Escribe 'min' o 'max'.")
            return

=======
>>>>>>> Stashed changes
        # --- Paso 1: Factor de descuento α ---
        alpha_str = simpledialog.askstring(
            "Factor de descuento",
            "Introduce el factor de descuento α (0 < α < 1):"
        )
        try:
            alpha = float(alpha_str)
            if not (0 < alpha < 1):
                raise ValueError
        except:
            messagebox.showerror("Error", "Factor de descuento inválido.")
            return

        # --- Preparo interfaz scrollable ---
        self.root.configure(bg="#DCDAD6")
        for w in self.root.winfo_children():
            w.destroy()
<<<<<<< Updated upstream
        ttk.Label(self.root, text=f"Mejoramiento con Descuento ({modo})", font=("Arial",16,"bold"), background="#DCDAD6").pack(pady=10)
=======
        ttk.Label(self.root, text="Mejoramiento con Descuento",
                font=("Arial",16,"bold"), background="#DCDAD6").pack(pady=10)
>>>>>>> Stashed changes

        container = tk.Frame(self.root, bg="#DCDAD6")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        canvas = tk.Canvas(container, bg="#DCDAD6", highlightthickness=0)
        vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y"); canvas.pack(side="left", fill="both", expand=True)
        scrollable = tk.Frame(canvas, bg="#DCDAD6")
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scrollable, anchor="nw")

        n = self.n_estados
        iteracion = 0

        while True:
            iteracion += 1

            # --- Paso 2: Resolver (I - α·P_π)·V = C_π ---
            Ppi = np.array([self.Pij[pol-1][i] for i, pol in enumerate(politica)])
            Cpi = np.array([self.Cik[pol-1][i] for i, pol in enumerate(politica)])
            A = np.eye(n) - alpha * Ppi
            b = Cpi

            # Mostrar sistema
            sys_text = f"Iter {iteracion} – Sistema con α={alpha}:\n"
            for i in range(n):
                terms = [f"{round(A[i,j],3)}·V{j}" for j in range(n) if abs(A[i,j])>1e-6]
                sys_text += " + ".join(terms) + f" = {round(b[i],3)}\n"
            tk.Label(scrollable, text=sys_text, font=("Arial",16), fg="black", bg="#DCDAD6", justify="left")\
                .pack(anchor="w", pady=5)

            try:
                V = np.linalg.solve(A, b)
            except np.linalg.LinAlgError:
                tk.Label(scrollable, text="Sistema singular. Termina.",
                        font=("Arial",16), fg="red", bg="#DCDAD6")\
                    .pack(anchor="w", pady=5)
                break

            # Mostrar V
            sol_text = f"Valores V (Iter {iteracion}):\n"
            for i, vi in enumerate(V):
                sol_text += f"V{i} = {round(vi,6)}\n"
            tk.Label(scrollable, text=sol_text, font=("Arial",16), fg="black", bg="#DCDAD6", justify="left")\
                .pack(anchor="w", pady=5)

            # --- Paso 3: Mejora de política ignorando decisiones con Pij[k][i] toda ceros ---
            detalle = f"Detalle mejora con α (Iter {iteracion}):\n"
            nueva = []
            for i in range(n):
                # Encuentro qué decisiones k tienen Pij[k][i] no todas ceros o un costo distinto de 0
                acciones = [
                    k for k in range(self.n_decisiones)
                    if any(abs(self.Pij[k][i][j])>1e-6 for j in range(n))
                    or abs(self.Cik[k][i])>1e-6
                ]
                if not acciones:
                    # Si ninguna decisión aplica (fila cero en todas), conservo la actual
                    detalle += f"Estado {i}: sin transiciones válidas → conservo k={politica[i]}\n"
                    nueva.append(politica[i])
                    continue

                mejor_val, mejor_k = None, None
                for k in acciones:
                    ci = round(self.Cik[k][i],2)
                    suma_pv = sum(self.Pij[k][i][j] * V[j] for j in range(n))
                    Q = ci + alpha * suma_pv
                    detalle += (f"Estado {i}, k={k+1}: "
                                f"{ci} + {alpha}*({round(suma_pv,3)}) = {round(Q,2)}\n")
<<<<<<< Updated upstream
                    if mejor_val is None or (modo.lower() == "min" and Q < mejor_val) or (modo.lower() == "max" and Q > mejor_val):
                        mejor_val, mejor_k = Q, k+1
                    
=======
                    if mejor_val is None or Q < mejor_val:
                        mejor_val, mejor_k = Q, k+1
>>>>>>> Stashed changes
                nueva.append(mejor_k)
                detalle += f"→ Mejor decisión: k={mejor_k}\n"

            tk.Label(scrollable, text=detalle, font=("Arial",16), fg="black", bg="#DCDAD6", justify="left")\
                .pack(anchor="w", pady=5)

            # Mostrar política nueva
            tk.Label(scrollable,
                    text=f"Política nueva (Iter {iteracion}): {nueva}",
                    font=("Arial",16,"bold"), fg="#2a9d8f", bg="#DCDAD6")\
                .pack(anchor="w", pady=5)

            # --- Paso 4: Convergencia ---
            if nueva == politica:
                tk.Label(scrollable,
                        text=f"Convergió en iteración {iteracion}.",
                        font=("Arial",16,"italic"), fg="#e76f51", bg="#DCDAD6")\
                    .pack(anchor="w", pady=10)
                break
            politica = nueva

        # Botón para regresar al menú
        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Volver al menú", style='Azul.TButton',
                command=self.inicio).pack(pady=10)

           
################################################################################################################################################################################################
    def metodo_aproximaciones_sucesivas(self):
        # --- Paso 0: Leer α, N y ε ---
        entrada = simpledialog.askstring(
            "Aproximaciones Sucesivas",
            "Introduce α, #iteraciones N y tolerancia ε (separados por espacio):"
        )
        if not entrada:
            return
        try:
            alpha_str, N_str, eps_str = entrada.strip().split()
            alpha = float(alpha_str)
            N = int(N_str)
            epsilon = float(eps_str)
            if not (0 < alpha <= 1 and N > 0 and epsilon >= 0):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Parámetros inválidos.")
            return

        # --- Preparo interfaz scrollable ---
        self.root.configure(bg="#DCDAD6")
        for w in self.root.winfo_children(): w.destroy()
        ttk.Label(
            self.root,
            text="Aproximaciones Sucesivas",
            font=("Arial",16,"bold"),
            background="#DCDAD6"
        ).pack(pady=10)

        container = tk.Frame(self.root, bg="#DCDAD6")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        canvas = tk.Canvas(container, bg="#DCDAD6", highlightthickness=0)
        vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y"); canvas.pack(side="left", fill="both", expand=True)
        scrollable = tk.Frame(canvas, bg="#DCDAD6")
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scrollable, anchor="nw")
        
        

        n = self.n_estados
        V = np.zeros(n)

        # --- Paso 1: n = 1, V¹ᵢ = min_k Cᵢₖ ---
        tk.Label(
            scrollable,
            text="                      Iteración 1",
            font=("Arial",20,"bold"),
            fg="#2a9d8f",
            bg="#DCDAD6"
        ).pack(anchor="w", pady=(10,2))
        decisiones = []
        for i in range(n):
            # filtramos solo las decisiones que realmente existen
            acciones = [
                k for k in range(self.n_decisiones)
                if any(abs(self.Pij[k][i][j])>1e-6 for j in range(n))
                or abs(self.Cik[k][i])>1e-6
            ]
            # si no hay ninguna, dejamos V[i] = 0 y decisión = 1
            if not acciones:
                tk.Label(
                    scrollable,
                    text=f"Estado {i}: sin acciones → V¹[{i}] = 0.0000",
                    font=("Arial",16),
                    fg="black",
                    bg="#DCDAD6"
                ).pack(anchor="w")
                
                V[i] = 0.0
                decisiones.append(1)
                continue

            # buscamos min Cik
            costos = [(self.Cik[k][i], k+1) for k in acciones]
            c_min, k_min = min(costos, key=lambda x: x[0])
            V[i] = c_min
            decisiones.append(k_min)
            for c,kp in costos:
                # crea un Frame para la línea completa
                line_frame = tk.Frame(scrollable, bg="#DCDAD6")
                line_frame.pack(anchor="w", pady=(0,5))
                tk.Label(
                    line_frame,
                    text=f"Estado {i}   ",
                    font=("Arial",17, "bold"),
                    fg="black",
                    bg="#DCDAD6"
                ).pack(side="left")
                tk.Label(
                    line_frame,
                    text=f"k= {kp}:   ",
                    font=("Arial",17, "italic"),
                    fg="black",
                    bg="#DCDAD6"
                ).pack(side="left")
                tk.Label(
                    line_frame,
                    text=f" C={c:.2f}",
                    font=("Arial",16, "italic", "bold"),
                    fg="#074A37",
                    bg="#DCDAD6"
                ).pack(side="left")
                
            tk.Label(
                scrollable,
                text=f"→ V¹[{i}] = {c_min:.4f}   d¹[{i}] = {k_min}",
                font=("Arial",16,"italic"),
                fg="#168aad",
                bg="#DCDAD6"
            ).pack(anchor="w", pady=(1))

        tk.Label(
            scrollable,
            text="V = [" + ", ".join(f"{v:.4f}" for v in V) + "]",
            font=("Arial",18, "bold"),
            fg="#25a244",
            bg="#DCDAD6"
        ).pack(anchor="w")

        # --- Paso 2: iteraciones 2..N ---
        for t in range(2, N+1):
            Vprev = V.copy()
            Vnew = np.zeros(n)

            tk.Label(
                scrollable,
                text=f"\n                    Iteración {t}",
                font=("Arial",20,"bold"),
                fg="#2a9d8f",
                bg="#DCDAD6"
            ).pack(anchor="w", pady=(10,2))

            nuevas_dec = []
            for i in range(n):
                acciones = [
                    k for k in range(self.n_decisiones)
                    if any(abs(self.Pij[k][i][j])>1e-6 for j in range(n))
                    or abs(self.Cik[k][i])>1e-6
                ]
                if not acciones:
                    tk.Label(
                        scrollable,
                        text=f"Estado {i}: sin acciones → Vᵗ[{i}] = {Vprev[i]:.4f}",
                        font=("Arial",16),
                        fg="black",
                        bg="#DCDAD6"
                    ).pack(anchor="w")
                    Vnew[i] = Vprev[i]
                    nuevas_dec.append(decisiones[i])
                    continue

                mejor_Q, mejor_k = None, None
                for k in acciones:
                    ci = self.Cik[k][i]
                    suma_pv = sum(self.Pij[k][i][j] * Vprev[j] for j in range(n))
                    Q = ci + alpha * suma_pv
                    # crea un Frame para la línea completa
                    line_frame = tk.Frame(scrollable, bg="#DCDAD6")
                    line_frame.pack(anchor="w", pady=(0,5))
                    
                    # fragmento 1: "Estado i, k=..."
                    tk.Label(
                        line_frame,
                        text=f"Estado {i}   ",
                        font=("Arial",17, "bold"),
                        fg="black",
                        bg="#DCDAD6"
                    ).pack(side="left")
                    tk.Label(
                        line_frame,
                        text=f" k={k+1}:    ",
                        font=("Arial",17, "italic"),
                        fg="black",
                        bg="#DCDAD6"
                    ).pack(side="left")
                    

                    # fragmento 2: "ci + "
                    tk.Label(
                        line_frame,
                        text=f"{ci:.2f} + {alpha}*({suma_pv:.4f}",
                        font=("Arial",16),
                        fg="#889696",
                        bg="#DCDAD6"
                    ).pack(side="left")

                    # fragmento 4: " = Q"
                    tk.Label(
                        line_frame,
                        text=f" = {Q:.4f}",
                        font=("Arial",16, "italic", "bold"),
                        fg="#074A37",
                        bg="#DCDAD6"
                    ).pack(side="left")
                    if mejor_Q is None or Q < mejor_Q:
                        mejor_Q, mejor_k = Q, k+1
                Vnew[i] = mejor_Q
                nuevas_dec.append(mejor_k)
                tk.Label(
                    scrollable,
                    text=f"→ Vᵗ[{i}] = {mejor_Q:.4f}   dᵗ[{i}] = {mejor_k}",
                    font=("Arial",16,"italic"),
                    fg="#168aad",
                    bg="#DCDAD6"
                ).pack(anchor="w", pady=(0,5))

            tk.Label(
                scrollable,
                text="V = [" + ", ".join(f"{v:.4f}" for v in Vnew) + "]",
                font=("Arial",18, "bold"),
                fg="#25a244",
                bg="#DCDAD6"
            ).pack(anchor="w")

            # comprobación de tolerancia
            diff = np.max(np.abs(Vnew - Vprev))
            if diff <= epsilon:
                tk.Label(
                    scrollable,
                    text=f"\nConvergió en iteración {t} (diff={diff:.6f}).",
                    font=("Arial",16,"italic"),
                    fg="#e76f51",
                    bg="#DCDAD6"
                ).pack(anchor="w", pady=(10,2))
                V = Vnew
                decisiones = nuevas_dec
                break

            V = Vnew
            decisiones = nuevas_dec

        # --- Resultado final de la política ---
        tk.Label(
            scrollable,
            text="\n--- Política Óptima ---",
            font=("Arial",20,"bold"),
            fg="#2a9d8f",
            bg="#DCDAD6"
        ).pack(anchor="w", pady=(10,2))
        for i,k in enumerate(decisiones):
            line_frame = tk.Frame(scrollable, bg="#DCDAD6")
            line_frame.pack(anchor="w", pady=(0,5))
            tk.Label(
                line_frame,
                text=f"Estado {i}: ",
                font=("Arial", 18, "bold"),
                fg="black",
                bg="#DCDAD6"
            ).pack(side="left")

            # Parte "k* = "
            tk.Label(
                line_frame,
                text="k* = ",
                font=("Arial", 18, "italic"),
                fg="#555555",     # gris oscuro
                bg="#DCDAD6"
            ).pack(side="left")

            # Parte del valor k
            tk.Label(
                line_frame,
                text=str(k),
                font=("Arial", 30, "bold"),
                fg="#2a9d8f",     # verde destacable
                bg="#DCDAD6"
            ).pack(side="left")

        # botón de regreso
        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(fill="x")
        ttk.Button(
            btn_frame,
            text="Volver al menú",
            style='Azul.TButton',
            command=self.inicio
        ).pack(pady=10)


    
    
    
# Punto de entrada principal
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

#fer 
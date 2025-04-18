import tkinter as tk
from tkinter import messagebox
import numpy as np

# yat

# Clase principal de la aplicación
class App:
    def __init__(self, root):
        self.politicas_usuario = []
        self.root = root  # Guarda la ventana principal (root) que nos dieron como argumento, dentro del objeto (self) para poder usarla más adelante
        self.root.title("Procesos de Decisión de Markov")  # Título de la ventana
        self.root.geometry("700x500")  # Tamaño de la ventana

        self.inicio()

    def inicio(self):
        # Limpia la pantalla si hay widgets anteriores
        for widget in self.root.winfo_children():  # Te da todos los widgets (botones, etiquetas, etc.) que están en la ventana principal
            widget.destroy()

        # Etiqueta de bienvenida
        label = tk.Label(self.root, text="Procesos Estocásticos: Procesos Markovianos de Decisión", font=("Arial", 16))
        label.pack(pady=20)

        # Botón para ir al menú de lectura de datos
        read_data_btn = tk.Button(self.root, text="Leer datos", command=self.abrir_lectura_datos)
        read_data_btn.pack(pady=10)
        
        btn_ejemplo = tk.Button(self.root, text="Cargar ejemplo de datos", command=self.cargar_ejemplo_datos)
        btn_ejemplo.pack(pady=10)
        btn_ejemplo = tk.Button(self.root, text="Cargar ejemplo de datos de la tarea", command=self.cargar_ejemplo_datos_Tarea)
        btn_ejemplo.pack(pady=10)
        btn_ejemplo = tk.Button(self.root, text="Mostrar datos", command=self.mostrar_datos_ingresados)
        btn_ejemplo.pack(pady=10)

        

        # Botón para El algoritmo de Enumeracion exhaustiva de políticas
        read_data_btn = tk.Button(self.root, text="Enumeracion exhaustiva de políticas", command=self.pedir_politicas)
        read_data_btn.pack(pady=10)
        
        

        # Botón para salir
        exit_btn = tk.Button(self.root, text="Salir", command=self.root.quit)
        exit_btn.pack(pady=10)

    def abrir_lectura_datos(self):
        # Borrar la pantalla actual
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título
        titulo = tk.Label(self.root, text="Ingreso de datos", font=("Arial", 16))
        titulo.pack(pady=10)

        # Entrada: número de estados
        label_estados = tk.Label(self.root, text="Ingresa el número de estados:")
        label_estados.pack()
        self.entry_estados = tk.Entry(self.root)  # Caja de texto donde se guarda el número de estados
        self.entry_estados.pack(pady=5)

        # Entrada: número de decisiones
        label_decisiones = tk.Label(self.root, text="Ingresa el número de decisiones:")
        label_decisiones.pack()
        self.entry_decisiones = tk.Entry(self.root)  # Caja de texto donde se guarda el número de decisiones
        self.entry_decisiones.pack(pady=5)

        # Botón continuar
        continuar_btn = tk.Button(self.root, text="Continuar", command=self.iniciar_llenado)
        continuar_btn.pack(pady=10)

        # Botón regresar
        regresar_btn = tk.Button(self.root, text="Volver al menú", command=self.inicio)
        regresar_btn.pack(pady=5)

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

        # Etiqueta con número de decisión
        tk.Label(self.root, text=f"Decisión {k + 1} de {self.n_decisiones}, matriz Pij:", font=("Arial", 30)).pack(pady=30)

        self.entry_pij = []  # Lista de listas de Entry para probabilidades
        self.entry_cik = []  # Lista de Entry para costos

        frame = tk.Frame(self.root)
        frame.pack()

        # Encabezado: columnas con estados destino
        tk.Label(frame,text="Estado inicial\\destino").grid(row=0,column=0)  # Espacio vacío en esquina
        for j in range(self.n_estados):
            tk.Label(frame, text=f" {j}").grid(row=0, column=j + 1, padx=20)
        tk.Label(frame, text="Costo").grid(row=0, column=self.n_estados + 3)
        
        # Sección para ingresar Pij y Cik
        for i in range(self.n_estados):
            fila = []
            fila_fisica = i + 1  # porque la fila 0 ahora está ocupada por los encabezados

            tk.Label(frame, text=f"{i}").grid(row=fila_fisica, column=0, padx=5) #Muestra una etiqueta como “Estado 0 → Pij:” en la primera columna (columna 0) y en la fila i.
            for j in range(self.n_estados):
                e = tk.Entry(frame, width=5) #Cada e es una caja de texto (Entry) donde se colocará la probabilidad Pij.
                e.grid(row=fila_fisica, column=j + 1, padx=2)
                fila.append(e)
                #Al final de esta parte, fila = [Entry, Entry, ...] → una fila con todas las cajas de probabilidad desde estado i.
            self.entry_pij.append(fila) # Guardamos esa lista fila dentro de self.entry_pij, que será una matriz 2D de Entrys para esta decisión actual.

            tk.Label(frame, text=f"C_{i}{k + 1}").grid(row=fila_fisica, column=self.n_estados + 2)
            e_costo = tk.Entry(frame, width=6) #Entrada donde se escribirá el costo Cik para el estado i en esta decisión
            e_costo.grid(row=fila_fisica, column=self.n_estados + 3)
            self.entry_cik.append(e_costo)

        # Botón para guardar y continuar
        btn_siguiente = tk.Button(self.root, text="Guardar y continuar", command=self.guardar_decision)
        btn_siguiente.pack(pady=10)

        # Botón para volver al inicio
        btn_volver = tk.Button(self.root, text="Volver al menú", command=self.inicio)
        btn_volver.pack()

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

    def evaluar_politicas_usuario(self):
            
        self.politicas_usuario = []
        for i, fila in enumerate(self.politicas_entries):# enumerate() te da el índice (i) y el elemento actual (fila) al mismo tiempo cuando recorres una lista.
            #Ejemplo: lista = ['a', 'b', 'c']
                        #for i, letra in enumerate(lista):
                        #    print(i, letra)
                            #PRINT:
                                #0 a
                                #1 b
                                #2 c
            try:
                valores = [int(entry.get()) for entry in fila]# Lee los valores ingresados por el usuario en esa política y los convierte a int, formando una lista                   
                if len(valores) != self.n_estados: # Verifica que la política tenga tantas decisiones como estados.
                    print(f"❌ Política #{i+1} - número de decisiones no coincide con el número de estados.")
                    raise ValueError
                if any(d < 1 or d > self.n_decisiones for d in valores):#Asegura que cada decisión esté dentro del rango válido (por ejemplo, si tienes 2 decisiones, los únicos valores válidos son 0 o 1).
                    print(f"❌ Política #{i+1} - decisiones fuera de rango permitido.")
                    raise ValueError                    
                self.politicas_usuario.append(valores)#Si todo está bien, guarda esa política en la lista
            except ValueError:
                messagebox.showerror("Error", f"Política #{i+1} inválida.")
                return
            

        # Evaluamos como antes
        resultados = []  # lista de diccionarios con info por política
        mejor_politica_min = None
        mejor_politica_max = None
        mejor_valor_min = float("inf")  # Minimizar
        mejor_valor_max = float("inf")  # Maximizar
        
        tk.Label(self.root, text="📊 Resultados por política", font=("Arial", 20)).pack(pady=10)
        frame = tk.Frame(self.root)
        frame.pack()
        
        for idx, politica in enumerate(self.politicas_usuario):
        #for politica in self.politicas_usuario:
            #print(f"\n🔍 Política #{idx+1}: {politica}")
            
            tk.Label(self.root, text= f"\n🔍 Política #{idx+1}: {politica}", font=("Arial", 14)).pack(pady=5)
            
            P = np.array([self.Pij[politica[i] - 1][i] for i in range(self.n_estados)])#una matriz P de tamaño n_estados x n_estados, específica de esa política.
            C = np.array([self.Cik[politica[i] - 1][i] for i in range(self.n_estados)]) # costos para cada estado usando la decisión correspondiente según la política.

            #print("📌 Matriz de transición P:")
            #print(P)
            #print("📌 Vector de costos C:")
            #print(C)
            
            # Crear matriz A = (P^T - I), y vector b
            A = P.T.copy()#matriz de transición transpuesta
            for i in range(self.n_estados):
                A[i][i] -= 1
            A[-1] = np.ones(self.n_estados)# suma de π = 1
            b = np.zeros(self.n_estados)#vector del lado derecho: ceros, excepto un 1 al final
            b[-1] = 1
            
            #print("📐 Matriz A = P^T - I con última fila = 1:")
            #print(A)
            #print("📐 Vector b:")
            #print(b)

            try:
                pi = np.linalg.solve(A, b)#vector estacionario
                # Mostrar el vector π en la ventana principal
                pi_texto = "π = [" + ", ".join([f"{round(x, 4)}" for x in pi]) + "]"
                tk.Label(self.root, text=pi_texto, font=("Arial", 14), fg="blue").pack(pady=5)
                
                costo_esperado = np.dot(pi, C)#costo promedio esperado de la política
                print(f"Política {politica} → Costo esperado: {round(costo_esperado, 4)}")
                tk.Label(self.root, text=f"Política {politica} → Costo esperado: {round(costo_esperado, 4)}", font=("Arial", 14)).pack(pady=5)
                if costo_esperado < mejor_valor_min:
                    mejor_valor_min = costo_esperado
                    mejor_politica_min = politica.copy()
                    #print("📉 Esta es la mejor política (mínima) hasta ahora ✅")
                if costo_esperado > mejor_valor_max:
                    mejor_valor_max = costo_esperado
                    mejor_politica_max = politica.copy()
                    #print("📈 Esta es la mejor política (máxima) hasta ahora ✅")

            except np.linalg.LinAlgError:
                print(f"Política {politica} → Sistema sin solución")
                print("❌ No se pudo resolver el sistema (matriz no invertible)")
        
        
        for res in resultados:
            texto = f"🔹 Política #{res['indice']}: {res['politica']}\n"
            if isinstance(res['costo'], str):
                texto += "   ❌ Sistema sin solución\n\n"
            else:
                texto += f"   π: {[round(x, 6) for x in res['pi']]}\n"
                texto += f"   E(CRi): {round(res['costo'], 6)}\n\n"
            tk.Label(frame, text=texto, justify="left", anchor="w").pack(fill="x", padx=10)

        def mostrar_resultado(tipo):
            if tipo == "min" and mejor_politica_min:
                messagebox.showinfo("Política Óptima (Minimizar)", 
                                    f"Política: {mejor_politica_min}\nE(CRi): {round(mejor_valor_min, 6)}")
            elif tipo == "max" and mejor_politica_max:
                messagebox.showinfo("Política Óptima (Maximizar)", 
                                    f"Política: {mejor_politica_max}\nE(CRi): {round(mejor_valor_max, 6)}")

        # Botones para mostrar política óptima
        tk.Button(self.root, text="Mostrar política para minimizar", command=lambda: mostrar_resultado("min")).pack(pady=5)
        tk.Button(self.root, text="Mostrar política para maximizar", command=lambda: mostrar_resultado("max")).pack(pady=5)
        tk.Button(self.root, text="Cerrar", command=self.root.destroy).pack(pady=10)
    
    
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

    def cargar_ejemplo_datos_Tarea(self):
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

    def mostrar_datos_ingresados(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="📋 Datos ingresados", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text=f"Número de estados: {self.n_estados}").pack()
        tk.Label(self.root, text=f"Número de decisiones: {self.n_decisiones}").pack(pady=5)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Mostrar matriz Pij por decisión
        for k in range(self.n_decisiones):
            tk.Label(frame, text=f"Matriz de transición Pij para decisión {k + 1}:", font=("Arial", 12, "bold")).pack(anchor='w', pady=5)
            for i in range(self.n_estados):
                fila = f"Estado {i} → " + str(self.Pij[k][i])
                tk.Label(frame, text=fila).pack(anchor='w')

        # Mostrar matriz de costos Cik
        tk.Label(frame, text="\nMatriz de costos Cik:", font=("Arial", 12, "bold")).pack(anchor='w', pady=5)
        for k in range(self.n_decisiones):
            fila_costos = f"Decisión {k + 1} → {self.Cik[k]}"
            tk.Label(frame, text=fila_costos).pack(anchor='w')

        # Botones de acción
        btn_corregir = tk.Button(self.root, text="Corregir datos", command=lambda: self.llenar_decision(0))
        btn_corregir.pack(pady=10)

        btn_continuar = tk.Button(self.root, text="Continuar a ingreso de políticas", command=self.pedir_politicas)
        btn_continuar.pack(pady=5)

        btn_inicio = tk.Button(self.root, text="Volver al menú", command=self.inicio)
        btn_inicio.pack(pady=5)
        
        

# Punto de entrada principal
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

#fer 
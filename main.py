import tkinter as tk
from tkinter import ttk, messagebox
import random
from abc import ABC, abstractmethod
from typing import List

# --- LÓGICA DE ALGORITMOS ---

class Algoritmo(ABC):
    def __init__(self) -> None:
        self._pasos: List[List[int]] = []

    @abstractmethod
    def ordenar(self, lista: List[int]) -> List[int]:
        pass

    def obtener_pasos(self) -> List[List[int]]:
        return self._pasos

    def registrar_paso(self, paso: List[int]) -> None:
        self._pasos.append(paso)

class AlgoritmoBusqueda(ABC):
    def __init__(self) -> None:
        # Los pasos guardan una tupla: (estado_lista, indices_comparados, indice_encontrado_o_menos1)
        self._pasos: List[tuple] = []

    @abstractmethod
    def buscar(self, lista: List[int], objetivo: int) -> int:
        pass

    def obtener_pasos(self) -> List[tuple]:
        return self._pasos

    def registrar_paso(self, paso: tuple) -> None:
        self._pasos.append(paso)

class BusquedaBinaria(AlgoritmoBusqueda):
    def buscar(self, lista: List[int], objetivo: int) -> int:
        lista_o = lista.copy()
        lista_o.sort() # La búsqueda binaria requiere una lista ordenada
        self._pasos = []
        
        low = 0
        high = len(lista_o) - 1
        
        while low <= high:
            mid = (low + high) // 2
            
            # Resaltar límites y pivote actual
            self.registrar_paso((lista_o.copy(), [low, mid, high], -1))
            
            if lista_o[mid] == objetivo:
                # Encontrado
                self.registrar_paso((lista_o.copy(), [], mid))
                return mid
            elif lista_o[mid] < objetivo:
                low = mid + 1
            else:
                high = mid - 1
                
        # No encontrado
        self.registrar_paso((lista_o.copy(), [], -1))
        return -1

class GestorDatos:
    @staticmethod
    def generar_lista_aleatoria(tamano: int, bajo: int = 1, alto: int = 100) -> List[int]:
        if tamano <= 0: raise ValueError("Tamaño inválido")
        return [random.randint(bajo, alto) for _ in range(tamano)]

class BubbleSort(Algoritmo):
    def ordenar(self, lista: List[int]) -> List[int]:
        n = len(lista)
        lista_o = lista.copy()
        self._pasos = [] # Reiniciar pasos
        self.registrar_paso(lista_o.copy())
        for i in range(n):
            intercambiado = False
            for j in range(0, n - i - 1):
                if lista_o[j] > lista_o[j + 1]:
                    lista_o[j], lista_o[j + 1] = lista_o[j + 1], lista_o[j]
                    intercambiado = True
                    self.registrar_paso(lista_o.copy())
            if not intercambiado: break
        return lista_o

class QuickSort(Algoritmo):
    def ordenar(self, lista: List[int]) -> List[int]:
        lista_o = lista.copy()
        self._pasos = [] # Reiniciar pasos
        self.registrar_paso(lista_o.copy())
        self._quicksort(lista_o, 0, len(lista_o) - 1)
        return lista_o

    def _quicksort(self, lista: List[int], low: int, high: int) -> None:
        if low < high:
            pi = self._partition(lista, low, high)
            self._quicksort(lista, low, pi - 1)
            self._quicksort(lista, pi + 1, high)

    def _partition(self, lista: List[int], low: int, high: int) -> int:
        pivot = lista[high]
        i = low - 1
        for j in range(low, high):
            if lista[j] < pivot:
                i += 1
                if i != j:
                    lista[i], lista[j] = lista[j], lista[i]
                    self.registrar_paso(lista.copy())
        if i + 1 != high:
            lista[i + 1], lista[high] = lista[high], lista[i + 1]
            self.registrar_paso(lista.copy())
        return i + 1

class InsertionSort(Algoritmo):
    def ordenar(self, lista: List[int]) -> List[int]:
        lista_o = lista.copy()
        self._pasos = [] # Reiniciar pasos
        self.registrar_paso(lista_o.copy())
        
        for i in range(1, len(lista_o)):
            key = lista_o[i]
            j = i - 1
            
            while j >= 0 and lista_o[j] > key:
                lista_o[j + 1] = lista_o[j]
                self.registrar_paso(lista_o.copy())
                j -= 1
                
            lista_o[j + 1] = key
            self.registrar_paso(lista_o.copy())
            
        return lista_o

# --- INTERFAZ GRÁFICA ---

class AppAlgoritmos:
    def __init__(self, root):
        self.root = root
        self.root.title("Explorador de Algoritmos - Grupo 6")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        self.lista_actual = []
        self.algoritmos = {"Bubble Sort": BubbleSort(), "Quick Sort": QuickSort(), "Insertion Sort": InsertionSort()}
        self.algoritmos_busqueda = {"Búsqueda Binaria": BusquedaBinaria()}
        self.comparaciones = 0

        self._crear_interfaz()

    def _crear_interfaz(self):
        # Panel Superior (Controles)
        panel_control = tk.Frame(self.root, pady=10, bg="#dcdcdc")
        panel_control.pack(fill="x")

        tk.Label(panel_control, text="Algoritmo:", bg="#dcdcdc").pack(side="left", padx=5)
        self.combo_algoritmo = ttk.Combobox(panel_control, values=list(self.algoritmos.keys()) + list(self.algoritmos_busqueda.keys()), width=15)
        self.combo_algoritmo.pack(side="left", padx=5)
        self.combo_algoritmo.current(0)

        # Entrada para el objetivo de búsqueda
        tk.Label(panel_control, text="Objetivo:", bg="#dcdcdc").pack(side="left", padx=2)
        self.entry_objetivo = tk.Entry(panel_control, width=5)
        self.entry_objetivo.pack(side="left", padx=2)

        # Entrada de datos manual
        tk.Label(panel_control, text="Datos (comas):", bg="#dcdcdc").pack(side="left", padx=2)
        self.entry_datos = tk.Entry(panel_control, width=15)
        self.entry_datos.pack(side="left", padx=2)
        
        btn_cargar = tk.Button(panel_control, text="Cargar Datos", command=self.cargar_datos_manuales)
        btn_cargar.pack(side="left", padx=5)

        btn_generar = tk.Button(panel_control, text="Generar Datos", command=self.generar_datos)
        btn_generar.pack(side="left", padx=5)

        # Control de velocidad
        tk.Label(panel_control, text="Velocidad (ms):", bg="#dcdcdc").pack(side="left", padx=2)
        self.scale_velocidad = tk.Scale(panel_control, from_=10, to=1000, orient="horizontal", bg="#dcdcdc", resolution=10, length=100)
        self.scale_velocidad.set(50)
        self.scale_velocidad.pack(side="left", padx=2)

        btn_iniciar = tk.Button(panel_control, text="Iniciar", command=self.ejecutar_animacion, bg="#4caf50", fg="white")
        btn_iniciar.pack(side="left", padx=5)

        # Panel para etiquetas
        panel_info = tk.Frame(self.root, bg="#f0f0f0")
        panel_info.pack(fill="x", padx=20)
        self.lbl_comparaciones = tk.Label(panel_info, text="Pasos/Comparaciones: 0", bg="#f0f0f0", font=("Arial", 12))
        self.lbl_comparaciones.pack(side="left")

        # Área de Visualización (Canvas)
        self.canvas = tk.Canvas(self.root, bg="white", height=400)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)

    def cargar_datos_manuales(self):
        texto = self.entry_datos.get()
        if not texto:
            messagebox.showwarning("Atención", "Ingresa una lista de números")
            return
        try:
            self.lista_actual = [int(x.strip()) for x in texto.split(',')]
            self.dibujar_lista(self.lista_actual, color_barras=None)
        except ValueError:
            messagebox.showerror("Error", "Formato inválido. Usa números enteros separados por comas (ej: 5,2,9,1).")

    def generar_datos(self):
        try:
            self.lista_actual = GestorDatos.generar_lista_aleatoria(tamano=20)
            self.dibujar_lista(self.lista_actual, color_barras=None)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def dibujar_lista(self, lista, color_barras=None, resaltados=None, encontrado=None):
        self.canvas.delete("all")
        if not lista: return

        self.canvas.update_idletasks() # Asegurar dimensiones actualizadas
        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()
        
        # Fallback de tamaño inicial
        if c_width <= 1: c_width = 760
        if c_height <= 1: c_height = 400
        
        ancho_barra = c_width / len(lista)
        max_val = max(lista)
        if max_val == 0: max_val = 1
        
        for i, valor in enumerate(lista):
            x0 = i * ancho_barra
            y0 = c_height - (valor * (c_height / max_val) * 0.9) # 90% del alto
            x1 = (i + 1) * ancho_barra
            y1 = c_height
            
            # Si no hay color especificado, usar diferentes colores (gradiente según el valor)
            color = color_barras
            if color is None:
                intensidad = int((valor / max_val) * 200) + 55 # 55 a 255
                color = f"#{intensidad:02x}90{255-intensidad:02x}" # Tono purpura/azulado a rojizo

            if resaltados and i in resaltados:
                color = "yellow"
            if encontrado is not None and i == encontrado:
                color = "#4caf50" # Verde para el encontrado

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white")
            self.canvas.create_text((x0 + x1) / 2, y0 - 10, text=str(valor), fill="black", font=("Arial", 10))

    def ejecutar_animacion(self):
        nombre_alg = self.combo_algoritmo.get()
        
        if not self.lista_actual:
            messagebox.showwarning("Atención", "Primero genera o carga datos")
            return

        # Reiniciar contador
        self.comparaciones = 0
        self.lbl_comparaciones.config(text=f"Pasos/Comparaciones: {self.comparaciones}")

        if nombre_alg in self.algoritmos:
            alg = self.algoritmos[nombre_alg]
            alg.ordenar(self.lista_actual)
            pasos = alg.obtener_pasos()

            def animar_ordenamiento(idx):
                if idx < len(pasos):
                    self.comparaciones = idx + 1
                    self.lbl_comparaciones.config(text=f"Pasos/Comparaciones: {self.comparaciones}")
                    self.dibujar_lista(pasos[idx], color_barras=None)
                    velocidad = self.scale_velocidad.get()
                    self.root.after(velocidad, lambda: animar_ordenamiento(idx + 1))
                else:
                    self.dibujar_lista(pasos[-1], color_barras="#4caf50")
                    messagebox.showinfo("Listo", "Ordenamiento completado")
            animar_ordenamiento(0)

        elif nombre_alg in self.algoritmos_busqueda:
            try:
                objetivo = int(self.entry_objetivo.get().strip())
            except ValueError:
                messagebox.showwarning("Atención", "Ingresa un número válido en 'Objetivo' para buscar")
                return

            alg = self.algoritmos_busqueda[nombre_alg]
            
            # Aseguramos que la lista original y actual estén ordenadas visualmente
            self.lista_actual.sort()
            
            alg.buscar(self.lista_actual, objetivo)
            pasos = alg.obtener_pasos()

            def animar_busqueda(idx):
                if idx < len(pasos):
                    self.comparaciones = idx + 1
                    self.lbl_comparaciones.config(text=f"Pasos/Comparaciones: {self.comparaciones}")
                    
                    estado_lista, resaltados, encontrado = pasos[idx]
                    self.dibujar_lista(estado_lista, color_barras=None, resaltados=resaltados, encontrado=encontrado if encontrado != -1 else None)
                    
                    velocidad = self.scale_velocidad.get()
                    self.root.after(velocidad, lambda: animar_busqueda(idx + 1))
                else:
                    _, _, encontrado = pasos[-1]
                    if encontrado != -1:
                        messagebox.showinfo("Listo", f"Elemento encontrado en el índice {encontrado}")
                    else:
                        messagebox.showinfo("Listo", "Elemento no encontrado en la lista")

            animar_busqueda(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppAlgoritmos(root)
    root.mainloop()
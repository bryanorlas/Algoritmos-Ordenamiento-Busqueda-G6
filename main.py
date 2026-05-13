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

# --- INTERFAZ GRÁFICA ---

class AppAlgoritmos:
    def __init__(self, root):
        self.root = root
        self.root.title("Explorador de Algoritmos - Grupo 6")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        self.lista_actual = []
        self.algoritmos = {"Bubble Sort": BubbleSort(), "Quick Sort": QuickSort()}

        self._crear_interfaz()

    def _crear_interfaz(self):
        # Panel Superior (Controles)
        panel_control = tk.Frame(self.root, pady=10, bg="#dcdcdc")
        panel_control.pack(fill="x")

        tk.Label(panel_control, text="Algoritmo:", bg="#dcdcdc").pack(side="left", padx=5)
        self.combo_algoritmo = ttk.Combobox(panel_control, values=list(self.algoritmos.keys()))
        self.combo_algoritmo.pack(side="left", padx=5)
        self.combo_algoritmo.current(0)

        btn_generar = tk.Button(panel_control, text="Generar Datos", command=self.generar_datos)
        btn_generar.pack(side="left", padx=5)

        btn_iniciar = tk.Button(panel_control, text="Iniciar Ordenamiento", command=self.ejecutar_animacion, bg="#4caf50", fg="white")
        btn_iniciar.pack(side="left", padx=5)

        # Área de Visualización (Canvas)
        self.canvas = tk.Canvas(self.root, bg="white", height=400)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)

    def generar_datos(self):
        try:
            self.lista_actual = GestorDatos.generar_lista_aleatoria(tamano=20)
            self.dibujar_lista(self.lista_actual)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def dibujar_lista(self, lista, color_barras="skyblue"):
        self.canvas.delete("all")
        if not lista: return

        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()
        ancho_barra = c_width / len(lista)
        
        # Normalizar altura para que quepa en el canvas
        max_val = max(lista)
        
        for i, valor in enumerate(lista):
            x0 = i * ancho_barra
            y0 = c_height - (valor * (c_height / max_val) * 0.9) # 90% del alto
            x1 = (i + 1) * ancho_barra
            y1 = c_height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_barras, outline="white")

    def ejecutar_animacion(self):
        nombre_alg = self.combo_algoritmo.get()
        alg = self.algoritmos[nombre_alg]
        
        if not self.lista_actual:
            messagebox.showwarning("Atención", "Primero genera datos")
            return

        # Obtener pasos
        alg.ordenar(self.lista_actual)
        pasos = alg.obtener_pasos()

        # Función interna para animar paso a paso
        def animar(idx):
            if idx < len(pasos):
                self.dibujar_lista(pasos[idx], color_barras="#ff9800")
                self.root.after(100, lambda: animar(idx + 1)) # Velocidad: 100ms
            else:
                self.dibujar_lista(pasos[-1], color_barras="#4caf50")
                messagebox.showinfo("Listo", "Ordenamiento completado")

        animar(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppAlgoritmos(root)
    root.mainloop()
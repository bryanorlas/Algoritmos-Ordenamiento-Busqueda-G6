import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from abc import ABC, abstractmethod
from typing import List

# --- LÓGICA DE ESTADÍSTICAS ---
class ModuloEstadisticas:
    """
    Clase encargada de registrar las estadísticas de rendimiento
    de los algoritmos (tiempo de ejecución, comparaciones e intercambios).
    """
    def __init__(self):
        self.tiempo_total = 0.0
        self.comparaciones = 0
        self.intercambios = 0

    def reset(self):
        """Reinicia las estadísticas para una nueva ejecución."""
        self.tiempo_total = 0.0
        self.comparaciones = 0
        self.intercambios = 0

# --- LÓGICA DE ALGORITMOS ---

class Algoritmo(ABC):
    """
    Clase base abstracta para los algoritmos de ordenamiento.
    Define la estructura que deben seguir todos los algoritmos.
    """
    def __init__(self) -> None:
        self._pasos: List[List[int]] = []
        self.estadisticas = ModuloEstadisticas()

    @abstractmethod
    def ordenar(self, lista: List[int]) -> List[int]:
        """Método abstracto que debe ser implementado por cada algoritmo para ordenar la lista."""
        pass

    def obtener_pasos(self) -> List[List[int]]:
        """Devuelve la lista de pasos (estados de la lista) registrados durante el ordenamiento."""
        return self._pasos

    def registrar_paso(self, paso: List[int]) -> None:
        """Guarda un estado de la lista en los pasos para la posterior animación."""
        self._pasos.append(paso)

class AlgoritmoBusqueda(ABC):
    """
    Clase base abstracta para los algoritmos de búsqueda.
    """
    def __init__(self) -> None:
        # Los pasos guardan una tupla: (estado_lista, indices_comparados, indice_encontrado_o_menos1)
        self._pasos: List[tuple] = []

    @abstractmethod
    def buscar(self, lista: List[int], objetivo: int) -> int:
        """Método abstracto que debe ser implementado por cada algoritmo para buscar un elemento."""
        pass

    def obtener_pasos(self) -> List[tuple]:
        """Devuelve los pasos registrados durante la búsqueda para la animación."""
        return self._pasos

    def registrar_paso(self, paso: tuple) -> None:
        """Guarda un estado de la búsqueda en los pasos."""
        self._pasos.append(paso)

class BusquedaBinaria(AlgoritmoBusqueda):
    """
    Implementación del algoritmo de Búsqueda Binaria.
    Requiere que la lista esté ordenada previamente.
    """
    def buscar(self, lista: List[int], objetivo: int) -> int:
        lista_o = lista.copy()
        lista_o.sort() # La búsqueda binaria requiere una lista ordenada
        self._pasos = []
        
        low = 0
        high = len(lista_o) - 1
        
        while low <= high:
            mid = (low + high) // 2
            
            # Registrar el paso actual resaltando los límites y el punto medio
            self.registrar_paso((lista_o.copy(), [low, mid, high], -1))
            
            if lista_o[mid] == objetivo:
                # Elemento encontrado
                self.registrar_paso((lista_o.copy(), [], mid))
                return mid
            elif lista_o[mid] < objetivo:
                low = mid + 1 # Descartar la mitad inferior
            else:
                high = mid - 1 # Descartar la mitad superior
                
        # Elemento no encontrado
        self.registrar_paso((lista_o.copy(), [], -1))
        return -1

class BusquedaLineal(AlgoritmoBusqueda):
    """
    Implementación del algoritmo de Búsqueda Lineal.
    Revisa secuencialmente cada elemento hasta encontrar el objetivo.
    """
    def buscar(self, lista: List[int], objetivo: int) -> int:
        lista_o = lista.copy()
        self._pasos = []
        
        for i in range(len(lista_o)):
            # Registrar el paso resaltando el elemento actual siendo evaluado
            self.registrar_paso((lista_o.copy(), [i], -1))
            
            if lista_o[i] == objetivo:
                # Elemento encontrado
                self.registrar_paso((lista_o.copy(), [], i))
                return i
                
        # Elemento no encontrado
        self.registrar_paso((lista_o.copy(), [], -1))
        return -1

class GestorDatos:
    """
    Clase utilitaria para la generación de datos aleatorios.
    """
    @staticmethod
    def generar_lista_aleatoria(tamano: int, bajo: int = 1, alto: int = 100) -> List[int]:
        """Genera una lista de números enteros aleatorios del tamaño especificado."""
        if tamano <= 0: raise ValueError("Tamaño inválido")
        return [random.randint(bajo, alto) for _ in range(tamano)]

class BubbleSort(Algoritmo):
    """
    Implementación del algoritmo de ordenamiento de Burbuja (Bubble Sort).
    """
    def ordenar(self, lista: List[int]) -> List[int]:
        n = len(lista)
        lista_o = lista.copy()
        self._pasos = [] # Reiniciar pasos para la nueva ejecución
        self.estadisticas.reset()
        self.registrar_paso(lista_o.copy())
        
        inicio = time.perf_counter()
        for i in range(n):
            intercambiado = False
            for j in range(0, n - i - 1):
                self.estadisticas.comparaciones += 1
                # Si el elemento actual es mayor que el siguiente, se intercambian
                if lista_o[j] > lista_o[j + 1]:
                    lista_o[j], lista_o[j + 1] = lista_o[j + 1], lista_o[j]
                    self.estadisticas.intercambios += 1
                    intercambiado = True
                    self.registrar_paso(lista_o.copy())
            # Optimización: Si en una pasada no hubo intercambios, la lista ya está ordenada
            if not intercambiado: break
        fin = time.perf_counter()
        
        self.estadisticas.tiempo_total = fin - inicio
        return lista_o

class QuickSort(Algoritmo):
    """
    Implementación del algoritmo de ordenamiento Quick Sort.
    Utiliza el enfoque de "divide y vencerás".
    """
    def ordenar(self, lista: List[int]) -> List[int]:
        lista_o = lista.copy()
        self._pasos = []
        self.estadisticas.reset()
        self.registrar_paso(lista_o.copy())
        
        inicio = time.perf_counter()
        self._quicksort(lista_o, 0, len(lista_o) - 1)
        fin = time.perf_counter()
        
        self.estadisticas.tiempo_total = fin - inicio
        return lista_o

    def _quicksort(self, lista: List[int], low: int, high: int) -> None:
        """Función recursiva principal de Quick Sort."""
        if low < high:
            # pi es el índice de partición, lista[pi] ya está en su lugar correcto
            pi = self._partition(lista, low, high)
            self._quicksort(lista, low, pi - 1) # Ordenar elementos antes de la partición
            self._quicksort(lista, pi + 1, high) # Ordenar elementos después de la partición

    def _partition(self, lista: List[int], low: int, high: int) -> int:
        """Toma el último elemento como pivote y lo ubica en su posición correcta."""
        pivot = lista[high]
        i = low - 1
        for j in range(low, high):
            self.estadisticas.comparaciones += 1
            if lista[j] < pivot:
                i += 1
                if i != j:
                    lista[i], lista[j] = lista[j], lista[i]
                    self.estadisticas.intercambios += 1
                    self.registrar_paso(lista.copy())
        # Ubicar el pivote en su lugar final
        if i + 1 != high:
            lista[i + 1], lista[high] = lista[high], lista[i + 1]
            self.estadisticas.intercambios += 1
            self.registrar_paso(lista.copy())
        return i + 1

class InsertionSort(Algoritmo):
    """
    Implementación del algoritmo de ordenamiento por Inserción (Insertion Sort).
    Construye la lista ordenada de a un elemento a la vez.
    """
    def ordenar(self, lista: List[int]) -> List[int]:
        lista_o = lista.copy()
        self._pasos = []
        self.estadisticas.reset()
        self.registrar_paso(lista_o.copy())
        
        inicio = time.perf_counter()
        for i in range(1, len(lista_o)):
            key = lista_o[i]
            j = i - 1
            
            # Mover los elementos de la lista que son mayores que la llave
            # a una posición adelante de su posición actual
            while j >= 0:
                self.estadisticas.comparaciones += 1
                if lista_o[j] > key:
                    lista_o[j + 1] = lista_o[j]
                    self.estadisticas.intercambios += 1
                    self.registrar_paso(lista_o.copy())
                    j -= 1
                else:
                    break
                
            lista_o[j + 1] = key
            self.registrar_paso(lista_o.copy())
            
        fin = time.perf_counter()
        self.estadisticas.tiempo_total = fin - inicio
        
        return lista_o

# --- INTERFAZ GRÁFICA ---

class AppAlgoritmos:
    """
    Clase principal que gestiona la Interfaz Gráfica de Usuario (GUI) y 
    la interacción con los algoritmos.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Explorador de Algoritmos - Grupo 6")
        self.root.geometry("850x650")
        
        # Paleta de colores mejorada
        self.color_bg = "#f4f7f6" # Fondo general (Gris muy claro)
        self.color_panel = "#ffffff" # Fondo de paneles (Blanco)
        self.color_btn = "#3498db" # Azul moderno
        self.color_btn_iniciar = "#2ecc71" # Verde moderno
        self.color_texto = "#2c3e50"
        
        self.root.config(bg=self.color_bg)

        # Configuración de estilos para ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TCombobox", padding=5, font=("Segoe UI", 10))

        self.lista_actual = []
        self.algoritmos = {"Bubble Sort": BubbleSort(), "Quick Sort": QuickSort(), "Insertion Sort": InsertionSort()}
        self.algoritmos_busqueda = {"Búsqueda Binaria": BusquedaBinaria(), "Búsqueda Lineal": BusquedaLineal()}
        self.comparaciones = 0

        self._crear_interfaz()

    def _crear_interfaz(self):
        """Construye y posiciona todos los elementos visuales de la ventana."""
        # Fuente general
        fuente_ui = ("Segoe UI", 10)
        fuente_titulo = ("Segoe UI", 10, "bold")

        # --- Panel Superior (Controles) ---
        panel_control = tk.Frame(self.root, pady=15, padx=15, bg=self.color_panel, relief="ridge", bd=1)
        panel_control.pack(fill="x", padx=10, pady=10)

        # Selección de Algoritmo
        tk.Label(panel_control, text="Algoritmo:", bg=self.color_panel, font=fuente_titulo, fg=self.color_texto).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_algoritmo = ttk.Combobox(panel_control, values=list(self.algoritmos.keys()) + list(self.algoritmos_busqueda.keys()), width=18, state="readonly")
        self.combo_algoritmo.grid(row=0, column=1, padx=5, pady=5)
        self.combo_algoritmo.current(0)

        # Entrada para el objetivo de búsqueda
        tk.Label(panel_control, text="Objetivo:", bg=self.color_panel, font=fuente_titulo, fg=self.color_texto).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_objetivo = tk.Entry(panel_control, width=8, font=fuente_ui, relief="solid", bd=1)
        self.entry_objetivo.grid(row=0, column=3, padx=5, pady=5)

        # Velocidad de animación
        tk.Label(panel_control, text="Velocidad (ms):", bg=self.color_panel, font=fuente_titulo, fg=self.color_texto).grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.scale_velocidad = tk.Scale(panel_control, from_=10, to=1000, orient="horizontal", bg=self.color_panel, resolution=10, length=120, highlightthickness=0, font=fuente_ui)
        self.scale_velocidad.set(50)
        self.scale_velocidad.grid(row=0, column=5, padx=5, pady=5)

        # --- Fila Inferior del Panel de Controles ---
        # Entrada de datos manual
        tk.Label(panel_control, text="Datos (comas):", bg=self.color_panel, font=fuente_titulo, fg=self.color_texto).grid(row=1, column=0, padx=5, pady=10, sticky="e")
        self.entry_datos = tk.Entry(panel_control, width=20, font=fuente_ui, relief="solid", bd=1)
        self.entry_datos.grid(row=1, column=1, padx=5, pady=10, columnspan=2, sticky="w")
        
        # Botones de Acción
        frame_botones = tk.Frame(panel_control, bg=self.color_panel)
        frame_botones.grid(row=1, column=3, columnspan=3, sticky="w")

        btn_cargar = tk.Button(frame_botones, text="Cargar Datos", command=self.cargar_datos_manuales, bg=self.color_btn, fg="white", font=fuente_ui, relief="flat", cursor="hand2", width=12)
        btn_cargar.pack(side="left", padx=5)

        btn_generar = tk.Button(frame_botones, text="Generar Datos", command=self.generar_datos, bg=self.color_btn, fg="white", font=fuente_ui, relief="flat", cursor="hand2", width=12)
        btn_generar.pack(side="left", padx=5)

        btn_iniciar = tk.Button(frame_botones, text="▶ Iniciar", command=self.ejecutar_animacion, bg=self.color_btn_iniciar, fg="white", font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", width=12)
        btn_iniciar.pack(side="left", padx=5)

        # --- Panel para Etiquetas (Información) ---
        panel_info = tk.Frame(self.root, bg=self.color_bg)
        panel_info.pack(fill="x", padx=15)
        
        self.lbl_comparaciones = tk.Label(panel_info, text="Pasos: 0", bg=self.color_bg, font=("Segoe UI", 12, "bold"), fg=self.color_texto)
        self.lbl_comparaciones.pack(side="left", padx=5)

        self.lbl_estadisticas = tk.Label(panel_info, text="", bg=self.color_bg, font=("Segoe UI", 11, "bold"), fg="#2980b9") # Azul para destacar
        self.lbl_estadisticas.pack(side="right", padx=5)

        # --- Área de Visualización (Canvas) ---
        self.canvas = tk.Canvas(self.root, bg="white", height=420, relief="solid", bd=1)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=10)

    def cargar_datos_manuales(self):
        """Lee los datos ingresados por el usuario y los valida."""
        texto = self.entry_datos.get().strip()
        
        if not texto:
            messagebox.showerror("Error", "La lista no puede estar vacía. Por favor, ingresa números separados por comas.")
            return
            
        try:
            # Procesar el texto dividiendo por comas, e intentar convertir a enteros
            elementos = [x.strip() for x in texto.split(',') if x.strip()]
            
            if not elementos:
                messagebox.showerror("Error", "La lista no puede estar vacía. Por favor, ingresa números válidos.")
                return

            # Si hay caracteres no numéricos, saltará ValueError
            self.lista_actual = [int(x) for x in elementos]
            self.dibujar_lista(self.lista_actual, color_barras=None)
            
        except ValueError:
            # Manejo de error si el usuario ingresó letras u otros caracteres
            messagebox.showerror("Error de Entrada", "Por favor, ingresa únicamente números enteros. Las letras o caracteres especiales no son válidos.")

    def generar_datos(self):
        """Genera una lista de datos aleatorios para la demostración."""
        try:
            self.lista_actual = GestorDatos.generar_lista_aleatoria(tamano=20)
            self.dibujar_lista(self.lista_actual, color_barras=None)
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un error inesperado:\n{e}")

    def dibujar_lista(self, lista, color_barras=None, resaltados=None, encontrado=None):
        """
        Dibuja los elementos de la lista en el canvas como un gráfico de barras.
        Permite resaltar índices específicos (por ejemplo, en comparaciones).
        """
        self.canvas.delete("all")
        if not lista: return

        self.canvas.update_idletasks() # Asegurar que las dimensiones estén actualizadas
        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()
        
        # Fallback de tamaño inicial
        if c_width <= 1: c_width = 800
        if c_height <= 1: c_height = 420
        
        ancho_barra = c_width / len(lista)
        max_val = max(lista)
        if max_val == 0: max_val = 1
        
        for i, valor in enumerate(lista):
            x0 = i * ancho_barra
            y0 = c_height - (valor * (c_height / max_val) * 0.85) # 85% del alto para dejar margen superior
            x1 = (i + 1) * ancho_barra
            y1 = c_height
            
            # Si no hay color especificado, crear un gradiente según el valor del elemento
            color = color_barras
            if color is None:
                intensidad = int((valor / max_val) * 150) + 100 # Rango para no ser muy oscuro ni muy claro
                color = f"#{intensidad:02x}b1{255-intensidad:02x}" # Gradiente azul a morado

            # Resaltar en rojo los elementos que se están comparando actualmente
            if resaltados and i in resaltados:
                color = "#e74c3c" # Rojo (Alerta/Comparación)
            
            # Resaltar en verde el elemento encontrado
            if encontrado is not None and i == encontrado:
                color = "#2ecc71" # Verde (Éxito)

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white")
            self.canvas.create_text((x0 + x1) / 2, y0 - 12, text=str(valor), fill=self.color_texto, font=("Segoe UI", 9, "bold"))

    def ejecutar_animacion(self):
        """
        Inicia la ejecución del algoritmo seleccionado.
        Maneja tanto ordenamiento como búsqueda, verificando estados previos.
        """
        nombre_alg = self.combo_algoritmo.get()
        
        # Validar que la lista no esté vacía antes de iniciar
        if not self.lista_actual:
            messagebox.showerror("Error", "La lista está vacía. Por favor genera o carga datos numéricos antes de iniciar.")
            return

        # Reiniciar el contador de pasos en la interfaz
        self.comparaciones = 0
        self.lbl_comparaciones.config(text=f"Pasos: {self.comparaciones}")
        self.lbl_estadisticas.config(text="")

        if nombre_alg in self.algoritmos:
            # Flujo para Algoritmos de Ordenamiento
            alg = self.algoritmos[nombre_alg]
            alg.ordenar(self.lista_actual)
            pasos = alg.obtener_pasos()

            def animar_ordenamiento(idx):
                """Función recursiva para animar los pasos del ordenamiento."""
                if idx < len(pasos):
                    self.comparaciones = idx + 1
                    self.lbl_comparaciones.config(text=f"Pasos: {self.comparaciones}")
                    self.dibujar_lista(pasos[idx], color_barras=None)
                    velocidad = self.scale_velocidad.get()
                    # Llama a sí misma después de 'velocidad' ms
                    self.root.after(velocidad, lambda: animar_ordenamiento(idx + 1))
                else:
                    # Finalizó la animación
                    self.dibujar_lista(pasos[-1], color_barras="#2ecc71") # Todo verde al terminar
                    stats = alg.estadisticas
                    self.lbl_estadisticas.config(text=f"Tiempo: {stats.tiempo_total:.6f} s | Comparaciones: {stats.comparaciones} | Swaps: {stats.intercambios}")
                    messagebox.showinfo("Completado", "El proceso de ordenamiento ha finalizado exitosamente.")
            animar_ordenamiento(0)

        elif nombre_alg in self.algoritmos_busqueda:
            # Flujo para Algoritmos de Búsqueda
            try:
                objetivo_str = self.entry_objetivo.get().strip()
                if not objetivo_str:
                    messagebox.showerror("Error", "El campo 'Objetivo' no puede estar vacío.")
                    return
                objetivo = int(objetivo_str)
            except ValueError:
                # Validar que el objetivo sea un número válido y no letras
                messagebox.showerror("Error de Entrada", "El 'Objetivo' de búsqueda debe ser un número entero válido. No se permiten letras.")
                return

            alg = self.algoritmos_busqueda[nombre_alg]
            
            # Para fines de visualización congruente, ordenamos la lista local si es binaria
            # (Aunque internamente BúsquedaBinaria también ordena una copia)
            if nombre_alg == "Búsqueda Binaria":
                self.lista_actual.sort()
                # Actualizamos la vista inicial ordenada antes de animar
                self.dibujar_lista(self.lista_actual)
            
            alg.buscar(self.lista_actual, objetivo)
            pasos = alg.obtener_pasos()

            def animar_busqueda(idx):
                """Función recursiva para animar los pasos de la búsqueda."""
                if idx < len(pasos):
                    self.comparaciones = idx + 1
                    self.lbl_comparaciones.config(text=f"Pasos: {self.comparaciones}")
                    
                    estado_lista, resaltados, encontrado = pasos[idx]
                    self.dibujar_lista(estado_lista, color_barras=None, resaltados=resaltados, encontrado=encontrado if encontrado != -1 else None)
                    
                    velocidad = self.scale_velocidad.get()
                    self.root.after(velocidad, lambda: animar_busqueda(idx + 1))
                else:
                    # Finalizó la animación de búsqueda
                    _, _, encontrado = pasos[-1]
                    if encontrado != -1:
                        messagebox.showinfo("Búsqueda Completada", f"¡Elemento {objetivo} encontrado en el índice {encontrado}!")
                    else:
                        messagebox.showinfo("Búsqueda Completada", f"El elemento {objetivo} NO se encuentra en la lista.")

            animar_busqueda(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppAlgoritmos(root)
    root.mainloop()
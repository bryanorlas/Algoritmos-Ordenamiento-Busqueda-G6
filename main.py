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
        self.root.geometry("900x750")
        
        # Paleta de colores limpia y moderna
        self.color_bg = "#f0f4f8"        # Fondo general (Gris-azul muy claro)
        self.color_panel = "#ffffff"     # Fondo de paneles (Blanco puro)
        self.color_btn_primary = "#3b82f6" # Azul vibrante moderno
        self.color_btn_success = "#10b981" # Verde esmeralda moderno
        self.color_texto = "#1f2937"     # Texto oscuro (Gris pizarra)
        self.color_texto_sec = "#4b5563" # Texto secundario
        
        self.root.config(bg=self.color_bg)

        # Configuración de estilos para ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Estilos personalizados para ttk
        self.style.configure("TCombobox", padding=5, font=("Inter", 10))
        self.style.configure("TLabelframe", background=self.color_bg, foreground=self.color_texto)
        self.style.configure("TLabelframe.Label", font=("Inter", 11, "bold"), background=self.color_bg, foreground=self.color_texto)

        self.lista_actual = []
        self.algoritmos = {"Bubble Sort": BubbleSort(), "Quick Sort": QuickSort(), "Insertion Sort": InsertionSort()}
        self.algoritmos_busqueda = {"Búsqueda Binaria": BusquedaBinaria(), "Búsqueda Lineal": BusquedaLineal()}
        self.comparaciones = 0

        self._crear_interfaz()

    def _crear_interfaz(self):
        """
        Construye y posiciona todos los elementos visuales de la ventana.
        Utiliza LabelFrames para agrupar lógicamente los controles y un layout 
        mejorado con padx/pady para que la interfaz 'respire'.
        """
        # Fuentes para mejor legibilidad
        fuente_ui = ("Inter", 10)
        fuente_titulo = ("Inter", 10, "bold")
        fuente_dashboard = ("Inter", 14, "bold")
        fuente_dashboard_lbl = ("Inter", 10)

        # Contenedor principal superior
        frame_superior = tk.Frame(self.root, bg=self.color_bg)
        frame_superior.pack(fill="x", padx=20, pady=15)

        # --- Panel 1: Configuración ---
        lf_config = ttk.LabelFrame(frame_superior, text="Configuración")
        lf_config.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Contenedor interno para padding
        panel_config = tk.Frame(lf_config, bg=self.color_panel, padx=15, pady=15)
        panel_config.pack(fill="both", expand=True)

        tk.Label(panel_config, text="Algoritmo:", bg=self.color_panel, font=fuente_titulo, fg=self.color_texto).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_algoritmo = ttk.Combobox(panel_config, values=list(self.algoritmos.keys()) + list(self.algoritmos_busqueda.keys()), width=20, state="readonly")
        self.combo_algoritmo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.combo_algoritmo.current(0)

        tk.Label(panel_config, text="Velocidad (ms):", bg=self.color_panel, font=fuente_titulo, fg=self.color_texto).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.scale_velocidad = tk.Scale(panel_config, from_=10, to=1000, orient="horizontal", bg=self.color_panel, resolution=10, length=150, highlightthickness=0, font=fuente_ui, troughcolor="#e5e7eb")
        self.scale_velocidad.set(50)
        self.scale_velocidad.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # --- Panel 2: Datos ---
        lf_datos = ttk.LabelFrame(frame_superior, text="Datos y Búsqueda")
        lf_datos.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        panel_datos = tk.Frame(lf_datos, bg=self.color_panel, padx=15, pady=15)
        panel_datos.pack(fill="both", expand=True)

        # Fila 1: Datos manuales
        tk.Label(panel_datos, text="Ingreso Manual (comas):", bg=self.color_panel, font=fuente_titulo, fg=self.color_texto).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_datos = tk.Entry(panel_datos, width=22, font=fuente_ui, relief="solid", bd=1, highlightbackground="#d1d5db")
        self.entry_datos.grid(row=0, column=1, padx=5, pady=5)
        
        btn_cargar = tk.Button(panel_datos, text="Cargar", command=self.cargar_datos_manuales, bg=self.color_btn_primary, fg="white", font=fuente_ui, relief="flat", cursor="hand2", width=10)
        btn_cargar.grid(row=0, column=2, padx=5, pady=5)

        # Fila 2: Objetivo de búsqueda
        tk.Label(panel_datos, text="Objetivo (Búsqueda):", bg=self.color_panel, font=fuente_titulo, fg=self.color_texto).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_objetivo = tk.Entry(panel_datos, width=22, font=fuente_ui, relief="solid", bd=1, highlightbackground="#d1d5db")
        self.entry_objetivo.grid(row=1, column=1, padx=5, pady=5)

        # --- Panel 3: Ejecución ---
        # Panel centralizado para los botones de acción principal
        panel_ejecucion = tk.Frame(self.root, bg=self.color_bg)
        panel_ejecucion.pack(fill="x", padx=20, pady=(0, 10))

        btn_generar = tk.Button(panel_ejecucion, text="Generar Datos Aleatorios", command=self.generar_datos, bg=self.color_btn_primary, fg="white", font=fuente_titulo, relief="flat", cursor="hand2", padx=15, pady=8)
        btn_generar.pack(side="left", padx=(0, 10))

        btn_iniciar = tk.Button(panel_ejecucion, text="▶ INICIAR ANIMACIÓN", command=self.ejecutar_animacion, bg=self.color_btn_success, fg="white", font=("Inter", 11, "bold"), relief="flat", cursor="hand2", padx=20, pady=8)
        btn_iniciar.pack(side="left")

        # --- Leyenda Visual (Encima del canvas) ---
        panel_leyenda = tk.Frame(self.root, bg=self.color_bg)
        panel_leyenda.pack(fill="x", padx=20, pady=(5, 0))
        
        tk.Label(panel_leyenda, text="Leyenda:", bg=self.color_bg, font=fuente_titulo, fg=self.color_texto).pack(side="left", padx=(0, 10))
        
        # Función auxiliar para crear items de leyenda
        def crear_item_leyenda(padre, color, texto):
            f = tk.Frame(padre, bg=self.color_bg)
            f.pack(side="left", padx=10)
            tk.Label(f, bg=color, width=2, height=1, relief="solid", bd=1).pack(side="left")
            tk.Label(f, text=texto, bg=self.color_bg, font=fuente_ui, fg=self.color_texto).pack(side="left", padx=(5, 0))

        crear_item_leyenda(panel_leyenda, "#8ca8d9", "Elemento Normal")
        crear_item_leyenda(panel_leyenda, "#ef4444", "Comparando (Rojo)")
        crear_item_leyenda(panel_leyenda, "#10b981", "Terminado / Encontrado (Verde)")

        # --- Área de Visualización (Canvas) ---
        self.canvas = tk.Canvas(self.root, bg="white", height=380, relief="flat", highlightthickness=1, highlightbackground="#e5e7eb")
        self.canvas.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Dashboard de Estadísticas (Panel Inferior) ---
        dashboard = tk.Frame(self.root, bg="#1e293b", pady=15) # Fondo oscuro para contraste
        dashboard.pack(fill="x", side="bottom")

        # Configurar columnas del dashboard para distribución equitativa
        dashboard.columnconfigure(0, weight=1)
        dashboard.columnconfigure(1, weight=1)
        dashboard.columnconfigure(2, weight=1)

        # Valores dinámicos del dashboard
        self.lbl_pasos_val = tk.Label(dashboard, text="0", bg="#1e293b", fg="white", font=fuente_dashboard)
        self.lbl_pasos_val.grid(row=0, column=0)
        tk.Label(dashboard, text="PASOS", bg="#1e293b", fg="#94a3b8", font=fuente_dashboard_lbl).grid(row=1, column=0)

        self.lbl_tiempo_val = tk.Label(dashboard, text="0.000 s", bg="#1e293b", fg="#38bdf8", font=fuente_dashboard)
        self.lbl_tiempo_val.grid(row=0, column=1)
        tk.Label(dashboard, text="TIEMPO (seg)", bg="#1e293b", fg="#94a3b8", font=fuente_dashboard_lbl).grid(row=1, column=1)

        self.lbl_comp_val = tk.Label(dashboard, text="0", bg="#1e293b", fg="#fbbf24", font=fuente_dashboard)
        self.lbl_comp_val.grid(row=0, column=2)
        tk.Label(dashboard, text="COMPARACIONES / SWAPS", bg="#1e293b", fg="#94a3b8", font=fuente_dashboard_lbl).grid(row=1, column=2)

    def cargar_datos_manuales(self):
        """
        Lee los datos ingresados manualmente por el usuario.
        Implementa un manejo de errores riguroso para evitar caídas del programa.
        """
        texto = self.entry_datos.get().strip()
        
        if not texto:
            messagebox.showwarning("Atención", "El campo de datos está vacío.\nPor favor, ingresa números separados por comas.")
            return
            
        try:
            # Separar por comas e ignorar espacios en blanco
            elementos = [x.strip() for x in texto.split(',') if x.strip()]
            
            if not elementos:
                messagebox.showwarning("Atención", "No se detectaron números válidos.\nAsegúrate de ingresarlos correctamente.")
                return

            # Intentar convertir cada elemento a entero. Si hay letras, lanza ValueError
            self.lista_actual = [int(x) for x in elementos]
            self.dibujar_lista(self.lista_actual, color_barras=None)
            
            # Limpiar dashboard al cargar nuevos datos
            self.reset_dashboard()
            messagebox.showinfo("Éxito", "Datos cargados correctamente.")
            
        except ValueError:
            # Capturar letras o caracteres especiales
            messagebox.showerror("Error de Formato", "Se encontraron caracteres no numéricos.\nPor favor, ingresa ÚNICAMENTE números enteros separados por comas.")

    def generar_datos(self):
        """Genera una lista de datos aleatorios para la demostración y la dibuja."""
        try:
            self.lista_actual = GestorDatos.generar_lista_aleatoria(tamano=20)
            self.dibujar_lista(self.lista_actual, color_barras=None)
            self.reset_dashboard()
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error al generar datos:\n{e}")

    def reset_dashboard(self):
        """Limpia los valores del dashboard de estadísticas para una nueva ejecución."""
        self.comparaciones = 0
        self.lbl_pasos_val.config(text="0")
        self.lbl_tiempo_val.config(text="0.000 s")
        self.lbl_comp_val.config(text="0")

    def dibujar_lista(self, lista, color_barras=None, resaltados=None, encontrado=None):
        """
        Dibuja los elementos de la lista en el canvas como un gráfico de barras.
        Aplica los colores definidos en la leyenda visual para indicar estados.
        """
        self.canvas.delete("all")
        if not lista: return

        self.canvas.update_idletasks() # Asegurar que las dimensiones estén actualizadas
        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()
        
        # Fallback de tamaño por si el canvas aún no se ha dibujado completamente
        if c_width <= 1: c_width = 860
        if c_height <= 1: c_height = 380
        
        ancho_barra = c_width / len(lista)
        max_val = max(lista)
        if max_val == 0: max_val = 1
        
        for i, valor in enumerate(lista):
            x0 = i * ancho_barra
            y0 = c_height - (valor * (c_height / max_val) * 0.85) # Margen superior del 15%
            x1 = (i + 1) * ancho_barra
            y1 = c_height
            
            # Lógica de color según la leyenda y el estado del elemento
            color = color_barras
            if color is None:
                intensidad = int((valor / max_val) * 150) + 100
                color = f"#{intensidad:02x}b1{255-intensidad:02x}" # Gradiente base

            # Elementos comparándose (Rojo)
            if resaltados and i in resaltados:
                color = "#ef4444" 
            
            # Elemento encontrado o terminado (Verde)
            if encontrado is not None and i == encontrado:
                color = "#10b981" 

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=1)
            # Dibujar el valor numérico sobre la barra
            self.canvas.create_text((x0 + x1) / 2, y0 - 12, text=str(valor), fill=self.color_texto, font=("Inter", 9, "bold"))

    def actualizar_pasos(self, num_paso):
        """Actualiza el contador de pasos en el dashboard en tiempo real."""
        self.comparaciones = num_paso
        self.lbl_pasos_val.config(text=str(self.comparaciones))

    def ejecutar_animacion(self):
        """
        Inicia la ejecución del algoritmo seleccionado.
        Realiza validaciones rigurosas antes de comenzar para evitar errores de ejecución.
        """
        nombre_alg = self.combo_algoritmo.get()
        
        # Validación 1: Lista vacía
        if not self.lista_actual:
            messagebox.showwarning("Faltan Datos", "No hay datos para procesar.\nPor favor, ingresa datos manualmente o haz clic en 'Generar Datos Aleatorios'.")
            return

        # Reiniciar el dashboard antes de iniciar nueva ejecución
        self.reset_dashboard()

        if nombre_alg in self.algoritmos:
            # --- Flujo de Algoritmos de Ordenamiento ---
            alg = self.algoritmos[nombre_alg]
            alg.ordenar(self.lista_actual)
            pasos = alg.obtener_pasos()

            def animar_ordenamiento(idx):
                """Bucle recursivo asíncrono para la animación de ordenamiento."""
                if idx < len(pasos):
                    self.actualizar_pasos(idx + 1)
                    self.dibujar_lista(pasos[idx], color_barras=None)
                    velocidad = self.scale_velocidad.get()
                    self.root.after(velocidad, lambda: animar_ordenamiento(idx + 1))
                else:
                    # Animación finalizada
                    self.dibujar_lista(pasos[-1], color_barras="#10b981") # Todo verde
                    stats = alg.estadisticas
                    # Actualizar dashboard con resultados finales calculados
                    self.lbl_tiempo_val.config(text=f"{stats.tiempo_total:.4f} s")
                    self.lbl_comp_val.config(text=f"{stats.comparaciones} / {stats.intercambios}")
                    messagebox.showinfo("Ordenamiento Completado", "El algoritmo ha terminado exitosamente.")
            
            animar_ordenamiento(0)

        elif nombre_alg in self.algoritmos_busqueda:
            # --- Flujo de Algoritmos de Búsqueda ---
            
            # Validación 2: Campo de objetivo vacío
            objetivo_str = self.entry_objetivo.get().strip()
            if not objetivo_str:
                messagebox.showwarning("Falta Objetivo", "Para ejecutar una búsqueda, debes ingresar un número en el campo 'Objetivo (Búsqueda)'.")
                return
                
            # Validación 3: Objetivo no numérico (ej. letras o caracteres)
            try:
                objetivo = int(objetivo_str)
            except ValueError:
                messagebox.showerror("Objetivo Inválido", "El 'Objetivo' debe ser un número entero válido.\nNo se permiten letras ni símbolos especiales.")
                return

            alg = self.algoritmos_busqueda[nombre_alg]
            
            # Preparación visual para Búsqueda Binaria (requiere lista ordenada)
            if nombre_alg == "Búsqueda Binaria":
                self.lista_actual.sort()
                self.dibujar_lista(self.lista_actual)
            
            alg.buscar(self.lista_actual, objetivo)
            pasos = alg.obtener_pasos()

            def animar_busqueda(idx):
                """Bucle recursivo asíncrono para la animación de búsqueda."""
                if idx < len(pasos):
                    self.actualizar_pasos(idx + 1)
                    estado_lista, resaltados, encontrado = pasos[idx]
                    self.dibujar_lista(estado_lista, color_barras=None, resaltados=resaltados, encontrado=encontrado if encontrado != -1 else None)
                    velocidad = self.scale_velocidad.get()
                    self.root.after(velocidad, lambda: animar_busqueda(idx + 1))
                else:
                    # Animación finalizada
                    _, _, encontrado = pasos[-1]
                    if encontrado != -1:
                        messagebox.showinfo("Búsqueda Exitosa", f"El elemento {objetivo} fue encontrado en la posición {encontrado}.")
                    else:
                        messagebox.showinfo("Búsqueda Fallida", f"El elemento {objetivo} NO se encuentra en la lista.")

            animar_busqueda(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppAlgoritmos(root)
    root.mainloop()
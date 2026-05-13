from abc import ABC, abstractmethod
import random
from typing import List

class Algoritmo(ABC):
    """
    Clase abstracta base para los algoritmos de ordenamiento.
    Proporciona la estructura para implementar métodos de ordenamiento y registrar sus pasos.
    """
    def __init__(self) -> None:
        self._pasos: List[List[int]] = []

    @abstractmethod
    def ordenar(self, lista: List[int]) -> List[int]:
        """
        Método abstracto que debe ser implementado por cada algoritmo específico
        para ordenar una lista de números.
        
        :param lista: Lista de enteros a ordenar.
        :return: Lista de enteros ordenada.
        """
        pass

    def obtener_pasos(self) -> List[List[int]]:
        """
        Retorna la lista de pasos registrados durante la ejecución del algoritmo.
        
        :return: Lista de estados de la lista en cada paso.
        """
        return self._pasos

    def registrar_paso(self, paso: List[int]) -> None:
        """
        Agrega un paso a la lista de pasos. (Método de apoyo para encapsulamiento)
        
        :param paso: Estado de la lista a registrar.
        """
        self._pasos.append(paso)


class GestorDatos:
    """
    Clase encargada de la gestión y generación de datos para el explorador de algoritmos.
    """
    @staticmethod
    def generar_lista_aleatoria(tamano: int, limite_inferior: int = 0, limite_superior: int = 100) -> List[int]:
        """
        Genera una lista de números enteros aleatorios.
        
        :param tamano: Cantidad de elementos de la lista.
        :param limite_inferior: Valor mínimo del rango (inclusivo).
        :param limite_superior: Valor máximo del rango (inclusivo).
        :return: Lista de enteros aleatorios.
        :raises ValueError: Si los parámetros proporcionados no son válidos.
        """
        if tamano < 0:
            raise ValueError("El tamaño de la lista no puede ser negativo.")
        if limite_inferior > limite_superior:
            raise ValueError("El límite inferior no puede ser mayor que el límite superior.")
            
        return [random.randint(limite_inferior, limite_superior) for _ in range(tamano)]


# =====================================================================
# Ejemplo de uso e implementación concreta para probar la estructura
# =====================================================================
class BubbleSort(Algoritmo):
    """
    Implementación del algoritmo de ordenamiento BubbleSort.
    """
    def ordenar(self, lista: List[int]) -> List[int]:
        n = len(lista)
        # Trabajamos sobre una copia para no mutar la lista original
        lista_ordenada = lista.copy()
        
        # Guardamos el estado inicial
        self.registrar_paso(lista_ordenada.copy())
        
        for i in range(n):
            intercambiado = False
            for j in range(0, n - i - 1):
                if lista_ordenada[j] > lista_ordenada[j + 1]:
                    # Intercambio manual
                    lista_ordenada[j], lista_ordenada[j + 1] = lista_ordenada[j + 1], lista_ordenada[j]
                    intercambiado = True
                    # Guardar una copia del estado actual de la lista
                    self.registrar_paso(lista_ordenada.copy())
            
            # Optimización: si no hubo intercambios en la pasada, ya está ordenado
            if not intercambiado:
                break
                
        return lista_ordenada


if __name__ == '__main__':
    # 1. Generar datos usando el GestorDatos
    try:
        lista_desordenada = GestorDatos.generar_lista_aleatoria(tamano=5, limite_inferior=1, limite_superior=50)
        print(f"Lista original: {lista_desordenada}\n")
        
        # 2. Instanciar un algoritmo
        algoritmo = BubbleSort()
        
        # 3. Ordenar la lista
        lista_ordenada = algoritmo.ordenar(lista_desordenada)
        
        # 4. Mostrar resultados
        print(f"Lista ordenada: {lista_ordenada}\n")
        print("Pasos del algoritmo (estados de la lista):")
        for paso in algoritmo.obtener_pasos():
            print(f"- {paso}")
            
    except ValueError as e:
        print(f"Error de validación: {e}")

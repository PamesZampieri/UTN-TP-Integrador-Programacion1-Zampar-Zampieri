# Programación1
# TP-INTEGRADOR: Algoritmos de Búsqueda y Ordenamiento en Python
# Integrantes: Pamela Zampieri y Facundo Zampar
# Implementación de búsqueda y ordenamiento en una lista de cursos online generados automáticamente

from faker import Faker  # Importa la librería Faker para generar datos falsos
import random  # Importa random para generar números aleatorios
import time  # Importa time para medir tiempos de ejecución
import unicodedata # Importa el módulo estándar unicodedata de Python, que permite trabajar con caracteres Unicode

# Crea una instancia de Faker configurada para español de España
fake = Faker('es_ES')

# Métodos de búsqueda
# Búsqueda binaria (lista previamente ordenada por la función clave)
# Devuelve el índice de una coincidencia (no necesariamente la primera si hay varias)
def busqueda_binaria(items, objetivo, funcion_clave):
    izquierda = 0
    derecha = len(items) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        valor_medio = funcion_clave(items[medio])
        if valor_medio == objetivo:
            return medio  # devuelve el índice
        elif valor_medio < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return None  # no encontrado

# Búsqueda lineal (lista no ordenada)
# Devuelve el índice de la primera coincidencia encontrada
def busqueda_lineal(items, objetivo, funcion_clave):
    for i in range(len(items)):
        if funcion_clave(items[i]) == objetivo:
            return i
    return None

# Métodos de ordenamiento
# Bubble Sort (Ordenamiento burbuja)
def bubble_sort(lista, funcion_clave):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if funcion_clave(lista[j]) > funcion_clave(lista[j + 1]):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]

# QuickSort (Ordenamiento rápido)
def quick_sort(lista, funcion_clave):
    if len(lista) <= 1:
        return lista
    else:
        pivote = lista[0]
        menores = [x for x in lista[1:] if funcion_clave(x) <= funcion_clave(pivote)]
        mayores = [x for x in lista[1:] if funcion_clave(x) > funcion_clave(pivote)]
        return quick_sort(menores, funcion_clave) + [pivote] + quick_sort(mayores, funcion_clave)

# Diccionario con temas y nombres posibles de cursos relacionados
temas_cursos = {
    "Programación": ["Python", "Java", "C++", "Desarrollo Web", "Algoritmos"],
    "Arte": ["Pintura al Óleo", "Escultura", "Historia del Arte", "Fotografía"],
    "Historia": ["Historia Universal", "Historia de América", "Historia Medieval"],
    "Diseño": ["Diseño Gráfico", "Diseño UX", "Diseño Industrial"],
    "Negocios": ["Marketing Digital", "Gestión Empresarial", "Finanzas"],
    "Idiomas": ["Inglés", "Francés", "Alemán", "Español para Extranjeros"],
    "Matemáticas": ["Álgebra", "Cálculo", "Estadística", "Matemáticas Discretas"]
}

# Niveles de dificultad
niveles = ["Básico", "Intermedio", "Avanzado"]

class Curso:
    def __init__(self, nombre, profesor, tema, duracion, calificacion):
        self.nombre = nombre
        self.profesor = profesor
        self.tema = tema
        self.duracion = duracion
        self.calificacion = calificacion

    def __str__(self):
        return f"{self.nombre} | {self.profesor} | {self.tema} | {self.duracion} hs | {self.calificacion:.1f}"

# Método para generar cursos
def generar_cursos(cantidad):
    lista = []
    for _ in range(cantidad):
        tema = random.choice(list(temas_cursos.keys()))
        nombre_base = random.choice(temas_cursos[tema])
        nombre = f"{nombre_base} {random.choice(niveles)}"
        profesor = fake.name()
        duracion = random.randint(5, 50)
        calificacion = round(random.uniform(1.0, 5.0), 1)
        lista.append(Curso(nombre, profesor, tema, duracion, calificacion))
    return lista

# Método para obtener el campo a buscar
def obtener_funcion_clave_campo(campo):
    campo = campo.lower()
    if campo == "nombre":
        return lambda c: c.nombre
    elif campo == "profesor":
        return lambda c: c.profesor
    elif campo == "tema":
        return lambda c: c.tema
    elif campo == "duracion":
        return lambda c: c.duracion
    elif campo == "calificacion":
        return lambda c: c.calificacion
    else:
        return None

# Mostrar los cursos
def mostrar_cursos(lista):
    for curso in lista:
        print(curso)

# Si son más de 50 cursos(umbral elegido) se muestra un resumen
def mostrar_resumen_cursos(lista):
    print("... Primeros 5 cursos ...")
    for curso in lista[:5]:
        print(curso)
    print("... Últimos 5 cursos ...")
    for curso in lista[-5:]:
        print(curso)

# Inicio
while True:
    try:
        print("------------------------------------------")
        cantidad = int(input("¡Bienvenid@! ¿Cuántos cursos desea generar? "))
        if cantidad > 0:
            break
        else:
            print("Ingrese un número mayor que cero.")
    except ValueError:
        print("Por favor, ingrese un número válido.")

#  Convierte el texto a minúsculas y elimina acentos para facilitar comparaciones y ordenamientos.
def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto

cursos = generar_cursos(cantidad)
criterio_ordenamiento = ""

print("\n--- CURSOS GENERADOS (DESORDENADOS) ---")
mostrar_resumen_cursos(cursos) if len(cursos) > 50 else mostrar_cursos(cursos)

while True:
    print("\n--- MENÚ ---")
    print("1. Ordenar cursos")
    print("2. Buscar curso")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        print("\n--- Ordenar cursos ---")
        campo = input("Ordenar por (nombre/profesor/tema/duracion/calificacion): ").strip().lower()

        funcion_clave_original = obtener_funcion_clave_campo(campo)
        if funcion_clave_original is None:
            print("Campo no válido. Intente de nuevo.")
            continue

        # Normalización si corresponde
        if campo in ["nombre", "profesor", "tema"]:
            funcion_clave = lambda c: normalizar_texto(funcion_clave_original(c))
        else:
            funcion_clave = funcion_clave_original

        lista_bubble = cursos.copy()
        inicio = time.time()
        bubble_sort(lista_bubble, funcion_clave)
        tiempo_bubble = time.time() - inicio

        lista_quick = cursos.copy()
        inicio = time.time()
        lista_quick_ordenada = quick_sort(lista_quick, funcion_clave)
        tiempo_quick = time.time() - inicio

        print(f"\nLista ordenada con Bubble Sort por {campo} en {tiempo_bubble:.6f} segundos:\n")
        mostrar_resumen_cursos(lista_bubble) if len(lista_bubble) > 50 else mostrar_cursos(lista_bubble)

        print(f"\nLista ordenada con Quick Sort por {campo} en {tiempo_quick:.6f} segundos:\n")
        mostrar_resumen_cursos(lista_quick_ordenada) if len(lista_quick_ordenada) > 50 else mostrar_cursos(lista_quick_ordenada)

        cursos = lista_bubble  # Ahora cursos está ordenado por este campo
        criterio_ordenamiento = campo

    elif opcion == "2":
        print("\n--- Buscar curso ---")
        campo = input("Buscar por (nombre/profesor/tema): ").strip().lower()
        if campo not in ["nombre", "profesor", "tema"]:
            print("Campo no válido.")
            continue

        valor = input(f"Ingrese el valor a buscar en {campo}: ").strip()
        funcion_clave_original = obtener_funcion_clave_campo(campo)

        # Normalización
        funcion_clave = lambda c: normalizar_texto(funcion_clave_original(c))
        valor = normalizar_texto(valor)

        # Búsqueda lineal
        inicio = time.time()
        indice_lineal = busqueda_lineal(cursos, valor, funcion_clave)
        tiempo_lineal = time.time() - inicio

        if criterio_ordenamiento == campo:
            # Búsqueda binaria solo si la lista está ordenada por el campo
            inicio = time.time()
            indice_binaria = busqueda_binaria(cursos, valor, funcion_clave)
            tiempo_binaria = time.time() - inicio
        else:
            indice_binaria = None
            tiempo_binaria = None

        # Mostrar resultados
        if indice_lineal is not None:
            print(f"\nResultado búsqueda lineal: {cursos[indice_lineal]} (en {tiempo_lineal:.6f} segundos)")
        else:
            print(f"No se encontró curso con búsqueda lineal (en {tiempo_lineal:.6f} segundos)")

        if tiempo_binaria is not None:
            if indice_binaria is not None:
                print(f"Resultado búsqueda binaria: {cursos[indice_binaria]} (en {tiempo_binaria:.6f} segundos)")
            else:
                print(f"No se encontró curso con búsqueda binaria (en {tiempo_binaria:.6f} segundos)")

    elif opcion == "3":
        print("Saliendo del programa.")
        break

    else:
        print("Opción inválida. Intente nuevamente.")

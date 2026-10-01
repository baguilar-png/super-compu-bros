"""
Persistencia de datos del juego (todo en archivos .txt al lado del juego).

    puntos.txt      -> puntos acumulados (un numero)
    personajes.txt  -> nombre del personaje elegido
    bebidas.txt     -> una bebida por linea, las que ya se recogieron
                       (asi no se pueden farmear puntos ni vidas)

Todo sobrevive a: ESC, cerrar la ventana y cerrar el programa.
Todo se borra junto SOLO cuando el jugador pierde todas las vidas
(ver reiniciar_progreso).
"""

import os

CARPETA = os.path.dirname(os.path.abspath(__file__))

RUTA_PUNTOS = os.path.join(CARPETA, "puntos.txt")
RUTA_PERSONAJE = os.path.join(CARPETA, "personajes.txt")
RUTA_BEBIDAS = os.path.join(CARPETA, "bebidas.txt")


# ==========================================================
# AYUDAS
# ==========================================================

def _leer(ruta):
    """Texto del archivo, o None si no existe / no se puede leer."""

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()

    except OSError:
        return None


def _escribir(ruta, texto):

    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(texto)

    except OSError:
        pass


def _borrar(ruta):

    try:
        os.remove(ruta)

    except OSError:
        pass


# ==========================================================
# PUNTOS
# ==========================================================

def cargar_puntos():
    """Puntos guardados (0 si no hay archivo o esta roto)."""

    texto = _leer(RUTA_PUNTOS)

    try:
        return max(0, int(texto.strip()))

    except (AttributeError, ValueError):
        return 0


def guardar_puntos(puntos):

    _escribir(RUTA_PUNTOS, str(int(puntos)) + "\n")


# ==========================================================
# PERSONAJE ELEGIDO
# ==========================================================

def cargar_personaje():
    """Nombre del personaje guardado, o None si hay que elegir."""

    texto = _leer(RUTA_PERSONAJE)

    if texto is None:
        return None

    nombre = texto.strip()

    return nombre or None


def guardar_personaje(nombre):

    _escribir(RUTA_PERSONAJE, str(nombre) + "\n")


# ==========================================================
# BEBIDAS YA RECOGIDAS
# ==========================================================

def cargar_bebidas():
    """Conjunto con los ids de las bebidas ya recogidas."""

    texto = _leer(RUTA_BEBIDAS)

    if texto is None:
        return set()

    return {linea.strip() for linea in texto.splitlines() if linea.strip()}


def guardar_bebida(id_bebida):
    """Agrega una bebida al txt (se guarda en el momento de recogerla)."""

    bebidas = cargar_bebidas()

    bebidas.add(id_bebida)

    _escribir(RUTA_BEBIDAS, "\n".join(sorted(bebidas)) + "\n")


# ==========================================================
# GAME OVER
# ==========================================================

def reiniciar_progreso():
    """
    Se pierden todas las vidas: se borran puntos, personaje y bebidas
    recogidas. La proxima partida empieza de cero y hay que elegir
    personaje de nuevo.
    """

    _borrar(RUTA_PUNTOS)
    _borrar(RUTA_PERSONAJE)
    _borrar(RUTA_BEBIDAS)

"""
Persistencia de datos del juego (todo en archivos .txt al lado del juego).

    puntos.txt      -> puntos acumulados (un numero)
    personajes.txt  -> nombre del personaje elegido
    bebidas.txt     -> una bebida por linea, las que ya se recogieron
                       (asi no se pueden farmear puntos ni vidas)
    nivel.txt       -> progreso en el mapa de Buenos Aires: niveles
                       completados, donde esta parado el personaje y por
                       que puntitos del camino ya paso (los negros)

Todo sobrevive a: ESC, cerrar la ventana y cerrar el programa.
Todo se borra junto SOLO cuando el jugador pierde todas las vidas
(ver reiniciar_progreso).
"""

import os

CARPETA = os.path.dirname(os.path.abspath(__file__))

RUTA_PUNTOS = os.path.join(CARPETA, "puntos.txt")
RUTA_PERSONAJE = os.path.join(CARPETA, "personajes.txt")
RUTA_BEBIDAS = os.path.join(CARPETA, "bebidas.txt")
RUTA_NIVEL = os.path.join(CARPETA, "nivel.txt")

# Cantidad de niveles del mapa (la Boca -> ... -> la Boca)
TOTAL_NIVELES = 15


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
# PROGRESO EN EL MAPA
# ==========================================================

def cargar_mapa():
    """
    (niveles_completados, x, y, tocados) guardados.

    x, y     -> donde quedo parado el personaje en el mapa (coordenadas de
                la imagen original); None si todavia no hay posicion
    tocados  -> puntitos del camino actual por los que ya paso (negros)
    Si no hay archivo (o esta roto) se empieza de cero.
    """

    texto = _leer(RUTA_NIVEL)

    try:
        lineas = texto.splitlines()

        completados, x, y = lineas[0].split()[:3]

        completados = max(0, min(TOTAL_NIVELES, int(completados)))

        x = None if x == "-" else float(x)
        y = None if y == "-" else float(y)

        tocados = []

        if len(lineas) > 1:

            tocados = [
                int(n) for n in lineas[1].split(",") if n.strip()
            ]

        return completados, x, y, tocados

    except (AttributeError, IndexError, ValueError):
        return 0, None, None, []


def guardar_mapa(completados, x, y, tocados):

    _escribir(
        RUTA_NIVEL,
        "%d %s %s\n%s\n" % (
            completados,
            "-" if x is None else "%.1f" % x,
            "-" if y is None else "%.1f" % y,
            ",".join(str(n) for n in sorted(tocados))
        )
    )


def completar_nivel(nivel):
    """
    Se llego a la meta del nivel (1 a 15). Se suma a los completados, el
    personaje queda donde estaba y el camino al siguiente arranca limpio.
    """

    completados, x, y, _ = cargar_mapa()

    if nivel > completados:

        guardar_mapa(min(nivel, TOTAL_NIVELES), x, y, [])


def nueva_vuelta():
    """
    Se terminaron los 15 niveles: el mapa y las bebidas se borran para
    poder volver a jugar desde la Boca (puntos y personaje se conservan).
    """

    _borrar(RUTA_NIVEL)
    _borrar(RUTA_BEBIDAS)


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
    _borrar(RUTA_NIVEL)

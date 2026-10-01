"""
Fuente pixel art para Super Compu Bros.

No hace falta ningun archivo de fuente (.ttf): las letras estan dibujadas
pixel por pixel aca mismo. Se usa igual que una fuente de pygame:

    fuente = FuentePixel(3)                  # 3 = cada pixel mide 3x3
    imagen = fuente.render("HOLA", True, (255, 255, 255))
    pantalla.blit(imagen, (10, 10))

La "escala" es el tamano de cada pixel de la letra en pantalla.
Como los pixeles son cuadrados y grandes, siempre se ven nitidos.

Soporta: A-Z, a-z, 0-9, simbolos comunes, vocales con tilde, n con tilde,
u con dieresis, y los signos de apertura de pregunta y exclamacion.
"""

import pygame


# ==========================================================
# DISENO DE LAS LETRAS
# ==========================================================
# Cada letra se dibuja en una grilla de 5 columnas de ancho.
#   '#' = pixel encendido      '.' = pixel apagado
# Junto a las filas va el "desfase" vertical: 0 es la linea de arriba
# de una mayuscula. Las minusculas bajas empiezan en 2 y las que tienen
# cola (g, j, p, q, y) siguen hacia abajo.

ALTO_MAYUS = 7          # filas de una mayuscula
FILAS_ARRIBA = 3        # espacio para las tildes (2 filas + 1 de aire)
FILAS_ABAJO = 3         # espacio para las colas de g, j, p, q, y
ALTO_CELDA = FILAS_ARRIBA + ALTO_MAYUS + FILAS_ABAJO   # 13 filas

ANCHO_ESPACIO = 3       # ancho (en pixeles) del espacio entre palabras
SEPARACION = 1          # pixeles vacios entre una letra y la siguiente


def _g(desfase, *filas):
    return (desfase, list(filas))


LETRAS = {
    # ---------------- MAYUSCULAS ----------------
    "A": _g(0, ".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": _g(0, "####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": _g(0, ".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."),
    "D": _g(0, "###..", "#..#.", "#...#", "#...#", "#...#", "#..#.", "###.."),
    "E": _g(0, "#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": _g(0, "#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": _g(0, ".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"),
    "H": _g(0, "#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": _g(0, ".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": _g(0, "..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": _g(0, "#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": _g(0, "#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": _g(0, "#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": _g(0, "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": _g(0, ".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": _g(0, "####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": _g(0, ".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": _g(0, "####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": _g(0, ".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": _g(0, "#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": _g(0, "#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": _g(0, "#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": _g(0, "#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": _g(0, "#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": _g(0, "#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": _g(0, "#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),

    # ---------------- NUMEROS ----------------
    "0": _g(0, ".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": _g(0, "..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": _g(0, ".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": _g(0, "#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."),
    "4": _g(0, "...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": _g(0, "#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": _g(0, "..##.", ".#...", "#....", "####.", "#...#", "#...#", ".###."),
    "7": _g(0, "#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."),
    "8": _g(0, ".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": _g(0, ".###.", "#...#", "#...#", ".####", "....#", "...#.", ".##.."),

    # ---------------- MINUSCULAS ----------------
    "a": _g(2, ".###.", "....#", ".####", "#...#", ".####"),
    "b": _g(0, "#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
    "c": _g(2, ".###.", "#...#", "#....", "#...#", ".###."),
    "d": _g(0, "....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"),
    "e": _g(2, ".###.", "#...#", "#####", "#....", ".###."),
    "f": _g(0, "..##.", ".#..#", ".#...", "###..", ".#...", ".#...", ".#..."),
    "g": _g(2, ".####", "#...#", "#...#", "#...#", ".####", "....#", ".###."),
    "h": _g(0, "#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "i": _g(0, "..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."),
    "j": _g(0, "...#.", ".....", "..##.", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "k": _g(0, "#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."),
    "l": _g(0, ".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "m": _g(2, "##.#.", "#.#.#", "#.#.#", "#.#.#", "#...#"),
    "n": _g(2, "####.", "#...#", "#...#", "#...#", "#...#"),
    "o": _g(2, ".###.", "#...#", "#...#", "#...#", ".###."),
    "p": _g(2, "####.", "#...#", "#...#", "#...#", "####.", "#....", "#...."),
    "q": _g(2, ".####", "#...#", "#...#", "#...#", ".####", "....#", "....#"),
    "r": _g(2, "#.##.", "##..#", "#....", "#....", "#...."),
    "s": _g(2, ".####", "#....", ".###.", "....#", "####."),
    "t": _g(0, ".#...", ".#...", "###..", ".#...", ".#...", ".#..#", "..##."),
    "u": _g(2, "#...#", "#...#", "#...#", "#..##", ".##.#"),
    "v": _g(2, "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "w": _g(2, "#...#", "#...#", "#.#.#", "#.#.#", ".#.#."),
    "x": _g(2, "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
    "y": _g(2, "#...#", "#...#", "#...#", ".####", "....#", "#...#", ".###."),
    "z": _g(2, "#####", "...#.", "..#..", ".#...", "#####"),

    # ---------------- SIMBOLOS ----------------
    "!": _g(0, "#", "#", "#", "#", "#", ".", "#"),
    '"': _g(0, "#.#", "#.#"),
    "#": _g(0, ".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
    "$": _g(0, "..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "%": _g(0, "##..#", "##..#", "...#.", "..#..", ".#...", "#..##", "#..##"),
    "&": _g(0, ".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "'": _g(0, "#", "#"),
    "(": _g(0, "..#", ".#.", "#..", "#..", "#..", ".#.", "..#"),
    ")": _g(0, "#..", ".#.", "..#", "..#", "..#", ".#.", "#.."),
    "*": _g(1, "..#..", "#.#.#", ".###.", "#.#.#", "..#.."),
    "+": _g(1, "..#..", "..#..", "#####", "..#..", "..#.."),
    ",": _g(5, ".#", ".#", "#."),
    "-": _g(3, "####"),
    ".": _g(6, "#"),
    "/": _g(0, "....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    ":": _g(0, ".", ".", "#", ".", ".", "#", "."),
    ";": _g(0, "..", "..", ".#", "..", "..", ".#", ".#", "#."),
    "<": _g(0, "...#.", "..#..", ".#...", "#....", ".#...", "..#..", "...#."),
    "=": _g(2, "#####", ".....", "#####"),
    ">": _g(0, ".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."),
    "?": _g(0, ".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "@": _g(0, ".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".###."),
    "[": _g(0, "###", "#..", "#..", "#..", "#..", "#..", "###"),
    "\\": _g(0, "#....", "#....", ".#...", "..#..", "...#.", "....#", "....#"),
    "]": _g(0, "###", "..#", "..#", "..#", "..#", "..#", "###"),
    "^": _g(0, "..#..", ".#.#.", "#...#"),
    "_": _g(7, "#####"),
    "`": _g(0, "#.", ".#"),
    "{": _g(0, "..##", ".#..", ".#..", "#...", ".#..", ".#..", "..##"),
    "|": _g(0, "#", "#", "#", "#", "#", "#", "#"),
    "}": _g(0, "##..", "..#.", "..#.", "...#", "..#.", "..#.", "##.."),
    "~": _g(3, ".##.#", "#.##."),

    # Signos de apertura del espanol
    "\u00a1": _g(0, "#", ".", "#", "#", "#", "#", "#"),                      # ¡
    "\u00bf": _g(0, "..#..", ".....", "..#..", ".#...", "#....", "#...#", ".###."),  # ¿
}


# ==========================================================
# LETRAS CON TILDE
# ==========================================================
# Se arman automaticamente: letra base + adorno.
# Cada adorno son 2 filas (en la grilla de 5 columnas).

ADORNOS = {
    "acento": ("...#.", "..#.."),
    "dieresis": (".....", ".#.#."),
    "tilde": (".##.#", "#.##."),
}

# caracter -> (letra base, adorno)
CON_TILDE = {
    "\u00e1": ("a", "acento"), "\u00e9": ("e", "acento"),   # á é
    "\u00f3": ("o", "acento"), "\u00fa": ("u", "acento"),   # ó ú
    "\u00c1": ("A", "acento"), "\u00c9": ("E", "acento"),   # Á É
    "\u00cd": ("I", "acento"), "\u00d3": ("O", "acento"),   # Í Ó
    "\u00da": ("U", "acento"),                              # Ú
    "\u00f1": ("n", "tilde"), "\u00d1": ("N", "tilde"),     # ñ Ñ
    "\u00fc": ("u", "dieresis"), "\u00dc": ("U", "dieresis"),  # ü Ü
    "\u00ed": ("i", "acento"),                              # í (sin el puntito)
}


def _armar_glifo_con_tilde(base, adorno):
    """Devuelve (fila_inicial_en_celda, filas) de una letra con tilde."""
    desfase, filas = LETRAS[base]
    filas = list(filas)
    es_mayuscula = base.isupper()

    if base == "i":
        # La i minuscula ya trae su puntito: se lo saca y se pone la tilde.
        filas[0] = "....."
        filas[1] = "....."

    # Fila de la celda donde va la tilde:
    #   mayusculas -> filas 0-1 (encima de la mayuscula, que empieza en 3)
    #   minusculas -> filas 2-3 (dejando 1 de aire antes de la x-height en 5)
    fila_adorno = 0 if es_mayuscula else 2
    fila_letra = FILAS_ARRIBA + desfase

    # Para la "i" la parte de abajo arranca en la fila 2 del glifo
    if base == "i":
        filas = filas[2:]
        fila_letra += 2

    alto_total = max(fila_letra + len(filas), fila_adorno + 2)
    lienzo = ["....."] * alto_total
    for k, fila in enumerate(ADORNOS[adorno]):
        lienzo[fila_adorno + k] = fila
    for k, fila in enumerate(filas):
        lienzo[fila_letra + k] = fila
    return 0, lienzo


def _glifo_en_celda(caracter):
    """
    Devuelve las filas del caracter ya ubicadas dentro de la celda
    (lista de strings, una por fila, empezando en la fila 0 de la celda),
    recortadas para que cada letra ocupe solo el ancho que necesita.
    """
    if caracter in CON_TILDE:
        base, adorno = CON_TILDE[caracter]
        _, filas = _armar_glifo_con_tilde(base, adorno)
        inicio = 0
    else:
        if caracter not in LETRAS:
            caracter = "?"
        desfase, filas = LETRAS[caracter]
        inicio = FILAS_ARRIBA + desfase

    ancho_fila = max(len(f) for f in filas)
    celda = ["." * ancho_fila] * ALTO_CELDA
    for k, fila in enumerate(filas):
        if inicio + k < ALTO_CELDA:
            celda[inicio + k] = fila.ljust(ancho_fila, ".")

    # Recortar columnas vacias a izquierda y derecha
    columnas = [c for c in range(ancho_fila) if any(f[c] == "#" for f in celda)]
    if not columnas:
        return ["." * ANCHO_ESPACIO] * ALTO_CELDA
    c0, c1 = columnas[0], columnas[-1]
    return [f[c0:c1 + 1] for f in celda]


_CACHE_GLIFOS = {}


def glifo(caracter):
    if caracter not in _CACHE_GLIFOS:
        if caracter == " ":
            _CACHE_GLIFOS[caracter] = ["." * ANCHO_ESPACIO] * ALTO_CELDA
        else:
            _CACHE_GLIFOS[caracter] = _glifo_en_celda(caracter)
    return _CACHE_GLIFOS[caracter]


def mapa_de_bits(texto):
    """
    Convierte un texto en una matriz de ALTO_CELDA filas de '#' y '.'.
    Es Python puro (no usa pygame), asi que se puede probar aparte.
    """
    filas = [""] * ALTO_CELDA
    primero = True
    for caracter in texto:
        g = glifo(caracter)
        if not primero:
            for i in range(ALTO_CELDA):
                filas[i] += "." * SEPARACION
        for i in range(ALTO_CELDA):
            filas[i] += g[i]
        primero = False
    return filas


# ==========================================================
# LA FUENTE (misma interfaz basica que pygame.font.Font)
# ==========================================================

class FuentePixel:
    """
    escala: tamano en pantalla de cada pixel de la letra.
            2 = chica, 3 = mediana, 5 o 6 = titulos.
    """

    def __init__(self, escala=3):
        self.escala = max(1, int(escala))
        self._cache = {}

    # --- medidas -------------------------------------------------

    def size(self, texto):
        filas = mapa_de_bits(texto)
        return (len(filas[0]) * self.escala, ALTO_CELDA * self.escala)

    def get_height(self):
        return ALTO_CELDA * self.escala

    def get_linesize(self):
        return self.get_height()

    # --- dibujo --------------------------------------------------

    def render(self, texto, antialias=True, color=(255, 255, 255), fondo=None):
        """
        Devuelve una Surface con el texto. 'antialias' se ignora: el pixel
        art nunca se suaviza.
        """
        color = tuple(color)[:3]
        clave = (texto, color, fondo)
        if clave in self._cache:
            return self._cache[clave]

        filas = mapa_de_bits(texto)
        ancho = max(1, len(filas[0]))

        chica = pygame.Surface((ancho, ALTO_CELDA), pygame.SRCALPHA)
        if fondo is not None:
            chica.fill(tuple(fondo))
        else:
            chica.fill((0, 0, 0, 0))

        for y, fila in enumerate(filas):
            for x, celda in enumerate(fila):
                if celda == "#":
                    chica.set_at((x, y), color + (255,))

        # scale() copia pixel por pixel (sin suavizar): queda pixel art.
        imagen = pygame.transform.scale(
            chica,
            (ancho * self.escala, ALTO_CELDA * self.escala)
        )

        if len(self._cache) > 300:
            self._cache.clear()
        self._cache[clave] = imagen
        return imagen

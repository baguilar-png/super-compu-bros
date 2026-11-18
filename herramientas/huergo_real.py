"""
El Instituto Industrial Luis A. Huergo "de verdad": lo que se sabe del edificio
real (la entrada de Peru 759, San Telmo) dibujado en pixel art.

La entrada (nivel 2: se arranca justo en la puerta) esta armada a partir de una
foto, solo la estructura:

    vidriera con un afiche azul | granito negro con "INSTITUTO INDUSTRIAL" |
    el portón de hierro de rombos con una plaquita blanca y el escalon amarillo |
    granito negro con "LUIS A. HUERGO" | vidriera con estantes

    arriba, una cornisa de hormigon gris y la fachada de piedra beige con
    sus ventanitas con rejas; abajo, la vereda de baldosas ocres con la banda
    amarilla del cordon y baldosas podotactiles grises.

Tambien esta el interior del nivel 1 (un colegio tecnico, plano y sin
enemigos): ver `modulos_planos`.

Todo se mide en pixeles de dibujo (1 = 3 de pantalla). Cada pieza se dibuja
sobre un `Lienzo` (ver pixelart.py).
"""

import random

from pixelart import Lienzo, rgb, luz, sombra, mezcla, BLANCO

# ----------------------------------------------------------
# Letras chicas (3 x 5) para lo grabado en el granito
# ----------------------------------------------------------

MICRO = {
    "A": (".#.", "#.#", "###", "#.#", "#.#"),
    "B": ("##.", "#.#", "##.", "#.#", "##."),
    "C": (".##", "#..", "#..", "#..", ".##"),
    "D": ("##.", "#.#", "#.#", "#.#", "##."),
    "E": ("###", "#..", "##.", "#..", "###"),
    "F": ("###", "#..", "##.", "#..", "#.."),
    "G": (".##", "#..", "#.#", "#.#", ".##"),
    "H": ("#.#", "#.#", "###", "#.#", "#.#"),
    "I": ("###", ".#.", ".#.", ".#.", "###"),
    "J": ("..#", "..#", "..#", "#.#", ".#."),
    "K": ("#.#", "#.#", "##.", "#.#", "#.#"),
    "L": ("#..", "#..", "#..", "#..", "###"),
    "M": ("#...#", "##.##", "#.#.#", "#...#", "#...#"),
    "N": ("#..#", "##.#", "#.##", "#..#", "#..#"),
    "O": (".#.", "#.#", "#.#", "#.#", ".#."),
    "P": ("##.", "#.#", "##.", "#..", "#.."),
    "R": ("##.", "#.#", "##.", "#.#", "#.#"),
    "S": (".##", "#..", ".#.", "..#", "##."),
    "T": ("###", ".#.", ".#.", ".#.", ".#."),
    "U": ("#.#", "#.#", "#.#", "#.#", "###"),
    "V": ("#.#", "#.#", "#.#", "#.#", ".#."),
    "X": ("#.#", "#.#", ".#.", "#.#", "#.#"),
    "Y": ("#.#", "#.#", ".#.", ".#.", ".#."),
    "Z": ("###", "..#", ".#.", "#..", "###"),
    "0": ("###", "#.#", "#.#", "#.#", "###"),
    "1": (".#.", "##.", ".#.", ".#.", "###"),
    "2": ("##.", "..#", ".#.", "#..", "###"),
    "3": ("##.", "..#", ".#.", "..#", "##."),
    "4": ("#.#", "#.#", "###", "..#", "..#"),
    "5": ("###", "#..", "##.", "..#", "##."),
    "6": (".##", "#..", "###", "#.#", "###"),
    "7": ("###", "..#", ".#.", ".#.", ".#."),
    "8": ("###", "#.#", "###", "#.#", "###"),
    "9": ("###", "#.#", "###", "..#", "##."),
    ".": (".", ".", ".", ".", "#"),
    "-": ("...", "...", "###", "...", "..."),
    "/": ("..#", "..#", ".#.", "#..", "#.."),
    " ": ("..", "..", "..", "..", ".."),
}


def micro_ancho(texto):
    """Ancho en pixeles de un texto de letras chicas (1 pixel entre letras)."""

    return sum(len(MICRO.get(ch, MICRO[" "])[0]) for ch in texto) + len(texto) - 1


def micro_texto(l, x, y, texto, color):
    """Dibuja texto de letras 3 x 5 con la esquina de arriba en (x, y)."""

    for ch in texto:

        glifo = MICRO.get(ch, MICRO[" "])

        for j, fila in enumerate(glifo):

            for i, p in enumerate(fila):

                if p == "#":

                    l.px(x + i, y + j, color)

        x += len(glifo[0]) + 1

    return x


def micro_centrado(l, cx, y, texto, color):
    """Lo mismo, centrado en cx."""

    micro_texto(l, cx - micro_ancho(texto) // 2, y, texto, color)


# ----------------------------------------------------------
# Materiales
# ----------------------------------------------------------

PIEDRA_BEIGE = rgb("#cdb994")
HORMIGON = rgb("#a9a8a3")
GRANITO_NEGRO = rgb("#1a1a1f")
HIERRO = rgb("#16161a")
GRIS_ALUM = rgb("#6c6f75")
AMARILLO_UMBRAL = rgb("#e6b92a")


def piedra_moteada(l, x0, y0, x1, y1, r, base=PIEDRA_BEIGE, densidad=0.16):
    """Piedra beige con motitas (como la de la fachada de la foto)."""

    l.rect(x0, y0, x1, y1, base)

    tonos = (
        sombra(base, 0.84), sombra(base, 0.92), luz(base, 0.14),
        rgb("#8d7a5a"), luz(base, 0.26)
    )

    for y in range(y0, y1 + 1):

        for x in range(x0, x1 + 1):

            if r.random() < densidad:

                l.px(x, y, r.choice(tonos))


def granito_negro(l, x0, y0, x1, y1, r):
    """Panel de granito negro pulido: motitas, un reflejo y un filete."""

    base = GRANITO_NEGRO

    ancho = x1 - x0

    for x in range(x0, x1 + 1):

        t = (x - x0) / max(1, ancho)

        k = 1.0 + 0.9 * max(0.0, 1.0 - abs(t - 0.2) / 0.16)

        l.rect(
            x, y0, x, y1,
            tuple(min(255, int(v * k)) for v in base)
        )

    for _ in range(int((x1 - x0) * (y1 - y0) * 0.10)):

        l.px(
            r.randint(x0, x1), r.randint(y0, y1),
            r.choice((
                rgb("#2e2e35"), rgb("#3d3d45"), rgb("#0d0d11"),
                rgb("#5a5a63"), rgb("#2a2a30")
            ))
        )

    # marco de piedra gris y un filete oscuro adentro
    l.marco(x0, y0, x1, y1, rgb("#77757a"))
    l.marco(x0 + 1, y0 + 1, x1 - 1, y1 - 1, rgb("#08080b"))


def grabado(l, cx, y, texto, color=None):
    """Texto grabado en el granito (letras chicas, claras, centradas en cx)."""

    micro_centrado(l, cx, y, texto, color or rgb("#c4c1b6"))


# ----------------------------------------------------------
# El portón de hierro de rombos
# ----------------------------------------------------------

def hall_oscuro(l, x0, y0, x1, y1):
    """Lo que se ve detras del porton: el hall, oscuro arriba y tibio abajo."""

    for y in range(y0, y1 + 1):

        t = (y - y0) / max(1, y1 - y0)

        l.rect(x0, y, x1, y, mezcla(rgb("#6a5238"), rgb("#c79c62"), t ** 1.2))


def reja_rombos(l, x0, y0, x1, y1, abierta=False):
    """
    Porton de dos hojas de hierro forjado con rombos, en el hueco (x0, y0) a
    (x1, y1). Cerrado: las dos hojas, con la plaquita blanca en el medio.
    Abierto: las dos hojas plegadas contra las jambas (el hall se ve entero).
    """

    ancho = x1 - x0 + 1
    alto = y1 - y0 + 1

    mitad = x0 + ancho // 2

    hierro = HIERRO

    def hoja(a, z):

        for j in range(alto):

            for i in range(z - a + 1):

                if (i + j) % 5 == 0 or (i - j) % 5 == 0:

                    l.px(a + i, y0 + j, hierro)

        # marco de la hoja: travesanos arriba, en el medio y abajo
        l.rect(a, y0, z, y0 + 1, hierro)
        l.rect(a, y1 - 1, z, y1, hierro)
        l.rect(a, y0 + alto // 2, z, y0 + alto // 2, hierro)
        l.rect(a, y0, a, y1, hierro)
        l.rect(z, y0, z, y1, hierro)

    if not abierta:

        hoja(x0, mitad - 1)
        hoja(mitad, x1)

        # la plaquita blanca en el medio
        py = y0 + alto // 2 - 3

        l.rect(mitad - 2, py, mitad + 1, py + 6, rgb("#f1efe6"))
        l.rect(mitad - 2, py, mitad - 2, py + 6, rgb("#c9c6bb"))
        l.rect(mitad - 1, py + 1, mitad, py + 1, rgb("#8b8a84"))
        l.rect(mitad - 1, py + 3, mitad, py + 3, rgb("#8b8a84"))

    else:

        ancho_hoja = max(3, ancho // 6)

        hoja(x0, x0 + ancho_hoja - 1)
        hoja(x1 - ancho_hoja + 1, x1)


def vidriera(l, x0, y0, x1, y1, interior, r, estantes=False):
    """
    Vidriera con marco de aluminio: el vidrio (azulado, con un reflejo en
    diagonal), el zocalo de abajo y, si se pide, estantes con cosas.
    """

    marco = GRIS_ALUM

    l.rect(x0, y0, x1, y1, marco)

    vx0, vy0, vx1, vy1 = x0 + 2, y0 + 2, x1 - 2, y1 - 6

    for y in range(vy0, vy1 + 1):

        t = (y - vy0) / max(1, vy1 - vy0)

        l.rect(vx0, y, vx1, y, mezcla(rgb("#5f7f94"), rgb("#2b4254"), t))

    interior(l, vx0, vy0, vx1, vy1)

    # reflejos en diagonal (dos franjas claras que cruzan el vidrio)
    for y in range(vy0, vy1 + 1):

        for x in range(vx0, vx1 + 1):

            d = (x + y) % 26

            if d < 3 or 8 <= d < 9:

                actual = l.im.getpixel((x, y))[:3]

                l.px(x, y, mezcla(actual, rgb("#cfe2ea"), 0.26 if d < 3 else 0.16))

    # el zocalo de abajo
    l.rect(x0, y1 - 5, x1, y1, rgb("#3a3a40"))
    l.rect(x0, y1 - 5, x1, y1 - 5, rgb("#8d8d93"))

    if estantes:

        for fy in (vy0 + 9, vy0 + 21, vy0 + 33):

            if fy < vy1:
                l.rect(vx0, fy, vx1, fy, rgb("#d8d3c4"))
                l.rect(vx0, fy + 1, vx1, fy + 1, rgb("#4b3f33"))


# ----------------------------------------------------------
# Ventanitas con reja de la fachada de piedra
# ----------------------------------------------------------

def ventanita_reja(l, x, y0, y1, ancho):
    """Ventana chica con marco de hormigon y reja de hierro."""

    l.rect(x - 1, y0 - 1, x + ancho, y1 + 1, HORMIGON)
    l.rect(x, y0, x + ancho - 1, y1, rgb("#26323f"))
    l.rect(x + 1, y0 + 1, x + 2, y0 + 2, rgb("#6d8aa0"))

    for xx in range(x + 1, x + ancho - 1, 2):

        l.rect(xx, y0, xx, y1, HIERRO)

    l.rect(x, (y0 + y1) // 2, x + ancho - 1, (y0 + y1) // 2, HIERRO)

    l.rect(x - 2, y1 + 2, x + ancho + 1, y1 + 2, luz(HORMIGON, 0.25))


# ==========================================================
# LA ENTRADA (nivel 2)
# ==========================================================

# Columnas (dentro del primer edificio) de cada pieza de la entrada
IZQ_VIDRIERA = (18, 53)
IZQ_PANEL = (54, 97)
PUERTA = (98, 123)
DER_PANEL = (124, 153)
DER_VIDRIERA = (154, 188)

# x del centro de la puerta (donde arranca el jugador)
ENTRADA_CX = (PUERTA[0] + PUERTA[1]) // 2

# Filas (dentro del edificio de 95 de alto)
FILA_CORNISA = 27
FILA_PB = 35                    # donde arranca la planta baja


def _afiche_azul(l, x0, y0, x1, y1):
    """Lo que se ve en la vidriera de la izquierda: un afiche azul."""

    ax0, ax1 = x0 + 5, x1 - 5

    ay0, ay1 = y0 + 6, y1 - 8

    l.rect(ax0, ay0, ax1, ay1, rgb("#1f4f9e"))
    l.rect(ax0, ay0, ax1, ay0 + 1, rgb("#3e74c8"))

    # renglones del afiche
    for k, yy in enumerate(range(ay0 + 5, ay1 - 2, 4)):

        corto = 3 if k % 3 == 2 else 0

        l.rect(ax0 + 3, yy, ax1 - 3 - corto, yy, rgb("#dfe8f6"))

    l.rect(ax0 + 3, ay1 - 6, ax0 + 9, ay1 - 3, rgb("#f0c030"))


def _estantes_con_cosas(l, x0, y0, x1, y1):
    """Vidriera de la derecha: estantes con un objeto rojo y otros chicos."""

    for fy, cosas in (
        (y0 + 9, ((3, 5, "#d8d3c4"), (9, 4, "#8f6f4a"), (21, 6, "#a8b4c0"))),
        (y0 + 21, ((4, 6, "#c8322d"), (13, 5, "#e6e0d0"), (23, 4, "#506a82"))),
        (y0 + 33, ((6, 5, "#d8b050"), (15, 6, "#7a8a96"))),
    ):

        for dx, h, col in cosas:

            if x0 + dx + 4 <= x1 and fy - h > y0:

                l.rect(x0 + dx, fy - h, x0 + dx + 3, fy - 1, rgb(col))
                l.rect(x0 + dx, fy - h, x0 + dx, fy - 1, luz(rgb(col), 0.3))


def fachada_entrada(ancho, cuerpo, r):
    """
    La entrada del Huergo como en la foto (nivel 2). Devuelve (lienzo, paleta).
    `cuerpo` es el alto del edificio chico (95); la planta baja va abajo y la
    cornisa de hormigon con la piedra y sus ventanitas, arriba.
    """

    b = cuerpo - 1

    piedra = PIEDRA_BEIGE

    c = dict(fachada=piedra, pared=piedra, guarda=piedra)

    l = Lienzo(ancho, cuerpo)

    # ---- la piedra de toda la fachada
    piedra_moteada(l, 0, 0, ancho - 1, b, r)

    # juntas verticales de los paneles de piedra
    for x in range(30, ancho, 46):

        l.rect(x, 0, x, FILA_CORNISA - 1, sombra(piedra, 0.9))

    # faja gris arriba (en la foto: una banda de hormigon bajo el techo)
    l.rect(0, 0, ancho - 1, 2, HORMIGON)
    l.rect(0, 0, ancho - 1, 0, luz(HORMIGON, 0.2))
    l.rect(0, 3, ancho - 1, 3, sombra(HORMIGON, 0.7))

    # ventanitas con reja arriba de la cornisa
    for x in range(26, ancho - 14, 29):

        ventanita_reja(l, x, 8, 21, 9)

    # ---- la cornisa de hormigon (sobresale: tiene luz arriba y sombra abajo)
    l.rect(0, FILA_CORNISA, ancho - 1, FILA_CORNISA + 1, luz(HORMIGON, 0.3))
    l.rect(0, FILA_CORNISA + 2, ancho - 1, FILA_CORNISA + 5, HORMIGON)
    l.rect(0, FILA_CORNISA + 6, ancho - 1, FILA_CORNISA + 6, sombra(HORMIGON, 0.62))

    # sombra que tira la cornisa sobre la planta baja
    for k, f in enumerate((0.78, 0.86, 0.93)):

        l.rect(0, FILA_CORNISA + 7 + k, ancho - 1, FILA_CORNISA + 7 + k, sombra(piedra, f))

    # ---- planta baja: ventanas con reja de cada lado de la entrada
    for x in (212, 246):

        if x + 18 < ancho - 4:

            l.rect(x - 2, 44, x + 19, 82, HORMIGON)
            l.rect(x, 46, x + 17, 80, rgb("#26323f"))
            l.rect(x + 1, 47, x + 4, 52, rgb("#6d8aa0"))

            for xx in range(x + 1, x + 17, 3):

                l.rect(xx, 46, xx, 80, HIERRO)

            for yy in range(52, 80, 9):

                l.rect(x, yy, x + 17, yy, HIERRO)

    # zocalo de granito gris en toda la fachada
    zoc = rgb("#6f6d6a")

    l.rect(0, b - 3, ancho - 1, b, zoc)
    l.rect(0, b - 3, ancho - 1, b - 3, luz(zoc, 0.3))

    # ---- vidriera izquierda (con el afiche azul)
    x0, x1 = IZQ_VIDRIERA

    vidriera(
        l, x0, FILA_PB + 3, x1, b - 3,
        lambda lz, a, y0, z, y1: _afiche_azul(lz, a, y0, z, y1),
        r
    )

    # ---- panel de granito negro de la izquierda
    x0, x1 = IZQ_PANEL

    granito_negro(l, x0, FILA_PB + 1, x1, b - 1, r)

    cx = (x0 + x1) // 2

    grabado(l, cx, 51, "INSTITUTO")
    grabado(l, cx, 59, "INDUSTRIAL")

    # ---- la puerta: nicho con el porton de hierro, el escalon amarillo
    x0, x1 = PUERTA

    l.rect(x0, FILA_PB, x1, b, rgb("#4a4a50"))
    l.rect(x0, FILA_PB, x1, FILA_PB + 2, rgb("#8f8e8a"))

    hall_oscuro(l, x0 + 2, FILA_PB + 5, x1 - 2, b - 4)

    # un poco de luz del hall, abajo
    l.rect(x0 + 2, b - 12, x1 - 2, b - 4, rgb("#8a6a40"))

    reja_rombos(l, x0 + 2, FILA_PB + 5, x1 - 2, b - 4)

    l.rect(x0, b - 3, x1, b - 1, AMARILLO_UMBRAL)
    l.rect(x0, b - 3, x1, b - 3, luz(AMARILLO_UMBRAL, 0.35))
    l.rect(x0, b, x1, b, sombra(AMARILLO_UMBRAL, 0.6))

    # ---- panel de granito negro de la derecha
    x0, x1 = DER_PANEL

    granito_negro(l, x0, FILA_PB + 1, x1, b - 1, r)

    cx = (x0 + x1) // 2

    grabado(l, cx, 47, "LUIS A.")
    grabado(l, cx, 55, "HUERGO")
    grabado(l, cx, 66, "759")

    # ---- vidriera derecha (estantes)
    x0, x1 = DER_VIDRIERA

    vidriera(
        l, x0, FILA_PB + 3, x1, b - 3,
        lambda lz, a, y0, z, y1: _estantes_con_cosas(lz, a, y0, z, y1),
        r, estantes=True
    )

    # ---- los dos postes finitos de los costados (blanco y negro)
    px0 = IZQ_VIDRIERA[0] - 3
    px1 = DER_VIDRIERA[1] + 3

    l.rect(px0, FILA_PB - 3, px0 + 1, b, rgb("#e8e6df"))
    l.rect(px0, FILA_PB - 3, px0, b, rgb("#ffffff"))
    l.rect(px0 + 1, FILA_PB - 3, px0 + 1, b, rgb("#bdbab0"))

    l.rect(px1, FILA_PB - 3, px1 + 1, b, rgb("#1d1d22"))
    l.rect(px1, FILA_PB - 3, px1, b, rgb("#4a4a52"))

    return l, c


def vereda_entrada(capa, x0, x1, fila_fachada, fila_calle, r):
    """
    La vereda de la entrada (se dibuja despues de la calle): baldosas ocres,
    la banda amarilla podotactil junto al cordon y baldosas grises con
    puntitos adelante de la puerta.
    """

    ocre = rgb("#c9a45a")

    y0 = fila_fachada + 1
    y1 = fila_calle + 1

    capa.rect(x0, y0, x1, y1, ocre)

    capa.rect(x0, y0, x1, y0 + 1, sombra(ocre, 0.78))

    # cada baldosa un poco distinta, con sus juntas
    for k, x in enumerate(range(x0, x1 + 1, 9)):

        for fila, yy in enumerate(range(y0 + 2, y1 - 3, 4)):

            f = (0.97, 1.04, 0.93, 1.0)[(k * 3 + fila) % 4]

            capa.rect(x, yy, min(x1, x + 8), min(y1 - 3, yy + 3), tuple(
                max(0, min(255, int(v * f))) for v in ocre
            ))

        capa.rect(x, y0 + 2, x, y1 - 3, sombra(ocre, 0.8))

    for yy in range(y0 + 5, y1 - 2, 4):

        capa.rect(x0, yy, x1, yy, sombra(ocre, 0.82))

    # banda amarilla junto al cordon, con puntitos
    amarillo = rgb("#f0c828")

    capa.rect(x0, y1 - 3, x1, y1, amarillo)
    capa.rect(x0, y1 - 3, x1, y1 - 3, luz(amarillo, 0.3))

    for x in range(x0 + 1, x1, 3):

        capa.px(x, y1 - 2, sombra(amarillo, 0.72))
        capa.px(x + 1, y1 - 1, sombra(amarillo, 0.72))

    # baldosas grises con puntitos: del cordon a la puerta
    gris = rgb("#5d5d63")

    gx0, gx1 = PUERTA[0] - 4, PUERTA[1] + 4

    capa.rect(gx0, y0 + 2, gx1, y1 - 4, gris)
    capa.marco(gx0, y0 + 2, gx1, y1 - 4, sombra(gris, 0.7))

    for yy in range(y0 + 4, y1 - 5, 3):

        for xx in range(gx0 + 2, gx1 - 1, 3):

            capa.px(xx, yy, luz(gris, 0.28))


# ==========================================================
# EL INTERIOR (nivel 1): un solo piso, chato, sin enemigos
# ==========================================================
#
# El nivel 1 es mas corto que los demas (ANCHO_INTERIOR) y se recorre por un
# solo piso: no hay techos a donde subir. Se camina por el pasillo de la
# planta baja del colegio, de un taller al hall de entrada, y se sale por el
# porton de la calle. Cada tramo es un "modulo" (aula, taller, laboratorio...)
# con las mismas piezas de interior_huergo.py, pero todos de la misma altura
# (del piso al cielorraso).

import interior_huergo as IH  # noqa: E402

ANCHO_INTERIOR = 1600                   # en pixeles de dibujo (4800 de pantalla)

# Donde arranca el cuerpo de los modulos (arriba de lo que se ve) y su alto
FILA_TOPE = 94
FILA_CIELORRASO = 108                   # la primera fila que se ve en pantalla
FILA_CORNISA_INT = 114                  # donde termina el cielorraso y arranca la pared

VESTIBULO_ANCHO = 120
SALIDA_ANCHO = 110
SALIDA_PUERTA_DX = 62                   # del centro del porton al final del nivel
SALIDA_PUERTA_MITAD = 19

# Los modulos del recorrido: (estilo, ancho). Suman ANCHO_INTERIOR junto con el
# vestibulo y la salida.
RUTA = (
    ("taller_mecanico", 106),
    ("aula", 84),
    ("taller_electrico", 98),
    ("casilleros", 70),
    ("laboratorio", 94),
    ("aula", 72),
    ("ventanal", 80),
    ("biblioteca", 100),
    ("escalera", 104),
    ("oficina", 84),
    ("casilleros", 56),
    ("mural", 78),
    ("aula", 70),
    ("taller_mecanico", 92),
    ("ventanal", 72),
    ("salon_actos", 110),
)


def verificar_ruta():
    """El recorrido tiene que llenar el nivel justo."""

    total = sum(a for _, a in RUTA) + VESTIBULO_ANCHO + SALIDA_ANCHO

    if total != ANCHO_INTERIOR:

        raise RuntimeError(
            "la ruta del interior mide {} y tiene que medir {}".format(total, ANCHO_INTERIOR)
        )


def _tacho(l, x, b, color):
    """Tacho de residuos de color (Escuelas Verdes)."""

    l.rect(x, b - 11, x + 6, b - 2, color)
    l.rect(x, b - 11, x, b - 2, luz(color, 0.3))
    l.rect(x + 6, b - 11, x + 6, b - 2, sombra(color, 0.7))
    l.rect(x - 1, b - 13, x + 7, b - 12, sombra(color, 0.6))
    l.rect(x + 2, b - 8, x + 4, b - 6, luz(color, 0.5))


def modulo_vestibulo(ancho, cuerpo, r):
    """
    El vestibulo de entrada: el nombre del colegio en el granito negro, la
    placa del lema, la bandera, la puerta de la secretaria y los tachos de
    Escuelas Verdes. Es lo ultimo antes de la puerta de calle.
    """

    pared = rgb("#e2d8bf")

    c = dict(pared=pared, guarda=rgb("#2f3f4a"), fachada=pared)

    l = Lienzo(ancho, cuerpo)

    b = cuerpo - 1

    IH._pared(l, c)

    # el granito negro con el nombre, como el de la entrada
    gx0, gx1 = 5, 62

    granito_negro(l, gx0, b - 104, gx1, b - 6, r)

    cx = (gx0 + gx1) // 2

    grabado(l, cx, b - 94, "INSTITUTO")
    grabado(l, cx, b - 86, "INDUSTRIAL")

    l.rect(cx - 12, b - 76, cx + 12, b - 76, rgb("#77757a"))

    grabado(l, cx, b - 70, "LUIS A.")
    grabado(l, cx, b - 62, "HUERGO")
    grabado(l, cx, b - 48, "FUNDADO")
    grabado(l, cx, b - 41, "EN 1934")

    # una bandera, la puerta de porteria (con su plaquita) y un matafuego
    IH._bandera_pared(l, 66, b - 100)

    IH._puerta(l, 94, 16, b, r, numero=None)

    # plaquita con el nombre de la puerta (letras chicas)
    px0 = 85

    l.rect(px0, b - 66, px0 + 33, b - 57, rgb("#2f3f4a"))
    l.rect(px0, b - 66, px0 + 33, b - 66, rgb("#6a7a86"))

    micro_centrado(l, px0 + 17, b - 63, "PORTERIA", rgb("#e8e4d6"))

    IH._matafuego(l, 112, b)

    # los tachos de colores (Escuelas Verdes)
    for k, col in enumerate(("#2e8a4a", "#d8b82a", "#2f6fb0")):

        _tacho(l, 64 + k * 9, b, rgb(col))

    return l, c


def _calle_de_afuera(l, x0, y0, x1, y1):
    """
    Lo que se ve por el porton abierto: la calle de San Telmo con sol, la
    vereda ocre, la banda amarilla y, enfrente, una casa de piedra con su
    puerta y un arbol.
    """

    for y in range(y0, y1 + 1):

        t = (y - y0) / max(1, y1 - y0)

        l.rect(x0, y, x1, y, mezcla(rgb("#9fd0f0"), rgb("#f2fbff"), t))

    ancho = x1 - x0 + 1

    # la casa de enfrente
    casa = rgb("#cdb994")

    cy0 = y0 + (y1 - y0) // 3

    l.rect(x0, cy0, x1, y1 - 12, casa)
    l.rect(x0, cy0, x1, cy0 + 1, luz(casa, 0.25))
    l.rect(x0, cy0 + 2, x1, cy0 + 3, sombra(casa, 0.8))

    for vx in range(x0 + 3, x1 - 6, 11):

        l.rect(vx, cy0 + 8, vx + 5, cy0 + 20, rgb("#3b5a86"))
        l.rect(vx, cy0 + 8, vx + 1, cy0 + 12, rgb("#8fb4d8"))
        l.rect(vx - 1, cy0 + 21, vx + 6, cy0 + 21, luz(casa, 0.3))

    # un arbol
    verde = rgb("#4f9a48")

    l.rect(x1 - 5, y1 - 22, x1 - 4, y1 - 10, rgb("#6b4a2f"))
    l.circulo(x1 - 4, y1 - 27, 7, verde)
    l.circulo(x1 - 8, y1 - 24, 5, sombra(verde, 0.85))

    # la vereda ocre y la banda amarilla
    ocre = rgb("#c9a45a")

    l.rect(x0, y1 - 11, x1, y1 - 3, ocre)
    l.rect(x0, y1 - 11, x1, y1 - 11, sombra(ocre, 0.8))

    for x in range(x0, x1 + 1, 8):

        l.rect(x, y1 - 10, x, y1 - 3, sombra(ocre, 0.85))

    amarillo = rgb("#f0c828")

    l.rect(x0, y1 - 2, x1, y1, amarillo)

    for x in range(x0 + 1, x1, 3):

        l.px(x, y1 - 1, sombra(amarillo, 0.72))


def modulo_salida_reja(ancho, cuerpo, r):
    """
    La salida: la puerta de calle del colegio vista desde adentro. A los dos
    lados, el granito negro; en el medio, el porton de rombos abierto (las dos
    hojas contra las jambas) y por el hueco la calle con sol. Arriba, el
    cartel verde de SALIDA. El centro del porton queda a SALIDA_PUERTA_DX del
    final del nivel (un poco antes de la bandera de meta, que esta a 100 px).
    """

    pared = rgb("#e2d8bf")

    c = dict(pared=pared, guarda=rgb("#2f3f4a"), fachada=pared)

    l = Lienzo(ancho, cuerpo)

    b = cuerpo - 1

    IH._pared(l, c)

    # a la izquierda: una ventana al patio y un matafuego
    IH._ventana(l, 6, 20, b - 120, b - 60, "patio")

    IH._matafuego(l, 26, b)

    cx = ancho - SALIDA_PUERTA_DX

    mitad = SALIDA_PUERTA_MITAD

    x0, x1 = cx - mitad, cx + mitad

    alto_p = 58

    # los paneles de granito de los costados (del piso a arriba del porton)
    granito_negro(l, x1 + 3, b - alto_p - 8, ancho - 2, b - 4, r)

    # el hueco: marco de piedra gris, la calle y, arriba, el dintel
    piedra = rgb("#8f8e8a")

    l.rect(x0 - 3, b - alto_p - 8, x1 + 3, b, piedra)
    l.rect(x0 - 3, b - alto_p - 8, x1 + 3, b - alto_p - 6, luz(piedra, 0.25))

    _calle_de_afuera(l, x0, b - alto_p - 3, x1, b - 3)

    # el porton, abierto contra las jambas
    reja_rombos(l, x0, b - alto_p - 3, x1, b - 3, abierta=True)

    # el escalon amarillo del umbral
    l.rect(x0 - 3, b - 3, x1 + 3, b - 1, AMARILLO_UMBRAL)
    l.rect(x0 - 3, b - 3, x1 + 3, b - 3, luz(AMARILLO_UMBRAL, 0.35))

    # el cartel verde de SALIDA, encima
    texto = "SALIDA"

    tw = IH.ancho_texto(texto)

    ancho_c = tw + 18

    xc = cx - ancho_c // 2

    y_c = b - alto_p - 26

    l.rect(xc - 1, y_c, xc + ancho_c, y_c + 13, rgb("#0f3a24"))
    l.rect(xc, y_c + 1, xc + ancho_c - 1, y_c + 12, rgb("#1f8a4a"))
    l.rect(xc, y_c + 1, xc + ancho_c - 1, y_c + 1, rgb("#58d08a"))
    l.texto(xc + 3, y_c + 4, texto, BLANCO)
    IH.E.flecha_derecha(l, xc + tw + 5, y_c + 4, BLANCO)

    return l, c


# ----------------------------------------------------------
# piso, cielorraso y luces
# ----------------------------------------------------------

def piso_granito(capa, r, fila0=258, fila1=312):
    """
    El piso del pasillo: granito reconstituido beige con motitas, juntas cada
    14 columnas y un zocalo oscuro donde toca la pared.
    """

    base = rgb("#c3bba6")

    capa.rect(0, fila0, capa.w - 1, fila1 - 1, base)

    tonos = (
        rgb("#8d8672"), rgb("#d9d3c0"), rgb("#a89f88"), rgb("#6f6a5c"),
        rgb("#e4dfce")
    )

    for _ in range(capa.w * (fila1 - fila0) // 5):

        capa.px(
            r.randrange(capa.w), r.randint(fila0 + 2, fila1 - 1),
            r.choice(tonos)
        )

    # juntas: verticales cada 14 y horizontales cada 10 (las baldosas se
    # ven mas altas arriba que abajo porque el piso se aleja)
    junta = sombra(base, 0.82)

    for x in range(0, capa.w, 14):

        capa.rect(x, fila0 + 2, x, fila1 - 1, junta)

    for y in (fila0 + 11, fila0 + 22, fila0 + 34, fila0 + 47):

        capa.rect(0, y, capa.w - 1, y, junta)

    # zocalo
    capa.rect(0, fila0, capa.w - 1, fila0, rgb("#2f2b26"))
    capa.rect(0, fila0 + 1, capa.w - 1, fila0 + 1, rgb("#6f6a5c"))
    capa.rect(0, fila0 + 2, capa.w - 1, fila0 + 2, sombra(base, 0.8))


def piso_umbral(capa, x0, x1, r, fila0=258, fila1=312):
    """El piso de la puerta de calle: baldosas ocres, con la banda amarilla."""

    ocre = rgb("#c9a45a")

    capa.rect(x0, fila0, x1, fila1 - 1, ocre)

    for k, x in enumerate(range(x0, x1 + 1, 9)):

        capa.rect(x, fila0 + 2, x, fila1 - 1, sombra(ocre, 0.8))

    for y in range(fila0 + 7, fila1, 9):

        capa.rect(x0, y, x1, y, sombra(ocre, 0.82))

    for _ in range((x1 - x0) * 3):

        capa.px(
            r.randint(x0, x1), r.randint(fila0 + 2, fila1 - 1),
            sombra(ocre, r.choice((0.86, 0.94, 1.08)))
        )

    capa.rect(x0, fila0, x1, fila0 + 1, sombra(ocre, 0.6))

    # la banda amarilla, de punta a punta, en el medio del piso
    amarillo = rgb("#f0c828")

    capa.rect(x0, fila0 + 22, x1, fila0 + 25, amarillo)
    capa.rect(x0, fila0 + 22, x1, fila0 + 22, luz(amarillo, 0.3))

    for x in range(x0 + 1, x1, 3):

        capa.px(x, fila0 + 24, sombra(amarillo, 0.72))


def cielorraso(capa, r, ancho=None):
    """
    El cielorraso y la cornisa de arriba de todo el pasillo: yeso claro,
    una moldura, y en el borde una sombra. Cubre desde FILA_TOPE.
    """

    ancho = ancho or capa.w

    yeso = rgb("#d6cfbc")

    for y in range(FILA_TOPE, FILA_CORNISA_INT):

        t = (y - FILA_TOPE) / (FILA_CORNISA_INT - FILA_TOPE)

        capa.rect(0, y, ancho - 1, y, mezcla(sombra(yeso, 0.62), yeso, t ** 0.7))

    # juntas del cielorraso (placas de 40 de ancho)
    for x in range(0, ancho, 40):

        capa.rect(x, FILA_TOPE, x, FILA_CORNISA_INT - 1, sombra(yeso, 0.82))

    # moldura (cornisa)
    cornisa = rgb("#ece4cf")

    capa.rect(0, FILA_CORNISA_INT, ancho - 1, FILA_CORNISA_INT, luz(cornisa, 0.3))
    capa.rect(0, FILA_CORNISA_INT + 1, ancho - 1, FILA_CORNISA_INT + 4, cornisa)
    capa.rect(0, FILA_CORNISA_INT + 5, ancho - 1, FILA_CORNISA_INT + 5, sombra(cornisa, 0.7))

    # sombra que tira la moldura en la pared
    for k, f in enumerate((0.84, 0.91, 0.96)):

        y = FILA_CORNISA_INT + 6 + k

        # (se oscurece lo que ya hay: las paredes tienen distintos colores)
        a = capa.im.crop((0, y, ancho, y + 1))

        px = a.load()

        for x in range(ancho):

            p = px[x, 0]

            px[x, 0] = (int(p[0] * f), int(p[1] * f), int(p[2] * f), p[3])

        capa.im.paste(a, (0, y))


def luminarias(capa, xs, r):
    """
    Tubos fluorescentes colgados del cielorraso, en las columnas `xs`: un
    artefacto blanco con su luz sobre la pared y el cano de un matafuegos al
    costado... (solo el artefacto y el resplandor).
    """

    for cx in xs:

        y = FILA_CORNISA_INT + 8

        # el resplandor sobre la pared (antes del artefacto)
        IH._resplandor(capa, cx, y + 8, 16, rgb("#fff4d0"), 120)

        capa.rect(cx - 9, y, cx + 9, y + 3, rgb("#f6f3e8"))
        capa.rect(cx - 9, y, cx + 9, y, rgb("#ffffff"))
        capa.rect(cx - 9, y + 3, cx + 9, y + 3, rgb("#a9a597"))

        # las barritas que lo cuelgan
        capa.rect(cx - 6, y - 3, cx - 6, y - 1, rgb("#6a6a70"))
        capa.rect(cx + 6, y - 3, cx + 6, y - 1, rgb("#6a6a70"))

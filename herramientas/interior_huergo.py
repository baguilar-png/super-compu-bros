"""
Los modulos del interior del Instituto Huergo (nivel 1): aulas, talleres, la
biblioteca, el laboratorio, la escalera, el salon de actos...

Cada modulo es el frente de un tramo de pasillo: un lienzo de `ancho` x `cuerpo`
donde la ultima fila es el piso. El nivel 1 los pone uno detras del otro (ver
huergo_real.RUTA y generar_techos.hacer_cercana_plana), todos de la misma altura:
es un solo piso, sin techos a donde subir y sin enemigos. Tambien estan las
capas de atras (cielo, lejos, medio), que casi no se ven: las paredes llegan
hasta el cielorraso.

La entrada y la salida del colegio (el granito negro, el porton de rombos...) estan
en huergo_real.py. Todo es un dibujo aproximado: lo importante es que se lea
como "un colegio tecnico por dentro".

Medidas en pixeles de dibujo (1 = 3 de pantalla).
"""

import numpy as np
from PIL import Image

from pixelart import (
    Lienzo, rgb, luz, sombra, mezcla, ancho_texto, bandera, arbusto,
    BLANCO, NEGRO, ORO, CELESTE_ARG, ROJO, VIDRIO, VIDRIO_LUZ, VIDRIO_OSC
)
import edificios as E

# Medidas (las mismas de generar_techos.py)
ANCHO = 3200
ALTO = 200
ALTO_CERCANA = 312
FILA_FACHADA = 258
FILA_CALLE = 268

# Filas de un modulo chico (de arriba a abajo del cuerpo): lo que sobra en los
# medianos y grandes es pared alta
BANDA = 95

# Alto de las puertas y de los ventanales de la banda de abajo
PUERTA_ALTO = 46


def _col(*hexes):
    return [rgb(h) for h in hexes]


PAREDES = _col("#e4d9bd", "#d8e0c4", "#ece0b0", "#d3dade", "#ead0b6", "#dfd2c4")
GUARDAS = _col("#2f5d4a", "#6b4a2f", "#2f4a6b", "#6a2f3a", "#3a5a3a")

MADERA = rgb("#7a4f2f")
MADERA_C = rgb("#9a6a40")
MADERA_O = rgb("#4a3320")
PIEDRA = rgb("#d6cbae")
ACERO = rgb("#8d939c")
HIERRO = rgb("#23262c")


# ==========================================================
# AYUDAS DE DIBUJO
# ==========================================================

def _paleta(r):

    pared = r.choice(PAREDES)

    return dict(pared=pared, guarda=r.choice(GUARDAS), fachada=pared)


def _posiciones(ancho, anchos, margen=5):
    """x de cada elemento, repartidos parejo (con el mismo hueco entre todos)."""

    libre = ancho - 2 * margen - sum(anchos)

    hueco = max(0.0, libre / (len(anchos) + 1))

    xs = []

    x = margen + hueco

    for a in anchos:

        xs.append(int(round(x)))

        x += a + hueco

    return xs


def _texto_que_entra(opciones, ancho_max):
    """La primera frase que entra en el ancho dado (si ninguna, la mas corta)."""

    for t in opciones:

        if ancho_texto(t) + 8 <= ancho_max:
            return t

    return opciones[-1]


def _cartel(l, cx, y, texto, fondo, color_texto=BLANCO):
    """Cartel de pared (de 11 filas) con su texto."""

    tw = ancho_texto(texto)

    x0 = cx - (tw + 8) // 2

    l.rect(x0 - 1, y - 1, x0 + tw + 8, y + 10, sombra(fondo, 0.55))
    l.rect(x0, y, x0 + tw + 7, y + 9, fondo)
    l.rect(x0, y, x0 + tw + 7, y, luz(fondo, 0.4))
    l.texto(x0 + 4, y + 1, texto, color_texto)


def _pared(l, c):
    """Pared de fondo: revoque, guarda de pintura al oleo, zocalo y bordes."""

    w, h = l.w, l.h

    b = h - 1

    pared, guarda = c["pared"], c["guarda"]

    # mas oscura arriba (lejos de las ventanas)
    for y in range(h):

        t = y / h

        l.rect(0, y, w - 1, y, mezcla(sombra(pared, 0.82), pared, min(1.0, t * 1.7)))

    # guarda y su filete
    l.rect(0, b - 26, w - 1, b, guarda)
    l.rect(0, b - 28, w - 1, b - 27, luz(pared, 0.2))
    l.rect(0, b - 26, w - 1, b - 26, luz(guarda, 0.35))
    l.rect(0, b - 25, w - 1, b - 25, sombra(guarda, 0.8))

    # zocalo
    l.rect(0, b - 1, w - 1, b, sombra(guarda, 0.55))

    # bordes del modulo
    l.rect(0, 0, 0, b, sombra(pared, 0.55))
    l.rect(w - 1, 0, w - 1, b, sombra(pared, 0.7))


# ----------------------------------------------------------
# cosas de pared
# ----------------------------------------------------------

def _ventana(l, x0, x1, y0, y1, vista="cielo"):
    """Ventana alta con arco: el vidrio muestra el dia de afuera y tiene cruz de madera."""

    marco = rgb("#8a6a3a")
    cielo_a = rgb("#b9dcf2")
    cielo_b = rgb("#e6f4fc")

    l.rect(x0 - 1, y0 + 4, x1 + 1, y1 + 1, marco)
    l.arco(x0 - 1, y0 + 5, x1 + 1, 6, marco)

    for y in range(y0 + 2, y1 + 1):

        t = (y - y0) / max(1, y1 - y0)

        l.rect(x0, y, x1, y, mezcla(cielo_a, cielo_b, t))

    l.arco(x0, y0 + 5, x1, 5, cielo_a)

    if vista == "patio":

        # un arbol y la pared de enfrente
        ancho = x1 - x0 + 1

        verde = rgb("#4f9a48")

        l.rect(x0, y1 - 8, x1, y1, rgb("#d8b98a"))
        l.rect(x0, y1 - 9, x1, y1 - 9, rgb("#b5532f"))

        l.circulo(x0 + ancho // 2, y1 - 13, max(3, ancho // 3), verde)
        l.circulo(x0 + ancho // 2 - 2, y1 - 11, max(2, ancho // 4), sombra(verde, 0.85))

    medio = (x0 + x1) // 2

    l.rect(medio, y0 + 1, medio, y1, marco)
    l.rect(x0, (y0 + y1) // 2, x1, (y0 + y1) // 2, marco)

    # el alfeizar
    l.rect(x0 - 2, y1 + 2, x1 + 2, y1 + 2, luz(rgb("#cfc4a8"), 0.2))


def _puerta(l, x, ancho, b, r, numero=None, color=None):
    """Puerta de aula: marco, hoja de madera con panel, vidrio y picaporte."""

    madera = color or r.choice((MADERA, MADERA_C, rgb("#6a4a2a")))

    alto = PUERTA_ALTO

    l.rect(x, b - alto - 1, x + ancho - 1, b, MADERA_O)

    ix0 = x + 2
    ix1 = x + ancho - 3

    l.rect(ix0, b - alto, ix1, b, madera)
    l.rect(ix0 + 1, b - alto + 1, ix0 + 1, b, luz(madera, 0.2))

    # vidrio
    l.rect(ix0 + 2, b - alto + 4, ix1 - 2, b - alto + 22, rgb("#8fb4d8"))
    l.rect(ix0 + 2, b - alto + 4, ix0 + 4, b - alto + 9, rgb("#d6ecfa"))
    l.rect((ix0 + ix1) // 2, b - alto + 4, (ix0 + ix1) // 2, b - alto + 22, MADERA_O)

    # panel de abajo
    l.rect(ix0 + 2, b - 19, ix1 - 2, b - 3, sombra(madera, 0.82))
    l.rect(ix0 + 3, b - 18, ix1 - 3, b - 4, madera)

    # picaporte
    l.rect(ix1 - 2, b - 24, ix1 - 1, b - 22, ORO)

    if numero:

        tw = ancho_texto(numero)

        cx = x + ancho // 2

        l.rect(cx - tw // 2 - 2, b - alto - 10, cx + tw // 2 + 2, b - alto - 3, rgb("#f4f1e8"))
        l.rect(cx - tw // 2 - 2, b - alto - 10, cx + tw // 2 + 2, b - alto - 10, rgb("#b0a890"))
        l.texto(cx - tw // 2, b - alto - 9, numero, rgb("#2a2630"))


def _ventana_aula(l, x, ancho, b, r):
    """Ventana de pasillo a un aula: se ve el pizarron y los bancos."""

    y1 = b - 30
    y0 = b - 62

    marco = rgb("#7a5a38")

    l.rect(x - 1, y0 - 1, x + ancho, y1 + 1, marco)
    l.rect(x, y0, x + ancho - 1, y1, rgb("#cfd9c4"))

    # pizarron
    l.rect(x + 2, y0 + 4, x + ancho - 3, y0 + 16, rgb("#2f4a3a"))
    l.rect(x + 2, y0 + 17, x + ancho - 3, y0 + 17, rgb("#8a6a3a"))

    for _ in range(3):

        gx = r.randint(x + 4, max(x + 5, x + ancho - 9))

        l.rect(gx, y0 + 7 + r.randint(0, 6), gx + r.randint(2, 5), y0 + 7 + r.randint(0, 6), rgb("#e8eee6"))

    # bancos y cabezas
    for bx in range(x + 3, x + ancho - 5, 8):

        l.rect(bx, y1 - 7, bx + 5, y1 - 5, rgb("#8a6a3a"))
        l.rect(bx + 1, y1 - 4, bx + 1, y1, rgb("#5a4a38"))
        l.rect(bx + 4, y1 - 4, bx + 4, y1, rgb("#5a4a38"))
        l.rect(bx + 1, y1 - 12, bx + 3, y1 - 9, r.choice((rgb("#3a2a20"), rgb("#7a5a3a"), rgb("#c8a070"))))

    # travesanos y brillo del vidrio
    l.rect(x + ancho // 2, y0, x + ancho // 2, y1, marco)

    for k in range(5):

        l.px(x + 2 + k, y0 + 7 - k, rgb("#e6f4fc"))
        l.px(x + 3 + k, y0 + 7 - k, rgb("#e6f4fc"))


def _cartelera(l, x, ancho, b, r):
    """Cartelera de corcho con papeles."""

    y0 = b - 56
    y1 = b - 32

    l.rect(x - 1, y0 - 1, x + ancho, y1 + 1, rgb("#5a4020"))
    l.rect(x, y0, x + ancho - 1, y1, rgb("#b08a58"))

    colores = (rgb("#f4f1e8"), rgb("#f2d65a"), rgb("#8fb8e0"), rgb("#e89aa0"), rgb("#a8d8a0"))

    for _ in range(5):

        px = r.randint(x + 1, x + ancho - 6)
        py = r.randint(y0 + 1, y1 - 8)

        l.rect(px, py, px + 4, py + 6, r.choice(colores))
        l.px(px + 2, py, rgb("#c8322d"))


def _cuadro(l, x, y, r):
    """Cuadro con retrato (marco dorado y un ovalo)."""

    l.rect(x, y, x + 9, y + 12, ORO)
    l.rect(x + 1, y + 1, x + 8, y + 11, rgb("#3a2f26"))

    l.elipse(x + 2, y + 2, x + 7, y + 8, rgb("#d8b08a"))
    l.rect(x + 2, y + 8, x + 7, y + 10, rgb(r.choice(("#23304a", "#4a2a2a", "#2a2a2a"))))
    l.rect(x + 2, y + 2, x + 7, y + 3, rgb(r.choice(("#e8e0d0", "#3a2a20", "#7a7a7a"))))


def _reloj(l, cx, cy):

    l.circulo(cx, cy, 8, rgb("#3a2f26"))
    l.circulo(cx, cy, 7, rgb("#f4f1e8"))

    for dx, dy in ((0, -6), (6, 0), (0, 6), (-6, 0)):

        l.px(cx + dx, cy + dy, NEGRO)

    l.linea(cx, cy, cx - 3, cy + 3, NEGRO)
    l.linea(cx, cy, cx, cy - 5, NEGRO)
    l.px(cx, cy, rgb("#c8322d"))


def _escudo(l, cx, cy):
    """Escudo nacional: ovalo celeste y blanco con el sol y laureles."""

    verde = rgb("#4a8a4a")

    l.elipse(cx - 8, cy - 7, cx + 8, cy + 8, verde)
    l.elipse(cx - 6, cy - 6, cx + 6, cy + 6, rgb("#f4f1e8"))
    l.elipse(cx - 5, cy - 5, cx + 5, cy + 1, CELESTE_ARG)
    l.rect(cx - 5, cy + 2, cx + 5, cy + 5, CELESTE_ARG)
    l.rect(cx - 5, cy - 1, cx + 5, cy + 1, rgb("#f4f1e8"))
    l.circulo(cx, cy - 5, 1, ORO)


def _afiche(l, x, y, r):
    """Afiche pegado en la pared."""

    col = r.choice((rgb("#c8322d"), rgb("#1f4a8f"), rgb("#e3b92f"), rgb("#2f7a4a")))

    l.rect(x, y, x + 11, y + 15, rgb("#f4f1e8"))
    l.rect(x + 1, y + 1, x + 10, y + 7, col)
    l.rect(x + 2, y + 9, x + 9, y + 9, rgb("#8a8a8a"))
    l.rect(x + 2, y + 11, x + 7, y + 11, rgb("#8a8a8a"))
    l.rect(x + 2, y + 13, x + 8, y + 13, rgb("#8a8a8a"))


def _matafuego(l, x, b):

    l.rect(x, b - 17, x + 3, b - 5, rgb("#c8322d"))
    l.rect(x + 1, b - 17, x + 1, b - 5, rgb("#e66a5a"))
    l.rect(x, b - 19, x + 3, b - 18, rgb("#23262c"))
    l.px(x + 4, b - 17, rgb("#23262c"))
    l.rect(x - 1, b - 8, x + 4, b - 8, rgb("#23262c"))


def _bandera_pared(l, x0, y0):
    """Bandera argentina colgada de la pared, con su asta."""

    ancho = 18

    l.rect(x0 - 1, y0, x0 + ancho, y0 + 1, ORO)
    l.rect(x0 - 2, y0 - 1, x0 - 2, y0 + 2, ORO)
    l.rect(x0 + ancho + 1, y0 - 1, x0 + ancho + 1, y0 + 2, ORO)

    celeste = CELESTE_ARG

    l.rect(x0, y0 + 2, x0 + ancho - 1, y0 + 12, celeste)
    l.rect(x0, y0 + 13, x0 + ancho - 1, y0 + 24, rgb("#f6f4ee"))
    l.rect(x0, y0 + 25, x0 + ancho - 1, y0 + 35, celeste)

    l.circulo(x0 + ancho // 2, y0 + 18, 3, ORO)
    l.circulo(x0 + ancho // 2, y0 + 18, 1, rgb("#f08a2e"))

    for x in range(x0 + 4, x0 + ancho, 6):

        l.rect(x, y0 + 3, x, y0 + 35, sombra(celeste, 0.88))

    l.rect(x0, y0 + 36, x0 + ancho - 1, y0 + 37, ORO)


def _casilleros(l, x0, cantidad, b, alto=46):
    """Una hilera de casilleros metalicos."""

    colores = (rgb("#5f7f9c"), rgb("#8a949e"))

    ancho = 8

    for i in range(cantidad):

        x = x0 + i * ancho

        c = colores[i % 2]

        top = b - alto

        l.rect(x, top, x + ancho - 1, b - 2, c)
        l.rect(x, top, x, b - 2, luz(c, 0.2))
        l.rect(x + ancho - 1, top, x + ancho - 1, b - 2, sombra(c, 0.6))

        for k in range(3):

            l.rect(x + 2, top + 4 + k * 3, x + ancho - 3, top + 4 + k * 3, sombra(c, 0.55))

        l.rect(x, top + 22, x + ancho - 1, top + 22, sombra(c, 0.6))

        for k in range(3):

            l.rect(x + 2, top + 26 + k * 3, x + ancho - 3, top + 26 + k * 3, sombra(c, 0.55))

        l.rect(x + ancho - 3, top + 18, x + ancho - 3, top + 20, rgb("#d6d8dc"))

    l.rect(x0, b - alto - 2, x0 + cantidad * ancho - 1, b - alto - 1, sombra(colores[0], 0.7))


def _banco(l, x, ancho, b):
    """Banco de madera de pasillo."""

    l.rect(x, b - 12, x + ancho - 1, b - 10, rgb("#8a6a3a"))
    l.rect(x, b - 12, x + ancho - 1, b - 12, rgb("#b08a58"))
    l.rect(x + 2, b - 9, x + 3, b - 3, rgb("#5a4020"))
    l.rect(x + ancho - 4, b - 9, x + ancho - 3, b - 3, rgb("#5a4020"))


# ----------------------------------------------------------
# cosas de taller
# ----------------------------------------------------------

def _torno(l, x, y):
    """Torno (silueta en la penumbra del taller). y = piso."""

    c = rgb("#6a727c")
    c_l = rgb("#8d96a0")
    c_o = rgb("#4a5058")

    l.rect(x, y - 7, x + 24, y - 5, c)
    l.rect(x, y - 7, x + 24, y - 7, c_l)
    l.rect(x + 2, y - 4, x + 4, y, c_o)
    l.rect(x + 20, y - 4, x + 22, y, c_o)

    l.rect(x, y - 15, x + 7, y - 8, c)
    l.rect(x, y - 15, x + 7, y - 15, c_l)
    l.circulo(x + 9, y - 11, 2, c_l)

    l.rect(x + 18, y - 12, x + 22, y - 8, c)
    l.rect(x + 10, y - 11, x + 17, y - 11, c_o)

    # lucecita amarilla
    l.px(x + 4, y - 12, rgb("#f2d65a"))


def _fresadora(l, x, y):
    """Fresadora (silueta). y = piso."""

    c = rgb("#6a727c")
    c_l = rgb("#8d96a0")
    c_o = rgb("#4a5058")

    l.rect(x, y - 4, x + 14, y, c_o)
    l.rect(x + 1, y - 22, x + 5, y - 4, c)
    l.rect(x + 1, y - 22, x + 1, y - 4, c_l)
    l.rect(x + 1, y - 24, x + 11, y - 20, c)
    l.rect(x + 8, y - 20, x + 9, y - 13, c_l)
    l.rect(x + 3, y - 9, x + 13, y - 8, c)


def _gabinete(l, x, ancho, b, r):
    """Gabinete electrico gris con luces."""

    alto = 46

    c = rgb("#8a949e")

    l.rect(x, b - alto, x + ancho - 1, b - 2, c)
    l.rect(x, b - alto, x, b - 2, luz(c, 0.25))
    l.rect(x + ancho - 1, b - alto, x + ancho - 1, b - 2, sombra(c, 0.6))
    l.rect(x, b - alto, x + ancho - 1, b - alto, luz(c, 0.3))

    # puerta con manija
    l.rect(x + 2, b - alto + 3, x + ancho - 3, b - 5, sombra(c, 0.9))
    l.rect(x + 2, b - alto + 3, x + ancho - 3, b - alto + 3, luz(c, 0.2))
    l.rect(x + ancho - 5, b - 24, x + ancho - 4, b - 21, rgb("#23262c"))

    # luces
    for k, col in enumerate(r.sample(("#d83a2a", "#3ad86a", "#f2d65a", "#d83a2a"), 3)):

        l.rect(x + 3 + k * 3, b - alto + 6, x + 4 + k * 3, b - alto + 7, rgb(col))

    # aviso
    if r.random() < 0.5:

        l.poly([(x + ancho // 2, b - 38), (x + ancho // 2 - 4, b - 31), (x + ancho // 2 + 4, b - 31)], rgb("#f2d65a"))
        l.px(x + ancho // 2, b - 34, NEGRO)
        l.px(x + ancho // 2, b - 36, NEGRO)


def _estante_libros(l, x0, x1, y0, filas, r):
    """Estantes con libros de colores."""

    madera = rgb("#4a3320")

    l.rect(x0, y0, x1, y0 + filas * 13 + 1, madera)

    cols = _col("#c8322d", "#1f4a8f", "#2f7a4a", "#e3b92f", "#7a3a8f", "#d8d0b8", "#8a4a2a")

    for f in range(filas):

        yb = y0 + 13 + f * 13

        x = x0 + 2

        while x < x1 - 3:

            a = r.choice((2, 2, 3))

            h = r.randint(8, 11)

            l.rect(x, yb - h, x + a - 1, yb - 1, r.choice(cols))

            x += a

            if r.random() < 0.1:
                x += 3

        l.rect(x0, yb, x1, yb + 1, rgb("#7a5a38"))


def _matraz(l, x, y, col):
    """Matraz de laboratorio con liquido. y = apoyo."""

    l.rect(x + 2, y - 11, x + 3, y - 7, rgb("#cfe0ea"))
    l.poly([(x + 2, y - 7), (x + 3, y - 7), (x + 6, y - 1), (x - 1, y - 1)], rgb("#cfe0ea"))
    l.poly([(x + 1, y - 4), (x + 4, y - 4), (x + 6, y - 1), (x - 1, y - 1)], col)
    l.px(x + 2, y - 12, rgb("#8a6a3a"))


def _tubos(l, x0, x1, y):
    """Dos caños horizontales con soportes y una valvula."""

    for k, dy in enumerate((0, 8)):

        l.rect(x0, y + dy, x1, y + dy + 3, ACERO)
        l.rect(x0, y + dy, x1, y + dy, luz(ACERO, 0.35))
        l.rect(x0, y + dy + 3, x1, y + dy + 3, sombra(ACERO, 0.6))

    for x in range(x0 + 8, x1 - 2, 24):

        l.rect(x, y - 3, x + 1, y + 13, rgb("#4a4f58"))

    vx = (x0 + x1) // 2

    l.rect(vx, y + 4, vx + 1, y + 7, rgb("#4a4f58"))
    l.circulo(vx, y + 9, 3, rgb("#c8322d"))
    l.circulo(vx, y + 9, 1, rgb("#4a4f58"))


def _engranaje(l, cx, cy, radio, col):

    l.circulo(cx, cy, radio, col)

    for k in range(8):

        ang = k * 3.14159 / 4

        dx = int(round((radio + 1) * np.cos(ang)))
        dy = int(round((radio + 1) * np.sin(ang)))

        l.rect(cx + dx - 1, cy + dy - 1, cx + dx + 1, cy + dy + 1, col)

    l.circulo(cx, cy, max(1, radio // 3), rgb("#2a2630"))


# ==========================================================
# LAS PARTES DE ARRIBA DE UN MODULO
# ==========================================================

def _zona_alta(l, c, r, especial=False):
    """
    Lo que queda arriba de las puertas: cuadros, reloj, escudo... y en los
    modulos medianos y grandes (que son mas altos) ventanas altas, un cartel
    con el lema o los caños del taller.

    Los modulos "especiales" ya traen su propio cartel y adornos arriba de la
    banda: ahi solo se dibuja lo de mas arriba (sin cuadros) y se deja aire.
    """

    w = l.w

    extra = l.h - BANDA

    if extra >= 20:

        modo = r.choice(("ventanas", "tubos", "ventanas", "ventanas"))

        if especial:
            extra -= 10

        if modo == "ventanas":

            n = max(1, (w - 8) // 28)

            av = max(10, min(20, (w - 8) // n - 8))

            for x in _posiciones(w, [av] * n, 4):

                # casi todas dan al cielo; alguna, al patio con su arbol
                _ventana(
                    l, x, x + av - 1, 3, extra + 8,
                    "patio" if r.random() < 0.3 else "cielo"
                )

        elif modo == "lema":

            frase = _texto_que_entra(("TRABAJO", "ESFUERZO", "TECNICA", "INDUSTRIA"), w - 36)

            tw = ancho_texto(frase)

            ancho_p = min(w - 8, tw * 2 + 20)

            x0 = (w - ancho_p) // 2

            fondo = c["guarda"]

            l.rect(x0, 6, x0 + ancho_p - 1, extra + 6, sombra(fondo, 0.7))
            l.rect(x0 + 1, 7, x0 + ancho_p - 2, extra + 5, fondo)
            l.rect(x0 + 1, 7, x0 + ancho_p - 2, 7, luz(fondo, 0.35))

            if tw * 2 + 8 <= ancho_p:

                l.texto((w - tw * 2) // 2, 6 + (extra - 8) // 2, frase, BLANCO, 2)

            else:

                l.texto((w - tw) // 2, 6 + (extra - 6) // 2, frase, BLANCO)

        else:

            _tubos(l, 2, w - 3, 6 + (extra - 16) // 2)

    if especial:
        return

    # cuadros y relojes en la parte de arriba de la banda de puertas
    y0 = extra

    ancho_adorno = {"cuadro": 10, "reloj": 17, "escudo": 17, "afiche": 12}

    cuantos = 1 if w < 64 else 2

    elegidos = [r.choice(("cuadro", "cuadro", "reloj", "escudo", "afiche")) for _ in range(cuantos)]

    for nombre, x in zip(elegidos, _posiciones(w, [ancho_adorno[n] for n in elegidos], 6)):

        if nombre == "cuadro":
            _cuadro(l, x, y0 + 8, r)
        elif nombre == "reloj":
            _reloj(l, x + 8, y0 + 16)
        elif nombre == "escudo":
            _escudo(l, x + 8, y0 + 16)
        else:
            _afiche(l, x, y0 + 6, r)


# ==========================================================
# LOS MODULOS
# ==========================================================

def _distribuir(w, patron):
    """
    Reparte puertas, ventanas y carteleras a lo ancho. Las puertas miden 16 y
    las carteleras 14; lo que sobra se lo reparten las ventanas.
    """

    fijos = {"puerta": 16, "cartelera": 14}

    n_vent = patron.count("ventana")

    ocupado = sum(fijos.get(p, 0) for p in patron)

    huecos = len(patron) + 1

    if n_vent:

        av = (w - 8 - ocupado - huecos * 3) // n_vent

        av = max(12, min(30, av))

    else:

        av = 0

    anchos = [fijos.get(p, av) for p in patron]

    return list(zip(patron, _posiciones(w, anchos, 4), anchos))


def _aula(l, c, r):

    w = l.w

    b = l.h - 1

    if w < 60:

        patron = r.choice((["ventana", "puerta"], ["puerta", "ventana"], ["puerta", "cartelera"]))

    elif w < 82:

        patron = r.choice((["ventana", "puerta", "ventana"], ["puerta", "ventana", "cartelera"], ["cartelera", "puerta", "ventana"]))

    else:

        patron = r.choice((
            ["ventana", "puerta", "cartelera", "ventana"],
            ["puerta", "ventana", "puerta", "cartelera"],
            ["ventana", "puerta", "ventana", "puerta"],
        ))

    for nombre, x, a in _distribuir(w, patron):

        if nombre == "puerta":

            _puerta(l, x, a, b, r, numero=r.choice(("1A", "1B", "2A", "2B", "3A", "3B", "4A", "5B", "6A", "7A")))

        elif nombre == "ventana":

            _ventana_aula(l, x, a, b, r)

        else:

            _cartelera(l, x, a, b, r)


def _taller_mecanico(l, c, r):

    w = l.w

    b = l.h - 1

    ax0 = 6
    ax1 = w - 7

    alto = 50

    # abertura del taller: marco de acero y adentro, la penumbra
    l.rect(ax0 - 2, b - alto - 2, ax1 + 2, b, rgb("#3f4a44"))
    l.rect(ax0, b - alto, ax1, b, rgb("#24242c"))

    ancho_int = ax1 - ax0 + 1

    # luz del taller
    l.rect(ax0 + 4, b - alto, ax1 - 4, b - alto + 1, rgb("#f2d65a"))

    if ancho_int >= 34:

        _torno(l, ax0 + 4, b - 2)

    if ancho_int >= 62:

        _fresadora(l, ax0 + 34, b - 2)

    # hoja corrediza del porton, cerrada sobre un costado
    ph = max(10, ancho_int * 2 // 5)

    verde = rgb("#4f7a5a")

    l.rect(ax1 - ph + 1, b - alto, ax1, b, verde)

    for xx in range(ax1 - ph + 3, ax1, 4):

        l.rect(xx, b - alto + 1, xx, b - 1, sombra(verde, 0.78))

    l.rect(ax1 - ph + 1, b - alto, ax1, b - alto + 1, luz(verde, 0.3))
    l.rect(ax1 - ph + 1, b - 14, ax1, b - 13, sombra(verde, 0.7))
    l.rect(ax1 - ph + 3, b - 26, ax1 - ph + 4, b - 22, rgb("#23262c"))

    # franja de peligro
    for k, xx in enumerate(range(0, w, 4)):

        l.rect(xx, b - 1, xx + 1, b, rgb("#e3b92f") if k % 2 == 0 else rgb("#23262c"))

    # cartel
    texto = _texto_que_entra(("TALLER MECANICO", "TALLER", "AJUSTE"), w - 8)

    _cartel(l, w // 2, b - alto - 14, texto, rgb("#1d3a2e"))

    if r.random() < 0.6 and ancho_int > 40:

        _matafuego(l, 2, b)


def _taller_electrico(l, c, r):

    w = l.w

    b = l.h - 1

    n = max(2, (w - 8) // 14)

    ancho_g = min(16, (w - 8) // n - 1)

    for x in _posiciones(w, [ancho_g] * n, 4):

        _gabinete(l, x, ancho_g, b, r)

    # bandeja de cables arriba, con cables que cuelgan
    l.rect(2, b - 52, w - 3, b - 50, rgb("#4a4f58"))
    l.rect(2, b - 52, w - 3, b - 52, rgb("#8d939c"))

    for x in _posiciones(w, [2] * n, 4):

        l.rect(x, b - 50, x, b - 46, rgb("#23262c"))

    texto = _texto_que_entra(("ELECTRICIDAD", "ELECTRO"), w - 8)

    _cartel(l, w // 2, b - 66, texto, rgb("#7a2a2a"), rgb("#ffe27a"))


def _modulo_casilleros(l, c, r):

    w = l.w

    b = l.h - 1

    n = max(2, (w - 8) // 8)

    x0 = (w - n * 8) // 2

    _casilleros(l, x0, n, b)

    _banco(l, x0 + 2, min(30, n * 8 - 4), b)

    if w >= 70 and r.random() < 0.7:

        _afiche(l, x0 + 4, b - 66, r)


def _biblioteca(l, c, r):

    w = l.w

    b = l.h - 1

    x0 = 5
    x1 = w - 6

    alto = 54

    l.rect(x0 - 2, b - alto - 2, x1 + 2, b, MADERA_O)

    _estante_libros(l, x0, x1, b - alto, 4, r)

    # mesa de lectura con lampara
    l.rect(x0 + 6, b - 11, x1 - 6, b - 9, rgb("#8a6a3a"))
    l.rect(x0 + 6, b - 11, x1 - 6, b - 11, rgb("#b08a58"))
    l.rect(x0 + 8, b - 8, x0 + 9, b - 2, rgb("#5a4020"))
    l.rect(x1 - 9, b - 8, x1 - 8, b - 2, rgb("#5a4020"))

    lx = (x0 + x1) // 2

    l.rect(lx, b - 18, lx, b - 12, rgb("#2f5d4a"))
    l.rect(lx - 3, b - 21, lx + 3, b - 19, rgb("#2f8a5a"))
    l.rect(lx - 1, b - 18, lx + 1, b - 17, rgb("#fff3b0"))

    texto = _texto_que_entra(("BIBLIOTECA", "LIBROS"), w - 8)

    _cartel(l, w // 2, b - alto - 15, texto, rgb("#3a2a1c"), rgb("#f2d65a"))


def _laboratorio(l, c, r):

    w = l.w

    b = l.h - 1

    # azulejos
    l.rect(4, b - 64, w - 5, b - 31, rgb("#e8ecee"))

    for x in range(4, w - 4, 6):

        l.rect(x, b - 64, x, b - 31, sombra(rgb("#e8ecee"), 0.9))

    for y in range(b - 64, b - 30, 6):

        l.rect(4, y, w - 5, y, sombra(rgb("#e8ecee"), 0.9))

    # mesada
    l.rect(2, b - 32, w - 3, b - 29, rgb("#7d858c"))
    l.rect(2, b - 32, w - 3, b - 32, luz(rgb("#7d858c"), 0.35))

    # matraces y tubos
    cols = _col("#4aa86a", "#4a8ad8", "#d8503a", "#d8b83a")

    for x in range(8, w - 14, 11):

        _matraz(l, x, b - 33, r.choice(cols))

    texto = _texto_que_entra(("LABORATORIO", "LAB"), w - 8)

    sw = ancho_texto(texto) + 8

    # tabla periodica (solo si queda lugar al lado del cartel)
    if w - sw - 10 >= 30:

        tx = w - 33

        l.rect(tx - 1, b - 84, tx + 28, b - 66, rgb("#5a5a5a"))

        for j in range(4):

            for i in range(9):

                l.rect(tx + i * 3, b - 83 + j * 4, tx + i * 3 + 1, b - 81 + j * 4, r.choice(cols + _col("#d8d0b8")))

        _cartel(l, 5 + sw // 2, b - 78, texto, rgb("#1f4a6a"))

    else:

        _cartel(l, w // 2, b - 78, texto, rgb("#1f4a6a"))


def _oficina(l, c, r):

    w = l.w

    b = l.h - 1

    nombre = r.choice(("DIRECCION", "SECRETARIA", "PRECEPTORIA"))

    anchos = [18, 22] if w >= 52 else [18]

    for k, (x, a) in enumerate(zip(_posiciones(w, anchos, 5), anchos)):

        if k == 0:

            # puerta de vidrio esmerilado
            l.rect(x, b - 52, x + a - 1, b, MADERA_O)
            l.rect(x + 2, b - 50, x + a - 3, b, MADERA)
            l.rect(x + 3, b - 48, x + a - 4, b - 22, rgb("#c8dce8"))
            l.rect(x + 3, b - 48, x + 5, b - 43, rgb("#eef6fa"))
            l.rect(x + a - 5, b - 27, x + a - 4, b - 24, ORO)

        else:

            # vitrina con copas
            l.rect(x, b - 54, x + a - 1, b - 2, MADERA_O)
            l.rect(x + 2, b - 52, x + a - 3, b - 4, rgb("#2a3a4a"))

            for yy in (b - 36, b - 20):

                l.rect(x + 2, yy, x + a - 3, yy, rgb("#8a6a3a"))

            for cx, yy in ((x + 6, b - 36), (x + 14, b - 36), (x + 10, b - 20)):

                l.rect(cx, yy - 7, cx + 3, yy - 5, ORO)
                l.rect(cx + 1, yy - 4, cx + 2, yy - 1, ORO)
                l.rect(cx - 1, yy - 1, cx + 4, yy - 1, ORO)

            l.rect(x + 2, b - 52, x + 4, b - 46, rgb("#5a7a9a"))

    texto = _texto_que_entra((nombre, "OFICINA"), w - 8)

    _cartel(l, w // 2, b - 68, texto, rgb("#4a3320"), rgb("#f2d65a"))


def _ventanal(l, c, r):

    w = l.w

    b = l.h - 1

    n = max(1, (w - 6) // 24)

    av = max(12, min(22, (w - 6) // n - 6))

    pilar = luz(c["pared"], 0.1)

    luces = []

    # en los modulos altos los ventanales suben hasta casi el techo
    arriba = max(3, b - 84 - max(0, l.h - BANDA - 8))

    for x in _posiciones(w, [av] * n, 3):

        _ventana(l, x, x + av - 1, arriba, b - 30, "patio")

        # pilastras a los costados
        l.rect(x - 3, arriba, x - 2, b - 28, pilar)
        l.rect(x + av + 2, arriba, x + av + 2, b - 28, sombra(pilar, 0.8))

        luces.append(x + av // 2)

    c["luces"] = luces


def _escalera(l, c, r):
    """La escalera del colegio: sube en diagonal por la pared, con baranda."""

    w = l.w

    b = l.h - 1

    x0 = 6
    x1 = w - 7

    pasos = (x1 - x0) // 4

    madera = rgb("#b08a58")
    contra = rgb("#6a4a2f")

    for k in range(pasos):

        x = x0 + k * 4

        alto = 3 + k * 2

        # la contrahuella (la parte de adelante de cada escalon) y la huella
        l.rect(x, b - alto - 2, x + 3, b - 2, contra if k % 2 == 0 else sombra(contra, 0.88))

        l.rect(x, b - alto - 2, x + 3, b - alto - 1, luz(madera, 0.1))
        l.rect(x, b - alto, x, b - 2, luz(contra, 0.18))

    # baranda
    for k in range(pasos + 1):

        x = x0 + k * 4

        alto = 3 + k * 2

        if k % 2 == 0:

            l.rect(x + 1, b - alto - 12, x + 1, b - alto - 3, rgb("#23262c"))

    l.linea(x0 + 1, b - 15, x0 + pasos * 4 - 3, b - 3 - (pasos - 1) * 2 - 12, rgb("#23262c"))

    # cartel
    _cartel(l, w // 2, b - 82, "PISO 1", rgb("#1f4a6a"))


def _salon_actos(l, c, r):

    w = l.w

    b = l.h - 1

    cx = w // 2

    # portones altos de dos hojas
    ancho_p = 28

    l.rect(cx - ancho_p // 2 - 2, b - 58, cx + ancho_p // 2 + 1, b, PIEDRA)

    rojo = rgb("#7a2f2a")

    for hoja in (0, 1):

        a = cx - ancho_p // 2 + hoja * (ancho_p // 2)

        l.rect(a, b - 56, a + ancho_p // 2 - 2, b, rojo)
        l.rect(a + 1, b - 55, a + 1, b, luz(rojo, 0.2))
        l.circulo(a + ancho_p // 4 - 1, b - 40, 3, rgb("#2a2630"))
        l.circulo(a + ancho_p // 4 - 1, b - 40, 2, rgb("#8fb4d8"))
        l.rect(a + 3, b - 28, a + ancho_p // 2 - 5, b - 4, sombra(rojo, 0.82))

    l.rect(cx, b - 56, cx, b, sombra(rojo, 0.5))

    # banderas a los costados
    if w >= 66:

        bandera(l, 9, b - 1, 44, 9, 6)
        bandera(l, w - 17, b - 1, 44, 9, 6)

    _escudo(l, cx, b - 70)

    texto = _texto_que_entra(("SALON DE ACTOS", "ACTOS"), w - 8)

    _cartel(l, cx, b - 90, texto, rgb("#4a2a2a"), rgb("#f2d65a"))


def _mural(l, c, r):
    """Mural de engranajes y circuitos en toda la pared."""

    w = l.w

    b = l.h - 1

    fondo = rgb(r.choice(("#2f4a6b", "#3a5a4a", "#6a3a4a")))

    l.rect(3, b - 82, w - 4, b - 28, fondo)
    l.rect(3, b - 82, w - 4, b - 82, luz(fondo, 0.3))
    l.marco(3, b - 82, w - 4, b - 28, sombra(fondo, 0.6))

    cols = _col("#f2d65a", "#e8e0d0", "#d8503a", "#8fc8f0")

    _engranaje(l, w // 3, b - 58, 11, r.choice(cols))

    if w >= 60:

        _engranaje(l, 2 * w // 3 + 2, b - 50, 7, r.choice(cols))

    # circuito: lineas con nodos
    y = b - 36

    l.rect(8, y, w - 9, y, rgb("#8fc8f0"))

    for x in range(12, w - 10, 14):

        l.rect(x, y - 4, x, y, rgb("#8fc8f0"))
        l.circulo(x, y - 5, 1, rgb("#f2d65a"))


ESTILOS = {
    "aula": _aula,
    "taller_mecanico": _taller_mecanico,
    "taller_electrico": _taller_electrico,
    "casilleros": _modulo_casilleros,
    "biblioteca": _biblioteca,
    "laboratorio": _laboratorio,
    "oficina": _oficina,
    "ventanal": _ventanal,
    "escalera": _escalera,
    "salon_actos": _salon_actos,
    "mural": _mural,
}

# Los que ya traen sus propios cuadros y adornos arriba
SIN_ADORNOS_ARRIBA = {"salon_actos", "mural", "escalera", "laboratorio"}


def fachada(estilo, ancho, cuerpo, r):
    """
    El frente de un modulo de pasillo: un lienzo de `ancho` x `cuerpo` (la
    ultima fila es el piso). Devuelve (lienzo, paleta); la paleta lleva el color
    de la pared y, en los ventanales, donde cae la luz sobre el piso.
    """

    c = _paleta(r)

    l = Lienzo(ancho, cuerpo)

    _pared(l, c)

    if estilo != "ventanal":

        _zona_alta(l, c, r, especial=estilo in SIN_ADORNOS_ARRIBA)

    ESTILOS[estilo](l, c, r)

    return l, c


# ==========================================================
# LUCES Y CHARCOS DE LUZ
# ==========================================================

def _resplandor(l, cx, cy, radio, color, alfa_max):
    """Resplandor redondo que se va transparentando hacia afuera."""

    lado = radio * 2 + 1

    yy, xx = np.mgrid[0:lado, 0:lado]

    d = np.sqrt((xx - radio) ** 2 + (yy - radio) ** 2) / radio

    a = np.clip(1.0 - d, 0.0, 1.0) ** 1.6 * alfa_max

    img = np.zeros((lado, lado, 4), np.uint8)

    img[..., 0] = color[0]
    img[..., 1] = color[1]
    img[..., 2] = color[2]
    img[..., 3] = np.clip(a, 0, 255).astype(np.uint8)

    l.pegar(Image.fromarray(img, "RGBA"), cx - radio, cy - radio)


def charco_de_luz(capa, cx, ancho_v, fila0=259, fila1=292, fuerza=0.30):
    """La luz de un ventanal sobre las baldosas: un trapecio claro que se va
    desvaneciendo hacia el frente."""

    x0 = max(0, cx - ancho_v - 14)
    x1 = min(capa.w, cx + ancho_v + 40)

    caja = (x0, fila0, x1, fila1)

    sub = np.array(capa.im.crop(caja)).astype(np.float32)

    for y in range(fila1 - fila0):

        t = y / max(1, fila1 - fila0)

        mitad = ancho_v / 2 + 10 * t

        centro = cx + 14 * t - x0

        a0 = int(centro - mitad)
        a1 = int(centro + mitad)

        f = fuerza * (1 - t * 0.8)

        for x in range(max(0, a0), min(sub.shape[1], a1)):

            borde = min(x - a0, a1 - x) / 3.0

            ff = f * min(1.0, borde)

            sub[y, x, :3] = sub[y, x, :3] * (1 - ff) + 255 * ff

    capa.im.paste(Image.fromarray(sub.astype(np.uint8), "RGBA"), (x0, fila0))


def luz_de_la_salida(capa, x_fin, fila0=259, fila1=312):
    """La luz que entra por el arco de salida: un charco claro sobre las
    baldosas, hacia el lado del pasillo."""

    a = np.array(capa.im).astype(np.float32)

    for y in range(fila0 + 1, fila1):

        t = (y - fila0) / (fila1 - fila0)

        largo = 38 + 40 * t

        for x in range(int(x_fin - largo), x_fin):

            if x < 4:
                continue

            fuerza = 0.30 * (1 - (x_fin - x) / largo)

            a[y, x, :3] = a[y, x, :3] * (1 - fuerza) + 255 * fuerza

    capa.im.paste(Image.fromarray(a.astype(np.uint8), "RGBA"))


# ==========================================================
# LAS CAPAS DE ATRAS: cielorraso, pared del fondo y galeria
# ==========================================================

MADERA_OSC = rgb("#4a3828")
MADERA_MEDIA = rgb("#7a5a3a")

# Fila (de la capa del cielo) donde termina el cielorraso y empieza la pared
TECHO_CIELO = 46

# Fila (de la capa lejana) donde empieza la pared del fondo
PARED_LEJOS = 52

# Fila (de la capa del medio) donde arranca la galeria de arcos
GALERIA_TOPE = 74


def capa_cielo(W, H):
    """El cielorraso alto del colegio: vigas de madera, claraboyas y la
    cornisa; abajo, la pared alta. (Arriba de todo el color se estira.)"""

    l = Lienzo(W, H)

    techo_osc = rgb("#3a2c22")
    techo_med = rgb("#8a7556")

    pared_a = rgb("#d4c8a8")
    pared_b = rgb("#ece2c4")

    for y in range(H):

        if y < TECHO_CIELO:

            c = mezcla(techo_osc, techo_med, y / TECHO_CIELO)

        else:

            c = mezcla(pared_a, pared_b, (y - TECHO_CIELO) / (H - TECHO_CIELO))

        l.rect(0, y, W - 1, y, c)

    paso = 64

    for x in range(-20, W + paso, paso):

        # la viga
        l.rect(x, 0, x + 5, TECHO_CIELO - 1, MADERA_OSC)
        l.rect(x, 0, x, TECHO_CIELO - 1, luz(MADERA_OSC, 0.25))
        l.rect(x + 5, 0, x + 5, TECHO_CIELO - 1, sombra(MADERA_OSC, 0.6))

        # la claraboya entre vigas
        a = x + 12
        z = x + paso - 8

        l.rect(a - 1, 7, z + 1, TECHO_CIELO - 8, MADERA_OSC)

        for y in range(8, TECHO_CIELO - 8):

            t = (y - 8) / (TECHO_CIELO - 16)

            l.rect(a, y, z, y, mezcla(rgb("#bfe0f2"), rgb("#f6fcff"), t))

        for xx in range(a + 9, z, 10):

            l.rect(xx, 8, xx, TECHO_CIELO - 9, MADERA_OSC)

        l.rect(a, (8 + TECHO_CIELO - 9) // 2, z, (8 + TECHO_CIELO - 9) // 2, MADERA_OSC)

    # cornisa: donde el cielorraso se encuentra con la pared
    l.rect(0, TECHO_CIELO, W - 1, TECHO_CIELO + 2, MADERA_MEDIA)
    l.rect(0, TECHO_CIELO, W - 1, TECHO_CIELO, luz(MADERA_MEDIA, 0.3))
    l.rect(0, TECHO_CIELO + 3, W - 1, TECHO_CIELO + 5, sombra(rgb("#d4c8a8"), 0.75))

    return l


def capa_lejos(W, H, r):
    """La pared del fondo del gran hall: ventanales altos con arco que dan al
    patio, pilastras y la guarda verde. Se ve con bruma."""

    l = Lienzo(W, H)

    pared_a = rgb("#cdbf9e")
    pared_b = rgb("#e0d5b6")

    top = PARED_LEJOS

    for y in range(top, H):

        l.rect(0, y, W - 1, y, mezcla(pared_a, pared_b, (y - top) / (H - top)))

    # guarda verde abajo
    l.rect(0, 148, W - 1, H - 1, rgb("#35604a"))
    l.rect(0, 146, W - 1, 147, luz(pared_b, 0.2))
    l.rect(0, 148, W - 1, 148, luz(rgb("#35604a"), 0.3))

    paso = 56

    aw = 24

    for x in range(10, W, paso):

        _ventana(l, x, x + aw - 1, top + 24, top + 92, "patio")

        # pilastras a los costados
        l.rect(x - 6, top + 8, x - 4, 146, luz(pared_b, 0.14))
        l.rect(x + aw + 3, top + 8, x + aw + 4, 146, sombra(pared_a, 0.8))

    # cornisa de madera arriba
    l.rect(0, top, W - 1, top + 4, MADERA_MEDIA)
    l.rect(0, top, W - 1, top, luz(MADERA_MEDIA, 0.3))
    l.rect(0, top + 5, W - 1, top + 6, sombra(pared_a, 0.7))

    l.bruma(rgb("#e8dfc4"), 0.22)

    return l


def capa_medio(W, H, r):
    """La galeria: una arcada de piedra con pilares, y colgando de la viga
    maestra los tubos fluorescentes del hall."""

    l = Lienzo(W, H)

    piedra = rgb("#c9bd9f")

    piedra_l = luz(piedra, 0.22)
    piedra_o = sombra(piedra, 0.7)

    top = GALERIA_TOPE

    # viga maestra (de la que cuelgan las lamparas)
    l.rect(0, 0, W - 1, 5, MADERA_OSC)
    l.rect(0, 0, W - 1, 0, luz(MADERA_OSC, 0.3))
    l.rect(0, 5, W - 1, 5, sombra(MADERA_OSC, 0.6))

    # pilares
    xs = []

    x = -6

    while x < W + 80:

        xs.append(x)

        x += 9 + r.randint(54, 74)

    for a, b_ in zip(xs, xs[1:]):

        bx0 = a + 9
        bx1 = b_ - 1

        radio = (bx1 - bx0 + 1) / 2.0

        cx = (bx0 + bx1) / 2.0

        y_corona = top + 14

        y_arranque = int(y_corona + radio)

        # el tímpano: piedra arriba del arco
        for xx in range(bx0, bx1 + 1):

            dx = xx - cx

            dy = int(round((radio * radio - dx * dx) ** 0.5)) if abs(dx) < radio else 0

            y_abajo = y_arranque - dy

            l.rect(xx, top, xx, y_abajo - 1, piedra)

            # moldura clara en el borde del arco
            l.rect(xx, y_abajo - 2, xx, y_abajo - 1, piedra_l)

        # pendientes del vano de abajo del arranque: libre

        # lampara colgante (tubo fluorescente): cable desde la viga
        if r.random() < 0.7:

            lx = int(cx + r.randint(-10, 10))

            largo = r.randint(64, 76)

            l.rect(lx - 7, 6, lx - 7, largo, rgb("#4a4f58"))
            l.rect(lx + 7, 6, lx + 7, largo, rgb("#4a4f58"))

            _resplandor(l, lx, largo + 2, 22, rgb("#fff4c8"), 90)

            l.rect(lx - 11, largo, lx + 11, largo + 2, rgb("#8d939c"))
            l.rect(lx - 10, largo + 1, lx + 10, largo + 1, rgb("#fffbe8"))

    for a in xs:

        l.rect(a, top, a + 8, H - 1, piedra)
        l.rect(a, top, a, H - 1, piedra_l)
        l.rect(a + 8, top, a + 8, H - 1, piedra_o)
        l.rect(a + 3, top + 14, a + 3, H - 1, sombra(piedra, 0.9))

        # capitel y base
        l.rect(a - 2, top + 8, a + 10, top + 13, piedra_l)
        l.rect(a - 2, top + 13, a + 10, top + 13, piedra_o)
        l.rect(a - 1, 150, a + 9, 153, piedra_o)

    # cornisa de la galeria
    l.rect(0, top - 3, W - 1, top - 1, luz(piedra, 0.3))
    l.rect(0, top, W - 1, top, piedra_o)

    # un toque calido: la luz de los tubos
    return l

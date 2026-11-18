"""
NIVEL 19 - VILLA LUGANO

    * Autodromo Oscar y Juan Galvez: tribunas, torre de control y la
      bandera a cuadros
    * Conjunto de monobloques de Villa Lugano (el barrio de edificios
      largos de hormigon, de los anos 70)
    * Reserva Ecologica Lago Lugano: la laguna con juncos y un mirador
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import cartel_nombre, pasto


def autodromo():

    ancho = 196
    alto = 112

    l = Lienzo(ancho, alto)

    base = alto - 1

    hormigon = rgb("#b9b8b2")

    # tribunas: gradas con butacas de colores
    volumen(l, 4, base - 40, 134, base, hormigon, 1, 3)

    for i, y in enumerate(range(base - 36, base - 6, 5)):

        l.rect(6, y, 132, y + 2, sombra(hormigon, 0.78))

        for x in range(8 + (i % 2) * 3, 130, 6):

            l.rect(x, y - 1, x + 2, y, [ROJO, AZUL_BOCA, AMARILLO_BOCA, BLANCO][(x // 6 + i) % 4])

    # techo de la tribuna, volado
    l.rect(0, base - 50, 140, base - 44, rgb("#7a8088"))
    l.rect(0, base - 50, 140, base - 50, luz(rgb("#7a8088"), 0.35))

    for x in range(8, 138, 20):

        l.rect(x, base - 44, x + 1, base - 38, rgb("#4a5058"))

    cartel_nombre(l, 70, base - 62, "AUTODROMO GALVEZ", rgb("#1d1a24"), rgb("#ffe27a"))

    # torre de control
    tx = 160

    l.rect(tx - 5, base - 78, tx + 5, base, hormigon)
    l.rect(tx - 5, base - 78, tx - 5, base, luz(hormigon, 0.2))
    l.rect(tx + 4, base - 78, tx + 5, base, sombra(hormigon, 0.75))

    for y in range(base - 70, base - 8, 14):

        l.rect(tx - 3, y, tx + 3, y + 5, VIDRIO)

    # cabina de vidrio arriba
    l.rect(tx - 14, base - 96, tx + 14, base - 78, rgb("#4a5058"))
    l.rect(tx - 12, base - 94, tx + 12, base - 82, VIDRIO)
    l.rect(tx - 12, base - 94, tx + 12, base - 93, VIDRIO_LUZ)

    for x in range(tx - 8, tx + 12, 7):

        l.rect(x, base - 94, x, base - 82, rgb("#4a5058"))

    l.rect(tx - 15, base - 98, tx + 15, base - 96, rgb("#c8322d"))

    # antena y bandera a cuadros
    l.rect(tx, base - 112, tx, base - 98, rgb("#cfcfcf"))

    for j in range(3):

        for i in range(5):

            l.rect(tx + 1 + i * 2, base - 111 + j * 2, tx + 2 + i * 2, base - 110 + j * 2,
                   BLANCO if (i + j) % 2 == 0 else NEGRO)

    # el piso con cuadros (linea de llegada)
    for x in range(0, ancho, 6):

        l.rect(x, base - 2, x + 2, base - 1, BLANCO)
        l.rect(x + 3, base - 2, x + 5, base - 1, NEGRO)
        l.rect(x, base, x + 2, base, NEGRO)
        l.rect(x + 3, base, x + 5, base, BLANCO)

    return l


def monobloques():

    ancho = 170
    alto = 128

    l = Lienzo(ancho, alto)

    base = alto - 1

    pasteles = [rgb("#e8c46a"), rgb("#d86a5a"), rgb("#6aa8c8"), rgb("#8cc08a")]

    bloques = [(6, 54, 112), (60, 100, 96), (106, 164, 120)]

    for k, (a, b, h) in enumerate(bloques):

        hormigon = rgb(["#c4beb0", "#b8b8b0", "#c8c0b4"][k])

        volumen(l, a, base - h, b, base, hormigon, 1, 3)

        # franjas de pisos con balcones de colores
        for j, y in enumerate(range(base - h + 6, base - 10, 12)):

            for x in range(a + 5, b - 5, 8):

                l.rect(x, y, x + 3, y + 6, VIDRIO)
                l.px(x, y, VIDRIO_LUZ)

            l.rect(a + 2, y + 8, b - 2, y + 9, pasteles[(j + k) % 4])

        # escalera vertical (franja oscura) y azotea con tanques
        l.rect((a + b) // 2 - 1, base - h, (a + b) // 2 + 1, base, sombra(hormigon, 0.7))

        l.rect(a + 4, base - h - 5, a + 14, base - h, rgb("#9aa0a8"))
        l.rect(b - 14, base - h - 5, b - 4, base - h, rgb("#9aa0a8"))

    pasto(l, 0, ancho - 1, base, rgb("#6a9a4a"))

    return l


def lago_lugano():

    ancho = 160
    alto = 100

    l = Lienzo(ancho, alto)

    base = alto - 1

    # la laguna
    agua = rgb("#4f9ad0")

    l.elipse(4, base - 30, ancho - 5, base + 14, rgb("#3a7ab0"))
    l.elipse(8, base - 27, ancho - 9, base + 10, agua)

    for x, y in ((30, base - 16), (60, base - 10), (96, base - 18), (120, base - 8)):

        l.rect(x, y, x + 10, y, luz(agua, 0.4))

    # orilla de pasto
    l.rect(0, base - 3, ancho - 1, base, rgb("#4f8f3f"))

    # juncos
    for x in range(8, 60, 5):

        h = 14 + (x * 7) % 10

        l.rect(x, base - 4 - h, x, base - 3, rgb("#7a9a3a"))
        l.rect(x + 1, base - 4 - h + 3, x + 1, base - 3, rgb("#5a7a2a"))
        l.rect(x - 1, base - 4 - h, x, base - 4 - h + 3, rgb("#8a5a2a"))

    # mirador de madera (torre sobre patas)
    mx = 118

    madera = rgb("#8a5a32")

    for dx in (-10, 10):

        l.rect(mx + dx - 1, base - 52, mx + dx + 1, base - 3, madera)

    l.linea(mx - 10, base - 6, mx + 10, base - 36, sombra(madera, 0.8))
    l.linea(mx + 10, base - 6, mx - 10, base - 36, sombra(madera, 0.8))

    l.rect(mx - 15, base - 56, mx + 15, base - 50, madera)
    l.rect(mx - 15, base - 56, mx + 15, base - 56, luz(madera, 0.3))

    # baranda y techito
    reja(l, mx - 14, mx + 14, base - 66, 8, sombra(madera, 0.85), 3)

    l.poly([(mx - 18, base - 66), (mx, base - 80), (mx + 18, base - 66)], rgb("#a9472f"))

    # escalera
    for i in range(8):

        l.rect(mx + 4 + i, base - 4 - i * 6, mx + 8 + i, base - 3 - i * 6, madera)

    # pajaros (garzas)
    for x, y in ((20, base - 30), (70, base - 38)):

        l.px(x, y, BLANCO)
        l.px(x + 1, y + 1, BLANCO)
        l.px(x + 2, y, BLANCO)
        l.px(x - 1, y + 1, BLANCO)

    arbol(l, 80, base - 3, 46, "sauce", seed=7)

    return l


MONUMENTOS = [
    dict(id="autodromo", nombre="Autodromo Oscar y Juan Galvez", fn=autodromo),
    dict(id="monobloques_lugano", nombre="Monobloques de Villa Lugano", fn=monobloques),
    dict(id="lago_lugano", nombre="Reserva Ecologica Lago Lugano", fn=lago_lugano),
]

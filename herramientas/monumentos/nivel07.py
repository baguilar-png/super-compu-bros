"""
NIVEL 7 - BARRIO NORTE

    * El Ateneo Grand Splendid (ex teatro, hoy libreria, Av. Santa Fe)
    * Palais de Glace (palacio con cupula)
    * Facultad de Medicina de la UBA (gran portico de columnas)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# EL ATENEO GRAND SPLENDID
# ==========================================================

def ateneo():

    ancho = 140
    alto = 112

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    crema = rgb("#e8d6ab")
    ocre = rgb("#b99a62")
    zinc = rgb("#6a7280")

    # mansarda de zinc
    l.poly([(8, base - 80), (18, base - 94), (ancho - 19, base - 94), (ancho - 9, base - 80)], zinc)

    l.rect(18, base - 94, ancho - 19, base - 94, luz(zinc, 0.3))

    for x in range(24, ancho - 24, 14):

        l.rect(x, base - 90, x + 6, base - 83, crema)
        l.rect(x + 1, base - 89, x + 5, base - 84, VIDRIO)
        l.poly([(x - 1, base - 90), (x + 3, base - 94), (x + 7, base - 90)], crema)

    # cuerpo
    volumen(l, 10, base - 80, ancho - 11, base, crema, 1, 3)

    cornisa(l, 10, ancho - 11, base - 82, luz(crema, 0.3))

    # pilastras
    for x in (14, 40, cx - 2, ancho - 44, ancho - 18):
        l.rect(x, base - 76, x + 3, base - 26, luz(crema, 0.25))
        l.rect(x + 3, base - 76, x + 3, base - 26, sombra(crema, 0.85))

    # ventanas altas con arco (los palcos del ex teatro)
    for x in (22, 30, 48, 56, ancho - 38, ancho - 30, ancho - 60, ancho - 52):

        ventana_arco(l, x, base - 32, x + 4, 30, VIDRIO, ocre)

    # gran arco central con vitral
    ventana_arco(l, cx - 15, base - 24, cx + 14, 50, rgb("#7a2f3a"), ocre, brillo=None)

    for dx in range(-12, 13, 4):
        l.rect(cx + dx, base - 70, cx + dx, base - 25, rgb("#d4a82a"))

    for y in range(base - 68, base - 26, 8):
        l.rect(cx - 13, y, cx + 12, y, rgb("#d4a82a"))

    # cartel
    texto = "EL ATENEO"

    w = ancho_texto(texto)

    l.rect(cx - w // 2 - 4, base - 22, cx + w // 2 + 3, base - 12, rgb("#3a1a1a"))
    l.marco(cx - w // 2 - 4, base - 22, cx + w // 2 + 3, base - 12, ORO)

    l.texto(cx - w // 2, base - 20, texto, rgb("#f4e7a3"))

    # marquesina de entrada
    l.rect(cx - 24, base - 26, cx + 24, base - 24, rgb("#7a2f3a"))

    for x in range(cx - 22, cx + 23, 4):
        l.rect(x, base - 24, x + 1, base - 22, rgb("#f4e7a3"))

    # puertas
    for dx in (-18, 12):

        l.rect(cx + dx, base - 10, cx + dx + 6, base, rgb("#3a2518"))
        l.rect(cx + dx + 1, base - 9, cx + dx + 5, base - 2, rgb("#e7c22b"))

    # vidrieras de la planta baja
    for x in (14, 24, ancho - 34, ancho - 24):

        l.rect(x, base - 14, x + 7, base - 2, rgb("#2f3a4a"))
        l.rect(x + 1, base - 13, x + 6, base - 3, rgb("#e7c22b"))

        for k in range(3):
            l.rect(x + 1, base - 12 + k * 4, x + 6, base - 12 + k * 4, rgb("#7a4a2a"))

    # baldosas de la vereda
    return l


# ==========================================================
# PALAIS DE GLACE
# ==========================================================

def palais_de_glace():

    ancho = 128
    alto = 106

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    crema = rgb("#efe5cc")
    gris = rgb("#7a8590")

    # cupula central con tambor
    l.rect(cx - 14, base - 84, cx + 14, base - 62, crema)
    l.rect(cx - 14, base - 84, cx - 14, base - 62, luz(crema, 0.2))
    l.rect(cx + 10, base - 84, cx + 14, base - 62, sombra(crema, 0.86))

    for dx in (-8, -2, 4, 10):
        ventana_arco(l, cx + dx - 2, base - 66, cx + dx, 12, rgb("#2f4a60"), rgb("#bfae86"))

    cupula(l, cx, base - 84, 17, 16, gris, costillas=7, linterna=True, remate=ORO)

    # cuerpo principal
    volumen(l, 10, base - 62, ancho - 11, base, crema, 1, 3)

    cornisa(l, 10, ancho - 11, base - 64, luz(crema, 0.3))

    # balaustrada
    for x in range(12, ancho - 12, 3):
        l.rect(x, base - 69, x, base - 65, luz(crema, 0.3))

    l.rect(10, base - 70, ancho - 11, base - 70, luz(crema, 0.3))

    # jarrones en las esquinas
    for x in (14, ancho - 17):
        l.rect(x, base - 76, x + 3, base - 71, rgb("#d6c9a8"))

    # portico central con columnas pareadas
    for dx in (-18, -12, 12, 18):

        columnas(l, cx + dx, cx + dx, base - 50, base - 6, 1, 4, luz(crema, 0.2))

    l.rect(cx - 22, base - 56, cx + 22, base - 51, luz(crema, 0.25))
    l.rect(cx - 22, base - 51, cx + 22, base - 51, sombra(crema, 0.8))

    # puerta central y ventanas
    ventana_arco(l, cx - 8, base - 6, cx + 8, 38, VIDRIO, rgb("#bfae86"))

    for x in range(cx - 7, cx + 8, 3):
        l.rect(x, base - 40, x, base - 7, VIDRIO_OSC)

    for x in (20, 30, 40, ancho - 46, ancho - 36, ancho - 26):

        ventana_arco(l, x, base - 8, x + 5, 20, VIDRIO, rgb("#bfae86"))
        ventana_arco(l, x, base - 36, x + 5, 16, VIDRIO, rgb("#bfae86"))

    # escalinata
    for i in range(4):
        l.rect(cx - 24 - i * 2, base - 3 + i, cx + 24 + i * 2, base - 3 + i,
               rgb("#e0d8c8") if i % 2 == 0 else rgb("#c4bba8"))

    return l


# ==========================================================
# FACULTAD DE MEDICINA
# ==========================================================

def facultad_medicina():

    ancho = 224
    alto = 96

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    piedra = rgb("#d4cfc4")

    # alas
    volumen(l, 4, base - 56, ancho - 5, base, piedra, 1, 3)

    cornisa(l, 4, ancho - 5, base - 58, luz(piedra, 0.25))

    l.rect(4, base - 62, ancho - 5, base - 59, sombra(piedra, 0.9))

    for x in range(8, ancho - 8, 3):
        l.rect(x, base - 62, x, base - 59, luz(piedra, 0.12))

    # ventanas rectangulares en tres pisos
    for x in list(range(10, cx - 50, 9)) + list(range(cx + 50, ancho - 10, 9)):

        for y in (base - 48, base - 33, base - 18):
            l.rect(x - 1, y - 1, x + 5, y + 8, luz(piedra, 0.3))
            l.rect(x, y, x + 4, y + 7, VIDRIO)
            l.px(x, y, VIDRIO_LUZ)

    # cuerpo central avanzado
    volumen(l, cx - 46, base - 66, cx + 46, base, rgb("#cdc7ba"), 1, 3, techo=False)

    # entablamento + friso con la leyenda
    l.rect(cx - 52, base - 80, cx + 52, base - 66, luz(piedra, 0.2))
    l.rect(cx - 52, base - 80, cx + 52, base - 80, rgb("#ffffff"))
    l.rect(cx - 52, base - 66, cx + 52, base - 66, sombra(piedra, 0.75))

    texto = "MEDICINA"

    w = ancho_texto(texto)

    l.texto(cx - w // 2, base - 76, texto, rgb("#7a7468"))

    for x in range(cx - 50, cx + 51, 6):
        l.rect(x, base - 70, x, base - 67, sombra(piedra, 0.88))

    # cornisa de remate
    l.rect(cx - 54, base - 84, cx + 54, base - 81, sombra(piedra, 0.86))
    l.rect(cx - 54, base - 84, cx + 54, base - 84, luz(piedra, 0.3))

    # gran columnata: seis columnas gigantes
    columnas(l, cx - 40, cx + 40, base - 64, base - 6, 6, 7, luz(piedra, 0.18))

    # puertas de entrada entre columnas
    for dx in (-24, 0, 24):

        l.rect(cx + dx - 6, base - 34, cx + dx + 6, base - 6, rgb("#2c3340"))
        l.rect(cx + dx - 5, base - 33, cx + dx + 5, base - 7, rgb("#3a4660"))
        l.rect(cx + dx, base - 33, cx + dx, base - 7, rgb("#2c3340"))

    # escalinata ancha
    for i in range(5):
        l.rect(cx - 52 - i * 2, base - 5 + i, cx + 52 + i * 2, base - 5 + i,
               rgb("#e0d8c8") if i % 2 == 0 else rgb("#c4bba8"))

    # bandera
    bandera(l, cx, base - 84, 16, ancho=12, alto=7)

    return l


MONUMENTOS = [
    dict(id="ateneo_grand_splendid", nombre="El Ateneo Grand Splendid", fn=ateneo),
    dict(id="palais_de_glace", nombre="Palais de Glace", fn=palais_de_glace),
    dict(id="facultad_medicina", nombre="Facultad de Medicina (UBA)", fn=facultad_medicina),
]

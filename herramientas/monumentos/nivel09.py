"""
NIVEL 9 - ABASTO

    * Abasto Shopping (ex Mercado de Abasto, art deco de hormigon, 1934)
    * Monumento a Carlos Gardel (el Morocho del Abasto)
    * Casa Museo Carlos Gardel (casa chorizo con el mural)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# ABASTO SHOPPING (EX MERCADO DE ABASTO)
# ==========================================================

def abasto_shopping():

    ancho = 232
    alto = 108

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    hormigon = rgb("#d6d1c4")
    oscuro = rgb("#8f8a7e")

    # cuerpo largo con pilares verticales
    volumen(l, 4, base - 62, ancho - 5, base, hormigon, 1, 3)

    for x in range(10, ancho - 8, 12):

        l.rect(x, base - 62, x + 3, base, luz(hormigon, 0.2))
        l.rect(x + 3, base - 62, x + 3, base, sombra(hormigon, 0.82))

        # ventanas verticales entre pilares
        l.rect(x + 5, base - 56, x + 8, base - 14, rgb("#3b5a86"))
        l.rect(x + 5, base - 56, x + 5, base - 14, VIDRIO_LUZ)

        for y in range(base - 52, base - 14, 8):
            l.rect(x + 5, y, x + 8, y, rgb("#27405f"))

    # cornisa escalonada (art deco)
    for i, w in enumerate((ancho - 8, ancho - 24, ancho - 44)):

        x0 = cx - w // 2

        y = base - 62 - i * 5

        l.rect(x0, y - 4, x0 + w - 1, y, hormigon)
        l.rect(x0, y - 4, x0 + w - 1, y - 4, luz(hormigon, 0.3))
        l.rect(x0 + w - 3, y - 4, x0 + w - 1, y, sombra(hormigon, 0.82))

    # gran arco central parabolico de hormigon (el portal del mercado)
    for k in range(5):

        l.semi(cx, base - 4, 31 - k * 3, 62 - k * 3 + 10, [hormigon, oscuro][k % 2] if k < 2 else VIDRIO)

    l.rect(cx - 31, base - 4, cx + 31, base, hormigon)

    # vidrio del portal
    l.semi(cx, base - 8, 18, 50, rgb("#3b5a86"))

    for dx in range(-16, 17, 4):
        l.rect(cx + dx, base - 8 - int(48 * math.sqrt(max(0, 1 - (dx / 18) ** 2))), cx + dx, base - 8, rgb("#27405f"))

    for y in range(base - 14, base - 58, -8):
        l.rect(cx - 17, y, cx + 17, y, rgb("#27405f"))

    # puertas
    l.rect(cx - 8, base - 12, cx + 8, base - 4, rgb("#1f2a3a"))

    l.rect(cx, base - 12, cx, base - 4, rgb("#3b5a86"))

    # letrero luminoso ABASTO
    texto = "ABASTO"

    w = ancho_texto(texto, 2)

    l.rect(cx - w // 2 - 4, base - 100, cx + w // 2 + 3, base - 83, rgb("#1f1a24"))
    l.marco(cx - w // 2 - 4, base - 100, cx + w // 2 + 3, base - 83, rgb("#e7c22b"))

    l.texto(cx - w // 2, base - 97, texto, rgb("#ffd84a"), 2)

    # escalones laterales (torrecitas art deco)
    for x0 in (4, ancho - 24):

        l.rect(x0, base - 78, x0 + 19, base - 62, hormigon)
        l.rect(x0, base - 78, x0 + 19, base - 78, luz(hormigon, 0.3))
        l.rect(x0 + 17, base - 78, x0 + 19, base - 62, sombra(hormigon, 0.82))

        l.rect(x0 + 5, base - 74, x0 + 8, base - 66, rgb("#3b5a86"))
        l.rect(x0 + 11, base - 74, x0 + 14, base - 66, rgb("#3b5a86"))

    return l


# ==========================================================
# MONUMENTO A GARDEL
# ==========================================================

def estatua_gardel():

    ancho = 64
    alto = 84

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = 30

    piedra = rgb("#bdb7a8")
    bronce = rgb("#8a6a3a")
    patina = rgb("#6c8a74")

    # pedestal de piedra
    for i in range(2):
        l.rect(cx - 15 + i * 2, base - i * 4 - 3, cx + 15 - i * 2, base - i * 4, piedra if i == 0 else luz(piedra, 0.15))

    volumen(l, cx - 10, base - 28, cx + 10, base - 8, piedra, 1, 3)

    l.rect(cx - 12, base - 31, cx + 12, base - 28, luz(piedra, 0.2))

    # placa
    l.rect(cx - 6, base - 22, cx + 6, base - 15, rgb("#6a5a2a"))
    l.marco(cx - 6, base - 22, cx + 6, base - 15, ORO)

    for x in range(cx - 4, cx + 5, 2):
        l.rect(x, base - 19, x, base - 18, ORO)

    # estatua: traje, bufanda y sombrero
    y0 = base - 32

    # piernas
    l.rect(cx - 4, y0 - 12, cx - 1, y0, patina)
    l.rect(cx + 1, y0 - 12, cx + 4, y0, patina)
    l.rect(cx - 5, y0 - 1, cx - 1, y0, sombra(patina, 0.7))
    l.rect(cx + 1, y0 - 1, cx + 5, y0, sombra(patina, 0.7))

    # saco
    l.rect(cx - 6, y0 - 28, cx + 6, y0 - 11, patina)
    l.rect(cx - 6, y0 - 28, cx - 6, y0 - 11, luz(patina, 0.25))
    l.rect(cx + 5, y0 - 28, cx + 6, y0 - 11, sombra(patina, 0.8))

    # solapa y camisa
    l.rect(cx - 1, y0 - 27, cx + 1, y0 - 18, rgb("#d6e0d8"))
    l.rect(cx, y0 - 27, cx, y0 - 18, rgb("#8a9a90"))

    # bufanda
    l.rect(cx - 5, y0 - 28, cx + 5, y0 - 26, rgb("#a8b8ac"))

    # brazo levantado saludando
    l.linea(cx + 6, y0 - 26, cx + 11, y0 - 33, patina)
    l.linea(cx + 7, y0 - 26, cx + 12, y0 - 33, sombra(patina, 0.8))
    l.rect(cx + 11, y0 - 35, cx + 13, y0 - 33, luz(patina, 0.3))

    # brazo caido
    l.rect(cx - 8, y0 - 25, cx - 6, y0 - 13, sombra(patina, 0.9))

    # cabeza sonriente
    l.elipse(cx - 4, y0 - 38, cx + 4, y0 - 29, luz(patina, 0.2))

    l.px(cx - 2, y0 - 34, NEGRO)
    l.px(cx + 2, y0 - 34, NEGRO)
    l.rect(cx - 2, y0 - 31, cx + 2, y0 - 31, rgb("#f4f1e8"))

    # sombrero de ala corta
    l.rect(cx - 7, y0 - 39, cx + 7, y0 - 38, sombra(patina, 0.7))
    l.rect(cx - 4, y0 - 44, cx + 4, y0 - 39, sombra(patina, 0.8))
    l.rect(cx - 4, y0 - 41, cx + 4, y0 - 41, rgb("#4a5a50"))

    # banco y farol tangueros
    banco(l, 46, base, 14, rgb("#3a3a3a"))

    farola(l, 3, base, 34, c=rgb("#1f2a2a"))

    return l


# ==========================================================
# CASA MUSEO GARDEL
# ==========================================================

def casa_museo_gardel():

    ancho = 150
    alto = 100

    l = Lienzo(ancho, alto)

    base = alto - 1

    amarillo = rgb("#ecc96a")

    # edificio medianera con el mural (a la derecha, alto)
    volumen(l, 70, base - 92, ancho - 5, base, rgb("#cfc7b6"), 1, 3)

    # ventanitas
    for y in (base - 84, base - 26):
        for x in (76, 140):
            l.rect(x, y, x + 3, y + 6, rgb("#3b5a86"))

    # mural: fondo ocre con el rostro de Gardel y su sombrero
    mx0, my0, mx1, my1 = 80, base - 80, 132, base - 8

    l.rect(mx0, my0, mx1, my1, rgb("#c7743a"))
    l.rect(mx0, my0, mx1, my0 + 3, rgb("#e0944f"))

    # cara
    cxm = (mx0 + mx1) // 2

    l.elipse(cxm - 11, my0 + 22, cxm + 11, my0 + 52, rgb("#e0b08a"))
    l.rect(cxm - 11, my0 + 40, cxm - 9, my0 + 50, rgb("#d09a74"))

    # sombrero gris
    l.rect(cxm - 20, my0 + 20, cxm + 20, my0 + 24, rgb("#4a4a52"))
    l.rect(cxm - 13, my0 + 7, cxm + 13, my0 + 20, rgb("#5a5a64"))
    l.rect(cxm - 13, my0 + 16, cxm + 13, my0 + 18, rgb("#2a2a30"))

    # ojos, cejas, sonrisa
    l.rect(cxm - 7, my0 + 31, cxm - 4, my0 + 31, NEGRO)
    l.rect(cxm + 4, my0 + 31, cxm + 7, my0 + 31, NEGRO)
    l.px(cxm - 6, my0 + 33, NEGRO)
    l.px(cxm + 5, my0 + 33, NEGRO)

    l.rect(cxm - 1, my0 + 34, cxm, my0 + 38, rgb("#c28a66"))

    l.rect(cxm - 6, my0 + 43, cxm + 6, my0 + 45, rgb("#f4f1e8"))
    l.rect(cxm - 7, my0 + 42, cxm - 7, my0 + 43, rgb("#8a4a3a"))
    l.rect(cxm + 7, my0 + 42, cxm + 7, my0 + 43, rgb("#8a4a3a"))

    # traje y pañuelo blanco
    l.poly([(cxm - 24, my1), (cxm - 14, my0 + 54), (cxm + 14, my0 + 54), (cxm + 24, my1)], rgb("#2a2a34"))
    l.poly([(cxm - 4, my0 + 54), (cxm, my0 + 62), (cxm + 4, my0 + 54)], rgb("#f4f1e8"))

    l.marco(mx0, my0, mx1, my1, rgb("#6a3a1a"))

    # la casa museo (baja, a la izquierda)
    volumen(l, 6, base - 44, 68, base, amarillo, 1, 3)

    l.rect(4, base - 47, 70, base - 44, rgb("#b8913a"))
    l.rect(4, base - 47, 70, base - 47, luz(rgb("#b8913a"), 0.3))

    # tejadito de chapa
    l.poly([(5, base - 47), (12, base - 54), (62, base - 54), (69, base - 47)], rgb("#8a8f98"))

    for x in range(14, 62, 3):
        l.rect(x, base - 53, x, base - 48, rgb("#6a7078"))

    # ventanas con rejas
    for x in (12, 50):

        l.rect(x - 1, base - 36, x + 8, base - 11, rgb("#b8913a"))
        l.rect(x, base - 35, x + 7, base - 12, VIDRIO)

        for k in range(x + 1, x + 8, 2):
            l.rect(k, base - 35, k, base - 12, NEGRO)

        l.rect(x, base - 24, x + 7, base - 24, NEGRO)

    # puerta con reja
    l.rect(29, base - 28, 41, base, rgb("#b8913a"))
    l.rect(30, base - 27, 40, base, rgb("#2a1f1a"))

    for k in range(31, 40, 2):
        l.rect(k, base - 27, k, base - 2, rgb("#5a4a3a"))

    # cartel
    texto = "CASA GARDEL"

    w = ancho_texto(texto)

    l.rect(35 - w // 2 - 2, base - 41, 35 + w // 2 + 1, base - 31, rgb("#1f2b4a"))

    l.texto(35 - w // 2, base - 39, texto, rgb("#ffd84a"))

    # bandoneon/tango: banco de la puerta
    banco(l, 46, base, 10, rgb("#3a3a3a"))

    return l


MONUMENTOS = [
    dict(id="abasto_shopping", nombre="Abasto Shopping (ex Mercado de Abasto)", fn=abasto_shopping),
    dict(id="estatua_gardel", nombre="Monumento a Carlos Gardel", fn=estatua_gardel),
    dict(id="casa_museo_gardel", nombre="Casa Museo Carlos Gardel y mural", fn=casa_museo_gardel),
]

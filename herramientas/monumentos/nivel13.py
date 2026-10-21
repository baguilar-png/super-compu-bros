"""
NIVEL 13 - MONSERRAT

    * Palacio Barolo (Av. de Mayo, con faro y cupula; homenaje a la Divina Comedia)
    * Cafe Tortoni (el cafe notable mas antiguo de la ciudad)
    * Iglesia de San Ignacio de Loyola (Manzana de las Luces, 1710)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# PALACIO BAROLO
# ==========================================================

def barolo():

    ancho = 92
    alto = 196

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = 46

    piedra = rgb("#dccaa2")
    cobre = rgb("#4f8a74")

    def cuerpo(x0, x1, y0, y1, filas, color=piedra):

        volumen(l, x0, y0, x1, y1, color, 1, 3)

        l.rect(x0 - 1, y0, x1 + 1, y0 + 2, luz(color, 0.3))
        l.rect(x0 - 1, y0 + 2, x1 + 1, y0 + 2, sombra(color, 0.75))

        # pilastras verticales
        for x in range(x0 + 2, x1 - 2, 8):

            l.rect(x, y0 + 3, x, y1 - 1, luz(color, 0.25))
            l.rect(x + 1, y0 + 3, x + 1, y1 - 1, sombra(color, 0.9))

        # ventanas en dos hileras por piso
        alto_piso = (y1 - y0 - 4) // filas

        for f in range(filas):

            y = y0 + 5 + f * alto_piso

            for x in range(x0 + 4, x1 - 4, 8):

                l.rect(x, y, x + 2, y + alto_piso - 5, VIDRIO)
                l.px(x, y, VIDRIO_LUZ)

            l.rect(x0, y + alto_piso - 3, x1, y + alto_piso - 3, sombra(color, 0.9))

    # --- cuerpo de abajo con portal ---
    cuerpo(cx - 44, cx + 44, base - 52, base, 3)

    # zocalo rusticado
    l.rect(cx - 44, base - 14, cx + 44, base, rgb("#b9a67c"))

    for y in range(base - 12, base, 3):
        l.rect(cx - 44, y, cx + 44, y, sombra(rgb("#b9a67c"), 0.85))

    # portal con arco y columnas
    l.arco(cx - 8, base, cx + 8, 26, rgb("#c9b78b"))
    l.arco(cx - 6, base - 1, cx + 6, 23, rgb("#2c3340"))

    l.rect(cx, base - 22, cx, base - 1, rgb("#4a5a70"))

    for dx in (-12, 12):
        columnas(l, cx + dx, cx + dx, base - 26, base - 1, 1, 3, rgb("#eadcb6"))

    # --- cuerpo medio ---
    cuerpo(cx - 34, cx + 34, base - 118, base - 52, 6)

    # torrecitas con cupula en las esquinas
    for dx in (-34, 34):

        l.rect(cx + dx - 4, base - 128, cx + dx + 4, base - 118, piedra)
        l.rect(cx + dx - 4, base - 128, cx + dx - 4, base - 118, luz(piedra, 0.2))
        l.rect(cx + dx + 2, base - 128, cx + dx + 4, base - 118, sombra(piedra, 0.84))

        cupula(l, cx + dx, base - 128, 5, 6, cobre, costillas=1)

    # --- cuerpo alto ---
    cuerpo(cx - 24, cx + 24, base - 150, base - 118, 3)

    # --- remate: tambor, cupula y faro ---
    volumen(l, cx - 12, base - 166, cx + 12, base - 150, piedra, 1, 3)

    for dx in (-7, -1, 5):

        ventana_arco(l, cx + dx, base - 152, cx + dx + 3, 9, rgb("#2f4a60"), luz(piedra, 0.3))

    l.rect(cx - 14, base - 168, cx + 14, base - 166, luz(piedra, 0.25))

    cupula(l, cx, base - 168, 12, 12, cobre, costillas=4)

    # faro: cilindro de vidrio con luz
    l.rect(cx - 3, base - 186, cx + 3, base - 180, rgb("#fff0a0"))
    l.rect(cx - 3, base - 186, cx - 3, base - 180, rgb("#ffffff"))
    l.rect(cx - 4, base - 188, cx + 4, base - 187, cobre)
    l.rect(cx - 4, base - 180, cx + 4, base - 180, cobre)

    l.rect(cx, base - 196 + 2, cx, base - 189, rgb("#3a3a3a"))

    # rayos de luz del faro
    for k in range(1, 6):

        l.px(cx - 4 - k * 2, base - 184 - k, rgb("#fff0a0"))
        l.px(cx + 4 + k * 2, base - 184 - k, rgb("#fff0a0"))
        l.px(cx - 4 - k * 2, base - 184 + k, rgb("#fff0a0"))
        l.px(cx + 4 + k * 2, base - 184 + k, rgb("#fff0a0"))

    return l


# ==========================================================
# CAFE TORTONI
# ==========================================================

def cafe_tortoni():

    ancho = 128
    alto = 90

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    crema = rgb("#e2d0ac")
    terracota = rgb("#a9553a")

    # edificio de tres plantas
    volumen(l, 6, base - 74, ancho - 7, base, crema, 1, 3)

    cornisa(l, 6, ancho - 7, base - 76, luz(crema, 0.3))

    # remate ornamental con frontis curvo
    l.poly([(cx - 24, base - 76), (cx - 14, base - 86), (cx + 14, base - 86), (cx + 24, base - 76)], crema)
    l.rect(cx - 14, base - 86, cx + 14, base - 86, luz(crema, 0.3))

    l.circulo(cx, base - 81, 3, terracota)
    l.circulo(cx, base - 81, 1, ORO)

    # balcones y ventanas
    for y in (base - 66, base - 44):

        for x in range(14, ancho - 14, 14):

            if abs(x + 3 - cx) < 12:
                continue

            ventana_arco(l, x, y + 13, x + 6, 13, VIDRIO, luz(crema, 0.4))

            balcon(l, x - 2, x + 8, y + 11, NEGRO, alto=2)

    # balcon central corrido
    ventana_arco(l, cx - 5, base - 40, cx + 5, 22, VIDRIO, luz(crema, 0.4))

    balcon(l, cx - 20, cx + 20, base - 46, NEGRO, alto=3)

    ventana_arco(l, cx - 5, base - 62, cx + 5, 18, VIDRIO, luz(crema, 0.4))

    # franja entre pisos
    l.rect(6, base - 28, ancho - 7, base - 26, terracota)

    # cartel de hierro con el nombre
    texto = "TORTONI"

    w = ancho_texto(texto)

    l.rect(cx - w // 2 - 4, base - 25, cx + w // 2 + 3, base - 14, rgb("#1a1a1a"))
    l.marco(cx - w // 2 - 4, base - 25, cx + w // 2 + 3, base - 14, ORO)

    l.texto(cx - w // 2, base - 23, texto, ORO)

    # planta baja: marcos de madera y vidrieras
    l.rect(6, base - 13, ancho - 7, base, rgb("#3a2518"))

    for x in range(10, ancho - 14, 18):

        if abs(x + 7 - cx) < 12:
            continue

        l.rect(x, base - 12, x + 14, base - 1, rgb("#e7c22b"))
        l.rect(x + 1, base - 11, x + 13, base - 2, rgb("#f4e7a3"))
        l.rect(x + 7, base - 11, x + 7, base - 2, rgb("#3a2518"))

    # puerta central
    l.rect(cx - 6, base - 12, cx + 6, base, rgb("#3a2518"))
    l.rect(cx - 5, base - 11, cx + 5, base - 1, rgb("#e7c22b"))

    # toldos verdes a rayas
    for x in range(8, ancho - 8, 2):

        if abs(x - cx) < 10:
            continue

        l.rect(x, base - 15, x + 1, base - 13, rgb("#2f6a4a") if (x // 2) % 2 else BLANCO)

    # mesitas en la vereda
    for x in (12, ancho - 24):

        l.rect(x, base - 5, x + 6, base - 4, rgb("#3a3a3a"))
        l.rect(x + 3, base - 4, x + 3, base, rgb("#3a3a3a"))

    return l


# ==========================================================
# IGLESIA SAN IGNACIO
# ==========================================================

def san_ignacio():

    ancho = 124
    alto = 112

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    muro = rgb("#efe0bf")
    ocre = rgb("#c99a52")

    # lateral de la Manzana de las Luces (a la derecha, bajo)
    volumen(l, cx + 30, base - 40, ancho - 4, base, rgb("#e6c9a0"), 1, 3)

    l.rect(cx + 28, base - 44, ancho - 3, base - 40, rgb("#a9472f"))

    for x in range(cx + 36, ancho - 12, 12):

        ventana_arco(l, x, base - 6, x + 5, 20, VIDRIO, rgb("#f4f1e8"))

    # cupula del crucero atras
    cupula(l, cx, base - 74, 15, 14, rgb("#7f8f98"), costillas=5, linterna=True, remate=ORO)

    l.rect(cx - 17, base - 86, cx + 17, base - 74, muro)

    # cuerpo central
    volumen(l, cx - 28, base - 64, cx + 28, base, muro, 1, 3)

    # frontis barroco curvo
    l.poly([(cx - 28, base - 64), (cx - 22, base - 70), (cx - 8, base - 74), (cx, base - 82),
            (cx + 8, base - 74), (cx + 22, base - 70), (cx + 28, base - 64)], muro)

    l.linea(cx - 28, base - 64, cx - 22, base - 70, ocre)
    l.linea(cx - 22, base - 70, cx - 8, base - 74, ocre)
    l.linea(cx - 8, base - 74, cx, base - 82, ocre)

    l.circulo(cx, base - 70, 3, ocre)
    l.circulo(cx, base - 70, 1, rgb("#2f4a60"))

    # cornisa
    l.rect(cx - 29, base - 40, cx + 29, base - 38, ocre)

    # portal con columnas
    l.arco(cx - 8, base, cx + 8, 32, ocre)
    l.arco(cx - 6, base - 1, cx + 6, 28, rgb("#5a3a22"))

    l.rect(cx, base - 28, cx, base - 1, rgb("#3a2518"))

    for dx in (-12, 12):
        columnas(l, cx + dx, cx + dx, base - 34, base - 2, 1, 3, rgb("#f4ead2"))

    # ventanas y nichos
    for dx in (-22, 16):

        l.arco(cx + dx, base - 36, cx + dx + 6, 14, ocre)
        l.arco(cx + dx + 1, base - 37, cx + dx + 5, 11, rgb("#7a7a7a"))

    ventana_arco(l, cx - 4, base - 54, cx + 4, 14, rgb("#2f4a60"), ocre)

    # torres campanario (bajas, a los costados)
    for lado in (-1, 1):

        tx = cx + lado * 38

        volumen(l, tx - 11, base - 78, tx + 11, base, muro, 1, 3)

        l.rect(tx - 12, base - 42, tx + 12, base - 40, ocre)

        ventana_arco(l, tx - 3, base - 8, tx + 3, 16, rgb("#2f4a60"), ocre)

        # campanario
        l.rect(tx - 12, base - 80, tx + 12, base - 78, ocre)

        l.arco(tx - 6, base - 58, tx - 2, 12, rgb("#2a3550"))
        l.arco(tx + 2, base - 58, tx + 6, 12, rgb("#2a3550"))

        # techo piramidal
        aguja(l, tx, base - 80, 26, 14, rgb("#7a8a9a"))

        l.rect(tx, base - 102, tx, base - 94, ORO)
        l.rect(tx - 2, base - 99, tx + 2, base - 99, ORO)

    # escalinata
    for i in range(3):
        l.rect(cx - 14 - i * 2, base - 2 + i, cx + 14 + i * 2, base - 2 + i,
               rgb("#e8e2d2") if i % 2 == 0 else rgb("#c8c0ad"))

    return l


MONUMENTOS = [
    # Se acortan tres pisos del cuerpo medio para que entre en la pantalla.
    dict(id="palacio_barolo", nombre="Palacio Barolo", fn=barolo,
         quitar_filas=[(83, 112)]),
    dict(id="cafe_tortoni", nombre="Cafe Tortoni", fn=cafe_tortoni),
    dict(id="san_ignacio", nombre="Iglesia de San Ignacio de Loyola", fn=san_ignacio),
]

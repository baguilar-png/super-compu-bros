"""
NIVEL 3 - PUERTO MADERO

    * Puente de la Mujer (Santiago Calatrava, 2001)
    * Fragata ARA Presidente Sarmiento (buque museo de tres palos)
    * Fuente de las Nereidas (Lola Mora, Costanera Sur)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# PUENTE DE LA MUJER
# ==========================================================

def puente_de_la_mujer():

    ancho = 200
    alto = 100

    l = Lienzo(ancho, alto)

    base = alto - 1

    blanco = rgb("#f4f6f8")
    sombra_b = rgb("#b7c4d2")

    # agua del dique
    agua_dibujo(l, 0, base - 20, ancho - 1, base - 5, rgb("#3f84c4"), seed=3)

    # muelle de adelante
    l.rect(0, base - 6, ancho - 1, base, rgb("#9a8f7c"))
    l.rect(0, base - 6, ancho - 1, base - 6, rgb("#cbbfa8"))

    for x in range(4, ancho, 10):
        l.rect(x, base - 5, x, base, rgb("#75705f"))

    # tablero del puente (blanco, bajito)
    y_t = base - 26

    l.rect(34, y_t, ancho - 8, y_t + 3, blanco)
    l.rect(34, y_t + 3, ancho - 8, y_t + 3, sombra_b)
    l.rect(34, y_t, ancho - 8, y_t, rgb("#ffffff"))

    # barandas
    for x in range(36, ancho - 8, 4):
        l.rect(x, y_t - 3, x, y_t - 1, rgb("#9aa8b8"))

    l.rect(34, y_t - 4, ancho - 8, y_t - 4, rgb("#9aa8b8"))

    # pilar de apoyo
    l.rect(ancho - 14, y_t + 4, ancho - 10, base - 6, rgb("#dcd6c6"))
    l.rect(40, y_t + 4, 44, base - 6, rgb("#dcd6c6"))

    # mastil blanco inclinado (curvo) que sale del extremo izquierdo
    base_x, base_y = 52, y_t

    tope_x, tope_y = 20, 6

    n = 64

    for i in range(n + 1):

        t = i / n

        x = base_x + (tope_x - base_x) * t - 6 * math.sin(math.pi * t) * 0.2

        y = base_y + (tope_y - base_y) * t

        grosor = int(round(5 - 2.6 * t))

        l.rect(int(x) - grosor // 2, int(y), int(x) + grosor // 2, int(y) + 1, blanco)

        l.px(int(x) + grosor // 2, int(y), sombra_b)
        l.px(int(x) - grosor // 2, int(y), rgb("#ffffff"))

    # contrapeso en la base
    l.poly([(44, y_t + 3), (58, y_t + 3), (54, y_t - 8), (46, y_t - 8)], blanco)

    # cables: abanico desde la punta del mastil hasta el tablero
    cable = rgb("#8795a8")

    for x in range(70, ancho - 10, 17):

        l.linea(tope_x + 1, tope_y + 2, x, y_t - 1, cable)

    # cables cortos de contrapeso
    l.linea(tope_x, tope_y + 2, 36, y_t, cable)
    l.linea(tope_x, tope_y + 2, 30, y_t - 8, cable)

    # farolas del puente
    for x in (90, 150):

        farola(l, x, y_t - 1, 10, c=rgb("#8a97a8"), estilo="clasico")

    # amarras
    for x in (14, 100, 186):

        l.rect(x, base - 9, x + 2, base - 7, rgb("#2c3a3a"))

    return l


# ==========================================================
# FRAGATA PRESIDENTE SARMIENTO
# ==========================================================

def _palo(l, x, y_cubierta, alto, vergas, vela=rgb("#f2ece0")):

    madera = rgb("#7a5a38")

    l.rect(x, y_cubierta - alto, x + 1, y_cubierta, madera)
    l.rect(x, y_cubierta - alto, x, y_cubierta, luz(madera, 0.2))

    for (dy, ancho) in vergas:

        y = y_cubierta - dy

        # verga con la vela enrollada (blanca)
        l.rect(x + 1 - ancho // 2, y, x + ancho // 2, y, madera)
        l.rect(x + 1 - ancho // 2 + 1, y - 2, x + ancho // 2 - 1, y - 1, vela)
        l.rect(x + 1 - ancho // 2 + 1, y - 1, x + ancho // 2 - 1, y - 1, sombra(vela, 0.82))

    # tope con banderin
    l.rect(x + 2, y_cubierta - alto, x + 6, y_cubierta - alto + 1, CELESTE_ARG)
    l.rect(x + 2, y_cubierta - alto + 2, x + 6, y_cubierta - alto + 2, BLANCO)


def fragata_sarmiento():

    ancho = 236
    alto = 134

    l = Lienzo(ancho, alto)

    base = alto - 1

    casco = rgb("#1f2330")

    # agua
    agua_dibujo(l, 0, base - 14, ancho - 1, base - 5, rgb("#3f84c4"), seed=5)

    # muelle
    l.rect(0, base - 6, ancho - 1, base, rgb("#9a8f7c"))
    l.rect(0, base - 6, ancho - 1, base - 6, rgb("#cbbfa8"))

    for x in range(4, ancho, 10):
        l.rect(x, base - 5, x, base, rgb("#75705f"))

    # casco: popa a la izquierda, proa a la derecha
    y_borda = base - 33
    y_agua = base - 12

    l.poly([(14, y_borda - 2), (30, y_agua), (190, y_agua), (220, y_borda + 2), (222, y_borda - 2)], casco)

    # franja blanca con portas de canones
    l.rect(24, y_borda + 5, 206, y_borda + 7, rgb("#f4f1e8"))

    for x in range(28, 204, 8):
        l.rect(x, y_borda + 5, x + 3, y_borda + 7, casco)

    # linea de flotacion
    l.rect(30, y_agua - 1, 190, y_agua, rgb("#7a2f2a"))

    # borda y cubierta
    l.rect(14, y_borda - 3, 222, y_borda - 2, rgb("#c9a86a"))
    l.rect(14, y_borda - 3, 222, y_borda - 3, rgb("#ead29a"))

    # alcazar de popa con ventanales
    l.rect(14, y_borda - 12, 42, y_borda - 3, rgb("#a98550"))
    l.rect(14, y_borda - 12, 42, y_borda - 12, rgb("#ead29a"))

    for x in (18, 26, 34):
        l.rect(x, y_borda - 9, x + 4, y_borda - 5, VIDRIO)
        l.px(x, y_borda - 9, VIDRIO_LUZ)

    # toldilla y cabinas
    l.rect(100, y_borda - 8, 126, y_borda - 3, rgb("#a98550"))
    l.rect(100, y_borda - 8, 126, y_borda - 8, rgb("#ead29a"))

    # palos: mesana, mayor, trinquete
    _palo(l, 56, y_borda - 3, 80, [(26, 20), (44, 16), (60, 11)])
    _palo(l, 112, y_borda - 3, 100, [(28, 26), (50, 21), (70, 15), (86, 10)])
    _palo(l, 168, y_borda - 3, 86, [(26, 22), (46, 17), (64, 12)])

    # bauprés
    l.linea(214, y_borda - 3, 234, y_borda - 14, rgb("#7a5a38"))
    l.linea(214, y_borda - 2, 234, y_borda - 13, rgb("#5a3f28"))

    # cuerdas (obenques y estais)
    cuerda = rgb("#4a4a5c")

    for (px_, py_), (qx, qy) in [
        ((57, y_borda - 80), (17, y_borda - 12)),
        ((169, y_borda - 86), (232, y_borda - 14)),
        ((113, y_borda - 100), (62, y_borda - 52)),
        ((113, y_borda - 100), (166, y_borda - 52)),
        ((113, y_borda - 100), (100, y_borda - 3)),
        ((113, y_borda - 100), (126, y_borda - 3)),
        ((169, y_borda - 86), (156, y_borda - 3)),
        ((169, y_borda - 86), (182, y_borda - 3)),
        ((57, y_borda - 80), (46, y_borda - 3)),
        ((57, y_borda - 80), (68, y_borda - 3)),
    ]:
        l.linea(px_, py_, qx, qy, cuerda)

    # bandera argentina en la popa
    bandera(l, 14, y_borda - 12, 12, ancho=9, alto=6)

    # figura de proa
    l.rect(218, y_borda - 3, 222, y_borda + 3, ORO)

    return l


# ==========================================================
# FUENTE DE LAS NEREIDAS
# ==========================================================

def fuente_nereidas():

    ancho = 120
    alto = 78

    l = Lienzo(ancho, alto)

    base = alto - 1

    marmol = rgb("#eeeae0")
    agua = rgb("#58a8d8")

    cx = 60

    # estanque grande de marmol
    l.rect(4, base - 11, ancho - 5, base, marmol)
    l.rect(4, base - 11, ancho - 5, base - 11, rgb("#ffffff"))
    l.rect(4, base - 3, ancho - 5, base, sombra(marmol, 0.86))
    l.rect(8, base - 9, ancho - 9, base - 5, agua)

    for x in range(10, ancho - 10, 8):
        l.rect(x, base - 8, x + 3, base - 8, luz(agua, 0.4))

    # pedestal central escalonado
    l.rect(cx - 16, base - 18, cx + 16, base - 11, marmol)
    l.rect(cx - 16, base - 18, cx + 16, base - 18, rgb("#ffffff"))
    l.rect(cx - 10, base - 28, cx + 10, base - 18, marmol)
    l.rect(cx - 10, base - 28, cx - 10, base - 18, rgb("#ffffff"))
    l.rect(cx + 8, base - 28, cx + 10, base - 18, sombra(marmol, 0.82))

    # conchas y rocas
    for dx in range(-8, 9, 4):
        l.rect(cx + dx, base - 26, cx + dx, base - 20, sombra(marmol, 0.88))

    # caballos marinos a los lados
    for lado in (-1, 1):

        x = cx + lado * 22

        l.elipse(x - 5, base - 26, x + 5, base - 15, marmol)
        l.rect(x - 2 + lado * 3, base - 31, x + 1 + lado * 3, base - 24, marmol)
        l.rect(x + lado * 5, base - 31, x + lado * 5 + lado * 2, base - 30, marmol)

        l.px(x + lado * 4, base - 29, rgb("#555555"))

        # cola
        l.linea(x - lado * 5, base - 17, x - lado * 9, base - 22, marmol)

        # chorro de agua de la boca hacia el estanque
        for k in range(10):

            xx = x + lado * (7 + k)

            yy = base - 29 + int((k * k) / 5)

            l.px(xx, yy, luz(agua, 0.5))

    # concha grande central (Venus naciendo)
    l.semi(cx, base - 28, 13, 11, rgb("#f4efe3"))

    for k in range(-10, 11, 4):
        l.linea(cx, base - 28, cx + k, base - 38, sombra(marmol, 0.85))

    # Venus sobre la concha
    figura(l, cx, base - 36, 24, marmol, pose="brazos_arriba", falda=False)

    # nereidas a los lados de la concha
    figura(l, cx - 13, base - 24, 12, marmol, pose="brazo_izq", falda=False)
    figura(l, cx + 13, base - 24, 12, marmol, pose="brazo_der", falda=False)

    # triton en el borde
    for lado in (-1, 1):

        figura(l, cx + lado * 36, base - 11, 12, marmol, pose="brazo_der" if lado > 0 else "brazo_izq", falda=False)

    # chorro central hacia arriba
    for k in range(8):

        l.px(cx, base - 62 - k, luz(agua, 0.5))

    l.px(cx - 1, base - 69, luz(agua, 0.5))
    l.px(cx + 1, base - 69, luz(agua, 0.5))

    return l


MONUMENTOS = [
    dict(id="puente_de_la_mujer", nombre="Puente de la Mujer", fn=puente_de_la_mujer),
    dict(id="fragata_sarmiento", nombre="Fragata ARA Presidente Sarmiento", fn=fragata_sarmiento),
    dict(id="fuente_nereidas", nombre="Fuente de las Nereidas", fn=fuente_nereidas),
]

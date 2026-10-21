"""
NIVEL 12 - OBELISCO

    * Obelisco (67,5 m, 1936, en la Plaza de la Republica)
    * Teatro Colon (ocupa toda una manzana, estilo italianizante)
    * Teatro Gran Rex (art deco de la Avenida Corrientes)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# OBELISCO
# ==========================================================

def obelisco():

    ancho = 50
    alto = 160

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = 25

    blanco = rgb("#f1eee6")

    # plazoleta escalonada
    for i in range(3):
        l.rect(cx - 17 + i * 2, base - i * 2 - 1, cx + 17 - i * 2, base - i * 2,
               rgb("#dcd6c6") if i % 2 == 0 else rgb("#c4bba8"))

    # pedestal
    volumen(l, cx - 11, base - 14, cx + 11, base - 6, blanco, 1, 3)

    # fuste: se afina hacia arriba
    top = base - 124

    for y in range(top, base - 14):

        t = (y - top) / (base - 14 - top)

        hw = 4.2 + 5.0 * t

        xa = int(round(cx - hw))
        xb = int(round(cx + hw))

        l.rect(xa, y, xb, y, blanco)
        l.px(xa, y, rgb("#ffffff"))
        l.rect(xb - 2, y, xb, y, sombra(blanco, 0.84))

        # hiladas de piedra
        if (base - y) % 9 == 0:
            l.rect(xa, y, xb, y, sombra(blanco, 0.93))

    # puntas: piramidion
    l.poly([(cx - 4, top), (cx, top - 14), (cx + 4, top)], blanco)
    l.poly([(cx, top - 14), (cx + 4, top), (cx + 1, top)], sombra(blanco, 0.84))

    # ventanitas de arriba (miradores)
    for dx in (-2, 1):
        l.rect(cx + dx, top + 4, cx + dx + 1, top + 6, rgb("#3a4660"))

    # placa del frente
    l.rect(cx - 4, base - 12, cx + 3, base - 8, rgb("#6a5a2a"))

    # farolas bajitas alrededor
    for dx in (-22, 22):

        farola(l, cx + dx, base, 12, c=rgb("#1f2a2a"))

    return l


# ==========================================================
# TEATRO COLON
# ==========================================================

def teatro_colon():

    ancho = 232
    alto = 112

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    piedra = rgb("#e3d2ab")
    oscuro = rgb("#b69a68")

    # sala: cupula con linterna, asoma por atras
    cupula(l, cx, base - 78, 26, 24, rgb("#7d8a8c"), costillas=8, linterna=True, remate=ORO)

    l.rect(cx - 28, base - 92, cx + 28, base - 78, piedra)

    # torre del escenario (mas alta) detras, a un costado
    volumen(l, cx + 40, base - 98, cx + 82, base - 60, rgb("#cdbd96"), 1, 3)

    l.rect(cx + 38, base - 102, cx + 84, base - 98, sombra(piedra, 0.8))

    for dx in (46, 58, 70):
        ventana_arco(l, cx + dx, base - 70, cx + dx + 4, 12, VIDRIO, oscuro)

    # cuerpo principal
    volumen(l, 6, base - 62, ancho - 7, base, piedra, 1, 3)

    # planta baja con arcos rusticados
    for x in range(10, ancho - 14, 12):

        ventana_arco(l, x, base, x + 8, 24, rgb("#2f3a4a"), luz(piedra, 0.3))

        for k in range(x + 1, x + 8, 2):
            l.rect(k, base - 22, k, base - 2, rgb("#3a4660"))

    # rusticado
    for y in range(base - 30, base, 4):

        l.rect(6, y, ancho - 7, y, sombra(piedra, 0.9))

    # entrepiso
    l.rect(6, base - 33, ancho - 7, base - 31, luz(piedra, 0.35))
    l.rect(6, base - 31, ancho - 7, base - 31, sombra(piedra, 0.75))

    # piso principal: pilastras y ventanas con arco
    for x in range(12, ancho - 14, 12):

        l.rect(x, base - 58, x + 1, base - 33, luz(piedra, 0.3))
        l.rect(x + 8, base - 58, x + 8, base - 33, sombra(piedra, 0.85))

        ventana_arco(l, x + 2, base - 36, x + 6, 20, VIDRIO, oscuro)

    # cornisa y balaustrada con estatuas
    l.rect(4, base - 66, ancho - 5, base - 62, luz(piedra, 0.25))
    l.rect(4, base - 66, ancho - 5, base - 66, rgb("#fff4d8"))
    l.rect(4, base - 62, ancho - 5, base - 62, sombra(piedra, 0.75))

    for x in range(8, ancho - 8, 3):
        l.rect(x, base - 71, x, base - 67, luz(piedra, 0.3))

    l.rect(4, base - 72, ancho - 5, base - 72, luz(piedra, 0.3))

    for x in range(16, ancho - 14, 24):

        figura(l, x, base - 72, 11, rgb("#efe7d0"), pose="brazos_arriba" if (x // 24) % 2 else "brazo_der", falda=True)

    # pabellon central con columnas
    volumen(l, cx - 26, base - 62, cx + 26, base, rgb("#e8d9b4"), 1, 3, techo=False)

    columnas(l, cx - 20, cx + 20, base - 60, base - 6, 5, 5, luz(piedra, 0.3))

    l.rect(cx - 28, base - 66, cx + 28, base - 61, luz(piedra, 0.3))

    # cartel
    texto = "TEATRO COLON"

    w = ancho_texto(texto)

    l.rect(cx - w // 2 - 3, base - 51, cx + w // 2 + 2, base - 41, rgb("#4a1f2a"))
    l.marco(cx - w // 2 - 3, base - 51, cx + w // 2 + 2, base - 41, ORO)

    l.texto(cx - w // 2, base - 49, texto, rgb("#f4e7a3"))

    # puertas
    for dx in (-12, -2, 8):

        l.rect(cx + dx, base - 18, cx + dx + 6, base - 2, rgb("#3a2518"))
        l.rect(cx + dx + 1, base - 17, cx + dx + 5, base - 3, rgb("#e7c22b"))

    # escalinata
    for i in range(3):
        l.rect(cx - 24 - i * 2, base - 3 + i, cx + 24 + i * 2, base - 3 + i,
               rgb("#e8e2d2") if i % 2 == 0 else rgb("#c8c0ad"))

    return l


# ==========================================================
# TEATRO GRAN REX
# ==========================================================

def gran_rex():

    ancho = 100
    alto = 142

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = 50

    blanco = rgb("#efe9dc")
    rojo = rgb("#c0322b")

    # cuerpo bajo con lineas horizontales
    volumen(l, 6, base - 56, ancho - 7, base, blanco, 1, 3)

    for y in range(base - 52, base - 20, 6):
        l.rect(6, y, ancho - 7, y, sombra(blanco, 0.88))

    l.rect(6, base - 56, ancho - 7, base - 53, rojo)

    # ventanas horizontales
    for x in (12, 22, ancho - 32, ancho - 22):

        l.rect(x, base - 46, x + 6, base - 38, VIDRIO)
        l.rect(x, base - 36, x + 6, base - 28, VIDRIO)

    # torre central vertical
    volumen(l, cx - 14, base - 118, cx + 14, base - 56, blanco, 1, 4)

    # remates art deco escalonados
    for i, w in enumerate((18, 14, 10)):

        l.rect(cx - w // 2, base - 118 - (i + 1) * 4, cx + w // 2, base - 118 - i * 4 - 1, blanco if i % 2 == 0 else luz(blanco, 0.2))
        l.rect(cx + w // 2 - 1, base - 118 - (i + 1) * 4, cx + w // 2, base - 118 - i * 4 - 1, sombra(blanco, 0.82))

    # aleta vertical con el cartel GRAN REX en letras apiladas
    l.rect(cx - 8, base - 116, cx + 8, base - 58, rgb("#1f1a24"))
    l.marco(cx - 8, base - 116, cx + 8, base - 58, rojo)

    letras = "GRANREX"

    for i, ch in enumerate(letras):

        l.texto(cx - 2, base - 113 + i * 8, ch, rgb("#ffd84a"))

    # lineas rojas verticales a los lados de la aleta
    for x in (cx - 12, cx + 11):
        l.rect(x, base - 114, x + 1, base - 58, rojo)

    # marquesina con luces
    l.rect(cx - 26, base - 22, cx + 26, base - 19, rojo)
    l.rect(cx - 26, base - 22, cx + 26, base - 22, luz(rojo, 0.4))

    for x in range(cx - 25, cx + 26, 3):
        l.px(x, base - 20, rgb("#ffe27a"))

    # carteleras de las obras
    for dx in (-22, 14):

        l.rect(cx + dx, base - 16, cx + dx + 8, base - 3, rgb("#2a3a5a"))
        l.rect(cx + dx + 1, base - 15, cx + dx + 7, base - 8, rgb("#e0944f"))
        l.rect(cx + dx + 1, base - 7, cx + dx + 7, base - 4, rgb("#f4f1e8"))

    # puertas
    for dx in (-10, 0, 10):

        l.rect(cx + dx - 3, base - 14, cx + dx + 3, base, rgb("#2c3340"))
        l.px(cx + dx, base - 8, rgb("#ffd84a"))

    return l


MONUMENTOS = [
    dict(id="obelisco", nombre="Obelisco", fn=obelisco),
    dict(id="teatro_colon", nombre="Teatro Colon", fn=teatro_colon),
    dict(id="teatro_gran_rex", nombre="Teatro Gran Rex", fn=gran_rex),
]

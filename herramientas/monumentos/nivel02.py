"""
NIVEL 2 - SAN TELMO

    * Mercado de San Telmo (1897, estructura de hierro, gran cupula central)
    * Iglesia Ortodoxa Rusa de la Santisima Trinidad (Parque Lezama,
      cupulas azules en forma de cebolla)
    * Iglesia de San Pedro Gonzalez Telmo (dos torres con azulejos blancos)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# MERCADO DE SAN TELMO
# ==========================================================

def mercado_san_telmo():

    ancho = 186
    alto = 112

    l = Lienzo(ancho, alto)

    base = alto - 1

    crema = rgb("#e6d6a4")
    rojo = rgb("#a9472f")
    hierro = rgb("#5f7f7c")

    # --- cupula central de hierro y vidrio (se ve detras de la fachada) ---
    cx = 93

    cupula(l, cx, base - 62, 30, 28, hierro, costillas=7,
           c_luz=rgb("#9fc2bc"), c_sombra=rgb("#46605e"), linterna=True)

    # paneles de vidrio entre las costillas
    for k in range(-24, 25, 8):

        for dy in range(6, 24, 6):

            x = cx + k

            if abs(k) < 30 * math.sqrt(max(0, 1 - (dy / 28) ** 2)) - 3:
                l.rect(x - 2, base - 62 - dy, x + 2, base - 62 - dy, VIDRIO_LUZ)

    l.rect(cx, base - 100, cx, base - 92, rgb("#3a3a3a"))
    l.rect(cx + 1, base - 100, cx + 4, base - 98, CELESTE_ARG)

    # --- cuerpo central del frente ---
    x0, x1 = 28, 158

    volumen(l, x0, base - 62, x1, base, crema, 1, 3)

    # franjas de ladrillo rojo
    l.rect(x0, base - 62, x1, base - 59, rojo)
    l.rect(x0, base - 62, x1, base - 62, luz(rojo, 0.25))
    l.rect(x0, base - 36, x1, base - 34, rojo)

    # cartel del mercado
    texto = "MERCADO DE SAN TELMO"

    w = ancho_texto(texto)

    sx = cx - w // 2

    l.rect(sx - 4, base - 58, sx + w + 3, base - 46, rgb("#1f4a38"))
    l.marco(sx - 4, base - 58, sx + w + 3, base - 46, ORO)

    l.texto(sx, base - 56, texto, BLANCO)

    # portal central con arco
    ventana_arco(l, 78, base - 6, 108, 37, VIDRIO, rojo)

    for x in range(81, 107, 5):
        l.rect(x, base - 40, x, base - 6, VIDRIO_OSC)

    l.rect(79, base - 26, 107, base - 26, VIDRIO_OSC)

    # puerta con escalones de marmol
    l.rect(88, base - 14, 98, base - 7, rgb("#3a2a22"))

    for i in range(3):
        l.rect(76 - i * 2, base - 6 + i * 2, 110 + i * 2, base - 5 + i * 2,
               rgb("#e9e4d6") if i % 2 == 0 else rgb("#cfc9bb"))

    # arcos a los costados (puestos)
    for lado in (-1, 1):

        for k in range(3):

            ax = cx + lado * (38 + k * 15) - 4

            ventana_arco(l, ax, base - 6, ax + 8, 26, VIDRIO, rojo)

            # toldo
            for j in range(0, 12, 3):
                l.rect(ax - 1 + j, base - 32, ax + 1 + j, base - 29,
                       [ROJO, BLANCO][(j // 3) % 2])

    # --- alas bajas ---
    for (a0, a1) in ((4, 27), (159, 182)):

        volumen(l, a0, base - 40, a1, base, crema, 1, 2)

        l.rect(a0, base - 40, a1, base - 38, rojo)

        for x in range(a0 + 4, a1 - 5, 9):

            ventana_arco(l, x, base - 8, x + 4, 18, VIDRIO, rojo)

    # farolitos de hierro en la entrada
    for x in (74, 112):

        l.rect(x, base - 20, x, base - 7, rgb("#2c3a3a"))
        l.rect(x - 1, base - 24, x + 1, base - 21, rgb("#f4e7a3"))

    return l


# ==========================================================
# IGLESIA ORTODOXA RUSA
# ==========================================================

def iglesia_rusa():

    ancho = 112
    alto = 140

    l = Lienzo(ancho, alto)

    base = alto - 1

    muro = rgb("#efe9dc")
    azul = rgb("#2f8fcc")
    azul_osc = rgb("#1f5f9c")

    cx = 56

    # --- cupulas de atras (las dos de los costados, mas altas que el cuerpo) ---
    for dx in (-31, 31):

        l.rect(cx + dx - 6, base - 70, cx + dx + 6, base - 46, muro)
        l.rect(cx + dx - 6, base - 70, cx + dx - 6, base - 46, luz(muro, 0.1))
        l.rect(cx + dx + 4, base - 70, cx + dx + 6, base - 46, sombra(muro, 0.85))
        l.rect(cx + dx - 2, base - 66, cx + dx + 1, base - 56, azul_osc)

        cebolla(l, cx + dx, base - 70, 18, 20, azul, estrellas=ORO)

    # --- tambor central y gran cupula ---
    l.rect(cx - 13, base - 100, cx + 13, base - 46, muro)
    l.rect(cx - 13, base - 100, cx - 13, base - 46, luz(muro, 0.1))
    l.rect(cx + 9, base - 100, cx + 13, base - 46, sombra(muro, 0.85))

    for dx in (-8, -2, 4):
        l.rect(cx + dx, base - 96, cx + dx + 2, base - 84, azul_osc)
        l.px(cx + dx, base - 96, azul)

    l.rect(cx - 14, base - 102, cx + 14, base - 100, azul_osc)

    cebolla(l, cx, base - 102, 30, 30, azul, estrellas=ORO)

    # --- cuerpo bajo ---
    volumen(l, 14, base - 46, 98, base, muro, 1, 3)

    l.rect(14, base - 46, 98, base - 43, azul_osc)
    l.rect(14, base - 46, 98, base - 46, azul)

    # ventanas con arco
    for x in (20, 30, 76, 86):

        ventana_arco(l, x, base - 8, x + 4, 22, azul_osc, muro)

        l.px(x + 1, base - 24, azul)

    # --- porche de entrada ---
    volumen(l, 40, base - 36, 72, base, muro, 1, 2)

    l.poly([(38, base - 36), (56, base - 52), (74, base - 36)], azul_osc)
    l.poly([(41, base - 37), (56, base - 49), (71, base - 37)], muro)

    l.rect(51, base - 49, 61, base - 47, azul)

    # arco de la puerta y cruz
    l.arco(49, base, 63, 26, rgb("#6a4a2a"))
    l.arco(51, base - 1, 61, 22, rgb("#8a6a3a"))

    l.rect(56, base - 44, 56, base - 40, ORO)
    l.rect(54, base - 43, 58, base - 43, ORO)

    # escalones
    for i in range(3):
        l.rect(44 - i * 2, base - 2 + i, 68 + i * 2, base - 2 + i, rgb("#cfc9bb"))

    return l


# ==========================================================
# SAN PEDRO TELMO
# ==========================================================

def _torre_telmo(l, cx, base):

    muro = rgb("#efe5cb")

    # cuerpo cubico
    volumen(l, cx - 11, base - 66, cx + 11, base, muro, 1, 3)

    l.rect(cx - 12, base - 68, cx + 12, base - 66, luz(muro, 0.3))

    # ventana de campanario
    ventana_arco(l, cx - 4, base - 40, cx + 4, 14, rgb("#2a3550"), rgb("#bfae86"))
    ventana_arco(l, cx - 3, base - 14, cx + 3, 10, rgb("#2a3550"), rgb("#bfae86"))

    # primer octogono
    volumen(l, cx - 8, base - 86, cx + 8, base - 68, muro, 1, 2)

    for x in (cx - 5, cx + 1):
        ventana_arco(l, x, base - 72, x + 3, 10, rgb("#2a3550"), rgb("#bfae86"))

    l.rect(cx - 9, base - 88, cx + 9, base - 86, rgb("#c9b78b"))

    # segundo octogono
    volumen(l, cx - 6, base - 102, cx + 6, base - 88, muro, 1, 2)

    l.rect(cx - 2, base - 98, cx + 1, base - 91, rgb("#2a3550"))

    l.rect(cx - 7, base - 104, cx + 7, base - 102, rgb("#c9b78b"))

    # azulejos blancos y azules en los remates
    for x in range(cx - 6, cx + 6, 2):
        l.px(x, base - 100, rgb("#6b8fd0"))

    # cupulita con linterna y cruz
    cupula(l, cx, base - 104, 7, 9, rgb("#7a8aa0"), costillas=2)

    l.rect(cx, base - 118, cx, base - 112, ORO)
    l.rect(cx - 2, base - 116, cx + 2, base - 116, ORO)


def san_pedro_telmo():

    ancho = 112
    alto = 130

    l = Lienzo(ancho, alto)

    base = alto - 1

    muro = rgb("#efe5cb")

    # cupula del crucero (atras)
    cupula(l, 56, base - 74, 17, 15, rgb("#8a97a8"), costillas=5, linterna=True, remate=ORO)

    l.rect(40, base - 90, 72, base - 74, muro)

    # torres
    _torre_telmo(l, 20, base)
    _torre_telmo(l, ancho - 21, base)

    # cuerpo central de la fachada
    volumen(l, 32, base - 76, ancho - 33, base, muro, 1, 3)

    # frontis curvo del remate
    l.poly([(32, base - 76), (56, base - 90), (ancho - 33, base - 76)], muro)
    l.linea(32, base - 76, 56, base - 90, luz(muro, 0.3))

    l.rect(51, base - 86, 61, base - 80, rgb("#2a3550"))

    # nicho con San Pedro Telmo
    l.arco(48, base - 40, 64, 22, rgb("#c9b78b"))
    l.arco(50, base - 41, 62, 19, rgb("#7a6a52"))

    figura(l, 56, base - 42, 14, rgb("#f4efe0"), pose="brazo_der", falda=True)

    # inscripcion
    l.rect(40, base - 62, 72, base - 62, rgb("#c9b78b"))

    for x in range(41, 72, 2):
        l.px(x, base - 58, rgb("#b0a074"))

    # portal con arco y puerta
    l.arco(47, base, 65, 30, rgb("#c9b78b"))
    l.arco(49, base - 1, 63, 26, rgb("#5a3a22"))

    l.rect(56, base - 24, 56, base - 1, rgb("#3a2518"))

    # puertas laterales
    for x in (36, 70):

        ventana_arco(l, x, base - 6, x + 5, 20, rgb("#5a3a22"), rgb("#c9b78b"))

    # ventanas del medio
    for x in (36, 70):

        ventana_arco(l, x, base - 38, x + 5, 12, rgb("#2a3550"), rgb("#c9b78b"))

    # escalinata de marmol
    for i in range(4):
        l.rect(40 - i * 2, base - 3 + i, 72 + i * 2, base - 3 + i,
               rgb("#e9e4d6") if i % 2 == 0 else rgb("#cfc9bb"))

    return l


MONUMENTOS = [
    dict(id="mercado_san_telmo", nombre="Mercado de San Telmo", fn=mercado_san_telmo),
    dict(id="iglesia_rusa", nombre="Catedral Ortodoxa Rusa (Parque Lezama)", fn=iglesia_rusa),
    dict(id="san_pedro_telmo", nombre="Iglesia de San Pedro Gonzalez Telmo", fn=san_pedro_telmo),
]

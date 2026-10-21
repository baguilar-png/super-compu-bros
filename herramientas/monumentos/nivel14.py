"""
NIVEL 14 - CONSTITUCION

    * Estacion Constitucion (cabecera del Ferrocarril Roca, 1887)
    * Iglesia del Inmaculado Corazon de Maria (neogotica, 1923)
    * Autopista 25 de Mayo (viaducto elevado sobre columnas de hormigon)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# ESTACION CONSTITUCION
# ==========================================================

def estacion_constitucion():

    ancho = 240
    alto = 120

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    ladrillo = rgb("#a9472f")
    piedra = rgb("#e0d6bc")
    zinc = rgb("#6a7280")

    # nave de hierro al fondo (galpon de andenes)
    for x0, x1 in ((6, 80), (ancho - 81, ancho - 7)):

        mx = (x0 + x1) // 2

        l.semi(mx, base - 50, (x1 - x0) // 2, 38, rgb("#4f5f68"))
        l.semi(mx, base - 50, (x1 - x0) // 2 - 3, 35, rgb("#a8c8d4"))

        for k in range(-30, 31, 10):
            l.rect(mx + k, base - 50 - int(34 * math.sqrt(max(0, 1 - (k / 36) ** 2))), mx + k, base - 50, rgb("#4f5f68"))

    # cuerpo principal de ladrillo con piedra
    ladrillos(l, 12, base - 58, ancho - 13, base, ladrillo)

    l.rect(12, base - 58, 13, base, luz(ladrillo, 0.2))
    l.rect(ancho - 15, base - 58, ancho - 13, base, sombra(ladrillo, 0.78))

    # zocalo y cornisas de piedra
    l.rect(12, base - 8, ancho - 13, base, rgb("#8d8a84"))
    l.rect(12, base - 8, ancho - 13, base - 8, rgb("#b4b0a8"))

    l.rect(11, base - 62, ancho - 12, base - 58, piedra)
    l.rect(11, base - 62, ancho - 12, base - 62, luz(piedra, 0.3))

    l.rect(12, base - 30, ancho - 13, base - 29, piedra)

    # arcos de piedra
    for x in range(20, ancho - 28, 12):

        ventana_arco(l, x, base - 8, x + 7, 20, rgb("#2f3a4a"), piedra)

        ventana_arco(l, x, base - 33, x + 7, 17, VIDRIO, piedra)

    # techo de zinc
    l.poly([(10, base - 62), (22, base - 74), (ancho - 23, base - 74), (ancho - 11, base - 62)], zinc)

    l.rect(22, base - 74, ancho - 23, base - 74, luz(zinc, 0.3))

    for x in range(34, ancho - 34, 22):

        l.rect(x, base - 71, x + 6, base - 64, piedra)
        l.rect(x + 1, base - 70, x + 5, base - 65, VIDRIO)

    # torre central con reloj
    volumen(l, cx - 15, base - 100, cx + 15, base - 58, piedra, 1, 3)

    l.rect(cx - 17, base - 102, cx + 17, base - 100, luz(piedra, 0.3))

    ventana_arco(l, cx - 6, base - 62, cx + 6, 14, VIDRIO, ladrillo)

    l.circulo(cx, base - 84, 9, rgb("#2c3340"))
    l.circulo(cx, base - 84, 8, rgb("#fbf8ee"))

    for k in range(12):

        ang = k * math.pi / 6

        l.px(int(round(cx + 6.5 * math.sin(ang))), int(round(base - 84 - 6.5 * math.cos(ang))), NEGRO)

    l.linea(cx, base - 84, cx, base - 90, NEGRO)
    l.linea(cx, base - 84, cx + 4, base - 82, NEGRO)

    # cupula de la torre
    cupula(l, cx, base - 102, 15, 12, rgb("#4f6a60"), costillas=5, linterna=True)

    l.rect(cx, base - 126 + 2, cx, base - 116, rgb("#3a3a3a"))

    bandera(l, cx, base - 124, 8, ancho=8, alto=5)

    # portal de entrada
    ventana_arco(l, cx - 8, base - 6, cx + 8, 20, rgb("#1f2a3a"), piedra)

    # cartel (sobre el portal)
    texto = "CONSTITUCION"

    w = ancho_texto(texto)

    l.rect(cx - w // 2 - 3, base - 46, cx + w // 2 + 2, base - 37, rgb("#1f2b4a"))
    l.marco(cx - w // 2 - 3, base - 46, cx + w // 2 + 2, base - 37, piedra)

    l.texto(cx - w // 2, base - 44, texto, rgb("#ffd84a"))

    # farolas
    for x in (6, ancho - 8):
        farola(l, x, base, 22, c=rgb("#1f2a2a"))

    return l


# ==========================================================
# IGLESIA DEL INMACULADO CORAZON DE MARIA
# ==========================================================

def _ojiva(l, x0, x1, y_base, alto, c):
    """Arco apuntado (gotico)."""

    ancho = x1 - x0 + 1

    recto = max(0, alto - ancho // 2 - 1)

    l.rect(x0, y_base - recto, x1, y_base, c)

    for dy in range(1, ancho // 2 + 2):

        t = dy / (ancho // 2 + 1)

        hw = (ancho / 2) * (1 - t) + 0.5

        cx = (x0 + x1) / 2

        l.rect(int(round(cx - hw)), y_base - recto - dy, int(round(cx + hw)), y_base - recto - dy, c)


def iglesia_claretiana():

    ancho = 112
    alto = 170

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = 56

    piedra = rgb("#d8cdb6")
    pizarra = rgb("#59656e")

    # nave con contrafuertes (detras de la fachada)
    volumen(l, cx - 30, base - 80, cx + 30, base, piedra, 1, 3)

    # frontis central empinado
    l.poly([(cx - 20, base - 78), (cx, base - 112), (cx + 20, base - 78)], piedra)
    l.poly([(cx, base - 112), (cx + 20, base - 78), (cx + 2, base - 78)], sombra(piedra, 0.86))
    l.linea(cx - 20, base - 78, cx, base - 112, luz(piedra, 0.3))

    # cruz de remate
    l.rect(cx, base - 124, cx, base - 112, rgb("#555a60"))
    l.rect(cx - 2, base - 120, cx + 2, base - 120, rgb("#555a60"))

    # rosetón
    l.circulo(cx, base - 84, 9, luz(piedra, 0.2))
    l.circulo(cx, base - 84, 7, rgb("#2f4a60"))

    for k in range(8):

        ang = k * math.pi / 4

        l.linea(cx, base - 84, int(round(cx + 7 * math.cos(ang))), int(round(base - 84 - 7 * math.sin(ang))), luz(piedra, 0.1))

    l.circulo(cx, base - 84, 2, rgb("#c0392b"))
    l.px(cx - 4, base - 88, rgb("#e7c22b"))
    l.px(cx + 4, base - 80, rgb("#3a6fd0"))

    # torres gemelas
    for lado in (-1, 1):

        tx = cx + lado * 36

        volumen(l, tx - 11, base - 100, tx + 11, base, piedra, 1, 3)

        # contrafuertes
        l.rect(tx - 12, base - 100, tx - 10, base, luz(piedra, 0.15))
        l.rect(tx + 10, base - 100, tx + 12, base, sombra(piedra, 0.82))

        # ventanas apuntadas
        _ojiva(l, tx - 3, tx + 3, base - 56, 28, rgb("#2f4a60"))
        _ojiva(l, tx - 3, tx + 3, base - 86, 18, rgb("#2f4a60"))

        l.rect(tx, base - 82, tx, base - 70, luz(piedra, 0.15))

        # cornisa
        l.rect(tx - 13, base - 102, tx + 13, base - 100, luz(piedra, 0.25))

        # aguja afilada de pizarra
        aguja(l, tx, base - 102, 20, 50, pizarra)

        l.rect(tx, base - 164, tx, base - 152, rgb("#555a60"))

        # pinaculos en las esquinas
        for dx in (-9, 9):
            aguja(l, tx + dx, base - 102, 4, 10, piedra)

    # tres portales apuntados
    for dx, h in ((-14, 26), (0, 34), (14, 26)):

        _ojiva(l, cx + dx - 5, cx + dx + 5, base, h, luz(piedra, 0.25))
        _ojiva(l, cx + dx - 3, cx + dx + 3, base - 1, h - 3, rgb("#4a2f1f"))

    l.rect(cx, base - 30, cx, base - 1, rgb("#2a1a10"))

    # escalones
    for i in range(3):
        l.rect(cx - 24 - i * 2, base - 2 + i, cx + 24 + i * 2, base - 2 + i,
               rgb("#e8e2d2") if i % 2 == 0 else rgb("#c8c0ad"))

    return l


# ==========================================================
# AUTOPISTA 25 DE MAYO
# ==========================================================

def autopista():

    ancho = 264
    alto = 110

    l = Lienzo(ancho, alto)

    base = alto - 1

    hormigon = rgb("#a9a9a5")
    oscuro = rgb("#6f6f6c")

    y_tab = base - 62

    # rampa que baja hacia la izquierda
    l.poly([(0, base - 4), (0, base - 14), (78, y_tab), (78, y_tab + 12), (0, base - 2)], hormigon)
    l.linea(0, base - 14, 78, y_tab, luz(hormigon, 0.3))
    l.linea(0, base - 2, 78, y_tab + 12, oscuro)

    # tablero elevado
    l.rect(78, y_tab, ancho - 1, y_tab + 11, hormigon)
    l.rect(78, y_tab, ancho - 1, y_tab, luz(hormigon, 0.35))
    l.rect(78, y_tab + 9, ancho - 1, y_tab + 11, oscuro)

    # baranda de hormigon (new jersey)
    l.poly([(0, base - 18), (0, base - 14), (78, y_tab), (78, y_tab - 6)], luz(hormigon, 0.1))

    l.rect(78, y_tab - 6, ancho - 1, y_tab - 1, luz(hormigon, 0.12))
    l.rect(78, y_tab - 6, ancho - 1, y_tab - 6, luz(hormigon, 0.4))

    for x in range(84, ancho, 16):
        l.rect(x, y_tab - 6, x, y_tab - 1, oscuro)

    # autos que se ven por encima de la baranda
    colores = [ROJO, rgb("#2f64b8"), rgb("#e7c22b"), rgb("#f4f1e8"), rgb("#2f9a5a")]

    for i, x in enumerate(range(96, ancho - 20, 38)):

        c = colores[i % len(colores)]

        l.rect(x, y_tab - 10, x + 10, y_tab - 7, c)
        l.rect(x + 2, y_tab - 12, x + 8, y_tab - 10, sombra(c, 0.85))
        l.rect(x + 3, y_tab - 11, x + 7, y_tab - 10, VIDRIO_LUZ)

    # columnas de hormigon con cabezal en T
    for x in range(100, ancho - 10, 62):

        l.rect(x - 14, y_tab + 12, x + 14, y_tab + 18, hormigon)
        l.rect(x - 14, y_tab + 12, x + 14, y_tab + 12, luz(hormigon, 0.25))
        l.rect(x - 14, y_tab + 18, x + 14, y_tab + 18, oscuro)

        l.rect(x - 5, y_tab + 19, x + 5, base, hormigon)
        l.rect(x - 5, y_tab + 19, x - 5, base, luz(hormigon, 0.25))
        l.rect(x + 3, y_tab + 19, x + 5, base, oscuro)

        # manchas y grafitis
        l.rect(x - 3, base - 24, x + 2, base - 20, rgb("#d8392b"))
        l.rect(x - 3, base - 18, x + 2, base - 15, rgb("#e7c22b"))
        l.rect(x - 3, base - 13, x + 2, base - 10, rgb("#2f64b8"))

    # columnas de la rampa
    for x in (24, 48):

        top = base - 4 - int((x / 78) * (base - 4 - (y_tab + 12)))

        l.rect(x - 4, top, x + 4, base, hormigon)
        l.rect(x + 2, top, x + 4, base, oscuro)

    # carteles y farolas en el tablero
    for x in (130, 220):

        l.rect(x, y_tab - 30, x, y_tab - 7, rgb("#3a3f48"))
        l.rect(x, y_tab - 30, x + 8, y_tab - 30, rgb("#3a3f48"))
        l.rect(x + 5, y_tab - 29, x + 9, y_tab - 28, rgb("#f4e7a3"))

    # cartel verde de ruta
    cx = 172

    l.rect(cx - 25, y_tab - 38, cx + 25, y_tab - 22, rgb("#1f6f3f"))
    l.marco(cx - 25, y_tab - 38, cx + 25, y_tab - 22, BLANCO)
    l.texto(cx - ancho_texto("25 MAYO") // 2, y_tab - 34, "25 MAYO", BLANCO)

    l.rect(cx - 18, y_tab - 22, cx - 18, y_tab - 7, rgb("#3a3f48"))
    l.rect(cx + 18, y_tab - 22, cx + 18, y_tab - 7, rgb("#3a3f48"))

    return l


MONUMENTOS = [
    dict(id="estacion_constitucion", nombre="Estacion Constitucion", fn=estacion_constitucion),
    dict(id="iglesia_claretiana", nombre="Iglesia del Inmaculado Corazon de Maria", fn=iglesia_claretiana),
    dict(id="autopista_25_de_mayo", nombre="Autopista 25 de Mayo", fn=autopista),
]

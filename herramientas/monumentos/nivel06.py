"""
NIVEL 6 - RECOLETA

    * Floralis Generica (flor de acero inoxidable de 23 m)
    * Cementerio de la Recoleta (portico dorico, mausoleos y cipreses)
    * Basilica Nuestra Senora del Pilar (iglesia colonial de 1732)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# FLORALIS GENERICA
# ==========================================================

def floralis():

    ancho = 104
    alto = 112

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    acero = rgb("#c3ceda")
    acero_luz = rgb("#f2f6fa")
    acero_sombra = rgb("#7f8da0")

    # espejo de agua
    l.rect(2, base - 9, ancho - 3, base, rgb("#dcd6c6"))
    l.rect(2, base - 9, ancho - 3, base - 9, rgb("#f2eee2"))
    l.rect(5, base - 7, ancho - 6, base - 2, rgb("#4f93cf"))

    for x in range(8, ancho - 8, 9):
        l.rect(x, base - 6, x + 3, base - 6, luz(rgb("#4f93cf"), 0.4))
        l.rect(x + 4, base - 4, x + 6, base - 4, luz(rgb("#4f93cf"), 0.3))

    # tallo
    y_flor = base - 36

    l.rect(cx - 2, y_flor, cx + 1, base - 8, acero_sombra)
    l.rect(cx - 2, y_flor, cx - 2, base - 8, acero)

    # base del tallo
    l.rect(cx - 6, base - 12, cx + 5, base - 9, rgb("#dcd6c6"))

    # petalos: abanico de cinco (el sexto queda atras)
    def petalo(angulo, largo, ancho_max, tono_base):

        rad = math.radians(angulo)

        dx = math.sin(rad)
        dy = -math.cos(rad)

        px_ = -dy
        py_ = dx

        pasos = largo

        izq = []
        der = []

        for i in range(pasos + 1):

            t = i / pasos

            w = ancho_max * math.sin(math.pi * (0.18 + 0.7 * t)) ** 0.9 / 2

            cxp = cx + dx * i
            cyp = y_flor + dy * i

            izq.append((cxp + px_ * w, cyp + py_ * w))
            der.append((cxp - px_ * w, cyp - py_ * w))

        pts = izq + der[::-1]

        l.poly(pts, tono_base)

        # luz a un lado, sombra al otro
        l.poly(izq[: pasos // 1] + [(cx + dx * pasos * 0.6, y_flor + dy * pasos * 0.6)], tono_base)

        for (x, y), (x2, y2) in zip(izq[:-1], izq[1:]):
            l.linea(x, y, x2, y2, acero_luz)

        for (x, y), (x2, y2) in zip(der[:-1], der[1:]):
            l.linea(x, y, x2, y2, acero_sombra)

    # los de atras primero
    petalo(-20, 52, 14, rgb("#aab7c6"))
    petalo(20, 52, 14, rgb("#aab7c6"))

    petalo(-58, 50, 13, acero)
    petalo(58, 50, 13, acero_sombra)
    petalo(-38, 56, 15, acero)
    petalo(38, 56, 15, rgb("#97a5b7"))
    petalo(0, 58, 15, rgb("#dbe3ec"))

    # estambres / pistilo en el centro
    for dx in (-3, -1, 1, 3):

        l.rect(cx + dx, y_flor - 14, cx + dx, y_flor + 2, rgb("#3a4452"))

    l.rect(cx - 3, y_flor - 15, cx + 3, y_flor - 14, ORO)
    l.rect(cx - 4, y_flor + 1, cx + 3, y_flor + 4, acero_sombra)

    return l


# ==========================================================
# CEMENTERIO DE LA RECOLETA
# ==========================================================

def cementerio_recoleta():

    ancho = 212
    alto = 112

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    muro = rgb("#d9d0b8")
    verde = rgb("#2f6b3a")

    # mausoleos y cipreses que asoman detras del muro
    r = random.Random(7)

    for x in range(8, ancho - 8, 14):

        h = r.randint(26, 52)

        if abs(x - cx) < 38:
            continue

        tipo = r.choice(["cupula", "cruz", "cipres", "cipres", "angel"])

        if tipo == "cipres":
            arbol(l, x + 4, base - 24, h, "cipres")
        elif tipo == "cupula":
            volumen(l, x, base - 40, x + 10, base - 24, rgb("#e6dfcf"), 1, 2)
            cupula(l, x + 5, base - 40, 6, 6, rgb("#7f8f8c"), costillas=1)
            l.rect(x + 5, base - 50, x + 5, base - 46, ORO)
        elif tipo == "cruz":
            volumen(l, x + 1, base - 36, x + 9, base - 24, rgb("#cfc7b4"), 1, 2)
            l.rect(x + 5, base - 48, x + 5, base - 37, rgb("#bdb5a2"))
            l.rect(x + 3, base - 45, x + 7, base - 45, rgb("#bdb5a2"))
        else:
            volumen(l, x + 1, base - 34, x + 9, base - 24, rgb("#d8d0be"), 1, 2)
            figura(l, x + 5, base - 34, 14, rgb("#f1ece0"), pose="brazos_arriba", falda=True)

    # muro bajo del cementerio con pilares
    volumen(l, 4, base - 26, ancho - 5, base, muro, 1, 3)

    cornisa(l, 4, ancho - 5, base - 28, luz(muro, 0.2))

    for x in range(14, ancho - 10, 22):

        l.rect(x, base - 24, x + 3, base - 2, sombra(muro, 0.88))
        l.rect(x, base - 24, x, base - 2, luz(muro, 0.15))

    # portico central de cuatro columnas
    px0, px1 = cx - 36, cx + 36

    # pared de fondo y escalones
    volumen(l, px0, base - 62, px1, base, rgb("#cfc6ae"), 1, 3, techo=False)

    # puerta de hierro
    ventana_arco(l, cx - 8, base - 4, cx + 8, 38, rgb("#1f2a2a"), rgb("#e6dfcf"))

    for x in range(cx - 7, cx + 8, 3):
        l.rect(x, base - 40, x, base - 5, rgb("#3a4a4a"))

    # entablamento
    l.rect(px0 - 2, base - 70, px1 + 2, base - 64, rgb("#e6dfcf"))
    l.rect(px0 - 2, base - 70, px1 + 2, base - 70, rgb("#f6f1e4"))
    l.rect(px0 - 2, base - 64, px1 + 2, base - 64, sombra(muro, 0.8))

    # inscripcion: renglon de letras (Requiescant in pace)
    for x in range(px0 + 4, px1 - 3, 3):
        l.rect(x, base - 68, x + 1, base - 66, rgb("#8a7f68"))

    # frontis
    fronton(l, px0 - 2, px1 + 2, base - 71, 15, rgb("#e6dfcf"), interior=rgb("#d1c8b0"))

    l.circulo(cx, base - 80, 2, rgb("#bdb5a2"))

    # columnas doricas
    columnas(l, px0 + 6, px1 - 6, base - 63, base - 3, 4, 7, rgb("#e6dfcf"))

    # escalones
    for i in range(3):
        l.rect(px0 - 2 - i * 2, base - 2 + i, px1 + 2 + i * 2, base - 2 + i,
               rgb("#e0d8c8") if i % 2 == 0 else rgb("#c4bba8"))

    # cipreses al frente
    arbol(l, 10, base, 52, "cipres")
    arbol(l, ancho - 11, base, 52, "cipres")

    return l


# ==========================================================
# BASILICA DEL PILAR
# ==========================================================

def basilica_pilar():

    ancho = 128
    alto = 118

    l = Lienzo(ancho, alto)

    base = alto - 1

    blanco = rgb("#f4f0e4")
    ocre = rgb("#c9a86a")

    # cupula del crucero con linterna
    cupula(l, 78, base - 66, 18, 17, rgb("#6d7e86"), costillas=6, linterna=True, remate=ORO)

    l.rect(62, base - 82, 94, base - 66, blanco)
    l.rect(62, base - 82, 62, base - 66, luz(blanco, 0.1))
    l.rect(88, base - 82, 94, base - 66, sombra(blanco, 0.86))

    for dx in (-8, 0, 8):
        l.arco(78 + dx - 2, base - 68, 78 + dx + 2, 10, rgb("#2f4a60"))

    # nave con techo de teja
    volumen(l, 30, base - 56, ancho - 6, base, blanco, 1, 3)

    l.poly([(28, base - 56), (36, base - 66), (ancho - 12, base - 66), (ancho - 4, base - 56)], rgb("#b5532f"))

    for x in range(36, ancho - 12, 4):
        l.rect(x, base - 65, x, base - 57, sombra(rgb("#b5532f"), 0.8))

    # ventanas de la nave
    for x in range(78, ancho - 12, 14):
        ventana_arco(l, x, base - 8, x + 4, 22, rgb("#2f4a60"), ocre)

    # fachada con frontis barroco
    fx0, fx1 = 38, 82

    volumen(l, fx0, base - 70, fx1, base, blanco, 1, 3)

    # frontis ondulado
    l.poly([(fx0, base - 70), (fx0 + 6, base - 76), (60, base - 90), (fx1 - 6, base - 76), (fx1, base - 70)], blanco)

    l.linea(fx0, base - 70, fx0 + 6, base - 76, ocre)
    l.linea(fx0 + 6, base - 76, 60, base - 90, ocre)

    l.circulo(60, base - 78, 3, ocre)
    l.circulo(60, base - 78, 1, rgb("#2f4a60"))

    # cornisa
    l.rect(fx0 - 1, base - 72, fx1 + 1, base - 70, ocre)

    # pilastras
    for x in (fx0 + 3, fx1 - 6):
        l.rect(x, base - 68, x + 2, base - 4, sombra(blanco, 0.93))
        l.rect(x, base - 68, x, base - 4, luz(blanco, 0.1))

    # portal con arco de piedra
    l.arco(52, base - 3, 68, 34, ocre)
    l.arco(54, base - 4, 66, 30, rgb("#5a3a22"))

    l.rect(60, base - 32, 60, base - 4, rgb("#3a2518"))

    # nichos laterales
    for x in (43, 71):
        l.arco(x, base - 36, x + 5, 14, ocre)
        l.arco(x + 1, base - 37, x + 4, 11, rgb("#6a6a6a"))

    # ventanita arriba
    ventana_arco(l, 56, base - 56, 63, 14, rgb("#2f4a60"), ocre)

    # torre campanario a la izquierda
    volumen(l, 8, base - 72, 33, base, blanco, 1, 3)

    for y in (base - 36, base - 54):
        l.rect(7, y, 34, y + 1, ocre)

    ventana_arco(l, 16, base - 8, 24, 18, rgb("#2f4a60"), ocre)

    # campanario
    volumen(l, 11, base - 92, 30, base - 72, blanco, 1, 2)

    for x in (14, 22):
        l.arco(x, base - 74, x + 4, 14, rgb("#2a3550"))

    l.rect(10, base - 94, 31, base - 92, ocre)

    cupula(l, 20, base - 94, 10, 11, rgb("#7a8a9a"), costillas=3)

    l.rect(20, base - 112, 20, base - 104, ORO)
    l.rect(18, base - 109, 22, base - 109, ORO)

    # escalones
    for i in range(3):
        l.rect(46 - i * 2, base - 2 + i, 74 + i * 2, base - 2 + i,
               rgb("#e0d8c8") if i % 2 == 0 else rgb("#c4bba8"))

    return l


MONUMENTOS = [
    dict(id="floralis_generica", nombre="Floralis Generica", fn=floralis),
    dict(id="cementerio_recoleta", nombre="Cementerio de la Recoleta", fn=cementerio_recoleta),
    dict(id="basilica_pilar", nombre="Basilica Nuestra Senora del Pilar", fn=basilica_pilar),
]

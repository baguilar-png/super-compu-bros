"""
NIVEL 8 - PALERMO

    * Planetario Galileo Galilei (cupula blanca + meteorito Campo del Cielo)
    * Jardin Japones (puente rojo, torii y pagoda)
    * Rosedal (pergola blanca con rosas, lago y puente)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# PLANETARIO
# ==========================================================

def planetario():

    ancho = 150
    alto = 92

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = 72

    blanco = rgb("#f2f0ea")

    # base circular de hormigon con ventanas corridas
    volumen(l, cx - 40, base - 22, cx + 40, base, rgb("#d9d6cc"), 1, 4)

    l.rect(cx - 40, base - 22, cx + 40, base - 20, luz(blanco, 0.2))

    for x in range(cx - 36, cx + 34, 8):
        l.rect(x, base - 14, x + 4, base - 6, rgb("#3b5a86"))
        l.px(x, base - 14, VIDRIO_LUZ)

    # cupula
    cupula(l, cx, base - 22, 34, 40, blanco, costillas=9,
           c_luz=rgb("#ffffff"), c_sombra=rgb("#b9bfc8"))

    # franja de ventanitas en la cupula
    for k in range(-4, 5):

        x = cx + k * 6

        l.rect(x, base - 36, x + 1, base - 33, rgb("#7a8aa0"))

    # aro superior y mastil
    l.rect(cx - 5, base - 64, cx + 5, base - 62, rgb("#c9cdd4"))

    l.rect(cx, base - 72, cx, base - 64, rgb("#555a60"))

    # escalinata de acceso
    for i in range(3):
        l.rect(cx - 12 - i * 2, base - 2 + i, cx + 12 + i * 2, base - 2 + i,
               rgb("#e0d8c8") if i % 2 == 0 else rgb("#c4bba8"))

    # puerta
    l.rect(cx - 5, base - 14, cx + 5, base - 3, rgb("#2c3340"))

    # meteorito Campo del Cielo (masa de hierro oscuro, a la derecha)
    mx = cx + 52

    l.elipse(mx - 6, base - 12, mx + 14, base, rgb("#4a4440"))
    l.elipse(mx - 5, base - 11, mx + 3, base - 4, rgb("#6a625a"))

    for (dx, dy) in ((2, -8), (8, -4), (5, -2), (11, -7)):
        l.px(mx + dx, base + dy, rgb("#2a2624"))

    # esfera armilar chica a la izquierda
    ex = cx - 52

    l.rect(ex, base - 8, ex, base, rgb("#555a60"))

    l.circulo(ex, base - 14, 6, rgb("#8a97a8"))
    l.circulo(ex, base - 14, 4, rgb("#d9e0ea"))

    for k in (-5, 5):
        l.px(ex + k, base - 14, rgb("#555a60"))

    l.rect(ex - 6, base - 14, ex + 6, base - 14, rgb("#555a60"))
    l.rect(ex, base - 20, ex, base - 8, rgb("#555a60"))

    return l


# ==========================================================
# JARDIN JAPONES
# ==========================================================

def jardin_japones():

    ancho = 168
    alto = 84

    l = Lienzo(ancho, alto)

    base = alto - 1

    rojo = rgb("#d8392b")

    # estanque
    agua_dibujo(l, 20, base - 14, ancho - 12, base - 3, rgb("#4f93a8"), seed=11)

    # costa de piedras
    l.rect(0, base - 4, ancho - 1, base, rgb("#8a8a78"))
    l.rect(0, base - 4, ancho - 1, base - 4, rgb("#b3b29e"))

    # carpas
    for x, c in ((60, rgb("#f08a3a")), (110, rgb("#f4f1e8"))):
        l.elipse(x, base - 8, x + 5, base - 6, c)
        l.px(x + 6, base - 7, c)

    # puente rojo en arco
    for dx in range(-26, 27):

        t = abs(dx) / 26

        y = base - 22 - int(round((1 - t * t) * 12))

        l.rect(84 + dx, y, 84 + dx, y + 1, rojo)
        l.px(84 + dx, y, luz(rojo, 0.35))

        # baranda
        l.px(84 + dx, y - 4, rgb("#8a2a20"))

        if dx % 5 == 0:
            l.rect(84 + dx, y - 4, 84 + dx, y, rgb("#8a2a20"))

        # apoyos
        if dx in (-20, -8, 8, 20):
            l.rect(84 + dx, y + 2, 84 + dx, base - 8, rgb("#8a2a20"))

    # farol de piedra
    fx = 28

    l.rect(fx - 1, base - 18, fx + 1, base - 5, rgb("#9a9a8a"))
    l.rect(fx - 3, base - 22, fx + 3, base - 19, rgb("#bcbcaa"))
    l.rect(fx - 1, base - 20, fx + 1, base - 20, rgb("#f4e7a3"))
    l.poly([(fx - 5, base - 22), (fx, base - 27), (fx + 5, base - 22)], rgb("#8a8a7a"))

    # torii rojo
    tx = 140

    l.rect(tx - 14, base - 40, tx + 14, base - 38, rgb("#2a2624"))
    l.rect(tx - 16, base - 44, tx + 16, base - 41, rojo)
    l.rect(tx - 16, base - 44, tx + 16, base - 44, luz(rojo, 0.3))
    l.px(tx - 17, base - 45, rojo)
    l.px(tx + 17, base - 45, rojo)

    for dx in (-11, 11):
        l.rect(tx + dx - 1, base - 38, tx + dx + 1, base - 4, rojo)
        l.rect(tx + dx - 1, base - 38, tx + dx - 1, base - 4, luz(rojo, 0.2))

    l.rect(tx - 11, base - 34, tx + 11, base - 33, rojo)

    # pagoda de tres pisos
    px_ = 14

    for i, (w, h) in enumerate(((16, 10), (13, 9), (10, 8))):

        y = base - 6 - i * 17

        # cuerpo
        l.rect(px_ - w // 2 + 2, y - h, px_ + w // 2 - 2, y, rgb("#efe7d4"))
        l.rect(px_ - w // 2 + 2, y - h, px_ - w // 2 + 2, y, rgb("#ffffff"))
        l.rect(px_ - 1, y - h + 2, px_ + 1, y - 2, rgb("#5a3a22"))

        # techo curvo hacia arriba
        l.poly([(px_ - w // 2 - 3, y - h + 1), (px_ - w // 2 + 1, y - h - 3),
                (px_ + w // 2 - 1, y - h - 3), (px_ + w // 2 + 3, y - h + 1)], rgb("#4a5a66"))

        l.rect(px_ - w // 2 + 1, y - h - 3, px_ + w // 2 - 1, y - h - 3, luz(rgb("#4a5a66"), 0.3))

    l.rect(px_, base - 6 - 3 * 17 - 6, px_, base - 6 - 3 * 17 + 4, ORO)

    # bonsai y cerezo en flor
    arbol(l, 52, base - 3, 34, "jacaranda", seed=3)

    for k in range(14):

        l.px(46 + (k * 7) % 14, base - 28 - (k * 5) % 10, rgb("#f6c6d8"))

    arbusto(l, 100, base - 3, 12, 8, rgb("#2f7f3f"))

    return l


# ==========================================================
# ROSEDAL
# ==========================================================

def rosedal():

    ancho = 168
    alto = 76

    l = Lienzo(ancho, alto)

    base = alto - 1

    blanco = rgb("#f4f1e8")

    # lago
    agua_dibujo(l, 0, base - 15, ancho - 1, base - 5, rgb("#4f93c9"), seed=2)

    l.rect(0, base - 6, ancho - 1, base, rgb("#c9bfa0"))
    l.rect(0, base - 6, ancho - 1, base - 6, rgb("#e0d8bc"))

    # puente de piedra con arcos (Puente de los Lagos)
    for dx in range(-30, 31):

        t = abs(dx) / 30

        y = base - 16 - int(round((1 - t * t) * 7))

        l.rect(40 + dx, y, 40 + dx, base - 6, rgb("#d8d0be"))
        l.px(40 + dx, y, rgb("#f2eee2"))

    for cxa in (28, 40, 52):

        l.arco(cxa - 4, base - 6, cxa + 4, 8, rgb("#4f93c9"))

    for x in range(10, 71, 4):
        l.rect(x, base - 26 + abs(x - 40) // 6 * 0, x, base - 20, rgb("#bdb5a2"))

    # cisnes
    for x in (96, 118):

        l.elipse(x, base - 10, x + 6, base - 7, blanco)
        l.rect(x + 5, base - 15, x + 6, base - 9, blanco)
        l.px(x + 7, base - 15, ORO)

    # pergola blanca cubierta de rosas (a la derecha)
    px0, px1 = 82, 160

    y_top = base - 46

    # columnas
    for x in range(px0, px1 + 1, 13):

        l.rect(x, y_top, x + 2, base - 6, blanco)
        l.rect(x, y_top, x, base - 6, rgb("#ffffff"))
        l.rect(x + 2, y_top, x + 2, base - 6, rgb("#bfc6cf"))

    # vigas
    l.rect(px0 - 3, y_top - 3, px1 + 5, y_top - 1, blanco)
    l.rect(px0 - 3, y_top - 3, px1 + 5, y_top - 3, rgb("#ffffff"))

    for x in range(px0, px1 + 1, 4):
        l.rect(x, y_top - 6, x + 1, y_top - 4, blanco)

    # enredadera con rosas
    r = random.Random(4)

    for x in range(px0 - 2, px1 + 5):

        for y in range(y_top - 9, y_top + 8):

            if r.random() < 0.35 - abs(y - (y_top - 2)) * 0.03:

                l.px(x, y, rgb("#3a8a3a") if r.random() < 0.7 else rgb("#2a6f2f"))

    for _ in range(46):

        x = r.randint(px0 - 2, px1 + 4)
        y = r.randint(y_top - 9, y_top + 7)

        l.px(x, y, r.choice([rgb("#e0405a"), rgb("#f27a95"), rgb("#f4a0b8"), rgb("#fff0f4")]))

    # bancos y canteros de rosas
    for x in range(92, 156, 12):

        banco(l, x, base - 6, 7, rgb("#4a3a2a"))

    for x in range(86, 160, 6):

        l.rect(x, base - 12, x + 2, base - 8, rgb("#3a8a3a"))
        l.px(x + 1, base - 12, r.choice([rgb("#e0405a"), rgb("#f4a0b8"), rgb("#fff0f4")]))

    # sauce llorón a la izquierda
    arbol(l, 8, base - 6, 40, "sauce")

    return l


MONUMENTOS = [
    dict(id="planetario", nombre="Planetario Galileo Galilei", fn=planetario),
    dict(id="jardin_japones", nombre="Jardin Japones", fn=jardin_japones),
    dict(id="rosedal", nombre="Rosedal de Palermo", fn=rosedal),
]

"""
Edificios de relleno, objetos de la calle y vehiculos para los fondos.

Todas las funciones de edificio tienen la misma forma:

    estilo(w, h, r, c) -> Lienzo de w x h pixeles

con la base del edificio en la ultima fila. 'r' es un random.Random y
'c' un dict de colores: fachada, borde, techo (y a veces extra).
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# AYUDAS
# ==========================================================

def _marco_ventana(l, x, y, w, h, marco, vidrio=VIDRIO, persiana=None,
                   cruz=False):
    """Ventana rectangular con marco; (x, y) = esquina de arriba."""

    l.rect(x - 1, y - 1, x + w, y + h, marco)
    l.rect(x, y, x + w - 1, y + h - 1, vidrio)

    if w >= 3 and h >= 4:
        l.px(x, y, VIDRIO_LUZ)

    if cruz and w >= 4:
        l.rect(x + w // 2, y, x + w // 2, y + h - 1, marco)

    if persiana is not None:
        l.rect(x, y, x + w - 1, y + h // 3, persiana)


def _reja_ventana(l, x, y, w, h, c=None):

    c = c or NEGRO

    for k in range(x, x + w, 2):
        l.rect(k, y, k, y + h - 1, c)


def _aire_acond(l, x, y):

    l.rect(x, y, x + 2, y + 1, rgb("#d8d8d4"))
    l.px(x + 1, y, rgb("#9a9a96"))


def _tanque(l, x, y_base, ancho=6, alto=5):
    """Tanque de agua de azotea, tipico de Buenos Aires."""

    l.rect(x, y_base - alto, x + ancho - 1, y_base, rgb("#8a8f94"))
    l.rect(x, y_base - alto, x, y_base, rgb("#b4b8bc"))
    l.rect(x + ancho - 1, y_base - alto, x + ancho - 1, y_base, rgb("#5d6268"))
    l.rect(x, y_base - alto - 1, x + ancho - 1, y_base - alto - 1, rgb("#6d7278"))
    l.rect(x + 1, y_base + 1, x + 1, y_base + 2, rgb("#444a50"))
    l.rect(x + ancho - 2, y_base + 1, x + ancho - 2, y_base + 2, rgb("#444a50"))


def _antena(l, x, y_base, alto=7):

    c = rgb("#3a3d45")

    l.rect(x, y_base - alto, x, y_base, c)
    l.rect(x - 2, y_base - alto + 1, x + 2, y_base - alto + 1, c)
    l.rect(x - 1, y_base - alto + 3, x + 1, y_base - alto + 3, c)


def _ropa_tendida(l, x0, x1, y, r):

    colores = [BLANCO, ROJO, AMARILLO_BOCA, rgb("#e88fb0"), CELESTE_ARG]

    for k in range(x0, x1, 3):

        if r.random() < 0.7:
            l.rect(k, y, k + 1, y + 3, r.choice(colores))

    l.rect(x0, y - 1, x1, y - 1, rgb("#5a5a5a"))


# ==========================================================
# EDIFICIOS "FRANCESES" (Barrio Norte, Recoleta, Congreso, Retiro)
# ==========================================================

def frances(w, h, r, c):
    """Edificio de la Belle Epoque: zocalo rusticado, balcones, mansarda."""

    l = Lienzo(w, h)

    base = h - 1

    col = c["fachada"]
    borde = c["borde"]
    pizarra = c.get("techo", rgb("#4d5762"))

    mans = 13
    cuerpo = mans + 2

    # mansarda con buhardillas
    l.poly([(0, cuerpo), (3, 3), (w - 4, 3), (w - 1, cuerpo)], pizarra)
    l.rect(3, 3, w - 4, 3, luz(pizarra, 0.3))

    for y in range(6, cuerpo, 2):
        l.rect(4, y, w - 5, y, sombra(pizarra, 0.84))

    for x in range(5, w - 9, 11):

        l.poly([(x - 1, 8), (x + 2, 4), (x + 5, 8)], luz(pizarra, 0.18))
        l.rect(x - 1, 8, x + 5, 13, borde)
        l.rect(x, 9, x + 4, 13, VIDRIO)
        l.px(x, 9, VIDRIO_LUZ)

    # chimenea
    cx = r.randint(6, max(7, w - 10))

    l.rect(cx, 0, cx + 2, 4, rgb("#9a6a55"))
    l.rect(cx, 0, cx + 2, 0, rgb("#5a4a44"))

    # cuerpo
    volumen(l, 0, cuerpo, w - 1, base, col, 1, 2, techo=False)

    cornisa(l, 0, w - 1, cuerpo, borde, 2, 1)

    zoc = 14

    pisos = max(2, (base - zoc - cuerpo - 3) // 12)

    # pisos con ventanas y balcones
    for k in range(pisos):

        yb = base - zoc - k * 12

        l.rect(0, yb, w - 1, yb, luz(col, 0.22))

        for x in range(4, w - 6, 8):

            _marco_ventana(l, x, yb - 10, 4, 8, borde, persiana=None)

        if k % 2 == 0 or k == pisos - 1:
            balcon(l, 1, w - 2, yb - 4, NEGRO, 2)

    # planta baja: zocalo rusticado
    l.rect(0, base - zoc + 1, w - 1, base, sombra(col, 0.9))

    for y in range(base - zoc + 3, base, 3):
        l.rect(0, y, w - 1, y, sombra(col, 0.78))

    l.rect(0, base - zoc + 1, w - 1, base - zoc + 1, luz(col, 0.3))

    mid = w // 2

    # puerta principal con arco
    ventana_arco(l, mid - 3, base, mid + 3, 12, rgb("#4a2f1c"), borde)
    l.rect(mid, base - 11, mid, base, rgb("#2e1c10"))
    l.px(mid - 2, base - 5, ORO)
    l.px(mid + 2, base - 5, ORO)

    # ventanas con reja a los lados
    for x in range(4, w - 6, 8):

        if abs(x + 2 - mid) > 6:

            _marco_ventana(l, x, base - 10, 4, 6, borde, VIDRIO_OSC)
            _reja_ventana(l, x, base - 10, 4, 6)

    return l


# ==========================================================
# ITALIANIZANTE (San Telmo, Monserrat, Plaza de Mayo, Once)
# ==========================================================

def italianizante(w, h, r, c):
    """Fachada con parapeto de balaustres, cornisa y ventanas con arco."""

    l = Lienzo(w, h)

    base = h - 1

    col = c["fachada"]
    borde = c["borde"]

    volumen(l, 0, 3, w - 1, base, col, 1, 2, techo=False)

    # balaustrada
    l.rect(0, 0, w - 1, 0, luz(col, 0.3))

    for x in range(1, w - 1, 2):
        l.rect(x, 1, x, 4, luz(col, 0.25))

    l.rect(0, 5, w - 1, 6, borde)
    l.rect(0, 5, w - 1, 5, luz(borde, 0.3))

    # pinaculos
    for x in (0, w - 2):
        l.rect(x, 0, x + 1, 5, luz(col, 0.15))

    cornisa(l, 0, w - 1, 7, borde, 2, 1)

    zoc = 16

    pisos = max(1, (base - zoc - 11) // 13)

    for k in range(pisos):

        yb = base - zoc - k * 13

        for x in range(4, w - 6, 8):

            ventana_arco(l, x, yb - 1, x + 3, 10, VIDRIO, borde)

        l.rect(0, yb + 1, w - 1, yb + 1, sombra(col, 0.82))

        if k == 0:
            balcon(l, 2, w - 3, yb - 4, NEGRO, 2)

    # pilastras
    for x in range(0, w, 14):
        l.rect(x, 9, x, base, luz(col, 0.18))

    # planta baja: arcos
    l.rect(0, base - zoc + 2, w - 1, base, sombra(col, 0.9))
    l.rect(0, base - zoc + 2, w - 1, base - zoc + 2, luz(col, 0.3))

    arcos = max(1, (w - 4) // 12)

    paso = (w - 4) / arcos

    for i in range(arcos):

        x0 = int(2 + i * paso + 2)

        puerta = (i == arcos // 2)

        ventana_arco(
            l, x0, base, x0 + int(paso) - 5, 14 if puerta else 10,
            rgb("#4a2f1c") if puerta else VIDRIO_OSC, luz(col, 0.25)
        )

    return l


# ==========================================================
# CASA BAJA (San Telmo, Monserrat, Constitucion)
# ==========================================================

def casa_baja(w, h, r, c):
    """Casona antigua de uno o dos pisos, con parapeto y rejas."""

    l = Lienzo(w, h)

    base = h - 1

    col = c["fachada"]
    borde = c["borde"]

    # techo de tejas que asoma detras del parapeto
    if r.random() < 0.5:

        l.poly([(2, 5), (w // 2, 0), (w - 3, 5)], TEJA)
        l.linea(2, 5, w // 2, 0, luz(TEJA, 0.3))

    volumen(l, 0, 4, w - 1, base, col, 1, 2, techo=False)

    l.rect(0, 4, w - 1, 6, borde)
    l.rect(0, 4, w - 1, 4, luz(borde, 0.3))

    for x in range(1, w - 1, 3):
        l.rect(x, 7, x + 1, 8, luz(col, 0.18))

    pisos = 2 if h >= 38 else 1

    # ventanas del piso de arriba
    if pisos == 2:

        for x in range(4, w - 6, 9):

            _marco_ventana(l, x, 11, 5, 9, borde, persiana=c.get("extra"))
            balcon(l, x - 1, x + 5, 17, NEGRO, 2)

    # planta baja
    yv = base - 17

    n = max(1, (w - 8) // 11)

    paso = (w - 4) / n

    puerta_i = r.randint(0, n - 1)

    for i in range(n):

        x0 = int(2 + i * paso + (paso - 6) / 2)

        if i == puerta_i:

            ventana_arco(l, x0, base, x0 + 5, 14, rgb("#5a3a22"), borde)
            l.rect(x0 + 2, base - 12, x0 + 2, base, rgb("#2e1c10"))
            l.px(x0 + 4, base - 6, ORO)

        else:

            _marco_ventana(l, x0, yv, 6, 11, borde, VIDRIO_OSC, persiana=c.get("extra"))
            _reja_ventana(l, x0, yv, 6, 11)

    l.rect(0, base - 2, w - 1, base, sombra(col, 0.85))

    return l


# ==========================================================
# CONVENTILLO DE CHAPA (La Boca)
# ==========================================================

def conventillo(w, h, r, c):
    """Casa de chapa acanalada con balcon de madera, muy colorida."""

    l = Lienzo(w, h)

    base = h - 1

    col = c["fachada"]
    borde = c["borde"]

    p = pal(col)

    techo_y = 6 if h >= 40 else 5

    volumen(l, 0, techo_y, w - 1, base, col, 1, 2, techo=False)

    # chapa acanalada
    for x in range(2, w - 2, 3):
        l.rect(x, techo_y + 2, x, base - 3, p["s"])

    # techo
    forma = r.choice(["dos_aguas", "una_agua", "recto"])

    if forma == "dos_aguas":

        mx = w // 2

        l.poly([(-1, techo_y + 1), (mx, 0), (w, techo_y + 1)], rgb("#9aa3ad"))

        for k in range(1, w - 1, 3):

            ya = abs(k - mx) * (techo_y) // max(1, w // 2)

            l.rect(k, ya + 1, k, techo_y, rgb("#7e8893"))

    elif forma == "una_agua":

        l.poly([(0, techo_y + 1), (0, 0), (w - 1, 3), (w - 1, techo_y + 1)], rgb("#9aa3ad"))

        for k in range(1, w - 1, 3):
            l.rect(k, 2 + k // 12, k, techo_y, rgb("#7e8893"))

    else:

        l.rect(0, techo_y - 2, w - 1, techo_y + 1, borde)
        l.rect(0, techo_y - 2, w - 1, techo_y - 2, luz(borde))

    # franja entre pisos
    ymed = base - 20

    l.rect(0, ymed, w - 1, ymed + 1, borde)

    # balcon de madera
    madera = rgb("#7a4a2a")

    l.rect(-1, ymed, w, ymed + 1, madera)
    l.rect(-1, ymed, w, ymed, luz(madera, 0.2))

    for x in range(0, w, 2):
        l.rect(x, ymed - 6, x, ymed - 1, madera)

    l.rect(-1, ymed - 7, w, ymed - 6, madera)
    l.rect(-1, ymed - 7, w, ymed - 7, luz(madera, 0.25))

    # puertas-ventana arriba
    n = 2 if w >= 28 else 1

    paso = (w - 2) / n

    for i in range(n):

        vx = int(1 + i * paso + (paso - 6) / 2)

        _marco_ventana(l, vx, ymed - 16, 6, 14, borde, cruz=True)

    # planta baja: puerta y ventana
    l.rect(3, base - 13, 8, base, rgb("#5a3a22"))
    l.rect(3, base - 13, 8, base - 13, borde)
    l.px(7, base - 6, ORO)

    if w >= 20:
        _marco_ventana(l, w - 12, base - 13, 7, 9, borde, cruz=True)

    # ropa colgada
    if r.random() < 0.5:
        _ropa_tendida(l, 3, w - 4, ymed - 5, r)

    return l


# ==========================================================
# TORRE DE VIDRIO / DE HORMIGON (Puerto Madero, Retiro, Abasto)
# ==========================================================

def torre_vidrio(w, h, r, c):

    l = Lienzo(w, h)

    base = h - 1

    col = c["fachada"]

    p = pal(col)

    # retranqueo superior
    ret = r.choice([0, 0, 1])

    cuerpo_x0 = 0
    cuerpo_x1 = w - 1

    top = 10

    l.rect(cuerpo_x0, top, cuerpo_x1, base, p["b"])

    # reflejos en diagonal
    for y in range(top, base + 1):

        for x in range(cuerpo_x0, cuerpo_x1 + 1):

            d = (x * 2 + y) % 23

            if d < 2:
                l.px(x, y, luz(col, 0.22))
            elif d == 12:
                l.px(x, y, sombra(col, 0.9))

    # entrepisos y parantes
    for y in range(top + 3, base, 3):
        l.rect(cuerpo_x0, y, cuerpo_x1, y, sombra(col, 0.78))

    for x in range(cuerpo_x0 + 3, cuerpo_x1, 4):
        l.rect(x, top, x, base, luz(col, 0.12))

    l.rect(cuerpo_x0, top, cuerpo_x0, base, p["l"])
    l.rect(cuerpo_x1 - 1, top, cuerpo_x1, base, p["s"])

    # corona
    l.rect(cuerpo_x0, top - 1, cuerpo_x1, top, sombra(col, 0.65))

    if ret:

        l.rect(2, top - 4, w - 3, top - 2, sombra(col, 0.7))

    _antena(l, w // 2, top - 3 if ret else top - 1, 7 if not ret else 6)

    l.px(w // 2, 0, ROJO)

    # planta baja: hall vidriado y columnas
    l.rect(0, base - 8, w - 1, base, rgb("#2a3342"))

    for x in range(2, w - 2, 5):
        l.rect(x, base - 7, x + 3, base - 1, VIDRIO_LUZ if (x // 5) % 2 else VIDRIO)

    return l


def torre_hormigon(w, h, r, c):
    """Edificio de oficinas de hormigon con franjas de ventanas."""

    l = Lienzo(w, h)

    base = h - 1

    col = c["fachada"]

    volumen(l, 0, 9, w - 1, base, col, 1, 2, techo=False)

    for y in range(14, base - 10, 6):

        l.rect(1, y, w - 3, y + 2, VIDRIO)
        l.rect(1, y, w - 3, y, VIDRIO_LUZ)

        for x in range(5, w - 3, 6):
            l.rect(x, y, x, y + 2, sombra(col, 0.8))

        l.rect(0, y + 3, w - 1, y + 3, luz(col, 0.18))

    l.rect(0, 9, w - 1, 11, sombra(col, 0.8))

    _tanque(l, 3, 8, 5, 3)

    if w > 16:
        _antena(l, w - 6, 9, 8)

    l.rect(0, base - 8, w - 1, base, rgb("#2d3646"))

    for x in range(2, w - 2, 6):
        l.rect(x, base - 7, x + 3, base - 1, VIDRIO)

    return l


# ==========================================================
# ART DECO
# ==========================================================

def art_deco(w, h, r, c):

    l = Lienzo(w, h)

    base = h - 1

    col = c["fachada"]
    borde = c["borde"]

    p = pal(col)

    # tres cuerpos que se achican hacia arriba
    cuerpos = [(0, w - 1, 0.55), (3, w - 4, 0.3), (7, w - 8, 0.15)]

    y_actual = base

    util = h - 14

    for (xa, xb, frac) in cuerpos:

        alto = int(util * frac)

        yt = y_actual - alto

        l.rect(xa, yt, xb, y_actual, p["b"])
        l.rect(xa, yt, xa, y_actual, p["l"])
        l.rect(xb - 1, yt, xb, y_actual, p["s"])

        # pilares verticales claros y ventanas entre medio
        for x in range(xa + 2, xb - 1, 4):

            l.rect(x, yt + 2, x, y_actual - 1, luz(col, 0.3))

            l.rect(x + 1, yt + 3, x + 2, y_actual - 2, VIDRIO)

        l.rect(xa - 1, yt, xb + 1, yt + 1, borde)

        y_actual = yt

    # remate
    cx = w // 2

    l.rect(cx - 1, y_actual - 6, cx + 1, y_actual, borde)
    l.rect(cx, y_actual - 12, cx, y_actual - 6, borde)

    # planta baja
    l.rect(0, base - 7, w - 1, base, sombra(col, 0.8))

    for x in range(2, w - 2, 6):
        l.rect(x, base - 6, x + 3, base, rgb("#2a3342"))

    return l


# ==========================================================
# GALPON DE LADRILLO (Puerto Madero, Barracas, Constitucion)
# ==========================================================

def galpon(w, h, r, c):
    """Deposito portuario de ladrillo con arcos y cornisa blanca."""

    l = Lienzo(w, h)

    base = h - 1

    ladrillo = c["fachada"]
    borde = c.get("borde", rgb("#e8dcc4"))

    cima = 8

    ladrillos(l, 0, cima, w - 1, base, ladrillo)

    # techo a dos aguas de chapa
    mx = w // 2

    l.poly([(-1, cima + 1), (mx, 0), (w, cima + 1)], rgb("#5d6670"))
    l.linea(0, cima, mx, 1, luz(rgb("#5d6670"), 0.3))

    # cornisa blanca
    l.rect(0, cima, w - 1, cima + 1, borde)
    l.rect(0, cima + 2, w - 1, cima + 2, sombra(borde, 0.7))

    # arcos de ventanas, en dos filas
    for fila in range(2):

        yb = base - 4 - fila * 17

        if fila == 1 and base - 24 < cima + 6:
            continue

        for x in range(4, w - 8, 9):

            ventana_arco(l, x, yb, x + 4, 12, VIDRIO, borde)

            l.rect(x, yb - 8, x + 4, yb - 8, borde)

    # portones de madera
    for dx in (w // 3, 2 * w // 3):

        l.rect(dx - 3, base - 10, dx + 3, base, rgb("#3a2518"))
        l.rect(dx - 3, base - 10, dx + 3, base - 10, borde)
        l.rect(dx, base - 10, dx, base, rgb("#241408"))

    # zocalo de piedra
    l.rect(0, base - 1, w - 1, base, rgb("#8a8478"))

    # chimenea
    if r.random() < 0.4:

        l.rect(w - 9, 0, w - 7, 6, rgb("#8f4a38"))

    return l


# ==========================================================
# FABRICA CON TECHO DE DIENTES DE SIERRA (Barracas, Constitucion)
# ==========================================================

def fabrica(w, h, r, c):

    l = Lienzo(w, h)

    base = h - 1

    ladrillo = c["fachada"]

    ladrillos(l, 0, 18, w - 1, base, ladrillo)

    # dientes de sierra
    paso = 10

    for x in range(0, w - 1, paso):

        l.poly([(x, 18), (x, 11), (x + paso - 1, 18)], rgb("#6d7680"))
        l.rect(x, 11, x, 18, VIDRIO_LUZ)

    l.rect(0, 17, w - 1, 18, rgb("#d8cdb4"))

    # ventanales altos
    for x in range(3, w - 6, 8):

        l.rect(x, 22, x + 3, base - 6, VIDRIO)
        l.rect(x, 22, x + 3, 22, rgb("#d8cdb4"))

    l.rect(3, base - 10, 10, base, rgb("#2e3a2e"))

    # chimenea alta
    cx = w - 6

    l.rect(cx, 0, cx + 3, 12, sombra(ladrillo, 0.85))
    l.rect(cx, 0, cx + 3, 0, rgb("#2a2a2a"))
    l.rect(cx, 4, cx + 3, 5, rgb("#d8cdb4"))

    return l


# ==========================================================
# EDIFICIO DE DEPARTAMENTOS CON MEDIANERA (barrios populares)
# ==========================================================

def departamentos(w, h, r, c):
    """Torre de departamentos de 5-9 pisos con balcones y azotea."""

    l = Lienzo(w, h)

    base = h - 1

    col = c["fachada"]
    borde = c["borde"]

    volumen(l, 0, 11, w - 1, base, col, 1, 2, techo=False)

    # azotea con baranda
    l.rect(0, 9, w - 1, 11, borde)
    l.rect(0, 9, w - 1, 9, luz(borde, 0.3))

    # cuarto de maquinas y tanque
    if r.random() < 0.6:
        _tanque(l, r.randint(3, max(4, w - 10)), 8, 6, 5)

    if r.random() < 0.5:
        _antena(l, r.randint(3, max(4, w - 4)), 9, 8)

    zoc = 12

    pisos = (base - zoc - 12) // 10

    for k in range(pisos):

        yb = base - zoc - k * 10

        for x in range(3, w - 5, 7):

            _marco_ventana(l, x, yb - 7, 4, 6, borde, persiana=r.choice([None, None, rgb("#d8d0bc"), rgb("#7a6a52")]))

        # balcon corrido
        l.rect(1, yb - 1, w - 2, yb, sombra(col, 0.8))

        if k % 2 == 0:
            l.rect(1, yb - 3, w - 2, yb - 3, NEGRO)

        if r.random() < 0.4:
            _aire_acond(l, r.randint(2, max(3, w - 6)), yb - 6)

    # planta baja con local
    l.rect(0, base - zoc + 1, w - 1, base, sombra(col, 0.9))

    l.rect(2, base - 9, w - 3, base, rgb("#2a3342"))

    for x in range(3, w - 4, 6):
        l.rect(x, base - 8, x + 3, base - 1, VIDRIO_LUZ if (x // 6) % 2 else VIDRIO)

    l.rect(1, base - 11, w - 2, base - 10, r.choice([ROJO, rgb("#2f8f5a"), AZUL_BOCA, rgb("#e0944f")]))

    return l


# ==========================================================
# MEDIANERA CON MURAL (Abasto, Palermo, La Boca)
# ==========================================================

def mural(w, h, r, c):
    """Pared ciega alta con un mural de colores."""

    l = Lienzo(w, h)

    base = h - 1

    col = c["fachada"]

    tipo = c.get("mural", "abstracto")

    volumen(l, 0, 0, w - 1, base, col, 1, 2, techo=False)

    for y in range(8, base, 12):
        l.rect(0, y, w - 1, y, sombra(col, 0.93))

    if tipo == "tango":

        # fondo rojo oscuro y dos siluetas bailando
        l.rect(2, 8, w - 3, base - 6, rgb("#7a1f2a"))
        l.rect(2, 8, w - 3, 10, rgb("#c0392b"))

        cx = w // 2

        negro = rgb("#17131c")

        # el hombre
        l.rect(cx - 5, base - 40, cx - 2, base - 12, negro)
        l.rect(cx - 6, base - 46, cx - 2, base - 41, negro)
        l.rect(cx - 7, base - 44, cx - 7, base - 43, negro)
        l.rect(cx - 5, base - 12, cx - 4, base - 6, negro)
        l.rect(cx - 2, base - 12, cx - 1, base - 6, negro)

        # la mujer
        l.rect(cx + 1, base - 38, cx + 4, base - 22, rgb("#e8c04a"))
        l.poly([(cx, base - 22), (cx + 5, base - 22), (cx + 8, base - 8), (cx - 2, base - 10)], rgb("#e8c04a"))
        l.rect(cx + 1, base - 44, cx + 4, base - 39, rgb("#e0b08a"))
        l.rect(cx + 1, base - 45, cx + 4, base - 43, negro)

        # manos unidas
        l.linea(cx - 2, base - 36, cx + 2, base - 34, rgb("#e0b08a"))

        # letras
        l.texto(cx - ancho_texto("TANGO") // 2, 13, "TANGO", rgb("#f4e7a3"))

    elif tipo == "boca":

        l.rect(2, 4, w - 3, base - 8, AZUL_BOCA)

        for y in range(base - 52, base - 28):

            if y > 6:
                l.rect(2, y, w - 3, y, AMARILLO_BOCA)

        l.rect(2, base - 56, w - 3, base - 52, AMARILLO_BOCA)

        for k in range(6):
            l.px(8 + k * 5 % (w - 12), 9 + (k * 7) % 25, BLANCO)

        l.texto(w // 2 - ancho_texto("BOCA") // 2, base - 46, "BOCA", AZUL_BOCA)

    else:

        # abstracto de colores fuertes
        paleta = [ROJO, AMARILLO_BOCA, CELESTE_ARG, rgb("#2f8f5a"), rgb("#e88fb0"), rgb("#f08a2e")]

        for _ in range(6):

            x = r.randint(2, max(3, w - 14))
            y = r.randint(4, max(6, base - 30))

            cc = r.choice(paleta)

            forma = r.random()

            if forma < 0.4:
                l.circulo(x + 5, y + 5, r.randint(3, 6), cc)
            elif forma < 0.7:
                l.rect(x, y, x + r.randint(5, 11), y + r.randint(5, 11), cc)
            else:
                l.poly([(x, y + 9), (x + 5, y), (x + 10, y + 9)], cc)

        l.rect(2, base - 14, w - 3, base - 8, NEGRO)

    # azotea
    l.rect(0, 0, w - 1, 1, sombra(col, 0.75))

    return l


# ==========================================================
# LOCAL COMERCIAL CON CARTELES (Once, Abasto, Corrientes, Congreso)
# ==========================================================

def local_comercial(w, h, r, c):
    """Edificio de 2-3 pisos con un gran cartel en la planta baja."""

    l = Lienzo(w, h)

    base = h - 1

    col = c["fachada"]
    borde = c["borde"]

    volumen(l, 0, 3, w - 1, base, col, 1, 2, techo=False)

    cornisa(l, 0, w - 1, 3, borde, 2, 1)

    pisos = max(1, (base - 22 - 8) // 12)

    for k in range(pisos):

        yb = base - 22 - k * 12

        for x in range(3, w - 5, 8):

            _marco_ventana(l, x, yb - 9, 4, 8, borde,
                           persiana=r.choice([None, rgb("#cfc6b0"), rgb("#6a8a6a")]))

        l.rect(0, yb + 1, w - 1, yb + 1, sombra(col, 0.85))

    # planta baja
    l.rect(0, base - 21, w - 1, base, rgb("#2a2f3a"))

    textos = c.get("textos") or ["OFERTA"]

    texto = r.choice(textos)

    tw = ancho_texto(texto)

    # si el texto no entra, se usa uno corto
    if tw + 6 > w:
        texto = "SALE"
        tw = ancho_texto(texto)

    fondo_cartel = r.choice([ROJO, rgb("#1f4a8f"), rgb("#2f8f5a"), rgb("#e0944f"), rgb("#7a2f8f"), rgb("#1d1a24")])

    luz_cartel = r.choice([BLANCO, rgb("#ffe27a")])

    l.rect(1, base - 20, w - 2, base - 11, fondo_cartel)
    l.marco(1, base - 20, w - 2, base - 11, luz(fondo_cartel, 0.4))

    l.texto(w // 2 - tw // 2, base - 18, texto, luz_cartel)

    # vidriera y puerta
    l.rect(2, base - 9, w - 3, base, VIDRIO_OSC)

    for x in range(3, w - 4, 7):

        l.rect(x, base - 8, x + 3, base - 1, r.choice([rgb("#c9607a"), rgb("#e8c04a"), rgb("#6aa6d8"), rgb("#f4f1e8"), rgb("#8a5ac8")]))

    l.rect(w - 8, base - 9, w - 4, base, rgb("#5a3a22"))

    # toldo
    if r.random() < 0.5:

        for x in range(0, w, 2):
            l.rect(x, base - 12, x + 1, base - 10, ROJO if (x // 2) % 2 else BLANCO)

    return l


# ==========================================================
# EDIFICIO DE FONDO (segundo plano, borroso)
# ==========================================================

def fondo_edificio(w, h, r, c):
    """Siluetas simples con ventanitas, para el plano de atras."""

    l = Lienzo(w, h)

    base = h - 1

    col = c["fachada"]

    l.rect(0, 6, w - 1, base, col)
    l.rect(0, 6, 0, base, luz(col, 0.15))
    l.rect(w - 1, 6, w - 1, base, sombra(col, 0.85))

    techo = r.random()

    if techo < 0.25 and w > 12:

        l.poly([(0, 6), (w // 2, 0), (w - 1, 6)], sombra(col, 0.8))

    elif techo < 0.5:

        l.rect(2, 2, 5, 6, sombra(col, 0.8))

    for y in range(10, base - 6, 7):

        for x in range(3, w - 4, 6):
            l.rect(x, y, x + 2, y + 3, VIDRIO)

    return l


# ==========================================================
# OBJETOS DE LA CALLE (nuevos)
# ==========================================================

def semaforo(l, x, y_base):

    c = rgb("#2a2f35")

    l.rect(x, y_base - 24, x, y_base, c)
    l.rect(x - 1, y_base - 1, x + 1, y_base, c)
    l.rect(x - 1, y_base - 31, x + 1, y_base - 25, rgb("#1d1a24"))
    l.px(x, y_base - 30, ROJO)
    l.px(x, y_base - 28, rgb("#f0c020"))
    l.px(x, y_base - 26, rgb("#30c060"))


def cesto(l, x, y_base):

    l.rect(x, y_base - 4, x + 3, y_base, rgb("#3c4a3c"))
    l.rect(x - 1, y_base - 5, x + 4, y_base - 5, rgb("#566656"))


def puesto_feria(l, x, y_base, color=None, ancho=18):
    """Puesto de feria con sombrilla y mercaderia."""

    color = color or ROJO

    # sombrilla
    mid = x + ancho // 2

    l.rect(mid, y_base - 22, mid, y_base, rgb("#6b6b6b"))

    for dy in range(0, 6):

        hw = ancho // 2 - dy * 1 + 1

        cc = color if dy % 2 == 0 else luz(color, 0.5)

        l.rect(mid - hw - 2, y_base - 27 + dy, mid + hw + 2, y_base - 27 + dy, cc)

    # mesa y objetos
    l.rect(x, y_base - 7, x + ancho, y_base - 6, rgb("#7a5230"))
    l.rect(x + 1, y_base - 6, x + 1, y_base, rgb("#5a3a22"))
    l.rect(x + ancho - 1, y_base - 6, x + ancho - 1, y_base, rgb("#5a3a22"))

    objetos = [ORO, rgb("#8a5ac8"), rgb("#e88fb0"), CELESTE_ARG, rgb("#f4f1e8"), rgb("#2f8f5a")]

    for i in range(1, ancho - 1, 3):

        l.rect(x + i, y_base - 10 - (i % 3), x + i + 1, y_base - 8, objetos[(i // 3) % len(objetos)])


def carrito_chori(l, x, y_base):
    """Parrilla ambulante de choripan, con humito."""

    l.rect(x, y_base - 9, x + 13, y_base - 5, rgb("#7a2f23"))
    l.rect(x, y_base - 9, x + 13, y_base - 9, rgb("#b0503c"))

    l.rect(x + 1, y_base - 5, x + 1, y_base, rgb("#3a3a3a"))
    l.rect(x + 12, y_base - 5, x + 12, y_base, rgb("#3a3a3a"))

    l.circulo(x + 3, y_base - 1, 1, rgb("#222222"))
    l.circulo(x + 10, y_base - 1, 1, rgb("#222222"))

    # chorizos
    l.rect(x + 2, y_base - 11, x + 4, y_base - 10, rgb("#a04a2a"))
    l.rect(x + 6, y_base - 11, x + 8, y_base - 10, rgb("#a04a2a"))

    # cartel
    l.rect(x + 10, y_base - 17, x + 14, y_base - 12, AMARILLO_BOCA)
    l.px(x + 12, y_base - 15, ROJO)

    l.rect(x + 12, y_base - 12, x + 12, y_base - 10, rgb("#3a3a3a"))

    # humo
    for k in range(4):

        l.px(x + 4 + (k % 2), y_base - 13 - k * 2, rgb("#d0d0d0"))
        l.px(x + 5 - (k % 2), y_base - 14 - k * 2, rgb("#e6e6e6"))


def banderin_boca(l, x, y_base, alto=36):
    """Poste con bandera azul y oro (Boca Juniors)."""

    l.rect(x, y_base - alto, x, y_base, rgb("#6a6a6a"))

    l.rect(x + 1, y_base - alto + 1, x + 9, y_base - alto + 4, AZUL_BOCA)
    l.rect(x + 1, y_base - alto + 5, x + 9, y_base - alto + 8, AMARILLO_BOCA)
    l.rect(x + 1, y_base - alto + 9, x + 9, y_base - alto + 12, AZUL_BOCA)


def farol_colgante(l, x, y_base, alto=30):
    """Farol de hierro con brazo, como los de San Telmo."""

    c = rgb("#23262a")

    l.rect(x, y_base - alto, x, y_base, c)
    l.rect(x - 1, y_base - 1, x + 1, y_base, c)
    l.rect(x, y_base - alto, x + 6, y_base - alto, c)
    l.px(x + 6, y_base - alto + 1, c)
    l.rect(x + 4, y_base - alto + 2, x + 8, y_base - alto + 5, rgb("#f6e08a"))
    l.rect(x + 3, y_base - alto + 1, x + 9, y_base - alto + 1, c)
    l.rect(x + 3, y_base - alto + 6, x + 9, y_base - alto + 6, c)


def pareja_tango(l, x, y_base):
    """Dos bailarines de tango chiquitos."""

    negro = rgb("#17131c")
    piel = rgb("#e0b08a")

    # el bailarin
    l.rect(x, y_base - 8, x + 2, y_base - 3, negro)
    l.rect(x, y_base - 3, x, y_base, negro)
    l.rect(x + 2, y_base - 3, x + 3, y_base, negro)
    l.rect(x, y_base - 11, x + 2, y_base - 9, piel)
    l.rect(x, y_base - 12, x + 2, y_base - 12, negro)
    l.rect(x - 1, y_base - 13, x + 3, y_base - 12, negro)

    # la bailarina, de rojo
    l.rect(x + 4, y_base - 8, x + 6, y_base - 4, ROJO)
    l.poly([(x + 3, y_base - 4), (x + 7, y_base - 4), (x + 9, y_base), (x + 3, y_base)], ROJO)
    l.rect(x + 4, y_base - 11, x + 6, y_base - 9, piel)
    l.rect(x + 4, y_base - 12, x + 6, y_base - 11, rgb("#3a2a1f"))


def paloma(l, x, y_base):

    gris = rgb("#8a8f9a")

    l.rect(x, y_base - 2, x + 3, y_base - 1, gris)
    l.rect(x + 3, y_base - 3, x + 4, y_base - 2, rgb("#5a6070"))
    l.px(x + 4, y_base - 2, rgb("#e0944f"))
    l.px(x + 1, y_base, rgb("#c0555a"))
    l.px(x + 2, y_base, rgb("#c0555a"))


def bolardo(l, x, y_base):

    l.rect(x, y_base - 4, x + 2, y_base, rgb("#3a3d45"))
    l.rect(x - 1, y_base - 5, x + 3, y_base - 4, rgb("#555a66"))


def grua_portuaria(l, x, y_base, alto=58, c=None):
    """Grua de puerto naranja (las que quedaron en Puerto Madero)."""

    c = c or rgb("#e0701f")

    osc = sombra(c, 0.7)

    # patas
    l.rect(x, y_base - 22, x + 1, y_base, osc)
    l.rect(x + 12, y_base - 22, x + 13, y_base, osc)

    # puente horizontal
    l.rect(x - 1, y_base - 26, x + 14, y_base - 22, c)
    l.rect(x - 1, y_base - 26, x + 14, y_base - 26, luz(c, 0.3))

    # torre
    l.rect(x + 4, y_base - alto + 12, x + 9, y_base - 26, c)
    l.rect(x + 4, y_base - alto + 12, x + 4, y_base - 26, luz(c, 0.25))

    for yy in range(y_base - alto + 14, y_base - 26, 5):
        l.linea(x + 4, yy, x + 9, yy + 4, osc)

    # pluma
    l.rect(x - 14, y_base - alto + 6, x + 34, y_base - alto + 9, c)
    l.rect(x - 14, y_base - alto + 6, x + 34, y_base - alto + 6, luz(c, 0.3))

    l.linea(x + 6, y_base - alto + 6, x + 6, y_base - alto, osc)
    l.linea(x + 6, y_base - alto, x - 12, y_base - alto + 6, osc)
    l.linea(x + 6, y_base - alto, x + 32, y_base - alto + 6, osc)

    # cabina
    l.rect(x + 3, y_base - alto + 10, x + 10, y_base - alto + 15, VIDRIO)

    # gancho
    l.rect(x + 28, y_base - alto + 9, x + 28, y_base - alto + 24, rgb("#303030"))
    l.rect(x + 27, y_base - alto + 24, x + 29, y_base - alto + 25, rgb("#303030"))


def cartel_cartelera(l, x, y_base, texto, fondo, color_texto=None, esc=1):
    """Cartel grande con dos postes."""

    color_texto = color_texto or BLANCO

    tw = ancho_texto(texto, esc)

    ancho = tw + 6

    alto = 7 * esc + 6

    l.rect(x + 2, y_base - alto - 12, x + 3, y_base, rgb("#555a60"))
    l.rect(x + ancho - 3, y_base - alto - 12, x + ancho - 2, y_base, rgb("#555a60"))

    l.rect(x, y_base - alto - 12, x + ancho, y_base - 12, luz(fondo, 0.5))
    l.rect(x + 1, y_base - alto - 11, x + ancho - 1, y_base - 13, fondo)

    l.texto(x + 3, y_base - alto - 8, texto, color_texto, esc)

    return ancho


def flecha_derecha(l, x, y, c):

    l.rect(x, y + 2, x + 6, y + 3, c)
    l.poly([(x + 5, y), (x + 9, y + 2.5), (x + 5, y + 5)], c)


# ==========================================================
# VEHICULOS (se dibujan sobre la calle)
# ==========================================================

def _ruedas(l, xs, y_base):

    for x in xs:

        l.rect(x, y_base - 2, x + 2, y_base, rgb("#17151c"))
        l.px(x + 1, y_base - 1, rgb("#8a8f98"))


def auto(l, x, y_base, color=None, flip=False):
    """Auto de perfil: 18 x 8."""

    color = color or ROJO

    p = pal(color)

    # carroceria
    l.rect(x, y_base - 4, x + 17, y_base - 2, p["b"])
    l.rect(x, y_base - 4, x + 17, y_base - 4, p["l"])
    l.rect(x, y_base - 2, x + 17, y_base - 2, p["s"])

    # cabina
    l.poly([(x + 4, y_base - 4), (x + 6, y_base - 7), (x + 12, y_base - 7), (x + 14, y_base - 4)], p["b"])
    l.rect(x + 6, y_base - 6, x + 8, y_base - 5, VIDRIO_LUZ)
    l.rect(x + 10, y_base - 6, x + 12, y_base - 5, VIDRIO_LUZ)

    # luces
    luz_del = x + (16 if not flip else 0)
    luz_tras = x + (0 if not flip else 16)

    l.px(luz_del, y_base - 4, rgb("#ffe9a0"))
    l.px(luz_tras, y_base - 4, rgb("#c03030"))

    _ruedas(l, (x + 3, x + 12), y_base)


def taxi(l, x, y_base, flip=False):
    """Taxi porteno: negro con el techo amarillo."""

    auto(l, x, y_base, rgb("#1d1d24"), flip)

    l.rect(x + 4, y_base - 8, x + 14, y_base - 7, AMARILLO_BOCA)

    l.rect(x + 8, y_base - 9, x + 10, y_base - 9, rgb("#f4f1e8"))

    l.rect(x + 1, y_base - 3, x + 16, y_base - 3, AMARILLO_BOCA)


def colectivo(l, x, y_base, color=None, flip=False):
    """Colectivo de perfil: 38 x 12."""

    color = color or rgb("#2a6fc0")

    p = pal(color)

    l.rect(x, y_base - 11, x + 37, y_base - 3, p["b"])
    l.rect(x, y_base - 11, x + 37, y_base - 11, p["l"])

    # franja blanca
    l.rect(x, y_base - 6, x + 37, y_base - 5, BLANCO)

    # ventanillas
    for k in range(2, 32, 6):

        l.rect(x + k, y_base - 10, x + k + 3, y_base - 7, VIDRIO_LUZ)

    # parabrisas
    px = x + (33 if not flip else 0)

    l.rect(px, y_base - 10, px + 3, y_base - 6, VIDRIO)

    # cartel del ramal
    l.rect(px + (0 if not flip else 0), y_base - 12, px + 3, y_base - 12, rgb("#ffd84a"))

    l.rect(x, y_base - 3, x + 37, y_base - 3, p["s"])

    _ruedas(l, (x + 6, x + 28), y_base)

"""
NIVEL 1 - LA BOCA

    * Caminito (calle museo de conventillos de chapa de colores)
    * Puente Transbordador Nicolas Avellaneda (1914, sobre el Riachuelo)
    * Usina del Arte (ex usina electrica de ladrillo, estilo florentino)
    * La Bombonera (el estadio queda en La Boca; el dibujo es el mismo del
      nivel 15, La Bombonera)
"""

from pixelart import *  # noqa: F401,F403
from monumentos.nivel15 import bombonera  # noqa: F401


# ==========================================================
# CAMINITO
# ==========================================================

def _casa_chapa(l, x0, x1, base_y, alto, color, borde, estilo, seed):
    """Conventillo de dos pisos con balcon de madera y techo de chapa."""

    r = random.Random(seed)

    p = pal(color)

    y_top = base_y - alto

    # pared
    volumen(l, x0, y_top, x1, base_y, color, 1, 2, techo=False)

    # lineas de chapa acanalada (como las del frente de los conventillos)
    for x in range(x0 + 2, x1 - 1, 3):

        l.rect(x, y_top + 4, x, base_y - 14, p["s"])

    # techo
    if estilo == "dos_aguas":

        mx = (x0 + x1) // 2

        l.poly([(x0 - 1, y_top + 1), (mx, y_top - 9), (x1 + 1, y_top + 1)], rgb("#9aa3ad"))

        for k in range(x0 + 1, x1, 3):

            ya = y_top - 9 + abs(k - mx) * 10 // max(1, (x1 - x0) // 2)

            l.rect(k, ya + 1, k, y_top, rgb("#7e8893"))

        l.linea(x0 - 1, y_top + 1, mx, y_top - 9, rgb("#cfd6dc"))

    elif estilo == "una_agua":

        l.poly([(x0 - 1, y_top + 1), (x0 - 1, y_top - 5), (x1 + 1, y_top - 1), (x1 + 1, y_top + 1)],
               rgb("#9aa3ad"))

        for k in range(x0 + 1, x1, 3):
            l.rect(k, y_top - 4 + (k - x0) // 8, k, y_top, rgb("#7e8893"))

    else:

        # parapeto recto con cornisa de otro color
        l.rect(x0 - 1, y_top - 2, x1 + 1, y_top + 1, borde)
        l.rect(x0 - 1, y_top - 2, x1 + 1, y_top - 2, luz(borde))

    # franja entre pisos
    l.rect(x0, base_y - 21, x1, base_y - 20, borde)

    # planta baja: puerta + ventana con postigos
    pw = 6

    l.rect(x0 + 3, base_y - 13, x0 + 3 + pw - 1, base_y, rgb("#5a3a22"))
    l.rect(x0 + 3, base_y - 13, x0 + 3 + pw - 1, base_y - 13, borde)
    l.px(x0 + 3 + pw - 2, base_y - 6, ORO)

    wx = x1 - 12

    l.rect(wx - 1, base_y - 14, wx + 7, base_y - 4, borde)
    l.rect(wx, base_y - 13, wx + 6, base_y - 5, VIDRIO)
    l.rect(wx + 3, base_y - 13, wx + 3, base_y - 5, borde)
    l.px(wx, base_y - 13, VIDRIO_LUZ)

    # primer piso: balcon corrido de madera
    madera = rgb("#7a4a2a")

    l.rect(x0 - 2, base_y - 21, x1 + 2, base_y - 20, madera)
    l.rect(x0 - 2, base_y - 21, x1 + 2, base_y - 21, luz(madera, 0.2))

    for x in range(x0 - 1, x1 + 2, 2):
        l.rect(x, base_y - 28, x, base_y - 22, madera)

    l.rect(x0 - 2, base_y - 29, x1 + 2, base_y - 28, madera)
    l.rect(x0 - 2, base_y - 29, x1 + 2, base_y - 29, luz(madera, 0.25))

    # puertas-ventana del piso de arriba
    n = 2 if (x1 - x0) >= 26 else 1

    paso = (x1 - x0 - 4) // n

    for i in range(n):

        vx = x0 + 3 + i * paso + (paso - 8) // 2

        l.rect(vx - 1, base_y - 38, vx + 8, base_y - 22, borde)
        l.rect(vx, base_y - 37, vx + 7, base_y - 22, VIDRIO)
        l.rect(vx + 3, base_y - 37, vx + 4, base_y - 22, borde)
        l.px(vx, base_y - 37, VIDRIO_LUZ)

        # postigos
        l.rect(vx - 3, base_y - 37, vx - 2, base_y - 23, sombra(borde, 0.8))
        l.rect(vx + 9, base_y - 37, vx + 10, base_y - 23, sombra(borde, 0.8))

    # ropa colgada en algun balcon
    if r.random() < 0.6:

        for k in range(3):

            l.rect(x0 + 3 + k * 4, base_y - 27, x0 + 4 + k * 4, base_y - 24,
                   r.choice([BLANCO, ROJO, AMARILLO_BOCA, rgb("#e88fb0")]))


def caminito():

    ancho = 214
    alto = 96

    l = Lienzo(ancho, alto)

    base = alto - 1

    casas = [
        (62, 90, 56, rgb("#f2c230"), rgb("#2e66c4"), "dos_aguas"),
        (91, 119, 63, rgb("#cf3b32"), rgb("#f4f1e8"), "recto"),
        (120, 152, 58, rgb("#2e66c4"), rgb("#f2c230"), "una_agua"),
        (153, 180, 64, rgb("#2f9a5a"), rgb("#e8892a"), "dos_aguas"),
        (181, 209, 55, rgb("#e8892a"), rgb("#2e66c4"), "recto"),
    ]

    for i, (x0, x1, h, c, b, est) in enumerate(casas):

        _casa_chapa(l, x0, x1, base, h, c, b, est, i)

    # guirnaldas de banderitas cruzando la calle
    cols = [ROJO, AMARILLO_BOCA, CELESTE_ARG, rgb("#3a9a58"), rgb("#f4f1e8"), rgb("#e88fb0")]

    y0 = base - 52

    for k in range(70, 205):

        y = y0 + int(4 * math.sin((k - 70) / 135 * math.pi * 3) ** 2)

        l.px(k, y, rgb("#3a3a3a"))

        if k % 4 == 0:

            c = cols[(k // 4) % len(cols)]

            l.rect(k, y + 1, k + 1, y + 3, c)
            l.px(k, y + 4, c)

    # cartel de entrada "CAMINITO"
    tx = 3

    texto = "CAMINITO"

    w = ancho_texto(texto)

    l.rect(tx, base - 24, tx, base, rgb("#6a4a2a"))
    l.rect(tx + w + 5, base - 24, tx + w + 5, base, rgb("#6a4a2a"))

    l.rect(tx - 2, base - 38, tx + w + 7, base - 23, rgb("#3a6fb0"))
    l.marco(tx - 2, base - 38, tx + w + 7, base - 23, rgb("#f4f1e8"))

    l.texto(tx + 3, base - 34, texto, AMARILLO_BOCA)

    # sombrilla roja de un cafe
    l.rect(30, base - 12, 30, base, rgb("#7a7a7a"))
    l.poly([(21, base - 12), (30, base - 19), (39, base - 12)], ROJO)
    l.poly([(30, base - 19), (39, base - 12), (34, base - 12)], sombra(ROJO, 0.75))

    # un par bailando tango
    persona(l, 44, base, rgb("#1d1a24"), pantalon=rgb("#1d1a24"))
    persona(l, 47, base, ROJO, pantalon=rgb("#f4f1e8"), pelo=rgb("#8a4a2a"))

    return l


# ==========================================================
# PUENTE TRANSBORDADOR
# ==========================================================

def _torre_reticulada(l, x, y0, y1, ancho_base, ancho_tope, acero, brillo, ox):
    """Torre de acero con patas y cruces en X."""

    alto = y1 - y0

    for dy in range(alto):

        t = dy / alto

        ancho = ancho_tope + (ancho_base - ancho_tope) * t

        xa = int(round(x - ancho / 2))
        xb = int(round(x + ancho / 2))

        y = y0 + dy

        for pata in (xa, xb):

            l.rect(pata, y, pata + 1, y, acero)
            l.px(pata, y, brillo)

    # cruces
    paso = 14

    for k in range(0, alto - paso, paso):

        ya = y0 + k
        yb = y0 + k + paso

        ta = k / alto
        tb = (k + paso) / alto

        wa = ancho_tope + (ancho_base - ancho_tope) * ta
        wb = ancho_tope + (ancho_base - ancho_tope) * tb

        la, ra = x - wa / 2, x + wa / 2
        lb, rb = x - wb / 2, x + wb / 2

        l.linea(la + 1, ya, rb, yb, acero)
        l.linea(ra, ya, lb + 1, yb, acero)

        # travesano horizontal
        l.rect(int(lb) + 1, yb, int(rb), yb, brillo if k % 2 == 0 else acero)


def transbordador():

    ancho = 186
    alto = 172

    l = Lienzo(ancho, alto)

    base = alto - 1

    acero = rgb("#4a5463")
    brillo = rgb("#8b98ab")
    oxido = rgb("#8a4f33")

    # agua del Riachuelo entre las dos torres (se ve detras del muelle)
    agua = rgb("#6d7f58")

    l.rect(22, base - 26, ancho - 24, base - 4, agua)

    for k in range(24, ancho - 24, 7):

        l.rect(k, base - 22 + (k // 7) % 3 * 4, k + 3, base - 22 + (k // 7) % 3 * 4, luz(agua, 0.3))
        l.rect(k + 3, base - 12 + (k // 7) % 2 * 5, k + 5, base - 12 + (k // 7) % 2 * 5, sombra(agua, 0.8))

    # costanera de piedra al frente
    l.rect(0, base - 6, ancho - 1, base, rgb("#8d8a84"))
    l.rect(0, base - 6, ancho - 1, base - 6, rgb("#b4b0a8"))

    for x in range(3, ancho, 9):
        l.rect(x, base - 5, x, base, rgb("#6c6a66"))

    # torres
    _torre_reticulada(l, 22, 14, base - 6, 22, 15, acero, brillo, 0)
    _torre_reticulada(l, ancho - 25, 14, base - 6, 22, 15, acero, brillo, 0)

    # viga superior: dos reticulados en N
    y0, y1 = 6, 21

    l.rect(8, y0, ancho - 11, y0 + 1, acero)
    l.rect(8, y1 - 1, ancho - 11, y1, acero)
    l.rect(8, y0, ancho - 11, y0, brillo)

    x = 8

    arriba = True

    while x < ancho - 22:

        l.linea(x, y1 - 1, x + 12, y0 + 1, acero)
        l.rect(x, y0, x, y1, acero)

        x += 12

    l.rect(ancho - 12, y0, ancho - 12, y1, acero)

    # manchas de oxido
    for k in range(10, ancho - 12, 17):
        l.rect(k, y0 + 2, k + 2, y0 + 3, oxido)

    # cables y barquilla (la gondola colgante)
    cx = 98

    cab_y = base - 54

    for dx in (-17, 17):

        l.linea(cx + dx, y1, cx + dx, cab_y, rgb("#2a2f38"))
        l.linea(cx + dx - 1, y1, cx + dx - 1, cab_y, rgb("#5a6372"))

    l.linea(cx - 17, y1, cx, y1 + 10, rgb("#2a2f38"))
    l.linea(cx + 17, y1, cx, y1 + 10, rgb("#2a2f38"))

    # plataforma
    l.rect(cx - 22, cab_y, cx + 22, cab_y + 3, rgb("#2a2f38"))
    l.rect(cx - 22, cab_y, cx + 22, cab_y, rgb("#6a7484"))

    # baranda y cabina
    for k in range(-20, 21, 4):
        l.rect(cx + k, cab_y - 5, cx + k, cab_y - 1, rgb("#2a2f38"))

    l.rect(cx - 20, cab_y - 6, cx + 20, cab_y - 6, rgb("#2a2f38"))

    l.rect(cx - 6, cab_y - 14, cx + 6, cab_y - 1, rgb("#c2452f"))
    l.rect(cx - 6, cab_y - 14, cx + 6, cab_y - 14, luz(rgb("#c2452f")))
    l.rect(cx - 4, cab_y - 12, cx - 1, cab_y - 8, VIDRIO)
    l.rect(cx + 1, cab_y - 12, cx + 4, cab_y - 8, VIDRIO)

    # autos arriba de la gondola
    l.rect(cx - 17, cab_y - 4, cx - 10, cab_y - 1, rgb("#e7c22b"))
    l.rect(cx + 10, cab_y - 4, cx + 17, cab_y - 1, rgb("#2f64b8"))

    # escalera de acceso a cada torre
    for x in (22, ancho - 25):

        l.rect(x - 2, base - 12, x + 2, base - 7, rgb("#2a2f38"))

    return l


# ==========================================================
# USINA DEL ARTE
# ==========================================================

def usina_del_arte():

    ancho = 196
    alto = 132

    l = Lienzo(ancho, alto)

    base = alto - 1

    ladrillo = rgb("#a3452e")
    piedra = rgb("#d9d0ba")

    # zocalo de granito
    # --- alas de ladrillo ---
    for (x0, x1) in ((40, 90), (122, 188)):

        ladrillos(l, x0, base - 52, x1, base, ladrillo)

        l.rect(x0, base - 52, x1, base - 52, luz(ladrillo, 0.2))

        # zocalo
        l.rect(x0, base - 7, x1, base, rgb("#7b7770"))
        l.rect(x0, base - 7, x1, base - 7, rgb("#a3a099"))

        # cornisa de piedra
        l.rect(x0 - 1, base - 55, x1 + 1, base - 53, piedra)
        l.rect(x0 - 1, base - 55, x1 + 1, base - 55, luz(piedra, 0.3))

        # ventanas con arco
        paso = 11

        for x in range(x0 + 5, x1 - 8, paso):

            ventana_arco(l, x, base - 10, x + 5, 20, VIDRIO, piedra)
            ventana_arco(l, x, base - 36, x + 5, 14, VIDRIO, piedra)

    # --- nave central de piedra ---
    nx0, nx1 = 90, 122

    volumen(l, nx0, base - 78, nx1, base, piedra, 1, 2)

    # zocalo de granito
    l.rect(nx0, base - 9, nx1, base, rgb("#8a8780"))
    l.rect(nx0, base - 9, nx1, base - 9, rgb("#aeaba3"))

    # hileras de piedra
    for y in range(base - 76, base - 10, 5):
        l.rect(nx0 + 1, y, nx1 - 2, y, sombra(piedra, 0.9))

    # pilastras
    l.rect(nx0 + 1, base - 74, nx0 + 3, base - 10, luz(piedra, 0.2))
    l.rect(nx1 - 4, base - 74, nx1 - 2, base - 10, sombra(piedra, 0.92))

    # gran ventanal con arco
    ventana_arco(l, 98, base - 12, 113, 44, VIDRIO, ladrillo)

    for y in range(base - 52, base - 12, 6):
        l.rect(99, y, 112, y, VIDRIO_OSC)

    l.rect(105, base - 52, 106, base - 12, VIDRIO_OSC)

    # puerta de entrada
    l.arco(102, base, 109, 14, rgb("#4a2f1f"))

    # cornisa y frontis
    l.rect(nx0 - 2, base - 82, nx1 + 2, base - 79, sombra(piedra, 0.85))
    l.rect(nx0 - 2, base - 82, nx1 + 2, base - 82, luz(piedra, 0.35))

    l.poly([(nx0, base - 83), (106, base - 96), (nx1, base - 83)], piedra)
    l.poly([(nx0 + 5, base - 84), (106, base - 93), (nx1 - 5, base - 84)], sombra(piedra, 0.86))

    l.circulo(106, base - 87, 2, ORO)

    # --- torre de ladrillo (a la izquierda) ---
    tx0, tx1 = 10, 36

    ladrillos(l, tx0, base - 108, tx1, base, ladrillo)

    l.rect(tx0, base - 108, tx0, base, luz(ladrillo, 0.2))
    l.rect(tx1 - 2, base - 108, tx1, base, sombra(ladrillo, 0.78))

    # bandas de piedra
    for y in (base - 30, base - 64, base - 92):

        l.rect(tx0 - 1, y, tx1 + 1, y + 1, piedra)

    # ventanitas con arco
    for y in (base - 20, base - 50, base - 80):

        ventana_arco(l, 20, y, 25, 12, VIDRIO, piedra)

    # remate: corona y techo piramidal
    l.rect(tx0 - 2, base - 112, tx1 + 2, base - 109, piedra)
    l.rect(tx0 - 2, base - 112, tx1 + 2, base - 112, luz(piedra, 0.3))

    aguja(l, (tx0 + tx1) // 2, base - 112, tx1 - tx0 + 6, 16, rgb("#5d6670"))

    l.rect((tx0 + tx1) // 2, base - 134, (tx0 + tx1) // 2, base - 126, rgb("#4a4a4a"))

    # tramo de union entre torre y ala
    ladrillos(l, 36, base - 40, 40, base, ladrillo)

    # cartel
    texto1, texto2 = "USINA", "DEL ARTE"

    cx = 155

    l.rect(cx - 25, base - 49, cx + 25, base - 26, rgb("#1f2b4a"))
    l.marco(cx - 25, base - 49, cx + 25, base - 26, piedra)

    l.texto(cx - ancho_texto(texto1) // 2, base - 46, texto1, BLANCO)
    l.texto(cx - ancho_texto(texto2) // 2, base - 36, texto2, AMARILLO_BOCA)

    return l


MONUMENTOS = [
    dict(id="caminito", nombre="Caminito", fn=caminito),
    dict(id="transbordador", nombre="Puente Transbordador Nicolas Avellaneda", fn=transbordador),
    dict(id="usina_del_arte", nombre="Usina del Arte", fn=usina_del_arte),
    dict(id="bombonera", nombre="La Bombonera", fn=bombonera),
]

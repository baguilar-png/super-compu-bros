"""
Genera las imagenes pixel art de los 30 niveles de Super Compu Bros.

Para cada nivel produce:

    assets/niveles/nivel_NN_cielo.png    cielo + skyline lejano (1300 x 200)
    assets/niveles/nivel_NN_ciudad.png   calle, edificios y monumentos
                                         (3200 x 200, con transparencia)
    assets/monumentos/<id>.png           cada monumento suelto

El juego dibuja el cielo con parallax (se mueve mas lento que la camara)
y la ciudad pegada al nivel, un pixel de dibujo = 3 pixeles de pantalla.

Uso (desde la carpeta del juego):

    python herramientas/generar_niveles.py            # los 30 niveles
    python herramientas/generar_niveles.py 1 4 12     # solo esos
    python herramientas/generar_niveles.py --vista    # ademas, vistas previas

Necesita Pillow y numpy.
"""

import math
import os
import random
import sys

HERRAMIENTAS = os.path.dirname(os.path.abspath(__file__))

if HERRAMIENTAS not in sys.path:
    sys.path.insert(0, HERRAMIENTAS)

from pixelart import *  # noqa: E402,F401,F403
import edificios as E  # noqa: E402
import monumentos  # noqa: E402
from niveles_config import NIVELES, PALETAS  # noqa: E402

CARPETA_JUEGO = os.path.dirname(HERRAMIENTAS)

CARPETA_NIVELES = os.path.join(CARPETA_JUEGO, "assets", "niveles")
CARPETA_MONUMENTOS = os.path.join(CARPETA_JUEGO, "assets", "monumentos")

# ----------------------------------------------------------
# Medidas (en pixeles de dibujo)
# ----------------------------------------------------------

ANCHO = 3200            # el nivel mide 9600 pixeles de pantalla
ALTO = 200
BASE = 175              # la fila donde apoyan los edificios (arriba de la vereda)
ANCHO_CIELO = 1300      # 0.35 de parallax sobre 8800 px de recorrido + pantalla

PIE = 180               # fila donde el personaje apoya los pies

CALLE_Y = 187           # primera fila de asfalto
CALLE_FIN = ALTO - 1

# Tipos de edificio: (funcion, (ancho min, max), (alto min, max))
ESTILOS = {
    "frances": (E.frances, (30, 56), (76, 128)),
    "italianizante": (E.italianizante, (36, 62), (58, 96)),
    "casa_baja": (E.casa_baja, (26, 44), (30, 48)),
    "conventillo": (E.conventillo, (24, 36), (38, 56)),
    "torre_vidrio": (E.torre_vidrio, (24, 40), (96, 168)),
    "torre_hormigon": (E.torre_hormigon, (24, 38), (74, 130)),
    "art_deco": (E.art_deco, (30, 44), (88, 134)),
    "galpon": (E.galpon, (56, 90), (44, 62)),
    "fabrica": (E.fabrica, (44, 70), (60, 84)),
    "departamentos": (E.departamentos, (26, 40), (72, 120)),
    "mural": (E.mural, (32, 44), (80, 120)),
    "local": (E.local_comercial, (34, 54), (52, 78)),
}


# ==========================================================
# AYUDAS DE COLOR
# ==========================================================

def hx(s):
    return rgb(s)


def elegir_paleta(cfg, estilo, r):
    """Devuelve el dict de colores que esperan las funciones de edificio."""

    tupla = r.choice(PALETAS[estilo])

    c = dict(fachada=hx(tupla[0]))

    if len(tupla) > 1:
        c["borde"] = hx(tupla[1])
    else:
        c["borde"] = luz(hx(tupla[0]), 0.35)

    if len(tupla) > 2:
        c["extra"] = hx(tupla[2])

    if estilo == "mural":
        c["mural"] = r.choice(cfg.get("mural", ["abstracto"]))

    if estilo == "local":
        c["textos"] = cfg.get("textos", ["OFERTA"])

    return c


def elegir_pesos(opciones, r):
    """opciones: lista de (valor, peso)."""

    total = sum(p for _, p in opciones)

    u = r.random() * total

    for v, p in opciones:

        u -= p

        if u <= 0:
            return v

    return opciones[-1][0]


# ==========================================================
# SKYLINE LEJANO (capa del cielo, con parallax)
# ==========================================================

def sil_casas(l, y, r, c, alto=(34, 74)):

    x = -6

    while x < l.w:

        w = r.randint(9, 22)
        h = r.randint(*alto)

        l.rect(x, y - h, x + w - 1, y, c)

        k = r.random()

        if k < 0.25:
            l.poly([(x - 1, y - h), (x + w // 2, y - h - 6), (x + w, y - h)], c)
        elif k < 0.45:
            l.rect(x + 2, y - h - 4, x + 5, y - h, c)
        elif k < 0.55:
            l.rect(x + w // 2, y - h - 9, x + w // 2, y - h, c)

        x += w + r.randint(0, 2)


def sil_centro(l, y, r, c):
    """Edificios con cupulas, agujas y torres con reloj."""

    x = -8

    while x < l.w:

        w = r.randint(12, 26)
        h = r.randint(46, 96)

        l.rect(x, y - h, x + w - 1, y, c)

        k = r.random()

        if k < 0.25:

            l.semi(x + w // 2, y - h, w // 2 - 1, w // 2, c)
            l.rect(x + w // 2, y - h - w // 2 - 6, x + w // 2, y - h - w // 2, c)

        elif k < 0.45:

            l.poly([(x + 1, y - h), (x + w // 2, y - h - 14), (x + w - 2, y - h)], c)

        elif k < 0.6:

            l.rect(x + w // 2 - 2, y - h - 14, x + w // 2 + 2, y - h, c)
            l.poly([(x + w // 2 - 3, y - h - 14), (x + w // 2, y - h - 22), (x + w // 2 + 3, y - h - 14)], c)

        x += w + r.randint(0, 3)


def sil_rascacielos(l, y, r, c):

    x = -8

    while x < l.w:

        w = r.randint(12, 24)
        h = r.randint(70, 150)

        l.rect(x, y - h, x + w - 1, y, c)

        k = r.random()

        if k < 0.4:
            l.rect(x + 3, y - h - 8, x + w - 4, y - h, c)

        if k < 0.25:
            l.rect(x + w // 2, y - h - 20, x + w // 2, y - h - 8, c)

        x += w + r.randint(1, 5)


def sil_puerto(l, y, r, c):
    """Grua, barcos y galpones."""

    x = -10

    while x < l.w:

        k = r.random()

        if k < 0.3:

            # barco: casco, castillo y mastiles
            w = r.randint(46, 80)

            l.poly([(x, y - 12), (x + w, y - 12), (x + w - 8, y), (x + 6, y)], c)
            l.rect(x + w // 3, y - 22, x + w // 3 + 12, y - 12, c)
            l.rect(x + w // 3 + 3, y - 28, x + w // 3 + 6, y - 22, c)

            for m in (x + w // 6, x + w - w // 5):
                l.rect(m, y - 40, m, y - 12, c)
                l.rect(m - 4, y - 34, m + 4, y - 34, c)

        elif k < 0.55:

            # grua de puerto
            l.rect(x, y - 40, x + 1, y, c)
            l.rect(x + 10, y - 40, x + 11, y, c)
            l.rect(x - 14, y - 46, x + 30, y - 43, c)
            l.rect(x + 4, y - 56, x + 7, y - 46, c)

            w = 18

        elif k < 0.8:

            w = r.randint(30, 54)
            h = r.randint(18, 30)

            l.rect(x, y - h, x + w, y, c)
            l.poly([(x - 1, y - h), (x + w // 2, y - h - 8), (x + w + 1, y - h)], c)

        else:

            # velero
            w = 24

            l.poly([(x, y - 6), (x + w, y - 6), (x + w - 5, y), (x + 4, y)], c)
            l.poly([(x + 10, y - 8), (x + 10, y - 34), (x + 21, y - 8)], c)
            l.poly([(x + 8, y - 8), (x + 8, y - 26), (x + 1, y - 8)], c)

            w = 26

        x += (w if k >= 0.3 else w) + r.randint(6, 26)


def sil_parque(l, y, r, c):
    """Copas de arboles y algun techo."""

    x = -10

    while x < l.w:

        h = r.randint(28, 56)
        rx = r.randint(8, 16)

        l.rect(x + rx - 1, y - h // 2, x + rx, y, c)

        l.elipse(x, y - h, x + rx * 2, y - h // 3, c)
        l.elipse(x + rx // 2, y - h - 4, x + rx * 2 - rx // 2, y - h // 2, c)

        if r.random() < 0.15:

            w = r.randint(10, 18)
            hh = r.randint(14, 26)

            l.rect(x + rx * 2, y - hh, x + rx * 2 + w, y, c)

            x += w

        x += rx * 2 + r.randint(-4, 6)


def sil_frances(l, y, r, c):
    """Techos de mansarda con chimeneas."""

    x = -8

    while x < l.w:

        w = r.randint(16, 30)
        h = r.randint(46, 84)

        l.rect(x, y - h, x + w - 1, y, c)
        l.poly([(x - 1, y - h), (x + 3, y - h - 10), (x + w - 4, y - h - 10), (x + w, y - h)], c)

        if r.random() < 0.6:
            l.rect(x + r.randint(3, max(4, w - 6)), y - h - 15, x + w // 2, y - h - 9, c)

        x += w + r.randint(0, 2)


def sil_estadio(l, y, r, c):
    """Cancha con las torres de luces y casitas bajas."""

    x = 60

    while x < l.w - 200:

        w = 190

        # tribunas
        l.poly([(x, y), (x + 14, y - 46), (x + w - 14, y - 46), (x + w, y)], c)
        l.rect(x + 14, y - 52, x + w - 14, y - 46, c)

        # torres de luz
        for tx in (x + 10, x + w - 14):

            l.rect(tx, y - 90, tx + 2, y - 46, c)
            l.rect(tx - 5, y - 100, tx + 7, y - 91, c)

        x += w + r.randint(380, 560)


def sil_industrial(l, y, r, c):
    """Chimeneas, tanques y galpones con dientes de sierra."""

    x = -10

    while x < l.w:

        k = r.random()

        if k < 0.3:

            h = r.randint(50, 90)

            l.rect(x, y - h, x + 3, y, c)
            l.rect(x - 1, y - h, x + 4, y - h + 2, c)

            w = 6

        elif k < 0.55:

            w = r.randint(12, 20)
            h = r.randint(24, 40)

            l.rect(x, y - h, x + w, y, c)
            l.semi(x + w // 2, y - h, w // 2, 5, c)

        else:

            w = r.randint(30, 60)
            h = r.randint(16, 28)

            l.rect(x, y - h, x + w, y, c)

            for sx in range(x, x + w - 5, 10):
                l.poly([(sx, y - h), (sx, y - h - 6), (sx + 9, y - h)], c)

        x += w + r.randint(0, 10)


SKYLINES = {
    "casas": sil_casas,
    "centro": sil_centro,
    "rascacielos": sil_rascacielos,
    "puerto": sil_puerto,
    "parque": sil_parque,
    "frances": sil_frances,
    "estadio": sil_estadio,
    "industrial": sil_industrial,
}


def puntos_de_luz(l, color_silueta, prob, color_luz, r):
    """Ventanitas prendidas sobre una silueta."""

    a = np.array(l.im)

    m = np.all(a[..., :3] == np.array(color_silueta[:3]), axis=-1)

    ys, xs = np.nonzero(m)

    for y, x in zip(ys, xs):

        if r.random() < prob and x % 2 == 0 and y % 3 == 0:
            l.px(int(x), int(y), color_luz)


def hacer_cielo(n, cfg):
    """La capa lejana: degradado, astros, nubes y siluetas."""

    r = random.Random(7000 + n)

    arriba, medio, abajo = (hx(c) for c in cfg["cielo"])

    l = cielo(ANCHO_CIELO, ALTO, arriba, medio, abajo)

    noche = cfg.get("noche", 0)

    # estrellas
    if cfg.get("estrellas") or noche > 0.45:

        for _ in range(110 if cfg.get("estrellas") else 60):

            x = r.randint(0, ANCHO_CIELO - 1)
            y = r.randint(0, 110)

            if r.random() < 0.6:
                l.px(x, y, rgb("#e8ecff"))
            else:
                l.px(x, y, rgb("#8c96d8"))

            if r.random() < 0.06:

                l.px(x + 1, y, rgb("#cfd6ff"))
                l.px(x - 1, y, rgb("#cfd6ff"))
                l.px(x, y + 1, rgb("#cfd6ff"))
                l.px(x, y - 1, rgb("#cfd6ff"))

    # sol
    if "sol" in cfg:

        sx, sy, sr, sc = cfg["sol"]

        col = hx(sc)

        for k, tt in ((sr + 6, 0.12), (sr + 3, 0.22)):
            l.circulo(sx, sy, k, mezcla(medio if sy < 100 else abajo, col, tt))

        l.circulo(sx, sy, sr, col)
        l.circulo(sx - 2, sy - 2, max(2, sr - 4), luz(col, 0.35))

    # luna
    if "luna" in cfg:

        lx, ly, lr = cfg["luna"][:3]

        l.circulo(lx, ly, lr + 4, mezcla(medio, rgb("#ffffff"), 0.12))
        l.circulo(lx, ly, lr, rgb("#f4f1de"))
        l.circulo(lx + lr // 3, ly - lr // 3, lr // 4, rgb("#d6d3bf"))
        l.circulo(lx - lr // 3, ly + lr // 4, lr // 5, rgb("#d6d3bf"))

    # nubes
    col_nube = hx(cfg.get("nubes", "#ffffff"))

    sombra_nube = mezcla(col_nube, medio, 0.5)

    cantidad = 11

    for i in range(cantidad):

        x = int((i + r.random() * 0.8) * ANCHO_CIELO / cantidad)
        y = r.randint(8, 78)
        w = r.randint(28, 70)

        nube(l, x, y, w, col_nube, sombra_nube)

    # siluetas: la primera es la mas lejana y clara
    base_sil = (70, 86, 130) if noche < 0.4 else (30, 36, 80)

    color_dia = abajo

    tonos = [0.30, 0.46]

    for i, nombre in enumerate(cfg["skyline"]):

        tt = tonos[min(i, 1)]

        c = mezcla(color_dia, base_sil, tt)

        # el skyline mas lejano de todos asoma mas arriba
        yb = 172 if i == 0 else 178

        SKYLINES[nombre](l, yb, r, c) if nombre != "estadio" else SKYLINES[nombre](l, yb, r, c)

        l.rect(0, yb, ANCHO_CIELO - 1, ALTO - 1, c)

        if noche > 0.45:
            puntos_de_luz(l, c, 0.10, rgb("#ffd890"), r)

    # los reflectores del estadio encendidos
    if "estadio" in cfg["skyline"] and noche > 0.4:

        a = np.array(l.im)

        # las cabezas de las torres de luz son rectangulos de 13 x 10 en el borde
        pass

    return l


# ==========================================================
# SUELO
# ==========================================================

def ruido(r, base, v):
    """Un color con un poco de variacion."""

    k = r.uniform(-v, v)

    return tuple(max(0, min(255, int(c + k))) for c in base)


def pintar_baldosa(l, r, y0, y1):

    base = (204, 199, 187)

    l.rect(0, y0, l.w - 1, y1, base)

    # junta de baldosas, en dos filas escalonadas
    junta = (176, 170, 158)

    filas = list(range(y0 + 3, y1 + 1, 5))

    for i, y in enumerate(filas):

        l.rect(0, y, l.w - 1, y, junta)

        desfase = 0 if i % 2 == 0 else 6

        for x in range(desfase, l.w, 12):
            l.rect(x, y - 4 if y - 4 >= y0 else y0, x, y - 1, junta)

    # manchitas
    for _ in range(l.w // 3):

        x = r.randint(0, l.w - 1)
        y = r.randint(y0, y1)

        l.px(x, y, ruido(r, (192, 186, 174), 8))


def pintar_adoquin(l, r, y0, y1, base=(132, 122, 112)):

    for fila, y in enumerate(range(y0, y1 + 1, 3)):

        desfase = 0 if fila % 2 == 0 else 3

        for x in range(-desfase, l.w, 6):

            c = ruido(r, base, 14)

            yy1 = min(y + 2, y1)

            l.rect(max(0, x), y, min(l.w - 1, x + 4), yy1, c)

            l.rect(max(0, x), y, min(l.w - 1, x + 4), y, luz(c, 0.18))

            # junta oscura
            l.rect(max(0, x + 5), y, max(0, x + 5), yy1, sombra(base, 0.55))

        l.rect(0, min(y + 2, y1), l.w - 1, min(y + 2, y1), sombra(base, 0.6))


def pintar_ladrillo_piso(l, r, y0, y1):

    base = (166, 86, 62)

    for fila, y in enumerate(range(y0, y1 + 1, 2)):

        desfase = 0 if fila % 2 == 0 else 2

        l.rect(0, y, l.w - 1, y, ruido(r, base, 6))

        for x in range(-desfase, l.w, 5):

            if 0 <= x < l.w:
                l.rect(x, y, x, min(y + 1, y1), (126, 62, 46))

        l.rect(0, min(y + 1, y1), l.w - 1, min(y + 1, y1), (132, 66, 48))


def pintar_plaza(l, r, y0, y1):

    base = (190, 183, 170)

    l.rect(0, y0, l.w - 1, y1, base)

    for x in range(0, l.w, 16):
        l.rect(x, y0, x, y1, (168, 161, 148))

    for y in range(y0 + 4, y1 + 1, 8):
        l.rect(0, y, l.w - 1, y, (168, 161, 148))

    for _ in range(l.w // 2):

        x = r.randint(0, l.w - 1)
        y = r.randint(y0, y1)

        l.px(x, y, ruido(r, (180, 173, 160), 10))


def pintar_asfalto(l, r, y0, y1):

    base = (82, 86, 94)

    l.rect(0, y0, l.w - 1, y1, base)

    for _ in range(l.w * (y1 - y0 + 1) // 9):

        x = r.randint(0, l.w - 1)
        y = r.randint(y0, y1)

        l.px(x, y, ruido(r, base, 12))

    # linea de carril
    yl = (y0 + y1) // 2 + 1

    for x in range(0, l.w, 24):
        l.rect(x, yl, x + 11, yl, (226, 214, 150))


def pintar_vias(l, r, y0, y1):
    """Calle con rieles (tranvia / tren de carga) sobre balasto."""

    base = (112, 104, 96)

    l.rect(0, y0, l.w - 1, y1, base)

    for _ in range(l.w * (y1 - y0 + 1) // 6):

        x = r.randint(0, l.w - 1)
        y = r.randint(y0, y1)

        l.px(x, y, ruido(r, base, 22))

    ya = y0 + 3
    yb = y0 + 9

    # durmientes
    for x in range(0, l.w, 7):
        l.rect(x, ya - 1, x + 1, yb + 1, (84, 60, 40))

    # rieles
    for y in (ya, yb):

        l.rect(0, y, l.w - 1, y, (178, 182, 188))
        l.rect(0, y + 1, l.w - 1, y + 1, (96, 100, 108))


def pintar_pasto(l, r, y0, y1):

    base = (70, 150, 66)

    l.rect(0, y0, l.w - 1, y1, base)

    for _ in range(l.w * (y1 - y0 + 1) // 5):

        x = r.randint(0, l.w - 1)
        y = r.randint(y0, y1)

        l.px(x, y, r.choice([(58, 132, 56), (88, 168, 80), (74, 156, 70)]))

    # florcitas
    for _ in range(l.w // 14):

        x = r.randint(0, l.w - 1)
        y = r.randint(y0, y1)

        l.px(x, y, r.choice([(250, 240, 120), (250, 250, 250), (240, 150, 200)]))


def pintar_sendero(l, r, y0, y1):

    base = (214, 190, 146)

    l.rect(0, y0, l.w - 1, y1, base)

    for _ in range(l.w * (y1 - y0 + 1) // 6):

        x = r.randint(0, l.w - 1)
        y = r.randint(y0, y1)

        l.px(x, y, ruido(r, base, 14))

    # borde de pasto
    l.rect(0, y1, l.w - 1, y1, (120, 120, 80))


PISOS = {
    "baldosa": pintar_baldosa,
    "adoquin": pintar_adoquin,
    "ladrillo": pintar_ladrillo_piso,
    "plaza": pintar_plaza,
    "asfalto": pintar_asfalto,
    "vias": pintar_vias,
    "pasto": pintar_pasto,
    "sendero": pintar_sendero,
}


def hacer_suelo(cfg, r, esquinas, lagos):
    """Las filas de abajo: vereda, cordon y calle."""

    l = Lienzo(ANCHO, ALTO)

    vereda, calle = cfg["suelo"]

    # vereda: BASE .. CALLE_Y - 3
    PISOS[vereda](l, r, BASE, CALLE_Y - 3)

    if calle == "adoquin":

        # la calle de adoquines: mas oscura que la vereda
        pintar_adoquin(l, r, CALLE_Y, CALLE_FIN, base=(104, 98, 94))

    else:

        PISOS[calle](l, r, CALLE_Y, CALLE_FIN)

    # sombra que proyectan los edificios sobre la vereda
    l.rect(0, BASE, ANCHO - 1, BASE, sombra((204, 199, 187), 0.62))
    l.rect(0, BASE + 1, ANCHO - 1, BASE + 1, sombra((204, 199, 187), 0.8))

    # cordon
    cordon = (232, 228, 216)

    if "boca" in cfg.get("especiales", []):

        for x in range(0, ANCHO, 8):

            l.rect(x, CALLE_Y - 2, x + 3, CALLE_Y - 2, AZUL_BOCA)
            l.rect(x + 4, CALLE_Y - 2, x + 7, CALLE_Y - 2, AMARILLO_BOCA)
            l.rect(x, CALLE_Y - 1, x + 3, CALLE_Y - 1, AZUL_BOCA)
            l.rect(x + 4, CALLE_Y - 1, x + 7, CALLE_Y - 1, AMARILLO_BOCA)

    elif cfg["suelo"][1] != "pasto":

        l.rect(0, CALLE_Y - 2, ANCHO - 1, CALLE_Y - 2, cordon)
        l.rect(0, CALLE_Y - 1, ANCHO - 1, CALLE_Y - 1, (140, 136, 128))

    # lagos / estanques (parques)
    for (x0, x1) in lagos:

        agua_dibujo(l, x0, CALLE_Y - 1, x1, CALLE_FIN, rgb("#4f8fc9"), seed=x0)

        l.rect(x0, CALLE_Y - 2, x1, CALLE_Y - 2, rgb("#8a9a7a"))

        # juncos y patitos
        for k in range(x0 + 4, x1 - 3, 11):

            l.rect(k, CALLE_Y - 5, k, CALLE_Y - 2, rgb("#5a8a4a"))
            l.rect(k + 1, CALLE_Y - 4, k + 1, CALLE_Y - 2, rgb("#6a9a5a"))

        for k in range(x0 + 8, x1 - 8, 26):

            l.rect(k, CALLE_Y + 4, k + 3, CALLE_Y + 5, BLANCO)
            l.rect(k + 3, CALLE_Y + 3, k + 4, CALLE_Y + 4, BLANCO)
            l.px(k + 5, CALLE_Y + 3, rgb("#e0944f"))

    # calles que cruzan: asfalto + paso peatonal
    for (x0, x1) in esquinas:

        if cfg["suelo"][1] == "pasto":
            continue

        l.rect(x0, CALLE_Y - 2, x1, CALLE_Y - 2, (120, 120, 122))

        # rampa en la vereda
        for k in range(x0 + 2, x1 - 1, 4):

            l.rect(k, CALLE_Y, k + 1, CALLE_FIN, (236, 234, 226))

    return l


def pintar_especiales(l, cfg, r, ancho_mundo=ANCHO):
    """Pañuelos blancos de la Plaza de Mayo, palomas, etc."""

    esp = cfg.get("especiales", [])

    if "panuelos" in esp:

        # los panuelos blancos pintados en el piso de la plaza
        for x in range(30, ancho_mundo - 20, 34):

            y = BASE + 5 + (x // 34) % 3

            blanco = rgb("#f6f4ee")
            borde = rgb("#9a968a")

            l.poly([(x, y), (x + 9, y), (x + 4, y + 5)], borde)
            l.poly([(x + 1, y), (x + 8, y), (x + 4, y + 4)], blanco)

            l.px(x + 4, y + 4, rgb("#d8d4c8"))


# ==========================================================
# LA CALLE: EDIFICIOS, ARBOLES, OBJETOS, VEHICULOS
# ==========================================================

class Zona:
    """Un monumento ya ubicado: x0..x1 es el dibujo, z0..z1 con margen."""

    def __init__(self, idm, sprite, cx, margen):

        self.id = idm
        self.sprite = sprite

        self.x0 = cx - sprite.w // 2
        self.x1 = self.x0 + sprite.w - 1

        self.z0 = self.x0 - margen
        self.z1 = self.x1 + margen


def zona_en(x, zonas):

    for z in zonas:

        if z.z0 <= x <= z.z1:
            return z

    return None


def proximo_inicio(x, zonas):

    c = [z.z0 for z in zonas if z.z0 > x]

    return min(c) if c else ANCHO


def sin_monumento(x0, x1, zonas, margen=2):
    """True si el rango no toca ningun monumento."""

    for z in zonas:

        if x1 >= z.x0 - margen and x0 <= z.x1 + margen:
            return False

    return True


def dibujar_fondo_edificios(cfg, r, zonas):
    """El plano de atras: siluetas continuas de edificios (se les da bruma)."""

    atras = Lienzo(ANCHO, ALTO)

    cols = {
        "frances": ["#c9b79a", "#bfae9a", "#d0c0aa"],
        "default": ["#b8b0a4", "#c4b8a8", "#aeb4b8", "#c8bcae", "#b8a898"],
    }

    base_cols = [hx(c) for c in cols["default"]]

    if "frances" in cfg["skyline"]:
        base_cols = [hx(c) for c in cols["frances"]]

    x = -4

    while x < ANCHO:

        w = r.randint(14, 30)

        h = r.randint(*cfg.get("fondo_alto", (30, 66)))

        if cfg.get("plaza", 0) > 0.3:
            h = r.randint(18, 40)

        spr = E.fondo_edificio(w, h, r, dict(fachada=r.choice(base_cols)))

        atras.pegar(spr, x, BASE - 2 - spr.h)

        x += w - 1

    return atras


def segmentos(cfg, r, zonas):
    """
    Reparte la calle en edificios, plazas y esquinas.
    Devuelve (edificios, plazas, esquinas) con (x, ancho, ...).
    """

    estilos = list(cfg["estilos"].items())

    edificios = []
    plazas = []
    esquinas = []

    x = -r.randint(0, 6)

    previo = None
    previo_estilo = None

    while x < ANCHO:

        z = zona_en(x, zonas)

        if z is not None:

            x = z.z1 + 1
            previo = "monumento"
            previo_estilo = None

            continue

        limite = proximo_inicio(x, zonas)

        libre = limite - x

        if libre < 20:

            plazas.append((x, limite - 1))
            x = limite
            previo = "plaza"
            continue

        u = r.random()

        # Despues de una plaza o una esquina viene un edificio
        if previo in ("plaza", "esquina", "monumento"):
            u = 1.0

        if u < cfg.get("plaza", 0.1):

            plazo_min, plazo_max = (60, 130) if cfg.get("plaza", 0) > 0.3 else (46, 90)

            w = min(r.randint(plazo_min, plazo_max), libre)

            if libre - w < 20:
                w = libre

            plazas.append((x, x + w - 1))
            x += w
            previo = "plaza"

            continue

        if u < cfg.get("plaza", 0.1) + cfg.get("esquina", 0.1) and libre >= 40:

            w = r.randint(26, 34)

            esquinas.append((x, x + w - 1))
            x += w
            previo = "esquina"

            continue

        # edificio
        opciones = [(n, p) for n, p in estilos if n != previo_estilo] or estilos

        nombre = elegir_pesos(opciones, r)

        fn, (wmin, wmax), (hmin, hmax) = ESTILOS[nombre]

        w = r.randint(wmin, wmax)

        if libre - w < 24:
            w = libre

        if w > wmax * 1.5:

            # no entra un edificio razonable: queda como plaza
            plazas.append((x, x + w - 1))
            x += w
            previo = "plaza"

            continue

        h = r.randint(hmin, hmax)

        edificios.append((x, w, h, nombre))

        x += w

        previo = "edificio"
        previo_estilo = nombre

    return edificios, plazas, esquinas


def prop_ancho_arbol(tipo, h):

    return int(h * (1.0 if tipo in ("ombu", "ficus", "sauce") else 0.7))


def colocar_props(cfg, r, zonas, plazas, esquinas, edificios):
    """
    Elige donde va cada arbol y cada objeto de la calle.
    Devuelve una lista de (x, tipo, extra) ordenada por x.
    """

    resultado = []

    ocupado = []   # intervalos (x0, x1) ya usados

    def libre(x0, x1):

        if not sin_monumento(x0, x1, zonas, 2):
            return False

        for (a, b) in ocupado:

            if x1 >= a - 2 and x0 <= b + 2:
                return False

        for (a, b) in esquinas:

            if x1 >= a + 2 and x0 <= b - 2:
                return False

        return True

    def poner(x0, x1, tipo, extra=None):

        ocupado.append((x0, x1))
        resultado.append(((x0 + x1) // 2, tipo, extra))

    # --- carteles de calle y semaforos en cada esquina
    for i, (a, b) in enumerate(esquinas):

        nombre = cfg["calles"][i % len(cfg["calles"])]

        resultado.append((a + 2, "cartel_calle", nombre))
        resultado.append((b - 2, "semaforo", None))

        ocupado.append((a, a + 4))
        ocupado.append((b - 4, b))

    # --- plazas: arboles y bancos
    for (a, b) in plazas:

        ancho = b - a + 1

        x = a + r.randint(4, 10)

        while x < b - 8:

            tipo = elegir_pesos(cfg["arboles"], r)

            h = r.randint(34, 54) if cfg.get("plaza", 0) > 0.3 else r.randint(32, 50)

            w = prop_ancho_arbol(tipo, h)

            if x + w // 2 > b:
                break

            if libre(x - w // 2, x + w // 2):

                poner(x - w // 2, x + w // 2, "arbol", (tipo, h))

                x += w // 2 + r.randint(8, 22)

            else:

                x += 6

        # un banco, a veces
        if ancho > 36 and r.random() < 0.7:

            bx = r.randint(a + 6, b - 18)

            if libre(bx, bx + 10):
                poner(bx, bx + 10, "banco")

    # --- farolas cada tanto, a lo largo de toda la calle
    x = r.randint(30, 80)

    while x < ANCHO - 20:

        if libre(x - 2, x + 2) and zona_en(x, zonas) is None:

            if "farol_colgante" in cfg["props"] and r.random() < 0.5:
                poner(x - 2, x + 8, "farol_colgante")
            else:
                poner(x - 2, x + 2, "farola")

        x += r.randint(80, 140)

    # --- arboles de vereda
    x = r.randint(20, 60)

    while x < ANCHO - 20:

        if r.random() < cfg.get("prob_arbol", 0.4):

            tipo = elegir_pesos(cfg["arboles"], r)

            h = r.randint(26, 40)

            w = prop_ancho_arbol(tipo, h)

            if libre(x - w // 2, x + w // 2):
                poner(x - w // 2, x + w // 2, "arbol", (tipo, h))

        x += r.randint(40, 90)

    # --- el resto de los objetos
    anchos = {
        "banco": 11, "cesto": 5, "kiosco": 18, "parada": 30, "subte": 16,
        "cabina": 6, "semaforo": 3, "feria": 22, "chori": 16, "banderin": 11,
        "tango": 10, "bandera": 9, "grua": 50, "bolardo": 4, "farola": 5,
        "farol_colgante": 10,
    }

    otros = [(k, v) for k, v in cfg["props"].items() if k not in ("farola", "farol_colgante")]

    x = r.randint(30, 90)

    while x < ANCHO - 40 and otros:

        tipo = elegir_pesos(otros, r)

        w = anchos[tipo]

        if tipo == "grua":
            x0 = x - 16
            x1 = x + 34
        else:
            x0 = x
            x1 = x + w

        if libre(x0, x1):
            poner(x0, x1, tipo)

        x += r.randint(34, 70)

    return sorted(resultado, key=lambda t: t[0])


def dibujar_prop(l, x, tipo, extra, cfg, r):
    """Dibuja un objeto de la calle con los pies en la vereda."""

    yb = BASE + 3

    if tipo == "arbol":

        t, h = extra

        E_arbol_base = BASE + 4

        arbol(l, x, E_arbol_base, h, t, seed=x)

    elif tipo == "farola":

        farola(l, x, yb, r.randint(26, 30), c=rgb("#2a3030"))

    elif tipo == "farol_colgante":

        E.farol_colgante(l, x - 4, yb, 30)

    elif tipo == "banco":

        banco(l, x - 5, yb)

    elif tipo == "cesto":

        E.cesto(l, x, yb)

    elif tipo == "kiosco":

        kiosco(l, x - 8, yb + 1, c=r.choice([rgb("#2f8f5a"), rgb("#c0322b"), rgb("#2f6fd0"), rgb("#e0944f")]))

    elif tipo == "parada":

        parada_colectivo(l, x - 14, yb)

    elif tipo == "subte":

        entrada_subte(l, x - 8, yb)

    elif tipo == "cabina":

        cabina_telefonica(l, x - 3, yb)

    elif tipo == "semaforo":

        E.semaforo(l, x, yb)

    elif tipo == "feria":

        E.puesto_feria(l, x - 11, yb + 1, r.choice([ROJO, rgb("#2f6fd0"), rgb("#e0944f"), rgb("#8a5ac8"), rgb("#2f8f5a")]))

    elif tipo == "chori":

        E.carrito_chori(l, x - 8, yb + 1)

    elif tipo == "banderin":

        E.banderin_boca(l, x - 4, yb, r.randint(30, 40))

    elif tipo == "tango":

        E.pareja_tango(l, x - 5, yb + 1)

    elif tipo == "bandera":

        bandera(l, x - 4, yb, 40, 9, 5)

    elif tipo == "grua":

        E.grua_portuaria(l, x - 7, yb + 1, r.randint(50, 62))

    elif tipo == "bolardo":

        E.bolardo(l, x - 1, yb + 1)

    elif tipo == "cartel_calle":

        cartel_calle(l, x, yb + 1, extra, alto=24)

    # (cartel_calle ya usa el nombre real de la calle)


def dibujar_trafico(l, cfg, r, zonas):
    """Autos, taxis y colectivos estacionados o parados en la calle."""

    tipos = list(cfg["trafico"].items())

    colores_auto = [ROJO, rgb("#2f6fd0"), rgb("#e8e4d8"), rgb("#2f8f5a"), rgb("#8a8f98"),
                    rgb("#e0944f"), rgb("#6a3a8a")]

    colores_cole = [rgb("#2a6fc0"), rgb("#c0322b"), rgb("#2f8f5a"), rgb("#e0944f"), rgb("#8a5ac8")]

    x = r.randint(10, 60)

    yb = CALLE_FIN - 1

    while x < ANCHO - 50:

        t = elegir_pesos(tipos, r)

        flip = r.random() < 0.5

        if t == "colectivo":

            E.colectivo(l, x, yb + 1, r.choice(colores_cole), flip)

            x += 38

        elif t == "taxi":

            E.taxi(l, x, yb, flip)

            x += 18

        else:

            E.auto(l, x, yb, r.choice(colores_auto), flip)

            x += 18

        x += r.randint(40, 150)


# ==========================================================
# LUCES DE LA NOCHE
# ==========================================================

VIDRIOS = {VIDRIO, VIDRIO_LUZ, VIDRIO_OSC}


def etiquetar_ventanas(mask):

    h, w = mask.shape

    lab = np.zeros((h, w), np.int32)

    n = 0

    ys, xs = np.nonzero(mask)

    for y0, x0 in zip(ys, xs):

        if lab[y0, x0]:
            continue

        n += 1

        lab[y0, x0] = n

        pila = [(y0, x0)]

        while pila:

            cy, cx = pila.pop()

            for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):

                if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]:

                    lab[ny, nx] = n
                    pila.append((ny, nx))

    return lab, n


def ventanas_a_encender(l, prob, r):
    """Mascara con las ventanas (de los colores de vidrio) que se prenden."""

    a = np.array(l.im)

    mask = np.zeros(a.shape[:2], bool)

    for c in VIDRIOS:
        mask |= np.all(a[..., :3] == np.array(c), axis=-1) & (a[..., 3] > 0)

    lab, n = etiquetar_ventanas(mask)

    prender = np.zeros(n + 1, bool)

    for i in range(1, n + 1):
        prender[i] = r.random() < prob

    return prender[lab] & mask


def tenir(l, color, t):
    """Mezcla todo lo dibujado con un color (hora del dia / lejania)."""

    l.bruma(color, t)


def prender_luces(l, mask):

    a = np.array(l.im)

    a[mask] = (255, 224, 128, 255)

    # un brillo arriba a la izquierda de cada ventana
    sup = np.zeros_like(mask)
    sup[1:, :] = mask[1:, :] & ~mask[:-1, :]

    a[sup] = (255, 244, 190, 255)

    l.im = Image.fromarray(a, "RGBA")
    l.d = ImageDraw.Draw(l.im)


# ==========================================================
# CARTELES DE BIENVENIDA Y DE SALIDA
# ==========================================================

def cartel_grande(l, x, y_base, lineas, fondo, color_texto, esc=1, flecha=False):
    """Cartel sobre dos postes con una o dos lineas de texto."""

    anchos = [ancho_texto(t, e) for t, e in lineas]

    ancho = max(anchos) + 10 + (12 if flecha else 0)

    alto = sum(7 * e + 3 for _, e in lineas) + 4

    y_top = y_base - alto - 14

    l.rect(x + 3, y_top, x + 5, y_base, rgb("#4a4f58"))
    l.rect(x + ancho - 6, y_top, x + ancho - 4, y_base, rgb("#4a4f58"))

    l.rect(x, y_top, x + ancho, y_top + alto, luz(fondo, 0.55))
    l.rect(x + 1, y_top + 1, x + ancho - 1, y_top + alto - 1, fondo)

    yy = y_top + 3

    for (t, e) in lineas:

        tw = ancho_texto(t, e)

        l.texto(x + (ancho - tw - (12 if flecha else 0)) // 2 + 1, yy, t, color_texto, e)

        yy += 7 * e + 3

    if flecha:

        E.flecha_derecha(l, x + ancho - 13, y_top + alto // 2 - 2, color_texto)

    return ancho


# ==========================================================
# ARMADO DE UN NIVEL
# ==========================================================

def armar_nivel(n, verbose=True):

    cfg = NIVELES[n]

    r = random.Random(1000 + n)

    # ---- monumentos
    todos = monumentos.cargar([n])[n]

    por_id = {m["id"]: m for m in todos}

    zonas = []

    sprites = {}

    for idm, cx in cfg["monumentos"]:

        spr = monumentos.construir(por_id[idm])

        sprites[idm] = spr

        zonas.append(Zona(idm, spr, cx, margen=10))

    zonas.sort(key=lambda z: z.x0)

    # ---- capas
    horizonte = hx(cfg["cielo"][2])

    atras = dibujar_fondo_edificios(cfg, r, zonas)

    edificios, plazas, esquinas = segmentos(cfg, r, zonas)

    frente = Lienzo(ANCHO, ALTO)

    for (x, w, h, nombre) in edificios:

        fn = ESTILOS[nombre][0]

        c = elegir_paleta(cfg, nombre, r)

        spr = fn(w, h, r, c)

        frente.pegar(spr, x, BASE - spr.h)

    # lagos del parque, en las plazas mas anchas
    lagos = []

    if "lagos" in cfg.get("especiales", []):

        for (a, b) in plazas:

            if b - a > 80 and r.random() < 0.7:
                lagos.append((a + 8, b - 8))

    props = colocar_props(cfg, r, zonas, plazas, esquinas, edificios)

    # ---- bruma, hora del dia y luces (capa por capa, antes de apilarlas,
    # para que las ventanas prendidas no queden tapadas por otra capa)
    luces = cfg.get("luces", 0.0) if cfg.get("noche", 0) > 0 else 0.0

    def preparar(capa, bruma, prob_luces):

        mascara = ventanas_a_encender(capa, prob_luces, r) if prob_luces > 0 else None

        tenir(capa, horizonte, bruma)

        if "tinte" in cfg:

            col, t = cfg["tinte"]

            tenir(capa, hx(col), t)

        if mascara is not None:
            prender_luces(capa, mascara)

    preparar(atras, 0.55, luces * 0.6)
    preparar(frente, 0.07, luces)

    ciudad = Lienzo(ANCHO, ALTO)

    ciudad.pegar(atras, 0, 0)
    ciudad.pegar(frente, 0, 0)

    mons = Lienzo(ANCHO, ALTO)

    for z in zonas:
        mons.pegar(z.sprite, z.x0, BASE - z.sprite.h)

    preparar(mons, 0.04, luces)

    ciudad.pegar(mons, 0, 0)

    suelo = hacer_suelo(cfg, r, esquinas, lagos)

    preparar(suelo, 0.0, 0.0)

    ciudad.pegar(suelo, 0, 0)

    # objetos de la calle
    objetos = Lienzo(ANCHO, ALTO)

    for (x, tipo, extra) in props:
        dibujar_prop(objetos, x, tipo, extra, cfg, r)

    pintar_especiales(objetos, cfg, r)

    # palomas en las plazas (Plaza de Mayo, Congreso)
    if "palomas" in cfg.get("especiales", []):

        for (a, b) in plazas:

            for _ in range(max(2, (b - a) // 20)):

                E.paloma(objetos, r.randint(a + 3, max(a + 4, b - 6)), BASE + r.randint(5, 8))

    if cfg["suelo"][1] != "pasto":
        dibujar_trafico(objetos, cfg, r, zonas)

    # carteles de bienvenida y de salida
    cartel_grande(
        objetos, 70, BASE + 5,
        [("BIENVENIDOS A", 1), (cfg["barrio"], 2)],
        rgb("#1f4a8f"), BLANCO
    )

    sig = cfg["siguiente"]

    if sig:
        cartel_grande(objetos, 3010, BASE + 5, [("SEGUI A", 1), (sig, 1)],
                      rgb("#1f6f3f"), BLANCO, flecha=True)
    else:
        cartel_grande(objetos, 3030, BASE + 5, [("FIN DEL", 1), ("RECORRIDO", 1)],
                      rgb("#8f1f2a"), rgb("#ffe27a"))

    preparar(objetos, 0.0, 0.0)

    ciudad.pegar(objetos, 0, 0)

    cielo_img = hacer_cielo(n, cfg)

    if verbose:
        print(f"nivel {n:2d} {cfg['barrio']:15s} edificios={len(edificios):3d} "
              f"plazas={len(plazas):2d} esquinas={len(esquinas):2d} props={len(props):3d}")

    return cielo_img, ciudad, sprites


def guardar_nivel(n, cielo_img, ciudad, sprites):

    os.makedirs(CARPETA_NIVELES, exist_ok=True)
    os.makedirs(CARPETA_MONUMENTOS, exist_ok=True)

    cielo_img.im.convert("RGB").save(os.path.join(CARPETA_NIVELES, f"nivel_{n:02d}_cielo.png"))

    ciudad.guardar(os.path.join(CARPETA_NIVELES, f"nivel_{n:02d}_ciudad.png"))

    for idm, spr in sprites.items():
        spr.guardar(os.path.join(CARPETA_MONUMENTOS, f"{idm}.png"))


def vista_previa(n, cielo_img, ciudad, carpeta, escala=2):
    """
    Imagen de control: el nivel entero con el cielo detras (parallax en 0),
    en una tira ancha, para revisar a ojo.
    """

    os.makedirs(carpeta, exist_ok=True)

    # cielo estirado para cubrir el nivel entero (solo vista previa)
    tira = Lienzo(ANCHO, ALTO)

    for x in range(0, ANCHO, ANCHO_CIELO):
        tira.pegar(cielo_img, x, 0)

    tira.pegar(ciudad, 0, 0)

    img = tira.im.convert("RGB")

    img.resize((ANCHO * escala // 2, ALTO * escala // 2), Image.NEAREST).save(
        os.path.join(carpeta, f"nivel_{n:02d}_tira.png")
    )

    # recortes del tamano de la pantalla del juego, centrados en cada
    # monumento (y el comienzo y el final del nivel)
    camaras = [0] + [max(0, min(ANCHO - ANCHO_VISTA, cx - ANCHO_VISTA // 2))
                     for _, cx in NIVELES[n]["monumentos"]] + [ANCHO - ANCHO_VISTA]

    paneles = []

    for k, camara in enumerate(camaras):

        pantalla = Lienzo(ANCHO_VISTA, ALTO)

        off_cielo = int(camara * 0.35)

        pantalla.pegar(cielo_img.im.crop((off_cielo, 0, off_cielo + ANCHO_VISTA, ALTO)), 0, 0)
        pantalla.pegar(ciudad.im.crop((camara, 0, camara + ANCHO_VISTA, ALTO)), 0, 0)

        grande = pantalla.im.convert("RGB").resize((ANCHO_VISTA * 3, ALTO * 3), Image.NEAREST)

        grande.save(os.path.join(carpeta, f"nivel_{n:02d}_pantalla_{k}.png"))

        paneles.append(grande.resize((ANCHO_VISTA * 3 // 2, ALTO * 3 // 2), Image.NEAREST))

    # montaje de 3 columnas
    pw, ph = paneles[0].size

    cols = 3

    filas = (len(paneles) + cols - 1) // cols

    m = Image.new("RGB", (pw * cols, ph * filas), (0, 0, 0))

    for i, p in enumerate(paneles):
        m.paste(p, ((i % cols) * pw, (i // cols) * ph))

    m.save(os.path.join(carpeta, f"nivel_{n:02d}_montaje.png"))


def main(argv):

    vista = "--vista" in argv

    numeros = [int(a) for a in argv if a.isdigit()]

    niveles = numeros or sorted(NIVELES)

    carpeta_vista = os.path.join(HERRAMIENTAS, "vistas")

    for n in niveles:

        cielo_img, ciudad, sprites = armar_nivel(n)

        guardar_nivel(n, cielo_img, ciudad, sprites)

        if vista:
            vista_previa(n, cielo_img, ciudad, carpeta_vista)

    print("Listo:", CARPETA_NIVELES)


if __name__ == "__main__":

    main(sys.argv[1:])

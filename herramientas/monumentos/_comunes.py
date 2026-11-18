"""
Dibujos que se repiten en varias localidades del conurbano (niveles 16 a 30):
estaciones de tren, iglesias, palacios municipales, estadios, fabricas,
edificios modernos y monumentos de plaza.

Cada funcion devuelve un Lienzo con la base en la fila de abajo. Los colores y
las medidas cambian de una localidad a otra, asi no se ven repetidos. Despues
los dibujos se achican (ver generar_techos.achicar_monumento), por eso importan
mas la silueta y el color que el detalle.
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# AYUDAS
# ==========================================================

def reloj_de_torre(l, cx, cy, r=5):
    """Reloj redondo con sus agujas (las ocho y diez)."""

    l.circulo(cx, cy, r + 1, rgb("#4a4038"))
    l.circulo(cx, cy, r, rgb("#f4f1e8"))
    l.linea(cx, cy, cx - r // 2, cy - r // 2 + 1, NEGRO)
    l.linea(cx, cy, cx + r // 2, cy - 1, NEGRO)


def cartel_nombre(l, cx, y, texto, fondo, color=BLANCO):
    """Cartel con el nombre del lugar, centrado en cx (arriba en y)."""

    w = ancho_texto(texto)

    l.rect(cx - w // 2 - 3, y, cx + w // 2 + 3, y + 10, sombra(fondo, 0.55))
    l.rect(cx - w // 2 - 2, y + 1, cx + w // 2 + 2, y + 9, fondo)
    l.texto(cx - w // 2, y + 2, texto, color)


def pasto(l, x0, x1, base, c=None):
    """Una franja de cesped y vereda al pie de un monumento."""

    c = c or rgb("#4f8f3f")

    l.rect(x0, base - 1, x1, base, c)
    l.rect(x0, base - 1, x1, base - 1, luz(c, 0.18))


def ventana_fila(l, x0, x1, y, w, h, sep, vidrio=VIDRIO, marco=None, arco=False):
    """Una fila de ventanas desde x0 hasta x1 (y = fila de abajo)."""

    x = x0

    while x + w <= x1:

        if arco:

            ventana_arco(l, x, y, x + w - 1, h, vidrio, marco)

        else:

            if marco is not None:
                l.rect(x - 1, y - h, x + w, y + 1, marco)

            l.rect(x, y - h + 1, x + w - 1, y, vidrio)
            l.px(x, y - h + 1, VIDRIO_LUZ)

        x += w + sep


# ==========================================================
# ESTACION DE TREN (Ferrocarril Roca, Sarmiento, Belgrano Sur)
# ==========================================================

def estacion(ancho=150, muro="#d8b878", techo="#a9472f", marco="#f0e6cc",
             texto="ESTACION", torre=True, alto_torre=30, farol=True):
    """
    Estacion de tren inglesa: cuerpo bajo con arcos, techo a dos aguas,
    marquesina sobre el anden con columnitas de hierro y, si hay, torre
    con reloj.
    """

    alto = 96

    l = Lienzo(ancho, alto)

    base = alto - 1

    muro = rgb(muro)
    techo = rgb(techo)
    marco = rgb(marco)

    x0, x1 = 6, ancho - 6

    # cuerpo
    y_top = base - 34

    volumen(l, x0, y_top, x1, base, muro, 1, 3)

    # techo a dos aguas con alero
    l.poly([(x0 - 4, y_top + 1), (x0 + 12, y_top - 13), (x1 - 12, y_top - 13), (x1 + 4, y_top + 1)], techo)
    l.rect(x0 - 4, y_top, x1 + 4, y_top + 1, sombra(techo, 0.7))
    l.rect(x0 + 12, y_top - 13, x1 - 12, y_top - 13, luz(techo, 0.3))

    # tejas
    for y in range(y_top - 11, y_top, 3):

        l.rect(x0 - 2 + (y_top - y), y, x1 + 2 - (y_top - y), y, sombra(techo, 0.84))

    # chimeneas
    for x in (x0 + 24, x1 - 26):

        l.rect(x, y_top - 22, x + 3, y_top - 10, rgb("#8a4a35"))
        l.rect(x - 1, y_top - 23, x + 4, y_top - 22, rgb("#5a2e22"))

    # cornisa
    l.rect(x0, y_top + 2, x1, y_top + 3, marco)

    # ventanas con arco y puertas
    ventana_fila(l, x0 + 7, x1 - 7, base - 3, 7, 19, 8, VIDRIO, marco, arco=True)

    # la puerta del medio
    cx = ancho // 2

    l.arco(cx - 5, base, cx + 5, 22, marco)
    l.arco(cx - 3, base - 1, cx + 3, 19, rgb("#3a2a22"))

    # torre con reloj
    if torre:

        volumen(l, cx - 10, y_top - alto_torre, cx + 10, y_top - 2, muro, 1, 3)

        l.rect(cx - 11, y_top - alto_torre - 1, cx + 11, y_top - alto_torre + 1, marco)

        aguja(l, cx, y_top - alto_torre - 1, 26, 17, techo)

        reloj_de_torre(l, cx, y_top - alto_torre // 2 - 4, 6)

        l.rect(cx, y_top - alto_torre - 22, cx, y_top - alto_torre - 17, rgb("#2c3a3a"))

    # marquesina del anden (a la derecha, apoyada en columnitas de hierro)
    l.rect(x1 - 30, base - 28, x1 + 2, base - 26, rgb("#4a5a5a"))

    for x in range(x1 - 28, x1 + 1, 9):

        l.rect(x, base - 26, x, base - 1, rgb("#2c3a3a"))

    # cartel de la estacion
    cartel_nombre(l, cx - 26, y_top + 5, texto[:12], rgb("#1f3f78"))

    # vias
    l.rect(0, base, ancho - 1, base, rgb("#4a4650"))

    for x in range(2, ancho, 6):

        l.rect(x, base, x + 2, base, rgb("#6b4a2f"))

    return l


# ==========================================================
# IGLESIA
# ==========================================================

def iglesia(ancho=104, muro="#e8dcc0", techo="#7a8aa0", detalle="#b8a880",
            torres=2, alto_torre=84, remate="aguja", cupula_central=False,
            roseton=True):
    """
    Iglesia de frente. torres = 0, 1 o 2. remate: "aguja" (punta), "cupula"
    (media naranja) o "plano" (campanario con balaustrada). Si hay
    cupula_central se ve una cupula detras de la fachada.
    """

    alto = 132

    l = Lienzo(ancho, alto)

    base = alto - 1

    muro = rgb(muro)
    techo = rgb(techo)
    detalle = rgb(detalle)

    cx = ancho // 2

    # cupula detras
    if cupula_central:

        l.rect(cx - 14, base - 96, cx + 14, base - 60, muro)

        l.rect(cx - 14, base - 96, cx - 14, base - 60, luz(muro, 0.1))
        l.rect(cx + 10, base - 96, cx + 14, base - 60, sombra(muro, 0.85))

        for dx in (-8, -2, 4):

            ventana_arco(l, cx + dx, base - 70, cx + dx + 3, 12, rgb("#2a3550"), detalle)

        cupula(l, cx, base - 96, 17, 17, techo, costillas=5, linterna=True, remate=ORO)

    # cuerpo central
    ancho_c = ancho - 2 * 22 if torres == 2 else ancho - 24

    x0 = cx - ancho_c // 2 if torres == 2 else (8 if torres == 1 else cx - ancho_c // 2)

    x1 = x0 + ancho_c

    volumen(l, x0, base - 70, x1, base, muro, 1, 3)

    # frontis
    l.poly([(x0 - 1, base - 70), (cx if torres == 2 else (x0 + x1) // 2, base - 92), (x1 + 1, base - 70)], muro)
    l.linea(x0 - 1, base - 70, (x0 + x1) // 2, base - 92, luz(muro, 0.3))
    l.linea((x0 + x1) // 2, base - 92, x1 + 1, base - 70, sombra(muro, 0.75))

    mid = (x0 + x1) // 2

    # roseton y cruz
    if roseton:

        l.circulo(mid, base - 60, 6, detalle)
        l.circulo(mid, base - 60, 4, rgb("#2a3550"))
        l.px(mid - 1, base - 62, rgb("#d86a4a"))
        l.px(mid + 1, base - 58, rgb("#e8c45a"))

    l.rect(mid, base - 100, mid, base - 94, ORO)
    l.rect(mid - 2, base - 98, mid + 2, base - 98, ORO)

    # portal con arco
    l.arco(mid - 8, base, mid + 8, 34, detalle)
    l.arco(mid - 6, base - 1, mid + 6, 30, rgb("#4a2e1c"))

    l.rect(mid, base - 28, mid, base - 1, rgb("#2a1a10"))

    # ventanas laterales
    for dx in (-17, 17):

        if x0 + 4 < mid + dx - 3 and mid + dx + 3 < x1 - 4:

            ventana_arco(l, mid + dx - 3, base - 18, mid + dx + 3, 22, rgb("#2a3550"), detalle)

    # escalones
    for i in range(3):

        l.rect(mid - 12 - i * 2, base - 2 + i, mid + 12 + i * 2, base - 2 + i,
               rgb("#e9e4d6") if i % 2 == 0 else rgb("#cfc9bb"))

    # torres
    posiciones = []

    if torres == 2:

        posiciones = [11, ancho - 12]

    elif torres == 1:

        posiciones = [ancho - 14]

    for tx in posiciones:

        l.rect(tx - 10, base - alto_torre + 18, tx + 10, base, muro)
        l.rect(tx - 10, base - alto_torre + 18, tx - 10, base, luz(muro, 0.1))
        l.rect(tx + 7, base - alto_torre + 18, tx + 10, base, sombra(muro, 0.85))

        # cornisas y ventanas del campanario
        l.rect(tx - 11, base - 56, tx + 11, base - 54, detalle)
        l.rect(tx - 11, base - alto_torre + 18, tx + 11, base - alto_torre + 20, detalle)

        ventana_arco(l, tx - 3, base - 30, tx + 3, 16, rgb("#2a3550"), detalle)
        ventana_arco(l, tx - 3, base - alto_torre + 36, tx + 3, 12, rgb("#2a3550"), detalle)

        top = base - alto_torre + 18

        if remate == "aguja":

            aguja(l, tx, top - 1, 22, alto_torre // 3 + 6, techo)

            l.rect(tx, top - alto_torre // 3 - 12, tx, top - alto_torre // 3 - 7, ORO)
            l.rect(tx - 2, top - alto_torre // 3 - 10, tx + 2, top - alto_torre // 3 - 10, ORO)

        elif remate == "cupula":

            cupula(l, tx, top - 1, 10, 12, techo, costillas=2, linterna=True, remate=ORO)

        else:

            reja(l, tx - 10, tx + 10, top - 5, 3, detalle)

    return l


# ==========================================================
# PALACIO MUNICIPAL
# ==========================================================

def palacio_municipal(ancho=160, muro="#e6dcc4", techo="#6a7a8a", detalle="#bfae86",
                      torre=True, alto_torre=46, estilo="clasico", texto=None):
    """
    Municipalidad: dos alas con ventanas, entrada con columnas y, si hay,
    una torre central con reloj y bandera. estilo: "clasico" (frontis y
    columnas) o "racionalista" (bloques lisos, ventanas verticales, como
    el Palacio Municipal de Moron).
    """

    alto = 118

    l = Lienzo(ancho, alto)

    base = alto - 1

    muro = rgb(muro)
    techo = rgb(techo)
    detalle = rgb(detalle)

    cx = ancho // 2

    y_top = base - 54

    # alas
    volumen(l, 4, y_top, ancho - 5, base, muro, 1, 3)

    l.rect(3, y_top - 2, ancho - 4, y_top, detalle)

    if estilo == "racionalista":

        # ventanas altas y angostas, entre pilastras
        for x in range(12, ancho - 12, 10):

            if abs(x - cx) < 22:
                continue

            l.rect(x, y_top + 6, x + 3, base - 8, VIDRIO)
            l.rect(x, y_top + 6, x, y_top + 7, VIDRIO_LUZ)
            l.rect(x + 4, y_top + 4, x + 4, base - 2, sombra(muro, 0.88))

        l.rect(4, base - 6, ancho - 5, base - 5, detalle)

    else:

        ventana_fila(l, 10, cx - 24, y_top + 14, 6, 11, 7, VIDRIO, detalle)
        ventana_fila(l, cx + 22, ancho - 10, y_top + 14, 6, 11, 7, VIDRIO, detalle)
        ventana_fila(l, 10, cx - 24, base - 6, 6, 12, 7, VIDRIO, detalle)
        ventana_fila(l, cx + 22, ancho - 10, base - 6, 6, 12, 7, VIDRIO, detalle)

    # cuerpo central, un poco mas alto
    volumen(l, cx - 22, y_top - 16, cx + 22, base, muro, 1, 3)

    l.rect(cx - 23, y_top - 18, cx + 23, y_top - 16, detalle)

    if estilo == "clasico":

        fronton(l, cx - 22, cx + 22, y_top - 18, 10, muro, rgb("#cfc4a8"), detalle)

        columnas(l, cx - 17, cx + 17, y_top - 6, base - 3, 5, 4, rgb("#f0e8d6"))

    else:

        # pilares lisos y el portal
        for dx in (-16, -8, 0, 8, 16):

            l.rect(cx + dx - 1, y_top - 8, cx + dx + 1, base - 3, luz(muro, 0.18))

        l.rect(cx - 5, base - 22, cx + 5, base - 1, rgb("#2a2630"))

    # escalinata
    for i in range(4):

        l.rect(cx - 20 - i * 2, base - 3 + i, cx + 20 + i * 2, base - 3 + i,
               rgb("#e9e4d6") if i % 2 == 0 else rgb("#cfc9bb"))

    # torre con reloj
    if torre:

        ya = y_top - 16

        volumen(l, cx - 9, ya - alto_torre, cx + 9, ya, muro, 1, 3)

        l.rect(cx - 10, ya - alto_torre - 2, cx + 10, ya - alto_torre, detalle)

        reloj_de_torre(l, cx, ya - alto_torre + 14, 6)

        if estilo == "racionalista":

            l.rect(cx - 9, ya - alto_torre - 6, cx + 9, ya - alto_torre - 2, sombra(muro, 0.9))

            l.rect(cx, ya - alto_torre - 20, cx, ya - alto_torre - 6, rgb("#cfcfcf"))

            bandera(l, cx, ya - alto_torre - 6, 14, 8, 5)

        else:

            aguja(l, cx, ya - alto_torre - 1, 20, 18, techo)

            bandera(l, cx, ya - alto_torre - 18, 10, 7, 4)

    if texto:

        cartel_nombre(l, cx, base - 40, texto, rgb("#1f3f78"))

    return l


# ==========================================================
# ESTADIO
# ==========================================================

def estadio(ancho=190, color="#c8322d", color2="#f4f1e8", texto="ESTADIO",
            torres=4, forma="frente", color_techo="#8d939c"):
    """
    Estadio visto de afuera. forma:
        "frente"   paredon con arcos, tribuna atras y techo (La Fortaleza)
        "cilindro" cuerpo redondo con cintas de colores (el Cilindro)
        "visera"   dos viseras enormes sobre las tribunas (la Doble Visera)
    """

    alto = 118

    l = Lienzo(ancho, alto)

    base = alto - 1

    c = rgb(color)
    c2 = rgb(color2)
    gris = rgb(color_techo)

    cx = ancho // 2

    # torres de luces
    def torre_luces(x):

        l.rect(x, base - 100, x + 1, base - 10, rgb("#6a707a"))

        l.rect(x - 6, base - 108, x + 7, base - 100, rgb("#3a3f48"))

        for i in range(5):

            l.px(x - 5 + i * 3, base - 105, rgb("#fff4c8"))
            l.px(x - 5 + i * 3, base - 102, rgb("#fff4c8"))

    if torres >= 2:

        torre_luces(8)
        torre_luces(ancho - 10)

    if torres >= 4:

        torre_luces(cx - 54)
        torre_luces(cx + 54)

    if forma == "cilindro":

        # cuerpo redondo: de frente es un rectangulo con la cabeza curva
        l.rect(12, base - 76, ancho - 13, base, sombra(c, 0.7))
        l.elipse(12, base - 100, ancho - 13, base - 52, sombra(c, 0.7))
        l.rect(15, base - 74, ancho - 16, base, c)
        l.elipse(15, base - 97, ancho - 16, base - 55, c)
        l.rect(15, base - 74, 56, base, luz(c, 0.12))

        # cintas horizontales de colores
        for i, y in enumerate(range(base - 66, base - 10, 14)):

            l.rect(24, y, ancho - 25, y + 5, c2 if i % 2 == 0 else sombra(c, 0.85))

        # corona
        l.rect(22, base - 79, ancho - 23, base - 73, gris)

        # arcos de la base
        for x in range(26, ancho - 26, 10):

            l.arco(x, base - 1, x + 5, 11, rgb("#1d1a24"))

    elif forma == "visera":

        # tribuna
        volumen(l, 14, base - 56, ancho - 15, base, c, 1, 3)

        for x in range(22, ancho - 22, 9):

            l.rect(x, base - 50, x + 4, base - 6, sombra(c, 0.8))
            l.rect(x, base - 50, x, base - 6, luz(c, 0.12))

        # las dos viseras (techos que sobresalen)
        l.poly([(4, base - 52), (cx - 4, base - 78), (cx - 4, base - 66), (4, base - 46)], gris)
        l.poly([(cx + 4, base - 78), (ancho - 5, base - 52), (ancho - 5, base - 46), (cx + 4, base - 66)], gris)

        l.linea(4, base - 52, cx - 4, base - 78, luz(gris, 0.4))
        l.linea(ancho - 5, base - 52, cx + 4, base - 78, luz(gris, 0.4))

        # tirantes
        l.linea(8, base - 48, cx - 12, base - 70, rgb("#4a5058"))
        l.linea(ancho - 9, base - 48, cx + 12, base - 70, rgb("#4a5058"))

        # escudo central
        l.rect(cx - 7, base - 62, cx + 7, base - 40, c2)
        l.rect(cx - 6, base - 61, cx + 6, base - 41, sombra(c, 0.8))
        l.circulo(cx, base - 51, 4, c2)

    else:

        # tribuna con techo
        volumen(l, 12, base - 52, ancho - 13, base, c, 1, 3)

        l.rect(8, base - 68, ancho - 9, base - 56, gris)
        l.rect(8, base - 68, ancho - 9, base - 68, luz(gris, 0.35))

        for x in range(14, ancho - 12, 14):

            l.rect(x, base - 56, x + 1, base - 50, sombra(gris, 0.7))

        # arcos del paredon
        for x in range(20, ancho - 20, 13):

            l.arco(x, base - 1, x + 7, 20, sombra(c, 0.55))

        # franja de color
        l.rect(12, base - 46, ancho - 13, base - 41, c2)

    # cartel con el nombre
    cartel_nombre(l, cx, base - 44 if forma != "cilindro" else base - 50, texto, rgb("#1d1a24"), c2)

    pasto(l, 0, ancho - 1, base)

    return l


# ==========================================================
# FABRICA
# ==========================================================

def fabrica(ancho=150, muro="#a9472f", texto="FABRICA", chimeneas=2,
            alto_chimenea=96, techo_diente=True, tanque=False, vidrio=VIDRIO):
    """Fabrica de ladrillo con techo en dientes de sierra y chimeneas."""

    alto = 112

    l = Lienzo(ancho, alto)

    base = alto - 1

    muro = rgb(muro)

    # chimeneas (atras)
    for k in range(chimeneas):

        x = ancho - 24 - k * 26 if chimeneas > 1 else ancho - 24

        h = alto_chimenea - k * 14

        l.poly([(x - 5, base - 20), (x - 3, base - h), (x + 3, base - h), (x + 5, base - 20)], rgb("#8a4a35"))
        l.rect(x - 4, base - h - 3, x + 4, base - h, rgb("#5a2e22"))
        l.rect(x - 4, base - h + 14, x + 4, base - h + 15, rgb("#e8dcc4"))
        l.rect(x - 4, base - h + 28, x + 4, base - h + 29, rgb("#e8dcc4"))

    # cuerpo
    ladrillos(l, 4, base - 46, ancho - 5, base, muro)

    l.rect(4, base - 46, 4, base, luz(muro, 0.2))
    l.rect(ancho - 6, base - 46, ancho - 5, base, sombra(muro, 0.75))

    l.rect(3, base - 48, ancho - 4, base - 46, rgb("#e8dcc4"))

    # techo de dientes de sierra
    if techo_diente:

        x = 4

        while x + 18 <= ancho - 4:

            l.poly([(x, base - 48), (x, base - 62), (x + 14, base - 48)], rgb("#7a8590"))
            l.rect(x, base - 62, x + 1, base - 48, VIDRIO_LUZ)

            x += 18

    else:

        l.poly([(2, base - 48), (ancho // 2, base - 64), (ancho - 3, base - 48)], rgb("#7a8590"))

    # ventanas y porton
    ventana_fila(l, 12, ancho - 12, base - 26, 8, 12, 9, vidrio, rgb("#e8dcc4"), arco=True)

    l.rect(ancho // 2 - 9, base - 22, ancho // 2 + 9, base - 1, rgb("#3a3f48"))

    for x in range(ancho // 2 - 8, ancho // 2 + 9, 3):

        l.rect(x, base - 21, x, base - 2, rgb("#4a5058"))

    cartel_nombre(l, ancho // 2, base - 40, texto, rgb("#1f3f78"))

    # tanque elevado
    if tanque:

        l.rect(14, base - 78, 28, base - 64, rgb("#9aa0a8"))
        l.rect(14, base - 80, 28, base - 78, rgb("#5a6068"))

        for x in (15, 21, 27):

            l.rect(x, base - 64, x, base - 50, rgb("#4a5058"))

    return l


# ==========================================================
# EDIFICIO MODERNO (hospital, universidad, museo)
# ==========================================================

def edificio_moderno(ancho=150, alto=104, muro="#d8d8d4", vidrio_c="#5a8ab0",
                     texto=None, franja="#2f6fb0", cuerpos=2, escalonado=True,
                     cartel_fondo="#1f3f78"):
    """
    Edificio de hormigon y vidrio: cuerpos de distinta altura, ventanas
    corridas, escalera y cartel con el nombre.
    """

    l = Lienzo(ancho, alto)

    base = alto - 1

    muro = rgb(muro)
    vid = rgb(vidrio_c)
    franja = rgb(franja)

    # cuerpos
    ancho_c = (ancho - 8) // cuerpos

    for i in range(cuerpos):

        x0 = 4 + i * ancho_c

        x1 = x0 + ancho_c - 2

        h = (62 + (i % 2) * 22) if escalonado else 70

        volumen(l, x0, base - h, x1, base, muro, 1, 3)

        # ventanas corridas
        for y in range(base - h + 6, base - 16, 11):

            l.rect(x0 + 4, y, x1 - 4, y + 6, vid)
            l.rect(x0 + 4, y, x1 - 4, y, luz(vid, 0.35))

            for x in range(x0 + 10, x1 - 6, 12):

                l.rect(x, y, x, y + 6, sombra(vid, 0.6))

        l.rect(x0, base - h, x1, base - h + 2, franja)

    # entrada con marquesina
    cx = ancho // 2

    l.rect(cx - 14, base - 22, cx + 14, base - 20, rgb("#4a4f58"))

    l.rect(cx - 12, base - 19, cx + 12, base - 1, rgb("#2a4a6a"))

    l.rect(cx, base - 19, cx, base - 1, rgb("#8fb4d8"))

    for i in range(3):

        l.rect(cx - 16 - i, base - 2 + i, cx + 16 + i, base - 2 + i,
               rgb("#e9e4d6") if i % 2 == 0 else rgb("#cfc9bb"))

    if texto:

        cartel_nombre(l, cx, base - 36, texto, rgb(cartel_fondo))

    return l


# ==========================================================
# MONUMENTO DE PLAZA (columna con estatua y arboles)
# ==========================================================

def monumento_plaza(ancho=96, alto=118, piedra="#d8d0bc", figura_c="#6a7a6a",
                    bandera_arriba=False, arboles=True, glorieta=False):
    """
    Plaza con un monumento: pedestal escalonado, columna y una figura
    (o una bandera). Detras, arboles; si glorieta=True, un kiosco de hierro.
    """

    l = Lienzo(ancho, alto)

    base = alto - 1

    piedra = rgb(piedra)

    cx = ancho // 2

    if arboles:

        arbol(l, 12, base - 2, 70, "platano", seed=1)
        arbol(l, ancho - 14, base - 2, 66, "platano", seed=2)

    if glorieta:

        # kiosco de hierro con techito de cinc
        l.rect(cx - 22, base - 26, cx - 20, base - 1, rgb("#2c3a3a"))
        l.rect(cx + 20, base - 26, cx + 22, base - 1, rgb("#2c3a3a"))

        l.poly([(cx - 28, base - 26), (cx, base - 44), (cx + 28, base - 26)], rgb("#5f7f7c"))
        l.rect(cx - 28, base - 27, cx + 28, base - 25, sombra(rgb("#5f7f7c"), 0.7))

        l.rect(cx - 22, base - 8, cx + 22, base - 7, rgb("#2c3a3a"))

        for x in range(cx - 21, cx + 22, 4):

            l.rect(x, base - 7, x, base - 1, rgb("#2c3a3a"))

        return l

    # pedestal en escalones
    l.rect(cx - 22, base - 4, cx + 22, base - 1, piedra)
    l.rect(cx - 17, base - 9, cx + 17, base - 5, sombra(piedra, 0.9))
    l.rect(cx - 12, base - 34, cx + 12, base - 10, piedra)

    l.rect(cx - 12, base - 34, cx - 12, base - 10, luz(piedra, 0.25))
    l.rect(cx + 10, base - 34, cx + 12, base - 10, sombra(piedra, 0.8))

    # placa
    l.rect(cx - 6, base - 26, cx + 6, base - 18, rgb("#8a6a3a"))
    l.rect(cx - 5, base - 25, cx + 5, base - 19, rgb("#b08a3a"))

    if bandera_arriba:

        # columna alta con bandera
        l.rect(cx - 4, base - 100, cx + 4, base - 34, piedra)
        l.rect(cx - 4, base - 100, cx - 4, base - 34, luz(piedra, 0.25))
        l.rect(cx + 3, base - 100, cx + 4, base - 34, sombra(piedra, 0.8))
        l.rect(cx - 6, base - 102, cx + 6, base - 100, luz(piedra, 0.2))

        bandera(l, cx, base - 102, 14, 10, 6)

    else:

        figura(l, cx, base - 34, 40, rgb(figura_c), pose="brazo_der", falda=False)

    return l


# ==========================================================
# CASA / EDIFICIO CHICO CON CARACTER
# ==========================================================

def casa_colonial(ancho=120, muro="#efe6d0", teja="#b5532f", detalle="#8a6a3a",
                  patio=True, palmera=True, texto=None):
    """Casona baja de una planta con galeria de arcos, patio y teja."""

    alto = 84

    l = Lienzo(ancho, alto)

    base = alto - 1

    muro = rgb(muro)
    teja = rgb(teja)
    detalle = rgb(detalle)

    if palmera:

        arbol(l, ancho - 12, base - 1, 66, "palmera", seed=3)

    x0, x1 = 6, ancho - 22

    volumen(l, x0, base - 38, x1, base, muro, 1, 3)

    # techo de teja
    l.poly([(x0 - 4, base - 37), (x0 + 8, base - 50), (x1 - 8, base - 50), (x1 + 4, base - 37)], teja)
    l.rect(x0 - 4, base - 38, x1 + 4, base - 37, sombra(teja, 0.7))

    for y in range(base - 48, base - 38, 3):

        l.rect(x0 + 8 - (y - base + 48), y, x1 - 8 + (y - base + 48), y, sombra(teja, 0.85))

    # galeria de arcos
    for x in range(x0 + 6, x1 - 8, 14):

        l.arco(x, base - 1, x + 8, 24, sombra(muro, 0.6))
        l.arco(x + 1, base - 1, x + 7, 21, rgb("#2a3550"))

    l.rect(x0, base - 3, x1, base - 1, sombra(muro, 0.88))

    if patio:

        l.rect(x0 + 6, base - 38, x0 + 7, base - 4, detalle)

    if texto:

        cartel_nombre(l, (x0 + x1) // 2, base - 36, texto, rgb("#1f3f78"))

    return l


# ==========================================================
# TANQUE DE AGUA DEL FERROCARRIL
# ==========================================================

def torre_agua(ancho=72, alto=124, ladrillo="#a9605a", chapa="#7a8890"):
    """Torre de agua de estacion: patas de ladrillo, tanque redondo y techo conico."""

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    ladrillo = rgb(ladrillo)
    chapa = rgb(chapa)

    # torre de ladrillo
    ladrillos(l, cx - 14, base - 60, cx + 14, base, ladrillo)

    l.rect(cx - 15, base - 62, cx + 15, base - 60, rgb("#e8dcc4"))

    l.arco(cx - 5, base, cx + 5, 24, rgb("#2a1a10"))

    for dx in (-9, 9):

        ventana_arco(l, cx + dx - 2, base - 36, cx + dx + 2, 12, VIDRIO, rgb("#e8dcc4"))

    # tanque
    l.rect(cx - 22, base - 100, cx + 22, base - 62, chapa)
    l.rect(cx - 22, base - 100, cx - 16, base - 62, luz(chapa, 0.2))
    l.rect(cx + 15, base - 100, cx + 22, base - 62, sombra(chapa, 0.8))

    for y in (base - 92, base - 80, base - 68):

        l.rect(cx - 22, y, cx + 22, y, sombra(chapa, 0.6))

    # techo conico
    aguja(l, cx, base - 100, 52, 20, rgb("#5a4a42"))

    l.rect(cx, base - 126, cx, base - 120, rgb("#2c3a3a"))

    # cano para cargar las locomotoras
    l.rect(cx + 22, base - 70, cx + 34, base - 68, rgb("#2c3a3a"))
    l.rect(cx + 33, base - 68, cx + 34, base - 52, rgb("#2c3a3a"))

    return l

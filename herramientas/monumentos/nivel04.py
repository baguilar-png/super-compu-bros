"""
NIVEL 4 - PLAZA DE MAYO

    * Casa Rosada (casa de gobierno, rosa)
    * Cabildo de Buenos Aires (arcadas blancas y torre con reloj)
    * Catedral Metropolitana (12 columnas y frontis triangular)
    * Piramide de Mayo (obelisco blanco con la estatua de la Libertad)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# CASA ROSADA
# ==========================================================

def casa_rosada():

    ancho = 252
    alto = 100

    l = Lienzo(ancho, alto)

    base = alto - 1

    rosa = rgb("#e8a2ab")
    blanco = rgb("#f6efe6")
    pizarra = rgb("#59606e")

    def pabellon(x0, x1):

        # cuerpo
        volumen(l, x0, base - 56, x1, base, rosa, 1, 3)

        # mansarda de pizarra con buhardillas
        l.poly([(x0 - 2, base - 56), (x0 + 5, base - 70), (x1 - 5, base - 70), (x1 + 2, base - 56)], pizarra)
        l.rect(x0 + 5, base - 70, x1 - 5, base - 70, luz(pizarra, 0.3))

        for x in range(x0 + 8, x1 - 8, 11):
            l.rect(x, base - 66, x + 4, base - 59, blanco)
            l.rect(x + 1, base - 65, x + 3, base - 60, VIDRIO)

        cornisa(l, x0, x1, base - 58, blanco)

        # ventanas
        for x in range(x0 + 5, x1 - 5, 9):

            ventana_arco(l, x, base - 6, x + 4, 14, VIDRIO, blanco)
            ventana_arco(l, x, base - 30, x + 4, 15, VIDRIO, blanco)

        # esquinas de piedra
        l.rect(x0, base - 56, x0 + 1, base, blanco)
        l.rect(x1 - 1, base - 56, x1, base, blanco)

    # alas bajas con galeria
    volumen(l, 4, base - 44, ancho - 5, base, rosa, 1, 3)

    cornisa(l, 4, ancho - 5, base - 46, blanco)

    # balaustrada del techo
    for x in range(6, ancho - 6, 3):
        l.rect(x, base - 51, x, base - 47, blanco)

    l.rect(4, base - 52, ancho - 5, base - 52, blanco)

    for x in range(14, ancho - 14, 12):

        ventana_arco(l, x, base - 6, x + 5, 16, VIDRIO, blanco)
        ventana_arco(l, x, base - 28, x + 5, 15, VIDRIO, blanco)

    # pabellones de los extremos
    pabellon(4, 40)
    pabellon(ancho - 41, ancho - 5)

    # cuerpo central, mas alto
    cx = ancho // 2

    volumen(l, cx - 38, base - 62, cx + 38, base, rosa, 1, 3)

    cornisa(l, cx - 38, cx + 38, base - 64, blanco)

    for x in range(cx - 38, cx + 39, 3):
        l.rect(x, base - 69, x, base - 65, blanco)

    l.rect(cx - 38, base - 70, cx + 38, base - 70, blanco)

    # frontis bajo del cuerpo central
    l.poly([(cx - 20, base - 70), (cx, base - 80), (cx + 20, base - 70)], blanco)
    l.poly([(cx - 17, base - 71), (cx, base - 78), (cx + 17, base - 71)], rosa)

    l.circulo(cx, base - 73, 2, ORO)

    # balcon principal (el del discurso)
    ventana_arco(l, cx - 6, base - 30, cx + 6, 26, VIDRIO, blanco)

    l.rect(cx - 12, base - 31, cx + 12, base - 30, blanco)

    balcon(l, cx - 12, cx + 12, base - 35, NEGRO, alto=3)

    # pilares a los costados del balcon
    for dx in (-18, 18):

        l.rect(cx + dx - 1, base - 58, cx + dx + 1, base - 8, blanco)

    for dx in (-30, 30):

        ventana_arco(l, cx + dx - 3, base - 30, cx + dx + 3, 20, VIDRIO, blanco)

    # tres arcos de entrada abajo
    for dx in (-24, 0, 24):

        ventana_arco(l, cx + dx - 6, base, cx + dx + 6, 26, rgb("#4a3a3a"), blanco)

        l.rect(cx + dx - 5, base - 14, cx + dx + 5, base - 14, rgb("#6a5a5a"))

    # escalinata
    for i in range(3):
        l.rect(cx - 36 + i * 2, base - 2 + i, cx + 36 - i * 2, base - 2 + i,
               rgb("#e0d8c8") if i % 2 == 0 else rgb("#c4bba8"))

    # banderas
    bandera(l, cx, base - 80, 22, ancho=14, alto=8)

    for x in (9, ancho - 12):
        bandera(l, x, base - 70, 14, ancho=9, alto=5)

    return l


# ==========================================================
# CABILDO
# ==========================================================

def cabildo():

    ancho = 156
    alto = 128

    l = Lienzo(ancho, alto)

    base = alto - 1

    blanco = rgb("#f6f2e8")
    verde = rgb("#2f6a4a")
    teja = rgb("#b5532f")

    cx = ancho // 2

    # --- techos de teja (a los costados de la torre) ---
    l.poly([(6, base - 54), (14, base - 62), (cx - 14, base - 62), (cx - 14, base - 54)], teja)
    l.poly([(ancho - 7, base - 54), (ancho - 15, base - 62), (cx + 14, base - 62), (cx + 14, base - 54)], teja)

    for x in range(10, cx - 14, 4):
        l.rect(x, base - 61, x, base - 55, sombra(teja, 0.8))

    for x in range(cx + 14, ancho - 12, 4):
        l.rect(x, base - 61, x, base - 55, sombra(teja, 0.8))

    # --- edificio de dos plantas con galerias ---
    volumen(l, 6, base - 54, ancho - 7, base, blanco, 1, 3)

    cornisa(l, 6, ancho - 7, base - 56, rgb("#e0dacb"))

    # galeria de abajo: arcos grandes
    n = 9

    paso = (ancho - 20) / n

    for i in range(n):

        ax = int(10 + i * paso)

        ventana_arco(l, ax + 1, base, ax + int(paso) - 3, 22, rgb("#3a4a58"), rgb("#d6d0c0"))

        # puerta o reja en algunos arcos
        l.rect(ax + 3, base - 12, ax + int(paso) - 5, base - 12, rgb("#2a323a"))

    # entrepiso
    l.rect(6, base - 28, ancho - 7, base - 27, rgb("#d6d0c0"))

    # galeria de arriba: arcos mas chicos con balcon
    for i in range(n):

        ax = int(10 + i * paso)

        ventana_arco(l, ax + 2, base - 31, ax + int(paso) - 4, 17, rgb("#2f4a60"), rgb("#d6d0c0"))

        # postigos verdes
        l.rect(ax + 1, base - 46, ax + 1, base - 33, verde)
        l.rect(ax + int(paso) - 3, base - 46, ax + int(paso) - 3, base - 33, verde)

    # baranda de hierro del balcon del primer piso
    balcon(l, 6, ancho - 7, base - 30, NEGRO, alto=3)

    # --- torre central ---
    # cuerpo alto
    volumen(l, cx - 11, base - 90, cx + 11, base - 54, blanco, 1, 3)

    # ventanas de la torre
    ventana_arco(l, cx - 5, base - 62, cx + 5, 13, rgb("#2f4a60"), rgb("#d6d0c0"))

    l.rect(cx - 12, base - 92, cx + 12, base - 90, rgb("#d6d0c0"))

    # segundo cuerpo con el reloj
    volumen(l, cx - 9, base - 108, cx + 9, base - 92, blanco, 1, 2)

    l.circulo(cx, base - 100, 6, rgb("#f4f1e8"))
    l.circulo(cx, base - 100, 5, rgb("#ffffff"))

    for k in range(12):

        ang = k * math.pi / 6

        l.px(int(cx + 4.5 * math.sin(ang)), int(base - 100 - 4.5 * math.cos(ang)), NEGRO)

    l.linea(cx, base - 100, cx, base - 104, NEGRO)
    l.linea(cx, base - 100, cx + 3, base - 99, NEGRO)

    l.rect(cx - 10, base - 110, cx + 10, base - 108, rgb("#d6d0c0"))

    # campanario con arcos
    volumen(l, cx - 7, base - 120, cx + 7, base - 110, blanco, 1, 2)

    l.arco(cx - 5, base - 111, cx - 2, 8, rgb("#3a4a58"))
    l.arco(cx + 2, base - 111, cx + 5, 8, rgb("#3a4a58"))

    # cupulita y veleta
    cupula(l, cx, base - 120, 8, 8, rgb("#6d7686"), costillas=2)

    l.rect(cx, base - 134, cx, base - 128, rgb("#3a3a3a"))
    l.rect(cx - 2, base - 132, cx + 2, base - 132, rgb("#3a3a3a"))

    # faroles de los costados
    for x in (12, ancho - 14):

        farola(l, x, base, 14, c=NEGRO)

    return l


# ==========================================================
# CATEDRAL METROPOLITANA
# ==========================================================

def catedral():

    ancho = 188
    alto = 128

    l = Lienzo(ancho, alto)

    base = alto - 1

    piedra = rgb("#d6cbb2")
    gris = rgb("#8a8c92")

    cx = ancho // 2

    # --- cupula grande al fondo ---
    l.rect(cx - 20, base - 104, cx + 20, base - 78, piedra)
    l.rect(cx - 20, base - 104, cx - 20, base - 78, luz(piedra, 0.2))
    l.rect(cx + 15, base - 104, cx + 20, base - 78, sombra(piedra, 0.84))

    for dx in (-12, -4, 4, 12):

        l.arco(cx + dx - 2, base - 82, cx + dx + 2, 12, rgb("#3a4a58"))

    cupula(l, cx, base - 104, 22, 22, rgb("#7d8a8c"), costillas=8, linterna=True, remate=ORO)

    # --- cuerpo de la iglesia detras del portico ---
    volumen(l, 8, base - 72, ancho - 9, base, piedra, 1, 3)

    # techo de pizarra lateral
    l.rect(8, base - 76, ancho - 9, base - 73, gris)
    l.rect(8, base - 76, ancho - 9, base - 76, luz(gris, 0.25))

    # ventanas del cuerpo (arriba, a los costados del frontis)
    for x in (11, 17, ancho - 22, ancho - 16):

        ventana_arco(l, x, base - 40, x + 4, 22, rgb("#2f4a60"), luz(piedra, 0.2))

    # --- portico de 12 columnas ---
    y_arq = base - 58

    # arquitrabe + friso
    l.rect(22, y_arq, ancho - 23, y_arq + 4, luz(piedra, 0.25))
    l.rect(22, y_arq + 4, ancho - 23, y_arq + 4, sombra(piedra, 0.8))

    for x in range(26, ancho - 24, 4):
        l.rect(x, y_arq + 1, x, y_arq + 3, sombra(piedra, 0.9))

    # frontis triangular
    fronton(l, 20, ancho - 21, y_arq - 1, 17, piedra, interior=sombra(piedra, 0.9))

    # relieve en el timpano (figuras claras)
    for dx in range(-24, 25, 6):

        alt = 5 - abs(dx) // 6

        l.rect(cx + dx, y_arq - 4 - max(0, alt), cx + dx + 1, y_arq - 4, luz(piedra, 0.35))

    # columnas
    columnas(l, 27, ancho - 28, y_arq + 5, base - 4, 12, 4, piedra)

    # puertas entre columnas
    for dx in (-24, 0, 24):

        l.arco(cx + dx - 4, base - 4, cx + dx + 4, 24, rgb("#3a2f28"))

    # escalinata
    for i in range(4):
        l.rect(18 - i * 2, base - 3 + i, ancho - 19 + i * 2, base - 3 + i,
               rgb("#e0d8c8") if i % 2 == 0 else rgb("#c4bba8"))

    # banderas
    bandera(l, 12, base - 76, 14, ancho=9, alto=5)
    bandera(l, ancho - 14, base - 76, 14, ancho=9, alto=5)

    return l


# ==========================================================
# PIRAMIDE DE MAYO
# ==========================================================

def piramide_de_mayo():

    ancho = 60
    alto = 124

    l = Lienzo(ancho, alto)

    base = alto - 1

    blanco = rgb("#f0ecdf")

    cx = ancho // 2

    # escalones del zocalo
    for i in range(4):
        l.rect(cx - 24 + i * 2, base - i * 3 - 2, cx + 24 - i * 2, base - i * 3,
               blanco if i % 2 == 0 else sombra(blanco, 0.9))
        l.rect(cx - 24 + i * 2, base - i * 3 - 2, cx - 24 + i * 2, base - i * 3, luz(blanco, 0.2))

    # pedestal
    volumen(l, cx - 14, base - 28, cx + 14, base - 12, blanco, 1, 3)

    cornisa(l, cx - 14, cx + 14, base - 30, blanco)

    # relieve en el pedestal
    for k in range(-10, 11, 4):
        l.rect(cx + k, base - 24, cx + k + 1, base - 17, sombra(blanco, 0.82))

    # columna / piramide: afinandose hacia arriba
    top = base - 94

    for y in range(top, base - 30):

        t = (y - top) / (base - 30 - top)

        hw = 1.5 + 5.5 * t

        xa = int(round(cx - hw))
        xb = int(round(cx + hw))

        l.rect(xa, y, xb, y, blanco)
        l.px(xa, y, luz(blanco, 0.2))
        l.rect(xb - 1, y, xb, y, sombra(blanco, 0.82))

        if (y - top) % 12 == 6:
            l.rect(xa, y, xb, y, sombra(blanco, 0.9))

    # capitel
    l.rect(cx - 4, top - 2, cx + 4, top, luz(blanco, 0.15))

    # estatua de la Libertad arriba
    figura(l, cx, top - 2, 22, rgb("#f4efe3"), pose="brazo_der", falda=True)

    # cuatro estatuas alegoricas en las esquinas del pedestal
    for dx in (-18, 18):

        figura(l, cx + dx, base - 11, 14, rgb("#f4efe3"), pose="brazo_der" if dx > 0 else "brazo_izq", falda=True)

    # rejas bajas alrededor
    for x in list(range(2, 12, 3)) + list(range(ancho - 12, ancho - 2, 3)):
        l.rect(x, base - 6, x, base, rgb("#2a323a"))

    l.rect(2, base - 6, 11, base - 6, rgb("#2a323a"))
    l.rect(ancho - 12, base - 6, ancho - 3, base - 6, rgb("#2a323a"))

    return l


MONUMENTOS = [
    dict(id="casa_rosada", nombre="Casa Rosada", fn=casa_rosada),
    dict(id="cabildo", nombre="Cabildo de Buenos Aires", fn=cabildo),
    dict(id="catedral_metropolitana", nombre="Catedral Metropolitana", fn=catedral),
    dict(id="piramide_de_mayo", nombre="Piramide de Mayo", fn=piramide_de_mayo),
]

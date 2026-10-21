"""
NIVEL 5 - RETIRO

    * Torre Monumental (ex Torre de los Ingleses, torre de ladrillo con reloj)
    * Edificio Kavanagh (rascacielos art deco escalonado de 1936)
    * Estacion Retiro del Ferrocarril Mitre (hall de hierro y vidrio)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# TORRE MONUMENTAL
# ==========================================================

def torre_monumental():

    ancho = 64
    alto = 170

    l = Lienzo(ancho, alto)

    base = alto - 1

    ladrillo = rgb("#a9472f")
    piedra = rgb("#e0d8c4")

    cx = ancho // 2

    # zocalo de piedra con escalones
    for i in range(3):
        l.rect(cx - 22 + i * 2, base - i * 2 - 1, cx + 22 - i * 2, base - i * 2,
               rgb("#d8d0be") if i % 2 == 0 else rgb("#bdb5a3"))

    volumen(l, cx - 15, base - 30, cx + 15, base - 6, piedra, 1, 3)

    # arco de entrada
    l.arco(cx - 4, base - 6, cx + 4, 18, rgb("#3a2f28"))

    # cuerpo de ladrillo
    ladrillos(l, cx - 14, base - 100, cx + 14, base - 30, ladrillo)

    l.rect(cx - 14, base - 100, cx - 14, base - 30, luz(ladrillo, 0.2))
    l.rect(cx + 11, base - 100, cx + 14, base - 30, sombra(ladrillo, 0.78))

    # esquinas de piedra
    for dx in (-15, 13):
        for y in range(base - 98, base - 30, 6):
            l.rect(cx + dx, y, cx + dx + 2, y + 2, piedra)

    # bandas de piedra
    for y in (base - 56, base - 80):
        l.rect(cx - 15, y, cx + 15, y + 1, piedra)

    # ventanitas
    for y in (base - 46, base - 70, base - 90):

        ventana_arco(l, cx - 2, y, cx + 2, 9, rgb("#2a3550"), piedra)

    # cornisa y cuerpo del reloj
    l.rect(cx - 17, base - 104, cx + 17, base - 100, piedra)
    l.rect(cx - 17, base - 104, cx + 17, base - 104, luz(piedra, 0.3))

    volumen(l, cx - 14, base - 128, cx + 14, base - 104, piedra, 1, 3)

    # esfera del reloj
    l.circulo(cx, base - 116, 10, rgb("#3a3f4a"))
    l.circulo(cx, base - 116, 9, rgb("#fbf8ee"))

    for k in range(12):

        ang = k * math.pi / 6

        l.px(int(round(cx + 7.5 * math.sin(ang))), int(round(base - 116 - 7.5 * math.cos(ang))), NEGRO)

    l.linea(cx, base - 116, cx, base - 122, NEGRO)
    l.linea(cx, base - 116, cx + 5, base - 114, NEGRO)

    # torrecitas en las esquinas del campanario
    for dx in (-17, 17):

        l.rect(cx + dx - 1, base - 140, cx + dx + 1, base - 126, piedra)
        l.rect(cx + dx, base - 144, cx + dx, base - 140, rgb("#4a4f58"))

    # campanario
    volumen(l, cx - 12, base - 142, cx + 12, base - 128, piedra, 1, 3)

    for dx in (-8, -2, 4):
        l.arco(cx + dx, base - 130, cx + dx + 3, 10, rgb("#2a3550"))

    l.rect(cx - 14, base - 144, cx + 14, base - 142, luz(piedra, 0.2))

    # techo piramidal y aguja
    aguja(l, cx, base - 144, 30, 22, rgb("#4d5a66"))

    l.rect(cx, base - 172 + 6, cx, base - 160, rgb("#3a3f4a"))

    l.px(cx, base - 167, ORO)

    return l


# ==========================================================
# EDIFICIO KAVANAGH
# ==========================================================

def kavanagh():

    ancho = 86
    alto = 190

    l = Lienzo(ancho, alto)

    base = alto - 1

    blanco = rgb("#ece8de")

    cx = ancho // 2

    def cuerpo(x0, x1, y0, y1, ventanas_fila=True):

        volumen(l, x0, y0, x1, y1, blanco, 1, 3)

        # remate: balcon corrido con maceteros
        l.rect(x0 - 1, y0, x1 + 1, y0 + 1, luz(blanco, 0.4))
        l.rect(x0 - 1, y0 + 2, x1 + 1, y0 + 2, sombra(blanco, 0.7))

        if ventanas_fila:

            for y in range(y0 + 6, y1 - 3, 7):

                for x in range(x0 + 4, x1 - 5, 5):

                    l.rect(x, y, x + 2, y + 3, VIDRIO)
                    l.px(x, y, VIDRIO_LUZ)

                # linea de balcon
                l.rect(x0, y + 5, x1, y + 5, sombra(blanco, 0.9))

        # plantas en la terraza (el Kavanagh tiene terrazas con arboles)
        for x in range(x0 + 2, x1 - 2, 7):

            l.rect(x, y0 - 2, x + 2, y0 - 1, rgb("#3f8f3a"))
            l.px(x + 1, y0 - 3, rgb("#4faf48"))

    # cuerpos escalonados de abajo hacia arriba
    cuerpo(cx - 40, cx + 40, base - 74, base - 12)
    cuerpo(cx - 33, cx + 33, base - 116, base - 74)
    cuerpo(cx - 25, cx + 25, base - 148, base - 116)
    cuerpo(cx - 17, cx + 17, base - 168, base - 148)

    # torre de remate
    volumen(l, cx - 8, base - 182, cx + 8, base - 168, blanco, 1, 2)

    l.rect(cx - 2, base - 178, cx + 1, base - 171, VIDRIO)

    l.rect(cx, base - 190, cx, base - 183, rgb("#4a4a4a"))

    bandera(l, cx, base - 183, 7, ancho=7, alto=4)

    # planta baja: arcadas con comercios
    l.rect(cx - 40, base - 12, cx + 40, base - 11, sombra(blanco, 0.7))

    volumen(l, cx - 40, base - 11, cx + 40, base, rgb("#cfc7b6"), 1, 3, techo=False)

    for x in range(cx - 36, cx + 34, 9):

        l.arco(x, base, x + 5, 9, rgb("#2f3a4a"))

        l.rect(x + 1, base - 5, x + 4, base - 3, rgb("#e7c22b"))

    return l


# ==========================================================
# ESTACION RETIRO (MITRE)
# ==========================================================

def estacion_retiro():

    ancho = 232
    alto = 112

    l = Lienzo(ancho, alto)

    base = alto - 1

    piedra = rgb("#cdbf9f")
    hierro = rgb("#4f6a60")

    cx = ancho // 2

    # nave de hierro y vidrio detras (arcos grandes)
    for x0, x1 in ((6, 78), (ancho - 79, ancho - 7)):

        mx = (x0 + x1) // 2

        l.semi(mx, base - 42, (x1 - x0) // 2, 38, hierro)
        l.semi(mx, base - 42, (x1 - x0) // 2 - 3, 35, rgb("#9cc2cf"))

        # costillas de hierro
        for k in range(-30, 31, 8):

            l.linea(mx + k, base - 42, mx + k // 2, base - 42 - int(30 * math.sqrt(max(0, 1 - (k / 35) ** 2))), hierro)

    # cuerpo principal de la estacion
    volumen(l, 14, base - 54, ancho - 15, base, piedra, 1, 3)

    cornisa(l, 14, ancho - 15, base - 56, luz(piedra, 0.2), alto=2)

    # techo de pizarra con buhardillas
    l.poly([(10, base - 56), (22, base - 70), (ancho - 23, base - 70), (ancho - 11, base - 56)], rgb("#5a6270"))

    for x in range(28, ancho - 30, 18):

        l.rect(x, base - 66, x + 6, base - 59, rgb("#efe7d4"))
        l.rect(x + 1, base - 65, x + 5, base - 60, VIDRIO)

    # arcos de entrada
    for x in range(26, ancho - 30, 12):

        ventana_arco(l, x, base, x + 7, 26, rgb("#2f3a4a"), luz(piedra, 0.3))

        ventana_arco(l, x, base - 33, x + 7, 16, VIDRIO, luz(piedra, 0.3))

    # torre del reloj central
    volumen(l, cx - 14, base - 98, cx + 14, base - 54, piedra, 1, 3)

    cornisa(l, cx - 14, cx + 14, base - 100, luz(piedra, 0.25), alto=2, vuelo=2)

    # reloj
    l.circulo(cx, base - 82, 9, rgb("#2c3340"))
    l.circulo(cx, base - 82, 8, rgb("#fbf8ee"))

    for k in range(12):

        ang = k * math.pi / 6

        l.px(int(round(cx + 6.5 * math.sin(ang))), int(round(base - 82 - 6.5 * math.cos(ang))), NEGRO)

    l.linea(cx, base - 82, cx + 1, base - 88, NEGRO)
    l.linea(cx, base - 82, cx + 5, base - 80, NEGRO)

    # entrada principal de la torre
    ventana_arco(l, cx - 6, base, cx + 6, 22, rgb("#2f3a4a"), luz(piedra, 0.3))

    # coronamiento: mansarda con cupula
    l.poly([(cx - 16, base - 100), (cx - 9, base - 114), (cx + 9, base - 114), (cx + 16, base - 100)], rgb("#5a6270"))

    cupula(l, cx, base - 114, 8, 7, rgb("#4f6a60"), costillas=2)

    l.rect(cx, base - 130, cx, base - 120, rgb("#3a3a3a"))

    bandera(l, cx, base - 130, 10, ancho=9, alto=5)

    # reloj de anden y farolas
    for x in (20, ancho - 22):

        farola(l, x, base, 18, c=rgb("#1f2a2a"))

    return l


MONUMENTOS = [
    dict(id="torre_monumental", nombre="Torre Monumental", fn=torre_monumental),
    # El Kavanagh real es altisimo: para que entre en la pantalla se le sacan
    # tres pisos (filas repetidas) sin cambiar su forma.
    dict(id="edificio_kavanagh", nombre="Edificio Kavanagh", fn=kavanagh,
         quitar_filas=[(121, 127), (79, 92), (47, 53)]),
    dict(id="estacion_retiro", nombre="Estacion Retiro (Mitre)", fn=estacion_retiro),
]

"""
NIVEL 11 - CONGRESO

    * Palacio del Congreso de la Nacion (gran cupula verde)
    * Confiteria El Molino (art nouveau, con molino en la torre)
    * Monumento a los Dos Congresos (granito blanco y carreta con bueyes)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# PALACIO DEL CONGRESO
# ==========================================================

def palacio_congreso():

    ancho = 264
    alto = 140

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    granito = rgb("#cfcfc9")
    verde = rgb("#4e9a86")

    # --- gran cupula con tambor de columnas ---
    # tambor
    l.rect(cx - 26, base - 98, cx + 26, base - 60, granito)
    l.rect(cx - 26, base - 98, cx - 26, base - 60, luz(granito, 0.25))
    l.rect(cx + 20, base - 98, cx + 26, base - 60, sombra(granito, 0.84))

    columnas(l, cx - 21, cx + 21, base - 94, base - 62, 8, 3, luz(granito, 0.2))

    for dx in range(-17, 18, 6):
        l.rect(cx + dx, base - 86, cx + dx + 2, base - 70, rgb("#2f4a60"))

    l.rect(cx - 28, base - 100, cx + 28, base - 97, luz(granito, 0.3))

    cupula(l, cx, base - 100, 28, 34, verde, costillas=10, linterna=True,
           c_luz=rgb("#8fd0b8"), c_sombra=rgb("#2f6a5c"))

    # estatua del remate
    figura(l, cx, base - 144 + 10, 12, rgb("#8a6a3a"), pose="brazo_der", falda=True)

    # --- alas laterales ---
    volumen(l, 4, base - 52, ancho - 5, base, granito, 1, 3)

    cornisa(l, 4, ancho - 5, base - 54, luz(granito, 0.3))

    for x in range(6, ancho - 6, 3):
        l.rect(x, base - 59, x, base - 55, luz(granito, 0.25))

    l.rect(4, base - 60, ancho - 5, base - 60, luz(granito, 0.25))

    for x in range(12, ancho - 12, 9):

        if abs(x - cx) < 56:
            continue

        ventana_arco(l, x, base - 6, x + 4, 14, VIDRIO, luz(granito, 0.3))
        ventana_arco(l, x, base - 30, x + 4, 15, VIDRIO, luz(granito, 0.3))

    # --- pabellones con frontis en los extremos ---
    for (x0, x1) in ((4, 44), (ancho - 45, ancho - 5)):

        volumen(l, x0, base - 64, x1, base, granito, 1, 3)

        fronton(l, x0 - 1, x1 + 1, base - 65, 11, granito, interior=sombra(granito, 0.92))

        columnas(l, x0 + 5, x1 - 5, base - 62, base - 4, 4, 4, luz(granito, 0.2))

    # --- cuerpo central con portico ---
    volumen(l, cx - 50, base - 66, cx + 50, base, rgb("#c4c4be"), 1, 3, techo=False)

    l.rect(cx - 54, base - 76, cx + 54, base - 66, luz(granito, 0.2))
    l.rect(cx - 54, base - 76, cx + 54, base - 76, rgb("#f4f4ee"))
    l.rect(cx - 54, base - 66, cx + 54, base - 66, sombra(granito, 0.75))

    for x in range(cx - 52, cx + 53, 5):
        l.rect(x, base - 73, x, base - 68, sombra(granito, 0.88))

    fronton(l, cx - 40, cx + 40, base - 77, 14, granito, interior=rgb("#b8b8b2"))

    # escultura en el timpano
    for dx in range(-26, 27, 5):

        alt = 5 - abs(dx) // 6

        l.rect(cx + dx, base - 82 - max(0, alt), cx + dx + 1, base - 82, luz(granito, 0.4))

    columnas(l, cx - 44, cx + 44, base - 65, base - 4, 10, 5, luz(granito, 0.22))

    # puertas
    for dx in (-24, 0, 24):

        l.rect(cx + dx - 7, base - 32, cx + dx + 7, base - 4, rgb("#2c3340"))
        l.rect(cx + dx - 6, base - 31, cx + dx + 6, base - 5, rgb("#3a4660"))
        l.rect(cx + dx, base - 31, cx + dx, base - 5, rgb("#2c3340"))

    # escalinata monumental
    for i in range(6):
        l.rect(cx - 56 - i * 2, base - 5 + i, cx + 56 + i * 2, base - 5 + i,
               rgb("#e8e2d2") if i % 2 == 0 else rgb("#c8c0ad"))

    # banderas
    bandera(l, cx - 49, base - 66, 14, ancho=10, alto=6)
    bandera(l, cx + 49, base - 66, 14, ancho=10, alto=6)

    return l


# ==========================================================
# CONFITERIA EL MOLINO
# ==========================================================

def el_molino():

    ancho = 92
    alto = 130

    l = Lienzo(ancho, alto)

    base = alto - 1

    piedra = rgb("#cbb99a")
    marron = rgb("#6a4a30")
    cobre = rgb("#5e8f78")

    cx = 46

    # cuerpo principal de cuatro pisos
    volumen(l, 8, base - 78, ancho - 9, base, piedra, 1, 3)

    # franjas decorativas art nouveau
    for y in (base - 58, base - 36):
        l.rect(8, y, ancho - 9, y + 1, luz(piedra, 0.3))

    # ventanas con marcos curvos
    for y, h in ((base - 72, 14), (base - 52, 14), (base - 30, 14)):

        for x in (16, 34, 52, 68):

            ventana_arco(l, x, y + h, x + 6, h, VIDRIO, luz(piedra, 0.4))

            balcon(l, x - 2, x + 8, y + h - 2, rgb("#2a323a"), alto=2)

    # planta baja: vidrieras de la confiteria
    l.rect(8, base - 20, ancho - 9, base, rgb("#3a2518"))

    for x in range(12, ancho - 14, 14):

        l.rect(x, base - 17, x + 10, base - 2, rgb("#e7c22b"))
        l.rect(x + 1, base - 16, x + 9, base - 3, rgb("#f4e7a3"))

        # tortas en la vidriera
        l.rect(x + 2, base - 8, x + 4, base - 5, rgb("#c0392b"))
        l.rect(x + 6, base - 8, x + 8, base - 5, rgb("#8a5a2a"))

    # cartel
    texto = "EL MOLINO"

    w = ancho_texto(texto)

    l.rect(cx - w // 2 - 3, base - 28, cx + w // 2 + 2, base - 20, rgb("#7a1f2a"))

    l.texto(cx - w // 2, base - 27, texto, rgb("#f4e7a3"))

    # cornisa
    l.rect(6, base - 82, ancho - 7, base - 78, luz(piedra, 0.2))
    l.rect(6, base - 82, ancho - 7, base - 82, luz(piedra, 0.45))

    # mansarda
    l.poly([(8, base - 82), (16, base - 94), (ancho - 17, base - 94), (ancho - 9, base - 82)], cobre)

    for x in range(20, ancho - 20, 12):

        l.rect(x, base - 90, x + 5, base - 84, piedra)
        l.rect(x + 1, base - 89, x + 4, base - 85, VIDRIO)

    # torre de esquina con el molino
    tx0, tx1 = 34, 58

    volumen(l, tx0, base - 108, tx1, base - 94, piedra, 1, 3)

    ventana_arco(l, 42, base - 96, 50, 11, VIDRIO, luz(piedra, 0.4))

    l.rect(tx0 - 2, base - 110, tx1 + 2, base - 108, luz(piedra, 0.25))

    # techo conico de cobre
    aguja(l, cx, base - 110, 28, 14, cobre)

    # aspas del molino (cruz de madera con celosia)
    mx, my = cx, base - 118

    l.circulo(mx, my, 2, marron)

    for ang in (45, 135, 225, 315):

        rad = math.radians(ang)

        for k in range(2, 14):

            x = int(round(mx + math.cos(rad) * k))
            y = int(round(my - math.sin(rad) * k))

            l.px(x, y, marron)

            if k > 4 and k % 2 == 0:

                nx = -math.sin(rad)
                ny = -math.cos(rad)

                for s in (-2, -1, 1, 2):

                    l.px(int(round(x + nx * s)), int(round(y + ny * s)), rgb("#d6c9a8"))

    l.rect(mx, my - 18, mx, my - 14, rgb("#3a3a3a"))

    return l


# ==========================================================
# MONUMENTO A LOS DOS CONGRESOS
# ==========================================================

def dos_congresos():

    ancho = 132
    alto = 118

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = 66

    blanco = rgb("#ebe7dc")
    bronce = rgb("#5f7a62")

    # estanque con fuente
    l.rect(2, base - 7, ancho - 3, base, blanco)
    l.rect(2, base - 7, ancho - 3, base - 7, rgb("#ffffff"))
    l.rect(5, base - 5, ancho - 6, base - 2, rgb("#58a8d8"))

    for x in range(8, ancho - 8, 8):
        l.rect(x, base - 4, x + 3, base - 4, luz(rgb("#58a8d8"), 0.4))

    # zocalo escalonado en forma de proa de barco (triangulo a la derecha)
    for i in range(4):

        l.rect(cx - 36 + i * 3, base - 8 - i * 4, cx + 36 - i * 3, base - 8 - i * 4 - 3, blanco if i % 2 == 0 else luz(blanco, 0.1))
        l.rect(cx - 36 + i * 3, base - 8 - i * 4 - 3, cx + 36 - i * 3, base - 8 - i * 4 - 3, sombra(blanco, 0.8))

    l.poly([(cx + 30, base - 10), (cx + 52, base - 10), (cx + 30, base - 28)], blanco)
    l.linea(cx + 30, base - 28, cx + 52, base - 10, sombra(blanco, 0.82))

    # columna / pilon central
    volumen(l, cx - 10, base - 80, cx + 10, base - 24, blanco, 1, 3)

    cornisa(l, cx - 10, cx + 10, base - 82, blanco)

    for y in range(base - 76, base - 26, 8):
        l.rect(cx - 9, y, cx + 8, y, sombra(blanco, 0.9))

    # relieve de bronce en el pilon
    l.rect(cx - 6, base - 62, cx + 5, base - 40, bronce)
    l.rect(cx - 6, base - 62, cx - 6, base - 40, luz(bronce, 0.3))

    for k in range(4):
        figura(l, cx - 4 + k * 3, base - 41, 15, luz(bronce, 0.25), pose="pie", falda=False)

    # la Republica arriba
    figura(l, cx, base - 84, 30, bronce, pose="brazo_der", falda=True)

    # antorcha
    l.rect(cx + 8, base - 126 + 16, cx + 8, base - 118 + 16, ORO)

    # carreta con bueyes (a la izquierda del zocalo)
    carreta = rgb("#6a4a30")

    gx = cx - 54

    # carro
    l.rect(gx, base - 20, gx + 16, base - 14, carreta)
    l.rect(gx, base - 20, gx + 16, base - 20, luz(carreta, 0.3))

    # toldo
    l.semi(gx + 8, base - 20, 9, 8, rgb("#bfae86"))

    # ruedas
    for dx in (3, 14):
        l.circulo(gx + dx, base - 12, 4, rgb("#3a2a1f"))
        l.circulo(gx + dx, base - 12, 2, carreta)

    # bueyes
    for k in range(2):

        bx = gx + 22 + k * 11

        l.rect(bx, base - 16, bx + 9, base - 10, rgb("#7a5a38"))
        l.rect(bx + 8, base - 20, bx + 12, base - 14, rgb("#7a5a38"))
        l.px(bx + 12, base - 21, rgb("#f4f1e8"))
        l.rect(bx + 1, base - 10, bx + 2, base - 8, rgb("#4a3a28"))
        l.rect(bx + 7, base - 10, bx + 8, base - 8, rgb("#4a3a28"))

    # chorros de la fuente
    for dx in (-28, 28):

        for k in range(7):
            l.px(cx + dx, base - 14 - k, luz(rgb("#58a8d8"), 0.5))

    return l


MONUMENTOS = [
    dict(id="palacio_congreso", nombre="Palacio del Congreso de la Nacion", fn=palacio_congreso),
    dict(id="confiteria_el_molino", nombre="Confiteria El Molino", fn=el_molino),
    dict(id="monumento_dos_congresos", nombre="Monumento a los Dos Congresos", fn=dos_congresos),
]

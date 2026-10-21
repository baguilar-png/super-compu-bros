"""
NIVEL 10 - ONCE

    * Palacio de Aguas Corrientes (fachada de terracota esmaltada)
    * Estacion Once de Septiembre (terminal del Ferrocarril Sarmiento)
    * Mausoleo de Rivadavia (Plaza Miserere, obra de Rogelio Yrurtia)
"""

from pixelart import *  # noqa: F401,F403


# ==========================================================
# PALACIO DE AGUAS CORRIENTES
# ==========================================================

def aguas_corrientes():

    ancho = 168
    alto = 118

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    crema = rgb("#e6cba2")
    rojo = rgb("#b4432f")
    verde_t = rgb("#3f8f6a")
    pizarra = rgb("#3f7f5f")

    def banda_de_azulejos(x0, x1, y):
        """Franja de terracota policroma (rojo, verde, crema)."""

        l.rect(x0, y, x1, y + 3, rojo)

        for x in range(x0, x1 + 1, 4):

            l.rect(x, y + 1, x + 1, y + 2, [verde_t, crema, rgb("#e7c22b")][(x // 4) % 3])

    # cuerpo largo
    volumen(l, 6, base - 56, ancho - 7, base, crema, 1, 3)

    banda_de_azulejos(6, ancho - 7, base - 58)

    banda_de_azulejos(6, ancho - 7, base - 28)

    # escudos del friso (hay noventa)
    for x in range(8, ancho - 8, 5):
        l.rect(x, base - 63, x + 2, base - 60, [rojo, verde_t][(x // 5) % 2])
        l.px(x + 1, base - 62, rgb("#f4f1e8"))

    # zocalo de piedra
    l.rect(6, base - 8, ancho - 7, base, rgb("#a8a090"))
    l.rect(6, base - 8, ancho - 7, base - 8, rgb("#cbc3b0"))

    # ventanas con marcos de colores
    for x in range(14, ancho - 14, 10):

        ventana_arco(l, x, base - 10, x + 5, 15, VIDRIO, rojo)

        ventana_arco(l, x, base - 36, x + 5, 15, VIDRIO, verde_t)

    # pabellones de los extremos, con mansarda de pizarra verde
    for (x0, x1) in ((4, 34), (ancho - 35, ancho - 5)):

        volumen(l, x0, base - 74, x1, base - 46, crema, 1, 3)

        banda_de_azulejos(x0, x1, base - 76)

        l.poly([(x0 - 2, base - 77), (x0 + 5, base - 94), (x1 - 5, base - 94), (x1 + 2, base - 77)], pizarra)
        l.rect(x0 + 5, base - 94, x1 - 5, base - 94, luz(pizarra, 0.3))

        l.rect((x0 + x1) // 2 - 1, base - 108, (x0 + x1) // 2 - 1, base - 94, rgb("#3a3a3a"))

        # ventana en el pabellon
        ventana_arco(l, (x0 + x1) // 2 - 3, base - 50, (x0 + x1) // 2 + 3, 16, VIDRIO, rojo)

        l.rect(x0 + 4, base - 66, x0 + 7, base - 60, rojo)
        l.rect(x1 - 7, base - 66, x1 - 4, base - 60, rojo)

    # cuerpo central con frontis
    volumen(l, cx - 26, base - 78, cx + 26, base - 20, crema, 1, 3)

    banda_de_azulejos(cx - 26, cx + 26, base - 80)

    # frontis triangular decorado
    l.poly([(cx - 28, base - 82), (cx, base - 106), (cx + 28, base - 82)], crema)
    l.poly([(cx - 22, base - 84), (cx, base - 102), (cx + 22, base - 84)], rojo)
    l.poly([(cx - 17, base - 85), (cx, base - 98), (cx + 17, base - 85)], verde_t)
    l.poly([(cx - 11, base - 86), (cx, base - 94), (cx + 11, base - 86)], crema)

    l.circulo(cx, base - 89, 3, rojo)
    l.circulo(cx, base - 89, 1, rgb("#e7c22b"))

    # ventanal y portal central
    ventana_arco(l, cx - 8, base - 44, cx + 8, 26, VIDRIO, rojo)

    for x in range(cx - 7, cx + 8, 3):
        l.rect(x, base - 66, x, base - 45, VIDRIO_OSC)

    l.arco(cx - 7, base - 4, cx + 7, 22, rgb("#3a2518"))
    l.arco(cx - 5, base - 5, cx + 5, 18, rgb("#5a3a22"))

    # escalinata
    for i in range(3):
        l.rect(cx - 12 - i * 2, base - 3 + i, cx + 12 + i * 2, base - 3 + i,
               rgb("#e0d8c8") if i % 2 == 0 else rgb("#c4bba8"))

    # reja del frente
    for x in range(6, ancho - 6, 4):

        if abs(x - cx) > 16:
            l.rect(x, base - 5, x, base, NEGRO)

    return l


# ==========================================================
# ESTACION ONCE
# ==========================================================

def estacion_once():

    ancho = 220
    alto = 108

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    gris = rgb("#d4cdbd")
    zinc = rgb("#6a7280")

    # naves de la estacion al fondo (arcos de hierro)
    for x0, x1 in ((6, 70), (ancho - 71, ancho - 7)):

        mx = (x0 + x1) // 2

        l.semi(mx, base - 44, (x1 - x0) // 2, 34, rgb("#556a74"))
        l.semi(mx, base - 44, (x1 - x0) // 2 - 3, 31, rgb("#a8c8d4"))

        for k in range(-26, 27, 9):
            l.rect(mx + k, base - 44 - int(30 * math.sqrt(max(0, 1 - (k / 32) ** 2))), mx + k, base - 44, rgb("#556a74"))

    # cuerpo principal
    volumen(l, 14, base - 56, ancho - 15, base, gris, 1, 3)

    cornisa(l, 14, ancho - 15, base - 58, luz(gris, 0.3))

    # techo de zinc
    l.rect(14, base - 66, ancho - 15, base - 59, zinc)
    l.rect(14, base - 66, ancho - 15, base - 66, luz(zinc, 0.3))

    # arcadas
    for x in range(22, ancho - 26, 11):

        ventana_arco(l, x, base, x + 6, 26, rgb("#2f3a4a"), luz(gris, 0.3))

        ventana_arco(l, x, base - 33, x + 6, 16, VIDRIO, luz(gris, 0.3))

    # cuerpo central con gran ventanal y frontis
    volumen(l, cx - 28, base - 76, cx + 28, base, rgb("#cdc5b2"), 1, 3)

    l.poly([(cx - 30, base - 76), (cx, base - 92), (cx + 30, base - 76)], gris)
    l.poly([(cx - 24, base - 77), (cx, base - 89), (cx + 24, base - 77)], sombra(gris, 0.9))

    cornisa(l, cx - 29, cx + 29, base - 78, luz(gris, 0.3))

    # reloj
    l.circulo(cx, base - 84, 5, rgb("#2c3340"))
    l.circulo(cx, base - 84, 4, rgb("#fbf8ee"))

    l.linea(cx, base - 84, cx, base - 87, NEGRO)
    l.linea(cx, base - 84, cx + 2, base - 83, NEGRO)

    # gran ventanal central
    ventana_arco(l, cx - 17, base - 12, cx + 17, 46, VIDRIO, luz(gris, 0.3))

    for x in range(cx - 16, cx + 17, 4):
        l.rect(x, base - 56, x, base - 13, VIDRIO_OSC)

    for y in range(base - 22, base - 56, -8):
        l.rect(cx - 16, y, cx + 16, y, VIDRIO_OSC)

    # cartel ONCE (arriba del ventanal)
    texto = "ONCE"

    w = ancho_texto(texto)

    l.rect(cx - w // 2 - 3, base - 72, cx + w // 2 + 2, base - 62, rgb("#1f2b4a"))
    l.marco(cx - w // 2 - 3, base - 72, cx + w // 2 + 2, base - 62, rgb("#d8d0b8"))

    l.texto(cx - w // 2, base - 70, texto, rgb("#ffd84a"))

    # puertas
    for dx in (-24, 24):

        l.rect(cx + dx - 5, base - 14, cx + dx + 5, base, rgb("#2c3340"))
        l.rect(cx + dx, base - 14, cx + dx, base, rgb("#3a4660"))

    # farolas
    for x in (8, ancho - 10):
        farola(l, x, base, 20, c=rgb("#1f2a2a"))

    # tren azul detras (Sarmiento)
    return l


# ==========================================================
# MAUSOLEO DE RIVADAVIA
# ==========================================================

def mausoleo_rivadavia():

    ancho = 120
    alto = 100

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    granito = rgb("#a79c9a")

    # escalinata ancha
    for i in range(5):

        l.rect(cx - 50 + i * 3, base - i * 2 - 1, cx + 50 - i * 3, base - i * 2,
               luz(granito, 0.18) if i % 2 == 0 else granito)

    # zocalo macizo
    volumen(l, cx - 34, base - 34, cx + 34, base - 10, granito, 1, 4)

    l.rect(cx - 36, base - 37, cx + 36, base - 34, luz(granito, 0.25))
    l.rect(cx - 36, base - 34, cx + 36, base - 34, sombra(granito, 0.75))

    # relieves: paneles con figuras
    for dx in (-24, -10, 4, 18):

        l.rect(cx + dx, base - 30, cx + dx + 8, base - 14, sombra(granito, 0.84))

        figura(l, cx + dx + 4, base - 14, 13, luz(granito, 0.3), pose="brazo_der", falda=True)

    # bloque central (sarcofago)
    volumen(l, cx - 22, base - 52, cx + 22, base - 37, granito, 1, 3)

    l.rect(cx - 24, base - 55, cx + 24, base - 52, luz(granito, 0.3))

    # inscripcion
    for x in range(cx - 14, cx + 15, 3):
        l.rect(x, base - 46, x + 1, base - 44, sombra(granito, 0.7))

    # gran figura femenina (La Patria) velando
    figura(l, cx, base - 55, 34, rgb("#bdb3b0"), pose="brazos_arriba", falda=True)

    # laureles a los costados
    for dx in (-30, 30):

        figura(l, cx + dx, base - 37, 20, rgb("#bdb3b0"),
               pose="brazo_der" if dx > 0 else "brazo_izq", falda=True)

    # arboles de la plaza
    arbol(l, 9, base - 2, 44, "jacaranda", seed=2)
    arbol(l, ancho - 10, base - 2, 44, "platano", seed=5)

    return l


MONUMENTOS = [
    dict(id="aguas_corrientes", nombre="Palacio de Aguas Corrientes", fn=aguas_corrientes),
    dict(id="estacion_once", nombre="Estacion Once de Septiembre", fn=estacion_once),
    dict(id="mausoleo_rivadavia", nombre="Mausoleo de Rivadavia (Plaza Miserere)", fn=mausoleo_rivadavia),
]

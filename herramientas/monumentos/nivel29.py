"""
NIVEL 29 - ADROGUE

    * Casa de Borges: la casona familiar frente a la Plaza Brown, con su
      patio y una palmera
    * La Cucaracha: la residencia de veraneo de estilo pintoresco, con
      torreon y entramado de madera
    * Plaza Brown: el monumento al Almirante Brown entre los eucaliptos
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import casa_colonial, monumento_plaza


def casa_de_borges():

    return casa_colonial(
        ancho=128, muro="#f4f0e0", teja="#b5532f", detalle="#3a5a8a",
        patio=True, palmera=True, texto=None
    )


def la_cucaracha():

    ancho = 128
    alto = 108

    l = Lienzo(ancho, alto)

    base = alto - 1

    blanco = rgb("#f4ecd6")
    madera = rgb("#5a3a22")
    teja = rgb("#a9472f")

    # cuerpo: planta baja de mamposteria
    volumen(l, 10, base - 32, ancho - 12, base, rgb("#e4cfa0"), 1, 3)

    for x in range(18, ancho - 24, 16):

        ventana_arco(l, x, base - 4, x + 7, 18, VIDRIO, blanco)

    # planta alta con entramado de madera
    volumen(l, 14, base - 62, ancho - 16, base - 32, blanco, 1, 3)

    for x in range(14, ancho - 16, 14):

        l.rect(x, base - 62, x + 1, base - 32, madera)

    l.rect(14, base - 62, ancho - 16, base - 61, madera)
    l.rect(14, base - 46, ancho - 16, base - 45, madera)

    l.linea(14, base - 62, 28, base - 46, madera)
    l.linea(ancho - 16, base - 62, ancho - 30, base - 46, madera)

    for x in (24, 52, 80):

        l.rect(x, base - 58, x + 6, base - 50, VIDRIO)
        l.rect(x, base - 58, x + 6, base - 58, VIDRIO_LUZ)

    # techo a dos aguas empinado
    l.poly([(8, base - 61), (30, base - 82), (ancho - 36, base - 82), (ancho - 10, base - 61)], teja)

    for y in range(base - 80, base - 62, 3):

        l.rect(30 - (base - 80 - y) * 1, y, ancho - 36 + (base - 80 - y), y, sombra(teja, 0.84))

    # torreon con techo conico
    tx = ancho - 22

    volumen(l, tx - 11, base - 86, tx + 11, base - 32, blanco, 1, 3)

    l.rect(tx - 5, base - 76, tx + 5, base - 64, VIDRIO)
    l.rect(tx, base - 76, tx, base - 64, madera)

    aguja(l, tx, base - 85, 30, 24, teja)

    l.rect(tx, base - 117 + 8, tx, base - 106 + 8, rgb("#2c3a3a"))

    # galeria de madera
    l.rect(8, base - 33, 70, base - 31, madera)

    for x in range(10, 70, 6):

        l.rect(x, base - 31, x, base - 2, madera)

    arbol(l, 106, base - 1, 56, "ficus", seed=9)

    return l


def plaza_brown():

    return monumento_plaza(ancho=108, alto=120, piedra="#d0c8b4", figura_c="#6a7a84")


MONUMENTOS = [
    dict(id="casa_de_borges", nombre="Casa de Borges (Adrogue)", fn=casa_de_borges),
    dict(id="la_cucaracha", nombre="La Cucaracha (Adrogue)", fn=la_cucaracha),
    dict(id="plaza_brown", nombre="Plaza Brown (Almirante Brown)", fn=plaza_brown),
]

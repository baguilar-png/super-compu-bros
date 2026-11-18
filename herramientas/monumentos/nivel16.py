"""
NIVEL 16 - MORON (primer nivel del mapa del conurbano)

    * Catedral de Nuestra Senora del Buen Viaje (Inmaculada Concepcion):
      dos torres con agujas y una cupula detras
    * Palacio Municipal de Moron (1939, de Alejandro Bustillo): bloque
      racionalista de piedra con una torre central con reloj
    * Museo Nacional de Aeronautica: un hangar y un avion a reaccion
      sobre su pedestal
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import (
    cartel_nombre, iglesia, palacio_municipal, pasto
)


def catedral_moron():

    return iglesia(
        ancho=112, muro="#e9dcc0", techo="#6f86a0", detalle="#b8a880",
        torres=2, alto_torre=96, remate="aguja", cupula_central=True
    )


def palacio_moron():

    return palacio_municipal(
        ancho=172, muro="#ddd3bc", techo="#6a7a8a", detalle="#b8ae96",
        torre=True, alto_torre=52, estilo="racionalista", texto="MORON"
    )


def avion_a_reaccion(l, cx, cy, escala=1.0, color="#c9ced4"):
    """Un avion de caza visto de costado, apuntando a la derecha."""

    c = rgb(color)

    s = escala

    def p(x, y):

        return (cx + x * s, cy + y * s)

    # fuselaje
    l.poly([p(-30, -1), p(-22, -5), p(18, -5), p(34, 0), p(18, 4), p(-22, 4)], c)

    # cabina
    l.poly([p(2, -5), p(8, -9), p(15, -5)], rgb("#3b5a86"))

    # cola
    l.poly([p(-30, -1), p(-34, -16), p(-26, -16), p(-18, -5)], sombra(c, 0.85))

    # alas
    l.poly([p(-6, 3), p(-20, 14), p(-12, 14), p(8, 3)], sombra(c, 0.78))

    # toma de aire y escarapela
    l.rect(int(cx + 12 * s), int(cy - 3 * s), int(cx + 16 * s), int(cy + 1 * s), rgb("#4a5058"))

    l.circulo(int(cx - 8 * s), int(cy - 1 * s), max(1, int(2 * s)), CELESTE_ARG)


def museo_aeronautica():

    ancho = 176
    alto = 122

    l = Lienzo(ancho, alto)

    base = alto - 1

    gris = rgb("#aab4be")
    blanco = rgb("#f0f2f4")

    # hangar de techo curvo
    l.semi(70, base - 34, 62, 30, gris)

    l.rect(8, base - 34, 132, base, blanco)

    l.rect(8, base - 34, 8, base, luz(blanco, 0.1))
    l.rect(130, base - 34, 132, base, sombra(blanco, 0.85))

    # nervaduras del techo
    for x in range(14, 130, 12):

        l.rect(x, base - 62, x, base - 34, sombra(gris, 0.82))

    # porton grande con franjas celestes
    l.rect(32, base - 28, 108, base - 1, rgb("#3a4a5a"))

    for i, x in enumerate(range(33, 108, 15)):

        l.rect(x, base - 27, x + 13, base - 2, CELESTE_ARG if i % 2 == 0 else rgb("#e8f0f6"))

    cartel_nombre(l, 70, base - 46, "AERONAUTICA", rgb("#1f4a8f"))

    # el avion en su pedestal, adelante a la derecha
    l.rect(150, base - 40, 152, base, rgb("#8a8f98"))
    l.rect(142, base - 3, 160, base, rgb("#cfc9bb"))

    avion_a_reaccion(l, 150, base - 52, 1.15)

    pasto(l, 0, ancho - 1, base)

    return l


MONUMENTOS = [
    dict(id="catedral_moron", nombre="Catedral de Moron (Buen Viaje)", fn=catedral_moron),
    dict(id="palacio_moron", nombre="Palacio Municipal de Moron", fn=palacio_moron),
    dict(id="museo_aeronautica", nombre="Museo Nacional de Aeronautica", fn=museo_aeronautica),
]

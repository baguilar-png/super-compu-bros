"""
NIVEL 21 - LANUS (de noche)

    * Estadio Ciudad de Lanus - Nestor Diaz Perez, "La Fortaleza" del
      Granate
    * Estacion Lanus (Ferrocarril Roca)
    * Palacio Municipal de Lanus, con su torre
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import estacion, estadio, palacio_municipal


def fortaleza_lanus():

    return estadio(
        ancho=190, color="#7a1f3a", color2="#f4f1e8", texto="LANUS",
        torres=4, forma="frente", color_techo="#8d939c"
    )


def estacion_lanus():

    return estacion(
        ancho=156, muro="#d9b27a", techo="#8a4a35", marco="#f4ecd6",
        texto="LANUS", torre=True, alto_torre=28
    )


def palacio_lanus():

    return palacio_municipal(
        ancho=164, muro="#e8dcc0", techo="#5f7a6a", detalle="#bfae86",
        torre=True, alto_torre=44, estilo="clasico", texto="LANUS"
    )


MONUMENTOS = [
    dict(id="fortaleza_lanus", nombre="Estadio Ciudad de Lanus (La Fortaleza)", fn=fortaleza_lanus),
    dict(id="estacion_lanus", nombre="Estacion Lanus", fn=estacion_lanus),
    dict(id="palacio_lanus", nombre="Palacio Municipal de Lanus", fn=palacio_lanus),
]

"""
NIVEL 20 - AVELLANEDA

    * Estadio Libertadores de America ("La Doble Visera"), de Independiente
    * El Cilindro de Avellaneda (Estadio Presidente Peron), de Racing
    * Puente Nicolas Avellaneda sobre el Riachuelo (1940), el que une
      La Boca con Avellaneda
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import estadio
from monumentos.nivel15 import puente_avellaneda  # noqa: F401


def doble_visera():

    return estadio(
        ancho=200, color="#c8322d", color2="#f4f1e8", texto="INDEPENDIENTE",
        torres=4, forma="visera"
    )


def cilindro_de_avellaneda():

    return estadio(
        ancho=190, color="#7cc0ec", color2="#f4f1e8", texto="RACING",
        torres=2, forma="cilindro"
    )


MONUMENTOS = [
    dict(id="doble_visera", nombre="Estadio Libertadores de America (Doble Visera)", fn=doble_visera),
    dict(id="cilindro_avellaneda", nombre="El Cilindro de Avellaneda", fn=cilindro_de_avellaneda),
    dict(id="puente_avellaneda", nombre="Puente Nicolas Avellaneda", fn=puente_avellaneda),
]

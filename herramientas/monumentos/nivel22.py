"""
NIVEL 22 - WILDE (Avellaneda)

    * Estacion Wilde (Ferrocarril Roca)
    * Parroquia de Wilde: iglesia de una sola torre con cupula
    * Plaza Wilde, con su glorieta de hierro
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import estacion, iglesia, monumento_plaza


def estacion_wilde():

    return estacion(
        ancho=158, muro="#e0c890", techo="#6a4a3a", marco="#f4ecd6",
        texto="WILDE", torre=False
    )


def parroquia_wilde():

    return iglesia(
        ancho=100, muro="#eadfc4", techo="#4f8f7a", detalle="#b8a880",
        torres=1, alto_torre=90, remate="cupula"
    )


def plaza_wilde():

    return monumento_plaza(ancho=104, alto=96, glorieta=True)


MONUMENTOS = [
    dict(id="estacion_wilde", nombre="Estacion Wilde", fn=estacion_wilde),
    dict(id="parroquia_wilde", nombre="Parroquia de Wilde", fn=parroquia_wilde),
    dict(id="plaza_wilde", nombre="Plaza Wilde (glorieta)", fn=plaza_wilde),
]

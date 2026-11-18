"""
NIVEL 27 - SAN FRANCISCO SOLANO (de noche)

    * Parroquia San Francisco Solano: iglesia con un campanario plano
    * Estacion Solano (Ferrocarril Roca)
    * Plaza de Solano: monumento con una bandera en lo alto
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import estacion, iglesia, monumento_plaza


def parroquia_solano():

    return iglesia(
        ancho=100, muro="#ecd8b0", techo="#8a6a4a", detalle="#b89c70",
        torres=1, alto_torre=84, remate="plano"
    )


def estacion_solano():

    return estacion(
        ancho=150, muro="#d6a070", techo="#6a4a40", marco="#f0e6cc",
        texto="SOLANO", torre=False
    )


def plaza_solano():

    return monumento_plaza(ancho=104, alto=122, piedra="#cfc8b8", bandera_arriba=True)


MONUMENTOS = [
    dict(id="parroquia_solano", nombre="Parroquia San Francisco Solano", fn=parroquia_solano),
    dict(id="estacion_solano", nombre="Estacion Solano", fn=estacion_solano),
    dict(id="plaza_solano", nombre="Plaza de Solano", fn=plaza_solano),
]

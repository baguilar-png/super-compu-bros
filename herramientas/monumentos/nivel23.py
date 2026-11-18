"""
NIVEL 23 - BERNAL (de noche)

    * Parroquia Maria Auxiliadora: iglesia salesiana con cupula y una
      torre alta
    * Estacion Bernal (Ferrocarril Roca)
    * Universidad Nacional de Quilmes: el campus de Bernal
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import edificio_moderno, estacion, iglesia


def maria_auxiliadora():

    return iglesia(
        ancho=112, muro="#efe2c4", techo="#6a8a9a", detalle="#c0a878",
        torres=1, alto_torre=100, remate="aguja", cupula_central=True
    )


def estacion_bernal():

    return estacion(
        ancho=160, muro="#c98a5a", techo="#4f5f70", marco="#f4ecd6",
        texto="BERNAL", torre=True, alto_torre=26
    )


def universidad_quilmes():

    return edificio_moderno(
        ancho=176, alto=108, muro="#d8d2c4", vidrio_c="#4a7a9a",
        texto="UNQ", franja="#c8322d", cuerpos=3, escalonado=True
    )


MONUMENTOS = [
    dict(id="maria_auxiliadora", nombre="Parroquia Maria Auxiliadora (Bernal)", fn=maria_auxiliadora),
    dict(id="estacion_bernal", nombre="Estacion Bernal", fn=estacion_bernal),
    dict(id="universidad_quilmes", nombre="Universidad Nacional de Quilmes", fn=universidad_quilmes),
]

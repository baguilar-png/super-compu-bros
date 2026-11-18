"""
NIVEL 28 - CLAYPOLE

    * Estacion Claypole (Ferrocarril Roca)
    * Parroquia de Claypole: dos torres chicas con cupulas
    * Tanque de agua del ferrocarril: torre de ladrillo con tanque
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import estacion, iglesia, torre_agua


def estacion_claypole():

    return estacion(
        ancho=154, muro="#bf6a4a", techo="#5a6a5a", marco="#f0e6cc",
        texto="CLAYPOLE", torre=True, alto_torre=30
    )


def parroquia_claypole():

    return iglesia(
        ancho=96, muro="#f0e4c8", techo="#a9472f", detalle="#c0a878",
        torres=2, alto_torre=70, remate="cupula"
    )


def tanque_de_agua():

    return torre_agua(ancho=78, alto=128)


MONUMENTOS = [
    dict(id="estacion_claypole", nombre="Estacion Claypole", fn=estacion_claypole),
    dict(id="parroquia_claypole", nombre="Parroquia de Claypole", fn=parroquia_claypole),
    dict(id="tanque_de_agua", nombre="Tanque de agua del ferrocarril", fn=tanque_de_agua),
]

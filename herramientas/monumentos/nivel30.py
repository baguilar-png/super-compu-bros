"""
NIVEL 30 - BURZACO (JEFE FINAL, de noche)

    En la arena del jefe final se ven de fondo:

    * El Primer Monumento a la Bandera, en la plaza de Burzaco
    * La Estacion Burzaco (Ferrocarril Roca)
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import estacion, monumento_plaza


def monumento_a_la_bandera():

    return monumento_plaza(ancho=108, alto=128, piedra="#d8d0bc", bandera_arriba=True)


def estacion_burzaco():

    return estacion(
        ancho=170, muro="#cf9a66", techo="#4f5f70", marco="#f4ecd6",
        texto="BURZACO", torre=True, alto_torre=34
    )


MONUMENTOS = [
    dict(id="monumento_bandera_burzaco", nombre="Primer Monumento a la Bandera (Burzaco)", fn=monumento_a_la_bandera),
    dict(id="estacion_burzaco", nombre="Estacion Burzaco", fn=estacion_burzaco),
]

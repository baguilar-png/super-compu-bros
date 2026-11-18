"""
NIVEL 17 - RAMOS MEJIA

    * Estacion Ramos Mejia (1906, estilo victoriano, hoy museo): ladrillo
      con molduras claras, techo de chapa y torre con reloj
    * Casa de la Cultura y Teatro Leopoldo Marechal: fachada clasica con
      columnas
    * Plaza Bartolome Mitre, el corazon del barrio: monumento y arboles
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import estacion, monumento_plaza, palacio_municipal


def estacion_ramos_mejia():

    return estacion(
        ancho=164, muro="#b8694a", techo="#4f5f70", marco="#f0e6cc",
        texto="RAMOS MEJIA", torre=True, alto_torre=34
    )


def casa_de_la_cultura():

    return palacio_municipal(
        ancho=150, muro="#e4d6b4", techo="#6a7a8a", detalle="#b8a070",
        torre=False, estilo="clasico", texto="TEATRO"
    )


def plaza_mitre():

    return monumento_plaza(ancho=104, alto=122, piedra="#d8d0bc", figura_c="#5f7a66")


MONUMENTOS = [
    dict(id="estacion_ramos_mejia", nombre="Estacion Ramos Mejia", fn=estacion_ramos_mejia),
    dict(id="casa_de_la_cultura", nombre="Casa de la Cultura (Teatro Marechal)", fn=casa_de_la_cultura),
    dict(id="plaza_mitre", nombre="Plaza Bartolome Mitre", fn=plaza_mitre),
]

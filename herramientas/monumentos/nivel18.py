"""
NIVEL 18 - LINIERS (de noche)

    * Estacion Liniers (1872, linea Sarmiento): la terminal del oeste
    * Estadio Jose Amalfitani, el Fortin de Velez Sarsfield
    * Santuario de San Cayetano (1900): el santo del pan y del trabajo
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import estacion, estadio, iglesia


def estacion_liniers():

    return estacion(
        ancho=176, muro="#dcc690", techo="#4f6a5a", marco="#f4ecd6",
        texto="LINIERS", torre=False
    )


def estadio_amalfitani():

    return estadio(
        ancho=196, color="#2a54b0", color2="#f4f1e8", texto="VELEZ",
        torres=4, forma="frente"
    )


def san_cayetano():

    return iglesia(
        ancho=108, muro="#e6d8b8", techo="#7a6a58", detalle="#b09c74",
        torres=2, alto_torre=88, remate="plano"
    )


MONUMENTOS = [
    dict(id="estacion_liniers", nombre="Estacion Liniers", fn=estacion_liniers),
    dict(id="estadio_amalfitani", nombre="Estadio Jose Amalfitani (Velez)", fn=estadio_amalfitani),
    dict(id="san_cayetano", nombre="Santuario de San Cayetano", fn=san_cayetano),
]

"""
NIVEL 24 - QUILMES

    * Catedral de Quilmes (Inmaculada Concepcion): dos torres con agujas
    * Cerveceria Quilmes: ladrillo, chimeneas y tanque
    * Casa de Santa Coloma: la casona colonial mas antigua de la ciudad
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import casa_colonial, fabrica, iglesia


def catedral_quilmes():

    return iglesia(
        ancho=116, muro="#d2cab4", techo="#4a5a6a", detalle="#a89c80",
        torres=2, alto_torre=96, remate="aguja", cupula_central=False
    )


def cerveceria_quilmes():

    return fabrica(
        ancho=170, muro="#9a4a30", texto="QUILMES", chimeneas=2,
        alto_chimenea=100, techo_diente=True, tanque=True
    )


def casa_santa_coloma():

    return casa_colonial(
        ancho=132, muro="#f2ead4", teja="#a9472f", detalle="#8a6a3a",
        patio=True, palmera=True, texto=None
    )


MONUMENTOS = [
    dict(id="catedral_quilmes", nombre="Catedral de Quilmes", fn=catedral_quilmes),
    dict(id="cerveceria_quilmes", nombre="Cerveceria Quilmes", fn=cerveceria_quilmes),
    dict(id="casa_santa_coloma", nombre="Casa de Santa Coloma", fn=casa_santa_coloma),
]

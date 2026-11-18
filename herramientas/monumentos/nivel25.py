"""
NIVEL 25 - BERAZATEGUI (de noche)

    * Cristalerias Rigolleau: la vidrieria de ladrillo con su chimenea
    * Museo del Vidrio: un edificio de vidrio y hormigon
    * Estacion Berazategui (Ferrocarril Roca)
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import edificio_moderno, estacion, fabrica


def rigolleau():

    return fabrica(
        ancho=164, muro="#b5603f", texto="RIGOLLEAU", chimeneas=1,
        alto_chimenea=104, techo_diente=False, tanque=True, vidrio=VIDRIO_LUZ
    )


def museo_del_vidrio():

    return edificio_moderno(
        ancho=150, alto=96, muro="#cfd8d8", vidrio_c="#5fb0c8",
        texto="VIDRIO", franja="#2a8aa8", cuerpos=2, escalonado=False,
        cartel_fondo="#1f5a6a"
    )


def estacion_berazategui():

    return estacion(
        ancho=158, muro="#d8c07a", techo="#7a4a3a", marco="#f4ecd6",
        texto="BERAZATEGUI", torre=False
    )


MONUMENTOS = [
    dict(id="rigolleau", nombre="Cristalerias Rigolleau", fn=rigolleau),
    dict(id="museo_del_vidrio", nombre="Museo del Vidrio", fn=museo_del_vidrio),
    dict(id="estacion_berazategui", nombre="Estacion Berazategui", fn=estacion_berazategui),
]

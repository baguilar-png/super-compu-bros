"""
NIVEL 26 - FLORENCIO VARELA

    * Hospital de Alta Complejidad El Cruce: cuerpos de vidrio con la
      cruz roja
    * Universidad Nacional Arturo Jauretche (UNAJ)
    * Estacion Florencio Varela (cabecera del ramal del Roca)
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import edificio_moderno, estacion


def hospital_el_cruce():

    l = edificio_moderno(
        ancho=184, alto=112, muro="#e6e6e2", vidrio_c="#6aa0c8",
        texto="EL CRUCE", franja="#c8322d", cuerpos=3, escalonado=True,
        cartel_fondo="#8a1f2a"
    )

    # la cruz roja en lo alto
    cx = 92

    l.rect(cx - 6, 2, cx + 6, 14, BLANCO)
    l.rect(cx - 2, 3, cx + 2, 13, ROJO)
    l.rect(cx - 5, 6, cx + 5, 10, ROJO)

    return l


def unaj():

    return edificio_moderno(
        ancho=168, alto=100, muro="#bfb4a0", vidrio_c="#7a98b0",
        texto="UNAJ", franja="#e0a020", cuerpos=2, escalonado=True,
        cartel_fondo="#2a4a2a"
    )


def estacion_florencio_varela():

    return estacion(
        ancho=164, muro="#c7b078", techo="#4f6a7a", marco="#f4ecd6",
        texto="F VARELA", torre=True, alto_torre=26
    )


MONUMENTOS = [
    dict(id="hospital_el_cruce", nombre="Hospital El Cruce", fn=hospital_el_cruce),
    dict(id="unaj", nombre="Universidad Nacional Arturo Jauretche", fn=unaj),
    dict(id="estacion_florencio_varela", nombre="Estacion Florencio Varela", fn=estacion_florencio_varela),
]

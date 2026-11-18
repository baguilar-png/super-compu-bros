"""
Monumentos de Buenos Aires dibujados en pixel art.

Cada modulo nivelNN.py define los monumentos de un barrio (un nivel del
juego) y una lista MONUMENTOS = [dict(id=..., nombre=..., fn=...)].

Ningun monumento aparece en mas de un nivel.
"""

import importlib

# (numero de nivel, nombre del modulo)
MODULOS = [
    (1, "nivel01"),
    (2, "nivel02"),
    (3, "nivel03"),
    (4, "nivel04"),
    (5, "nivel05"),
    (6, "nivel06"),
    (7, "nivel07"),
    (8, "nivel08"),
    (9, "nivel09"),
    (10, "nivel10"),
    (11, "nivel11"),
    (12, "nivel12"),
    (13, "nivel13"),
    (14, "nivel14"),
    (15, "nivel15"),
    (16, "nivel16"),
    (17, "nivel17"),
    (18, "nivel18"),
    (19, "nivel19"),
    (20, "nivel20"),
    (21, "nivel21"),
    (22, "nivel22"),
    (23, "nivel23"),
    (24, "nivel24"),
    (25, "nivel25"),
    (26, "nivel26"),
    (27, "nivel27"),
    (28, "nivel28"),
    (29, "nivel29"),
    (30, "nivel30"),
]


def cargar(niveles=None):
    """
    Devuelve {nivel: [monumento, ...]} con los modulos que existan.
    """

    resultado = {}

    for nivel, nombre in MODULOS:

        if niveles is not None and nivel not in niveles:
            continue

        try:
            modulo = importlib.import_module("monumentos." + nombre)
        except ModuleNotFoundError as e:
            if e.name != "monumentos." + nombre:
                raise
            continue

        resultado[nivel] = list(modulo.MONUMENTOS)

    return resultado


def quitar_filas(lienzo, rangos):
    """
    Saca filas del dibujo (rangos inclusivos de y). Sirve para acortar un
    edificio quitandole pisos repetidos, sin deformarlo.
    """

    from pixelart import Lienzo

    quitar = set()

    for a, b in rangos:
        quitar.update(range(a, b + 1))

    filas = [y for y in range(lienzo.h) if y not in quitar]

    nuevo = Lienzo(lienzo.w, len(filas))

    for i, y in enumerate(filas):
        nuevo.im.paste(lienzo.im.crop((0, y, lienzo.w, y + 1)), (0, i))

    return nuevo


def construir(monumento):
    """Dibuja un monumento: contorno + recorte (la base queda abajo)."""

    lienzo = monumento["fn"]()

    if monumento.get("quitar_filas"):
        lienzo = quitar_filas(lienzo, monumento["quitar_filas"])

    # 1 pixel de aire para que entre el contorno
    from pixelart import Lienzo

    con_borde = Lienzo(lienzo.w + 4, lienzo.h + 4)
    con_borde.pegar(lienzo, 2, 2)

    con_borde.contorno()

    return con_borde.recortar()

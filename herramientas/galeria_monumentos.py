"""
Hoja con todos los monumentos del juego, nivel por nivel (para ver a ojo
que no se repite ninguno).

Uso:  python herramientas/galeria_monumentos.py [ruta_de_salida.png]
"""

import os
import sys

HERRAMIENTAS = os.path.dirname(os.path.abspath(__file__))

if HERRAMIENTAS not in sys.path:
    sys.path.insert(0, HERRAMIENTAS)

from pixelart import *  # noqa: E402,F401,F403
import monumentos  # noqa: E402
from niveles_config import NIVELES  # noqa: E402


def limpio(s):

    return "".join(c for c in s.upper() if c.isalnum() or c in " .-/")


def partir(texto, ancho_max):
    """Parte el texto en lineas que entren en ancho_max pixeles."""

    lineas = []

    actual = ""

    for palabra in texto.split():

        prueba = (actual + " " + palabra).strip()

        if ancho_texto(prueba) <= ancho_max or not actual:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra

    if actual:
        lineas.append(actual)

    return lineas


def main(salida):

    todos = monumentos.cargar()

    filas = []

    for n in sorted(todos):

        sprites = [(m["nombre"], monumentos.construir(m)) for m in todos[n]]

        filas.append((n, sprites))

    ancho = max(sum(s.w for _, s in sp) + 14 * (len(sp) + 1) for _, sp in filas)

    ancho = max(ancho, 820)

    alto = sum(max(s.h for _, s in sp) + 62 for _, sp in filas) + 20

    hoja = Lienzo(ancho, alto)

    hoja.rect(0, 0, ancho - 1, alto - 1, rgb("#eee9db"))

    y = 10

    for n, sprites in filas:

        h = max(s.h for _, s in sprites)

        titulo = "{}  {}".format(n, NIVELES[n]["barrio"])

        hoja.texto(14, y, titulo, rgb("#1f3a7a"), 2)

        base = y + 22 + h

        # piso
        hoja.rect(0, base + 1, ancho - 1, base + 1, rgb("#bdb6a0"))

        x = 14

        for nombre, s in sprites:

            hoja.pegar(s, x, base - s.h + 1)

            etiqueta = limpio(nombre)

            if "(" in nombre:
                etiqueta = limpio(nombre.split("(")[0].strip())

            for k, linea in enumerate(partir(etiqueta, s.w + 8)[:3]):
                hoja.texto(x, base + 6 + k * 9, linea, rgb("#555048"))

            x += s.w + 14

        y = base + 44

    img = hoja.im.convert("RGB").resize((ancho * 2, alto * 2), Image.NEAREST)

    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)

    img.save(salida)

    print("Listo:", salida, img.size)


if __name__ == "__main__":

    destino = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(HERRAMIENTAS), "previsualizacion", "galeria_monumentos.png"
    )

    main(destino)

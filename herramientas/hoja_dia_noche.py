"""
Arma previsualizacion/dia_y_noche.png: los 30 niveles tal como los dibuja el
juego (con el sol, la luna y las luces animadas), marcados DIA o NOCHE.

Uso (desde la carpeta del juego):

    python herramientas/hoja_dia_noche.py

Necesita pygame y Pillow.
"""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

HERRAMIENTAS = os.path.dirname(os.path.abspath(__file__))

JUEGO = os.path.dirname(HERRAMIENTAS)

for ruta in (JUEGO, HERRAMIENTAS):
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

os.chdir(JUEGO)

import pygame  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import fondos_nivel  # noqa: E402
from niveles_config import NIVELES  # noqa: E402
from terreno import Terreno  # noqa: E402

ANCHO_FOTO = 480
ALTO_FOTO = 360


def main():

    pygame.init()

    pantalla = pygame.display.set_mode((800, 600))

    reloj = {"t": 0.0}

    # el tiempo lo manejamos nosotros: los destellos y las luces salen en
    # distinto momento en cada nivel
    pygame.time.get_ticks = lambda: int(reloj["t"] * 1000)

    filas = (len(NIVELES) + 2) // 3

    hoja = Image.new("RGB", (ANCHO_FOTO * 3, ALTO_FOTO * filas), (20, 20, 28))

    dibujo = ImageDraw.Draw(hoja)

    try:

        fuente = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17
        )

    except OSError:

        fuente = ImageFont.load_default()

    for n in sorted(NIVELES):

        terreno = Terreno.cargar(n)

        # (el nivel 1, por dentro, es mas corto que los demas)
        fondo = fondos_nivel.FondoNivel(
            n, 800, 600, 804, terreno.ancho if terreno.interior else 9600,
            (79, 154, 224), (60, 120, 60), terreno
        )

        reloj["t"] = 1.15 + n * 0.37

        pantalla.fill((0, 0, 0))

        # a la altura de los techos (los impares) o de la calle (los pares; el
        # nivel 1, por dentro, solo tiene calle)
        fondo.dibujar(
            pantalla, 2300 + (n % 3) * 900,
            0 if n % 2 and not terreno.interior else 324
        )

        foto = Image.frombytes(
            "RGB", (800, 600), pygame.image.tostring(pantalla, "RGB")
        ).resize((ANCHO_FOTO, ALTO_FOTO), Image.LANCZOS)

        x = ((n - 1) % 3) * ANCHO_FOTO

        y = ((n - 1) // 3) * ALTO_FOTO

        hoja.paste(foto, (x, y))

        if fondo.oscuro:
            momento = "NOCHE"
        elif fondo.interior:
            momento = "POR DENTRO"
        else:
            momento = "DIA"

        etiqueta = "{}  {}  -  {}{}".format(
            n, NIVELES[n]["barrio"], momento,
            "  (JEFE)" if NIVELES[n].get("jefe") else ""
        )

        dibujo.rectangle([x, y, x + ANCHO_FOTO, y + 26], fill=(0, 0, 0))

        dibujo.text(
            (x + 8, y + 3), etiqueta,
            fill=(255, 255, 255) if fondo.oscuro else (255, 232, 140),
            font=fuente
        )

    salida = os.path.join(JUEGO, "previsualizacion", "dia_y_noche.png")

    hoja.save(salida)

    print("Listo:", salida)


if __name__ == "__main__":

    main()

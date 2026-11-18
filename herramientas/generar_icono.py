"""
Icono del juego (acceso directo, ventana y barra de tareas): un medallon
redondo de pixel art, con borde negro y anillo blanco, y adentro la cara de
MXROY (de su dibujo de frente) asomando desde abajo.

    assets/icono.png   (para la ventana)
    icono.ico          (para el acceso directo)

Uso: python herramientas/generar_icono.py
"""

import math
import os

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TAM = 44                 # pixeles del dibujo (despues se agranda)
R_AFUERA = 21.6          # borde negro
R_ANILLO = 18.6          # anillo blanco
R_ADENTRO = 16.4         # adentro (fondo)

NEGRO = (0, 0, 0, 255)
BLANCO = (255, 255, 255, 255)
GRIS = (110, 110, 110, 255)
GRIS_CLARO = (200, 200, 200, 255)
FONDO = (120, 176, 232, 255)


def main():
    img = Image.new("RGBA", (TAM, TAM), (0, 0, 0, 0))
    c = (TAM - 1) / 2

    for y in range(TAM):
        for x in range(TAM):
            d = math.hypot(x - c, y - c)
            if d <= R_ADENTRO:
                img.putpixel((x, y), FONDO)
            elif d <= R_ANILLO:
                # Anillo blanco con algunos grises (como el medallon original)
                a = math.atan2(y - c, x - c)
                gris = (int((a + math.pi) * 6) % 5 == 0)
                img.putpixel((x, y), GRIS_CLARO if gris and d > R_ANILLO - 1 else BLANCO)
            elif d <= R_AFUERA:
                a = math.atan2(y - c, x - c)
                img.putpixel((x, y), GRIS if int((a + math.pi) * 7) % 6 == 0 and d < R_ANILLO + 1.2 else NEGRO)

    # Mxroy: cabeza y hombros, agrandado x2, apoyado abajo y recortado al circulo
    frente = Image.open(os.path.join(RAIZ, "assets", "personajes", "MXROY", "frente.png")).convert("RGBA")
    frente = frente.crop(frente.getbbox())
    medio = frente.crop((0, 0, frente.width, int(frente.height * 0.72)))
    medio = medio.resize((medio.width * 2, medio.height * 2), Image.NEAREST)
    x0 = int(round(c - medio.width / 2)) + 1
    y0 = int(round(c + R_ADENTRO)) - medio.height + 2
    for y in range(medio.height):
        for x in range(medio.width):
            px = medio.getpixel((x, y))
            X, Y = x0 + x, y0 + y
            if px[3] and 0 <= X < TAM and 0 <= Y < TAM and math.hypot(X - c, Y - c) <= R_ADENTRO + 0.4:
                img.putpixel((X, Y), px)

    grande = img.resize((TAM * 6, TAM * 6), Image.NEAREST)
    grande.save(os.path.join(RAIZ, "assets", "icono.png"))
    tamanos = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.resize((264, 264), Image.NEAREST).resize((256, 256), Image.LANCZOS).save(
        os.path.join(RAIZ, "icono.ico"), sizes=tamanos)
    print("icono listo")


if __name__ == "__main__":
    main()

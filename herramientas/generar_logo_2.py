"""
Logo de "SUPER COMPU BROS 2" para el final del juego: el logo de siempre
(assets/fondos/logo.png) con un 2 grande a la derecha, al lado de COMPU y
BROS, azul con la franja amarilla como SUPER y un poco inclinado.

    assets/fondos/logo_2.png

Uso: python herramientas/generar_logo_2.py
"""

import os

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOS = [
    "...######...",
    ".##########.",
    "############",
    "####....####",
    "###.....####",
    "........####",
    ".......####.",
    "......####..",
    ".....####...",
    "....####....",
    "...####.....",
    "..####......",
    ".####.......",
    "####........",
    "############",
    "############",
    "############",
]

AZUL = (52, 60, 168, 255)
AZUL_CLARO = (78, 90, 200, 255)
AMARILLO = (250, 226, 20, 255)
NEGRO = (0, 0, 0, 255)


def dos():
    alto, ancho = len(DOS) * 2, len(DOS[0]) * 2
    img = Image.new("RGBA", (ancho + 2, alto + 2), (0, 0, 0, 0))
    lleno = set()
    for fy, fila in enumerate(DOS):
        for fx, c in enumerate(fila):
            if c == "#":
                for dy in (0, 1):
                    for dx in (0, 1):
                        lleno.add((fx * 2 + dx + 1, fy * 2 + dy + 1))
    for x, y in lleno:
        # Franja amarilla en el medio (como en SUPER), brillo arriba
        if 15 <= y <= 19:
            color = AMARILLO
        elif y <= 4:
            color = AZUL_CLARO
        else:
            color = AZUL
        img.putpixel((x, y), color)
    # Contorno negro
    for x, y in list(lleno):
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            v = (x + dx, y + dy)
            if v not in lleno and 0 <= v[0] < img.width and 0 <= v[1] < img.height:
                img.putpixel(v, NEGRO)
    return img.rotate(-8, resample=Image.NEAREST, expand=True)


def main():
    logo = Image.open(os.path.join(RAIZ, "assets", "fondos", "logo.png")).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    d = dos()
    ancho = logo.width + d.width - 4
    alto = max(logo.height, d.height + 18)
    lienzo = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    lienzo.alpha_composite(logo, (0, 0))
    # Abajo a la derecha, apoyado en la linea de BROS
    lienzo.alpha_composite(d, (logo.width - 4, alto - d.height))
    lienzo.save(os.path.join(RAIZ, "assets", "fondos", "logo_2.png"))
    print("logo_2 listo", lienzo.size)


if __name__ == "__main__":
    main()

"""
Sprites del PRINCESITO MXROY.

El dibujo de partida es el de frente (Mxroy_Default.png, 35x35), que se guarda
en assets/personajes/MXROY/original/frente.png. Igual que con Iki, las poses
de costado salen del molde de BAUTO (assets/personajes/BAUTO/bauto *.png):
cada color de Bauto se cambia por el que tiene Mxroy en ese mismo lugar
(pelo negro, piel, remera azul, pantalon gris y zapatillas blancas).

    frente.png          de frente (el dibujo original, recortado a 30x32)
    cabeza.png          solo la cabeza (para los retratos y el final)
    final.png           quieto de costado (16x27)
    frame_1/2/3.png     caminar
    saltando.png        saltar
    agachado.png        agacharse

Todas las poses de costado miran a la DERECHA (como las de los bros).

Uso: python herramientas/generar_mxroy.py
"""

import os

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAUTO = os.path.join(RAIZ, "assets", "personajes", "BAUTO")
SALIDA = os.path.join(RAIZ, "assets", "personajes", "MXROY")
ORIGINAL = os.path.join(SALIDA, "original", "frente.png")

# Color de Bauto -> color de Mxroy
CAMBIOS = {
    # piel
    (242, 210, 155): (230, 194, 124),
    (245, 199, 135): (214, 182, 118),
    (237, 201, 135): (214, 182, 118),
    (245, 219, 176): (254, 202, 152),
    # pelo
    (148, 116, 59): (36, 33, 36),
    (120, 93, 46): (8, 8, 10),
    # remera (y la banda de Bauto, que Mxroy no tiene)
    (237, 232, 208): (9, 23, 71),
    (219, 216, 197): (7, 17, 56),
    (199, 46, 76): (9, 23, 71),
    (184, 33, 63): (7, 17, 56),
    (173, 0, 35): (5, 12, 42),
    # zapatillas (los detalles verdes de Bauto pasan a gris)
    (40, 87, 24): (179, 179, 179),
    (23, 56, 12): (140, 140, 140),
    (10, 61, 22): (120, 120, 120),
}

POSES = {
    "bauto final.png": "final.png",
    "bauto frame 1.png": "frame_1.png",
    "bauto frame 2.png": "frame_2.png",
    "bauto frame 3.png": "frame_3.png",
    "bauto saltando.png": "saltando.png",
    "bauto agachado.png": "agachado.png",
}


def recolorear(img):
    img = img.convert("RGBA")
    salida = Image.new("RGBA", img.size, (0, 0, 0, 0))
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = img.getpixel((x, y))
            if a:
                r, g, b = CAMBIOS.get((r, g, b), (r, g, b))
            salida.putpixel((x, y), (r, g, b, a))
    return salida


def main():
    os.makedirs(SALIDA, exist_ok=True)

    # De frente: el dibujo original, apoyado abajo y centrado en 30x32 (el
    # mismo tamano que el frente de los bros)
    original = Image.open(ORIGINAL).convert("RGBA")
    figura = original.crop(original.getbbox())
    frente = Image.new("RGBA", (30, 32), (0, 0, 0, 0))
    frente.alpha_composite(figura, ((30 - figura.width) // 2, 32 - figura.height))
    frente.save(os.path.join(SALIDA, "frente.png"))

    # Cabeza: desde arriba hasta la primera fila con remera azul
    azul = {(7, 17, 56), (9, 23, 71)}
    fin = figura.height
    for y in range(figura.height):
        if any(figura.getpixel((x, y))[:3] in azul and figura.getpixel((x, y))[3] for x in range(figura.width)):
            fin = y
            break
    cabeza = figura.crop((0, 0, figura.width, fin))
    cabeza.crop(cabeza.getbbox()).save(os.path.join(SALIDA, "cabeza.png"))

    for molde, nombre in POSES.items():
        recolorear(Image.open(os.path.join(BAUTO, molde))).save(os.path.join(SALIDA, nombre))

    print("Mxroy listo")


if __name__ == "__main__":
    main()

"""
Arma los botones "nueva partida", "cargar partida" y "volver" con el mismo
estilo que los del menu (boton_jugar.png, boton_salir.png...): un panel gris
de 9 pixeles de alto con las letras chiquitas de 5 pixeles.

Uso (desde la carpeta del juego):
    python herramientas/generar_botones_partida.py
"""

import os

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "assets", "fondos")

FONDO = (180, 180, 180, 255)
BORDE = (70, 70, 70, 255)
SOMBRA = (163, 163, 163, 255)

# Letras de 5 de alto (las mismas que los botones que ya habia)
LETRAS = {
    "a": ["####", "...#", "####", "#..#", "####"],
    "c": ["####", "#...", "#...", "#...", "####"],
    "d": ["...#", "####", "#..#", "#..#", "####"],
    "e": ["####", "#..#", "####", "#...", "####"],
    "g": ["####", "#..#", "####", "...#", "####"],
    "i": ["#", ".", "#", "#", "#"],
    "l": ["#..", "#..", "#..", "#..", "###"],
    "n": ["####", "#..#", "#..#", "#..#", "#..#"],
    "o": ["####", "#..#", "#..#", "#..#", "####"],
    "p": ["####", "#..#", "####", "#...", "#..."],
    "r": ["####", "#..#", "#...", "#...", "#..."],
    "t": ["#..", "###", "#..", "#..", "###"],
    "u": ["#..#", "#..#", "#..#", "#..#", "####"],
    "v": ["#..#", "#..#", "#..#", ".##.", ".##."],
    " ": ["..", "..", "..", "..", ".."],
}


def boton(texto, ancho_minimo=54):

    columnas = [""] * 5
    for i, letra in enumerate(texto):
        g = LETRAS[letra]
        for f in range(5):
            columnas[f] += ("." if i else "") + g[f]
    ancho_texto = len(columnas[0])
    ancho = max(ancho_minimo, ancho_texto + 12)

    img = Image.new("RGBA", (ancho, 9), (0, 0, 0, 0))
    for x in range(1, ancho - 1):
        img.putpixel((x, 0), BORDE)
        img.putpixel((x, 8), BORDE)
    for y in range(1, 8):
        img.putpixel((0, y), BORDE)
        img.putpixel((ancho - 1, y), BORDE)
        for x in range(1, ancho - 1):
            img.putpixel((x, y), FONDO)
    # Sombrita abajo y a la derecha, como los otros
    for x in range(ancho // 2, ancho - 1):
        img.putpixel((x, 7), SOMBRA)
    for y in range(1, 8):
        img.putpixel((ancho - 2, y), SOMBRA)
        img.putpixel((ancho - 3, y), SOMBRA)

    x0 = (ancho - ancho_texto) // 2
    for f in range(5):
        for x, c in enumerate(columnas[f]):
            if c == "#":
                img.putpixel((x0 + x, 2 + f), BORDE)
    return img


def main():
    for texto, archivo in (
        ("nueva partida", "boton_nueva_partida.png"),
        ("cargar partida", "boton_cargar_partida.png"),
        ("volver", "boton_volver.png"),
    ):
        boton(texto).save(os.path.join(SALIDA, archivo))
    print("Botones en", SALIDA)


if __name__ == "__main__":
    main()

"""
Pasa una imagen de pixel art agrandada (por ejemplo una captura o una
imagen generada, donde cada "pixel" mide 20 o 25 pixeles reales y los
bordes estan medio borrosos) a pixel art de verdad: 1 pixel por pixel, con
el fondo transparente.

  1. Saca el fondo: lo transparente, o el color liso que toca los bordes
     de la imagen (blanco o negro).
  2. Busca solo el tamano de la grilla (cuanto mide cada pixel) y donde
     empieza, mirando donde cambian los colores.
  3. Toma el color del medio de cada casillero.
  4. Si el fondo era negro (y se comio el contorno), le vuelve a poner un
     contorno negro de 1 pixel.

Se uso para los sprites de LORD TEICHI (assets/personajes/TEICHI/).

Uso, desde la carpeta del juego:

    python herramientas/extraer_pixelart.py entrada.png salida.png
"""

import cmath
import math
import sys
from collections import deque

import numpy as np
from PIL import Image


def _sacar_fondo(img):
    """Pone transparente el fondo liso que toca los bordes de la imagen."""

    a = np.array(img.convert("RGBA")).astype(int)
    alto, ancho = a.shape[:2]

    if (a[:, :, 3] < 128).mean() > 0.2:
        # Ya tiene fondo transparente
        return a, False

    esquina = a[2, 2, :3]
    fondo_negro = esquina.sum() < 100

    def es_fondo(y, x):
        return np.abs(a[y, x, :3] - esquina).sum() < (70 if fondo_negro else 60)

    visto = np.zeros((alto, ancho), dtype=bool)
    cola = deque()
    for x in range(ancho):
        cola.append((0, x))
        cola.append((alto - 1, x))
    for y in range(alto):
        cola.append((y, 0))
        cola.append((y, ancho - 1))

    while cola:
        y, x = cola.popleft()
        if visto[y, x] or not es_fondo(y, x):
            continue
        visto[y, x] = True
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < alto and 0 <= xx < ancho and not visto[yy, xx]:
                cola.append((yy, xx))

    a[visto, 3] = 0
    return a, fondo_negro


def _grilla(a, eje):
    """
    Tamano de pixel y desfasaje en un eje, mirando donde cambia el color
    (series de Fourier: el tamano que mejor alinea todos los cambios).
    """

    if eje == 1:
        b = a
    else:
        b = a.transpose(1, 0, 2)

    alto, ancho = b.shape[:2]
    bordes = []
    for y in range(0, alto, 3):
        fila = b[y]
        dif = np.abs(fila[1:, :3] - fila[:-1, :3]).sum(axis=1) + np.abs(fila[1:, 3] - fila[:-1, 3])
        bordes.extend(np.nonzero(dif > 90)[0] + 1)

    bordes = np.array(bordes, dtype=float)

    mejor = (0, 20.0, 0.0)
    for tam in np.arange(14.0, 40.0, 0.02):
        suma = np.exp(2j * math.pi * bordes / tam).sum()
        fuerza = abs(suma) / len(bordes)
        if fuerza > mejor[0]:
            mejor = (fuerza, tam, (cmath.phase(suma) / (2 * math.pi)) * tam % tam)

    return mejor[1], mejor[2]


def extraer(ruta_entrada):

    a, fondo_negro = _sacar_fondo(Image.open(ruta_entrada))
    alto, ancho = a.shape[:2]

    tam_x, inicio_x = _grilla(a, 1)
    tam_y, inicio_y = _grilla(a, 0)

    columnas = int((ancho - inicio_x) // tam_x)
    filas = int((alto - inicio_y) // tam_y)

    salida = np.zeros((filas, columnas, 4), dtype=np.uint8)

    for j in range(filas):
        for i in range(columnas):
            cx = inicio_x + (i + 0.5) * tam_x
            cy = inicio_y + (j + 0.5) * tam_y
            r = max(2, int(min(tam_x, tam_y) * 0.22))
            x0, x1 = int(cx - r), int(cx + r) + 1
            y0, y1 = int(cy - r), int(cy + r) + 1
            parche = a[max(0, y0):y1, max(0, x0):x1].reshape(-1, 4)
            opacos = parche[parche[:, 3] > 128]
            if len(opacos) * 2 < len(parche):
                continue
            salida[j, i, :3] = np.median(opacos[:, :3], axis=0)
            salida[j, i, 3] = 255

    if fondo_negro:
        salida = _contorno(salida)

    img = Image.fromarray(salida, "RGBA")
    return img.crop(img.getbbox()), (tam_x, tam_y)


def _contorno(a):
    """Contorno negro de 1 pixel alrededor de lo que no es transparente."""

    alto, ancho = a.shape[:2]
    grande = np.zeros((alto + 2, ancho + 2, 4), dtype=np.uint8)
    grande[1:-1, 1:-1] = a
    lleno = grande[:, :, 3] > 0
    salida = grande.copy()
    for y in range(alto + 2):
        for x in range(ancho + 2):
            if lleno[y, x]:
                continue
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < alto + 2 and 0 <= xx < ancho + 2 and lleno[yy, xx]:
                    salida[y, x] = (0, 0, 0, 255)
                    break
    return salida


if __name__ == "__main__":

    imagen, tam = extraer(sys.argv[1])
    imagen.save(sys.argv[2])
    print(sys.argv[2], imagen.size, "pixel de", tam)

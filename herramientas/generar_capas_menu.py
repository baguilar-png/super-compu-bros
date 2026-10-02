"""
Genera, a partir de assets/fondos/fondo_menu.png:
  - fondo_menu_frente.png   (todo menos el cielo, que queda transparente)
  - fondo_menu_carteles.png (solo los pixeles de los carteles de publicidad)
La capa "frente" tiene el cielo transparente. En el juego se dibuja
  fondo -> nubes -> frente -> brillo de carteles
asi las nubes pasan POR DETRAS de edificios y obelisco.

Se corre una sola vez (necesita Pillow, numpy y scipy):
    python herramientas/generar_capas_menu.py
"""
import os
import numpy as np
from PIL import Image
from scipy import ndimage

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, "assets", "fondos")

img = np.array(Image.open(os.path.join(DIR, "fondo_menu.png")).convert("RGB")).astype(int)
alto, ancho, _ = img.shape

# --- color de cielo por fila (columna libre de edificios) -------------
ref = np.zeros((alto, 3), int)
for y in range(alto):
    ref[y] = np.median(img[y, 440:470], axis=0)

# --- candidatos a cielo: cerca del color de referencia de su fila -----
dif = np.abs(img - ref[:, None, :]).sum(axis=2)
r0, g0, b0 = img[..., 0], img[..., 1], img[..., 2]
cand = (dif < 40) | ((b0 >= 235) & (g0 > 150) & (g0 < 215) & (r0 < 100))
cand[640:, :] = False                      # el cielo no baja de aca

# solo el cielo conectado con el borde de arriba
etiquetas, _ = ndimage.label(cand)
cielo = np.isin(etiquetas, np.unique(etiquetas[0, :][etiquetas[0, :] > 0]))
cielo = ndimage.binary_opening(cielo, iterations=1)

# --- obelisco: por fila, el tramo crema mas largo cerca del centro ----
r, g, b = img[..., 0], img[..., 1], img[..., 2]
crema = (r > 190) & (g > 180) & (b > 150) & (r >= b)
obelisco = np.zeros((alto, ancho), bool)
izq = der = None
for y in range(100, 962):
    xs = np.where(crema[y, 520:715])[0]
    if len(xs) < 3:
        continue
    cortes = np.where(np.diff(xs) > 4)[0]
    inicios = np.r_[0, cortes + 1]
    fines = np.r_[cortes, len(xs) - 1]
    k = np.argmax(fines - inicios)
    a_, b_ = xs[inicios[k]] + 520, xs[fines[k]] + 520
    if izq is not None:                        # suavizar saltos
        a_ = int(round(0.5 * a_ + 0.5 * izq)); b_ = int(round(0.5 * b_ + 0.5 * der))
    izq, der = a_, b_
    obelisco[y, max(izq - 2, 0):der + 3] = True

# --- arboles / pasto (verde) para que tapen a los autos ---------------
verde = (g > r + 25) & (g > b + 10)
verde[:, :] &= True
verde[900:, :] = False                     # el pasto de la plazoleta no tapa

# --- alpha final -------------------------------------------------------
alpha = np.zeros((alto, ancho), np.uint8)
parte_alta = ~cielo
parte_alta[640:, :] = False                # abajo de 640 solo obelisco/arboles
alpha[parte_alta] = 255
alpha[obelisco] = 255
alpha[verde & (np.arange(alto)[:, None] < 900)] = 255
alpha[cielo] = 0

rgba = np.dstack([img.astype(np.uint8), alpha])
Image.fromarray(rgba, "RGBA").save(os.path.join(DIR, "fondo_menu_frente.png"), optimize=True)
print("listo:", int(cielo.sum()), "px de cielo,", int(obelisco.sum()), "px de obelisco")


# ======================================================================
# CARTELES: capa con solo los pixeles de los carteles de publicidad
# (fondo_menu_carteles.png). El juego les anima el brillo.
# Cada cartel es un poligono (coordenadas de la imagen original); se le
# saca el cielo y los arboles que lo tapan.
# ======================================================================

from PIL import ImageDraw

CARTELES = {
    "hotel":    [(48, 360), (154, 379), (151, 443), (48, 414)],
    "samsung":  [(1127, 391), (1245, 378), (1245, 473), (1127, 485)],
    "rosa":     [(1057, 492), (1104, 478), (1105, 568), (1057, 582)],
    "pantalla": [(253, 551), (287, 551), (287, 712), (253, 712)],
    "inferior": [(1108, 755), (1237, 758), (1237, 795), (1108, 792)],
}

lienzo = Image.new("L", (ancho, alto), 0)
dib = ImageDraw.Draw(lienzo)
for poligono in CARTELES.values():
    dib.polygon(poligono, fill=255)

capa = np.array(lienzo) > 0
capa &= ~ndimage.binary_dilation(cielo, iterations=2)
capa &= ~((g > r + 25) & (g > b + 10))
capa = ndimage.binary_opening(capa, iterations=1)
print("carteles:", int(capa.sum()), "px")

salida = np.zeros((alto, ancho, 4), np.uint8)
salida[..., :3] = img.astype(np.uint8)
salida[..., 3] = np.where(capa, 255, 0)
Image.fromarray(salida, "RGBA").save(os.path.join(DIR, "fondo_menu_carteles.png"), optimize=True)

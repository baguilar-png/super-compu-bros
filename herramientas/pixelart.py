"""
Herramientas de dibujo pixel art para generar los fondos de los niveles.

Todo se dibuja pixel por pixel con Pillow (sin suavizado). Un "pixel de
dibujo" mide PX x PX pixeles en la pantalla del juego (PX = 3), asi que la
ventana de 800 x 600 equivale a 267 x 200 pixeles de dibujo.

Las coordenadas son INCLUSIVAS: rect(0, 0, 3, 3, c) pinta 4 x 4 pixeles.
"""

import math
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from pixel_font import mapa_de_bits  # noqa: E402  (fuente 5x7 del juego)


# ==========================================================
# MEDIDAS DEL JUEGO
# ==========================================================

PX = 3                      # pixeles de pantalla por pixel de dibujo
ANCHO_VISTA = 800 // PX + 1  # 267
ALTO_NIVEL = 200            # 600 / 3
SUELO = 180                 # fila donde termina el dibujo y empieza el piso


# ==========================================================
# COLOR
# ==========================================================

def rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def tono(c, f):
    """Multiplica el brillo (f < 1 oscurece, f > 1 aclara)."""
    return tuple(max(0, min(255, int(round(v * f)))) for v in c[:3])


def mezcla(a, b, t):
    """t = 0 -> a, t = 1 -> b."""
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def luz(c, t=0.28):
    return mezcla(c, (255, 250, 235), t)


def sombra(c, f=0.76):
    # oscurece un poco hacia el azul, que da sombras mas lindas
    return mezcla(tono(c, f), (40, 40, 90), 0.06)


def pal(c):
    """Cuatro tonos de un mismo color: base, luz, sombra, oscuro."""
    return {
        "b": tuple(c[:3]),
        "l": luz(c),
        "s": sombra(c),
        "o": sombra(c, 0.5),
    }


# Colores que se repiten en muchos dibujos
VIDRIO = rgb("#3b5a86")
VIDRIO_LUZ = rgb("#8fb4d8")
VIDRIO_OSC = rgb("#27405f")
NEGRO = rgb("#1d1a24")
BLANCO = rgb("#f4f1e8")
PIEDRA = rgb("#d9cdb0")
PIEDRA_BLANCA = rgb("#e9e4d6")
GRIS_PIEDRA = rgb("#aaa8a6")
LADRILLO = rgb("#a9472f")
TEJA = rgb("#b5532f")
VERDE_ARBOL = rgb("#3f8f3a")
TRONCO = rgb("#6b4a2f")
AZUL_BOCA = rgb("#0b2f8f")
AMARILLO_BOCA = rgb("#f5c60c")
CELESTE_ARG = rgb("#74acdf")
ROJO = rgb("#c8322d")
ORO = rgb("#e3b92f")
BRONCE = rgb("#8a6a3a")
CUPULA_VERDE = rgb("#4d8f7a")


# ==========================================================
# LIENZO
# ==========================================================

class Lienzo:

    def __init__(self, ancho, alto):

        self.w = ancho
        self.h = alto

        self.im = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))

        self.d = ImageDraw.Draw(self.im)

    # ------------------------------------------------------
    # primitivas
    # ------------------------------------------------------

    def px(self, x, y, c):

        if 0 <= x < self.w and 0 <= y < self.h:

            self.im.putpixel((int(x), int(y)), tuple(c[:3]) + (255,))

    def rect(self, x0, y0, x1, y1, c):

        if x1 < x0 or y1 < y0:
            return

        self.d.rectangle(
            [int(x0), int(y0), int(x1), int(y1)],
            fill=tuple(c[:3]) + (255,)
        )

    def marco(self, x0, y0, x1, y1, c):

        self.rect(x0, y0, x1, y0, c)
        self.rect(x0, y1, x1, y1, c)
        self.rect(x0, y0, x0, y1, c)
        self.rect(x1, y0, x1, y1, c)

    def linea(self, x0, y0, x1, y1, c):

        self.d.line(
            [int(x0), int(y0), int(x1), int(y1)],
            fill=tuple(c[:3]) + (255,)
        )

    def poly(self, pts, c):

        self.d.polygon(
            [(int(x), int(y)) for x, y in pts],
            fill=tuple(c[:3]) + (255,)
        )

    def elipse(self, x0, y0, x1, y1, c):
        """Elipse rellena dentro del rectangulo (inclusivo)."""

        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2
        rx = (x1 - x0 + 1) / 2
        ry = (y1 - y0 + 1) / 2

        for y in range(int(y0), int(y1) + 1):

            dy = (y - cy) / ry

            if abs(dy) > 1:
                continue

            hw = rx * math.sqrt(max(0.0, 1 - dy * dy))

            xa = int(math.ceil(cx - hw + 0.01))
            xb = int(math.floor(cx + hw - 0.01))

            if xb < xa:
                xa = xb = int(round(cx))

            self.rect(xa, y, xb, y, c)

    def circulo(self, cx, cy, r, c):

        self.elipse(cx - r, cy - r, cx + r, cy + r, c)

    def semi(self, cx, y_base, rx, ry, c):
        """Media elipse superior apoyada en y_base (para arcos y cupulas)."""

        for dy in range(0, int(ry) + 1):

            t = dy / max(1, ry)

            hw = rx * math.sqrt(max(0.0, 1 - t * t))

            xa = int(round(cx - hw))
            xb = int(round(cx + hw))

            self.rect(xa, y_base - dy, xb, y_base - dy, c)

    def arco(self, x0, y_base, x1, alto, c):
        """Rectangulo con la parte de arriba redondeada (ventana o puerta)."""

        ancho = x1 - x0 + 1
        rx = ancho / 2
        cx = (x0 + x1) / 2

        alto_recto = max(0, alto - int(rx))

        self.rect(x0, y_base - alto_recto, x1, y_base, c)

        for dy in range(0, int(math.ceil(rx))):

            t = (dy + 0.5) / rx

            hw = rx * math.sqrt(max(0.0, 1 - t * t))

            xa = int(math.ceil(cx - hw + 0.01))
            xb = int(math.floor(cx + hw - 0.01))

            if xb < xa:
                continue

            self.rect(xa, y_base - alto_recto - 1 - dy, xb,
                      y_base - alto_recto - 1 - dy, c)

    # ------------------------------------------------------
    # combinar / exportar
    # ------------------------------------------------------

    def pegar(self, otro, x, y):
        """Pega otro lienzo (con transparencia) con su esquina en (x, y)."""

        src = otro.im if isinstance(otro, Lienzo) else otro

        x = int(x)
        y = int(y)

        sx0 = max(0, -x)
        sy0 = max(0, -y)
        sx1 = min(src.width, self.w - x)
        sy1 = min(src.height, self.h - y)

        if sx1 <= sx0 or sy1 <= sy0:
            return

        recorte = src.crop((sx0, sy0, sx1, sy1))

        self.im.alpha_composite(recorte, (x + sx0, y + sy0))

    def copia(self):

        n = Lienzo(self.w, self.h)
        n.im = self.im.copy()
        n.d = ImageDraw.Draw(n.im)

        return n

    def contorno(self, factor=0.40, color=None):
        """
        Borde de 1 pixel alrededor de la silueta. Si no se da color, cada
        pixel del borde toma el color del dibujo que tiene al lado, oscuro
        (como los sprites de los personajes, pero menos duro).
        """

        a = np.array(self.im).astype(np.int32)

        alfa = a[..., 3] > 0

        h, w = alfa.shape

        pad = np.pad(alfa, 1)

        vecinos = [
            pad[0:h, 1:w + 1],
            pad[2:h + 2, 1:w + 1],
            pad[1:h + 1, 0:w],
            pad[1:h + 1, 2:w + 2],
        ]

        rgbp = np.pad(a[..., :3], ((1, 1), (1, 1), (0, 0)))

        cols = [
            rgbp[0:h, 1:w + 1],
            rgbp[2:h + 2, 1:w + 1],
            rgbp[1:h + 1, 0:w],
            rgbp[1:h + 1, 2:w + 2],
        ]

        suma = np.zeros((h, w, 3), np.int32)
        cuenta = np.zeros((h, w), np.int32)

        for v, col in zip(vecinos, cols):

            suma += col * v[..., None]
            cuenta += v

        borde = (cuenta > 0) & (~alfa)

        out = a.copy()

        if color is None:

            medio = suma / np.maximum(cuenta, 1)[..., None]

            medio = medio * factor + np.array([14, 12, 30]) * 0.5

            out[..., :3][borde] = np.clip(medio[borde], 0, 255).astype(np.int32)

        else:

            out[..., :3][borde] = np.array(color[:3])

        out[..., 3][borde] = 255

        self.im = Image.fromarray(out.astype(np.uint8), "RGBA")

        self.d = ImageDraw.Draw(self.im)

        return self

    def bruma(self, color, t):
        """Mezcla los colores con 'color' (efecto de lejania)."""

        a = np.array(self.im).astype(np.float32)

        m = a[..., 3] > 0

        for i in range(3):

            a[..., i][m] = a[..., i][m] * (1 - t) + color[i] * t

        self.im = Image.fromarray(a.astype(np.uint8), "RGBA")

        self.d = ImageDraw.Draw(self.im)

        return self

    def recortar(self):
        """Recorta los bordes transparentes."""

        caja = self.im.getbbox()

        if caja is None:
            return self

        n = Lienzo(caja[2] - caja[0], caja[3] - caja[1])
        n.im = self.im.crop(caja)
        n.d = ImageDraw.Draw(n.im)

        return n

    def guardar(self, ruta):

        os.makedirs(os.path.dirname(ruta), exist_ok=True)

        self.im.save(ruta)

    # ------------------------------------------------------
    # texto con la fuente pixel del juego (letras de 5 x 7)
    # ------------------------------------------------------

    def texto(self, x, y, s, c, esc=1):
        """Dibuja texto en mayusculas. (x, y) es la esquina de arriba."""

        filas = mapa_de_bits(s)

        # Las mayusculas ocupan las filas 3 a 9 de la celda
        filas = filas[3:10]

        for j, fila in enumerate(filas):

            for i, ch in enumerate(fila):

                if ch == "#":

                    self.rect(
                        x + i * esc, y + j * esc,
                        x + i * esc + esc - 1, y + j * esc + esc - 1,
                        c
                    )

        return len(filas[0]) * esc


def ancho_texto(s, esc=1):

    return len(mapa_de_bits(s)[0]) * esc


# ==========================================================
# FORMAS ARQUITECTONICAS
# ==========================================================

def volumen(l, x0, y0, x1, y1, base, luz_ancho=1, sombra_ancho=2,
            techo=True):
    """
    Bloque con luz desde la izquierda: borde izquierdo claro, borde
    derecho oscuro y una linea clara arriba.
    """

    p = pal(base)

    l.rect(x0, y0, x1, y1, p["b"])

    if luz_ancho > 0:
        l.rect(x0, y0, x0 + luz_ancho - 1, y1, p["l"])

    if sombra_ancho > 0:
        l.rect(x1 - sombra_ancho + 1, y0, x1, y1, p["s"])

    if techo:
        l.rect(x0, y0, x1, y0, p["l"])

    return p


def ladrillos(l, x0, y0, x1, y1, c1, c2=None, junta=None, alto=2, largo=5):
    """Pared de ladrillos con juntas."""

    c2 = c2 or sombra(c1, 0.88)
    junta = junta or sombra(c1, 0.7)

    l.rect(x0, y0, x1, y1, c1)

    fila = 0

    for y in range(y0, y1 + 1, alto):

        # linea de junta horizontal
        if y + alto - 1 <= y1:
            l.rect(x0, y + alto - 1, x1, y + alto - 1, junta)

        desfase = (largo // 2) if fila % 2 else 0

        for x in range(x0 - desfase, x1 + 1, largo):

            if x >= x0 and y + alto - 2 >= y:
                l.rect(x, y, x, min(y + alto - 2, y1), junta)

            # algun ladrillo mas oscuro para que no se vea plano
            if ((x * 7 + y * 13) % 5) == 0 and x + 1 <= x1 and x >= x0:
                l.rect(x + 1, y, min(x + largo - 2, x1), min(y + alto - 2, y1), c2)

        fila += 1


def ventanas(l, x, y, cols, filas, w, h, sep_x, sep_y, vidrio=VIDRIO,
             marco=None, brillo=VIDRIO_LUZ, persiana=None):
    """Grilla de ventanas rectangulares. (x, y) = esquina de la primera."""

    for j in range(filas):

        for i in range(cols):

            vx = x + i * (w + sep_x)
            vy = y + j * (h + sep_y)

            if marco is not None:

                l.rect(vx - 1, vy - 1, vx + w, vy + h, marco)

            l.rect(vx, vy, vx + w - 1, vy + h - 1, vidrio)

            if w >= 3 and h >= 3 and brillo is not None:

                l.px(vx, vy, brillo)

                if w >= 4:
                    l.px(vx + 1, vy, brillo)

            if persiana is not None:

                l.rect(vx, vy, vx + w - 1, vy, persiana)


def ventana_arco(l, x0, y_base, x1, alto, vidrio=VIDRIO, marco=None,
                 brillo=VIDRIO_LUZ):
    """Ventana o puerta con arco de medio punto."""

    if marco is not None:

        l.arco(x0 - 1, y_base + 1, x1 + 1, alto + 2, marco)

    l.arco(x0, y_base, x1, alto, vidrio)

    if brillo is not None:

        l.px(x0 + 1, y_base - alto + 3, brillo)


def columnas(l, x0, x1, y0, y1, n, w, c, capitel=True, base=True,
             estrias=True):
    """
    n columnas repartidas entre x0 y x1 (centros incluidos en los
    extremos). y0 = arriba del capitel, y1 = abajo de la base.
    """

    p = pal(c)

    if n == 1:
        centros = [(x0 + x1) / 2]
    else:
        centros = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]

    for cx in centros:

        xa = int(round(cx - w / 2))
        xb = xa + w - 1

        l.rect(xa, y0, xb, y1, p["b"])

        if estrias and w >= 3:
            l.rect(xa, y0, xa, y1, p["l"])
            l.rect(xb, y0, xb, y1, p["s"])

        if capitel:
            l.rect(xa - 1, y0, xb + 1, y0 + 1, p["l"])
            l.rect(xa - 1, y0 + 1, xb + 1, y0 + 1, p["s"])

        if base:
            l.rect(xa - 1, y1 - 1, xb + 1, y1, p["s"])


def fronton(l, x0, x1, y_base, alto, c, interior=None, borde=None):
    """Triangulo clasico (frontispicio) apoyado en y_base."""

    p = pal(c)

    mx = (x0 + x1) / 2

    l.poly([(x0, y_base), (mx, y_base - alto), (x1, y_base)], borde or p["l"])

    # el hueco interior (timpano)
    if x1 - x0 > 8 and alto > 4:

        l.poly(
            [(x0 + 3, y_base - 1), (mx, y_base - alto + 3), (x1 - 3, y_base - 1)],
            interior or p["s"]
        )

    l.rect(x0 - 1, y_base, x1 + 1, y_base + 1, p["l"])


def cupula(l, cx, y_base, rx, ry, c, costillas=0, c_luz=None, c_sombra=None,
           linterna=False, remate=None):
    """
    Cupula (media elipse) con luz a la izquierda y costillas verticales.
    """

    p = pal(c)

    c_luz = c_luz or p["l"]
    c_sombra = c_sombra or p["s"]

    for dy in range(0, int(ry) + 1):

        t = dy / max(1, ry)

        hw = rx * math.sqrt(max(0.0, 1 - t * t))

        xa = int(round(cx - hw))
        xb = int(round(cx + hw))

        y = y_base - dy

        l.rect(xa, y, xb, y, p["b"])

        # zona de luz y de sombra segun la posicion horizontal
        ancho = xb - xa

        if ancho >= 3:

            l.rect(xa, y, xa + max(0, int(ancho * 0.22)), y, c_luz)

            l.rect(xb - max(0, int(ancho * 0.28)), y, xb, y, c_sombra)

    if costillas:

        for k in range(1, costillas + 1):

            u = -1 + 2 * k / (costillas + 1)

            for dy in range(0, int(ry) + 1):

                t = dy / max(1, ry)

                hw = rx * math.sqrt(max(0.0, 1 - t * t))

                x = int(round(cx + u * hw))

                if abs(x - cx) <= hw:
                    l.px(x, y_base - dy, p["o"])

    if linterna:

        l.rect(cx - 2, y_base - ry - 4, cx + 2, y_base - ry + 1, p["l"])
        l.rect(cx - 1, y_base - ry - 3, cx + 1, y_base - ry - 1, VIDRIO)
        l.rect(cx - 3, y_base - ry - 5, cx + 3, y_base - ry - 5, p["s"])

    if remate:

        arriba = y_base - ry - (6 if linterna else 0)

        l.rect(cx, arriba - 4, cx, arriba, remate)
        l.rect(cx - 1, arriba - 3, cx + 1, arriba - 3, remate)


def aguja(l, cx, y_base, ancho, alto, c, cuatro_caras=True):
    """Techo piramidal / aguja con dos caras (luz y sombra)."""

    p = pal(c)

    l.poly([(cx - ancho // 2, y_base), (cx, y_base - alto), (cx + ancho // 2, y_base)], p["b"])

    # cara derecha en sombra
    l.poly([(cx, y_base - alto), (cx + ancho // 2, y_base), (cx + 1, y_base)], p["s"])

    l.linea(cx - ancho // 2, y_base, cx, y_base - alto, p["l"])


def escalera(l, x0, x1, y_base, peldanos, c, alto=1):
    """Escalinata ancha: cada peldano es mas angosto que el de abajo."""

    p = pal(c)

    for i in range(peldanos):

        y = y_base - i * alto

        l.rect(x0 + i, y, x1 - i, y, p["l"] if i % 2 == 0 else p["b"])


def reja(l, x0, x1, y, alto, c, sep=2):
    """Baranda / reja de hierro."""

    l.rect(x0, y, x1, y, c)

    for x in range(x0, x1 + 1, sep):
        l.rect(x, y, x, y + alto, c)

    l.rect(x0, y + alto, x1, y + alto, c)


def balcon(l, x0, x1, y, c=None, alto=2):
    """Balcon con baranda."""

    c = c or NEGRO

    l.rect(x0, y, x1, y, c)

    for x in range(x0, x1 + 1, 2):
        l.rect(x, y + 1, x, y + alto, c)

    l.rect(x0, y + alto, x1, y + alto, c)


def cornisa(l, x0, x1, y, c, alto=2, vuelo=1):
    """Cornisa que sobresale (franja clara + franja de sombra)."""

    p = pal(c)

    l.rect(x0 - vuelo, y, x1 + vuelo, y, p["l"])

    l.rect(x0 - vuelo, y + 1, x1 + vuelo, y + alto - 1, p["b"])

    l.rect(x0 - vuelo, y + alto, x1 + vuelo, y + alto, p["s"])


def bandera(l, x, y_mastil_base, alto_mastil, ancho=8, alto=5):
    """Mastil con bandera argentina flameando."""

    l.rect(x, y_mastil_base - alto_mastil, x, y_mastil_base, rgb("#cfcfcf"))

    y0 = y_mastil_base - alto_mastil

    for i in range(ancho):

        onda = 1 if (i // 2) % 2 else 0

        l.rect(x + 1 + i, y0 + onda, x + 1 + i, y0 + onda + alto // 3 - 0, CELESTE_ARG)
        l.rect(x + 1 + i, y0 + onda + alto // 3 + 1, x + 1 + i, y0 + onda + 2 * alto // 3, rgb("#fafafa"))
        l.rect(x + 1 + i, y0 + onda + 2 * alto // 3 + 1, x + 1 + i, y0 + onda + alto, CELESTE_ARG)

    l.px(x + 1 + ancho // 2, y0 + (alto // 2) + (1 if (ancho // 2 // 2) % 2 else 0), ORO)


# ==========================================================
# NATURALEZA
# ==========================================================

def arbol(l, x, y_base, h, tipo="platano", seed=0):
    """
    Arbol con base en (x, y_base). tipos: platano, jacaranda, ombu,
    cipres, palmera, palo_borracho, ficus, sauce.
    """

    r = random.Random(seed * 131 + x)

    tr = TRONCO

    if tipo == "cipres":

        verde = rgb("#2f6b3a")

        ancho = max(4, h // 4)

        for dy in range(h):

            t = dy / h

            hw = (ancho / 2) * math.sin(math.pi * min(1, (t * 0.85 + 0.12))) ** 0.7

            hw = max(0.8, hw) if dy > 1 else 0.8

            xa = int(round(x - hw))
            xb = int(round(x + hw))

            y = y_base - dy

            l.rect(xa, y, xb, y, verde)
            l.px(xa, y, luz(verde, 0.18))
            l.px(xb, y, sombra(verde, 0.7))

        l.rect(x, y_base - 1, x, y_base, tr)

        return

    if tipo == "palmera":

        alto_tronco = int(h * 0.72)

        for dy in range(alto_tronco):

            l.rect(x - 1 + (dy // 9), y_base - dy, x + (dy // 9), y_base - dy,
                   tr if dy % 3 else sombra(tr, 0.8))

        tx = x + alto_tronco // 9

        ty = y_base - alto_tronco

        hoja = rgb("#3f8a3a")

        for ang in (-170, -140, -110, -70, -40, -10):

            ra = math.radians(ang)

            largo = h * 0.32

            for k in range(int(largo)):

                px = tx + math.cos(ra) * k
                py = ty + math.sin(ra) * k * 0.55 + (k * k) / (largo * 3.2)

                l.px(int(px), int(py), hoja)
                l.px(int(px), int(py) + 1, sombra(hoja, 0.8))

        l.circulo(tx, ty + 1, 1, rgb("#7a5230"))

        return

    if tipo == "palo_borracho":

        verde = rgb("#4a8d3a")

        ancho_tr = max(3, h // 8)

        for dy in range(int(h * 0.5)):

            ww = ancho_tr / 2 + (1.5 if dy < 4 else 0) - dy * 0.02

            l.rect(int(x - ww), y_base - dy, int(x + ww), y_base - dy, rgb("#7a8a5a"))
            l.px(int(x - ww) + 1, y_base - dy, rgb("#9aa876"))
            l.px(int(x + ww), y_base - dy, rgb("#5a6a42"))

            if dy % 4 == 1:
                l.px(int(x), y_base - dy, rgb("#a28a5a"))

        cy = y_base - int(h * 0.62)

        l.elipse(x - h // 3, cy - h // 4, x + h // 3, cy + h // 5, verde)

        for _ in range(h // 3):

            px_ = x + r.randint(-h // 3 + 1, h // 3 - 1)
            py_ = cy + r.randint(-h // 4 + 1, h // 5 - 1)

            l.px(px_, py_, rgb("#f0a8c8"))

        return

    if tipo == "sauce":

        verde = rgb("#6aa646")

        for dy in range(int(h * 0.45)):
            l.rect(x - 1, y_base - dy, x, y_base - dy, tr)

        cy = y_base - int(h * 0.5)

        l.elipse(x - h // 2 + 1, cy - h // 5, x + h // 2 - 1, cy + h // 8, verde)

        for k in range(-h // 2 + 2, h // 2 - 1, 2):

            largo = r.randint(h // 5, h // 3)

            l.rect(x + k, cy, x + k, cy + largo, sombra(verde, 0.85) if k % 4 else verde)

        return

    # arboles de copa redonda (platano / jacaranda / ombu / ficus)
    copa = {
        "platano": rgb("#4c9a3c"),
        "jacaranda": rgb("#a98bd6"),
        "ombu": rgb("#3a8a45"),
        "ficus": rgb("#2f7f3f"),
    }.get(tipo, VERDE_ARBOL)

    alto_tronco = int(h * (0.42 if tipo != "ombu" else 0.32))

    ancho_tr = max(2, h // 9)

    if tipo in ("ombu", "ficus"):
        ancho_tr = max(3, h // 6)

    for dy in range(alto_tronco):

        extra = 1 if (tipo in ("ombu", "ficus") and dy < 4) else 0

        l.rect(x - ancho_tr // 2 - extra, y_base - dy, x + ancho_tr // 2 + extra, y_base - dy, tr)

        l.px(x - ancho_tr // 2 - extra, y_base - dy, luz(tr, 0.2))

        l.px(x + ancho_tr // 2 + extra, y_base - dy, sombra(tr, 0.75))

    rad_x = int(h * (0.34 if tipo != "ombu" else 0.5))
    rad_y = int(h * (0.3 if tipo != "ombu" else 0.26))

    cy = y_base - alto_tronco - rad_y + 3

    # copa: varias "bolas" para silueta irregular
    bolas = [
        (0, 0, rad_x, rad_y),
        (-rad_x * 0.55, rad_y * 0.25, rad_x * 0.62, rad_y * 0.7),
        (rad_x * 0.55, rad_y * 0.25, rad_x * 0.62, rad_y * 0.7),
        (-rad_x * 0.2, -rad_y * 0.5, rad_x * 0.6, rad_y * 0.6),
        (rad_x * 0.25, -rad_y * 0.45, rad_x * 0.55, rad_y * 0.55),
    ]

    for bx, by, brx, bry in bolas:

        l.elipse(int(x + bx - brx), int(cy + by - bry),
                 int(x + bx + brx), int(cy + by + bry), copa)

    # luz arriba-izquierda y sombra abajo-derecha
    for bx, by, brx, bry in bolas[:1] + bolas[3:4]:

        l.elipse(int(x + bx - brx * 0.8), int(cy + by - bry * 0.95),
                 int(x + bx + brx * 0.1), int(cy + by - bry * 0.05), luz(copa, 0.22))

    l.elipse(int(x - rad_x * 0.2), int(cy + rad_y * 0.25),
             int(x + rad_x * 0.95), int(cy + rad_y * 0.95), sombra(copa, 0.82))

    # hojitas sueltas
    for _ in range(rad_x):

        px_ = int(x + r.uniform(-rad_x, rad_x))
        py_ = int(cy + r.uniform(-rad_y, rad_y * 0.8))

        if abs(px_ - x) < rad_x * (1 - abs(py_ - cy) / (rad_y + 1) * 0.5):
            l.px(px_, py_, luz(copa, 0.3) if r.random() < 0.5 else sombra(copa, 0.8))


def arbusto(l, x, y_base, ancho, alto, c=None):

    c = c or rgb("#3a8a3a")

    l.elipse(x - ancho // 2, y_base - alto, x + ancho // 2, y_base, c)
    l.elipse(x - ancho // 2 + 1, y_base - alto, x, y_base - alto // 2, luz(c, 0.2))
    l.rect(x - ancho // 2, y_base - 1, x + ancho // 2, y_base, sombra(c, 0.8))


# ==========================================================
# OBJETOS DE LA CALLE
# ==========================================================

def farola(l, x, y_base, alto=26, c=None, estilo="clasico"):

    c = c or rgb("#2c3a3a")

    l.rect(x, y_base - alto, x, y_base, c)

    l.rect(x - 1, y_base - 1, x + 1, y_base, c)

    if estilo == "clasico":

        l.rect(x - 2, y_base - alto - 3, x + 2, y_base - alto - 1, rgb("#f4e7a3"))
        l.rect(x - 2, y_base - alto - 4, x + 2, y_base - alto - 4, c)
        l.px(x, y_base - alto - 5, c)

    else:

        l.rect(x, y_base - alto, x + 5, y_base - alto, c)
        l.rect(x + 3, y_base - alto + 1, x + 6, y_base - alto + 1, rgb("#f4e7a3"))


def banco(l, x, y_base, ancho=9, c=None):

    c = c or rgb("#7a5230")

    l.rect(x, y_base - 4, x + ancho, y_base - 4, c)
    l.rect(x, y_base - 2, x + ancho, y_base - 2, luz(c, 0.15))
    l.rect(x, y_base - 4, x, y_base, rgb("#3a3a3a"))
    l.rect(x + ancho, y_base - 4, x + ancho, y_base, rgb("#3a3a3a"))


def cartel_calle(l, x, y_base, nombre, alto=22, fondo=None):
    """Cartel de calle azul/verde en un poste (como los de la ciudad)."""

    fondo = fondo or rgb("#1f6f3f")

    l.rect(x, y_base - alto, x, y_base, rgb("#555a60"))

    ancho = ancho_texto(nombre) + 4

    l.rect(x - ancho // 2, y_base - alto - 9, x + ancho // 2, y_base - alto + 1, BLANCO)
    l.rect(x - ancho // 2 + 1, y_base - alto - 8, x + ancho // 2 - 1, y_base - alto, fondo)

    l.texto(x - ancho // 2 + 2, y_base - alto - 7, nombre, BLANCO)


def parada_colectivo(l, x, y_base, ancho=22):

    c = rgb("#3d6b8a")

    l.rect(x, y_base - 20, x + ancho, y_base - 18, c)
    l.rect(x, y_base - 20, x + ancho, y_base - 20, luz(c, 0.3))

    l.rect(x + 1, y_base - 18, x + 1, y_base, rgb("#2a2f35"))
    l.rect(x + ancho - 1, y_base - 18, x + ancho - 1, y_base, rgb("#2a2f35"))

    l.rect(x + 2, y_base - 17, x + ancho - 2, y_base - 5, rgb("#9fc7e0"))
    l.rect(x + 2, y_base - 17, x + ancho - 2, y_base - 17, rgb("#cfe6f2"))

    l.rect(x + 4, y_base - 4, x + ancho - 4, y_base - 3, rgb("#7a5230"))

    # cartelito de la parada
    l.rect(x + ancho + 3, y_base - 24, x + ancho + 3, y_base, rgb("#555a60"))
    l.rect(x + ancho + 1, y_base - 28, x + ancho + 5, y_base - 23, rgb("#e7c22b"))
    l.px(x + ancho + 3, y_base - 26, NEGRO)


def kiosco(l, x, y_base, c=None, ancho=16):
    """Kiosco de diarios y revistas."""

    c = c or rgb("#2f8f5a")

    volumen(l, x, y_base - 17, x + ancho, y_base, c)

    l.rect(x - 1, y_base - 19, x + ancho + 1, y_base - 17, sombra(c, 0.7))

    for i in range(0, ancho, 3):

        l.rect(x + 1 + i, y_base - 12, x + 2 + i, y_base - 8,
               [ROJO, AMARILLO_BOCA, rgb("#e88fb0"), rgb("#f4f1e8")][(i // 3) % 4])

    l.rect(x + 1, y_base - 7, x + ancho - 1, y_base - 6, rgb("#2b2b2b"))

    # toldo a rayas
    for i in range(0, ancho + 3, 2):

        l.rect(x - 1 + i, y_base - 15, x + i, y_base - 14, ROJO if (i // 2) % 2 else BLANCO)


def cabina_telefonica(l, x, y_base):

    l.rect(x, y_base - 12, x + 5, y_base, rgb("#d8362f"))
    l.rect(x + 1, y_base - 10, x + 4, y_base - 3, rgb("#9fc7e0"))
    l.rect(x, y_base - 12, x + 5, y_base - 12, rgb("#f4a09a"))


def entrada_subte(l, x, y_base, ancho=14):
    """Boca de subte con el techo verde y la baranda."""

    verde = rgb("#2f8f5a")

    l.rect(x, y_base - 14, x + ancho, y_base - 12, verde)
    l.rect(x, y_base - 14, x + ancho, y_base - 14, luz(verde, 0.3))
    l.rect(x + 1, y_base - 12, x + 1, y_base, rgb("#2a2f35"))
    l.rect(x + ancho - 1, y_base - 12, x + ancho - 1, y_base, rgb("#2a2f35"))
    l.rect(x + 2, y_base - 11, x + ancho - 2, y_base, rgb("#1a1d22"))
    l.rect(x + 2, y_base - 9, x + ancho - 2, y_base - 9, rgb("#e7c22b"))


def persona(l, x, y_base, camisa, pantalon=None, pelo=None, alto=11):
    """Persona chiquita (silueta con color) para dar escala."""

    pantalon = pantalon or rgb("#2b3550")
    pelo = pelo or rgb("#3a2a1f")

    piel = rgb("#e0b08a")

    l.rect(x, y_base - 4, x, y_base, pantalon)
    l.rect(x + 2, y_base - 4, x + 2, y_base, pantalon)
    l.rect(x, y_base - 8, x + 2, y_base - 5, camisa)
    l.rect(x, y_base - 10, x + 2, y_base - 9, piel)
    l.rect(x, y_base - 11, x + 2, y_base - 11, pelo)


# ==========================================================
# CIELO
# ==========================================================

def cielo(ancho, alto, arriba, medio, abajo):
    """Degradado vertical en bandas (queda mas pixel art que uno suave)."""

    l = Lienzo(ancho, alto)

    bandas = 14

    for i in range(bandas):

        t = i / (bandas - 1)

        if t < 0.55:
            c = mezcla(arriba, medio, t / 0.55)
        else:
            c = mezcla(medio, abajo, (t - 0.55) / 0.45)

        y0 = int(i * alto / bandas)
        y1 = int((i + 1) * alto / bandas) - 1

        l.rect(0, y0, ancho - 1, y1, c)

    return l


def nube(l, x, y, ancho, c=(255, 255, 255), sombra_c=None):
    """Nube pixel art de panza plana."""

    sombra_c = sombra_c or mezcla(c, (150, 175, 215), 0.35)

    alto = max(5, ancho // 4)

    l.elipse(x, y + alto // 2, x + ancho, y + alto + alto // 2, c)
    l.elipse(x + ancho // 6, y, x + ancho // 2 + ancho // 8, y + alto, c)
    l.elipse(x + ancho // 2 - ancho // 10, y + alto // 4, x + ancho - ancho // 8, y + alto + 1, c)

    l.rect(x + 1, y + alto + alto // 2 - 1, x + ancho - 1, y + alto + alto // 2, sombra_c)


# ==========================================================
# ESTATUAS Y CUPULAS DE CEBOLLA
# ==========================================================

def figura(l, x, y_base, h, c, pose="pie", sombrero=None, falda=True):
    """
    Estatua / figura humana estilizada. x = centro, y_base = pies.
    poses: pie, brazo_der, brazo_izq, brazos_arriba, mira_lejos
    """

    p = pal(c)

    cab = max(3, h // 6)

    ancho = max(3, h // 4 + (1 if falda else 0))

    y_cuerpo = y_base - h + cab + 1

    xa = x - ancho // 2
    xb = xa + ancho - 1

    # cuerpo / tunica
    l.rect(xa, y_cuerpo, xb, y_base, p["b"])
    l.rect(xa, y_cuerpo, xa, y_base, p["l"])
    l.rect(xb, y_cuerpo, xb, y_base, p["s"])

    if falda:
        l.rect(xa - 1, y_base - h // 4, xb + 1, y_base, p["b"])
        l.rect(xa - 1, y_base - h // 4, xa - 1, y_base, p["l"])
        l.rect(xb + 1, y_base - h // 4, xb + 1, y_base, p["s"])

    # cabeza
    l.elipse(x - cab // 2, y_base - h, x - cab // 2 + cab - 1, y_base - h + cab - 1, p["l"])

    if sombrero:
        l.rect(x - cab // 2 - 1, y_base - h + 1, x - cab // 2 + cab, y_base - h + 1, sombrero)
        l.rect(x - cab // 2, y_base - h - 1, x - cab // 2 + cab - 1, y_base - h, sombrero)

    hombro = y_cuerpo + 1

    largo = max(3, h // 3)

    if pose in ("brazo_der", "brazos_arriba", "mira_lejos"):
        l.linea(xb, hombro, xb + largo // 2, hombro - largo, p["b"])
        l.linea(xb + 1, hombro, xb + largo // 2 + 1, hombro - largo, p["s"])

    if pose in ("brazo_izq", "brazos_arriba"):
        l.linea(xa, hombro, xa - largo // 2, hombro - largo, p["l"])

    return p


def cebolla(l, cx, y_base, w, h, c, cruz=True, estrellas=None):
    """Cupula bulbosa (de iglesia rusa) con su cruz."""

    p = pal(c)

    for dy in range(h):

        t = dy / h

        if t <= 0.35:
            prof = 0.6 + 0.4 * math.sin(t / 0.35 * math.pi / 2)
        else:
            u = (t - 0.35) / 0.65
            prof = max(0.0, math.cos(u * math.pi / 2)) ** 1.5

        hw = (w / 2) * prof

        xa = int(round(cx - hw))
        xb = int(round(cx + hw))

        y = y_base - dy

        l.rect(xa, y, xb, y, p["b"])

        ancho = xb - xa

        if ancho >= 2:
            l.rect(xa, y, xa + max(0, int(ancho * 0.25)), y, p["l"])
            l.rect(xb - max(0, int(ancho * 0.28)), y, xb, y, p["s"])

    if estrellas:

        for k in range(3):
            l.px(cx - w // 4 + k * w // 4, y_base - int(h * 0.28), estrellas)

        l.px(cx - w // 6, y_base - int(h * 0.5), estrellas)
        l.px(cx + w // 6, y_base - int(h * 0.5), estrellas)

    if cruz:

        arriba = y_base - h

        l.rect(cx, arriba - 6, cx, arriba, ORO)
        l.rect(cx - 2, arriba - 4, cx + 2, arriba - 4, ORO)
        l.rect(cx - 1, arriba - 2, cx + 1, arriba - 2, ORO)


def agua_dibujo(l, x0, y0, x1, y1, c=None, seed=0):
    """Superficie de agua con reflejos."""

    c = c or rgb("#4f8fc9")

    r = random.Random(seed)

    l.rect(x0, y0, x1, y1, c)

    for _ in range(max(4, (x1 - x0) * (y1 - y0) // 60)):

        x = r.randint(x0, x1 - 3)
        y = r.randint(y0, y1)

        l.rect(x, y, x + r.randint(1, 3), y, luz(c, 0.3))

    l.rect(x0, y0, x1, y0, luz(c, 0.15))

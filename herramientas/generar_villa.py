"""
Genera el fondo de la villa para la escena de Di Lolio (escena_dilolio.py):

    assets/historia/villa_lejos.png   casillas a lo lejos (silueta oscura
                                      con alguna ventana prendida)
    assets/historia/villa_casas.png   las casillas de adelante: ladrillo
                                      hueco, chapas, tanques de agua,
                                      rejas, cables, ropa colgada y la
                                      calle de tierra con charcos

Es pixel art chiquito (alto 218): el juego lo agranda x2.
Siempre sale igual (semilla fija). Uso, desde la carpeta del juego:

    python herramientas/generar_villa.py
"""

import os
import random

from PIL import Image, ImageDraw

CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(CARPETA, "assets", "historia")

ALTO = 218
PISO = 178          # donde termina la pared y empieza la calle

TRANSPARENTE = (0, 0, 0, 0)
NEGRO = (16, 12, 20, 255)


def c(hexa, a=255):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


LADRILLOS = [c("#b8553a"), c("#c4623f"), c("#a84a33"), c("#cf7048")]
JUNTA = c("#8a3c2a")
REVOQUE = [c("#c9b79a"), c("#9fb2a6"), c("#d8c27c"), c("#b7a3c2"), c("#8fa7c4")]
CHAPA = c("#8d949c")
CHAPA_OSCURA = c("#5f666e")
OXIDO = c("#8a4b2a")


# ==========================================================
# LEJOS
# ==========================================================

def generar_lejos(azar):

    ancho = 700
    imagen = Image.new("RGBA", (ancho, ALTO), TRANSPARENTE)
    d = ImageDraw.Draw(imagen)

    silueta = c("#2a1f3d")
    ventana = c("#ffcf6a")

    x = 0
    while x < ancho:
        w = azar.randint(14, 34)
        pisos = azar.randint(2, 5)
        alto = pisos * 12 + azar.randint(0, 6)
        top = PISO - 20 - alto
        d.rectangle((x, top, x + w, PISO), fill=silueta)

        # Tanque de agua arriba de algunas
        if azar.random() < 0.4:
            tx = x + azar.randint(2, max(2, w - 8))
            d.rectangle((tx, top - 7, tx + 6, top - 1), fill=silueta)

        # Ventanitas prendidas
        for p in range(pisos):
            for vx in range(x + 3, x + w - 3, 7):
                if azar.random() < 0.18:
                    vy = top + 4 + p * 12
                    d.rectangle((vx, vy, vx + 2, vy + 3), fill=ventana)

        x += w + azar.randint(-3, 2)

    return imagen


# ==========================================================
# CASAS DE ADELANTE
# ==========================================================

def pared_ladrillo(d, azar, x0, y0, x1, y1):
    d.rectangle((x0, y0, x1, y1), fill=JUNTA)
    fila = 0
    for y in range(y0, y1 + 1, 4):
        corrido = 3 if fila % 2 else 0
        for x in range(x0 - corrido, x1 + 1, 7):
            bx0 = max(x0, x)
            bx1 = min(x1, x + 5)
            if bx1 > bx0:
                d.rectangle((bx0, y, bx1, min(y1, y + 2)), fill=azar.choice(LADRILLOS))
        fila += 1


def techo_chapa(d, azar, x0, y, x1):
    d.rectangle((x0 - 3, y - 4, x1 + 3, y), fill=CHAPA)
    for x in range(x0 - 3, x1 + 4, 3):
        d.line((x, y - 4, x, y), fill=CHAPA_OSCURA)
    # Manchas de oxido
    for _ in range(max(1, (x1 - x0) // 12)):
        ox = azar.randint(x0, x1)
        d.rectangle((ox, y - 3, ox + 2, y - 1), fill=OXIDO)
    d.line((x0 - 3, y + 1, x1 + 3, y + 1), fill=NEGRO)
    # Ladrillos y una goma arriba de la chapa (para que no se vuele)
    for _ in range(azar.randint(1, 2)):
        lx = azar.randint(x0, max(x0, x1 - 6))
        if azar.random() < 0.5:
            d.rectangle((lx, y - 7, lx + 5, y - 5), fill=azar.choice(LADRILLOS))
        else:
            d.ellipse((lx, y - 9, lx + 6, y - 4), outline=NEGRO, width=2)


def ventana(d, azar, x, y, w=10, h=9):
    d.rectangle((x - 1, y - 1, x + w + 1, y + h + 1), fill=NEGRO)
    luz = azar.random() < 0.35
    d.rectangle((x, y, x + w, y + h), fill=c("#ffd77a") if luz else c("#2b3550"))
    # Reja
    for rx in range(x + 2, x + w, 3):
        d.line((rx, y, rx, y + h), fill=c("#222222"))
    d.line((x, y + h // 2, x + w, y + h // 2), fill=c("#222222"))


def puerta(d, azar, x, y_piso):
    color = azar.choice([c("#3d6b8f"), c("#7a3b3b"), c("#4f7a45"), c("#6b5a8f")])
    d.rectangle((x - 1, y_piso - 22, x + 11, y_piso), fill=NEGRO)
    d.rectangle((x, y_piso - 21, x + 10, y_piso), fill=color)
    d.point((x + 8, y_piso - 11), fill=c("#e8d070"))


def tanque(d, x, y):
    """Tanque de agua negro (tipo Rotoplas) arriba del techo."""
    d.rectangle((x, y - 12, x + 9, y), fill=c("#1c1c1c"))
    d.rectangle((x - 1, y - 14, x + 10, y - 12), fill=c("#2a2a2a"))
    d.line((x + 2, y - 10, x + 2, y - 2), fill=c("#3a3a3a"))


def generar_casas(azar):

    ancho = 1100
    imagen = Image.new("RGBA", (ancho, ALTO), TRANSPARENTE)
    d = ImageDraw.Draw(imagen)

    techos = []     # (x, y) para colgar los cables

    x = -4
    while x < ancho:

        w = azar.randint(40, 76)
        pisos = azar.randint(1, 3)
        alto_piso = 26
        y_top = PISO - pisos * alto_piso

        for p in range(pisos):
            y0 = PISO - (p + 1) * alto_piso
            y1 = PISO - p * alto_piso
            # Algunos pisos revocados y pintados, la mayoria ladrillo
            if azar.random() < 0.3:
                d.rectangle((x, y0, x + w, y1), fill=azar.choice(REVOQUE))
                for _ in range(3):
                    mx = azar.randint(x, x + w - 6)
                    my = azar.randint(y0, y1 - 4)
                    d.rectangle((mx, my, mx + 5, my + 3), fill=JUNTA)
            else:
                pared_ladrillo(d, azar, x, y0, x + w, y1)

            # Losa entre pisos
            d.rectangle((x, y0, x + w, y0 + 1), fill=c("#7d7d7d"))

            # Ventanas
            for vx in range(x + 6, x + w - 12, 22):
                if p == 0 and vx < x + 20:
                    continue
                if azar.random() < 0.8:
                    ventana(d, azar, vx, y0 + 7)

        # Bordes
        d.line((x, y_top, x, PISO), fill=NEGRO)
        d.line((x + w, y_top, x + w, PISO), fill=NEGRO)

        puerta(d, azar, x + 6, PISO)

        # Techo: chapa, o losa sin terminar con los hierros para arriba
        if azar.random() < 0.6:
            techo_chapa(d, azar, x, y_top, x + w)
        else:
            d.rectangle((x, y_top - 2, x + w, y_top), fill=c("#8b8b8b"))
            for hx in range(x + 2, x + w, 9):
                d.line((hx, y_top - 2, hx, y_top - 9), fill=c("#5a3a2a"))
            if azar.random() < 0.5:
                # Un pedazo de piso que se esta levantando
                cx = x + azar.randint(4, max(5, w - 22))
                pared_ladrillo(d, azar, cx, y_top - 12, cx + 16, y_top - 2)

        if azar.random() < 0.6:
            tanque(d, x + azar.randint(4, max(5, w - 14)), y_top - 4)

        techos.append((x + 2, y_top - 2))
        techos.append((x + w - 2, y_top - 2))

        # Ropa colgada en la terraza
        if azar.random() < 0.35:
            cx0, cx1 = x + 6, x + w - 6
            cy = y_top - 14
            d.line((cx0, cy, cx1, cy), fill=c("#dddddd"))
            for rx in range(cx0 + 3, cx1 - 6, 9):
                ropa = azar.choice([c("#e04848"), c("#3f7fd0"), c("#f2f2f2"), c("#f0c040"), c("#40a060")])
                d.rectangle((rx, cy + 1, rx + 5, cy + 7), fill=ropa)

        x += w + azar.randint(0, 3)

    # Postes de luz y cables (cuelgan haciendo panza)
    postes = list(range(30, ancho, 150))
    for px in postes:
        d.rectangle((px, PISO - 120, px + 2, PISO), fill=c("#5b4632"))
        d.rectangle((px - 6, PISO - 120, px + 8, PISO - 118), fill=c("#5b4632"))

    for i in range(len(postes) - 1):
        a, b = postes[i], postes[i + 1]
        for k, alto in enumerate((119, 113, 106)):
            panza = 10 + k * 4
            puntos = []
            for t in range(0, 41):
                f = t / 40
                puntos.append((a + 1 + (b - a) * f, PISO - alto + panza * 4 * f * (1 - f)))
            d.line(puntos, fill=c("#111111"))

    # Algunos cables "colgados" del poste a las casas
    for px in postes:
        for _ in range(3):
            tx, ty = azar.choice(techos)
            if abs(tx - px) < 90:
                d.line((px + 1, PISO - 110, tx, ty), fill=c("#1a1a1a"))

    # Pintadas en las paredes
    for texto_x, texto in ((180, "DL"), (520, "VILLA"), (860, "AGUANTE")):
        d.text((texto_x, PISO - 20), texto, fill=c("#2a2a2a"))

    # Calle de tierra con charcos y piedritas
    d.rectangle((0, PISO, ancho, ALTO), fill=c("#8a6a48"))
    d.rectangle((0, PISO, ancho, PISO + 2), fill=c("#6e5238"))
    for _ in range(900):
        px = azar.randint(0, ancho)
        py = azar.randint(PISO + 3, ALTO)
        d.point((px, py), fill=azar.choice([c("#9c7b56"), c("#755a3e"), c("#a88a64")]))
    for _ in range(8):
        px = azar.randint(0, ancho - 40)
        py = azar.randint(PISO + 14, ALTO - 8)
        w = azar.randint(16, 36)
        d.ellipse((px, py, px + w, py + 6), fill=c("#5e7f96"))
        d.line((px + 4, py + 2, px + w // 2, py + 2), fill=c("#9fc0d4"))

    return imagen


def main():

    azar = random.Random(1906)
    os.makedirs(DESTINO, exist_ok=True)

    generar_lejos(azar).save(os.path.join(DESTINO, "villa_lejos.png"))
    generar_casas(azar).save(os.path.join(DESTINO, "villa_casas.png"))
    print("Guardado en", DESTINO)


if __name__ == "__main__":
    main()

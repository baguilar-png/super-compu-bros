"""
Genera la cuadra de la calle BOLIVAR entre AV. CASEROS y AV. MARTIN
GARCIA (limite de San Telmo y Barracas) para las escenas de Carlitos
(escenas_carlitos.py):

    assets/historia/bolivar.png           a color (reencuentro con Carlitos)
    assets/historia/bolivar_recuerdo.png  en sepia (el recuerdo de la mision)

Casas viejas de dos pisos con balcones de hierro y puertas altas, el
edificio de ladrillo rojo cerca de Caseros, arboles, faroles, vereda de
baldosas y la calle de adoquines. Las dos esquinas (al principio Caseros,
al final Martin Garcia) quedan libres: los carteles con los nombres de
las calles los dibuja el juego.

Pixel art chico (alto 218): el juego lo agranda x2. Uso:

    python herramientas/generar_bolivar.py
"""

import os
import random

from PIL import Image, ImageDraw

CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(CARPETA, "assets", "historia", "bolivar.png")
DESTINO_SEPIA = os.path.join(CARPETA, "assets", "historia", "bolivar_recuerdo.png")


def en_sepia(imagen):
    """Copia en tonos sepia (como una foto vieja)."""
    salida = imagen.copy()
    pixeles = salida.load()
    for y in range(salida.height):
        for x in range(salida.width):
            r, g, b, a = pixeles[x, y]
            v = r * 0.3 + g * 0.59 + b * 0.11
            pixeles[x, y] = (min(255, int(v * 1.07 + 20)), min(255, int(v * 0.92 + 8)), int(v * 0.72), a)
    return salida

ANCHO = 1000
ALTO = 218
VEREDA = 176            # donde empieza la vereda
CORDON = 188            # donde empieza la calle de adoquines

# Esquinas (en pixeles de este dibujo): de 0 a ESQUINA_CASEROS esta la
# Av. Caseros; de ESQUINA_MARTIN_GARCIA al final, la Av. Martin Garcia
ESQUINA_CASEROS = 70
ESQUINA_MARTIN_GARCIA = 905


def c(hexa):
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


NEGRO = c("#1c1814")
FACHADAS = [c("#e8d6b0"), c("#d9a88a"), c("#b9c9b0"), c("#e3c46e"),
            c("#c7b2cf"), c("#a9c2d6"), c("#e2b9a8"), c("#d8cdb8")]
HIERRO = c("#2a2a2a")
MADERA = [c("#5a3a22"), c("#3d5a3a"), c("#4a3c5e"), c("#6a2f2a")]


def _cielo(d):
    arriba, abajo = (120, 176, 230), (206, 230, 246)
    for y in range(VEREDA):
        f = y / VEREDA
        col = tuple(int(arriba[i] + (abajo[i] - arriba[i]) * f) for i in range(3)) + (255,)
        d.line((0, y, ANCHO, y), fill=col)


def _ventana_balcon(d, x, y, azar):
    # Ventana alta con arco y postigos
    d.rectangle((x - 1, y - 1, x + 11, y + 24), fill=NEGRO)
    d.rectangle((x, y + 2, x + 10, y + 23), fill=c("#3a4a62"))
    d.rectangle((x, y, x + 10, y + 2), fill=c("#3a4a62"))
    d.line((x + 5, y + 2, x + 5, y + 23), fill=c("#d8d0c0"))
    d.line((x, y + 10, x + 10, y + 10), fill=c("#d8d0c0"))
    postigo = azar.choice(MADERA)
    d.rectangle((x - 4, y + 2, x - 1, y + 23), fill=postigo)
    d.rectangle((x + 11, y + 2, x + 14, y + 23), fill=postigo)
    # Balcon con baranda de hierro
    d.rectangle((x - 6, y + 23, x + 16, y + 25), fill=c("#9a9488"))
    d.line((x - 6, y + 15, x + 16, y + 15), fill=HIERRO)
    for bx in range(x - 6, x + 17, 3):
        d.line((bx, y + 15, bx, y + 23), fill=HIERRO)
    if azar.random() < 0.4:
        # Maceta con plantas
        d.rectangle((x + 10, y + 11, x + 14, y + 14), fill=c("#a0522d"))
        d.rectangle((x + 9, y + 8, x + 15, y + 11), fill=c("#4f8a3a"))


def _puerta(d, x, y_piso, azar):
    madera = azar.choice(MADERA)
    d.rectangle((x - 2, y_piso - 38, x + 16, y_piso), fill=NEGRO)
    d.rectangle((x - 1, y_piso - 37, x + 15, y_piso), fill=madera)
    d.pieslice((x - 1, y_piso - 45, x + 15, y_piso - 29), 180, 360, fill=madera, outline=NEGRO)
    d.line((x + 7, y_piso - 37, x + 7, y_piso), fill=NEGRO)
    # Banderola de vidrio
    d.pieslice((x + 2, y_piso - 42, x + 12, y_piso - 32), 180, 360, fill=c("#9ec4d8"))
    d.point((x + 5, y_piso - 18), fill=c("#e0c060"))
    d.point((x + 9, y_piso - 18), fill=c("#e0c060"))


def _casa(d, x, ancho, azar):
    alto = azar.choice([92, 100, 108])
    top = VEREDA - alto
    fachada = azar.choice(FACHADAS)

    d.rectangle((x, top, x + ancho, VEREDA), fill=fachada)
    # Zocalo
    d.rectangle((x, VEREDA - 10, x + ancho, VEREDA), fill=c("#8c8070"))
    # Cornisa y pretil con balaustres
    d.rectangle((x - 2, top - 2, x + ancho + 2, top + 3), fill=c("#f2ead8"))
    d.line((x - 2, top + 3, x + ancho + 2, top + 3), fill=NEGRO)
    d.rectangle((x, top - 10, x + ancho, top - 3), fill=fachada)
    for bx in range(x + 3, x + ancho - 2, 4):
        d.rectangle((bx, top - 8, bx + 1, top - 4), fill=c("#f2ead8"))
    d.line((x, top - 10, x + ancho, top - 10), fill=NEGRO)
    # Moldura entre pisos
    d.line((x, top + alto // 2, x + ancho, top + alto // 2), fill=c("#f2ead8"))
    # Bordes
    d.line((x, top - 10, x, VEREDA), fill=NEGRO)
    d.line((x + ancho, top - 10, x + ancho, VEREDA), fill=NEGRO)

    # Primer piso: ventanas con balcon
    for vx in range(x + 12, x + ancho - 16, 30):
        _ventana_balcon(d, vx, top + 10, azar)

    # Planta baja: puerta alta y alguna ventana con reja
    _puerta(d, x + 8, VEREDA, azar)
    for vx in range(x + 36, x + ancho - 14, 30):
        d.rectangle((vx - 1, VEREDA - 36, vx + 11, VEREDA - 12), fill=NEGRO)
        d.rectangle((vx, VEREDA - 35, vx + 10, VEREDA - 13), fill=c("#3a4a62"))
        for rx in range(vx + 1, vx + 10, 3):
            d.line((rx, VEREDA - 35, rx, VEREDA - 13), fill=HIERRO)

    # Manchas de humedad y algun afiche
    for _ in range(3):
        mx = azar.randint(x + 2, x + ancho - 8)
        my = azar.randint(top + 4, VEREDA - 16)
        d.rectangle((mx, my, mx + 4, my + 2), fill=tuple(max(0, v - 18) for v in fachada[:3]) + (255,))
    if azar.random() < 0.5:
        ax = azar.randint(x + 20, x + ancho - 16)
        d.rectangle((ax, VEREDA - 30, ax + 9, VEREDA - 18), fill=azar.choice([c("#e04040"), c("#f0e040"), c("#40a0e0")]))


def _edificio_ladrillo(d, x, ancho):
    """Edificio grande de ladrillo rojo, estilo ingles (cerca de Caseros)."""
    top = VEREDA - 150
    d.rectangle((x, top, x + ancho, VEREDA), fill=c("#9c3f2c"))
    for y in range(top, VEREDA, 4):
        corrido = 3 if (y // 4) % 2 else 0
        for bx in range(x - corrido, x + ancho, 7):
            d.line((max(x, bx), y, max(x, bx), y + 3), fill=c("#7d3122"))
        d.line((x, y, x + ancho, y), fill=c("#863424"))
    d.rectangle((x - 3, top - 4, x + ancho + 3, top + 2), fill=c("#e8e0d0"))
    d.line((x - 3, top + 2, x + ancho + 3, top + 2), fill=NEGRO)
    for piso in range(4):
        y = top + 12 + piso * 32
        for vx in range(x + 10, x + ancho - 12, 22):
            d.rectangle((vx - 1, y - 1, vx + 11, y + 21), fill=c("#e8e0d0"))
            d.rectangle((vx + 1, y + 1, vx + 9, y + 19), fill=c("#2e3c54"))
            d.line((vx + 5, y + 1, vx + 5, y + 19), fill=c("#e8e0d0"))
            d.line((vx + 1, y + 9, vx + 9, y + 9), fill=c("#e8e0d0"))
    d.line((x, top, x, VEREDA), fill=NEGRO)
    d.line((x + ancho, top, x + ancho, VEREDA), fill=NEGRO)
    _puerta(d, x + ancho // 2 - 7, VEREDA, random.Random(3))


def _arbol(d, x, azar):
    d.rectangle((x - 2, VEREDA - 40, x + 2, VEREDA + 4), fill=c("#5a3e28"))
    d.rectangle((x - 5, VEREDA + 2, x + 5, VEREDA + 6), fill=c("#6b4a2e"))
    verdes = [c("#3f7a34"), c("#4f8f3c"), c("#356a2c")]
    for _ in range(22):
        bx = x + azar.randint(-20, 20)
        by = VEREDA - 50 + azar.randint(-22, 14)
        r = azar.randint(5, 9)
        d.ellipse((bx - r, by - r, bx + r, by + r), fill=azar.choice(verdes))


def _farol(d, x):
    d.rectangle((x - 1, VEREDA - 62, x + 1, VEREDA + 2), fill=HIERRO)
    d.rectangle((x - 4, VEREDA - 72, x + 4, VEREDA - 62), fill=HIERRO)
    d.rectangle((x - 3, VEREDA - 70, x + 3, VEREDA - 64), fill=c("#f0e0a0"))
    d.polygon([(x - 6, VEREDA - 72), (x + 6, VEREDA - 72), (x, VEREDA - 77)], fill=HIERRO)


def _vereda_y_calle(d, azar):
    d.rectangle((0, VEREDA, ANCHO, CORDON), fill=c("#b8aea0"))
    for x in range(0, ANCHO, 6):
        d.line((x, VEREDA, x, CORDON), fill=c("#a49a8c"))
    d.line((0, VEREDA + 6, ANCHO, VEREDA + 6), fill=c("#a49a8c"))
    d.rectangle((0, CORDON, ANCHO, CORDON + 2), fill=c("#d8d4cc"))
    d.line((0, CORDON + 3, ANCHO, CORDON + 3), fill=NEGRO)
    # Adoquines
    d.rectangle((0, CORDON + 4, ANCHO, ALTO), fill=c("#5a5a62"))
    fila = 0
    for y in range(CORDON + 4, ALTO, 5):
        corrido = 4 if fila % 2 else 0
        for x in range(-corrido, ANCHO, 8):
            tono = azar.choice([c("#6c6c76"), c("#74747e"), c("#66666f"), c("#7a7884")])
            d.rectangle((x + 1, y + 1, x + 7, y + 4), fill=tono)
        fila += 1


def _esquina(d, x0, x1):
    """Cruce con la avenida: sin casas, se ve la avenida que cruza."""
    d.rectangle((x0, VEREDA - 6, x1, VEREDA), fill=c("#4a4a52"))
    # Rampa y senda peatonal en la calle
    for y in range(CORDON + 6, ALTO - 2, 6):
        d.rectangle((x0 + 12, y, x1 - 12, y + 2), fill=c("#e8e8e0"))


def main():

    azar = random.Random(2026)
    imagen = Image.new("RGBA", (ANCHO, ALTO), (0, 0, 0, 0))
    d = ImageDraw.Draw(imagen)

    _cielo(d)

    # Edificios lejanos (silueta clara)
    for x in range(0, ANCHO, 40):
        alto = azar.randint(40, 90)
        d.rectangle((x, VEREDA - 60 - alto, x + 36, VEREDA), fill=c("#b6c8da"))

    # Cuadra de casas
    x = ESQUINA_CASEROS
    _edificio_ladrillo(d, x, 120)
    x += 120
    while x < ESQUINA_MARTIN_GARCIA - 40:
        ancho = min(azar.choice([62, 70, 78, 86]), ESQUINA_MARTIN_GARCIA - x)
        _casa(d, x, ancho, azar)
        x += ancho

    _vereda_y_calle(d, azar)
    _esquina(d, 0, ESQUINA_CASEROS)
    _esquina(d, ESQUINA_MARTIN_GARCIA, ANCHO)

    # Arboles de la plaza/parque del lado de Martin Garcia
    for ax in (ESQUINA_MARTIN_GARCIA + 30, ESQUINA_MARTIN_GARCIA + 70):
        _arbol(d, ax, azar)

    # Arboles y faroles en la vereda
    for ax in range(ESQUINA_CASEROS + 150, ESQUINA_MARTIN_GARCIA - 40, 170):
        _arbol(d, ax, azar)
    for fx in range(ESQUINA_CASEROS + 70, ESQUINA_MARTIN_GARCIA, 120):
        _farol(d, fx)

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    imagen.save(DESTINO)
    en_sepia(imagen).save(DESTINO_SEPIA)
    print("Guardado:", DESTINO, "y", DESTINO_SEPIA)


if __name__ == "__main__":
    main()

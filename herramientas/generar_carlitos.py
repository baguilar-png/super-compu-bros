"""
Genera los sprites de CARLITOS, el perro amarillo (pixel art hecho a
partir de su foto): pelo dorado/amarillo, hocico negro, orejas caidas
mas oscuras y las patas claras.

    assets/personajes/CARLITOS/parado.png     de costado, quieto
    assets/personajes/CARLITOS/correr_1.png   corriendo (4 poses)
    assets/personajes/CARLITOS/correr_2.png
    assets/personajes/CARLITOS/correr_3.png
    assets/personajes/CARLITOS/correr_4.png
    assets/personajes/CARLITOS/morder.png     saltando con la boca abierta
    assets/personajes/CARLITOS/cara.png       la cara de frente (para el mapa)

Todos miran a la DERECHA (la izquierda se da vuelta en el juego).

Uso, desde la carpeta del juego:

    python herramientas/generar_carlitos.py
"""

import math
import os

from PIL import Image, ImageDraw

CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(CARPETA, "assets", "personajes", "CARLITOS")

ANCHO, ALTO = 44, 34

PELO = (214, 166, 92, 255)
PELO_OSCURO = (176, 124, 64, 255)
PELO_CLARO = (238, 206, 152, 255)
OREJA = (128, 84, 46, 255)
HOCICO = (34, 28, 26, 255)
NARIZ = (12, 10, 10, 255)
OJO = (20, 14, 10, 255)
BRILLO = (255, 255, 255, 255)
PATA = (232, 222, 200, 255)
BOCA = (150, 30, 40, 255)
LENGUA = (236, 110, 130, 255)
DIENTE = (250, 250, 240, 255)
BORDE = (58, 36, 20, 255)


def _pierna(d, cadera, angulo, largo, color, ancho=3):
    """Pata recta desde la cadera; angulo en grados (0 = para abajo)."""

    x0, y0 = cadera
    a = math.radians(angulo)
    x1 = x0 + math.sin(a) * largo
    y1 = y0 + math.cos(a) * largo
    d.line((x0, y0, x1, y1), fill=color, width=ancho)
    # Patita clara al final
    d.rectangle((round(x1) - 1, round(y1) - 1, round(x1) + 1, round(y1)), fill=PATA)


def _perro(patas, salto=0, boca_abierta=False, cola=0):
    """
    patas: (atras_lejos, atras_cerca, adelante_lejos, adelante_cerca) en
    grados. salto: cuanto se levanta el cuerpo. cola: angulo de la cola.
    """

    img = Image.new("RGBA", (ANCHO, ALTO), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    s = 4 - salto      # margen arriba para la cabeza al saltar
    cadera = (12, 17 + s)
    hombro = (28, 17 + s)

    # Patas de atras/adelante del lado lejano (mas oscuras, abajo de todo)
    _pierna(d, (cadera[0] + 2, cadera[1]), patas[0], 11, PELO_OSCURO)
    _pierna(d, (hombro[0] - 1, hombro[1]), patas[2], 11, PELO_OSCURO)

    # Cola (un poco curva para arriba)
    ac = math.radians(cola)
    base = (8, 12 + s)
    medio = (base[0] - 3 * math.cos(ac), base[1] - 3 - 2 * math.sin(ac))
    punta = (base[0] - 5 * math.cos(ac), base[1] - 7 - 3 * math.sin(ac))
    d.line((base, medio, punta), fill=PELO, width=2)
    d.point((round(punta[0]), round(punta[1])), fill=PELO_CLARO)

    # Cuerpo y pecho
    d.ellipse((7, 9 + s, 31, 20 + s), fill=PELO)
    d.ellipse((24, 8 + s, 34, 20 + s), fill=PELO)
    # Lomo un poco mas oscuro y panza clara
    d.ellipse((10, 9 + s, 28, 13 + s), fill=PELO_OSCURO)
    d.ellipse((12, 15 + s, 30, 20 + s), fill=PELO_CLARO)
    d.ellipse((27, 12 + s, 33, 19 + s), fill=PELO_CLARO)

    # Cuello y cabeza
    d.polygon([(27, 12 + s), (31, 4 + s), (36, 6 + s), (33, 14 + s)], fill=PELO)
    d.ellipse((29, 0 + s, 39, 10 + s), fill=PELO)
    d.ellipse((31, 1 + s, 37, 5 + s), fill=PELO_CLARO)

    # Hocico negro
    if boca_abierta:
        # Mandibula de arriba levantada y la de abajo bajada
        d.rectangle((36, 3 + s, 42, 5 + s), fill=HOCICO)
        d.point((42, 3 + s), fill=NARIZ)
        d.rectangle((36, 6 + s, 41, 8 + s), fill=BOCA)
        d.rectangle((37, 7 + s, 40, 8 + s), fill=LENGUA)
        d.rectangle((36, 9 + s, 41, 10 + s), fill=HOCICO)
        for x in (37, 39, 41):
            d.point((x, 6 + s), fill=DIENTE)
            d.point((x - 1, 9 + s), fill=DIENTE)
    else:
        d.rectangle((36, 4 + s, 42, 8 + s), fill=HOCICO)
        d.rectangle((41, 4 + s, 42, 5 + s), fill=NARIZ)
        d.line((37, 8 + s, 40, 8 + s), fill=(60, 50, 46, 255))

    # Oreja caida (mas oscura)
    d.polygon([(30, 1 + s), (34, 0 + s), (33, 7 + s), (30, 6 + s)], fill=OREJA)

    # Ojo
    d.rectangle((35, 3 + s, 36, 4 + s), fill=OJO)
    d.point((35, 3 + s), fill=BRILLO)

    # Patas del lado de cerca (arriba de todo)
    _pierna(d, cadera, patas[1], 11, PELO)
    _pierna(d, hombro, patas[3], 11, PELO)

    return _con_borde(img)


def _con_borde(img):
    """Agrega un borde oscuro de 1 pixel alrededor del dibujo."""

    ancho, alto = img.size
    lleno = [[img.getpixel((x, y))[3] > 0 for x in range(ancho)] for y in range(alto)]
    salida = img.copy()

    for y in range(alto):
        for x in range(ancho):
            if lleno[y][x]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < ancho and 0 <= ny < alto and lleno[ny][nx]:
                    salida.putpixel((x, y), BORDE)
                    break

    return salida


def _cara():
    """Cara de frente, para el mapa (igual que la foto: orejas caidas)."""

    img = Image.new("RGBA", (17, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.ellipse((2, 1, 14, 14), fill=PELO)
    d.ellipse((4, 1, 12, 6), fill=PELO_CLARO)
    # Orejas caidas a los costados
    d.polygon([(2, 2), (5, 1), (4, 9), (1, 8)], fill=OREJA)
    d.polygon([(14, 2), (11, 1), (12, 9), (15, 8)], fill=OREJA)
    # Ojos
    for x in (5, 10):
        d.rectangle((x, 6, x + 1, 7), fill=OJO)
        d.point((x, 6), fill=BRILLO)
    # Hocico negro y nariz
    d.ellipse((5, 9, 11, 14), fill=HOCICO)
    d.rectangle((7, 9, 9, 10), fill=NARIZ)
    d.point((8, 13), fill=(80, 60, 60, 255))
    # Mejillas un poco mas oscuras
    d.point((4, 10), fill=PELO_OSCURO)
    d.point((12, 10), fill=PELO_OSCURO)

    return _con_borde(img)


POSES = {
    "parado": dict(patas=(4, -4, 4, -4), cola=60),
    "correr_1": dict(patas=(-55, -40, 55, 40), salto=2, cola=10),
    "correr_2": dict(patas=(-20, -5, 25, 10), salto=1, cola=20),
    "correr_3": dict(patas=(25, 15, -20, -10), salto=0, cola=30),
    "correr_4": dict(patas=(10, -10, -5, 15), salto=1, cola=20),
    "morder": dict(patas=(-60, -45, 60, 50), salto=3, boca_abierta=True, cola=0),
}


def main():

    os.makedirs(DESTINO, exist_ok=True)

    for nombre, pose in POSES.items():
        _perro(**pose).save(os.path.join(DESTINO, nombre + ".png"))

    _cara().save(os.path.join(DESTINO, "cara.png"))

    print("Guardado en", DESTINO)


if __name__ == "__main__":
    main()

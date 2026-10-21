"""
Animaciones de los personajes HISTORICOS.

De cada historico solo hay una imagen: la pose quieta (16 x 27), que es
`assets/personajes/<NOMBRE>/historico/final.png`. Este script arma el resto
de las poses cortando ese dibujo en partes (cabeza, torso, brazos y piernas)
y moviendolas, asi se mantiene el dibujo original pixel por pixel:

    frame_1.png / frame_2.png / frame_3.png   caminar (35 x 35)
    saltando.png                              salto   (35 x 35)
    agachado.png                              agachado (24 x 30)
    cabeza.png                                cara para la barra de vidas (16 x 14)
    frente.png                                pantalla de seleccion (30 x 32)

Los tamanos de los lienzos son los mismos que los de los personajes
normales, asi el juego los trata igual (misma caja de choque).

Si quedan ganas de redibujar alguna pose a mano, alcanza con reemplazar el
PNG: por defecto el script NO pisa los archivos que ya existen.

Uso (hace falta `pip install pillow numpy`):

    python herramientas/generar_historicos.py            # solo los que faltan
    python herramientas/generar_historicos.py --forzar   # rehace todos
    python herramientas/generar_historicos.py BENJA      # solo un personaje
    python herramientas/generar_historicos.py --vista    # + hoja de vista previa
"""

import os
import sys

import numpy as np
from PIL import Image


CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PERSONAJES = ["BAUTO", "BENJA", "CASTRO", "POSHO", "THIAGO"]

# ----------------------------------------------------------
# PARTES DEL DIBUJO ORIGINAL (16 x 27)
# ----------------------------------------------------------

ALTO, ANCHO = 27, 16

FILA_CABEZA_FIN = 15     # filas 0..14: pelo, cara y cuello
FILA_TORSO_FIN = 23      # filas 15..22: torso y brazos
                         # filas 23..26: piernas y zapatos

COL_PIERNAS = 7          # piernas: izquierda 0..6, derecha 7..15
COL_BRAZO_IZQ = 5        # brazo izquierdo: columnas 0..4
COL_BRAZO_DER = 11       # brazo derecho: columnas 11..15
FILA_BRAZOS = 17         # los brazos arrancan en esta fila


# ----------------------------------------------------------
# UTILIDADES
# ----------------------------------------------------------

def vacio(alto, ancho):

    return np.zeros((alto, ancho, 4), dtype=np.uint8)


def pegar(destino, origen, y, x):
    """Pega `origen` en `destino` desde (y, x); lo transparente no tapa."""

    for fy in range(origen.shape[0]):

        for fx in range(origen.shape[1]):

            if origen[fy, fx, 3] == 0:
                continue

            dy, dx = y + fy, x + fx

            if 0 <= dy < destino.shape[0] and 0 <= dx < destino.shape[1]:
                destino[dy, dx] = origen[fy, fx]


def recorte(img, f0, f1, c0, c1):
    """Copia de img[f0:f1, c0:c1] (el resto queda transparente)."""

    parte = vacio(*img.shape[:2])

    parte[f0:f1, c0:c1] = img[f0:f1, c0:c1]

    return parte


# ----------------------------------------------------------
# ARMADO DE UNA POSE
# ----------------------------------------------------------

FILA_CINTURA = 20        # fila del torso que se repite / se saca para
                         # estirar o agachar el cuerpo

ALTO_PIERNAS = ALTO - FILA_TORSO_FIN


def armar_pose(
    idle,
    *,
    cuerpo=0,           # +1 agacha el cuerpo, -1 lo estira
    piernas=((0, 0), (0, 0)),   # (dx, dy) de la pierna izquierda y la derecha
    brazos=(0, 0),      # dy del brazo izquierdo y del derecho (- = arriba)
    brazos_x=(0, 0),    # dx del brazo izquierdo y del derecho
    cabeza_dx=0,
    quitar_filas=(),    # filas del torso que se eliminan (agacharse)
    margen=6
):
    """
    Devuelve la pose en un lienzo de (ALTO + 8) x (ANCHO + 2 * margen),
    con el cuerpo quieto en el medio (para que entren las piernas abiertas
    y los brazos en alto) y los pies pegados al borde de abajo.
    """

    alto_total = ALTO + 8

    ancho_total = ANCHO + 2 * margen

    lienzo = vacio(alto_total, ancho_total)

    # ---- filas del cuerpo de arriba (cabeza + torso), ya comprimidas ----
    filas = [f for f in range(FILA_TORSO_FIN) if f not in quitar_filas]

    if cuerpo > 0 and FILA_CINTURA in filas:

        filas.remove(FILA_CINTURA)

    elif cuerpo < 0:

        filas.insert(filas.index(FILA_CINTURA), FILA_CINTURA)

    def comprimir(img):

        salida = vacio(len(filas), ANCHO)

        for nueva, vieja in enumerate(filas):

            salida[nueva] = img[vieja]

        return salida

    # ---- capas del cuerpo ----
    capa_cabeza = comprimir(recorte(idle, 0, FILA_CABEZA_FIN, 0, ANCHO))

    torso = recorte(idle, FILA_CABEZA_FIN, FILA_TORSO_FIN, COL_BRAZO_IZQ, COL_BRAZO_DER)

    hombros = recorte(idle, FILA_CABEZA_FIN, FILA_BRAZOS, 0, ANCHO)

    capa_torso = comprimir(np.where(hombros[:, :, 3:4] > 0, hombros, torso))

    capa_brazo_izq = comprimir(recorte(idle, FILA_BRAZOS, FILA_TORSO_FIN, 0, COL_BRAZO_IZQ))

    capa_brazo_der = comprimir(recorte(idle, FILA_BRAZOS, FILA_TORSO_FIN, COL_BRAZO_DER, ANCHO))

    # ---- piernas (van atras de todo) ----
    y_piernas = alto_total - ALTO_PIERNAS

    for desde, hasta, (dx, dy) in (
        (0, COL_PIERNAS, piernas[0]),
        (COL_PIERNAS, ANCHO, piernas[1])
    ):

        pierna = recorte(idle, FILA_TORSO_FIN, ALTO, desde, hasta)[FILA_TORSO_FIN:ALTO]

        pegar(lienzo, pierna, y_piernas + dy, margen + dx)

    # ---- cuerpo: torso, cabeza y despues los brazos ----
    y_cuerpo = y_piernas - len(filas)

    pegar(lienzo, capa_torso, y_cuerpo, margen)

    pegar(lienzo, capa_cabeza, y_cuerpo, margen + cabeza_dx)

    pegar(lienzo, capa_brazo_izq, y_cuerpo + brazos[0], margen + brazos_x[0])

    pegar(lienzo, capa_brazo_der, y_cuerpo + brazos[1], margen + brazos_x[1])

    return lienzo


def poner_en_lienzo(pose, ancho, alto, borde_abajo, margen=6):
    """Centra la pose en un lienzo (ancho x alto) con los pies abajo."""

    lienzo = vacio(alto, ancho)

    x0 = (ancho - ANCHO) // 2 - margen

    y0 = alto - borde_abajo - pose.shape[0]

    pegar(lienzo, pose, y0, x0)

    return lienzo


# ----------------------------------------------------------
# LAS POSES
# ----------------------------------------------------------

def generar(idle):
    """Devuelve {nombre_de_archivo: imagen} con todas las poses."""

    poses = {}

    # --- caminar ---
    # 1: apoya la pierna izquierda, brazo izquierdo atras
    caminar_1 = armar_pose(
        idle,
        cuerpo=1,
        piernas=((-2, 0), (2, -1)),
        brazos=(1, -1),
        brazos_x=(0, 0),
        cabeza_dx=1
    )

    # 2: paso intermedio, cuerpo estirado y piernas juntas
    caminar_2 = armar_pose(
        idle,
        cuerpo=-1,
        piernas=((1, -1), (-1, 0)),
        brazos=(0, 0)
    )

    # 3: apoya la pierna derecha, brazos al reves
    caminar_3 = armar_pose(
        idle,
        cuerpo=1,
        piernas=((-2, -1), (2, 0)),
        brazos=(-1, 1),
        brazos_x=(0, 0),
        cabeza_dx=1
    )

    poses["frame_1.png"] = poner_en_lienzo(caminar_1, 35, 35, 0)
    poses["frame_2.png"] = poner_en_lienzo(caminar_2, 35, 35, 0)
    poses["frame_3.png"] = poner_en_lienzo(caminar_3, 35, 35, 0)

    # --- salto: cuerpo estirado, piernas recogidas, brazos en alto ---
    saltando = armar_pose(
        idle,
        cuerpo=-1,
        piernas=((-2, -2), (3, -1)),
        brazos=(-3, -5),
        brazos_x=(-1, 1)
    )

    poses["saltando.png"] = poner_en_lienzo(saltando, 35, 35, 2)

    # --- agachado: se sacan 4 filas del cuerpo, brazos y piernas abiertos ---
    agachado = armar_pose(
        idle,
        piernas=((-1, 0), (1, 0)),
        brazos=(0, 0),
        brazos_x=(-1, 1),
        quitar_filas=(16, 18, 20, 22)
    )

    poses["agachado.png"] = poner_en_lienzo(agachado, 24, 30, 0)

    # --- cabeza: las primeras 14 filas del dibujo original ---
    poses["cabeza.png"] = idle[0:14, 0:ANCHO].copy()

    # --- frente: el dibujo quieto en el lienzo de 30 x 32 ---
    frente = vacio(32, 30)

    pegar(frente, idle, 32 - ALTO, (30 - ANCHO) // 2)

    poses["frente.png"] = frente

    return poses


# ----------------------------------------------------------
# PRINCIPAL
# ----------------------------------------------------------

def hoja_de_vista_previa(carpeta_salida):
    """Una imagen con todas las poses de cada historico (ampliadas)."""

    escala = 6

    nombres = [
        "final.png", "frame_1.png", "frame_2.png", "frame_3.png",
        "saltando.png", "agachado.png", "cabeza.png", "frente.png"
    ]

    filas = []

    for personaje in PERSONAJES:

        carpeta = os.path.join(CARPETA, "assets", "personajes", personaje, "historico")

        imgs = [
            Image.open(os.path.join(carpeta, n)).convert("RGBA") for n in nombres
        ]

        ancho = sum(i.width * escala + 10 for i in imgs) + 10
        alto = max(i.height for i in imgs) * escala + 20

        fila = Image.new("RGBA", (ancho, alto), (237, 237, 237, 255))

        x = 10

        for i in imgs:

            grande = i.resize((i.width * escala, i.height * escala), Image.NEAREST)

            fila.alpha_composite(grande, (x, alto - 10 - grande.height))

            x += grande.width + 10

        filas.append(fila)

    hoja = Image.new(
        "RGBA",
        (max(f.width for f in filas), sum(f.height for f in filas)),
        (237, 237, 237, 255)
    )

    y = 0

    for f in filas:

        hoja.alpha_composite(f, (0, y))

        y += f.height

    ruta = os.path.join(carpeta_salida, "historicos_vista_previa.png")

    hoja.save(ruta)

    return ruta


def main(argumentos):

    forzar = "--forzar" in argumentos

    vista = "--vista" in argumentos

    elegidos = [a.upper() for a in argumentos if not a.startswith("--")]

    for personaje in PERSONAJES:

        if elegidos and personaje not in elegidos:
            continue

        carpeta = os.path.join(
            CARPETA, "assets", "personajes", personaje, "historico"
        )

        ruta_idle = os.path.join(carpeta, "final.png")

        idle = np.array(Image.open(ruta_idle).convert("RGBA"))

        assert idle.shape[:2] == (ALTO, ANCHO), (
            personaje + ": final.png tiene que medir 16 x 27"
        )

        for nombre, pose in generar(idle).items():

            ruta = os.path.join(carpeta, nombre)

            if os.path.exists(ruta) and not forzar:
                continue

            Image.fromarray(pose, "RGBA").save(ruta)

            print("  ", personaje, nombre)

    if vista:

        salida = os.path.join(CARPETA, "herramientas", "vistas")

        os.makedirs(salida, exist_ok=True)

        print("vista previa:", hoja_de_vista_previa(salida))


if __name__ == "__main__":

    main(sys.argv[1:])

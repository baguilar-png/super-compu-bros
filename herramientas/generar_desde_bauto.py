"""
Arma todos los sprites de IKI y de los personajes HISTORICOS usando como
molde las poses de BAUTO (assets/personajes/BAUTO/bauto *.png), pero
respetando como es cada uno (su pelo, su cara y su ropa):

    final.png        quieto: el dibujo original del personaje, tal cual
    frame_1/2/3.png  caminar: el cuerpo de Bauto con la CABEZA del dibujo
    saltando.png     original (pelo y cara pixel por pixel) y la ropa con
    agachado.png     los colores que el personaje tiene en ese mismo lugar
    frente.png       de frente: la cara de frente de Bauto con el peinado
    cabeza.png       del personaje (su pelo, hecho simetrico) y su ropa

Como todos los dibujos (Bauto incluido) estan hechos sobre el mismo molde
de 16 x 27, cada pixel de Bauto se corresponde con el mismo pixel del otro
personaje: asi se sabe de que color es la remera, el saco, la bufanda, etc.

Dibujos de partida (todo tiene que quedar mirando a la DERECHA, como Bauto):
    historicos: assets/personajes/<NOMBRE>/historico/original/final.png
                (ya miran a la derecha: se usan tal cual)
    Iki:        assets/personajes/IKI/iki frente.png (mira a la izquierda:
                se da vuelta)

Se guardan en:
    assets/personajes/IKI/
    assets/personajes/<NOMBRE>/historico/

Uso, desde la carpeta del juego (hace falta numpy y pillow):

    python herramientas/generar_desde_bauto.py
"""

import os
from collections import Counter, defaultdict

import numpy as np
from PIL import Image

CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSONAJES = os.path.join(CARPETA, "assets", "personajes")

HISTORICOS = ["BAUTO", "BENJA", "CASTRO", "POSHO", "THIAGO"]

# Poses de costado: molde de Bauto -> archivo de salida
POSES_COSTADO = {
    "bauto frame 1.png": "frame_1.png",
    "bauto frame 2.png": "frame_2.png",
    "bauto frame 3.png": "frame_3.png",
    "bauto saltando.png": "saltando.png",
    "bauto agachado.png": "agachado.png",
}

FILAS_CABEZA = 14           # filas 0..13 del dibujo de 16 x 27: pelo y cara

# La cabeza de frente de Bauto (bauto cabeza.png) esta en su sprite de
# frente en esta posicion
CABEZA_EN_FRENTE = (7, 4)

PELO_BAUTO = [(148, 116, 59), (120, 93, 46)]

# Colores de Bauto agrupados (para cuando un color no aparece en su
# dibujo quieto pero si en otra pose)
GRUPOS_BAUTO = {
    "borde": [(0, 0, 0), (40, 40, 40), (28, 28, 28), (41, 38, 41), (39, 39, 39), (41, 41, 41)],
    "pelo": PELO_BAUTO,
    "piel": [(242, 210, 155), (245, 219, 176), (245, 199, 135), (237, 201, 135)],
    "blanco": [(255, 255, 255)],
    "remera": [(237, 232, 208), (219, 216, 197)],
    "franja": [(184, 33, 63), (199, 46, 76), (173, 0, 35)],
    "pantalon": [(62, 65, 66), (43, 45, 45), (29, 31, 31)],
    "zapatilla": [(10, 69, 1), (40, 87, 24), (23, 56, 12), (10, 61, 22)],
}
GRUPO_DE = {c: g for g, colores in GRUPOS_BAUTO.items() for c in colores}

# Logo de la remera de Iki (en el pecho de las poses nuevas)
LOGO_IKI = [("a", "n"), ("m", "n")]
COLORES_LOGO = {"a": (64, 177, 214), "m": (220, 75, 60), "n": (189, 87, 36)}


# ----------------------------------------------------------
# AYUDAS
# ----------------------------------------------------------

def abrir(ruta, dar_vuelta=False):

    img = Image.open(ruta).convert("RGBA")

    if dar_vuelta:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

    return np.array(img)


def color(a, y, x):
    return tuple(int(v) for v in a[y, x, :3])


def buscar_cabeza(pose, cabeza):
    """Donde esta la cabeza de Bauto dentro de una pose (dx, dy)."""

    alto, ancho = pose.shape[:2]
    mascara = cabeza[:, :, 3] > 0
    mejor = (-1, (0, 0))

    for dy in range(-3, alto - 6):
        for dx in range(-3, ancho - 6):
            total = iguales = 0
            for y, x in zip(*np.nonzero(mascara)):
                total += 1
                yy, xx = y + dy, x + dx
                if 0 <= yy < alto and 0 <= xx < ancho and pose[yy, xx, 3] and \
                        color(pose, yy, xx) == color(cabeza, y, x):
                    iguales += 1
            if iguales / total > mejor[0]:
                mejor = (iguales / total, (dx, dy))

    return mejor[1]


def armar_tabla(bauto, otro, filas):
    """
    Que color tiene el otro personaje donde Bauto tiene cada color.
    Devuelve (por_color, por_grupo).
    """

    por_color = defaultdict(Counter)
    por_grupo = defaultdict(Counter)

    for y in filas:
        for x in range(bauto.shape[1]):
            if bauto[y, x, 3] and otro[y, x, 3]:
                cb, co = color(bauto, y, x), color(otro, y, x)
                por_color[cb][co] += 1
                por_grupo[GRUPO_DE.get(cb, "?")][co] += 1

    return (
        {c: cnt.most_common(1)[0][0] for c, cnt in por_color.items()},
        {g: cnt.most_common(1)[0][0] for g, cnt in por_grupo.items()},
    )


def _lum(c):
    return c[0] * 0.3 + c[1] * 0.59 + c[2] * 0.11


def piel_de(otro):
    """
    (principal, clara, sombra) de la piel del personaje: los colores claros
    de la cara (filas 4 a 13 del dibujo).
    """

    cuenta = Counter()
    for y in range(4, FILAS_CABEZA):
        for x in range(otro.shape[1]):
            if otro[y, x, 3]:
                c = color(otro, y, x)
                if 110 < _lum(c) < 235:
                    cuenta[c] += 1

    colores = [c for c, n in cuenta.most_common() if n >= 2] or [(200, 170, 130)]
    principal = colores[0]
    clara = max(colores, key=_lum)
    sombra = min(colores, key=_lum)

    return principal, clara, sombra


def fijar_piel_y_borde(tablas, otro):
    """
    La piel y el borde no se copian por posicion (donde Bauto tiene frente
    otro puede tener flequillo, donde Bauto tiene brazo otro tiene manga):
    se usan los de la cara del personaje.
    """

    por_color, por_grupo = tablas
    principal, clara, sombra = piel_de(otro)

    por_color[(242, 210, 155)] = principal
    por_color[(245, 219, 176)] = clara
    por_color[(245, 199, 135)] = sombra
    por_color[(237, 201, 135)] = sombra
    por_grupo["piel"] = principal

    for c in GRUPOS_BAUTO["borde"]:
        por_color[c] = (40, 40, 40)
    por_grupo["borde"] = (40, 40, 40)

    por_color[(255, 255, 255)] = (255, 255, 255)
    por_grupo["blanco"] = (255, 255, 255)

    return por_color, por_grupo


def zapato_de(otro):
    """Color de los zapatos del personaje (las 2 filas de abajo del dibujo)."""

    cuenta = Counter()
    for y in range(otro.shape[0] - 2, otro.shape[0]):
        for x in range(otro.shape[1]):
            if otro[y, x, 3] and color(otro, y, x) != (40, 40, 40):
                cuenta[color(otro, y, x)] += 1

    return cuenta.most_common(1)[0][0] if cuenta else (255, 255, 255)


def pintar_zapatos(img, molde, zapato):
    """Lo blanco de abajo del molde (las zapatillas de Bauto) va del color
    de los zapatos del personaje; lo blanco de arriba son los ojos."""

    caja = np.nonzero(molde[:, :, 3] > 0)
    if len(caja[0]) == 0:
        return img
    arriba, abajo = caja[0].min(), caja[0].max()
    limite = arriba + (abajo - arriba) * 0.45     # los ojos estan mas arriba

    for y, x in zip(*np.nonzero(molde[:, :, 3] > 0)):
        if y >= limite and color(molde, y, x) == (255, 255, 255) and img[y, x, 3]:
            img[y, x, :3] = zapato

    return img


def recolorear(img, tablas, saltear=None):
    """Cambia cada color de Bauto por el del otro personaje."""

    por_color, por_grupo = tablas[0], tablas[1]
    salida = img.copy()

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if not img[y, x, 3] or (saltear is not None and saltear[y, x]):
                continue
            c = color(img, y, x)
            nuevo = por_color.get(c) or por_grupo.get(GRUPO_DE.get(c, "?"))
            if nuevo is not None:
                salida[y, x, :3] = nuevo

    return salida


def poner_logo(img, bauto):
    """Logo de Iki en el medio de donde Bauto tiene la franja."""

    franja = [
        (x, y)
        for y in range(bauto.shape[0])
        for x in range(bauto.shape[1])
        if bauto[y, x, 3] and GRUPO_DE.get(color(bauto, y, x)) == "franja"
    ]

    if len(franja) < 4:
        return img

    cx = round(sum(p[0] for p in franja) / len(franja))
    cy = round(sum(p[1] for p in franja) / len(franja))

    for fy, fila in enumerate(LOGO_IKI):
        for fx, letra in enumerate(fila):
            x, y = cx - 1 + fx, cy - 1 + fy
            if 0 <= y < img.shape[0] and 0 <= x < img.shape[1] and img[y, x, 3]:
                img[y, x, :3] = COLORES_LOGO[letra]

    return img


# ----------------------------------------------------------
# POSES DE COSTADO: cuerpo de Bauto + cabeza del personaje
# ----------------------------------------------------------

def pose_costado(pose, cabeza_bauto, cabeza_otro, tablas_cuerpo, es_iki):

    dx, dy = buscar_cabeza(pose, cabeza_bauto)
    alto, ancho = pose.shape[:2]

    # Que pixeles de la pose son la cabeza de Bauto
    es_cabeza = np.zeros((alto, ancho), dtype=bool)
    for y, x in zip(*np.nonzero(cabeza_bauto[:, :, 3] > 0)):
        yy, xx = y + dy, x + dx
        if 0 <= yy < alto and 0 <= xx < ancho and pose[yy, xx, 3] and \
                color(pose, yy, xx) == color(cabeza_bauto, y, x):
            es_cabeza[yy, xx] = True

    salida = recolorear(pose, tablas_cuerpo, saltear=es_cabeza)
    salida = pintar_zapatos(salida, pose, tablas_cuerpo[2])

    if es_iki:
        salida = poner_logo(salida, pose)

    # Se saca la cabeza de Bauto y se pone la del personaje
    salida[es_cabeza] = 0
    for y, x in zip(*np.nonzero(cabeza_otro[:, :, 3] > 0)):
        yy, xx = y + dy, x + dx
        if 0 <= yy < alto and 0 <= xx < ancho:
            salida[yy, xx] = cabeza_otro[y, x]

    return salida


# ----------------------------------------------------------
# DE FRENTE: cara de Bauto + peinado del personaje (simetrico)
# ----------------------------------------------------------

def cabeza_de_frente(cabeza_frente_bauto, bauto_quieto, otro, tablas_cabeza):
    """
    Devuelve la cabeza de frente (18 x 16: la de Bauto con un pixel de
    margen) con el pelo del otro personaje.
    """

    alto, ancho = cabeza_frente_bauto.shape[:2]          # 14 x 16
    base = np.zeros((alto + 2, ancho + 2, 4), dtype=np.uint8)
    base[1:-1, 1:-1] = recolorear(cabeza_frente_bauto, tablas_cabeza)

    borde = tuple(tablas_cabeza[1].get("borde", (40, 40, 40)))

    # Se saca el pelo de Bauto (y su borde de arriba)
    for y in range(alto):
        for x in range(ancho):
            if cabeza_frente_bauto[y, x, 3] and color(cabeza_frente_bauto, y, x) in PELO_BAUTO:
                base[y + 1, x + 1] = 0

    # Colores de pelo del otro: los que tiene donde Bauto tiene pelo
    colores_pelo = Counter()
    for y in range(FILAS_CABEZA):
        for x in range(otro.shape[1]):
            if bauto_quieto[y, x, 3] and otro[y, x, 3] and color(bauto_quieto, y, x) in PELO_BAUTO:
                colores_pelo[color(otro, y, x)] += 1
    piel = set(piel_de(otro))
    pelo = {
        c for c, n in colores_pelo.items()
        if n >= 2 and c != (40, 40, 40) and c not in piel and _lum(c) <= 200
    }

    # Mascara del pelo del otro (de costado) centrada y hecha simetrica
    mascara = np.zeros((FILAS_CABEZA, otro.shape[1]), dtype=bool)
    for y in range(FILAS_CABEZA):
        for x in range(otro.shape[1]):
            if otro[y, x, 3] and color(otro, y, x) in pelo:
                mascara[y, x] = True

    columnas = np.nonzero(mascara.any(axis=0))[0]
    if len(columnas) == 0:
        return base

    corrimiento = round((ancho - 1) / 2 - (columnas[0] + columnas[-1]) / 2)

    ancho_b = ancho + 2
    simetrica = np.zeros((alto + 2, ancho_b), dtype=bool)
    color_en = {}
    for y, x in zip(*np.nonzero(mascara)):
        for xx in (x + corrimiento + 1, ancho_b - 1 - (x + corrimiento + 1)):
            if 0 <= xx < ancho_b and y + 1 < alto + 2:
                simetrica[y + 1, xx] = True
                color_en.setdefault((y + 1, xx), color(otro, y, x))

    # El pelo no tapa los ojos ni la boca: de la fila 8 para abajo solo
    # en los costados (patillas)
    for y in range(alto + 2):
        for x in range(ancho_b):
            if simetrica[y, x] and y >= 8 and 3 <= x <= ancho_b - 4:
                simetrica[y, x] = False

    for y, x in zip(*np.nonzero(simetrica)):
        base[y, x, :3] = color_en[(y, x)]
        base[y, x, 3] = 255

    # Borde nuevo: se sacan los bordes viejos que quedaron sueltos y se
    # rodea todo con un pixel de borde
    lleno = (base[:, :, 3] > 0)
    es_borde = np.zeros_like(lleno)
    for y, x in zip(*np.nonzero(lleno)):
        if color(base, y, x) == borde:
            es_borde[y, x] = True

    for y, x in zip(*np.nonzero(es_borde)):
        vecinos = [
            (y + a, x + b) for a in (-1, 0, 1) for b in (-1, 0, 1)
            if (a or b) and 0 <= y + a < base.shape[0] and 0 <= x + b < base.shape[1]
        ]
        if not any(lleno[v] and not es_borde[v] for v in vecinos):
            base[y, x] = 0

    lleno = (base[:, :, 3] > 0) & ~((base[:, :, 3] > 0) & es_borde)
    for y in range(base.shape[0]):
        for x in range(base.shape[1]):
            if base[y, x, 3]:
                continue
            for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 <= y + a < base.shape[0] and 0 <= x + b < base.shape[1] and lleno[y + a, x + b]:
                    base[y, x, :3] = borde
                    base[y, x, 3] = 255
                    break

    return base


def frente(frente_bauto, cabeza_nueva, tablas_cuerpo, es_iki):

    cx, cy = CABEZA_EN_FRENTE
    alto_c, ancho_c = cabeza_nueva.shape[0] - 2, cabeza_nueva.shape[1] - 2

    salida = recolorear(frente_bauto, tablas_cuerpo)
    salida = pintar_zapatos(salida, frente_bauto, tablas_cuerpo[2])

    if es_iki:
        salida = poner_logo(salida, frente_bauto)

    # Se borra la cabeza de Bauto y se pega la nueva (con su margen)
    salida[cy:cy + alto_c, cx:cx + ancho_c] = 0
    for y, x in zip(*np.nonzero(cabeza_nueva[:, :, 3] > 0)):
        yy, xx = cy - 1 + y, cx - 1 + x
        if 0 <= yy < salida.shape[0] and 0 <= xx < salida.shape[1]:
            salida[yy, xx] = cabeza_nueva[y, x]

    return salida


# ----------------------------------------------------------
# PRINCIPAL
# ----------------------------------------------------------

def armar(nombre, quieto_otro, carpeta, es_iki):

    bauto_quieto = abrir(os.path.join(PERSONAJES, "BAUTO", "bauto final.png"))
    cabeza_bauto = bauto_quieto[:FILAS_CABEZA]
    cabeza_otro = quieto_otro[:FILAS_CABEZA]

    tablas_cuerpo = armar_tabla(bauto_quieto, quieto_otro, range(FILAS_CABEZA, bauto_quieto.shape[0]))
    tablas_cabeza = armar_tabla(bauto_quieto, quieto_otro, range(0, FILAS_CABEZA))

    # Manos y cara con la piel del personaje; el borde siempre el mismo
    fijar_piel_y_borde(tablas_cuerpo, quieto_otro)
    fijar_piel_y_borde(tablas_cabeza, quieto_otro)

    # Tercer dato: el color de los zapatos
    tablas_cuerpo = tablas_cuerpo + (zapato_de(quieto_otro),)

    os.makedirs(carpeta, exist_ok=True)

    def guardar(img, archivo):
        Image.fromarray(img.astype(np.uint8), "RGBA").save(os.path.join(carpeta, archivo))

    guardar(quieto_otro, "final.png")

    for molde, archivo in POSES_COSTADO.items():
        pose = abrir(os.path.join(PERSONAJES, "BAUTO", molde))
        guardar(pose_costado(pose, cabeza_bauto, cabeza_otro, tablas_cuerpo, es_iki), archivo)

    cabeza_frente_bauto = abrir(os.path.join(PERSONAJES, "BAUTO", "bauto cabeza.png"))
    cabeza_nueva = cabeza_de_frente(cabeza_frente_bauto, bauto_quieto, quieto_otro, tablas_cabeza)

    guardar(cabeza_nueva, "cabeza.png")

    frente_bauto = abrir(os.path.join(PERSONAJES, "BAUTO", "bauto frente.png"))
    guardar(frente(frente_bauto, cabeza_nueva, tablas_cuerpo, es_iki), "frente.png")

    print("  listo:", nombre)


def main():

    armar(
        "IKI",
        abrir(os.path.join(PERSONAJES, "IKI", "iki frente.png"), dar_vuelta=True),
        os.path.join(PERSONAJES, "IKI"),
        True,
    )

    for nombre in HISTORICOS:
        armar(
            nombre + " HISTORICO",
            abrir(os.path.join(PERSONAJES, nombre, "historico", "original", "final.png")),
            os.path.join(PERSONAJES, nombre, "historico"),
            False,
        )


if __name__ == "__main__":
    main()

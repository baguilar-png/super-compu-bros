"""
Genera los niveles de TRES PISOS apilados:

    la calle     abajo de todo, por donde empieza el nivel (vereda, cordon
                 y asfalto), libre de punta a punta. Hay escaleras de mano
                 que suben a los techos.
    los techos   una fila de edificios (chicos, medianos y grandes) con
                 balcones. Se baja a la calle por las mismas escaleras.
    el cielo     nubes (las genera el juego al azar, ver terreno.py) y,
                 cuanto mas arriba, mas negro (lo dibuja fondos_nivel.py).

A lo lejos se ven los monumentos del barrio.

Los niveles de JEFE (15 y 30, "jefe": True en niveles_config.py) son una
arena corta: nada mas que la calle, ANCHO_ARENA px de ancho. Se arma igual
que los demas (mismos edificios de fondo) y al final se recorta el terreno;
ver recortar_arena().

Para cada nivel produce, en assets/niveles/:

    nivel_NN_cielo.png     cielo, astros y nubes             (casi quieto)
    nivel_NN_lejos.png     ciudad lejana + monumentos         (se mueve lento)
    nivel_NN_medio.png     edificios del medio                (se mueve medio)
    nivel_NN_ciudad.png    la calle, los edificios y los techos por donde se
                           camina (3200 x 312, pegado al nivel)
    nivel_NN_terreno.json  donde esta cada techo, balcon y escalera
                           (lo lee terreno.py para las colisiones)
    nivel_NN_efectos.json  lo que el juego anima en vivo: destellos del sol
                           (dia), luz de las farolas y balizas (noche)

Cada nivel es de DIA (sol: reflejos en los vidrios, brillo en la calle,
destellos y rayos) o de NOCHE (luna, ventanas prendidas, postes de luz,
carteles de neon y luces rojas de aviso). Ver efectos_luz.py y la clave
"noche" de niveles_config.py.

El dibujo y los datos de colision salen del mismo calculo, asi que nunca se
desacomodan. Un pixel de dibujo = 3 pixeles de pantalla (el nivel mide 9600).

Alturas de donde se pisa (en pixeles del mundo):

    calle             804  (fila 268 del dibujo)
    edificio chico    480  (fila 160)
    edificio mediano  372  (fila 124)
    edificio grande   264  (fila  88)
    nubes             de 156 para arriba

Cada escalon son 108 px, menos de lo que llega un salto (160). Cuando un
edificio grande tiene al lado uno chico (dos escalones), sale de su pared
un BALCON a media altura que sirve de escalon.

Uso (desde la carpeta del juego):

    python herramientas/generar_techos.py            # los 30 niveles
    python herramientas/generar_techos.py 1 4 12     # solo esos
    python herramientas/generar_techos.py --vista    # + vistas en herramientas/vistas/

Necesita Pillow y numpy.
"""

import json
import math
import os
import random
import sys

HERRAMIENTAS = os.path.dirname(os.path.abspath(__file__))

CARPETA_JUEGO = os.path.dirname(HERRAMIENTAS)

for ruta in (HERRAMIENTAS, CARPETA_JUEGO):
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

from pixelart import *  # noqa: E402,F401,F403
import edificios as E  # noqa: E402
import monumentos  # noqa: E402
import generar_niveles as G  # noqa: E402
import efectos_luz as L  # noqa: E402
import interior_huergo as IH  # noqa: E402
import huergo_real as HR  # noqa: E402
from niveles_config import NIVELES  # noqa: E402
from terreno import Terreno, ANCHO_ARENA  # noqa: E402

CARPETA_NIVELES = os.path.join(CARPETA_JUEGO, "assets", "niveles")

# ----------------------------------------------------------
# Medidas
# ----------------------------------------------------------

ANCHO = 3200                    # dibujo del nivel (9600 px de pantalla)
ALTO = 200                      # alto de las capas lejanas (cielo, lejos, medio)

# La capa cercana es mas alta: llega hasta abajo de la calle
ALTO_CERCANA = 312
FILA_CALLE = 268                # fila donde se pisa en la calle (804 px)
FILA_FACHADA = 258              # hasta aca llegan las fachadas; abajo, la vereda

NIVEL_PX = ANCHO * PX           # 9600

PANTALLA = 800 / PX             # 266.67: ancho de pantalla en pixeles de dibujo

# Fila del dibujo donde esta la superficie de cada altura de techo
FILAS_TECHO = (160, 124, 88)

# Lo mismo en pixeles de pantalla (tiene que coincidir con terreno.TECHOS)
TECHOS_Y = tuple(f * PX for f in FILAS_TECHO)

LOSA = 3                        # filas del borde del techo (arriba de la fachada)

# Escaleras de mano (en pixeles de dibujo)
ESCALERA_ANCHO = 12             # 36 px de pantalla

# Donde van las escaleras de subida y de bajada (x de pantalla, mas o menos)
ESCALERAS_X = (1700, 3700, 4700, 6300, 7300, 8700)
ESCALERAS_SEP_TECHOS = 900     # de la que sube a la que baja (tramo de techos)
ESCALERAS_SEP_CALLE = 600       # de la que baja a la que sube (tramo de calle)
ESCALERA_CASTIGO_TIER = 350     # px de "desvio" por cada altura de techo mas
ESCALERA_X_MIN = 1000           # la primera: despues de un tramo largo de calle
ESCALERA_X_MAX = 8800
ESCALERA_MARGEN = 150           # px: lo que se deja libre a cada lado del techo

# Cuanto se mueve cada capa respecto de la camara
PARALLAX = dict(cielo=0.06, lejos=0.22, medio=0.50)

# Balcones
BALCON_ANCHO = 36               # en pixeles de dibujo (108 de pantalla)
BALCON_FILA = FILAS_TECHO[1]    # a la altura de los techos medianos
BALCON_FILA_ALTO = 100          # el que sale sobre un techo mediano (72 px arriba)
BALCON_GROSOR = 4               # 12 px de pantalla

# Lo maximo que se sube de un salto (el salto llega a 160)
SALTO_ESCALON = 111

# Primer y ultimo edificio (chicos y anchos: ahi se arranca y se llega a
# la meta)
INICIO_ANCHO = 900              # px de pantalla
FINAL_MIN = 660

# Ancho de cada edificio segun su altura, en pixeles de dibujo
TIER_ANCHO = {0: (100, 150), 1: (110, 170), 2: (140, 210)}

# Que altura sigue a cual: (chico, mediano, grande)
TRANSICIONES = {
    0: (0.22, 0.38, 0.40),
    1: (0.28, 0.22, 0.50),
    2: (0.40, 0.30, 0.30),
}

# En que alturas puede estar cada tipo de fachada
ESTILOS_EN_TIER = {
    "casa_baja": {0},
    "conventillo": {0, 1},
    "galpon": {0, 1},
    "local": {0, 1, 2},
    "italianizante": {0, 1, 2},
    "frances": {0, 1, 2},
    "departamentos": {0, 1, 2},
    "art_deco": {0, 1, 2},
    "fabrica": {0, 1, 2},
    "mural": {0, 1},
    "torre_hormigon": {1, 2},
    "torre_vidrio": {1, 2},
}

# Si el barrio no tiene ninguno de estos en esa altura
ESTILOS_RESERVA = ["departamentos", "mural", "fabrica", "local"]

# Cuanto pesa un estilo que el barrio no pide (para que no desentone). Los
# edificios grandes son mas variados: el barrio no tiene tantos tan altos.
PESO_AJENO = {0: 0.04, 1: 0.12, 2: 0.45}

# Cosas que se ponen en las azoteas segun el barrio (peso extra)
PROPS_BARRIO = {
    "LA BOCA": {"banderin": 6},
    "LA BOMBONERA": {"banderin": 7},
    "SAN TELMO": {"ropa": 3, "planta": 2},
    "PUERTO MADERO": {"antena": 2, "aire": 2},
    "RETIRO": {"antena": 2},
    "RECOLETA": {"planta": 3},
    "BARRIO NORTE": {"planta": 2, "aire": 1},
    "PALERMO": {"planta": 6},
    "ONCE": {"ropa": 3, "antena": 2},
    "ABASTO": {"ropa": 2},
    "CONSTITUCION": {"antena": 2, "ropa": 1},
}

VIDRIO_COL = {VIDRIO, VIDRIO_LUZ, VIDRIO_OSC}


# ==========================================================
# AYUDAS
# ==========================================================

def ancho_capa(parallax, ancho_nivel=None):
    """
    Ancho de una capa (en px de dibujo) para que se mueva a esa velocidad. Los
    niveles cortos (el 1) pasan su ancho en pixeles de dibujo.
    """

    return int(round(PANTALLA + parallax * ((ancho_nivel or ANCHO) - PANTALLA)))


def es_noche(cfg):
    """Los niveles de noche tienen 'noche' (0.7 a 0.8); los de dia no."""

    return cfg.get("noche", 0) >= 0.5


def multiplicar_rgb(lienzo, factores):
    """Multiplica el color (donde hay dibujo) por un mapa de factores (alto x ancho)."""

    a = np.array(lienzo.im).astype(np.float32)

    visible = a[..., 3] > 0

    for i in range(3):
        a[..., i] = np.where(visible, a[..., i] * factores, a[..., i])

    lienzo.im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")

    lienzo.d = ImageDraw.Draw(lienzo.im)


def fila_llena(sprite, fraccion=0.92):
    """Primera fila (de arriba) que ocupa todo el ancho: ahi empieza el cuerpo."""

    a = np.array(sprite.im)[..., 3] > 0

    ancho = a.shape[1]

    for y in range(a.shape[0]):

        if a[y].sum() >= fraccion * ancho and a[y, 0] and a[y, -1]:
            return y

    return 0


def repartir(total, minimo, maximo, r):
    """Parte `total` en tramos de entre `minimo` y `maximo`."""

    tramos = []

    resto = total

    while resto > 0:

        if resto <= maximo:
            tramos.append(resto)
            break

        t = r.randint(minimo, maximo)

        # no dejar un resto demasiado chico
        if 0 < resto - t < minimo:
            t = resto - minimo

        tramos.append(t)

        resto -= t

    return tramos


# ==========================================================
# DISTRIBUCION DE LOS EDIFICIOS (el terreno)
# ==========================================================

def elegir_estilo(cfg, tier, previo, r):

    opciones = []

    for nombre, tiers in ESTILOS_EN_TIER.items():

        if tier not in tiers or nombre == previo:
            continue

        peso = cfg["estilos"].get(nombre, PESO_AJENO[tier])

        opciones.append((nombre, peso))

    # si el barrio no pide ninguno de los que entran, se usan los de reserva
    if not any(nombre in cfg["estilos"] for nombre, _ in opciones):

        opciones = [
            (nombre, 1) for nombre in ESTILOS_RESERVA
            if tier in ESTILOS_EN_TIER[nombre] and nombre != previo
        ]

    return G.elegir_pesos(opciones, r)


def armar_terreno(n, cfg):
    """
    Reparte los edificios a lo largo del nivel. Devuelve el dict que se
    guarda en nivel_NN_terreno.json (medidas en pixeles de pantalla).
    """

    r = random.Random(4000 + n)

    # [x0, x1, tier]
    lista = [[0, INICIO_ANCHO, 0]]

    x = INICIO_ANCHO

    racha = 1

    while True:

        resto = NIVEL_PX - x

        if resto <= 1000:

            lista.append([x, NIVEL_PX, 0])

            break

        previo = lista[-1][2]

        pesos = list(TRANSICIONES[previo])

        # nunca mas de dos seguidos de la misma altura
        if racha >= 2:
            pesos[previo] = 0

        # nunca grande - chico - grande (el chico quedaria como un pozo)
        if previo == 0 and len(lista) >= 2 and lista[-2][2] == 2:
            pesos[2] = 0

        tier = G.elegir_pesos(list(enumerate(pesos)), r)

        amin, amax = TIER_ANCHO[tier]

        w = r.randint(amin, amax) * PX

        w = min(w, resto - FINAL_MIN)

        if w < amin * PX:

            # no entra uno de esa altura: queda un chico, mas ancho
            tier = 0

            w = (resto - FINAL_MIN) // PX * PX

        lista.append([x, x + w, tier])

        racha = racha + 1 if tier == previo else 1

        x += w

    edificios = []

    previo_estilo = None

    for i, (x0, x1, tier) in enumerate(lista):

        # el primero y el ultimo tienen fachadas tranquilas
        estilo = elegir_estilo(cfg, tier, previo_estilo, r)

        previo_estilo = estilo

        edificios.append(dict(
            x0=x0, x1=x1, y=TECHOS_Y[tier], tier=tier, estilo=estilo
        ))

    # Balcones: todo edificio grande tiene uno del lado donde el vecino es
    # mas bajo. Si el vecino es chico (dos escalones) el balcon queda a la
    # altura de los techos medianos y es el escalon que falta; si es
    # mediano, queda un poco mas arriba (una subida corta).
    balcones = []

    for i, e in enumerate(edificios):

        if e["tier"] != 2:
            continue

        for lado, j in (("izq", i - 1), ("der", i + 1)):

            if not 0 <= j < len(edificios):
                continue

            vecino = edificios[j]["tier"]

            if vecino == 2:
                continue

            fila = BALCON_FILA if vecino == 0 else BALCON_FILA_ALTO

            if lado == "izq":
                x0, x1 = e["x0"] - BALCON_ANCHO * PX, e["x0"]
            else:
                x0, x1 = e["x1"], e["x1"] + BALCON_ANCHO * PX

            balcones.append(dict(
                x0=x0, x1=x1, y=fila * PX, lado=lado, edificio=i
            ))

    escaleras = colocar_escaleras(edificios, r)

    return dict(
        nivel=n,
        ancho=NIVEL_PX,
        edificios=edificios,
        balcones=balcones,
        escaleras=escaleras
    )


def armar_terreno_interior(n):
    """
    El terreno del nivel 1 (adentro del Huergo): un nivel corto con un solo piso.
    Hay un unico "edificio" (la pared de fondo, no se pisa: la calle esta abajo
    de todo y no hay escaleras ni balcones ni nubes) y la marca "interior".
    """

    ancho = HR.ANCHO_INTERIOR * PX

    return dict(
        nivel=n,
        ancho=ancho,
        interior=True,
        edificios=[dict(
            x0=0, x1=ancho, y=TECHOS_Y[0], tier=0, estilo="interior"
        )],
        balcones=[],
        escaleras=[]
    )


def colocar_escaleras(edificios, r):
    """
    Escaleras de mano entre la calle y los techos. La calle esta libre de
    punta a punta (no hay obras ni nada que la corte): las escaleras son un
    atajo opcional, y los techos tambien se recorren enteros sin bajar.

    Son seis, repartidas a lo largo del nivel (de a pares, una cerca de la
    otra: se sube por una y se baja por la que sigue). Las escaleras salen a
    edificios (mejor chicos), a mas de ESCALERA_MARGEN del borde. Devuelve la
    lista de escaleras.
    """

    ultimo = len(edificios) - 1

    objetivos = [x + r.randint(-250, 250) for x in ESCALERAS_X]

    # Lugares posibles: cualquier edificio menos el ultimo, con lugar a los
    # lados. Se prefieren los chicos (la escalera es mas corta y el techo de
    # llegada es el de siempre): cada altura mas suma un castigo.
    lugares = []

    for i, e in enumerate(edificios):

        if i == ultimo:
            continue

        if e["x1"] - e["x0"] < 2 * ESCALERA_MARGEN:
            continue

        lugares.append((i, e["x0"] + ESCALERA_MARGEN, e["x1"] - ESCALERA_MARGEN))

    # Por programacion dinamica: la combinacion de lugares (uno por escalera,
    # separados lo que pide cada tramo) que menos se aleja de los objetivos.
    posibles = []

    for i, a_, b_ in lugares:

        for x in range(int(a_), int(b_) + 1, 30):

            x = int(x) // PX * PX

            if ESCALERA_X_MIN <= x <= ESCALERA_X_MAX:

                posibles.append((x, i))

    castigo = {i: ESCALERA_CASTIGO_TIER * edificios[i]["tier"] for _, i in posibles}

    posibles.sort()

    # mejor[(x, i)] = (costo, camino) con la ultima escalera ahi
    mejor = {}

    for k, objetivo in enumerate(objetivos):

        # separacion con la anterior: en los techos (sube -> baja) mas larga
        # que en la calle (baja -> sube)
        separacion = ESCALERAS_SEP_TECHOS if k % 2 else ESCALERAS_SEP_CALLE

        nuevo_mejor = {}

        for x, i in posibles:

            desvio = abs(x - objetivo) + castigo[i]

            if k == 0:

                nuevo_mejor[(x, i)] = (desvio, [(x, i)])

                continue

            candidatos = [
                (costo + desvio, camino + [(x, i)])
                for (px_, _), (costo, camino) in mejor.items()
                if x - px_ >= separacion
            ]

            if candidatos:

                nuevo_mejor[(x, i)] = min(candidatos, key=lambda t: t[0])

        mejor = nuevo_mejor

    escaleras = []

    if mejor:

        _, camino = min(mejor.values(), key=lambda t: t[0])

        for x, i in camino:

            escaleras.append(dict(x=x, y=edificios[i]["y"], edificio=i))

    return escaleras


def verificar_terreno(datos):
    """Revisa que el terreno se pueda recorrer. Devuelve una lista de problemas."""

    problemas = []

    edificios = datos["edificios"]

    if edificios[0]["x0"] != 0 or edificios[-1]["x1"] != NIVEL_PX:
        problemas.append("no cubre todo el nivel")

    if edificios[0]["tier"] != 0 or edificios[-1]["tier"] != 0:
        problemas.append("el primero y el ultimo tienen que ser chicos")

    for i, (a, b) in enumerate(zip(edificios, edificios[1:])):

        if a["x1"] != b["x0"]:
            problemas.append("hueco entre edificios")

        # Un escalon de mas de un salto necesita un balcon pegado a la pared
        # del edificio alto, del lado del bajo (para subir desde cualquiera
        # de los dos lados)
        if abs(a["y"] - b["y"]) > SALTO_ESCALON:

            alto_i, lado = (i, "der") if a["y"] < b["y"] else (i + 1, "izq")

            if not any(
                bal["edificio"] == alto_i and bal["lado"] == lado
                for bal in datos["balcones"]
            ):
                problemas.append("escalon sin balcon")

    # Escaleras: de a pares (sube / baja), a edificios chicos, lejos del borde
    esc = datos["escaleras"]

    if len(esc) != len(ESCALERAS_X):
        problemas.append("faltan escaleras")

    if len(esc) % 2:
        problemas.append("escaleras impares")

    for k, (a, b) in enumerate(zip(esc, esc[1:])):
        minimo = ESCALERAS_SEP_TECHOS if k % 2 == 0 else ESCALERAS_SEP_CALLE
        if b["x"] - a["x"] < minimo:
            problemas.append("escaleras muy juntas")

    for e_ in esc:
        ed = edificios[e_["edificio"]]
        if e_["y"] != ed["y"]:
            problemas.append("escalera a otra altura que su techo")
        if e_["x"] - ed["x0"] < ESCALERA_MARGEN or ed["x1"] - e_["x"] < ESCALERA_MARGEN:
            problemas.append("escalera pegada al borde")

    # La calle no tiene nada que la corte
    if datos.get("bloqueos"):
        problemas.append("la calle tiene obras")

    for bal in datos["balcones"]:

        # Del techo bajo hasta el balcon hay un solo salto, y del balcon al
        # techo grande (264) tambien
        if bal["y"] not in (BALCON_FILA * PX, BALCON_FILA_ALTO * PX):
            problemas.append("balcon a otra altura")

        vecino = edificios[bal["edificio"] + (-1 if bal["lado"] == "izq" else 1)]

        if vecino["y"] - bal["y"] > SALTO_ESCALON or bal["y"] - TECHOS_Y[2] > SALTO_ESCALON:
            problemas.append("balcon fuera de alcance")

        # que el balcon no se pise con otro
        for otro in datos["balcones"]:

            if otro is not bal and otro["x0"] < bal["x1"] and bal["x0"] < otro["x1"]:
                problemas.append("balcones superpuestos")

    return problemas


# ==========================================================
# FACHADAS Y TECHOS
# ==========================================================

def hacer_fachada(estilo, ancho, cuerpo, cfg, r):
    """
    Dibuja una fachada de `ancho` x `cuerpo` pixeles, con el techo cortado
    plano (se saca la mansarda, el frontis, etc.: el borde lo pone el techo).
    Devuelve (lienzo, colores).
    """

    fn = G.ESTILOS[estilo][0]

    c = G.elegir_paleta(cfg, estilo, r)

    semilla = r.randint(0, 10 ** 9)

    alto_gen = cuerpo + 14

    spr = None

    for _ in range(6):

        spr = fn(ancho, alto_gen, random.Random(semilla), c)

        k = fila_llena(spr)

        sobra = alto_gen - k

        if sobra == cuerpo:
            break

        alto_gen += cuerpo - sobra

    k = fila_llena(spr)

    sobra = spr.h - k

    # ajuste fino si no cerro justo
    if sobra > cuerpo:
        k += sobra - cuerpo

    out = Lienzo(ancho, cuerpo)

    if sobra < cuerpo:

        # faltan filas: se estira la pared repitiendo la de arriba
        fila = spr.im.crop((0, k, ancho, k + 1))

        for y in range(cuerpo - sobra):
            out.im.paste(fila, (0, y))

        out.im.paste(spr.im.crop((0, k, ancho, spr.h)), (0, cuerpo - sobra))

    else:

        out.im.paste(spr.im.crop((0, k, ancho, k + cuerpo)), (0, 0))

    out.d = ImageDraw.Draw(out.im)

    return out, c


def dibujar_losa(capa, x0, x1, fila, color):
    """El borde del techo: arriba una linea clara (ahi se pisa) y debajo la losa."""

    capa.rect(x0, fila, x1, fila, luz(color, 0.55))

    capa.rect(x0, fila + 1, x1, fila + LOSA - 1, mezcla(color, rgb("#3a3a46"), 0.32))

    # una sombrita bajo el borde
    capa.rect(x0, fila + LOSA, x1, fila + LOSA, sombra(color, 0.78))


def dibujar_puerta_balcon(capa, x, fila, color):
    """Puerta-ventana de la fachada que da al balcon (apoya en la losa)."""

    marco = sombra(color, 0.5)

    capa.rect(x - 1, fila - 12, x + 6, fila - 1, marco)

    capa.rect(x, fila - 11, x + 5, fila - 1, VIDRIO)
    capa.rect(x, fila - 11, x, fila - 8, VIDRIO_LUZ)
    capa.rect(x + 2, fila - 11, x + 3, fila - 1, marco)

    capa.rect(x - 2, fila - 13, x + 7, fila - 13, luz(color, 0.4))


def dibujar_balcon(capa, x0, x1, fila, lado, color, r):
    """Balcon que sale de la pared: losa con barandal de hierro y macetas."""

    # losa
    capa.rect(x0, fila, x1, fila, luz(color, 0.6))
    capa.rect(x0, fila + 1, x1, fila + BALCON_GROSOR - 2, mezcla(color, rgb("#8a8a92"), 0.30))
    capa.rect(x0, fila + BALCON_GROSOR - 1, x1, fila + BALCON_GROSOR - 1, sombra(color, 0.5))

    # el extremo de afuera, mas oscuro
    afuera = x0 if lado == "izq" else x1

    capa.rect(afuera, fila, afuera, fila + BALCON_GROSOR - 1, sombra(color, 0.6))

    # ménsulas abajo
    for k in range(x0 + 4, x1 - 2, 9):

        capa.poly(
            [(k, fila + BALCON_GROSOR), (k + 3, fila + BALCON_GROSOR),
             (k, fila + BALCON_GROSOR + 3)],
            sombra(color, 0.55)
        )

    # baranda de hierro (detras del personaje)
    hierro = rgb("#2a2a34")

    capa.rect(x0, fila - 6, x1, fila - 6, hierro)

    for k in range(x0, x1 + 1, 2):
        capa.rect(k, fila - 5, k, fila - 1, hierro)

    for k in range(x0, x1 + 1, 12):

        capa.rect(k, fila - 8, k + 1, fila - 1, hierro)
        capa.px(k, fila - 9, hierro)

    # macetas con flores
    for _ in range(r.randint(1, 3)):

        px = r.randint(x0 + 3, x1 - 5)

        capa.rect(px, fila - 8, px + 3, fila - 7, rgb("#9a4a30"))
        capa.rect(px, fila - 11, px + 3, fila - 9, rgb("#3f8f3a"))
        capa.px(px + 1, fila - 12, r.choice([ROJO, rgb("#e88fb0"), AMARILLO_BOCA, BLANCO]))


# ----------------------------------------------------------
# COSAS DE LAS AZOTEAS
# ----------------------------------------------------------

def prop_tanque(l, x, fila, r):
    ancho = r.choice([6, 7, 8])
    alto = r.choice([5, 6, 7])

    E._tanque(l, x, fila - 3, ancho, alto)

    return ancho


# Puntas de antena del ultimo nivel dibujado (x, y): de noche llevan una luz roja
PUNTAS_DE_ANTENA = []


def prop_antena(l, x, fila, r):

    alto = r.randint(7, 13)

    E._antena(l, x, fila - 1, alto)

    PUNTAS_DE_ANTENA.append((x, fila - 2 - alto))

    return 5


def prop_aire(l, x, fila, r):
    E._aire_acond(l, x, fila - 2)

    if r.random() < 0.5:
        E._aire_acond(l, x + 4, fila - 2)

        return 8

    return 4


def prop_planta(l, x, fila, r):
    ancho = r.randint(6, 10)
    alto = r.randint(4, 7)

    arbusto(l, x + ancho // 2, fila - 1, ancho, alto, rgb(r.choice(["#3a8a3a", "#4a9a44", "#2f7a3a"])))

    return ancho + 1


def prop_ropa(l, x, fila, r):
    largo = r.randint(14, 22)

    alto = 8

    l.rect(x, fila - alto, x, fila - 1, rgb("#5a5a5a"))
    l.rect(x + largo, fila - alto, x + largo, fila - 1, rgb("#5a5a5a"))

    E._ropa_tendida(l, x + 1, x + largo, fila - alto + 1, r)

    return largo + 2


def prop_chimenea(l, x, fila, r):
    alto = r.randint(4, 7)

    l.rect(x, fila - alto, x + 2, fila - 1, rgb("#9a6a55"))
    l.rect(x - 1, fila - alto - 1, x + 3, fila - alto, rgb("#5a4a44"))

    return 6


def prop_banderin(l, x, fila, r):
    E.banderin_boca(l, x, fila - 1, r.randint(12, 18))

    return 11


def prop_cartel(l, x, fila, r):
    """Cartel de chapa sobre dos patas (publicidad de azotea)."""

    ancho = r.randint(14, 22)

    col = r.choice([rgb("#c8322d"), rgb("#1f4a8f"), rgb("#e3b92f"), rgb("#2f7a4a")])

    l.rect(x + 2, fila - 6, x + 3, fila - 1, rgb("#4a4f58"))
    l.rect(x + ancho - 3, fila - 6, x + ancho - 2, fila - 1, rgb("#4a4f58"))

    l.rect(x, fila - 12, x + ancho, fila - 6, luz(col, 0.5))
    l.rect(x + 1, fila - 11, x + ancho - 1, fila - 7, col)

    for k in range(x + 3, x + ancho - 3, 3):
        l.rect(k, fila - 10, k + 1, fila - 8, luz(col, 0.7))

    return ancho + 2


PROPS = {
    "tanque": (prop_tanque, 3),
    "antena": (prop_antena, 3),
    "aire": (prop_aire, 3),
    "planta": (prop_planta, 2),
    "ropa": (prop_ropa, 2),
    "chimenea": (prop_chimenea, 2),
    "cartel": (prop_cartel, 1),
    "banderin": (prop_banderin, 0),
}


def poner_props(capa, terr, cfg, r, ocupados_extra):
    """
    Cosas sobre los techos (tanques, antenas, ropa tendida...). Son puro
    decorado: el personaje pasa por delante. Se evitan los balcones de los
    edificios vecinos y las partes donde van los carteles.
    """

    extra = PROPS_BARRIO.get(cfg["barrio"], {})

    pesos = [
        (nombre, peso + extra.get(nombre, 0))
        for nombre, (_, peso) in PROPS.items()
    ]

    pesos = [(n_, p) for n_, p in pesos if p > 0]

    paloma_ok = "palomas" in cfg.get("especiales", [])

    for e in terr.edificios:

        fila = e.y // PX

        a, b = terr.zona_libre(e)

        a //= PX
        b //= PX

        # primero y ultimo: libres para los carteles y el arranque
        if e.indice == 0:
            a = max(a, 250)

        if e.indice == len(terr.edificios) - 1:
            b = min(b, (e.x1 // PX) - 140)

        if b - a < 24:
            continue

        # chicos: 1 a 3 cosas; medianos y grandes: 2 a 4
        cantidad = r.randint(1, 3) if e.tier == 0 else r.randint(2, 5)

        ocupado = [tuple(o) for o in ocupados_extra if a - 40 < o[1] and o[0] < b + 40]

        for _ in range(cantidad):

            nombre = G.elegir_pesos(pesos, r)

            fn = PROPS[nombre][0]

            # prueba un lugar libre
            for _ in range(8):

                x = r.randint(a, b - 10)

                if all(x + 24 < o0 or x > o1 + 2 for o0, o1 in ocupado):

                    ancho = fn(capa, x, fila, r)

                    ocupado.append((x, x + ancho))

                    break

        if paloma_ok or r.random() < 0.20:

            for _ in range(r.randint(1, 3)):

                x = r.randint(a, b - 6)

                if all(x + 8 < o0 or x > o1 + 2 for o0, o1 in ocupado):
                    E.paloma(capa, x, fila - 1)


# ==========================================================
# LA CALLE: vereda, cordon y asfalto; escaleras y farolas
# ==========================================================

def dibujar_calle(capa, r):
    """Las filas de abajo de las fachadas: vereda, cordon y calle."""

    # zocalo: la sombra donde la pared toca la vereda
    capa.rect(0, FILA_FACHADA, ANCHO - 1, FILA_FACHADA, rgb("#4a4650"))

    # vereda (donde se camina; los pies quedan en FILA_CALLE)
    vereda = rgb("#b4aea2")

    capa.rect(0, FILA_FACHADA + 1, ANCHO - 1, FILA_CALLE + 1, vereda)

    capa.rect(0, FILA_FACHADA + 1, ANCHO - 1, FILA_FACHADA + 2, sombra(vereda, 0.86))

    # baldosas: juntas verticales cada 12 y una horizontal
    for x in range(0, ANCHO, 12):

        capa.rect(x, FILA_FACHADA + 3, x, FILA_CALLE + 1, sombra(vereda, 0.9))

    capa.rect(0, FILA_FACHADA + 6, ANCHO - 1, FILA_FACHADA + 6, sombra(vereda, 0.92))

    # manchitas de las baldosas
    for _ in range(ANCHO // 10):

        x = r.randrange(ANCHO)

        y = r.randint(FILA_FACHADA + 3, FILA_CALLE + 1)

        capa.px(x, y, sombra(vereda, r.choice((0.88, 0.94, 1.06))))

    # cordon
    cordon = rgb("#d6d1c4")

    capa.rect(0, FILA_CALLE + 2, ANCHO - 1, FILA_CALLE + 2, luz(cordon, 0.3))

    capa.rect(0, FILA_CALLE + 3, ANCHO - 1, FILA_CALLE + 4, cordon)

    capa.rect(0, FILA_CALLE + 5, ANCHO - 1, FILA_CALLE + 5, sombra(cordon, 0.55))

    # asfalto
    asfalto = rgb("#4a4c56")

    capa.rect(0, FILA_CALLE + 6, ANCHO - 1, ALTO_CERCANA - 1, asfalto)

    # el asfalto se va oscureciendo hacia abajo
    for y in range(FILA_CALLE + 6, ALTO_CERCANA):

        t = (y - FILA_CALLE - 6) / (ALTO_CERCANA - FILA_CALLE - 6)

        capa.rect(0, y, ANCHO - 1, y, mezcla(asfalto, rgb("#2e3038"), 0.15 + 0.6 * t))

    # grano y parches
    for _ in range(ANCHO * 2):

        x = r.randrange(ANCHO)

        y = r.randint(FILA_CALLE + 7, ALTO_CERCANA - 1)

        capa.px(x, y, r.choice((rgb("#5a5c66"), rgb("#3c3e48"), rgb("#62646e"))))

    # linea de carril discontinua
    for x in range(4, ANCHO, 36):

        capa.rect(x, FILA_CALLE + 26, x + 17, FILA_CALLE + 27, rgb("#e6cf5c"))

    # alcantarillas
    for _ in range(ANCHO // 400):

        x = r.randint(20, ANCHO - 30)

        capa.elipse(x, FILA_CALLE + 14, x + 11, FILA_CALLE + 17, rgb("#2a2c34"))

        capa.elipse(x + 1, FILA_CALLE + 14, x + 10, FILA_CALLE + 16, rgb("#6a6c78"))


def dibujar_escalera(l, x, fila_techo, fila_pie=FILA_CALLE):
    """
    Escalera de mano pegada a la fachada: dos varales de metal y travesanos.
    `x` es el centro; sobresale un poco arriba del techo. Con carteles
    amarillos con flecha (arriba en la calle, abajo en el techo) para que se
    vea que se puede usar.
    """

    mitad = ESCALERA_ANCHO // 2 - 1

    metal = rgb("#8a93a3")

    metal_luz = rgb("#c9d1de")

    metal_osc = rgb("#4a505e")

    tope = fila_techo - 7

    izq = x - mitad

    der = x + mitad

    # varales: el de afuera de cada lado, mas oscuro (da volumen)
    l.rect(izq, tope, izq, fila_pie, metal)
    l.rect(izq - 1, tope + 1, izq - 1, fila_pie, metal_osc)

    l.rect(der, tope, der, fila_pie, metal)
    l.rect(der + 1, tope + 1, der + 1, fila_pie, metal_osc)

    # el brillo de arriba, donde sobresale del techo
    l.rect(izq, tope, izq, fila_techo - 1, metal_luz)
    l.rect(der, tope, der, fila_techo - 1, metal_luz)

    # travesanos cada 5 filas
    for fila in range(tope + 3, fila_pie - 1, 5):

        l.rect(izq + 1, fila, der - 1, fila, metal_luz)

        l.rect(izq + 1, fila + 1, der - 1, fila + 1, metal_osc)

    # soportes contra la pared
    for fila in range(fila_techo + 10, fila_pie - 6, 38):

        l.rect(izq - 3, fila, izq - 2, fila + 1, metal_osc)

        l.rect(der + 2, fila, der + 3, fila + 1, metal_osc)

    # remate de arriba (los varales se doblan hacia el techo)
    l.rect(izq - 2, tope, izq, tope, metal_luz)

    l.rect(der, tope, der + 2, tope, metal_luz)

    # carteles amarillos con flecha: hacia arriba en la calle y hacia abajo
    # en el techo
    negro = rgb("#2a2a2a")

    for cx, cy, abajo in (
        (der + 7, fila_pie - 24, False),
        (der + 7, fila_techo - 9, True)
    ):

        l.rect(cx - 3, cy - 3, cx + 3, cy + 3, rgb("#3a3a3a"))

        l.rect(cx - 2, cy - 2, cx + 2, cy + 2, rgb("#f2c230"))

        if abajo:

            l.rect(cx, cy - 2, cx, cy, negro)

            l.px(cx - 1, cy, negro)

            l.px(cx + 1, cy, negro)

            l.px(cx, cy + 1, negro)

        else:

            l.rect(cx, cy, cx, cy + 2, negro)

            l.px(cx - 1, cy, negro)

            l.px(cx + 1, cy, negro)

            l.px(cx, cy - 1, negro)


def componer_recortado(capa, img, x, y):
    """Pega una imagen con transparencia, recortando lo que se sale del lienzo."""

    sx0 = max(0, -x)
    sy0 = max(0, -y)
    sx1 = min(img.width, capa.w - x)
    sy1 = min(img.height, capa.h - y)

    if sx1 > sx0 and sy1 > sy0:

        capa.im.alpha_composite(img.crop((sx0, sy0, sx1, sy1)), (x + sx0, y + sy0))

        capa.d = ImageDraw.Draw(capa.im)


def halo(capa, cx, cy, radio, color, alfa_max):
    """Resplandor redondo (se va transparentando hacia afuera)."""

    lado = radio * 2 + 1

    yy, xx = np.mgrid[0:lado, 0:lado]

    d = np.sqrt((xx - radio) ** 2 + (yy - radio) ** 2) / radio

    a = np.clip(1.0 - d, 0.0, 1.0) ** 1.6 * alfa_max

    # el dibujo es de pocos colores: el resplandor se hace en escalones
    a = (np.round(a / 14.0) * 14.0).astype(np.uint8)

    img = np.zeros((lado, lado, 4), np.uint8)

    img[..., 0], img[..., 1], img[..., 2] = color

    img[..., 3] = a

    componer_recortado(capa, Image.fromarray(img, "RGBA"), int(cx - radio), int(cy - radio))


ALTO_FAROLA = 64


def una_farola(objetos, x, cfg, ef, azar, color_luz):
    """Un poste de la vereda. De noche esta prendido: cono de luz, charcos y halo."""

    cabeza = FILA_CALLE - 2 - ALTO_FAROLA - 3

    noche = es_noche(cfg)

    if noche:

        # la luz cae detras del poste: cono sobre la fachada, charco en la vereda
        # y un reflejo largo en el asfalto
        L.cono_de_luz(objetos, x, cabeza, FILA_CALLE - 1, 58, color_luz, 60)

        L.charco_de_luz(objetos, x, FILA_CALLE - 1, 30, 4, color_luz, 130)

        L.charco_de_luz(objetos, x, FILA_CALLE + 14, 40, 8, color_luz, 70)

        L.reflejo_en_asfalto(objetos, x, FILA_CALLE + 8, 26, color_luz, 110)

    farola(objetos, x, FILA_CALLE - 2, ALTO_FAROLA, rgb("#2c3438"))

    if noche:

        objetos.rect(x - 2, cabeza, x + 2, cabeza + 2, mezcla(color_luz, (255, 255, 255), 0.65))

        halo(objetos, x, cabeza + 1, 28, color_luz, 170)

        halo(objetos, x, cabeza + 1, 11, mezcla(color_luz, (255, 255, 255), 0.5), 150)

        if ef is not None:

            ef.lampara("ciudad", x, cabeza + 1, 24, color_luz, parpadea=azar.random() < 0.12)


def poner_farolas(objetos, terr, cfg, r, ef=None, azar=None, desde=0):
    """
    Farolas sobre la vereda, lejos de las escaleras. De noche estan prendidas
    y hay el doble (una entre cada par). No se pone ninguna antes de `desde`
    (el hall del Huergo del nivel 1 es un interior).
    """

    noche = es_noche(cfg)

    azar = azar or random.Random(0)

    color_luz = G.hx(cfg.get("farola_luz", "#ffe28c"))

    libres = [
        (esc.x // PX - 16, esc.x // PX + 16) for esc in terr.escaleras
    ]

    x = r.randint(120, 200)

    while x < ANCHO - 120:

        salto = r.randint(170, 240)

        if x >= desde and all(x < a or x > b for a, b in libres):

            una_farola(objetos, x, cfg, ef, azar, color_luz)

        # de noche, una mas a mitad de camino hasta la siguiente
        medio = x + salto // 2

        if (
            noche and medio >= desde and medio < ANCHO - 120
            and all(medio < a or medio > b for a, b in libres)
        ):

            una_farola(objetos, medio, cfg, ef, azar, color_luz)

        x += salto


def poner_luminarias_de_azotea(objetos, terr, cfg, ocupados, ef, azar):
    """
    De noche, postes de luz chicos sobre los techos (con su charco de luz en la
    azotea) y luces rojas de aviso en la punta de las antenas.
    """

    color_luz = G.hx(cfg.get("farola_luz", "#ffe28c"))

    for e in terr.edificios:

        fila = e.y // PX

        a, b = terr.zona_libre(e)

        a //= PX
        b //= PX

        if e.indice == 0:
            a = max(a, 250)

        if e.indice == len(terr.edificios) - 1:
            b = min(b, (e.x1 // PX) - 140)

        if b - a < 40 or azar.random() > 0.6:

            continue

        x = a + 5 if azar.random() < 0.5 else b - 5

        if any(o0 - 4 < x < o1 + 4 for o0, o1 in ocupados):

            continue

        L.charco_de_luz(objetos, x, fila - 1, 15, 2, color_luz, 70)

        L.luminaria_azotea(objetos, x, fila - 1, 11, color_luz, ef, "ciudad")

        halo(objetos, x, fila - 14, 12, color_luz, 120)

    for x, y in PUNTAS_DE_ANTENA:

        halo(objetos, x, y, 6, (255, 70, 60), 110)

        L.antena_con_baliza(objetos, x, y, ef, "ciudad")


# ==========================================================
# CAPA CERCANA (calle, edificios y techos por donde se camina)
# ==========================================================

def hacer_cercana(n, cfg, datos, r, ef=None):
    """
    Devuelve el lienzo de 3200 x 312 con la calle, los edificios, los techos,
    los balcones y las escaleras. De dia le da el sol (reflejos en los vidrios y
    en la calle); de noche, ventanas prendidas, postes de luz y balizas.
    """

    terr = Terreno.desde_dict(datos)

    noche = es_noche(cfg)

    # los efectos de luz tienen su propio azar: no cambian el dibujo de los
    # edificios
    azar = random.Random(9100 + n)

    lado = L.lado_del_sol(cfg)

    del PUNTAS_DE_ANTENA[:]

    capa = Lienzo(ANCHO, ALTO_CERCANA)

    horizonte = G.hx(cfg["cielo"][2])

    # color de la fachada que toca cada pared (para pintar los balcones)
    color_izq = {}
    color_der = {}

    for e in terr.edificios:

        x0 = e.x0 // PX
        x1 = e.x1 // PX

        fila = e.y // PX

        cuerpo = FILA_FACHADA - fila - LOSA

        minimo, maximo = (46, 84) if e.tier < 2 else (52, 100)

        x = x0

        previo = None

        for ancho in repartir(x1 - x0, minimo, maximo, r):

            # cada tramo puede ser una casa distinta (misma altura de techo)
            est = e.estilo if previo is None else elegir_estilo(cfg, e.tier, previo, r)

            fachada, c = hacer_fachada(est, ancho, cuerpo, cfg, r)

            capa.pegar(fachada, x, fila + LOSA)

            dibujar_losa(capa, x, x + ancho - 1, fila, c["fachada"])

            # linea oscura entre una casa y la otra
            capa.rect(x, fila, x, FILA_FACHADA - 1, sombra(c["fachada"], 0.42))

            # de dia: el sol le da a un costado de la pared (una linea clara)
            if not noche:

                borde = x + ancho - 2 if lado == "der" else x + 1

                capa.rect(
                    borde, fila + LOSA + 1, borde, FILA_FACHADA - 3,
                    luz(c["fachada"], 0.24)
                )

            if previo is None:
                color_izq[e.indice] = c["fachada"]

            color_der[e.indice] = c["fachada"]

            previo = est

            x += ancho

    # el nivel 2 arranca en la puerta de entrada del Instituto Huergo (de donde
    # se salio en el nivel 1): la fachada del primer edificio se redibuja como
    # la entrada real (granito negro, porton de rombos, vidrieras, cornisa).
    # (Los tramos de arriba ya se dibujaron, asi el azar de los edificios que
    # siguen no cambia.)
    if cfg.get("puerta") == "huergo":

        primero = terr.edificios[0]

        fila0 = primero.y // PX

        ancho0 = primero.x1 // PX - primero.x0 // PX

        fachada, c = HR.fachada_entrada(
            ancho0, FILA_FACHADA - fila0 - LOSA, random.Random(4242)
        )

        capa.pegar(fachada, 0, fila0 + LOSA)

        dibujar_losa(capa, 0, ancho0 - 1, fila0, c["fachada"])

        capa.rect(0, fila0, 0, FILA_FACHADA - 1, sombra(c["fachada"], 0.42))

        color_izq[0] = color_der[0] = c["fachada"]

    # cierre del ultimo edificio
    capa.rect(ANCHO - 1, FILAS_TECHO[0], ANCHO - 1, FILA_FACHADA - 1, rgb("#2a2630"))

    # la calle: vereda, cordon y asfalto
    dibujar_calle(capa, r)

    # la vereda de la entrada del Huergo: baldosas ocres y banda amarilla
    if cfg.get("puerta") == "huergo":

        HR.vereda_entrada(
            capa, 0, terr.edificios[0].x1 // PX - 1, FILA_FACHADA, FILA_CALLE,
            random.Random(4343)
        )

    # Sombra donde el edificio alto le tapa la luz al bajo (da profundidad)
    factores = np.ones((ALTO_CERCANA, ANCHO), np.float32)

    for a, b in zip(terr.edificios, terr.edificios[1:]):

        if a.y == b.y:
            continue

        bajo, alto_ = (a, b) if a.y > b.y else (b, a)

        ancho_sombra = 7

        for d in range(ancho_sombra):

            if bajo is a:
                col = a.x1 // PX - 1 - d
            else:
                col = b.x0 // PX + d

            if 0 <= col < ANCHO:

                f = 0.72 + 0.28 * d / ancho_sombra

                factores[bajo.y // PX + LOSA:FILA_FACHADA, col] = f

    # abajo de las fachadas (planta baja) queda un poco mas oscuro: la calle
    # es angosta y le llega menos luz
    for y in range(FILA_FACHADA - 18, FILA_FACHADA):

        factores[y, :] *= 1.0 - 0.22 * (y - (FILA_FACHADA - 18)) / 18

    # y el asfalto, lejos abajo, tambien
    for y in range(FILA_CALLE + 6, ALTO_CERCANA):

        factores[y, :] *= 0.96

    multiplicar_rgb(capa, factores)

    # ---- sol (dia) o luces (noche), bruma y tinte (antes de poner lo de adelante)
    ventanas = None

    if noche:

        # se eligen ahora (los vidrios se buscan por su color) y se prenden
        # despues de teñir, asi la luz no se apaga con la bruma
        luces = cfg.get("luces", 0.0)

        ventanas = L.elegir_ventanas(capa, luces, azar)

        # de noche las paredes se ven mas oscuras: asi resaltan las luces
        multiplicar_rgb(capa, np.full((ALTO_CERCANA, ANCHO), NOCHE_OSCURIDAD_CERCANA, np.float32))

    else:

        # los vidrios se buscan ahora (por su color); el sol se les pone
        # despues de la bruma, asi brillan
        ventanas_dia = L.Ventanas(capa)

    G.tenir(capa, horizonte, 0.05)

    if "tinte" in cfg:

        col, t = cfg["tinte"]

        G.tenir(capa, G.hx(col), t)

    if noche:

        L.prender_ventanas(
            capa, ventanas[0], ventanas[1], azar, cfg.get("paleta_luces", "calida")
        )

    else:

        # vidrios que reflejan el sol, brillo en la calle y destellos
        L.reflejos_en_ventanas(
            capa, 0.42, azar, G.hx(cfg["cielo"][1]), lado, ef, "ciudad",
            max_brillos=110, ventanas=ventanas_dia
        )

        L.brillo_de_calle(capa, azar, ef, (FILA_FACHADA, FILA_CALLE, ALTO_CERCANA), ANCHO)

    # ---- balcones
    for bal in terr.balcones:

        e = terr.edificios[bal.edificio]

        color = (color_izq if bal.lado == "izq" else color_der).get(
            bal.edificio, rgb("#d8d0c0")
        )

        lienzo_extra = Lienzo(ANCHO, ALTO)

        dibujar_balcon(
            lienzo_extra,
            bal.x0 // PX, bal.x1 // PX - 1,
            bal.y // PX, bal.lado, color, r
        )

        if "tinte" in cfg:

            col, t = cfg["tinte"]

            G.tenir(lienzo_extra, G.hx(col), t)

        capa.pegar(lienzo_extra, 0, 0)

        # la puerta de la fachada que sale al balcon
        e_x = (e.x0 // PX + 4) if bal.lado == "izq" else (e.x1 // PX - 11)

        dibujar_puerta_balcon(capa, e_x, bal.y // PX, color)

    # ---- cosas de las azoteas y carteles (sin bruma, solo tinte)
    objetos = Lienzo(ANCHO, ALTO_CERCANA)

    primero = terr.edificios[0]

    ultimo = terr.edificios[-1]

    ocupados = []

    # carteles de bienvenida y de salida
    textos = [("BIENVENIDOS A", 1), (cfg["barrio"], 2)]

    ancho_cartel = G.cartel_grande(
        objetos, 60, FILAS_TECHO[0], textos, rgb("#1f4a8f"), BLANCO
    )

    ocupados.append((55, 60 + ancho_cartel + 6))

    sig = cfg["siguiente"]

    x_salida = ultimo.x1 // PX - 200

    if sig:

        ancho_cartel = G.cartel_grande(
            objetos, x_salida, FILAS_TECHO[0],
            [("SEGUI A", 1), (sig, 1)],
            rgb("#1f6f3f"), BLANCO, flecha=True
        )

    else:

        ancho_cartel = G.cartel_grande(
            objetos, x_salida, FILAS_TECHO[0],
            [("FIN DEL", 1), ("RECORRIDO", 1)],
            rgb("#8f1f2a"), rgb("#ffe27a")
        )

    ocupados.append((x_salida - 5, x_salida + ancho_cartel + 6))

    # escaleras de mano (los techos las dejan libres: ver Terreno.zona_libre)
    for esc in terr.escaleras:

        dibujar_escalera(objetos, esc.x // PX, esc.y_alto // PX)

        ocupados.append((esc.x // PX - 14, esc.x // PX + 14))

    # (en el nivel 2 las farolas arrancan despues de la puerta de entrada)
    poner_farolas(
        objetos, terr, cfg, r, ef, azar,
        desde=HR.DER_VIDRIERA[1] + 14 if cfg.get("puerta") else 12
    )

    poner_props(objetos, terr, cfg, r, ocupados)

    if noche:

        poner_luminarias_de_azotea(objetos, terr, cfg, ocupados, ef, azar)

    if "tinte" in cfg:

        col, t = cfg["tinte"]

        G.tenir(objetos, G.hx(col), t)

    capa.pegar(objetos, 0, 0)

    return capa


# ==========================================================
# LA CAPA CERCANA DEL NIVEL 1: TODO POR DENTRO DEL HUERGO
# ==========================================================

def hacer_cercana_plana(n, cfg, datos, r, ef=None):
    """
    El nivel 1 transcurre ADENTRO del Instituto Huergo y es mas corto que los
    demas: 1600 columnas de dibujo (4800 px). Se recorre por un solo piso, el
    del pasillo, asi que no hay techos, balcones ni escaleras: las paredes
    llegan hasta el cielorraso, de punta a punta.

    El recorrido (huergo_real.RUTA) va de un taller a los pasillos con aulas,
    el laboratorio, la biblioteca, la escalera, la secretaria y el salon de
    actos; despues el vestibulo (con el nombre en el granito negro) y, justo
    en la bandera de meta, el porton de calle abierto.
    Devuelve el lienzo de 1600 x 312.
    """

    HR.verificar_ruta()

    ancho_total = HR.ANCHO_INTERIOR

    capa = Lienzo(ancho_total, ALTO_CERCANA)

    cuerpo = FILA_FACHADA - HR.FILA_TOPE

    modulos = list(HR.RUTA) + [
        ("vestibulo", HR.VESTIBULO_ANCHO),
        ("salida", HR.SALIDA_ANCHO)
    ]

    ventanales = []

    x_puerta = None

    x = 0

    for est, ancho in modulos:

        if est == "vestibulo":
            fachada, c = HR.modulo_vestibulo(ancho, cuerpo, r)
        elif est == "salida":
            fachada, c = HR.modulo_salida_reja(ancho, cuerpo, r)
        else:
            fachada, c = IH.fachada(est, ancho, cuerpo, r)

        capa.pegar(fachada, x, HR.FILA_TOPE)

        # linea oscura entre un modulo y el otro
        capa.rect(x, HR.FILA_TOPE, x, FILA_FACHADA - 1, sombra(c["fachada"], 0.42))

        for lx in c.get("luces", []):
            ventanales.append(x + lx)

        if est == "salida":
            x_puerta = x + ancho - HR.SALIDA_PUERTA_DX

        x += ancho

    # cierre del final del nivel
    capa.rect(ancho_total - 1, HR.FILA_TOPE, ancho_total - 1, FILA_FACHADA - 1, rgb("#2a2630"))

    # el cielorraso con su cornisa, el piso de granito y el umbral de la calle
    HR.cielorraso(capa, r)

    HR.piso_granito(capa, r)

    HR.piso_umbral(capa, x_puerta - HR.SALIDA_PUERTA_MITAD - 3, ancho_total - 1, r)

    for cx in ventanales:

        IH.charco_de_luz(capa, cx, 18)

    IH.luz_de_la_salida(capa, x_puerta - HR.SALIDA_PUERTA_MITAD - 5)

    # abajo de las paredes queda un poco mas oscuro (le llega menos luz)
    factores = np.ones((ALTO_CERCANA, ancho_total), np.float32)

    for y in range(FILA_FACHADA - 14, FILA_FACHADA):

        factores[y, :] *= 1.0 - 0.14 * (y - (FILA_FACHADA - 14)) / 14

    multiplicar_rgb(capa, factores)

    # un tinte calido: luz de tubos y de ventanales
    G.tenir(capa, rgb("#fff0c8"), 0.05)

    # los tubos fluorescentes del cielorraso (uno cada tanto, no sobre la salida)
    HR.luminarias(capa, list(range(40, x_puerta - 40, 78)), r)

    return capa


# ==========================================================
# CIELO
# ==========================================================

def luna_con_fase(l, lx, ly, lr, fase):
    """
    La luna (llena, creciente o media), con sus crateres. Lo que queda en sombra
    no se dibuja: se ve el cielo (y el resplandor) a traves.
    """

    color = rgb("#f4f1de")
    crater = rgb("#d6d3bf")

    # mordida de la fase: un circulo corrido que tapa parte de la luna
    if fase == "creciente":
        mx, my, mr = lx + int(lr * 0.62), ly - int(lr * 0.12), int(lr * 0.92)
    elif fase == "media":
        mx, my, mr = lx + int(lr * 1.05), ly, int(lr * 1.05)
    else:
        mx, my, mr = None, None, 0

    for y in range(ly - lr, ly + lr + 1):

        for x in range(lx - lr, lx + lr + 1):

            if (x - lx) ** 2 + (y - ly) ** 2 > lr * lr + lr * 0.6:

                continue

            if mx is not None and (x - mx) ** 2 + (y - my) ** 2 < mr * mr:

                continue

            l.px(x, y, color)

    if fase == "llena":

        l.circulo(lx + lr // 3, ly - lr // 3, lr // 4, crater)
        l.circulo(lx - lr // 3, ly + lr // 4, lr // 5, crater)

    else:

        l.px(lx - lr // 2, ly + lr // 4, crater)
        l.px(lx - lr // 2, ly - lr // 5, crater)
        l.px(lx - lr // 3, ly + lr // 2, crater)


def hacer_cielo(n, cfg, ef=None):
    """Degradado, estrellas, sol o luna y nubes (sin ciudad)."""

    r = random.Random(7000 + n)

    azar = random.Random(9300 + n)

    W = ancho_capa(PARALLAX["cielo"])

    arriba, medio, abajo = (G.hx(c) for c in cfg["cielo"])

    l = cielo(W, ALTO, arriba, medio, abajo)

    noche = es_noche(cfg)

    k = W / 1300.0

    # estrellas
    if cfg.get("estrellas") or cfg.get("noche", 0) > 0.45:

        for _ in range(60 if cfg.get("estrellas") else 28):

            x = r.randint(0, W - 1)
            y = r.randint(0, 120)

            l.px(x, y, rgb("#e8ecff") if r.random() < 0.6 else rgb("#8c96d8"))

            if r.random() < 0.06:

                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    l.px(x + dx, y + dy, rgb("#cfd6ff"))

        # de noche, mas estrellas (y mas chicas) en el borde de arriba
        if noche:

            for _ in range(70):

                x = azar.randint(0, W - 1)
                y = azar.randint(0, 100)

                l.px(x, y, rgb("#aab4f0") if azar.random() < 0.7 else rgb("#e8ecff"))

            # estrellas que brillan en cruz
            for _ in range(7):

                x = azar.randint(6, W - 7)
                y = azar.randint(4, 70)

                l.px(x, y, rgb("#ffffff"))

                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    l.px(x + dx, y + dy, rgb("#d8deff"))

    # sol (la x de la configuracion era para un cielo de 1300 de ancho)
    if "sol" in cfg:

        sx, sy, sr, sc = cfg["sol"]

        sx = int(60 + sx * k * 0.85)

        col = G.hx(sc)

        # rayos y resplandor grande (debajo del disco)
        L.rayos_de_sol(l, sx, sy, col, 70, 12, azar)

        halo(l, sx, sy, sr * 7, col, 90)

        halo(l, sx, sy, sr * 4, mezcla(col, (255, 255, 255), 0.4), 110)

        for kk, tt in ((sr + 6, 0.16), (sr + 3, 0.30)):
            l.circulo(sx, sy, kk, mezcla(medio if sy < 100 else abajo, col, tt))

        l.circulo(sx, sy, sr, col)
        l.circulo(sx - 2, sy - 2, max(2, sr - 4), luz(col, 0.35))
        l.circulo(sx - 1, sy - 1, max(1, sr - 6), rgb("#ffffff"))

        if ef is not None:

            ef.astro_en_cielo("sol", sx, sy, sr, col)

    # luna
    if "luna" in cfg:

        lx, ly, lr = cfg["luna"][:3]

        fase = cfg["luna"][3] if len(cfg["luna"]) > 3 else "llena"

        lx = int(70 + lx * k * 0.8)

        halo(l, lx, ly, lr * 6, (170, 190, 255), 70)

        halo(l, lx, ly, lr * 3, (220, 228, 255), 90)

        luna_con_fase(l, lx, ly, lr, fase)

        if ef is not None:

            ef.astro_en_cielo("luna", lx, ly, lr, (190, 205, 255))

    # nubes
    col_nube = G.hx(cfg.get("nubes", "#ffffff"))

    sombra_nube = mezcla(col_nube, medio, 0.5)

    cantidad = 5

    for i in range(cantidad):

        x = int((i + r.random() * 0.8) * W / cantidad)
        y = r.randint(8, 70)
        w = r.randint(30, 66)

        nube(l, x, y, w, col_nube, sombra_nube)

    return l


# ==========================================================
# CIUDAD LEJANA + MONUMENTOS
# ==========================================================

# Los monumentos se achican para que quepan a lo lejos
MON_MAX_ANCHO = 120
MON_MAX_ALTO = 96
MON_ESCALA_MAX = 0.9

# Fila donde apoyan los monumentos y la ciudad lejana
LEJOS_BASE = 138

# Cuanto se oscurecen de noche las paredes de la calle y las del medio (1 = nada)
NOCHE_OSCURIDAD_CERCANA = 0.66
NOCHE_OSCURIDAD_MEDIO = 0.80

# Que tan nebulosos se ven
BRUMA_MONUMENTO = 0.34
BRUMA_MEDIO = 0.30


def achicar_monumento(spr):
    """Reduce el dibujo de un monumento (mezclando colores) sin dejar bordes borrosos."""

    esc = min(MON_ESCALA_MAX, MON_MAX_ANCHO / spr.w, MON_MAX_ALTO / spr.h)

    w = max(6, int(round(spr.w * esc)))
    h = max(6, int(round(spr.h * esc)))

    im = spr.im.resize((w, h), Image.BOX)

    a = np.array(im)

    # bordes nitidos: o se ve o no se ve
    a[..., 3] = np.where(a[..., 3] >= 110, 255, 0)

    out = Lienzo(w, h)

    out.im = Image.fromarray(a, "RGBA")

    out.d = ImageDraw.Draw(out.im)

    return out


def luces_lejanas(spr, prob, r):
    """Ventanitas prendidas en un monumento lejano (las partes oscuras)."""

    a = np.array(spr.im)

    brillo = a[..., :3].astype(np.int32).sum(axis=-1) / 3

    candidatos = (a[..., 3] > 0) & (brillo < 125)

    ys, xs = np.nonzero(candidatos)

    for y, x in zip(ys, xs):

        if r.random() < prob and x % 2 == 0 and y % 2 == 0:
            a[y, x] = (255, 224, 128, 255)

    spr.im = Image.fromarray(a, "RGBA")

    spr.d = ImageDraw.Draw(spr.im)


def balizas_en_siluetas(l, azar, ef, prob):
    """
    Luces rojas de aviso en las puntas mas altas de la ciudad lejana (cada una
    con una antenita; en el juego prenden y apagan).
    """

    a = np.array(l.im)[..., 3] > 0

    ancho = a.shape[1]

    tope = np.where(a.any(axis=0), a.argmax(axis=0), 10 ** 6)

    x = 8

    while x < ancho - 8:

        y = int(tope[x])

        if y < LEJOS_BASE - 24 and y == tope[x - 6:x + 7].min() and azar.random() < prob:

            l.rect(x, y - 4, x, y - 1, (44, 50, 90))

            L.antena_con_baliza(l, x, y - 5, ef, "lejos")

            halo(l, x, y - 5, 4, (255, 70, 60), 110)

            x += 26

        else:

            x += 1


def hacer_lejos(n, cfg, ef=None):
    """
    La ciudad de lejos: siluetas del barrio y, encima, sus monumentos
    (achicados y con bruma). Cada monumento aparece en pantalla cuando el
    personaje pasa por donde estaba en el dibujo viejo con la calle.
    De dia, el sol les aclara el borde; de noche tienen ventanitas prendidas,
    luces rojas de aviso y focos en los monumentos.
    """

    r = random.Random(7500 + n)

    azar = random.Random(9200 + n)

    es_de_noche = es_noche(cfg)

    W = ancho_capa(PARALLAX["lejos"])

    velocidad = (W - PANTALLA) / (ANCHO - PANTALLA)

    arriba, medio, abajo = (G.hx(c) for c in cfg["cielo"])

    l = Lienzo(W, ALTO)

    noche = cfg.get("noche", 0)

    base_sil = (70, 86, 130) if noche < 0.4 else (30, 36, 80)

    tonos = [0.30, 0.46]

    for i, nombre in enumerate(cfg["skyline"]):

        c = mezcla(abajo, base_sil, tonos[min(i, 1)])

        yb = LEJOS_BASE + 6 * i

        G.SKYLINES[nombre](l, yb, r, c)

        l.rect(0, yb, W - 1, ALTO - 1, c)

        if noche > 0.45:
            G.puntos_de_luz(l, c, 0.10, rgb("#ffd890"), r)

            # mas ventanitas, de varios colores
            G.puntos_de_luz(l, c, 0.05, rgb(azar.choice(["#fff0b0", "#ffb860", "#b8d8ff"])), azar)

    if es_de_noche:

        balizas_en_siluetas(l, azar, ef, 0.5)

    # monumentos
    todos = monumentos.cargar([n])[n]

    por_id = {m["id"]: m for m in todos}

    horizonte = G.hx(cfg["cielo"][2])

    sprites = {}

    for idm, cx in cfg["monumentos"]:

        spr = achicar_monumento(monumentos.construir(por_id[idm]))

        # bruma y hora del dia
        G.tenir(spr, horizonte, BRUMA_MONUMENTO)

        if "tinte" in cfg:

            col, t = cfg["tinte"]

            G.tenir(spr, G.hx(col), t)

        # aparece al centro de la pantalla cuando el personaje esta en cx
        # del dibujo viejo
        centro = (cx - PANTALLA / 2) * velocidad + PANTALLA / 2

        x = int(round(centro - spr.w / 2))

        x = max(2, min(W - spr.w - 2, x))

        luces = cfg.get("luces", 0.0) if es_de_noche else 0.0

        if luces > 0:
            luces_lejanas(spr, luces * 0.35, r)

        # de noche, un foco ilumina el monumento desde abajo
        if es_de_noche:

            halo(
                l, x + spr.w // 2, LEJOS_BASE - spr.h // 3,
                max(16, int(spr.w * 0.62)),
                G.hx(cfg.get("farola_luz", "#ffe28c")), 70
            )

        l.pegar(spr, x, LEJOS_BASE + 2 - spr.h)

        sprites[idm] = (x, spr.w, spr.h)

    # de dia, el sol le aclara el borde de arriba y el lado que da al sol
    if not es_de_noche:

        L.luz_de_borde(l, (255, 244, 210), 0.30, L.lado_del_sol(cfg))

    return l, sprites


# ==========================================================
# EDIFICIOS DEL MEDIO
# ==========================================================

NEON_COLORES = [
    (255, 90, 190), (90, 230, 255), (190, 140, 255), (120, 255, 170), (255, 150, 60),
    (255, 70, 90),
]


def hacer_medio(n, cfg, ef=None):
    """
    Los edificios del medio. De dia reflejan el sol en los vidrios y en el
    borde; de noche tienen ventanas prendidas, postes de luz y carteles de neon
    en las terrazas y luces rojas de aviso en los mas altos.
    """

    r = random.Random(7800 + n)

    azar = random.Random(9400 + n)

    noche = es_noche(cfg)

    lado = L.lado_del_sol(cfg)

    W = ancho_capa(PARALLAX["medio"])

    l = Lienzo(W, ALTO)

    cols = {
        "frances": ["#c9b79a", "#bfae9a", "#d0c0aa"],
        "default": ["#b8b0a4", "#c4b8a8", "#aeb4b8", "#c8bcae", "#b8a898"],
    }

    base_cols = [G.hx(c) for c in (cols["frances"] if "frances" in cfg["skyline"] else cols["default"])]

    f0, f1 = cfg.get("fondo_alto", (30, 66))

    if cfg.get("plaza", 0) > 0.3:
        alto_min, alto_max = 36, 74
    else:
        alto_min, alto_max = min(int(f0 * 1.5), 80), min(int(f1 * 1.7), 118)

    alto_min = max(alto_min, 40)

    arboles = cfg.get("arboles", [])

    edificios = []

    x = -4

    while x < W:

        w = r.randint(18, 40)

        h = r.randint(alto_min, alto_max)

        spr = E.fondo_edificio(w, h, r, dict(fachada=r.choice(base_cols)))

        l.pegar(spr, x, ALTO - h)

        edificios.append((x, ALTO - h, w, h))

        x += w - 1 + r.randint(0, 3)

        # algun arbol entre edificios
        if arboles and r.random() < cfg.get("prob_arbol", 0.3) * 0.8:

            tipo = G.elegir_pesos(arboles, r)

            ha = r.randint(30, 46)

            arbol(l, x + r.randint(0, 8), ALTO, ha, tipo, r.randint(0, 99999))

            x += int(ha * 0.7)

    horizonte = G.hx(cfg["cielo"][2])

    # los vidrios se buscan antes de la bruma (por su color)
    if noche:

        ventanas = L.elegir_ventanas(l, cfg.get("luces", 0.0) * 0.7, azar)

        multiplicar_rgb(l, np.full((ALTO, W), NOCHE_OSCURIDAD_MEDIO, np.float32))

    else:

        ventanas_dia = L.Ventanas(l)

    G.tenir(l, horizonte, BRUMA_MEDIO)

    if "tinte" in cfg:

        col, t = cfg["tinte"]

        G.tenir(l, G.hx(col), t)

    if not noche:

        L.reflejos_en_ventanas(
            l, 0.40, azar, G.hx(cfg["cielo"][1]), lado, ef, "medio",
            max_brillos=70, ventanas=ventanas_dia
        )

        L.luz_de_borde(l, (255, 244, 210), 0.30, lado)

        return l

    # ---- noche
    L.prender_ventanas(l, ventanas[0], ventanas[1], azar, cfg.get("paleta_luces", "calida"))

    color_luz = G.hx(cfg.get("farola_luz", "#ffe28c"))

    prob_neon = 0.5 if cfg.get("neon") else 0.12

    for x, y, w, h in edificios:

        # poste de luz en la terraza
        if w >= 20 and azar.random() < 0.55:

            px_ = x + 3 if azar.random() < 0.5 else x + w - 4

            halo(l, px_, y - 6, 11, color_luz, 120)

            L.luminaria_azotea(l, px_, y - 1, 5, color_luz, ef, "medio")

        # cartel de neon en la fachada
        if h > 50 and azar.random() < prob_neon:

            ancho = azar.randint(6, min(12, w - 6))

            L.letrero_neon(
                l, x + azar.randint(2, w - ancho - 2), y + azar.randint(10, int(h * 0.6)),
                ancho, azar.choice(NEON_COLORES), ef, "medio"
            )

        # los mas altos llevan una luz roja de aviso
        if h >= alto_max * 0.82 and azar.random() < 0.6:

            ax = x + w // 2

            l.rect(ax, y - 4, ax, y - 1, (44, 50, 90))

            L.antena_con_baliza(l, ax, y - 5, ef, "medio")

            halo(l, ax, y - 5, 4, (255, 70, 60), 110)

    return l


# ==========================================================
# ARMADO Y GUARDADO
# ==========================================================

# Las escaleras que quedan en la arena de un jefe: se dejan solo las que
# estan mas alla de ARENA_ESCALERAS_X, fuera de la pantalla. Hacen falta
# porque terreno.py toma "hay escaleras" como "el nivel tiene calle"; si no
# quedara ninguna, el jugador arrancaria arriba de un techo.
ARENA_ESCALERAS_X = ANCHO_ARENA + 800


def recortar_arena(datos):
    """
    Convierte el terreno de un nivel entero en la arena de un jefe: ancho
    corto y calle libre (sin escaleras al alcance). Se llama despues de
    verificar_terreno, que pide el nivel completo.
    """

    datos["ancho"] = ANCHO_ARENA

    datos["escaleras"] = [
        e for e in datos["escaleras"] if e["x"] > ARENA_ESCALERAS_X
    ]

    if not datos["escaleras"]:
        raise RuntimeError("arena sin escaleras lejanas: el juego la tomaria sin calle")

    return datos


def armar_nivel(n, verbose=True):

    cfg = NIVELES[n]

    r = random.Random(1000 + n)

    if cfg.get("interior"):

        # el nivel 1 es por dentro del colegio: un solo piso, sin techos
        datos = armar_terreno_interior(n)

    else:

        datos = armar_terreno(n, cfg)

        problemas = verificar_terreno(datos)

        if problemas:
            raise RuntimeError("nivel {}: {}".format(n, "; ".join(sorted(set(problemas)))))

        if cfg.get("jefe"):
            recortar_arena(datos)

        # el nivel 2 arranca justo en la puerta del Huergo (a unos 16 px de la
        # mitad del personaje, que mide como 32 de ancho)
        if cfg.get("puerta") == "huergo":
            datos["inicio_x"] = HR.ENTRADA_CX * PX - 16

    # lo que el juego anima en vivo (destellos, luz de farolas, balizas)
    ef = L.Efectos(random.Random(9000 + n))

    if cfg.get("interior"):

        # por dentro: las paredes llegan hasta el cielorraso (la capa cercana
        # tapa toda la pantalla); las capas lejanas son de reserva
        cercana = hacer_cercana_plana(n, cfg, datos, r, ef)

        medio = IH.capa_medio(
            ancho_capa(PARALLAX["medio"], HR.ANCHO_INTERIOR), ALTO, random.Random(7800 + n)
        )

        lejos = IH.capa_lejos(
            ancho_capa(PARALLAX["lejos"], HR.ANCHO_INTERIOR), ALTO, random.Random(7500 + n)
        )

        mons = {}

        cielo_img = IH.capa_cielo(ancho_capa(PARALLAX["cielo"], HR.ANCHO_INTERIOR), ALTO)

    else:

        cercana = hacer_cercana(n, cfg, datos, r, ef)

        medio = hacer_medio(n, cfg, ef)

        lejos, mons = hacer_lejos(n, cfg, ef)

        cielo_img = hacer_cielo(n, cfg, ef)

    if verbose:

        tiers = [e["tier"] for e in datos["edificios"]]

        print(
            "nivel {:2d} {:14s} edificios={:2d} (chicos {}, medianos {}, grandes {}) "
            "balcones={} {}".format(
                n, cfg["barrio"], len(tiers),
                tiers.count(0), tiers.count(1), tiers.count(2),
                len(datos["balcones"]),
                "NOCHE" if es_noche(cfg) else "dia"
            )
        )

    return dict(
        datos=datos, cercana=cercana, medio=medio, lejos=lejos,
        cielo=cielo_img, monumentos=mons, efectos=ef
    )


def guardar_nivel(n, nivel):

    os.makedirs(CARPETA_NIVELES, exist_ok=True)

    base = os.path.join(CARPETA_NIVELES, "nivel_{:02d}".format(n))

    nivel["cielo"].im.convert("RGB").save(base + "_cielo.png")

    nivel["lejos"].guardar(base + "_lejos.png")

    nivel["medio"].guardar(base + "_medio.png")

    nivel["cercana"].guardar(base + "_ciudad.png")

    with open(base + "_terreno.json", "w", encoding="utf-8") as f:

        json.dump(nivel["datos"], f, indent=1)

    with open(base + "_efectos.json", "w", encoding="utf-8") as f:

        json.dump(nivel["efectos"].a_dict(), f, separators=(",", ":"))


# Cuanto se mueve cada capa en vertical respecto de la camara (igual que en
# fondos_nivel.py)
PARALLAX_Y = dict(cielo=0.08, lejos=0.30, medio=0.60, ciudad=1.0)


def componer(nivel, camara_px, camara_y_px=0):
    """
    Como se ve la pantalla del juego con la camara en (camara_px, camara_y_px),
    sin personaje ni nubes. En pixeles de dibujo (267 x 200).
    """

    ancho_v = 800 // PX + 1

    # ancho del nivel en pixeles de dibujo (el nivel 1, por dentro, es mas corto)
    ancho_n = nivel["datos"]["ancho"] // PX if nivel["datos"].get("interior") else ANCHO

    pantalla = Image.new("RGBA", (ancho_v, ALTO), (0, 0, 0, 255))

    for nombre, clave in (("cielo", "cielo"), ("lejos", "lejos"), ("medio", "medio"), ("ciudad", "cercana")):

        capa = nivel[clave]

        if clave == "cercana":
            x = camara_px // PX
        else:
            vel = (capa.w - PANTALLA) / (ancho_n - PANTALLA)
            x = int(camara_px / PX * vel)

        x = max(0, min(capa.w - ancho_v, x))

        oy = -int(camara_y_px * PARALLAX_Y[nombre] / PX)

        corte = capa.im.crop((x, 0, x + ancho_v, capa.im.height))

        # el cielo se estira si no llega a tapar la pantalla
        if nombre == "cielo":

            if oy > 0:
                pantalla.paste(corte.getpixel((0, 0)), (0, 0, ancho_v, oy))

            bajo = oy + corte.height

            if bajo < ALTO:
                pantalla.paste(corte.getpixel((0, corte.height - 1)), (0, bajo, ancho_v, ALTO))

        destino_y = max(0, oy)

        origen_y = max(0, -oy)

        if origen_y >= corte.height or destino_y >= ALTO:
            continue

        corte = corte.crop((0, origen_y, ancho_v, corte.height))

        pantalla.alpha_composite(corte.convert("RGBA"), (0, destino_y))

    return pantalla


def vista_previa(n, nivel, carpeta):

    os.makedirs(carpeta, exist_ok=True)

    interior = nivel["datos"].get("interior")

    ancho_px = nivel["datos"]["ancho"] if interior else NIVEL_PX

    # por dentro solo hay un piso: no hay vista de los techos
    vistas = (("calle", FILA_CALLE * PX - 480),) if interior else (
        ("techos", 0), ("calle", FILA_CALLE * PX - 480)
    )

    for nombre, camara_y in vistas:

        paneles = []

        for k in range(6):

            camara = int(k * (ancho_px - 800) / 5)

            im = componer(nivel, camara, camara_y).convert("RGB")

            paneles.append(im.resize((im.width * 2, im.height * 2), Image.NEAREST))

        pw, ph = paneles[0].size

        m = Image.new("RGB", (pw * 2, ph * 3), (0, 0, 0))

        for i, p in enumerate(paneles):
            m.paste(p, ((i % 2) * pw, (i // 2) * ph))

        m.save(os.path.join(carpeta, "techos_nivel_{:02d}_{}.png".format(n, nombre)))

    # el nivel entero (capa cercana sobre el cielo), achicado
    tira = Image.new("RGBA", (nivel["cercana"].w, ALTO_CERCANA), (0, 0, 0, 255))

    tira.alpha_composite(nivel["cielo"].im.crop((0, 0, nivel["cielo"].w, ALTO)).convert("RGBA"), (0, 0))

    tira.alpha_composite(nivel["lejos"].im, (0, 0))

    tira.alpha_composite(nivel["cercana"].im, (0, 0))

    tira.convert("RGB").save(
        os.path.join(carpeta, "techos_nivel_{:02d}_tira.png".format(n))
    )


def main(argv):

    vista = "--vista" in argv

    numeros = [int(a) for a in argv if a.isdigit()]

    niveles = numeros or sorted(NIVELES)

    carpeta_vista = os.path.join(HERRAMIENTAS, "vistas")

    for n in niveles:

        nivel = armar_nivel(n)

        guardar_nivel(n, nivel)

        if vista:
            vista_previa(n, nivel, carpeta_vista)

    print("Listo:", CARPETA_NIVELES)


if __name__ == "__main__":

    main(sys.argv[1:])

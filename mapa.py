"""
Mapa de Buenos Aires (estilo mapa de Super Mario Bros 3).

Hay 15 niveles, puntos que arrancan en La Boca y terminan en La Boca.
La imagen ocupa toda la pantalla (la camara sigue al personaje) y el
personaje se mueve libremente por el mapa.

    - Punto blanco con borde azul: el nivel que toca jugar.
    - Punto negro: nivel completado o todavia bloqueado.
    - Al llegar a un punto aparece un globo de texto con el nivel (en gris
      si todavia esta bloqueado).
    - Al terminar un nivel el punto se vuelve negro y salen puntitos que
      guian hacia el proximo; se ponen negros cuando se pasa por encima.
    - Parado sobre el punto del nivel actual, ENTER (o ESPACIO) lo juega.
    - Tienda de San Telmo: aparece con la cara de la tienda (en gris hasta
      llegar al nivel 5). Al desbloquearla salen dos signos de
      exclamacion hasta que se entra por primera vez. Adentro se vende
      el chipa (10000 puntos = 1 vida): se ve el precio al pasar el mouse
      por encima y se compra con click. ESC para volver.
    - Mision de San Telmo: aparece con la cara del chico (en gris hasta
      llegar al nivel 3) y funciona igual que la tienda: signos de
      exclamacion al desbloquearse, ENTER para entrar. Adentro hay una
      pantalla negra que dice "MISION EN PROGRESO". ESC para volver.
"""

import math
import os
import sys

import pygame

from archivos import (
    TOTAL_NIVELES,
    cargar_mapa,
    cargar_puntos,
    cargar_vidas_extra,
    guardar_mapa,
    guardar_puntos,
    guardar_vidas_extra,
    marcar_mision_visitada,
    marcar_tienda_visitada,
    mision_visitada,
    nueva_vuelta,
    tienda_visitada
)
from pixel_font import FuentePixel


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

ANCHO, ALTO = 800, 600

FPS = 60

CARPETA = os.path.dirname(os.path.abspath(__file__))

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (20, 90, 255)
GRIS_CLARO = (175, 175, 175)
GRIS_OSCURO = (60, 60, 60)

# La imagen del mapa (1659 x 948) se escala al ALTO de la ventana: llena
# toda la pantalla sin deformarse. Como es mas ancha que la ventana, la
# camara se desplaza de costado siguiendo al personaje.
MAPA_ARCHIVO = os.path.join("assets", "fondos", "mapa_buenos_aires.png")

MAPA_ANCHO_ORIGINAL = 1659
MAPA_ALTO_ORIGINAL = 948

ESCALA_MAPA = ALTO / MAPA_ALTO_ORIGINAL

MAPA_ANCHO = round(MAPA_ANCHO_ORIGINAL * ESCALA_MAPA)

# Movimiento y animaciones
VELOCIDAD_MAPA = 170        # pixeles por segundo

SEPARACION_PUNTITOS = 20    # pixeles entre puntitos del camino

RADIO_PUNTITO = 12          # a esta distancia se "toca" un puntito

RADIO_GLOBO = 16            # a esta distancia de un nivel sale el globo

RADIO_ENTRADA = 14          # a esta distancia del nivel actual se puede entrar

ESCALA_PIXEL = 2            # tamano de cada pixel de los puntos y globos

REDUCCION_PERSONAJE = 2     # los sprites vienen escalados x2: se bajan a x1

TIEMPO_FRAME_CAMINATA = 0.11

# Animacion al terminar un nivel (segundos)
ESPERA_ANTES = 0.5          # quieto antes de empezar
PARPADEO_TOTAL = 0.9        # el punto parpadea y queda negro
PARPADEO_CADA = 0.15
PERIODO_PUNTITO = 0.05      # un puntito nuevo cada tanto


# ==========================================================
# NIVELES (x, y sobre la imagen original del mapa)
#
# Sale de La Boca, da toda la vuelta por la ciudad y vuelve a
# La Boca (la Bombonera).
# ==========================================================

NIVELES = [
    ("LA BOCA",         (1420, 800)),
    ("SAN TELMO",       (1245, 650)),
    ("PUERTO MADERO",   (1085, 455)),
    ("PLAZA DE MAYO",   (925, 420)),
    ("RETIRO",          (835, 300)),
    ("RECOLETA",        (580, 405)),
    ("BARRIO NORTE",    (420, 545)),
    ("PALERMO",         (330, 730)),
    ("ABASTO",          (560, 830)),
    ("ONCE",            (720, 740)),
    ("CONGRESO",        (830, 720)),
    ("OBELISCO",        (885, 550)),
    ("MONSERRAT",       (1010, 730)),
    ("CONSTITUCION",    (1130, 870)),
    ("LA BOMBONERA",    (1580, 775)),
]

# Curvas intermedias del camino entre un nivel y el siguiente
# (TRAMOS[i] va del nivel i al nivel i + 1)
TRAMOS = [
    [(1330, 730)],
    [(1190, 590), (1120, 500)],
    [(1000, 425)],
    [(870, 360)],
    [(700, 340)],
    [(480, 470)],
    [(360, 640)],
    [(430, 790)],
    [(640, 790)],
    [],
    [(850, 640)],
    [(960, 640)],
    [(1070, 800)],
    [(1300, 905), (1540, 905)],
]

assert len(NIVELES) == TOTAL_NIVELES
assert len(TRAMOS) == TOTAL_NIVELES - 1


# ==========================================================
# TIENDA DE SAN TELMO
# ==========================================================

# Posicion sobre la imagen original del mapa (al lado del nivel de San Telmo)
TIENDA_PUNTO = (1160, 655)

# Se desbloquea al llegar a este nivel (el nivel 5 es el que toca jugar
# cuando ya se completaron 4)
NIVEL_TIENDA = 5

TIENDA_CARPETA = os.path.join("assets", "tienda")

ESCALA_STAND = 8            # tamano del stand dentro de la tienda

ESCALA_CHIPA = 5            # tamano del chipa en el mostrador

# Fila (del dibujo del stand, sin borde transparente) donde empieza el
# mostrador de madera de abajo: ahi se apoya el chipa
FILA_MOSTRADOR = 46

PRECIO_CHIPA = 10000        # puntos que cuesta el chipa

VIDAS_CHIPA = 1             # vidas que da el chipa

DURACION_EFECTO = 0.9       # segundos que dura el efecto de la compra

DIBUJO_CORAZON = [
    ".BB.BB.",
    "BWWBWWB",
    "BWWWWWB",
    ".BWWWB.",
    "..BWB..",
    "...B...",
]

# ==========================================================
# MISION DE SAN TELMO
# ==========================================================

# Posicion sobre la imagen original del mapa (abajo del cartel de San Telmo)
MISION_PUNTO = (1225, 762)

# Se desbloquea al llegar a este nivel (el nivel 3 es el que toca jugar
# cuando ya se completaron 2)
NIVEL_MISION = 3

MISION_CARPETA = os.path.join("assets", "mision")

ESCALA_CARA_MISION = 2      # tamano de la cara en el mapa (el dibujo es chico)

ESCALA_TEXTO_MISION = 5     # tamano de las letras de la pantalla negra

TEXTO_MISION = "MISION EN PROGRESO"


ESCALA_EXCLAMACION = 2      # tamano de los signos de exclamacion

REBOTE_EXCLAMACION = 3      # pixeles que sube y baja la exclamacion

VELOCIDAD_REBOTE = 5.0      # rapidez del rebote (radianes por segundo)


# ==========================================================
# PIXEL ART DE LOS PUNTOS
# B = borde, W = relleno
# ==========================================================

DIBUJO_NIVEL = [
    "...BBBBB...",
    "..BWWWWWB..",
    ".BWWWWWWWB.",
    "BWWWWWWWWWB",
    "BWWWWWWWWWB",
    "BWWWWWWWWWB",
    "BWWWWWWWWWB",
    "BWWWWWWWWWB",
    ".BWWWWWWWB.",
    "..BWWWWWB..",
    "...BBBBB...",
]

DIBUJO_PUNTITO = [
    ".BBB.",
    "BWWWB",
    "BWWWB",
    "BWWWB",
    ".BBB.",
]


def crear_punto(dibujo, color_borde, color_relleno):
    """Pasa un dibujo de letras a una imagen pixel art."""

    alto = len(dibujo)
    ancho = len(dibujo[0])

    chica = pygame.Surface((ancho, alto), pygame.SRCALPHA)

    for y, fila in enumerate(dibujo):

        for x, celda in enumerate(fila):

            if celda == "B":

                chica.set_at((x, y), color_borde)

            elif celda == "W":

                chica.set_at((x, y), color_relleno)

    return pygame.transform.scale(
        chica,
        (ancho * ESCALA_PIXEL, alto * ESCALA_PIXEL)
    )


# ==========================================================
# CAMINO DE PUNTITOS (solo es una guia, no limita el movimiento)
# ==========================================================

def a_mapa(punto):
    """Pasa un punto de la imagen original a coordenadas del mapa."""

    return (punto[0] * ESCALA_MAPA, punto[1] * ESCALA_MAPA)


def crear_puntitos():
    """
    Puntitos que guian de un nivel al siguiente.
    Devuelve una lista por tramo: [[(x, y), ...], ...]
    """

    tramos = []

    for i in range(TOTAL_NIVELES - 1):

        vertices = (
            [a_mapa(NIVELES[i][1])]
            + [a_mapa(c) for c in TRAMOS[i]]
            + [a_mapa(NIVELES[i + 1][1])]
        )

        # Distancia acumulada del camino de este tramo
        acumulada = [0.0]

        for (x1, y1), (x2, y2) in zip(vertices, vertices[1:]):

            acumulada.append(
                acumulada[-1] + math.hypot(x2 - x1, y2 - y1)
            )

        largo = acumulada[-1]

        cantidad = max(2, round(largo / SEPARACION_PUNTITOS))

        puntitos = []

        for k in range(1, cantidad):

            d = k * largo / cantidad

            j = max(
                0,
                min(
                    len(vertices) - 2,
                    sum(1 for a in acumulada[1:-1] if a <= d)
                )
            )

            (x1, y1), (x2, y2) = vertices[j], vertices[j + 1]

            t = (d - acumulada[j]) / (acumulada[j + 1] - acumulada[j])

            puntitos.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t))

        tramos.append(puntitos)

    return tramos


# ==========================================================
# PERSONAJE EN EL MAPA
# ==========================================================

def _reducir(sprite):
    """Recorta el sprite al dibujo y lo baja a tamaño de mapa."""

    recorte = sprite.subsurface(sprite.get_bounding_rect()).copy()

    return pygame.transform.scale(
        recorte,
        (
            max(1, recorte.get_width() // REDUCCION_PERSONAJE),
            max(1, recorte.get_height() // REDUCCION_PERSONAJE)
        )
    )


def preparar_sprites_mapa(sprites):
    """
    Sprites chicos del personaje para el mapa. Todos quedan en un mismo
    lienzo con los pies abajo en el centro, para que no salte al caminar.
    """

    grupos = {
        "quieto_der": [sprites["idle_der"]],
        "quieto_izq": [sprites["idle_izq"]],
        "caminar_der": sprites["caminar_der"],
        "caminar_izq": sprites["caminar_izq"],
    }

    chicos = {
        nombre: [_reducir(s) for s in lista]
        for nombre, lista in grupos.items()
    }

    ancho = max(s.get_width() for lista in chicos.values() for s in lista)
    alto = max(s.get_height() for lista in chicos.values() for s in lista)

    resultado = {}

    for nombre, lista in chicos.items():

        resultado[nombre] = []

        for s in lista:

            lienzo = pygame.Surface((ancho, alto), pygame.SRCALPHA)

            lienzo.blit(
                s,
                s.get_rect(midbottom=(ancho // 2, alto))
            )

            resultado[nombre].append(lienzo)

    return resultado


# ==========================================================
# GLOBOS DE TEXTO PIXEL ART
# ==========================================================

def crear_globo(lineas, fuente, color_texto, color_borde, color_relleno,
                con_cola=True):
    """
    Globo de dialogo pixel art con el texto adentro. La cola (abajo, en
    el centro) apunta al personaje.
    """

    u = ESCALA_PIXEL

    textos = []

    for linea in lineas:

        t = fuente.render(linea, True, color_texto)

        textos.append(t.subsurface(t.get_bounding_rect()).copy())

    ancho_texto = max(t.get_width() for t in textos)

    alto_texto = sum(t.get_height() for t in textos) + u * 3 * (len(textos) - 1)

    relleno = 3 * u

    # Medidas en "pixeles de globo" (cada uno mide u pantalla)
    ancho_u = (ancho_texto + 2 * relleno) // u + 2

    ancho_u += ancho_u % 2     # par, para que la cola quede centrada

    alto_u = (alto_texto + 2 * relleno) // u + 2

    cola_u = 3 if con_cola else 0

    chico = pygame.Surface((ancho_u, alto_u + cola_u), pygame.SRCALPHA)

    chico.fill((0, 0, 0, 0))

    # Borde y relleno
    pygame.draw.rect(chico, color_borde, (0, 0, ancho_u, alto_u))

    pygame.draw.rect(chico, color_relleno, (1, 1, ancho_u - 2, alto_u - 2))

    # Esquinas cortadas
    for x, y, dx, dy in (
        (0, 0, 1, 1),
        (ancho_u - 1, 0, -1, 1),
        (0, alto_u - 1, 1, -1),
        (ancho_u - 1, alto_u - 1, -1, -1)
    ):

        chico.set_at((x, y), (0, 0, 0, 0))

        chico.set_at((x + dx, y), color_borde)

        chico.set_at((x, y + dy), color_borde)

        chico.set_at((x + dx, y + dy), color_borde)

    if con_cola:

        c = ancho_u // 2

        fila = alto_u - 1

        # Abertura en el borde de abajo
        for x in range(c - 2, c + 2):

            chico.set_at((x, fila), color_relleno)

        # Cola: filas que se van achicando hasta la punta
        chico.set_at((c - 3, fila + 1), color_borde)
        chico.set_at((c + 2, fila + 1), color_borde)

        for x in range(c - 2, c + 2):

            chico.set_at((x, fila + 1), color_relleno)

        chico.set_at((c - 2, fila + 2), color_borde)
        chico.set_at((c + 1, fila + 2), color_borde)

        for x in range(c - 1, c + 1):

            chico.set_at((x, fila + 2), color_relleno)

        chico.set_at((c - 1, fila + 3), color_borde)
        chico.set_at((c, fila + 3), color_borde)

    globo = pygame.transform.scale(
        chico,
        (chico.get_width() * u, chico.get_height() * u)
    )

    # Texto centrado en la parte del cuerpo del globo
    y = (alto_u * u - alto_texto) // 2

    for t in textos:

        globo.blit(t, ((ancho_u * u - t.get_width()) // 2, y))

        y += t.get_height() + u * 3

    return globo


# ==========================================================
# IMAGENES DE LA TIENDA
# ==========================================================

def _cargar_recortada(nombre, escala=1, carpeta=TIENDA_CARPETA):
    """Carga una imagen de assets/<carpeta> sin el borde transparente."""

    imagen = pygame.image.load(
        os.path.join(CARPETA, carpeta, nombre)
    ).convert_alpha()

    recorte = imagen.subsurface(imagen.get_bounding_rect()).copy()

    if escala != 1:

        recorte = pygame.transform.scale(
            recorte,
            (recorte.get_width() * escala, recorte.get_height() * escala)
        )

    return recorte


def _en_gris(imagen):
    """La misma imagen en gris (para la tienda todavia bloqueada)."""

    gris = imagen.copy()

    for y in range(gris.get_height()):

        for x in range(gris.get_width()):

            r, g, b, a = gris.get_at((x, y))

            if a:

                # Gris apagado: se achica el contraste para que se note
                # que esta bloqueada
                v = int((r * 0.3 + g * 0.59 + b * 0.11) * 0.5 + 70)

                gris.set_at((x, y), (v, v, v, a))

    return gris


# ==========================================================
# RECURSOS (se cargan una sola vez)
# ==========================================================

_recursos = {}


def _cargar_recursos():

    if _recursos:

        return _recursos

    imagen = pygame.image.load(
        os.path.join(CARPETA, MAPA_ARCHIVO)
    ).convert()

    _recursos["mapa"] = pygame.transform.smoothscale(
        imagen,
        (MAPA_ANCHO, ALTO)
    )

    _recursos["nivel_blanco"] = crear_punto(DIBUJO_NIVEL, AZUL, BLANCO)
    _recursos["nivel_negro"] = crear_punto(DIBUJO_NIVEL, NEGRO, NEGRO)
    _recursos["puntito_blanco"] = crear_punto(DIBUJO_PUNTITO, AZUL, BLANCO)
    _recursos["puntito_negro"] = crear_punto(DIBUJO_PUNTITO, NEGRO, NEGRO)

    _recursos["puntitos"] = crear_puntitos()

    fuente = FuentePixel(2)

    # Globos de "NIVEL n": blancos si se puede/pudo jugar, grises si el
    # nivel todavia esta bloqueado
    _recursos["globos"] = {}

    for n in range(1, TOTAL_NIVELES + 1):

        texto = "NIVEL %d" % n

        _recursos["globos"][(n, False)] = crear_globo(
            [texto], fuente, NEGRO, NEGRO, BLANCO
        )

        _recursos["globos"][(n, True)] = crear_globo(
            [texto], fuente, GRIS_OSCURO, GRIS_OSCURO, GRIS_CLARO
        )

    # Tienda de San Telmo: cara (gris si esta bloqueada), exclamaciones,
    # stand de adentro y sus globos
    cara = _cargar_recortada("icono_tienda.png")

    _recursos["tienda_cara"] = cara
    _recursos["tienda_cara_gris"] = _en_gris(cara)
    _recursos["tienda_exclamacion"] = _cargar_recortada(
        "exclamacion.png", ESCALA_EXCLAMACION
    )
    _recursos["tienda_stand"] = _cargar_recortada(
        "stand_parashop.png", ESCALA_STAND
    )
    _recursos["tienda_chipa"] = _cargar_recortada(
        "chipa.png", ESCALA_CHIPA
    )

    # Fondo de la tienda: se escala para cubrir la ventana y se recorta
    # el sobrante de los costados (sin deformar la imagen)
    fondo = pygame.image.load(
        os.path.join(CARPETA, TIENDA_CARPETA, "fondo_tienda.png")
    ).convert()

    escala_fondo = max(ANCHO / fondo.get_width(), ALTO / fondo.get_height())

    fondo = pygame.transform.smoothscale(
        fondo,
        (
            round(fondo.get_width() * escala_fondo),
            round(fondo.get_height() * escala_fondo)
        )
    )

    _recursos["tienda_fondo"] = fondo.subsurface(
        (
            (fondo.get_width() - ANCHO) // 2,
            (fondo.get_height() - ALTO) // 2,
            ANCHO,
            ALTO
        )
    ).copy()

    _recursos["fuente"] = fuente

    _recursos["globo_tienda"] = crear_globo(
        ["TIENDA"], fuente, NEGRO, NEGRO, BLANCO
    )

    _recursos["globo_tienda_bloqueada"] = crear_globo(
        ["TIENDA", "NIVEL %d" % NIVEL_TIENDA],
        fuente, GRIS_OSCURO, GRIS_OSCURO, GRIS_CLARO
    )

    # Mision de San Telmo: cara (gris si esta bloqueada) y sus globos
    cara_mision = _cargar_recortada(
        "icono_mision.png", ESCALA_CARA_MISION, MISION_CARPETA
    )

    _recursos["mision_cara"] = cara_mision
    _recursos["mision_cara_gris"] = _en_gris(cara_mision)

    _recursos["globo_mision"] = crear_globo(
        ["MISION"], fuente, NEGRO, NEGRO, BLANCO
    )

    _recursos["globo_mision_bloqueada"] = crear_globo(
        ["MISION", "NIVEL %d" % NIVEL_MISION],
        fuente, GRIS_OSCURO, GRIS_OSCURO, GRIS_CLARO
    )

    _recursos["texto_mision"] = FuentePixel(ESCALA_TEXTO_MISION).render(
        TEXTO_MISION, True, BLANCO
    )

    # Cartel del final (sin cola, arriba en el centro de la pantalla)
    _recursos["globo_final"] = crear_globo(
        ["¡FELICITACIONES!", "ENTER PARA SALIR"],
        fuente, NEGRO, NEGRO, BLANCO, con_cola=False
    )

    return _recursos


# ==========================================================
# PANTALLA DE LA TIENDA (vende el chipa)
# ==========================================================

# (color del texto, color del borde, color del relleno) de cada globo
ESTILOS_GLOBO = {
    "blanco": (NEGRO, NEGRO, BLANCO),
    "gris": (GRIS_OSCURO, GRIS_OSCURO, GRIS_CLARO),
}


def pantalla_tienda(pantalla, reloj, rec):
    """
    Tienda de San Telmo. Sin textos: solo el stand abajo, en el centro de
    la pantalla, con el chipa apoyado en el mostrador.

        mouse sobre el chipa -> aparece el precio (gris si no alcanzan
                                los puntos)
        click en el chipa    -> lo compra: cuesta PRECIO_CHIPA puntos y da
                                una vida extra (se guarda en
                                vidas_extra.txt hasta que se use). Sale un
                                corazoncito. Si no alcanzan los puntos, el
                                chipa tiembla.
        ESC                  -> vuelve al mapa

    Devuelve True si se cerro la ventana, False si se volvio con ESC.
    """

    fuente = rec["fuente"]

    fondo = rec["tienda_fondo"]

    stand = rec["tienda_stand"]

    chipa = rec["tienda_chipa"]

    corazon = pygame.transform.scale(
        crear_punto(DIBUJO_CORAZON, (110, 0, 25), (240, 35, 65)),
        (14 * 2, 12 * 2)
    )

    puntos = cargar_puntos()

    extras = cargar_vidas_extra()

    # Stand abajo de todo, apoyado en el borde de la pantalla y centrado
    rect_stand = stand.get_rect(midbottom=(ANCHO // 2, ALTO))

    # Chipa apoyado en la madera del mostrador, centrado
    base_mostrador = rect_stand.top + FILA_MOSTRADOR * ESCALA_STAND + 8

    rect_chipa = chipa.get_rect(
        midbottom=(rect_stand.centerx, base_mostrador)
    )

    corazones = []          # [x, y, segundos_de_vida]

    t_tiembla = 0.0         # sin puntos: el chipa tiembla

    t_salta = 0.0           # recien comprado: el chipa pega un saltito

    t = 0.0

    cache = {}

    def globo(lineas, estilo):
        """Globos pixel art; se arman una sola vez y se guardan."""

        clave = (tuple(lineas), estilo)

        if clave not in cache:

            texto, borde, relleno = ESTILOS_GLOBO[estilo]

            cache[clave] = crear_globo(
                lineas, fuente, texto, borde, relleno, con_cola=False
            )

        return cache[clave]

    def cursor(hay_mano):

        try:

            pygame.mouse.set_cursor(
                pygame.SYSTEM_CURSOR_HAND if hay_mano
                else pygame.SYSTEM_CURSOR_ARROW
            )

        except (pygame.error, AttributeError):

            pass

    mano = False

    while True:

        dt = min(reloj.tick(FPS) / 1000.0, 0.05)

        t += dt

        t_tiembla = max(0.0, t_tiembla - dt)

        t_salta = max(0.0, t_salta - dt)

        mouse = pygame.mouse.get_pos()

        encima = rect_chipa.collidepoint(mouse)

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                cursor(False)

                return True

            if evento.type == pygame.KEYDOWN:

                if evento.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):

                    cursor(False)

                    return False

            # Se compra clickeando el chipa (no con el teclado)
            if (
                evento.type == pygame.MOUSEBUTTONDOWN
                and evento.button == 1
                and rect_chipa.collidepoint(evento.pos)
            ):

                if puntos >= PRECIO_CHIPA:

                    puntos -= PRECIO_CHIPA

                    extras += VIDAS_CHIPA

                    guardar_puntos(puntos)

                    guardar_vidas_extra(extras)

                    t_salta = DURACION_EFECTO / 2

                    corazones.append(
                        [rect_chipa.centerx, rect_chipa.top - 4, DURACION_EFECTO]
                    )

                else:

                    t_tiembla = DURACION_EFECTO / 2

        # Manito cuando el mouse esta sobre el chipa
        if encima != mano:

            mano = encima

            cursor(mano)

        # ----- fondo y stand -----
        pantalla.blit(fondo, (0, 0))

        pantalla.blit(stand, rect_stand)

        # ----- chipa -----
        dx = 0

        dy = 0

        if t_tiembla > 0:

            dx = round(math.sin(t * 60) * 5)

        if t_salta > 0:

            fase = 1 - t_salta / (DURACION_EFECTO / 2)

            dy = -round(math.sin(fase * math.pi) * 14)

        imagen = chipa

        if encima:

            # Un poquito mas grande para que se note que se puede clickear
            imagen = pygame.transform.scale(
                chipa,
                (chipa.get_width() + 8, chipa.get_height() + 8)
            )

        pantalla.blit(
            imagen,
            imagen.get_rect(
                midbottom=(rect_chipa.centerx + dx, rect_chipa.bottom + dy)
            )
        )

        # ----- corazones que suben al comprar -----
        for c in corazones:

            c[1] -= 60 * dt

            c[2] -= dt

            h = corazon.copy()

            h.set_alpha(max(0, min(255, int(255 * c[2] / DURACION_EFECTO))))

            pantalla.blit(h, h.get_rect(center=(round(c[0]), round(c[1]))))

        corazones = [c for c in corazones if c[2] > 0]

        # ----- precio al pasar el mouse -----
        if encima:

            cartel = globo(
                ["%d PUNTOS" % PRECIO_CHIPA],
                "blanco" if puntos >= PRECIO_CHIPA else "gris"
            )

            # Al costado del cursor, para no tapar el chipa
            rect_cartel = cartel.get_rect(
                topleft=(mouse[0] + 16, mouse[1] + 6)
            )

            rect_cartel.clamp_ip(pantalla.get_rect())

            pantalla.blit(cartel, rect_cartel)

        pygame.display.flip()


# ==========================================================
# PANTALLA DE LA MISION (por ahora solo el cartel)
# ==========================================================

def pantalla_mision(pantalla, reloj, rec):
    """
    Mision de San Telmo: pantalla negra con "MISION EN PROGRESO" y nada
    mas. ESC vuelve al mapa.

    Devuelve True si se cerro la ventana, False si se volvio con ESC.
    """

    texto = rec["texto_mision"]

    while True:

        reloj.tick(FPS)

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                return True

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:

                return False

        pantalla.fill(NEGRO)

        pantalla.blit(
            texto,
            texto.get_rect(center=(ANCHO // 2, ALTO // 2))
        )

        pygame.display.flip()


# ==========================================================
# PANTALLA DEL MAPA
# ==========================================================

def pantalla_mapa(pantalla, reloj, sprites, animar_completado=False):
    """
    Devuelve:
        "jugar" -> el jugador entro al nivel que tiene bajo los pies
        "menu"  -> volvio al menu (ESC o termino los 15 niveles)

    animar_completado=True se usa cuando se viene de terminar un nivel:
    el punto se vuelve negro y salen los puntitos hacia el siguiente.
    """

    rec = _cargar_recursos()

    puntitos = rec["puntitos"]

    sprites_mapa = preparar_sprites_mapa(sprites)

    completados, x_guardada, y_guardada, tocados = cargar_mapa()

    tocados = set(tocados)

    fin = completados >= TOTAL_NIVELES

    # La tienda de San Telmo se desbloquea al llegar al nivel 5
    tienda_abierta = completados >= NIVEL_TIENDA - 1

    tienda_vista = tienda_visitada()

    tx, ty = a_mapa(TIENDA_PUNTO)

    # La mision de San Telmo se desbloquea al llegar al nivel 3
    mision_abierta = completados >= NIVEL_MISION - 1

    mision_vista = mision_visitada()

    mx, my = a_mapa(MISION_PUNTO)

    t_reloj = 0.0

    # El nivel que toca jugar (o el ultimo, si ya esta todo completo)
    actual = min(completados, TOTAL_NIVELES - 1)

    # Posicion del personaje (coordenadas del mapa ya escalado)
    if x_guardada is None or y_guardada is None:

        px, py = a_mapa(NIVELES[actual][1])

    else:

        px, py = a_mapa((x_guardada, y_guardada))

    # Despues de terminar un nivel el personaje esta parado en su punto
    animando = animar_completado and completados > 0

    if animando:

        px, py = a_mapa(NIVELES[completados - 1][1])

        tocados = set()

    t_anim = 0.0

    mirando_derecha = True

    t_caminata = 0.0

    def guardar():

        guardar_mapa(
            completados,
            px / ESCALA_MAPA,
            py / ESCALA_MAPA,
            tocados
        )

    while True:

        dt = min(reloj.tick(FPS) / 1000.0, 0.05)

        t_reloj += dt

        # ==================================================
        # EVENTOS
        # ==================================================

        quiere_entrar = False

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                guardar()

                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:

                    guardar()

                    return "menu"

                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):

                    quiere_entrar = True

        # ==================================================
        # ANIMACIÓN DE NIVEL COMPLETADO
        # ==================================================

        if animando:

            t_anim += dt

            nuevos = (
                len(puntitos[completados - 1])
                if completados - 1 < len(puntitos)
                else 0
            )

            if t_anim >= ESPERA_ANTES + PARPADEO_TOTAL + nuevos * PERIODO_PUNTITO:

                animando = False

        # ==================================================
        # MOVIMIENTO LIBRE
        # ==================================================

        moviendose = False

        if not animando:

            teclas = pygame.key.get_pressed()

            vx = (
                (teclas[pygame.K_RIGHT] or teclas[pygame.K_d])
                - (teclas[pygame.K_LEFT] or teclas[pygame.K_a])
            )

            vy = (
                (teclas[pygame.K_DOWN] or teclas[pygame.K_s])
                - (teclas[pygame.K_UP] or teclas[pygame.K_w])
            )

            if vx or vy:

                largo_v = math.hypot(vx, vy)

                px += vx / largo_v * VELOCIDAD_MAPA * dt
                py += vy / largo_v * VELOCIDAD_MAPA * dt

                # No se sale de la imagen
                px = max(10, min(MAPA_ANCHO - 10, px))
                py = max(30, min(ALTO - 6, py))

                moviendose = True

                if vx:

                    mirando_derecha = vx > 0

            # Los puntitos del camino actual que se tocan se vuelven negros
            if completados > 0 and completados - 1 < len(puntitos):

                for k, (x, y) in enumerate(puntitos[completados - 1]):

                    if math.hypot(px - x, py - y) <= RADIO_PUNTITO:

                        tocados.add(k)

        # ==================================================
        # ENTRAR AL NIVEL / TERMINAR EL JUEGO
        # ==================================================

        nx, ny = a_mapa(NIVELES[actual][1])

        parado_en_nivel = (
            not fin
            and not animando
            and math.hypot(px - nx, py - ny) <= RADIO_ENTRADA
        )

        parado_en_tienda = (
            tienda_abierta
            and not animando
            and math.hypot(px - tx, py - ty) <= RADIO_ENTRADA
        )

        parado_en_mision = (
            mision_abierta
            and not animando
            and math.hypot(px - mx, py - my) <= RADIO_ENTRADA
        )

        if quiere_entrar and parado_en_mision:

            mision_vista = True

            marcar_mision_visitada()

            guardar()

            if pantalla_mision(pantalla, reloj, rec):

                pygame.quit()
                sys.exit()

            continue

        if quiere_entrar and parado_en_tienda:

            tienda_vista = True

            marcar_tienda_visitada()

            guardar()

            if pantalla_tienda(pantalla, reloj, rec):

                pygame.quit()
                sys.exit()

            continue

        if quiere_entrar and not animando:

            if fin:

                # Dio toda la vuelta: se empieza de nuevo
                nueva_vuelta()

                return "menu"

            if parado_en_nivel:

                px, py = nx, ny

                guardar()

                return "jugar"

        # ==================================================
        # CÁMARA (sigue al personaje y no se sale de la imagen)
        # ==================================================

        camara_x = round(
            max(0, min(MAPA_ANCHO - ANCHO, px - ANCHO // 2))
        )

        # ==================================================
        # DIBUJAR
        # ==================================================

        pantalla.blit(rec["mapa"], (-camara_x, 0))

        # ----- puntitos del camino -----
        for tramo, lista in enumerate(puntitos):

            if tramo > completados - 1:

                break

            # En el tramo recien desbloqueado salen de a uno
            if animando and tramo == completados - 1:

                visibles = max(
                    0,
                    int(
                        (t_anim - ESPERA_ANTES - PARPADEO_TOTAL)
                        / PERIODO_PUNTITO
                    )
                )

            else:

                visibles = len(lista)

            for k, (x, y) in enumerate(lista[:visibles]):

                negro = tramo < completados - 1 or k in tocados

                imagen = (
                    rec["puntito_negro"] if negro else rec["puntito_blanco"]
                )

                pantalla.blit(
                    imagen,
                    imagen.get_rect(center=(round(x) - camara_x, round(y)))
                )

        # ----- puntos de nivel -----
        for i, (_, punto) in enumerate(NIVELES):

            # Solo el nivel que toca jugar esta en blanco; los completados
            # y los que todavia no se desbloquearon estan en negro
            blanco = i == completados

            # El que se acaba de completar parpadea y queda negro
            if animando and i == completados - 1:

                t = t_anim - ESPERA_ANTES

                if t < 0:

                    blanco = True

                elif t < PARPADEO_TOTAL:

                    blanco = int(t / PARPADEO_CADA) % 2 == 1

            imagen = (
                rec["nivel_blanco"] if blanco else rec["nivel_negro"]
            )

            x, y = a_mapa(punto)

            pantalla.blit(
                imagen,
                imagen.get_rect(center=(round(x) - camara_x, round(y)))
            )

        # ----- tienda de San Telmo -----
        cara = (
            rec["tienda_cara"] if tienda_abierta else rec["tienda_cara_gris"]
        )

        rect_cara = cara.get_rect(center=(round(tx) - camara_x, round(ty)))

        pantalla.blit(cara, rect_cara)

        # Desbloqueada y todavia sin entrar: exclamaciones que rebotan
        if tienda_abierta and not tienda_vista:

            excl = rec["tienda_exclamacion"]

            rebote = round(
                math.sin(t_reloj * VELOCIDAD_REBOTE) * REBOTE_EXCLAMACION
            )

            pantalla.blit(
                excl,
                excl.get_rect(
                    midbottom=(rect_cara.centerx, rect_cara.top - 2 + rebote)
                )
            )

        # ----- mision de San Telmo -----
        cara_m = (
            rec["mision_cara"] if mision_abierta else rec["mision_cara_gris"]
        )

        rect_cara_m = cara_m.get_rect(
            center=(round(mx) - camara_x, round(my))
        )

        pantalla.blit(cara_m, rect_cara_m)

        # Desbloqueada y todavia sin entrar: exclamaciones que rebotan
        if mision_abierta and not mision_vista:

            excl = rec["tienda_exclamacion"]

            rebote = round(
                math.sin(t_reloj * VELOCIDAD_REBOTE) * REBOTE_EXCLAMACION
            )

            pantalla.blit(
                excl,
                excl.get_rect(
                    midbottom=(
                        rect_cara_m.centerx, rect_cara_m.top - 2 + rebote
                    )
                )
            )

        # ----- personaje -----
        if moviendose:

            t_caminata += dt

            lista = sprites_mapa[
                "caminar_der" if mirando_derecha else "caminar_izq"
            ]

            sprite = lista[
                int(t_caminata / TIEMPO_FRAME_CAMINATA) % len(lista)
            ]

        else:

            t_caminata = 0.0

            sprite = sprites_mapa[
                "quieto_der" if mirando_derecha else "quieto_izq"
            ][0]

        rect_personaje = sprite.get_rect(
            midbottom=(round(px) - camara_x, round(py) + 4)
        )

        pantalla.blit(sprite, rect_personaje)

        # ----- globo con el nivel en el que se esta -----
        cerca = None

        for i, (_, punto) in enumerate(NIVELES):

            x, y = a_mapa(punto)

            if math.hypot(px - x, py - y) <= RADIO_GLOBO:

                cerca = i

        if cerca is not None:

            # Bloqueado: todavia no se llego a ese nivel
            bloqueado = cerca > completados

            globo = rec["globos"][(cerca + 1, bloqueado)]

            rect_globo = globo.get_rect(
                midbottom=(rect_personaje.centerx, rect_personaje.top - 2)
            )

            rect_globo.clamp_ip(pantalla.get_rect())

            pantalla.blit(globo, rect_globo)

        # ----- globo de la tienda -----
        if cerca is None and math.hypot(px - tx, py - ty) <= RADIO_GLOBO:

            globo = (
                rec["globo_tienda"]
                if tienda_abierta
                else rec["globo_tienda_bloqueada"]
            )

            rect_globo = globo.get_rect(
                midbottom=(rect_personaje.centerx, rect_personaje.top - 2)
            )

            rect_globo.clamp_ip(pantalla.get_rect())

            pantalla.blit(globo, rect_globo)

        # ----- globo de la mision -----
        if cerca is None and math.hypot(px - mx, py - my) <= RADIO_GLOBO:

            globo = (
                rec["globo_mision"]
                if mision_abierta
                else rec["globo_mision_bloqueada"]
            )

            rect_globo = globo.get_rect(
                midbottom=(rect_personaje.centerx, rect_personaje.top - 2)
            )

            rect_globo.clamp_ip(pantalla.get_rect())

            pantalla.blit(globo, rect_globo)

        # ----- cartel del final -----
        if fin and not animando:

            globo = rec["globo_final"]

            pantalla.blit(globo, globo.get_rect(midtop=(ANCHO // 2, 16)))

        pygame.display.flip()

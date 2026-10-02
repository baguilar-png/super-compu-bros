"""
Transición de círculo (iris) entre pantallas.

Orden de la animación:

    1. Se CIERRA el círculo sobre la pantalla en la que estabas
       (el menú, el nivel, el mapa... sigue viéndose mientras se cierra).
    2. Queda un instante en negro.
    3. Se ABRE el círculo y aparece la pantalla nueva.

Uso:

    import transicion

    transicion.cerrar_circulo(pantalla, reloj)   # bloquea hasta cerrar
    ...cambiar de pantalla / nivel...
    transicion.abrir_circulo()                   # se abre solo, sobre
                                                 # los próximos frames

abrir_circulo() NO bloquea: deja armada la apertura y el círculo se
va abriendo sobre los siguientes pygame.display.flip() de la pantalla
nueva. Por eso no hay que tocar el bucle de cada pantalla.

El círculo se dibuja en "celdas" (CELDA x CELDA píxeles) para que tenga
el mismo look pixel art que los frames del círculo (pixil-frame).
"""

import math
import sys

import pygame


# ==========================================================
# AJUSTES (tocá estos números para cambiar la sensación)
# ==========================================================

# Tamaño de cada "pixel" del círculo. Más grande = más pixelado
# (el frame de 17x17 escalado a la ventana sería ~47), más chico = más
# suave.
CELDA = 10

# Duraciones en segundos
DURACION_CIERRE = 0.55
DURACION_APERTURA = 0.60

# Cuánto queda la pantalla en negro entre el cierre y la apertura
PAUSA_NEGRO = 0.12

FPS = 60

NEGRO = (0, 0, 0)


# ==========================================================
# ESTADO INTERNO
# ==========================================================

# Se guarda el flip real de pygame para poder reemplazarlo por uno que
# dibuja el círculo encima mientras hay una apertura en curso.
_flip_original = pygame.display.flip

# None = no hay apertura en curso. Si hay, es un diccionario con
# "inicio" (ms, se completa en el primer flip) y "centro".
_apertura = None


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

def _suave(t):
    """Ease in-out (arranca y frena despacio) para que sea fluido."""

    t = max(0.0, min(1.0, t))

    if t < 0.5:

        return 4 * t * t * t

    return 1 - ((-2 * t + 2) ** 3) / 2


def _radio_maximo(ancho, alto, centro):
    """Radio (en celdas) con el que el círculo ya cubre toda la pantalla."""

    cx, cy = centro

    lejos_x = max(cx, ancho - cx)
    lejos_y = max(cy, alto - cy)

    return math.hypot(lejos_x, lejos_y) / CELDA + 1.5


def dibujar_iris(superficie, radio, centro, celda=None):
    """
    Pinta de negro todo lo que queda FUERA de un círculo pixelado.

    radio  -> radio del círculo en celdas (0 = todo negro)
    centro -> (x, y) en píxeles
    """

    if celda is None:

        celda = CELDA

    ancho, alto = superficie.get_size()

    cx = centro[0] / celda
    cy = centro[1] / celda

    columnas = math.ceil(ancho / celda)
    filas = math.ceil(alto / celda)

    radio2 = radio * radio

    for j in range(filas):

        y = j * celda

        dy = j + 0.5 - cy

        resto = radio2 - dy * dy

        # Fila fuera del círculo: toda negra
        if radio <= 0 or resto < 0:

            superficie.fill(NEGRO, (0, y, ancho, celda))

            continue

        mitad = math.sqrt(resto)

        # Primera y última celda cuyo centro cae dentro del círculo
        primera = math.ceil(cx - mitad - 0.5)
        ultima = math.floor(cx + mitad - 0.5)

        if ultima < primera:

            superficie.fill(NEGRO, (0, y, ancho, celda))

            continue

        if primera > 0:

            superficie.fill(NEGRO, (0, y, primera * celda, celda))

        if ultima < columnas - 1:

            x_der = (ultima + 1) * celda

            superficie.fill(NEGRO, (x_der, y, ancho - x_der, celda))


def _vaciar_eventos():
    """
    Durante la transición los clicks y teclas se ignoran (así no se
    apreta dos veces un botón). Cerrar la ventana sí funciona.
    """

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            pygame.quit()
            sys.exit()


# ==========================================================
# CERRAR EL CÍRCULO (bloquea hasta terminar)
# ==========================================================

def cerrar_circulo(pantalla, reloj, centro=None):
    """
    Cierra el círculo sobre lo que haya en pantalla en este momento y
    deja un instante en negro. La pantalla de antes se sigue viendo
    mientras se cierra.
    """

    global _apertura

    # Si se estaba abriendo otro círculo, se cancela
    _apertura = None

    ancho, alto = pantalla.get_size()

    if centro is None:

        centro = (ancho // 2, alto // 2)

    # Foto de la pantalla actual: es la que se va quedando atrás
    foto = pantalla.copy()

    radio_max = _radio_maximo(ancho, alto, centro)

    inicio = pygame.time.get_ticks()

    while True:

        t = (pygame.time.get_ticks() - inicio) / 1000.0 / DURACION_CIERRE

        if t >= 1:

            break

        _vaciar_eventos()

        pantalla.blit(foto, (0, 0))

        dibujar_iris(
            pantalla,
            radio_max * (1 - _suave(t)),
            centro
        )

        _flip_original()

        reloj.tick(FPS)

    # Totalmente cerrado: un ratito en negro
    pantalla.fill(NEGRO)

    inicio = pygame.time.get_ticks()

    while pygame.time.get_ticks() - inicio < PAUSA_NEGRO * 1000:

        _vaciar_eventos()

        _flip_original()

        reloj.tick(FPS)


# ==========================================================
# ABRIR EL CÍRCULO (no bloquea)
# ==========================================================

def abrir_circulo(centro=None):
    """
    Deja armada la apertura: el círculo se va a abrir sobre los
    próximos frames de la pantalla nueva.
    """

    global _apertura

    _apertura = {
        "inicio": None,
        "centro": centro
    }


def _flip_con_iris():
    """
    Reemplaza a pygame.display.flip(). Si hay una apertura en curso,
    dibuja el círculo encima del frame; si no, hace el flip normal.
    """

    global _apertura

    apertura = _apertura

    if apertura is None:

        _flip_original()

        return

    pantalla = pygame.display.get_surface()

    ancho, alto = pantalla.get_size()

    centro = apertura["centro"] or (ancho // 2, alto // 2)

    # El reloj arranca en el primer frame real de la pantalla nueva
    # (así lo que tarda en cargarse no se come la animación)
    if apertura["inicio"] is None:

        apertura["inicio"] = pygame.time.get_ticks()

    t = (
        (pygame.time.get_ticks() - apertura["inicio"])
        / 1000.0
        / DURACION_APERTURA
    )

    if t >= 1:

        _apertura = None

        _flip_original()

        return

    # Se guarda el frame limpio para devolverlo después del flip
    # (si no, el círculo negro quedaría "pegado" en la superficie)
    limpio = pantalla.copy()

    dibujar_iris(
        pantalla,
        _radio_maximo(ancho, alto, centro) * _suave(t),
        centro
    )

    _flip_original()

    pantalla.blit(limpio, (0, 0))


# Todas las pantallas llaman a pygame.display.flip(): se reemplaza por
# la versión que sabe dibujar el círculo mientras se abre.
pygame.display.flip = _flip_con_iris

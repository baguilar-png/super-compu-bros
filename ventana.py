"""
Modos de la ventana del juego (se eligen en AJUSTES y quedan guardados en
ajustes.txt):

    NORMAL      ventana de 800 x 600, como siempre
    AGRANDABLE  ventana que se puede agrandar o achicar con el mouse (o
                maximizar): el juego se estira manteniendo la proporcion
    COMPLETA    pantalla completa (el juego se agranda y quedan bandas
                negras a los costados si la pantalla es mas ancha)
    SIN BORDES  ventana grande sin barra de titulo ni bordes, centrada
                (lo mas grande que entra en la pantalla)

Para cambiar de modo con el juego abierto se cierra la ventana y se abre
otra: pygame no pasa una ventana ya abierta al modo escalado.

El juego siempre dibuja en 800 x 600: en AGRANDABLE y COMPLETA lo agranda
pygame solo (modo SCALED), incluido el mouse, asi que el resto del codigo
no se entera.
"""

import os

import pygame

ANCHO, ALTO = 800, 600

MODOS = ["normal", "agrandable", "completa", "sin_bordes"]

NOMBRES = {
    "normal": "NORMAL",
    "agrandable": "AGRANDABLE",
    "completa": "COMPLETA",
    "sin_bordes": "SIN BORDES",
}

TITULO = "Super Compu Bros"


def _banderas(modo):

    if modo == "agrandable":
        return pygame.SCALED | pygame.RESIZABLE

    if modo == "completa":
        return pygame.SCALED | pygame.FULLSCREEN

    if modo == "sin_bordes":
        return pygame.SCALED | pygame.NOFRAME

    return 0


def aplicar(modo):
    """
    Cambia la ventana al modo pedido y devuelve la superficie de la
    pantalla. Si la compu no puede usar ese modo, queda en NORMAL.
    """

    if modo not in MODOS:
        modo = "normal"

    # Ventanas (normal y sin bordes) centradas en la pantalla
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    # Si ya habia una ventana, se cierra y se abre de nuevo (si no, pygame
    # deja la ventana como estaba)
    if pygame.display.get_init() and pygame.display.get_surface() is not None:
        pygame.display.quit()
        pygame.display.init()

    # En Windows, para que la barra de tareas muestre el icono del juego (y
    # no el de Python) el juego se presenta con su propio "AppUserModelID"
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("compubros.supercompubros")
        except Exception:
            pass

    # Icono de la ventana y de la barra de tareas (el mismo del acceso directo)
    try:
        ruta_icono = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icono.png")
        pygame.display.set_icon(pygame.image.load(ruta_icono))
    except (pygame.error, OSError, AttributeError):
        pass

    try:
        pantalla = pygame.display.set_mode((ANCHO, ALTO), _banderas(modo))
    except pygame.error:
        pantalla = pygame.display.set_mode((ANCHO, ALTO))

    pygame.display.set_caption(TITULO)

    return pantalla


def siguiente(modo, paso=1):
    """El modo siguiente (o el anterior con paso=-1) de la lista."""

    i = MODOS.index(modo) if modo in MODOS else 0
    return MODOS[(i + paso) % len(MODOS)]

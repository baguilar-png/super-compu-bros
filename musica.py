import os

import pygame

import ajustes


# ==========================================================
# MÚSICA DE FONDO
#
# Una sola canción suena a la vez. Si se pide la que ya está
# sonando no se reinicia (por ejemplo al ir del menú a
# instrucciones y volver).
# ==========================================================

CARPETA = os.path.dirname(os.path.abspath(__file__))

# Yoshi's Island OST - Athletic. (La cancion anterior, menu.mp3, sigue en la
# carpeta por si se quiere volver a usar: alcanza con cambiar este nombre.)
MUSICA_MENU = os.path.join(CARPETA, "assets", "musica", "menu_athletic.mp3")

MUSICA_SELECCION = os.path.join(
    CARPETA, "assets", "musica", "seleccion_personajes.mp3"
)

MUSICA_TUTORIAL = os.path.join(
    CARPETA, "assets", "musica", "tutorial.mp3"
)

# Volumen base (el que tenia la musica antes de los ajustes). El volumen
# que se oye es este por lo que se eligio en AJUSTES (0 a 100 %).
VOLUMEN = 0.6

_actual = None


def _mixer_listo():
    """Inicializa el mixer si hace falta. False si no hay audio."""

    if pygame.mixer.get_init():
        return True

    try:
        pygame.mixer.init()
        return True
    except pygame.error:
        return False


def volumen_actual():
    """Volumen real de la musica (base x ajuste del jugador)."""

    return VOLUMEN * ajustes.factor_musica()


def aplicar_volumen():
    """Pone el volumen de ajustes a la musica que esta sonando."""

    if pygame.mixer.get_init():

        pygame.mixer.music.set_volume(volumen_actual())


def reproducir(ruta):
    """Reproduce la canción en loop (si no es la que ya suena)."""

    global _actual

    if ruta == _actual and pygame.mixer.music.get_busy():
        return

    if not _mixer_listo():
        return

    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(volumen_actual())
        pygame.mixer.music.play(-1)
        _actual = ruta
    except pygame.error:
        _actual = None


def detener(fade_ms=400):
    """Corta la música con un fade out."""

    global _actual

    if pygame.mixer.get_init():
        pygame.mixer.music.fadeout(fade_ms)

    _actual = None

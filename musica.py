import os

import pygame


# ==========================================================
# MÚSICA DE FONDO
#
# Una sola canción suena a la vez. Si se pide la que ya está
# sonando no se reinicia (por ejemplo al ir del menú a
# instrucciones y volver).
# ==========================================================

CARPETA = os.path.dirname(os.path.abspath(__file__))

MUSICA_MENU = os.path.join(CARPETA, "assets", "musica", "menu.mp3")

MUSICA_SELECCION = os.path.join(
    CARPETA, "assets", "musica", "seleccion_personajes.mp3"
)

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


def reproducir(ruta):
    """Reproduce la canción en loop (si no es la que ya suena)."""

    global _actual

    if ruta == _actual and pygame.mixer.music.get_busy():
        return

    if not _mixer_listo():
        return

    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(VOLUMEN)
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

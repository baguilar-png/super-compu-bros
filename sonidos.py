"""
Efectos de sonido (assets/sonidos/*.wav).

    import sonidos
    sonidos.reproducir("guinness")

El volumen sale de AJUSTES (ajustes.efectos, 0 a 100): si esta en 0 no suena
nada. Cada sonido tiene ademas su propio volumen base (VOLUMENES) para que
los que se repiten mucho, como el salto, no molesten.

Si no hay placa de sonido, o falta un .wav, el juego sigue sin sonido (nunca
se rompe por eso). Los .wav los genera herramientas/generar_sonidos.py.
"""

import os

import pygame

import ajustes

CARPETA = os.path.dirname(os.path.abspath(__file__))

CARPETA_SONIDOS = os.path.join(CARPETA, "assets", "sonidos")

# Volumen base de cada efecto (1.0 = el .wav tal cual)
VOLUMENES = {
    "click": 0.45,
    "salto": 0.30,
    "aplastar": 0.60,
    "golpe": 0.70,
    "guinness": 0.50,
    "heineken": 0.50,
    "vidrio": 0.50,
    "meta": 0.55,
}

_cache = {}


def _mixer_listo():
    """Inicializa el mixer si hace falta. False si no hay audio."""

    if pygame.mixer.get_init():
        return True

    try:
        pygame.mixer.init()
        return True
    except pygame.error:
        return False


def _cargar(nombre):
    """El Sound ya cargado (None si no hay audio o falta el archivo)."""

    if nombre in _cache:

        return _cache[nombre]

    sonido = None

    if _mixer_listo():

        try:
            sonido = pygame.mixer.Sound(
                os.path.join(CARPETA_SONIDOS, nombre + ".wav")
            )
        except (pygame.error, FileNotFoundError, OSError):
            sonido = None

    # Si el mixer no estaba listo no se recuerda el fallo (puede que
    # se inicialice despues)
    if sonido is not None or pygame.mixer.get_init():

        _cache[nombre] = sonido

    return sonido


def volumen_de(nombre):
    """Volumen real con el que suena un efecto (base x ajuste)."""

    return VOLUMENES.get(nombre, 0.6) * ajustes.factor_efectos()


def reproducir(nombre):
    """Hace sonar un efecto (si el volumen de efectos no esta en 0)."""

    volumen = volumen_de(nombre)

    if volumen <= 0:

        return

    sonido = _cargar(nombre)

    if sonido is None:

        return

    sonido.set_volume(volumen)

    sonido.play()

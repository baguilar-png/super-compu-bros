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

# True si la cancion actual esta en pausa (al perder una vida o en una
# cinematica): al volver a pedirla sigue desde donde quedo
_pausada = False


def _mixer_listo():
    """Inicializa el mixer si hace falta. False si no hay audio."""

    # VERSION SIN SONIDO: nunca hay audio
    return False

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

    global _actual, _pausada, _inicio_ultimo_play

    if ruta == _actual and _pausada:
        # Estaba en pausa: sigue desde donde quedo
        reanudar()
        return

    if ruta == _actual and pygame.mixer.music.get_busy():
        return

    if not _mixer_listo():
        return

    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(volumen_actual())
        pygame.mixer.music.play(-1)
        _actual = ruta
        _pausada = False
        _inicio_ultimo_play = 0.0
    except pygame.error:
        _actual = None


def detener(fade_ms=400):
    """Corta la música con un fade out."""

    global _actual, _pausada

    if pygame.mixer.get_init():
        if _pausada:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.fadeout(fade_ms)

    _actual = None
    _pausada = False


# Segundos de cancion que ya habian sonado cuando se pauso (por si la placa
# de sonido no puede "despausar": se vuelve a arrancar desde ahi)
_posicion = 0.0
_inicio_ultimo_play = 0.0


def pausar():
    """Pausa la cancion que suena (al perder una vida o en una cinematica)."""

    global _pausada, _posicion

    if _actual is None or _pausada or not pygame.mixer.get_init():
        return

    try:
        _posicion = _inicio_ultimo_play + max(0, pygame.mixer.music.get_pos()) / 1000.0
    except pygame.error:
        _posicion = 0.0

    pygame.mixer.music.pause()
    _pausada = True


def reanudar():
    """Sigue la cancion pausada desde donde quedo."""

    global _pausada, _inicio_ultimo_play

    if not _pausada or not pygame.mixer.get_init():
        return

    pygame.mixer.music.set_volume(volumen_actual())
    pygame.mixer.music.unpause()
    _pausada = False

    # Si no siguio sonando, se vuelve a cargar y arranca desde donde iba
    if not pygame.mixer.music.get_busy() and _actual is not None:
        try:
            pygame.mixer.music.load(_actual)
            pygame.mixer.music.play(-1, start=_posicion)
            _inicio_ultimo_play = _posicion
        except pygame.error:
            pass


# ==========================================================
# CANCIONES DE LOS NIVELES (assets/musica/niveles/)
# ==========================================================
#
# Van en assets/musica/niveles/ con estos nombres (.mp3, .ogg o .wav):
#
#   dia_1 ... dia_5       niveles de dia
#   noche_1 ... noche_5   niveles de noche (y el castillo del nivel 30)
#   jefe_15               pelea del nivel 15
#   jefe_teichi           pelea contra Lord Teichi (nivel 30)
#   recuerdo_iki          el recuerdo de la mision de Iki
#   reencuentro_iki       el reencuentro de Iki con Carlitos (hasta la mordida)
#
# Si falta una cancion, ese nivel va en silencio (no se rompe nada).
#
# Las de dia y las de noche se eligen AL AZAR entre las 5 de su tipo, pero
# nunca sale la misma que sono en el nivel anterior.

CARPETA_NIVELES = os.path.join(CARPETA, "assets", "musica", "niveles")

EXTENSIONES = (".mp3", ".ogg", ".wav")

CANCIONES_POR_TIPO = 5


def ruta_cancion(nombre):
    """Ruta del archivo de la cancion, o None si no esta."""

    for extension in EXTENSIONES:
        ruta = os.path.join(CARPETA_NIVELES, nombre + extension)
        if os.path.isfile(ruta):
            return ruta
    return None


def reproducir_cancion(nombre):
    """Pone la cancion `nombre` (sin extension). Si no esta: silencio."""

    ruta = ruta_cancion(nombre)

    if ruta is None:
        detener()
        return

    reproducir(ruta)


# La ultima cancion de nivel que sono (para no repetirla)
_ultima_cancion = None


def cancion_de_nivel(nivel):
    """
    Nombre de la cancion de un nivel comun (para los jefes se usan
    jefe_15 y jefe_teichi). El castillo del nivel 30 usa una de noche.

    Niveles de dia: una de dia_1 ... dia_5 al azar; de noche: una de
    noche_1 ... noche_5. Nunca la misma dos veces seguidas.
    """

    global _ultima_cancion

    import random

    from fondos_nivel import NIVELES_OSCUROS

    nivel = int(nivel)

    if nivel == 15:
        return "jefe_15"

    tipo = "noche" if nivel in NIVELES_OSCUROS else "dia"

    nombres = ["%s_%d" % (tipo, n) for n in range(1, CANCIONES_POR_TIPO + 1)]

    # Solo las que estan en la carpeta (si no hay ninguna: todas, y suena
    # en silencio)
    hay = [n for n in nombres if ruta_cancion(n) is not None] or nombres

    opciones = [n for n in hay if n != _ultima_cancion] or hay

    _ultima_cancion = random.choice(opciones)

    return _ultima_cancion

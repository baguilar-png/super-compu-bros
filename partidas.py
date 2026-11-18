"""
Pantallas de las PARTIDAS (6 casillas).

    elegir_casilla()  las 6 casillas: nombre de la partida y abajo el nivel
                      en el que esta (y el barrio). Sirve para CARGAR (solo
                      las ocupadas) y para NUEVA PARTIDA (cualquiera: si
                      esta ocupada pregunta antes de borrarla)
    pedir_texto()     cuadro para escribir el nombre o la contrasena
    confirmar()       pregunta de SI / NO

    nueva_partida()   casilla -> nombre -> contrasena -> crea la partida
    cargar_partida()  casilla -> contrasena -> la deja en uso

Todas reciben dibujar_fondo(): lo que se ve atras (el menu).
"""

import sys

import pygame

import sonidos
from archivos import (
    CANTIDAD_PARTIDAS,
    contrasena_correcta,
    crear_partida,
    info_partidas,
    usar_partida,
)
from pixel_font import FuentePixel

ANCHO, ALTO = 800, 600
FPS = 60

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (180, 180, 180)
GRIS_OSCURO = (70, 70, 70)
GRIS_SOMBRA = (150, 150, 150)
GRIS_VACIA = (120, 120, 120)
AMARILLO = (255, 214, 64)
ROJO = (230, 60, 60)

LARGO_NOMBRE = 14
LARGO_CONTRASENA = 12

# Casillas: 2 columnas x 3 filas
ANCHO_CASILLA = 340
ALTO_CASILLA = 118
COLUMNAS_X = (40, ANCHO - 40 - ANCHO_CASILLA)
FILAS_Y = (112, 248, 384)

_fuentes = {}


def _fuente(escala):
    if escala not in _fuentes:
        _fuentes[escala] = FuentePixel(escala)
    return _fuentes[escala]


def _texto(pantalla, texto, escala, color, sombra=True, **donde):
    fuente = _fuente(escala)
    imagen = fuente.render(texto, True, color)
    rect = imagen.get_rect(**donde)
    if sombra:
        negro = fuente.render(texto, True, NEGRO)
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            pantalla.blit(negro, rect.move(dx, dy))
    pantalla.blit(imagen, rect)
    return rect


def _panel(pantalla, rect, claro=False, apagado=False):
    """Panel gris como los botones del menu (blanco si esta apuntado)."""

    fondo = BLANCO if claro else (GRIS_VACIA if apagado else GRIS)
    pygame.draw.rect(pantalla, GRIS_OSCURO, rect.inflate(10, 10))
    pygame.draw.rect(pantalla, fondo, rect)
    if not claro:
        sombra = (GRIS_SOMBRA if not apagado else (105, 105, 105))
        pygame.draw.rect(pantalla, sombra, (rect.right - 10, rect.top, 10, rect.height))
        pygame.draw.rect(pantalla, sombra, (rect.centerx, rect.bottom - 5, rect.width // 2, 5))


def _oscurecer(pantalla, alfa=140):
    velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    velo.fill((0, 0, 0, alfa))
    pantalla.blit(velo, (0, 0))


def _salir_si_cierra(evento):
    if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


def _nombre_del_lugar(nivel):
    try:
        from mapa import NIVELES
        return NIVELES[nivel - 1][0]
    except Exception:
        return ""


# ==========================================================
# LAS 6 CASILLAS
# ==========================================================

def _rect_casilla(i):
    return pygame.Rect(COLUMNAS_X[i % 2], FILAS_Y[i // 2], ANCHO_CASILLA, ALTO_CASILLA)


def _dibujar_casillas(pantalla, partidas, modo, elegida, titulo, aviso=None):

    _texto(pantalla, titulo, 4, BLANCO, midtop=(ANCHO // 2, 30))

    for i, info in enumerate(partidas):
        rect = _rect_casilla(i)
        se_puede = info is not None or modo == "nueva"
        _panel(pantalla, rect, claro=(i == elegida and se_puede), apagado=not se_puede)

        _texto(pantalla, "PARTIDA %d" % (i + 1), 2, GRIS_OSCURO, sombra=False,
               topleft=(rect.left + 14, rect.top + 10))

        if info is None:
            _texto(pantalla, "VACIA", 3, GRIS_OSCURO if se_puede else (90, 90, 90), sombra=False,
                   center=(rect.centerx, rect.centery + 8))
            continue

        _texto(pantalla, info["nombre"], 3, NEGRO, sombra=False,
               midleft=(rect.left + 14, rect.top + 52))
        lugar = _nombre_del_lugar(info["nivel"])
        abajo = "NIVEL %d" % info["nivel"] + (" - " + lugar if lugar else "")
        _texto(pantalla, abajo, 2, GRIS_OSCURO, sombra=False,
               bottomleft=(rect.left + 14, rect.bottom - 12))
        if info["con_contrasena"]:
            _candado(pantalla, rect.right - 34, rect.top + 12)

    pista = "FLECHAS Y ENTER / CLICK: ELEGIR      ESC: VOLVER"
    _texto(pantalla, pista, 2, BLANCO, midbottom=(ANCHO // 2, ALTO - 18))

    if aviso:
        _texto(pantalla, aviso, 2, AMARILLO, midbottom=(ANCHO // 2, ALTO - 48))


def _candado(pantalla, x, y):
    """Candadito de pixel art: la partida tiene contrasena."""
    u = 2
    pygame.draw.rect(pantalla, GRIS_OSCURO, (x + 2 * u, y, 6 * u, 2 * u))
    pygame.draw.rect(pantalla, GRIS_OSCURO, (x + 2 * u, y, 2 * u, 6 * u))
    pygame.draw.rect(pantalla, GRIS_OSCURO, (x + 6 * u, y, 2 * u, 6 * u))
    pygame.draw.rect(pantalla, GRIS_OSCURO, (x, y + 5 * u, 10 * u, 7 * u))
    pygame.draw.rect(pantalla, AMARILLO, (x + 4 * u, y + 7 * u, 2 * u, 3 * u))


def elegir_casilla(pantalla, reloj, dibujar_fondo, modo):
    """
    modo "cargar": solo se pueden elegir las ocupadas.
    modo "nueva":  cualquiera.
    Devuelve el numero de casilla (1 a 6) o None (ESC).
    """

    partidas = info_partidas()
    titulo = "CARGAR PARTIDA" if modo == "cargar" else "NUEVA PARTIDA"
    ocupadas = [i for i, p in enumerate(partidas) if p is not None]

    if modo == "cargar" and not ocupadas:
        elegida = 0
        aviso = "TODAVIA NO HAY PARTIDAS GUARDADAS"
    else:
        elegida = ocupadas[0] if modo == "cargar" else next(
            (i for i, p in enumerate(partidas) if p is None), 0)
        aviso = "ELEGI UNA CASILLA" if modo == "nueva" else None

    def se_puede(i):
        return modo == "nueva" or partidas[i] is not None

    while True:

        mouse = pygame.mouse.get_pos()
        for i in range(CANTIDAD_PARTIDAS):
            if _rect_casilla(i).collidepoint(mouse) and se_puede(i):
                elegida = i

        for evento in pygame.event.get():
            _salir_si_cierra(evento)

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for i in range(CANTIDAD_PARTIDAS):
                    if _rect_casilla(i).collidepoint(evento.pos) and se_puede(i):
                        sonidos.reproducir("boton")
                        return i + 1

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return None
                if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and se_puede(elegida):
                    sonidos.reproducir("boton")
                    return elegida + 1
                mover = {pygame.K_LEFT: -1, pygame.K_RIGHT: 1, pygame.K_UP: -2, pygame.K_DOWN: 2}.get(evento.key)
                if mover:
                    nueva = elegida
                    for _ in range(CANTIDAD_PARTIDAS):
                        nueva = (nueva + mover) % CANTIDAD_PARTIDAS
                        if se_puede(nueva):
                            elegida = nueva
                            break

        dibujar_fondo()
        _oscurecer(pantalla)
        _dibujar_casillas(pantalla, partidas, modo, elegida, titulo, aviso)
        pygame.display.flip()
        reloj.tick(FPS)


# ==========================================================
# CUADRO PARA ESCRIBIR
# ==========================================================

def pedir_texto(pantalla, reloj, dibujar_fondo, titulo, oculto=False, largo=LARGO_NOMBRE,
                subtitulo=None, validar=None):
    """
    Cuadro para escribir. oculto=True muestra asteriscos (contrasena).
    validar(texto) -> mensaje de error o None. Devuelve el texto o None.
    """

    texto = ""
    error = None
    t = 0.0
    sacudida = 0.0
    caja = pygame.Rect(0, 0, 600, 230)
    caja.center = (ANCHO // 2, ALTO // 2)
    campo = pygame.Rect(0, 0, 480, 56)
    campo.center = (ANCHO // 2, caja.centery + 6)

    while True:

        dt = reloj.tick(FPS) / 1000.0
        t += dt
        sacudida = max(0.0, sacudida - dt)

        for evento in pygame.event.get():
            _salir_si_cierra(evento)
            if evento.type != pygame.KEYDOWN:
                continue
            if evento.key == pygame.K_ESCAPE:
                return None
            if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if not texto.strip():
                    error = "NO PUEDE QUEDAR VACIO"
                    sacudida = 0.3
                    continue
                problema = validar(texto) if validar else None
                if problema:
                    error = problema
                    sacudida = 0.3
                    texto = "" if oculto else texto
                    sonidos.reproducir("golpe")
                    continue
                sonidos.reproducir("boton")
                return texto.strip() if not oculto else texto
            if evento.key == pygame.K_BACKSPACE:
                texto = texto[:-1]
                continue
            letra = getattr(evento, "unicode", "") or ""
            if len(letra) == 1 and letra.isprintable() and len(texto) < largo:
                texto += letra
                error = None
                sonidos.reproducir("teclado")

        dibujar_fondo()
        _oscurecer(pantalla, 160)

        dx = int(8 * (sacudida / 0.3) * (1 if int(t * 40) % 2 else -1)) if sacudida else 0
        _panel(pantalla, caja.move(dx, 0))
        _texto(pantalla, titulo, 3, NEGRO, sombra=False, midtop=(caja.centerx + dx, caja.top + 18))
        if subtitulo:
            _texto(pantalla, subtitulo, 2, GRIS_OSCURO, sombra=False, midtop=(caja.centerx + dx, caja.top + 56))

        pygame.draw.rect(pantalla, GRIS_OSCURO, campo.move(dx, 0).inflate(8, 8))
        pygame.draw.rect(pantalla, BLANCO, campo.move(dx, 0))
        visible = "*" * len(texto) if oculto else texto
        if int(t * 2) % 2 == 0:
            visible += "_"
        _texto(pantalla, visible, 3, NEGRO, sombra=False, midleft=(campo.left + 14 + dx, campo.centery))

        abajo = error or "ENTER: ACEPTAR      ESC: VOLVER"
        _texto(pantalla, abajo, 2, ROJO if error else GRIS_OSCURO, sombra=False,
               midbottom=(caja.centerx + dx, caja.bottom - 16))

        pygame.display.flip()


def confirmar(pantalla, reloj, dibujar_fondo, linea_1, linea_2=""):
    """Pregunta de SI (ENTER) / NO (ESC)."""

    caja = pygame.Rect(0, 0, 620, 200)
    caja.center = (ANCHO // 2, ALTO // 2)

    while True:
        for evento in pygame.event.get():
            _salir_si_cierra(evento)
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_s):
                    sonidos.reproducir("boton")
                    return True
                if evento.key in (pygame.K_ESCAPE, pygame.K_n):
                    return False

        dibujar_fondo()
        _oscurecer(pantalla, 160)
        _panel(pantalla, caja)
        _texto(pantalla, linea_1, 3, NEGRO, sombra=False, midtop=(caja.centerx, caja.top + 26))
        if linea_2:
            _texto(pantalla, linea_2, 3, NEGRO, sombra=False, midtop=(caja.centerx, caja.top + 70))
        _texto(pantalla, "ENTER: SI      ESC: NO", 2, GRIS_OSCURO, sombra=False,
               midbottom=(caja.centerx, caja.bottom - 20))
        pygame.display.flip()
        reloj.tick(FPS)


# ==========================================================
# NUEVA PARTIDA / CARGAR PARTIDA
# ==========================================================

def nueva_partida(pantalla, reloj, dibujar_fondo):
    """True si se creo (y quedo en uso) una partida nueva."""

    while True:
        numero = elegir_casilla(pantalla, reloj, dibujar_fondo, "nueva")
        if numero is None:
            return False

        info = info_partidas()[numero - 1]
        if info is not None and not confirmar(
            pantalla, reloj, dibujar_fondo,
            "¿BORRAR \"%s\"" % info["nombre"], "Y EMPEZAR DE NUEVO?"
        ):
            continue

        nombre = pedir_texto(pantalla, reloj, dibujar_fondo, "NOMBRE DE LA PARTIDA",
                             largo=LARGO_NOMBRE)
        if nombre is None:
            continue

        contrasena = pedir_texto(
            pantalla, reloj, dibujar_fondo, "PONELE UNA CONTRASEÑA", oculto=True,
            largo=LARGO_CONTRASENA, subtitulo="LA VAS A NECESITAR PARA ENTRAR"
        )
        if contrasena is None:
            continue

        repetida = pedir_texto(
            pantalla, reloj, dibujar_fondo, "REPETI LA CONTRASEÑA", oculto=True,
            largo=LARGO_CONTRASENA,
            validar=lambda t: None if t == contrasena else "NO ES IGUAL A LA PRIMERA"
        )
        if repetida is None:
            continue

        crear_partida(numero, nombre, contrasena)
        return True


def cargar_partida(pantalla, reloj, dibujar_fondo):
    """True si se eligio una partida (con la contrasena correcta)."""

    while True:
        numero = elegir_casilla(pantalla, reloj, dibujar_fondo, "cargar")
        if numero is None:
            return False

        info = info_partidas()[numero - 1]
        if info is None:
            continue

        if info["con_contrasena"]:
            contrasena = pedir_texto(
                pantalla, reloj, dibujar_fondo, "CONTRASEÑA", oculto=True,
                largo=LARGO_CONTRASENA, subtitulo=info["nombre"],
                validar=lambda t: None if contrasena_correcta(numero, t) else "CONTRASEÑA INCORRECTA"
            )
            if contrasena is None:
                continue

        usar_partida(numero)
        return True

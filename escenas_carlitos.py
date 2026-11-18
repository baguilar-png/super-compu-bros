"""
Escenas de CARLITOS, el perro amarillo.

    recuerdo_bolivar(...)       La MISION DE IKI: un recuerdo (en sepia) de
                                los Compu Bros e Iki caminando por Bolivar,
                                de Av. Caseros a Av. Martin Garcia. Cerca
                                del final aparece un perro amarillo y le
                                muerde la entrepierna a Iki. Al terminar,
                                Iki (ya en el presente) pide ayuda para
                                encontrarlo: anda por Palermo.

    llamada_carlitos(...)       Despues del nivel 8: un Compu Bro al azar
                                (nunca el que se esta usando) llama a los
                                demas y avisa que encontro a Carlitos.
                                Despues aparece la cara de Carlitos en el
                                mapa de Buenos Aires.

    reencuentro_carlitos(...)   Al entrar a Carlitos en el mapa: Iki y
                                Carlitos corren a abrazarse... y Carlitos
                                le vuelve a morder la entrepierna y se va.

En todas: ENTER / ESPACIO / click adelantan, ESC saltea.

Los sprites de Carlitos los genera herramientas/generar_carlitos.py y la
calle Bolivar herramientas/generar_bolivar.py.
"""

import math
import random
import sys

import pygame

import musica
import sonidos
from historia import (
    AMARILLO,
    BLANCO,
    CUADRO,
    FPS,
    NEGRO,
    PERSONAJES,
    RETRATO_GRANDE,
    TEXTO_ANCHO,
    TEXTO_X,
    TEXTO_Y,
    Retrato,
    _cargar,
    _dibujar_cuadro,
    _dibujar_flechita,
    _dibujar_globo,
    _dibujar_signo,
    _dibujar_texto_con_sombra,
    _escalar,
    _partir_en_lineas,
)


COMPU_BROS = ["BAUTO", "BENJA", "CASTRO", "POSHO", "THIAGO"]

# Poses de caminar de cada Compu Bro (miran a la derecha)
CAMINAR = {
    "BAUTO": ["bauto frame 1.png", "bauto frame 2.png", "bauto frame 3.png"],
    "BENJA": ["Benja frame 1.png", "Benja frame 2.png", "Benja frame 3.png"],
    "CASTRO": ["castro frame 1.png", "castro frame 2.png", "castro frame 3.png"],
    "POSHO": ["Posho Frame 1.png", "Posho Frame 2.png", "Posho Frame 3.png"],
    "THIAGO": ["thiago frame 1.png", "thiago frame 2.png", "thiago frame 3.png"],
}

CARLITOS = "assets/personajes/CARLITOS/"
CARLITOS_CORRER = ["correr_1.png", "correr_2.png", "correr_3.png", "correr_4.png"]

ESCALA_PERSONAJES = 3
ESCALA_PERRO = 2
ESCALA_FONDO = 2

PISO_Y = 372            # pies de los personajes (sobre la vereda)
ALTO_FONDO = 436        # el fondo (218 x 2); abajo queda la franja negra

# Esquinas de la cuadra (en pixeles de pantalla, el fondo ya agrandado)
X_CARTEL_CASEROS = 64
X_CARTEL_MARTIN_GARCIA = 1832


# ==========================================================
# AYUDAS
# ==========================================================

def _salir_si_cierra(evento):

    if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


def _leer_teclas():
    """(avanzar, saltear) segun lo que se apreto en este frame."""

    avanzar = saltear = False

    for evento in pygame.event.get():

        _salir_si_cierra(evento)

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                saltear = True
            elif evento.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                avanzar = True

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            avanzar = True

    return avanzar, saltear


def _sepia(imagen):

    copia = imagen.copy()

    for x in range(copia.get_width()):
        for y in range(copia.get_height()):
            r, g, b, a = copia.get_at((x, y))
            if a:
                v = r * 0.3 + g * 0.59 + b * 0.11
                copia.set_at((x, y), (min(255, int(v * 1.07 + 20)), min(255, int(v * 0.92 + 8)), int(v * 0.72), a))

    return copia


def _tenido(imagen, color):
    """Copia de la imagen pintada de un color (para el "ay" de Iki)."""

    copia = imagen.copy()

    for x in range(copia.get_width()):
        for y in range(copia.get_height()):
            r, g, b, a = copia.get_at((x, y))
            if a:
                copia.set_at((x, y), ((r + color[0] * 2) // 3, (g + color[1] * 2) // 3, (b + color[2] * 2) // 3, a))

    return copia


def _cargar_escalado(ruta, escala, filtro=None):

    imagen = _cargar(ruta)

    if filtro is not None:
        imagen = filtro(imagen)

    return _escalar(imagen, escala)


def _cargar_carlitos(escala, filtro=None):
    """Poses de Carlitos mirando a la derecha y a la izquierda."""

    der = {
        "correr": [_cargar_escalado(CARLITOS + n, escala, filtro) for n in CARLITOS_CORRER],
        "parado": _cargar_escalado(CARLITOS + "parado.png", escala, filtro),
        "morder": _cargar_escalado(CARLITOS + "morder.png", escala, filtro),
    }

    izq = {
        "correr": [pygame.transform.flip(i, True, False) for i in der["correr"]],
        "parado": pygame.transform.flip(der["parado"], True, False),
        "morder": pygame.transform.flip(der["morder"], True, False),
    }

    return der, izq


IKI = "assets/personajes/IKI/"


def _cargar_iki(escala, filtro=None):
    """
    Poses de Iki mirando a la derecha (las genera
    herramientas/generar_historicos.py a partir de su dibujo):
    quieto, caminar (1, 2, 3, 2), salto, y las mismas en rojo (para el "ay").
    """

    def cargar(nombre):
        return _cargar_escalado(IKI + nombre, escala, filtro)

    poses = {
        "quieto": cargar("final.png"),
        "caminar": [cargar("frame_1.png"), cargar("frame_2.png"), cargar("frame_3.png")],
        "salto": cargar("saltando.png"),
    }
    poses["caminar"].append(poses["caminar"][1])

    poses["quieto_rojo"] = _tenido(poses["quieto"], (230, 60, 50))
    poses["salto_rojo"] = _tenido(poses["salto"], (230, 60, 50))

    return poses


def _dibujar_iki_mordido(pantalla, iki_p, centro_x, dt_m, t):
    """
    Iki despues de la mordida: salta del dolor (pose de salto), titila en
    rojo y queda temblando. Devuelve cuanto subio (para el perro).
    """

    salto = int(math.sin(dt_m / 0.5 * math.pi) * 60) if dt_m < 0.5 else 0
    temblor = int(math.sin(t * 60) * 3) if dt_m < 3.0 else 0
    rojo = dt_m < 1.6 and int(dt_m * 10) % 2 == 0

    if dt_m < 0.5:
        imagen = iki_p["salto_rojo"] if rojo else iki_p["salto"]
        abajo = PISO_Y + 4
    else:
        imagen = iki_p["quieto_rojo"] if rojo else iki_p["quieto"]
        abajo = PISO_Y

    _sombra(pantalla, centro_x, 50)
    pantalla.blit(imagen, imagen.get_rect(midbottom=(centro_x + temblor, abajo - salto)))

    return salto


def _sombra(pantalla, centro_x, ancho, y=PISO_Y):

    sombra = pygame.Surface((ancho, 12), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 80), sombra.get_rect())
    pantalla.blit(sombra, (centro_x - ancho // 2, y - 7))


def _cartel_calle(pantalla, fuente, x, nombres, base_y=PISO_Y):
    """Poste con los carteles de las calles de la esquina."""

    pygame.draw.rect(pantalla, (30, 30, 30), (x - 3, base_y - 190, 6, 190))

    y = base_y - 196
    for nombre in nombres:
        texto = fuente.render(nombre, True, BLANCO)
        cartel = texto.get_rect()
        cartel.inflate_ip(16, -2)
        cartel.midtop = (x, y)
        pygame.draw.rect(pantalla, NEGRO, cartel.inflate(6, 6))
        pygame.draw.rect(pantalla, (24, 24, 28), cartel)
        pygame.draw.rect(pantalla, BLANCO, cartel, 2)
        pantalla.blit(texto, texto.get_rect(center=(cartel.centerx, cartel.centery + 1)))
        y += cartel.height + 8


def _vineta(ancho, alto):
    """Bordes oscuros y borrosos, como de recuerdo."""

    vineta = pygame.Surface((ancho, alto), pygame.SRCALPHA)

    pasos = 40
    for i in range(pasos):
        alfa = int(150 * (1 - i / pasos) ** 2)
        pygame.draw.rect(vineta, (30, 18, 8, alfa), (i * 3, i * 3, ancho - i * 6, alto - i * 6), 3)

    return vineta


def _texto_centrado(pantalla, fuente, texto, centro_y, alfa=255, color=BLANCO):

    imagen = fuente.render(texto, True, color)
    if alfa < 255:
        imagen = imagen.copy()
        imagen.set_alpha(alfa)
    pantalla.blit(imagen, imagen.get_rect(center=(pantalla.get_width() // 2, centro_y)))


def _grito(pantalla, fuente, texto, centro_x, base_y, t):
    """Grito grande que tiembla ("¡AAAAAY!")."""

    dx = int(math.sin(t * 50) * 4)
    dy = int(math.cos(t * 43) * 3)

    sombra = fuente.render(texto, True, NEGRO)
    imagen = fuente.render(texto, True, (255, 70, 60))
    rect = imagen.get_rect(midbottom=(centro_x + dx, base_y + dy))
    rect.clamp_ip(pantalla.get_rect().inflate(-10, -10))

    for ox, oy in ((-3, 0), (3, 0), (0, -3), (0, 3)):
        pantalla.blit(sombra, rect.move(ox, oy))
    pantalla.blit(imagen, rect)


def _estrellitas(pantalla, centro_x, centro_y, t, color=AMARILLO):
    """Estrellitas que dan vueltas (Iki dolorido)."""

    for k in range(4):
        a = t * 5 + k * math.pi / 2
        x = centro_x + int(math.cos(a) * 30)
        y = centro_y + int(math.sin(a) * 9)
        pygame.draw.rect(pantalla, color, (x - 1, y - 4, 3, 9))
        pygame.draw.rect(pantalla, color, (x - 4, y - 1, 9, 3))


def _corazon(pantalla, x, y, escala=3, alfa=255):

    dibujo = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]
    capa = pygame.Surface((7 * escala, 6 * escala), pygame.SRCALPHA)
    for fy, fila in enumerate(dibujo):
        for fx, c in enumerate(fila):
            if c == "#":
                pygame.draw.rect(capa, (235, 60, 90, alfa), (fx * escala, fy * escala, escala, escala))
    pantalla.blit(capa, (x - capa.get_width() // 2, y - capa.get_height() // 2))


def _posicion_mordida(iki_rect, perro, mirando_izq):
    """
    Donde va Carlitos para morder la entrepierna de Iki. El hocico esta en
    la punta del sprite (a la izquierda si mira a la izquierda).
    """

    entrepierna_y = iki_rect.bottom - int(iki_rect.height * 0.36)
    alto_hocico = int(perro.get_height() * 0.30)

    if mirando_izq:
        x = iki_rect.centerx - 4
    else:
        x = iki_rect.centerx + 4 - perro.get_width()

    return x, entrepierna_y - alto_hocico


# ==========================================================
# 1) RECUERDO: BOLIVAR, DE AV. CASEROS A AV. MARTIN GARCIA
# ==========================================================

# Lo que dice Iki al terminar el recuerdo
PEDIDO_IKI = [
    ("IKI", "Desde ese día no dejo de pensar en ese perro..."),
    ("IKI", "¿Me ayudás a encontrarlo? Dicen que anda dando vueltas por Palermo."),
]


def recuerdo_bolivar(pantalla, reloj, fuente_grande, fuente_media):
    """La mision de Iki. Vuelve al terminar o con ESC."""

    musica.reproducir_cancion("recuerdo_iki")

    try:
        _recuerdo(pantalla, reloj, fuente_grande, fuente_media)
        _pedido_iki(pantalla, reloj, fuente_media)
    finally:
        sonidos.detener("teclado")
        musica.detener()


def _pedido_iki(pantalla, reloj, fuente_media):
    """
    De vuelta en el presente (a color): Iki parado en Bolivar pide que lo
    ayudes a encontrar al perro, que esta por Palermo. Dialogo igual que
    los de historia.py.
    """

    ancho, alto = pantalla.get_size()
    fuente_chica = type(fuente_media)(2)

    fondo = _cargar_escalado("assets/historia/bolivar.png", ESCALA_FONDO)
    camara = 1180

    iki = _cargar_escalado(PERSONAJES["IKI"][0], ESCALA_PERSONAJES)
    retrato = Retrato("IKI", _cargar(PERSONAJES["IKI"][0]))
    retrato.mandar_a(RETRATO_GRANDE.centerx, RETRATO_GRANDE.bottom, 6, gris=False)

    lineas = [(q, _partir_en_lineas(fuente_media, txt, TEXTO_ANCHO)) for q, txt in PEDIDO_IKI]

    t = 0.0
    linea = 0
    letras = 0.0
    T_EMPIEZA = 0.9

    while True:

        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt

        avanzar, saltear = _leer_teclas()

        if saltear:
            return

        quien, partes = lineas[linea]
        total = sum(len(p) for p in partes)

        if t >= T_EMPIEZA:

            if letras < total:
                letras = min(total, letras + 38 * dt)

            if avanzar:
                if letras < total:
                    letras = total
                elif linea + 1 < len(lineas):
                    sonidos.reproducir("boton")
                    linea += 1
                    letras = 0.0
                    continue
                else:
                    sonidos.reproducir("boton")
                    return

        escribiendo = t >= T_EMPIEZA and letras < total

        if escribiendo:
            sonidos.reproducir_en_bucle("teclado")
        else:
            sonidos.detener("teclado")

        retrato.actualizar(dt)

        # --------------------------------------------------
        # DIBUJAR
        # --------------------------------------------------

        pantalla.fill(NEGRO)
        pantalla.blit(fondo, (-camara, 0))
        pygame.draw.rect(pantalla, (40, 40, 46), (0, ALTO_FONDO, ancho, alto - ALTO_FONDO))

        salto = int(abs(math.sin(t / 0.32 * math.pi)) * 6) if escribiendo else 0
        _sombra(pantalla, ancho // 2, 50)
        pantalla.blit(iki, iki.get_rect(midbottom=(ancho // 2, PISO_Y - salto)))

        if t < 2.5:
            alfa = int(255 * min(1.0, t / 0.4, (2.5 - t) / 0.4))
            _texto_centrado(pantalla, fuente_media, "HOY", 40, alfa)

        if t >= T_EMPIEZA:

            velo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            velo.fill((0, 0, 0, 80))
            pantalla.blit(velo, (0, 0))

            _dibujar_cuadro(pantalla, fuente_media, quien, PERSONAJES[quien][1])

            retrato.dibujar(pantalla, int(abs(math.sin(t / 0.32 * math.pi)) * 3) if escribiendo else 0)

            restantes = int(letras)
            alto_linea = fuente_media.get_height() - 4
            for k, parte in enumerate(partes):
                if restantes <= 0:
                    break
                _dibujar_texto_con_sombra(pantalla, fuente_media, parte[:restantes], BLANCO, (TEXTO_X, TEXTO_Y + k * alto_linea))
                restantes -= len(parte)

            if not escribiendo:
                _dibujar_flechita(pantalla, t)

        # Sale del negro
        if t < 0.6:
            negro = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            negro.fill((0, 0, 0, int(255 * (1 - t / 0.6))))
            pantalla.blit(negro, (0, 0))

        ayuda = fuente_chica.render("ESC: saltear", True, (230, 230, 230))
        pantalla.blit(ayuda, ayuda.get_rect(topright=(ancho - 10, 8)))

        pygame.display.flip()


def _recuerdo(pantalla, reloj, fuente_grande, fuente_media):

    ancho, alto = pantalla.get_size()
    fuente_chica = type(fuente_media)(2)

    fondo = _cargar_escalado("assets/historia/bolivar_recuerdo.png", ESCALA_FONDO)
    vineta = _vineta(ancho, ALTO_FONDO)

    # Los Compu Bros (4 poses: 1, 2, 3, 2) e Iki, en sepia
    bros = {}
    for nombre in COMPU_BROS:
        poses = [
            _cargar_escalado("assets/personajes/%s/%s" % (nombre, archivo), ESCALA_PERSONAJES, _sepia)
            for archivo in CAMINAR[nombre]
        ]
        bros[nombre] = poses + [poses[1]]

    iki_p = _cargar_iki(ESCALA_PERSONAJES, _sepia)
    iki = iki_p["quieto"]

    # El perro va a color: es lo unico amarillo del recuerdo
    perro_der, perro_izq = _cargar_carlitos(ESCALA_PERRO)

    # Fila de izquierda a derecha; Iki va adelante
    fila = ["THIAGO", "POSHO", "CASTRO", "BENJA", "BAUTO", "IKI"]
    separacion = 82
    velocidad = 120                 # px por segundo
    x_lider = 600.0                 # Iki (en el mundo)

    fin_mundo = fondo.get_width()

    t = 0.0
    camara = 0.0

    # Fases
    caminando = True
    t_perro = None                  # cuando aparece el perro
    x_perro = 0.0
    t_mordida = None
    t_escapa = None
    t_final = None
    x_iki_mordida = 0

    VELOCIDAD_PERRO = 380
    X_APARECE_PERRO = 1460          # cuando Iki llega aca, aparece el perro
    DURACION_MORDIDA = 1.1
    DURACION_FINAL = 4.0

    while True:

        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt

        avanzar, saltear = _leer_teclas()

        if saltear:
            return

        # Apretar al final termina el recuerdo
        if avanzar and t_final is not None and t - t_final > 1.0:
            return

        # --------------------------------------------------
        # MOVIMIENTO
        # --------------------------------------------------

        if caminando:
            x_lider += velocidad * dt

        camara = max(0.0, min(fin_mundo - ancho, x_lider - 600))

        if t_perro is None and x_lider >= X_APARECE_PERRO:
            t_perro = t
            x_perro = camara + ancho + 60

        iki_x = x_lider if t_mordida is None else x_iki_mordida
        iki_rect = iki.get_rect(midbottom=(int(iki_x - camara), PISO_Y))

        if t_perro is not None and t_mordida is None:
            x_perro -= VELOCIDAD_PERRO * dt
            # Llega a Iki: lo muerde
            if x_perro - camara <= iki_rect.centerx + 10:
                t_mordida = t
                x_iki_mordida = x_lider
                caminando = False
                sonidos.reproducir("golpe")

        if t_mordida is not None and t_escapa is None and t - t_mordida >= DURACION_MORDIDA:
            t_escapa = t
            x_perro = iki_x + 10

        if t_escapa is not None:
            x_perro += VELOCIDAD_PERRO * 1.3 * dt
            if t_final is None and x_perro - camara > ancho + 80:
                t_final = t

        if t_final is not None and t - t_final >= DURACION_FINAL:
            return

        # --------------------------------------------------
        # DIBUJAR
        # --------------------------------------------------

        pantalla.fill(NEGRO)
        pantalla.blit(fondo, (-int(camara), 0))

        # Carteles de las esquinas
        _cartel_calle(pantalla, fuente_chica, X_CARTEL_CASEROS - int(camara), ["AV. CASEROS", "BOLIVAR"])
        _cartel_calle(pantalla, fuente_chica, X_CARTEL_MARTIN_GARCIA - int(camara), ["AV. MARTIN GARCIA", "BOLIVAR"])

        # Compu Bros
        for k, nombre in enumerate(fila[:-1]):

            x = x_lider - (len(fila) - 1 - k) * separacion - camara

            if caminando:
                imagen = bros[nombre][int(t * 8 + k) % 4]
            else:
                imagen = bros[nombre][1]

            _sombra(pantalla, int(x), 56)
            rect = imagen.get_rect(midbottom=(int(x), PISO_Y + 4))
            pantalla.blit(imagen, rect)

            # Charlando mientras caminan
            if caminando and int(t * 1.3 + k * 1.9) % 4 == 0:
                _dibujar_globo(pantalla, fuente_chica, int(x), rect.top + 14, "bla" if k % 2 else "...")

            # Ven al perro
            if t_perro is not None and (t_final is None):
                _dibujar_signo(pantalla, fuente_media, "!", AMARILLO, int(x), rect.top + 12)

        # Iki (camina igual que los demas)
        if t_mordida is None:
            _sombra(pantalla, iki_rect.centerx, 50)
            if caminando:
                imagen = iki_p["caminar"][int(t * 8 + 5) % 4]
                pantalla.blit(imagen, imagen.get_rect(midbottom=(iki_rect.centerx, PISO_Y + 4)))
            else:
                pantalla.blit(iki, iki_rect)
        else:
            dt_m = t - t_mordida
            salto = _dibujar_iki_mordido(pantalla, iki_p, iki_rect.centerx, dt_m, t)

            if dt_m < 3.2:
                _grito(pantalla, fuente_grande, "¡AAAAAY!", iki_rect.centerx, iki_rect.top - 20 - salto, t)
            else:
                _estrellitas(pantalla, iki_rect.centerx, iki_rect.top - 6, t)

        # Perro
        if t_perro is not None and t_escapa is None:

            if t_mordida is None:
                distancia = (x_perro - camara) - iki_rect.centerx
                if distancia < 90:
                    imagen = perro_izq["morder"]
                    subida = int((1 - max(0, distancia) / 90) * 30)
                else:
                    imagen = perro_izq["correr"][int(t * 14) % 4]
                    subida = 0
                rect = imagen.get_rect(bottomleft=(int(x_perro - camara), PISO_Y + 2 - subida))
                _sombra(pantalla, rect.centerx, 70)
                pantalla.blit(imagen, rect)
            else:
                # Colgado de la entrepierna
                imagen = perro_izq["morder"]
                dt_m = t - t_mordida
                salto = int(math.sin(dt_m / 0.5 * math.pi) * 60) if dt_m < 0.5 else 0
                x, y = _posicion_mordida(iki_rect.move(0, -salto), imagen, True)
                sacudida = int(math.sin(t * 40) * 4)
                pantalla.blit(imagen, (x + sacudida, y))

        if t_escapa is not None and t_final is None:
            imagen = perro_der["correr"][int(t * 16) % 4]
            rect = imagen.get_rect(bottomleft=(int(x_perro - camara), PISO_Y + 2))
            _sombra(pantalla, rect.centerx, 70)
            pantalla.blit(imagen, rect)

        pantalla.blit(vineta, (0, 0))

        # Parpadeo de pelicula vieja
        if random.random() < 0.06:
            destello = pygame.Surface((ancho, ALTO_FONDO), pygame.SRCALPHA)
            destello.fill((255, 240, 200, 22))
            pantalla.blit(destello, (0, 0))

        # Franja de abajo: textos del recuerdo
        pygame.draw.rect(pantalla, NEGRO, (0, ALTO_FONDO, ancho, alto - ALTO_FONDO))

        if t < 4.0:
            alfa = int(255 * min(1.0, t / 0.6, (4.0 - t) / 0.6))
            _texto_centrado(pantalla, fuente_media, "HACE UN TIEMPO...", ALTO_FONDO + 50, alfa)
            _texto_centrado(pantalla, fuente_chica, "Calle Bolívar, de Av. Caseros a Av. Martín García", ALTO_FONDO + 100, alfa, (210, 190, 150))

        if t_final is not None:
            alfa = int(255 * min(1.0, (t - t_final) / 0.8))
            _texto_centrado(pantalla, fuente_media, "Nadie supo nunca de dónde", ALTO_FONDO + 50, alfa)
            _texto_centrado(pantalla, fuente_media, "salió ese perro amarillo...", ALTO_FONDO + 92, alfa)

        # Fundido a negro al terminar
        if t_final is not None and t - t_final > DURACION_FINAL - 0.8:
            negro = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            negro.fill((0, 0, 0, int(255 * min(1.0, (t - t_final - (DURACION_FINAL - 0.8)) / 0.8))))
            pantalla.blit(negro, (0, 0))

        # Fundido desde negro al empezar
        if t < 0.8:
            negro = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            negro.fill((0, 0, 0, int(255 * (1 - t / 0.8))))
            pantalla.blit(negro, (0, 0))

        ayuda = fuente_chica.render("ESC: saltear", True, (230, 230, 230))
        pantalla.blit(ayuda, ayuda.get_rect(topright=(ancho - 10, 8)))

        pygame.display.flip()


# ==========================================================
# 2) LLAMADA: "¡ENCONTRE A CARLITOS!" (DESPUES DEL NIVEL 8)
# ==========================================================

# Color de la "pieza" de cada uno en la videollamada
FONDOS_LLAMADA = {
    "BAUTO": (196, 120, 110),
    "BENJA": (90, 120, 190),
    "CASTRO": (200, 90, 90),
    "POSHO": (150, 110, 160),
    "THIAGO": (90, 160, 200),
}


def _dialogo_llamada(llama, jugador, otros):
    """Las lineas de la llamada (llama = el que encontro a Carlitos)."""

    return [
        (llama, "¿Me escuchan, Bros? ¡Tengo una noticia!"),
        (jugador, "Sí, te escuchamos. ¿Qué pasó?"),
        (llama, "¡ENCONTRÉ A CARLITOS!"),
        (otros[0], "¿Carlitos? ¿El perro amarillo que le mordió la entrepierna a Iki?"),
        (llama, "¡Ese mismo! Lo vi dando vueltas por Palermo."),
        (otros[1], "Hay que avisarle a Iki ya mismo."),
        (llama, "Les mando la ubicación. ¡Fíjense en el mapa!"),
    ]


def llamada_carlitos(pantalla, reloj, fuente_grande, fuente_media, jugador="BENJA", historico=False):
    """
    jugador: el Compu Bro que se esta usando (no puede ser el que llama).
    historico: True si se usa su aspecto historico.
    """

    try:
        _llamada(pantalla, reloj, fuente_media, jugador, historico)
    finally:
        sonidos.detener("llamada")
        sonidos.detener("teclado")


def _llamada(pantalla, reloj, fuente_media, jugador, historico):

    ancho, alto = pantalla.get_size()
    fuente_chica = type(fuente_media)(2)

    if jugador not in COMPU_BROS:
        jugador = COMPU_BROS[0]

    llama = random.choice([n for n in COMPU_BROS if n != jugador])
    otros = [n for n in COMPU_BROS if n not in (llama, jugador)]
    random.shuffle(otros)

    # Sprites de frente (el del jugador con su aspecto)
    frentes = {}
    for nombre in COMPU_BROS:
        ruta = PERSONAJES[nombre][0]
        if nombre == jugador and historico:
            ruta = "assets/personajes/%s/historico/frente.png" % nombre
        try:
            frentes[nombre] = _cargar(ruta)
        except (pygame.error, FileNotFoundError):
            frentes[nombre] = _cargar(PERSONAJES[nombre][0])

    en_ventana = {n: _escalar(img, 3) for n, img in frentes.items()}
    retratos = {n: Retrato(n, img) for n, img in frentes.items()}

    # Ventanitas de la videollamada: el que llama arriba a la izquierda,
    # despues el jugador y los demas
    orden = [llama, jugador] + otros
    ventanas = {}
    w, h = 236, 176
    for i, nombre in enumerate(orden):
        if i < 3:
            x = 24 + i * (w + 16)
            y = 34
        else:
            x = 24 + (w + 16) // 2 + (i - 3) * (w + 16)
            y = 34 + h + 16
        ventanas[nombre] = pygame.Rect(x, y, w, h)

    dialogo = _dialogo_llamada(llama, jugador, otros)
    lineas = [(q, _partir_en_lineas(fuente_media, txt, TEXTO_ANCHO)) for q, txt in dialogo]

    t = 0.0
    conectados = {llama}
    T_PRIMERO = 1.6         # los demas se van conectando de a uno
    CADA = 0.5
    t_hablar = T_PRIMERO + CADA * 4 + 0.4

    sonidos.reproducir_en_bucle("llamada")

    banco = []
    hablando = None
    linea = -1
    letras = 0.0
    total = 0
    t_dialogo = None

    def pasar_a(i):
        nonlocal linea, letras, total, hablando
        linea = i
        letras = 0.0
        quien, partes = lineas[i]
        total = sum(len(p) for p in partes)
        if quien == hablando:
            return
        if hablando is not None and hablando not in banco:
            banco.append(hablando)
        if quien in banco:
            banco.remove(quien)
        hablando = quien
        retratos[quien].mandar_a(RETRATO_GRANDE.centerx, RETRATO_GRANDE.bottom, 6, gris=False)
        for k, nombre in enumerate(banco):
            retratos[nombre].mandar_a(CUADRO.right - 34 - k * 66, CUADRO.y - 10, 2, gris=True)

    while True:

        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt

        avanzar, saltear = _leer_teclas()

        if saltear:
            return

        # Se van conectando
        for k, nombre in enumerate(orden[1:]):
            if nombre not in conectados and t >= T_PRIMERO + k * CADA:
                conectados.add(nombre)
                sonidos.reproducir("boton")
                if len(conectados) == len(orden):
                    sonidos.detener("llamada")

        if avanzar and linea < 0:
            t = max(t, t_hablar)
            for nombre in orden:
                conectados.add(nombre)
            sonidos.detener("llamada")
            avanzar = False

        if linea < 0 and t >= t_hablar:
            t_dialogo = t
            pasar_a(0)

        if linea >= 0:
            if letras < total:
                letras = min(total, letras + 38 * dt)
            if avanzar:
                if letras < total:
                    letras = total
                elif linea + 1 < len(lineas):
                    sonidos.reproducir("boton")
                    pasar_a(linea + 1)
                else:
                    sonidos.reproducir("boton")
                    return

        escribiendo = linea >= 0 and letras < total

        if escribiendo:
            sonidos.reproducir_en_bucle("teclado")
        else:
            sonidos.detener("teclado")

        for r in retratos.values():
            r.actualizar(dt)

        # --------------------------------------------------
        # DIBUJAR: la videollamada
        # --------------------------------------------------

        pantalla.fill((18, 20, 30))

        titulo = "LLAMADA GRUPAL - COMPU BROS" if len(conectados) == len(orden) else "LLAMANDO" + "." * (int(t * 3) % 4)
        _texto_centrado(pantalla, fuente_chica, titulo, 16, color=(170, 220, 170))

        for nombre in orden:

            rect = ventanas[nombre]
            conectado = nombre in conectados

            pygame.draw.rect(pantalla, NEGRO, rect.inflate(8, 8))

            if conectado:
                fondo = FONDOS_LLAMADA[nombre]
                pygame.draw.rect(pantalla, fondo, rect)
                piso = rect.copy()
                piso.top = rect.bottom - 30
                piso.height = 30
                pygame.draw.rect(pantalla, tuple(max(0, v - 50) for v in fondo), piso)

                salto = 0
                if nombre == hablando and escribiendo:
                    salto = int(abs(math.sin(t / 0.32 * math.pi)) * 6)

                imagen = en_ventana[nombre]
                pantalla.blit(imagen, imagen.get_rect(midbottom=(rect.centerx, rect.bottom - 8 - salto)))

                # Celular del que llama
                if nombre == llama:
                    x = rect.centerx + 30
                    y = rect.bottom - 100 - salto
                    pygame.draw.rect(pantalla, NEGRO, (x - 3, y - 3, 24, 39))
                    pygame.draw.rect(pantalla, (60, 60, 70), (x, y, 18, 33))
                    pygame.draw.rect(pantalla, (120, 220, 255), (x + 3, y + 3, 12, 18))
            else:
                pygame.draw.rect(pantalla, (40, 42, 54), rect)
                puntos = "." * (int(t * 3) % 4)
                _texto_centrado_en(pantalla, fuente_chica, "CONECTANDO" + puntos, rect.center, (150, 150, 170))

            # Nombre abajo a la izquierda
            etiqueta = fuente_chica.render(nombre + (" (VOS)" if nombre == jugador else ""), True, BLANCO)
            caja = etiqueta.get_rect(bottomleft=(rect.x + 6, rect.bottom - 4)).inflate(8, -2)
            pygame.draw.rect(pantalla, (0, 0, 0), caja)
            pantalla.blit(etiqueta, etiqueta.get_rect(center=caja.center))

            # Borde: verde el que habla, gris el resto
            color = (90, 230, 120) if nombre == hablando else (90, 90, 110)
            pygame.draw.rect(pantalla, color, rect.inflate(8, 8), 4)

        # --------------------------------------------------
        # DIALOGO
        # --------------------------------------------------

        if linea >= 0:

            velo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            velo.fill((0, 0, 0, int(80 * min(1.0, (t - t_dialogo) / 0.25))))
            pantalla.blit(velo, (0, 0))

            quien, partes = lineas[linea]

            _dibujar_cuadro(pantalla, fuente_media, quien, PERSONAJES[quien][1])

            for nombre in banco:
                retratos[nombre].dibujar(pantalla)

            retratos[quien].dibujar(pantalla, int(abs(math.sin(t / 0.32 * math.pi)) * 3) if escribiendo else 0)

            restantes = int(letras)
            alto_linea = fuente_media.get_height() - 4
            for k, parte in enumerate(partes):
                if restantes <= 0:
                    break
                _dibujar_texto_con_sombra(pantalla, fuente_media, parte[:restantes], BLANCO, (TEXTO_X, TEXTO_Y + k * alto_linea))
                restantes -= len(parte)

            if not escribiendo:
                _dibujar_flechita(pantalla, t)

        ayuda = fuente_chica.render("ESC: saltear", True, (230, 230, 230))
        pantalla.blit(ayuda, ayuda.get_rect(topright=(ancho - 10, 8)))

        pygame.display.flip()


def _texto_centrado_en(pantalla, fuente, texto, centro, color=BLANCO):

    imagen = fuente.render(texto, True, color)
    pantalla.blit(imagen, imagen.get_rect(center=centro))


# ==========================================================
# 3) REENCUENTRO CON CARLITOS (DESDE EL MAPA)
# ==========================================================

def reencuentro_carlitos(pantalla, reloj, fuente_grande, fuente_media):
    """Iki y Carlitos corren a abrazarse... y Carlitos lo muerde."""

    # Suena hasta la mordida (ahi se corta y suena "faaaa")
    musica.reproducir_cancion("reencuentro_iki")

    try:
        _reencuentro(pantalla, reloj, fuente_grande, fuente_media)
    finally:
        musica.detener()


def _reencuentro(pantalla, reloj, fuente_grande, fuente_media):

    ancho, alto = pantalla.get_size()
    fuente_chica = type(fuente_media)(2)

    fondo = _cargar_escalado("assets/historia/bolivar.png", ESCALA_FONDO)
    camara = 700        # un pedazo de la cuadra con casas y arboles

    iki_p = _cargar_iki(ESCALA_PERSONAJES)
    iki = iki_p["quieto"]
    perro_der, perro_izq = _cargar_carlitos(ESCALA_PERRO)

    t = 0.0
    x_iki = -40.0
    x_perro = ancho + 40.0          # borde izquierdo del perro

    VELOCIDAD = 230
    CAMARA_LENTA = 0.22             # que tan lento van al acercarse

    t_mordida = None
    t_escapa = None
    t_final = None
    corazones = []

    while True:

        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt

        avanzar, saltear = _leer_teclas()

        if saltear:
            return

        if avanzar and t_final is not None and t - t_final > 1.0:
            return

        iki_rect = iki.get_rect(midbottom=(int(x_iki), PISO_Y))
        distancia = x_perro - iki_rect.centerx

        # --------------------------------------------------
        # MOVIMIENTO
        # --------------------------------------------------

        lento = t_mordida is None and distancia < 230
        factor = CAMARA_LENTA if lento else 1.0

        if t_mordida is None:
            x_iki += VELOCIDAD * factor * dt
            x_perro -= VELOCIDAD * factor * dt

            if lento and random.random() < 0.12:
                corazones.append([iki_rect.centerx + distancia / 2 + random.randint(-60, 60), PISO_Y - 90, t])

            # A punto de abrazarse... ¡ÑAM!
            if distancia <= 34:
                t_mordida = t
                musica.detener(80)
                sonidos.reproducir("golpe")
                sonidos.reproducir("faaaa")

        if t_mordida is not None and t_escapa is None and t - t_mordida >= 1.2:
            t_escapa = t
            x_perro = iki_rect.centerx + 10

        if t_escapa is not None:
            x_perro += VELOCIDAD * 1.9 * dt
            if t_final is None and x_perro > ancho + 60:
                t_final = t

        if t_final is not None and t - t_final >= 4.0:
            return

        # --------------------------------------------------
        # DIBUJAR
        # --------------------------------------------------

        pantalla.fill(NEGRO)
        pantalla.blit(fondo, (-camara, 0))

        # Corazoncitos (camara lenta), se rompen con la mordida
        for c in corazones:
            vida = t - c[2]
            if vida < 1.6 and (t_mordida is None or t - t_mordida < 0.15):
                _corazon(pantalla, int(c[0]), int(c[1] - vida * 40), 3, int(255 * (1 - vida / 1.6)))

        # Iki
        if t_mordida is None:
            # Corre con las poses de caminar (mas rapido) dando saltitos
            imagen = iki_p["caminar"][int(t * (14 * factor + 2)) % 4]
            paso = int(abs(math.sin(t * (14 * factor + 3))) * 6)
            _sombra(pantalla, iki_rect.centerx, 50)
            pantalla.blit(imagen, imagen.get_rect(midbottom=(iki_rect.centerx, PISO_Y + 4 - paso)))
            # Rayitas de velocidad detras
            if not lento:
                for k in range(3):
                    y = iki_rect.top + 20 + k * 18
                    pygame.draw.line(pantalla, BLANCO, (iki_rect.left - 40, y), (iki_rect.left - 10, y), 3)
            if t < 2.2:
                _dibujar_globo(pantalla, fuente_chica, iki_rect.centerx, iki_rect.top - 6, "¡CARLITOS!")
        else:
            dt_m = t - t_mordida
            salto = _dibujar_iki_mordido(pantalla, iki_p, iki_rect.centerx, dt_m, t)
            if dt_m < 3.2:
                _grito(pantalla, fuente_grande, "¡AAAAAAY!", iki_rect.centerx, iki_rect.top - 20 - salto, t)
            else:
                _estrellitas(pantalla, iki_rect.centerx, iki_rect.top - 6, t)

        # Carlitos
        if t_mordida is None:
            imagen = perro_izq["correr"][int(t * 14 * factor + 1) % 4]
            rect = imagen.get_rect(bottomleft=(int(x_perro), PISO_Y + 2))
            _sombra(pantalla, rect.centerx, 70)
            pantalla.blit(imagen, rect)
            if t < 2.2:
                _dibujar_globo(pantalla, fuente_chica, rect.centerx - 30, rect.top - 4, "¡GUAU!")
        elif t_escapa is None:
            imagen = perro_izq["morder"]
            dt_m = t - t_mordida
            salto = int(math.sin(dt_m / 0.5 * math.pi) * 60) if dt_m < 0.5 else 0
            x, y = _posicion_mordida(iki_rect.move(0, -salto), imagen, True)
            pantalla.blit(imagen, (x + int(math.sin(t * 40) * 4), y))
        elif t_final is None:
            imagen = perro_der["correr"][int(t * 16) % 4]
            rect = imagen.get_rect(bottomleft=(int(x_perro), PISO_Y + 2))
            _sombra(pantalla, rect.centerx, 70)
            pantalla.blit(imagen, rect)
            _dibujar_globo(pantalla, fuente_chica, rect.centerx, rect.top - 4, "jeje")

        # Franja de abajo
        pygame.draw.rect(pantalla, NEGRO, (0, ALTO_FONDO, ancho, alto - ALTO_FONDO))

        if t < 3.0:
            alfa = int(255 * min(1.0, t / 0.5, (3.0 - t) / 0.5))
            _texto_centrado(pantalla, fuente_media, "EL REENCUENTRO", ALTO_FONDO + 70, alfa)

        if t_final is not None:
            alfa = int(255 * min(1.0, (t - t_final) / 0.8))
            _texto_centrado(pantalla, fuente_media, "Carlitos se escapó otra vez...", ALTO_FONDO + 70, alfa)

        if t_final is not None and t - t_final > 3.2:
            negro = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            negro.fill((0, 0, 0, int(255 * min(1.0, (t - t_final - 3.2) / 0.8))))
            pantalla.blit(negro, (0, 0))

        ayuda = fuente_chica.render("ESC: saltear", True, (230, 230, 230))
        pantalla.blit(ayuda, ayuda.get_rect(topright=(ancho - 10, 8)))

        pygame.display.flip()

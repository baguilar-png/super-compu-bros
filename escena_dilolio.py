"""
Escena de presentacion de DI LOLIO, el enemigo nuevo.

Aparece una vez por partida: despues de pasar el nivel 4, antes de empezar el 5.

    1. Di Lolio camina por la villa (el fondo se mueve detras de el).
    2. Le suena el celular (assets/sonidos/telefono.wav), se frena.
    3. Atiende: Lord Teichi le habla por telefono y Di Lolio contesta.
       Dialogo igual que el de historia.py: el que habla se ve grande
       (aca, su cabeza) y cuando deja de hablar se achica, se pone gris
       y se va al costado.
    4. Termina y arranca el nivel 5.

ENTER / ESPACIO / click pasan el texto, ESC saltea la escena.

El fondo lo genera herramientas/generar_villa.py. Las cabezas estan en
assets/personajes/TEICHI/teichi cabeza.png y
assets/personajes/DILOLIO/cabeza.png.
"""

import math
import random
import sys

import pygame

import sonidos
from historia import (
    BLANCO,
    CUADRO,
    FPS,
    NEGRO,
    TEXTO_ANCHO,
    TEXTO_X,
    TEXTO_Y,
    Retrato,
    _cargar,
    _dibujar_cuadro,
    _dibujar_flechita,
    _dibujar_texto_con_sombra,
    _escalar,
    _partir_en_lineas,
)


# ==========================================================
# PERSONAJES Y DIALOGO
# ==========================================================

# nombre -> (cabeza, escala del retrato grande, color del cartel)
CABEZAS = {
    "LORD TEICHI": ("assets/personajes/TEICHI/teichi cabeza.png", 6, (120, 30, 40)),
    "DI LOLIO": ("assets/personajes/DILOLIO/cabeza.png", 7, (30, 50, 150)),
}

# Sprites de Di Lolio (40x40, los mismos del hincha lanzador). Las poses
# de caminar miran a la derecha.
SPRITE_FRENTE = "assets/personajes/DILOLIO/frente.png"
SPRITES_CAMINAR = [
    "assets/personajes/DILOLIO/caminar_1.png",
    "assets/personajes/DILOLIO/caminar_2.png",
    "assets/personajes/DILOLIO/caminar_3.png",
    "assets/personajes/DILOLIO/caminar_4.png",
]
CUADROS_POR_SEGUNDO = 8     # velocidad de la animacion de caminar

DIALOGO = [
    ("LORD TEICHI", "Necesito que impidas que los Compus Broskis sigan avanzando."),
    ("LORD TEICHI", "A este punto no voy a poder gozar del alma de Mxroy."),
    ("DI LOLIO", "Altoke perri."),
]


# ==========================================================
# TIEMPOS (segundos)
# ==========================================================

DURACION_CAMINATA = 2.6     # camina antes de que suene el telefono
DURACION_RING = 3.0         # suena el telefono hasta que atiende
PAUSA_ATENDER = 0.5         # atiende y recien ahi habla Teichi
LETRAS_POR_SEGUNDO = 38


# ==========================================================
# MEDIDAS
# ==========================================================

ESCALA_FONDO = 2            # el fondo es pixel art de 218 de alto
ESCALA_DILOLIO = 4
X_DILOLIO = 330
PISO_Y = 404                # pies de Di Lolio

VELOCIDAD_CASAS = 70        # px por segundo en pantalla
VELOCIDAD_LEJOS = 22

ESCALA_BANCO = 3            # cabezas chicas y grises al costado

# Centro del panel del retrato (el mismo que en historia.py)
RETRATO_X = CUADRO.x + 112
RETRATO_BASE = CUADRO.bottom - 14


# ==========================================================
# FONDO
# ==========================================================

def _cielo(ancho, alto):
    """Cielo de atardecer: violeta arriba, naranja abajo."""

    cielo = pygame.Surface((ancho, alto))

    arriba = (62, 34, 98)
    abajo = (238, 138, 92)

    for y in range(alto):
        f = y / max(1, alto - 1)
        color = tuple(int(arriba[i] + (abajo[i] - arriba[i]) * f) for i in range(3))
        pygame.draw.rect(cielo, color, (0, y, ancho, 1))

    return cielo


def _cargar_capa(ruta):

    try:
        return _escalar(_cargar(ruta), ESCALA_FONDO)
    except (pygame.error, FileNotFoundError):
        return None


def _tierra(ancho, alto):

    azar = random.Random(7)
    tierra = pygame.Surface((ancho, alto))
    tierra.fill((138, 106, 72))

    colores = [(156, 123, 86), (117, 90, 62), (168, 138, 100)]
    for _ in range(ancho * alto // 90):
        x = azar.randrange(0, ancho, 2)
        y = azar.randrange(0, alto, 2)
        pygame.draw.rect(tierra, azar.choice(colores), (x, y, 2, 2))

    for _ in range(ancho // 260):
        w = azar.randint(40, 80)
        x = azar.randint(0, ancho - w)
        y = azar.randint(20, max(21, alto - 30))
        pygame.draw.ellipse(tierra, (94, 127, 150), (x, y, w, 14))
        pygame.draw.rect(tierra, (159, 192, 212), (x + 8, y + 4, w // 2, 2))

    return tierra


class FondoVilla:

    def __init__(self, ancho, alto):

        self.ancho = ancho
        self.alto = alto

        self.lejos = _cargar_capa("assets/historia/villa_lejos.png")
        self.casas = _cargar_capa("assets/historia/villa_casas.png")

        alto_fondo = self.casas.get_height() if self.casas else 436
        self.cielo = _cielo(ancho, alto_fondo)

        # Calle de abajo (debajo de la capa de casas): tierra con
        # piedritas y algun charco, se mueve junto con las casas
        self.alto_fondo = alto_fondo
        ancho_tierra = self.casas.get_width() if self.casas else ancho
        self.tierra = _tierra(ancho_tierra, max(1, alto - alto_fondo))

    def dibujar(self, pantalla, avance):

        pantalla.blit(self.cielo, (0, 0))

        if self.lejos is not None:
            x = -int(avance * VELOCIDAD_LEJOS / VELOCIDAD_CASAS) % max(1, self.lejos.get_width() - self.ancho)
            pantalla.blit(self.lejos, (-x, 0))

        if self.casas is not None:
            x = int(avance) % max(1, self.casas.get_width() - self.ancho)
            pantalla.blit(self.casas, (-x, 0))

            pantalla.blit(self.tierra, (-x, self.alto_fondo))


# ==========================================================
# CELULAR
# ==========================================================

def _dibujar_celular(pantalla, x, y, escala=3, pantalla_prendida=True):
    """Celular pixel art (6x11 pixeles)."""

    e = escala
    pygame.draw.rect(pantalla, NEGRO, (x - e, y - e, 8 * e, 13 * e))
    pygame.draw.rect(pantalla, (60, 60, 70), (x, y, 6 * e, 11 * e))
    color = (120, 220, 255) if pantalla_prendida else (30, 40, 60)
    pygame.draw.rect(pantalla, color, (x + e, y + e, 4 * e, 6 * e))
    pygame.draw.rect(pantalla, (30, 30, 36), (x + 2 * e, y + 8 * e, 2 * e, 2 * e))


def _dibujar_ring(pantalla, fuente, centro_x, base_y, t):
    """Celular vibrando con un globo de "RING RING"."""

    temblor = int(math.sin(t * 60) * 3)

    _dibujar_celular(pantalla, centro_x - 15 + temblor, base_y - 52, 5, pantalla_prendida=int(t * 6) % 2 == 0)

    # Rayitas de vibracion
    for lado in (-1, 1):
        for k in range(2):
            x = centro_x + lado * (30 + k * 9) + temblor
            pygame.draw.line(pantalla, BLANCO, (x, base_y - 44), (x, base_y - 18), 4)

    texto = fuente.render("RING RING!", True, NEGRO)
    globo = texto.get_rect()
    globo.inflate_ip(16, -4)
    globo.midbottom = (centro_x + 40, base_y - 62)

    pygame.draw.rect(pantalla, BLANCO, globo)
    pygame.draw.rect(pantalla, NEGRO, globo, 3)
    pantalla.blit(texto, texto.get_rect(center=(globo.centerx, globo.centery + 1)))


# ==========================================================
# ESCENA
# ==========================================================

def escena_dilolio(pantalla, reloj, fuente_grande, fuente_media):
    """Muestra la escena. Vuelve al terminar o con ESC."""

    try:
        _escena(pantalla, reloj, fuente_media)
    finally:
        sonidos.detener("telefono")
        sonidos.detener("teclado")


def _escena(pantalla, reloj, fuente_media):

    ancho, alto = pantalla.get_size()

    fuente_chica = type(fuente_media)(2)

    fondo = FondoVilla(ancho, alto)

    frente = _escalar(_cargar(SPRITE_FRENTE), ESCALA_DILOLIO)
    caminar = [_escalar(_cargar(ruta), ESCALA_DILOLIO) for ruta in SPRITES_CAMINAR]

    def cabeza(nombre, ruta):
        imagen = _cargar(ruta)
        # Todavia no se sabe como es Teichi: su cara es una silueta negra
        if nombre == "LORD TEICHI":
            imagen = imagen.copy()
            for x in range(imagen.get_width()):
                for y in range(imagen.get_height()):
                    a = imagen.get_at((x, y))[3]
                    if a:
                        imagen.set_at((x, y), (8, 8, 12, a))
        return imagen

    retratos = {
        nombre: Retrato(nombre, cabeza(nombre, ruta))
        for nombre, (ruta, _, _) in CABEZAS.items()
    }

    lineas_dialogo = [
        (quien, _partir_en_lineas(fuente_media, texto, TEXTO_ANCHO))
        for quien, texto in DIALOGO
    ]

    banco = []
    hablando = None
    linea = -1
    letras = 0.0
    total_letras = 0

    t = 0.0
    avance = 0.0            # cuanto se movio el fondo
    t_dialogo = None
    sono = False
    atendio = False

    t_ring = DURACION_CAMINATA
    t_atiende = t_ring + DURACION_RING
    t_hablar = t_atiende + PAUSA_ATENDER

    def pasar_a(indice):
        nonlocal linea, letras, total_letras, hablando

        linea = indice
        letras = 0.0
        quien, partes = lineas_dialogo[linea]
        total_letras = sum(len(p) for p in partes)

        if quien == hablando:
            return

        if hablando is not None and hablando not in banco:
            banco.append(hablando)

        if quien in banco:
            banco.remove(quien)

        hablando = quien

        retratos[quien].mandar_a(RETRATO_X, RETRATO_BASE, CABEZAS[quien][1], gris=False)

        x = CUADRO.right - 10
        for nombre in banco:
            ancho_chico = retratos[nombre].color.get_width() * ESCALA_BANCO
            retratos[nombre].mandar_a(x - ancho_chico // 2, CUADRO.y - 12, ESCALA_BANCO, gris=True)
            x -= ancho_chico + 12

    while True:

        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt

        # --------------------------------------------------
        # EVENTOS
        # --------------------------------------------------

        avanzar = False

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    return

                if evento.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                    avanzar = True

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                avanzar = True

        # --------------------------------------------------
        # FASES
        # --------------------------------------------------

        # Antes del dialogo, apretar adelanta: al telefono y despues a atender
        if avanzar and linea < 0:
            if t < t_ring:
                t = t_ring
            elif t < t_atiende:
                t = t_atiende
            avanzar = False

        caminando = t < t_ring

        if caminando:
            avance += VELOCIDAD_CASAS * dt

        if t >= t_ring and not sono:
            sono = True
            sonidos.reproducir_en_bucle("telefono")

        if t >= t_atiende and not atendio:
            atendio = True
            sonidos.detener("telefono")
            sonidos.reproducir("boton")

        if linea < 0 and t >= t_hablar:
            t_dialogo = t
            pasar_a(0)

        if linea >= 0:

            if letras < total_letras:
                letras = min(total_letras, letras + LETRAS_POR_SEGUNDO * dt)

            if avanzar:
                if letras < total_letras:
                    letras = total_letras
                elif linea + 1 < len(lineas_dialogo):
                    sonidos.reproducir("boton")
                    pasar_a(linea + 1)
                else:
                    sonidos.reproducir("boton")
                    return

        escribiendo = linea >= 0 and letras < total_letras

        if escribiendo:
            sonidos.reproducir_en_bucle("teclado")
        else:
            sonidos.detener("teclado")

        for retrato in retratos.values():
            retrato.actualizar(dt)

        # --------------------------------------------------
        # DIBUJAR
        # --------------------------------------------------

        fondo.dibujar(pantalla, avance)

        # Di Lolio: caminando usa las 4 poses; quieto mira al frente y
        # sube y baja cuando habla
        if caminando:
            dilolio = caminar[int(t * CUADROS_POR_SEGUNDO) % len(caminar)]
            salto = 0
        else:
            dilolio = frente
            if hablando == "DI LOLIO" and escribiendo:
                salto = int(abs(math.sin(t / 0.32 * math.pi)) * 6)
            else:
                salto = 0
        balanceo = 0

        sombra = pygame.Surface((100, 14), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
        pantalla.blit(sombra, (X_DILOLIO - 50, PISO_Y - 8))

        rect = dilolio.get_rect(midbottom=(X_DILOLIO + balanceo, PISO_Y - salto))
        pantalla.blit(dilolio, rect)

        # Rectangulo del cuerpo (sin el margen transparente del sprite)
        cuerpo = dilolio.get_bounding_rect().move(rect.topleft)

        # Celular: sonando al costado, o en la oreja una vez que atiende
        if sono and not atendio:
            _dibujar_ring(pantalla, fuente_media, cuerpo.right + 40, cuerpo.top + 70, t)
        elif atendio:
            # En la oreja (del lado derecho de la cabeza)
            _dibujar_celular(pantalla, cuerpo.right - 22, cuerpo.top + 34, 3)

        # --------------------------------------------------
        # DIALOGO
        # --------------------------------------------------

        if linea >= 0:

            velo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            velo.fill((0, 0, 0, int(90 * min(1.0, (t - t_dialogo) / 0.25))))
            pantalla.blit(velo, (0, 0))

            quien, partes = lineas_dialogo[linea]

            _dibujar_cuadro(pantalla, fuente_media, quien, CABEZAS[quien][2])

            for nombre in banco:
                retratos[nombre].dibujar(pantalla)

            salto_retrato = int(abs(math.sin(t / 0.32 * math.pi)) * 3) if escribiendo else 0
            retratos[quien].dibujar(pantalla, salto_retrato)

            restantes = int(letras)
            alto_linea = fuente_media.get_height() - 4
            for k, parte in enumerate(partes):
                if restantes <= 0:
                    break
                _dibujar_texto_con_sombra(
                    pantalla,
                    fuente_media,
                    parte[:restantes],
                    BLANCO,
                    (TEXTO_X, TEXTO_Y + k * alto_linea)
                )
                restantes -= len(parte)

            if not escribiendo:
                _dibujar_flechita(pantalla, t)

            # Teichi habla por telefono
            if quien == "LORD TEICHI":
                aviso = fuente_chica.render("(por telefono)", True, (200, 200, 220))
                pantalla.blit(aviso, aviso.get_rect(bottomleft=(TEXTO_X + 240, CUADRO.y + 2)))

        ayuda = fuente_chica.render("ESC: saltear", True, (230, 230, 230))
        pantalla.blit(ayuda, ayuda.get_rect(topright=(ancho - 10, 8)))

        pygame.display.flip()

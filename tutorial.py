"""
NIVEL TUTORIAL (el boton INSTRUCCIONES del menu).

Se juega con el personaje elegido, sin vidas ni puntos:

    1. Al aparecer: "USA D PARA MOVERTE A LA DERECHA, A PARA MOVERTE A LA
       IZQUIERDA".
    2. Un poco mas adelante (afuera de la pantalla al aparecer):
       "USA S PARA AGACHARTE". Llega una pelota a la altura MAS BAJA que
       todavia pasa por arriba de un personaje agachado: de pie te pega.
       Si te pega, volves al principio de esa parte.
    3. Un bloque con "W PARA SALTAR".
    4. Un circuito de bloques (valla, escalera, vallas altas).
    5. Una bandera gris. Al tocarla se vuelve directo al menu.

ESC vuelve al menu en cualquier momento.

Los dibujos (bloque, piso y fondo) estan en assets/tutorial/ y la musica en
assets/musica/tutorial.mp3.
"""

import math
import os
import sys

import pygame

import musica
import sonidos

from juego import (
    ALTO,
    ANCHO,
    FPS,
    SALTO_FUERZA,
    SUELO_Y,
    Jugador,
    Pelota,
    cargar_sprites_pelotas
)


CARPETA = os.path.dirname(os.path.abspath(__file__))

CARPETA_TUTORIAL = os.path.join(CARPETA, "assets", "tutorial")


# ==========================================================
# AJUSTES
# ==========================================================

NEGRO = (0, 0, 0)

# Largo del nivel (da igual, solo tiene que entrar todo)
TUT_ANCHO = 5300

# Tamano de cada pixel de los dibujos (el piso mide justo lo que el suelo
# del juego: 12 pixeles de dibujo x 5 = 60)
ESCALA_BLOQUE = 4
ESCALA_PISO = 5
ESCALA_FONDO = 4

# Los textos van en el mundo (se ven al llegar a ellos), arriba de todo.
# (lineas, centro x, y de la primera linea)
Y_TEXTO = 50
INTERLINEA = 36

TEXTOS = [
    (
        ["USA D PARA MOVERTE A LA DERECHA,", "A PARA MOVERTE A LA IZQUIERDA"],
        400
    ),
    (["USA S PARA AGACHARTE"], 1500),
    (["W PARA SALTAR"], 2430)
]

# ---- pelota ----
# Cuando el jugador pasa por esta x sale una pelota desde la derecha
X_DISPARO_PELOTA = 1300

# Si te pega, volves a esta x (antes de que se vea el cartel de agacharse)
X_REAPARECER = 1000

# Mas lenta que las del juego (840) para dar tiempo a reaccionar
VELOCIDAD_PELOTA_TUTORIAL = 480

# Segundos que se queda titilando el jugador antes de reaparecer
ESPERA_REAPARECER = 0.9

# ---- bloques ----
# (x del borde izquierdo, cantidad de bloques apilados)
TORRES = [
    # un bloque para saltar ("W PARA SALTAR")
    (2400, 1),

    # circuito: una valla...
    (3050, 1),

    # ...una escalera que sube hasta 3 bloques y baja...
    (3350, 1),
    (3410, 2),
    (3470, 3),
    (3530, 3),
    (3590, 2),
    (3650, 1),

    # ...y vallas altas para el final
    (3950, 1),
    (4170, 2),
    (4400, 1),
    (4460, 2)
]

# ---- bandera ----
X_BANDERA = 4950
ALTO_POSTE = 190


# ==========================================================
# CARGA DE DIBUJOS
# ==========================================================

_recursos = {}


def _recortar(imagen):
    """Saca el borde transparente de un dibujo."""

    return imagen.subsurface(imagen.get_bounding_rect()).copy()


def _escalar(imagen, escala):

    return pygame.transform.scale(
        imagen,
        (imagen.get_width() * escala, imagen.get_height() * escala)
    )


def cargar_recursos():

    if _recursos:

        return _recursos

    def cargar(nombre):

        return pygame.image.load(
            os.path.join(CARPETA_TUTORIAL, nombre)
        ).convert_alpha()

    _recursos["bloque"] = _escalar(_recortar(cargar("bloque.png")), ESCALA_BLOQUE)

    _recursos["piso"] = _escalar(_recortar(cargar("piso.png")), ESCALA_PISO)

    _recursos["fondo"] = _escalar(cargar("fondo.png"), ESCALA_FONDO)

    return _recursos


# ==========================================================
# NIVEL
# ==========================================================

def crear_bloques(bloque):
    """Lista de rectangulos solidos a partir de TORRES."""

    ancho, alto = bloque.get_size()

    bloques = []

    for x, cantidad in TORRES:

        for i in range(cantidad):

            bloques.append(
                pygame.Rect(x, SUELO_Y - alto * (i + 1), ancho, alto)
            )

    return bloques


def altura_visible(sprite):
    """Alto (en pixeles) del dibujo visible, medido desde los pies."""

    return sprite.get_height() - sprite.get_bounding_rect().top


def crear_pelota(camara_x, jugador):
    """
    Pelota que entra por la derecha a la altura MAS BAJA que pasa por
    arriba del personaje agachado (sin tocarlo) y le pega si esta parado.
    """

    sprite = cargar_sprites_pelotas()[0]

    pelota = Pelota(sprite, camara_x + ANCHO + 120, 0)

    pelota.vel_x = -VELOCIDAD_PELOTA_TUTORIAL

    # El borde de abajo de la pelota queda justo arriba de la cabeza del
    # personaje agachado
    pelota.rect.bottom = (
        SUELO_Y - altura_visible(jugador.sprites["agachado_der"])
    )

    pelota.y = float(pelota.rect.y)

    return pelota


# ==========================================================
# FISICA DE LOS BLOQUES
# ==========================================================

def resolver_bloques(jugador, antes, bloques):
    """
    Los bloques son solidos: se puede caminar encima, chocan de costado y
    de abajo. `antes` es el rectangulo del jugador antes de moverse.
    """

    r = jugador.rect

    apoyado = False

    for b in bloques:

        solapa_x = r.right > b.left and r.left < b.right

        # Cayendo (o quieto) encima del bloque
        if (
            solapa_x
            and antes.bottom <= b.top
            and r.bottom >= b.top
            and jugador.vel_y >= 0
        ):

            r.bottom = b.top

            jugador.vel_y = 0

            apoyado = True

            continue

        if not r.colliderect(b):

            continue

        # Cabezazo contra el bloque de arriba
        if antes.top >= b.bottom and jugador.vel_y < 0:

            r.top = b.bottom

            jugador.vel_y = 0

        # De costado
        elif antes.right <= b.left:

            r.right = b.left

        elif antes.left >= b.right:

            r.left = b.right

        # Ya estaba adentro (por ejemplo al pararse): sale por donde
        # menos se metio
        else:

            salidas = [
                (r.right - b.left, "izq"),
                (b.right - r.left, "der"),
                (b.bottom - r.top, "abajo")
            ]

            _, lado = min(salidas)

            if lado == "izq":
                r.right = b.left
            elif lado == "der":
                r.left = b.right
            else:
                r.top = b.bottom
                jugador.vel_y = max(0, jugador.vel_y)

    if r.bottom < SUELO_Y:

        jugador.en_suelo = apoyado


# ==========================================================
# PELOTA CONTRA EL JUGADOR
# ==========================================================

def toca_pelota(jugador, pelota):
    """
    Choque por pixeles contra el dibujo del jugador TAL COMO SE VE en
    pantalla (el sprite se dibuja pegado abajo y al medio del rectangulo).
    """

    sprite = jugador.obtener_sprite_actual()

    caja = sprite.get_rect(midbottom=jugador.rect.midbottom)

    if not caja.colliderect(pelota.rect):

        return False

    mascara = pygame.mask.from_surface(sprite)

    return mascara.overlap(
        pelota.mask,
        (pelota.rect.x - caja.x, pelota.rect.y - caja.y)
    ) is not None


def resolver_pelota(jugador, pelota, bottom_anterior):
    """
    True si la pelota le pega al jugador. Si el jugador cae encima de la
    pelota la tira al piso y rebota (igual que en el juego).
    """

    if pelota.cayendo:

        return False

    if not toca_pelota(jugador, pelota):

        return False

    esta_cayendo = jugador.vel_y > 0

    viene_desde_arriba = bottom_anterior <= pelota.rect.top + 18

    if esta_cayendo and viene_desde_arriba:

        pelota.tirar()

        sonidos.reproducir("aplastar")

        jugador.rect.bottom = pelota.rect.top

        jugador.vel_y = SALTO_FUERZA * 0.55

        jugador.en_suelo = False

        return False

    return True


# ==========================================================
# DIBUJO
# ==========================================================

def dibujar_fondo(pantalla, fondo, camara_x):

    ancho, alto = fondo.get_size()

    x0 = -(camara_x % ancho)

    for x in range(x0, ANCHO, ancho):

        for y in range(0, ALTO, alto):

            pantalla.blit(fondo, (x, y))


def dibujar_piso(pantalla, piso, camara_x):

    ancho = piso.get_width()

    x0 = -(camara_x % ancho)

    for x in range(x0, ANCHO, ancho):

        pantalla.blit(piso, (x, SUELO_Y))


def dibujar_textos(pantalla, fuente, camara_x):

    for lineas, centro_x in TEXTOS:

        for i, linea in enumerate(lineas):

            texto = fuente.render(linea, True, NEGRO)

            rect = texto.get_rect(
                midtop=(centro_x - camara_x, Y_TEXTO + i * INTERLINEA)
            )

            # Solo si entra en pantalla
            if rect.right > 0 and rect.left < ANCHO:

                pantalla.blit(texto, rect)


GRIS_POSTE = (120, 120, 120)
GRIS_TELA = (173, 173, 173)
GRIS_CLARO = (204, 204, 204)
GRIS_OSCURO = (100, 100, 100)

PIXEL_BANDERA = 4
COLUMNAS_TELA = 18
FILAS_TELA = 11


def dibujar_bandera(pantalla, camara_x, tiempo):
    """Bandera gris pixel art que ondea."""

    x = X_BANDERA - camara_x

    if x < -200 or x > ANCHO + 200:

        return

    px = PIXEL_BANDERA

    arriba = SUELO_Y - ALTO_POSTE

    # base
    pygame.draw.rect(
        pantalla, GRIS_OSCURO, (x - 8, SUELO_Y - 2 * px, 24, 2 * px)
    )

    # poste
    pygame.draw.rect(
        pantalla, GRIS_POSTE, (x, arriba, 2 * px, ALTO_POSTE)
    )

    pygame.draw.rect(
        pantalla, GRIS_CLARO, (x, arriba, px, ALTO_POSTE)
    )

    # bolita de arriba
    pygame.draw.rect(
        pantalla, GRIS_OSCURO, (x - px, arriba - 2 * px, 4 * px, 2 * px)
    )

    # tela: columnas que suben y bajan de a un pixel
    for c in range(COLUMNAS_TELA):

        onda = round(math.sin(tiempo * 5 - c * 0.5) * 1.2)

        # la tela se queda quieta cerca del poste
        onda = round(onda * min(1.0, c / 4))

        cx = x + 2 * px + c * px

        cy = arriba + px + onda * px

        pygame.draw.rect(
            pantalla, GRIS_TELA, (cx, cy, px, FILAS_TELA * px)
        )

        # borde de arriba (claro) y de abajo (oscuro)
        pygame.draw.rect(pantalla, GRIS_CLARO, (cx, cy, px, px))

        pygame.draw.rect(
            pantalla, GRIS_OSCURO, (cx, cy + (FILAS_TELA - 1) * px, px, px)
        )


# ==========================================================
# TUTORIAL
# ==========================================================

def jugar_tutorial(pantalla, reloj, sprites, fuente_grande, fuente_media):
    """
    Corre el nivel tutorial. Devuelve "menu" (al llegar a la bandera o con
    ESC).
    """

    musica.reproducir(musica.MUSICA_TUTORIAL)

    rec = cargar_recursos()

    bloques = crear_bloques(rec["bloque"])

    jugador = Jugador(sprites)

    pelota = None

    # True una vez que salio la pelota (sale una sola vez, salvo que te pegue)
    pelota_lanzada = False

    # Segundos que faltan para reaparecer (None = jugando normal)
    reaparecer = None

    tiempo = 0.0

    rect_bandera = pygame.Rect(
        X_BANDERA - 10, SUELO_Y - ALTO_POSTE, 100, ALTO_POSTE
    )

    while True:

        dt = min(reloj.tick(FPS) / 1000.0, 0.05)

        tiempo += dt

        # ------------------------------------------------------
        # EVENTOS
        # ------------------------------------------------------

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:

                return "menu"

        teclas = pygame.key.get_pressed()

        # ------------------------------------------------------
        # JUGADOR
        # ------------------------------------------------------

        bottom_anterior = jugador.rect.bottom

        if reaparecer is None:

            antes = jugador.rect.copy()

            jugador.mover(teclas, dt)

            resolver_bloques(jugador, antes, bloques)

            jugador.rect.right = min(TUT_ANCHO, jugador.rect.right)

        jugador.actualizar_parpadeo(dt)

        camara_x = max(
            0,
            min(jugador.rect.centerx - ANCHO // 2, TUT_ANCHO - ANCHO)
        )

        # ------------------------------------------------------
        # PELOTA
        # ------------------------------------------------------

        if (
            not pelota_lanzada
            and reaparecer is None
            and jugador.rect.centerx >= X_DISPARO_PELOTA
        ):

            pelota = crear_pelota(camara_x, jugador)

            pelota_lanzada = True

        if pelota is not None:

            pelota.mover(dt)

            if pelota.salio_de_pantalla(camara_x) or pelota.terminada:

                pelota = None

        if (
            pelota is not None
            and reaparecer is None
            and resolver_pelota(jugador, pelota, bottom_anterior)
        ):

            # Te pego: titila y vuelve al principio de esta parte
            reaparecer = ESPERA_REAPARECER

            sonidos.reproducir("golpe")

            jugador.iniciar_parpadeo()

        if reaparecer is not None:

            reaparecer -= dt

            if reaparecer <= 0:

                reaparecer = None

                jugador = Jugador(sprites)

                jugador.rect.x = X_REAPARECER

                pelota = None

                pelota_lanzada = False

                continue

        # ------------------------------------------------------
        # BANDERA: se termina el tutorial
        # ------------------------------------------------------

        if reaparecer is None and jugador.rect.colliderect(rect_bandera):

            sonidos.reproducir("meta")

            return "menu"

        # ------------------------------------------------------
        # DIBUJO
        # ------------------------------------------------------

        dibujar_fondo(pantalla, rec["fondo"], camara_x)

        dibujar_textos(pantalla, fuente_media, camara_x)

        dibujar_piso(pantalla, rec["piso"], camara_x)

        for b in bloques:

            if b.right > camara_x and b.left < camara_x + ANCHO:

                pantalla.blit(rec["bloque"], (b.x - camara_x, b.y))

        dibujar_bandera(pantalla, camara_x, tiempo)

        if pelota is not None:

            pelota.dibujar(pantalla, camara_x)

        jugador.dibujar(pantalla, camara_x)

        pygame.display.flip()

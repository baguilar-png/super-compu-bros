"""
Niveles de JEFE (el 15 y el 30). juego.jugar() los manda aca.

NIVEL 30 - BURZACO: EL CASTILLO DE LORD TEICHI
    Un castillo largo lleno de cuadros (las imagenes de
    assets/castillo/cuadros/), con muchos gagambas y hinchas, y pozos de
    LAVA: si te caes, moris. De la lava saltan bolas de fuego. Al final esta
    la puerta de la SALA DE LORD TEICHI: si moris adentro de la sala, volves
    a la sala (no al principio del castillo).

NIVEL 15 - LA BOMBONERA: un jefe provisorio (un CUBO) hasta que se defina
    quien es. Mismos ataques que Teichi. En vez de lava hay bombas en los
    costados.

COMO SE LE GANA A UN JEFE (combinacion de Mario 64 y Odyssey):

    Ataques del jefe
      - Tira piedras (en arco, hacia donde estas).
      - Golpe al piso: levanta los brazos, salta y cae: salen dos ondas por
        el piso para los costados. Hay que saltarlas.
      - Embestida: se agacha (aparece un "!") y sale corriendo derecho. Si
        llega al borde queda MAREADO.

    Como pegarle
      1) Cuando esta MAREADO (estrellitas), saltarle en la cabeza: le saca
         una vida.
      2) Cuando esta MAREADO, agarrarlo (tecla E) y revolearlo (E otra vez)
         a la lava (o contra una bomba): le saca una vida.
      3) Las piedras que tira quedan un rato en el piso: agarrarlas (E) y
         tirarselas (E) lo deja MAREADO.

    Tocarlo cuando no esta mareado, que te pegue una piedra o una onda, o
    caerte a la lava, es perder una vida.

Teclas nuevas: E (o K): agarrar / tirar.
Los sprites de Teichi estan en assets/personajes/TEICHI/ (los paso a pixel
art herramientas/extraer_pixelart.py).
"""

import glob
import math
import os
import random
import sys

import pygame

import cheats
import juego as J
import musica
import sonidos
import transicion
from archivos import (
    escena_vista,
    marcar_escena_vista,
    cargar_puntos,
    cargar_vidas_extra,
    completar_nivel,
    gastar_vida_extra,
    reiniciar_progreso,
)
from escenas_teichi import (
    dibujar_jaula,
    escena_final,
    escena_teichi_antes,
    imagen_mxroy,
)
from escenas_robot import (
    escena_robot_destruido,
    escena_robot_llega,
    nombre_robot,
    sprites_robot,
)
from historia import (
    CUADRO,
    RETRATO_GRANDE,
    TEXTO_ANCHO,
    TEXTO_X,
    TEXTO_Y,
    Retrato,
    _dibujar_cuadro,
    _dibujar_flechita,
    _dibujar_texto_con_sombra,
    _partir_en_lineas,
)

CARPETA = os.path.dirname(os.path.abspath(__file__))

ANCHO, ALTO = J.ANCHO, J.ALTO
FPS = J.FPS

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 214, 64)
ROJO = (230, 50, 50)

# y del piso en el mundo (el mismo de la calle, asi los hinchas tiran) y
# camara fija: el piso queda en la y 520 de la pantalla
PISO_Y = 804
PISO_PANTALLA = 520
CAMARA_Y = PISO_Y - PISO_PANTALLA

TECLAS_AGARRAR = (pygame.K_e, pygame.K_k)

CARPETA_CUADROS = os.path.join(CARPETA, "assets", "castillo", "cuadros")
CARPETA_TEICHI = os.path.join(CARPETA, "assets", "personajes", "TEICHI")

ESCALA_JEFE = 3


# ==========================================================
# TERRENO SIMPLE (pisos con pozos de lava y plataformas)
# ==========================================================

class TerrenoSimple:
    """
    Lo que el Jugador necesita de un terreno (ver terreno.py), para niveles
    hechos a mano: tramos de piso a la altura PISO_Y (entre tramo y tramo
    hay lava) y plataformas de un solo sentido.
    """

    def __init__(self, ancho, pisos, plataformas=(), inicio_x=100):

        self.ancho = ancho
        self.pisos = list(pisos)                    # [(x0, x1)]
        self.plataformas = list(plataformas)        # [(x0, x1, y)]
        self.inicio_x = inicio_x

        self.tiene_calle = True
        self.calle_y = PISO_Y
        self.escaleras = []
        self.interior = True
        self.meta_x = ancho + 10_000                # la meta es otra cosa

    def superficies(self):
        for x0, x1 in self.pisos:
            yield x0, x1, PISO_Y
        for x0, x1, y in self.plataformas:
            yield x0, x1, y

    def hay_piso(self, x):
        return any(x0 <= x <= x1 for x0, x1 in self.pisos)

    def pozos(self):
        """Tramos con lava (lo que no es piso)."""
        x = 0
        for x0, x1 in sorted(self.pisos):
            if x0 > x:
                yield x, x0
            x = max(x, x1)
        if x < self.ancho:
            yield x, self.ancho

    # --- lo que usa el Jugador ---

    def resolver_x(self, rect, x_antes):
        return rect.x

    def apoyo(self, izq, der, bottom_antes, bottom, vel_y):

        if vel_y < 0:
            return None

        mejor = None
        for x0, x1, y in self.superficies():
            if der - 8 > x0 and izq + 8 < x1 and bottom_antes <= y + 1 and bottom >= y:
                if mejor is None or y < mejor:
                    mejor = y
        return mejor

    def techo_en(self, x):
        return PISO_Y

    # --- lo que usan las botellas de los hinchas ---

    def superficie_bajo(self, x, y_ref, margen=1):
        mejor = None
        for x0, x1, y in self.superficies():
            if x0 <= x <= x1 and y >= y_ref - margen:
                if mejor is None or y < mejor:
                    mejor = y
        return mejor

    def choca_pared(self, rect, tolerancia=4):
        return False


# ==========================================================
# DIBUJOS: LAVA, ANTORCHAS, CUADROS, PIEDRA DEL CASTILLO
# ==========================================================

def dibujar_lava(pantalla, x0, x1, y, t, alto=None):
    """Lava animada entre x0 y x1 (pantalla), con la superficie en y."""

    alto = alto if alto is not None else ALTO - y
    if x1 <= 0 or x0 >= ANCHO:
        return

    x0, x1 = max(-10, int(x0)), min(ANCHO + 10, int(x1))

    pygame.draw.rect(pantalla, (170, 30, 10), (x0, y + 6, x1 - x0, alto))
    pygame.draw.rect(pantalla, (220, 70, 10), (x0, y + 6, x1 - x0, 14))

    # Superficie con olas
    puntos = [(x0, y + 30)]
    for x in range(x0, x1 + 6, 6):
        puntos.append((x, y + 6 + int(math.sin(x * 0.07 + t * 3.2) * 4)))
    puntos.append((x1, y + 30))
    pygame.draw.polygon(pantalla, (255, 120, 20), puntos)

    for x in range(x0 + ((int(t * 40)) % 24), x1, 24):
        yy = y + 8 + int(math.sin(x * 0.07 + t * 3.2) * 4)
        pygame.draw.rect(pantalla, (255, 220, 90), (x, yy, 6, 3))

    # Burbujas
    for k in range(max(1, (x1 - x0) // 50)):
        fase = (t * 0.7 + k * 0.37) % 1.0
        bx = x0 + ((k * 53 + 17) % max(1, x1 - x0))
        by = y + 40 - int(fase * 34)
        r = 3 + int(fase * 4)
        pygame.draw.circle(pantalla, (255, 170, 40), (bx, by), r)
        pygame.draw.circle(pantalla, (255, 230, 120), (bx - 1, by - 1), max(1, r - 3))


def dibujar_brillo_lava(pantalla, x0, x1, y):
    """Resplandor naranja arriba de la lava."""

    if x1 <= 0 or x0 >= ANCHO:
        return
    brillo = pygame.Surface((max(1, int(x1 - x0)), 90), pygame.SRCALPHA)
    for k in range(90):
        pygame.draw.line(brillo, (255, 110, 20, int(70 * (1 - k / 90) ** 2)), (0, 89 - k), (brillo.get_width(), 89 - k))
    pantalla.blit(brillo, (int(x0), y - 84))


def _pared_piedra(superficie, x0, x1, y0, y1, semilla=0):
    """Pared de ladrillos de piedra gris oscura."""

    azar = random.Random(semilla)
    pygame.draw.rect(superficie, (46, 44, 56), (x0, y0, x1 - x0, y1 - y0))
    fila = 0
    for y in range(y0, y1, 24):
        corrido = 24 if fila % 2 else 0
        for x in range(x0 - corrido, x1, 48):
            tono = azar.choice([(62, 60, 74), (58, 56, 70), (68, 66, 80), (54, 52, 66)])
            pygame.draw.rect(superficie, tono, (x + 2, y + 2, 44, 20))
            pygame.draw.line(superficie, (80, 78, 94), (x + 2, y + 2), (x + 45, y + 2))
        fila += 1


def _ventana_castillo(superficie, x, y):
    pygame.draw.rect(superficie, (20, 18, 28), (x - 4, y - 4, 48, 92))
    pygame.draw.ellipse(superficie, (20, 18, 28), (x - 4, y - 28, 48, 50))
    pygame.draw.rect(superficie, (30, 34, 70), (x, y, 40, 84))
    pygame.draw.ellipse(superficie, (30, 34, 70), (x, y - 22, 40, 44))
    pygame.draw.circle(superficie, (230, 230, 200), (x + 26, y + 10), 7)
    pygame.draw.line(superficie, (20, 18, 28), (x + 20, y - 20), (x + 20, y + 84), 3)
    pygame.draw.line(superficie, (20, 18, 28), (x, y + 30), (x + 40, y + 30), 3)


def _estandarte(superficie, x, y):
    pygame.draw.rect(superficie, (90, 70, 30), (x - 30, y - 6, 60, 6))
    pygame.draw.polygon(superficie, (130, 20, 30), [(x - 24, y), (x + 24, y), (x + 24, y + 110), (x, y + 92), (x - 24, y + 110)])
    pygame.draw.polygon(superficie, (200, 160, 40), [(x - 24, y), (x + 24, y), (x + 24, y + 110), (x, y + 92), (x - 24, y + 110)], 3)
    # Una "T" de Teichi
    pygame.draw.rect(superficie, (220, 180, 50), (x - 12, y + 24, 24, 6))
    pygame.draw.rect(superficie, (220, 180, 50), (x - 3, y + 24, 6, 36))


def _antorcha_soporte(superficie, x, y):
    pygame.draw.rect(superficie, (40, 30, 24), (x - 3, y, 6, 26))
    pygame.draw.polygon(superficie, (70, 50, 30), [(x - 9, y), (x + 9, y), (x + 5, y + 10), (x - 5, y + 10)])


def dibujar_fuego(pantalla, x, y, t, k=0):
    """Llama de antorcha que titila (x, y = base de la llama)."""

    f = math.sin(t * 13 + k * 1.7) * 2 + math.sin(t * 7.3 + k) * 2
    pygame.draw.ellipse(pantalla, (255, 120, 20), (x - 8, y - 22 - f, 16, 24 + f))
    pygame.draw.ellipse(pantalla, (255, 220, 80), (x - 4, y - 14 - f / 2, 8, 14 + f / 2))


def cargar_cuadros():
    """Las imagenes de assets/castillo/cuadros/ (png, jpg o jpeg)."""

    rutas = []
    for patron in ("*.png", "*.jpg", "*.jpeg", "*.PNG", "*.JPG", "*.JPEG"):
        rutas += glob.glob(os.path.join(CARPETA_CUADROS, patron))

    imagenes = []
    for ruta in sorted(set(rutas)):
        try:
            imagenes.append(pygame.image.load(ruta).convert_alpha())
        except (pygame.error, FileNotFoundError):
            pass
    return imagenes


def _cuadro(imagen, ancho_max, alto_max, fuente=None):
    """Cuadro con marco dorado. Sin imagen: un marco con un signo '?'."""

    if imagen is not None:
        w, h = imagen.get_size()
        escala = min(ancho_max / w, alto_max / h)
        w, h = max(8, int(w * escala)), max(8, int(h * escala))
        try:
            pintura = pygame.transform.smoothscale(imagen, (w, h))
        except (ValueError, pygame.error):
            pintura = pygame.transform.scale(imagen, (w, h))
    else:
        w, h = ancho_max, alto_max
        pintura = pygame.Surface((w, h))
        pintura.fill((60, 40, 70))
        if fuente is not None:
            signo = fuente.render("?", True, (200, 170, 90))
            pintura.blit(signo, signo.get_rect(center=(w // 2, h // 2)))

    marco = pygame.Surface((w + 24, h + 24), pygame.SRCALPHA)
    marco.fill((120, 80, 20))
    pygame.draw.rect(marco, (220, 170, 60), marco.get_rect(), 4)
    pygame.draw.rect(marco, (250, 220, 120), marco.get_rect().inflate(-8, -8), 2)
    pygame.draw.rect(marco, (60, 36, 10), marco.get_rect().inflate(-18, -18))
    marco.blit(pintura, (12, 12))
    return marco


def _piso_piedra(superficie, x0, x1, y):
    """Piso de bloques de piedra (de y para abajo)."""

    pygame.draw.rect(superficie, (90, 86, 100), (x0, y, x1 - x0, ALTO - y))
    for bx in range(x0, x1, 40):
        pygame.draw.rect(superficie, (110, 106, 122), (bx + 1, y + 1, 38, 18))
        pygame.draw.rect(superficie, (74, 70, 84), (bx + 1, y + 21, 38, 36))
        pygame.draw.line(superficie, (140, 136, 150), (bx + 1, y + 1), (bx + 38, y + 1))
    pygame.draw.line(superficie, (20, 18, 24), (x0, y), (x1, y), 2)
    pygame.draw.line(superficie, (20, 18, 24), (x0, y), (x0, ALTO), 2)
    pygame.draw.line(superficie, (20, 18, 24), (x1 - 1, y), (x1 - 1, ALTO), 2)


def _plataforma_piedra(pantalla, x0, x1, y):
    pygame.draw.rect(pantalla, (20, 18, 24), (x0 - 2, y - 2, x1 - x0 + 4, 22))
    pygame.draw.rect(pantalla, (110, 106, 122), (x0, y, x1 - x0, 18))
    for bx in range(int(x0), int(x1), 30):
        pygame.draw.line(pantalla, (74, 70, 84), (bx, y), (bx, y + 18))
    pygame.draw.line(pantalla, (150, 146, 160), (x0, y), (x1, y), 2)
    # Cadenas de las que cuelga
    for cx in (x0 + 10, x1 - 10):
        for cy in range(int(y) - 200, int(y), 10):
            pygame.draw.ellipse(pantalla, (70, 70, 80), (cx - 3, cy, 6, 9), 2)


# ==========================================================
# FONDOS
# ==========================================================

class FondoCastillo:
    """
    El castillo (o la sala del trono): paredes de piedra con ventanas,
    estandartes, antorchas y cuadros. Se dibuja todo una vez (lo que no se
    mueve) y la lava y el fuego se animan en cada frame.
    """

    def __init__(self, terreno, cuadros, fuente, separacion_cuadros=230, sala=False, semilla=7, sin_cuadros=None):

        self.terreno = terreno
        self.t = 0.0
        self.oscuro = True

        ancho = terreno.ancho
        self.imagen = pygame.Surface((ancho, ALTO))
        _pared_piedra(self.imagen, 0, ancho, 0, ALTO, semilla)

        azar = random.Random(semilla)
        self.antorchas = []

        # Columnas
        for x in range(160, ancho, 640):
            pygame.draw.rect(self.imagen, (36, 34, 44), (x, 0, 40, PISO_PANTALLA))
            pygame.draw.rect(self.imagen, (76, 74, 90), (x + 4, 0, 6, PISO_PANTALLA))

        # Ventanas y estandartes
        for x in range(420, ancho, 640):
            _ventana_castillo(self.imagen, x, 60)
        for x in range(260, ancho, 640):
            _estandarte(self.imagen, x, 34)

        # Cuadros: uno atras del otro, todo el largo del castillo
        x = 80 if sala else 300
        k = 0
        while x < ancho - 160:
            imagen = cuadros[k % len(cuadros)] if cuadros else None
            alto_max = azar.choice([96, 110, 124])
            marco = _cuadro(imagen, 150, alto_max, fuente)
            y = azar.choice([170, 190, 210]) if not sala else 160
            # Sin tapar las ventanas ni la puerta de la sala del jefe
            tapa_puerta = sin_cuadros is not None and x + marco.get_width() > sin_cuadros[0] and x < sin_cuadros[1]
            if not tapa_puerta and not any(abs(x + marco.get_width() // 2 - c) < 70 for c in range(420 + 20, ancho, 640)):
                self.imagen.blit(marco, (x, y))
                # Clavo y cordel
                pygame.draw.line(self.imagen, (40, 30, 20), (x + marco.get_width() // 2, y - 26), (x + 12, y), 2)
                pygame.draw.line(self.imagen, (40, 30, 20), (x + marco.get_width() // 2, y - 26), (x + marco.get_width() - 12, y), 2)
                pygame.draw.circle(self.imagen, (180, 160, 90), (x + marco.get_width() // 2, y - 26), 3)
                k += 1
                x += marco.get_width() + separacion_cuadros
            else:
                x += 90

        # Antorchas entre los cuadros
        for x in range(110, ancho, 320):
            _antorcha_soporte(self.imagen, x, 330)
            self.antorchas.append((x, 330))

        # Piso de piedra en los tramos con piso
        for x0, x1 in terreno.pisos:
            _piso_piedra(self.imagen, x0, x1, PISO_PANTALLA)

        # Oscurecer un poco hacia arriba
        sombra = pygame.Surface((ancho, 200), pygame.SRCALPHA)
        for y in range(200):
            pygame.draw.line(sombra, (0, 0, 0, int(120 * (1 - y / 200))), (0, y), (ancho, y))
        self.imagen.blit(sombra, (0, 0))

    def actualizar(self, dt):
        self.t += dt

    def dibujar(self, pantalla, camara_x, camara_y=0):

        pantalla.blit(self.imagen, (-int(camara_x), 0))

        for k, (x, y) in enumerate(self.antorchas):
            sx = x - camara_x
            if -30 < sx < ANCHO + 30:
                dibujar_fuego(pantalla, sx, y, self.t, k)

        for x0, x1 in self.terreno.pozos():
            dibujar_brillo_lava(pantalla, x0 - camara_x, x1 - camara_x, PISO_PANTALLA + 10)
            dibujar_lava(pantalla, x0 - camara_x, x1 - camara_x, PISO_PANTALLA + 10, self.t)

        for x0, x1, y in self.terreno.plataformas:
            _plataforma_piedra(pantalla, x0 - camara_x, x1 - camara_x, y - CAMARA_Y)


class FondoBombonera:
    """La Bombonera de noche: tribunas azul y oro llenas de gente (tan
    ancha como la arena)."""

    def __init__(self, terreno):

        self.terreno = terreno
        self.t = 0.0
        self.oscuro = True
        ancho = terreno.ancho
        self.imagen = pygame.Surface((ancho, ALTO))

        cielo_a, cielo_b = (10, 14, 40), (40, 50, 100)
        for y in range(ALTO):
            f = y / ALTO
            pygame.draw.line(self.imagen, tuple(int(cielo_a[i] + (cielo_b[i] - cielo_a[i]) * f) for i in range(3)), (0, y), (ancho, y))

        azar = random.Random(12)

        # Tribunas en tres bandejas, azul y amarillo
        for k, (y0, y1) in enumerate(((150, 260), (270, 380), (390, 490))):
            color = (20, 60, 160) if k % 2 == 0 else (240, 200, 30)
            pygame.draw.rect(self.imagen, color, (0, y0, ancho, y1 - y0))
            pygame.draw.rect(self.imagen, (10, 10, 20), (0, y1, ancho, 10))
            for _ in range(ancho * 11 // 8):
                x = azar.randrange(0, ancho, 4)
                y = azar.randrange(y0 + 4, y1 - 4, 4)
                gente = azar.choice([(250, 210, 160), (200, 150, 110), (30, 60, 170), (250, 210, 40), (240, 240, 240)])
                pygame.draw.rect(self.imagen, gente, (x, y, 3, 3))

        # Torres de luz
        for x in range(60, ancho, 560):
            pygame.draw.rect(self.imagen, (60, 60, 70), (x - 4, 30, 8, 120))
            pygame.draw.rect(self.imagen, (240, 240, 220), (x - 30, 20, 60, 20))

        # Cancha
        pygame.draw.rect(self.imagen, (40, 140, 50), (0, PISO_PANTALLA, ancho, ALTO - PISO_PANTALLA))
        for x in range(0, ancho, 80):
            pygame.draw.rect(self.imagen, (50, 160, 60), (x, PISO_PANTALLA, 40, ALTO - PISO_PANTALLA))
        pygame.draw.line(self.imagen, BLANCO, (0, PISO_PANTALLA + 4), (ancho, PISO_PANTALLA + 4), 3)
        pygame.draw.rect(self.imagen, (20, 18, 24), (0, PISO_PANTALLA - 2, ancho, 3))
        # Linea de mitad de cancha
        pygame.draw.line(self.imagen, BLANCO, (ancho // 2, PISO_PANTALLA + 4), (ancho // 2, ALTO), 3)

        self.luces = [azar.randrange(0, ancho) for _ in range(30 * ancho // ANCHO)]

    def actualizar(self, dt):
        self.t += dt

    def dibujar(self, pantalla, camara_x=0, camara_y=0):
        pantalla.blit(self.imagen, (-int(camara_x), 0))
        # Flashes de la hinchada
        for k, x in enumerate(self.luces):
            if (self.t * 3 + k * 0.37) % 1.0 < 0.06:
                pygame.draw.circle(pantalla, BLANCO, (int(x - camara_x), 160 + (k * 37) % 320), 3)
        # Plataformas: andamios de metal
        for x0, x1, y in self.terreno.plataformas:
            _plataforma_metal(pantalla, x0 - camara_x, x1 - camara_x, y - CAMARA_Y)


def _plataforma_metal(pantalla, x0, x1, y):
    pygame.draw.rect(pantalla, (20, 18, 24), (x0 - 2, y - 2, x1 - x0 + 4, 18))
    pygame.draw.rect(pantalla, (170, 176, 186), (x0, y, x1 - x0, 14))
    pygame.draw.line(pantalla, (230, 234, 240), (x0, y), (x1, y), 2)
    for px in range(int(x0) + 8, int(x1), 26):
        pygame.draw.line(pantalla, (90, 94, 104), (px, y + 14), (px - 10, PISO_PANTALLA), 3)
        pygame.draw.line(pantalla, (90, 94, 104), (px, y + 14), (px + 10, PISO_PANTALLA), 3)


# ==========================================================
# BOLAS DE LAVA (saltan de los pozos)
# ==========================================================

# Bolas de lava: siempre salen del mismo lugar (repartidas parejo en cada
# pozo), a la misma altura y cada ESPERA_BOLA_LAVA segundos
ESPERA_BOLA_LAVA = 3.6
SALTO_BOLA_LAVA = 1050
DESFASE_BOLA_LAVA = 1.3      # para que las de un mismo pozo no salgan juntas


class BolaLava:

    def __init__(self, x, numero=0):
        self.x = float(x)
        self.y = PISO_Y + 40.0
        self.vy = 0.0
        self.espera = 1.5 + (numero * DESFASE_BOLA_LAVA) % ESPERA_BOLA_LAVA
        self.rect = pygame.Rect(0, 0, 26, 26)

    def actualizar(self, dt):
        if self.espera > 0:
            self.espera -= dt
            if self.espera <= 0:
                self.vy = -SALTO_BOLA_LAVA
            return
        self.vy += 2200 * dt
        self.y += self.vy * dt
        if self.y > PISO_Y + 40 and self.vy > 0:
            self.y = PISO_Y + 40
            self.espera = ESPERA_BOLA_LAVA
        self.rect.center = (int(self.x), int(self.y))

    @property
    def activa(self):
        return self.espera <= 0 and self.y < PISO_Y + 20

    def dibujar(self, pantalla, camara_x, t):
        if not self.activa:
            return
        x, y = int(self.x - camara_x), int(self.y - CAMARA_Y)
        cayendo = self.vy > 0
        # Cola de fuego
        for k in range(4):
            dy = (-1 if cayendo else 1) * (k + 1) * 8
            pygame.draw.circle(pantalla, (255, 140 - k * 25, 20), (x, y + dy), 11 - k * 2)
        pygame.draw.circle(pantalla, (20, 10, 10), (x, y), 14)
        pygame.draw.circle(pantalla, (255, 110, 20), (x, y), 12)
        pygame.draw.circle(pantalla, (255, 210, 70), (x - 3, y - 3), 6)
        # Ojitos enojados
        for ox in (-5, 4):
            pygame.draw.rect(pantalla, NEGRO, (x + ox, y - 1, 3, 4))


# ==========================================================
# SPRITES DEL JEFE (TEICHI o el CUBO provisorio)
# ==========================================================

# Orden de la hoja de sprites de Teichi (assets/personajes/TEICHI/
# teichi_hoja.png, la arma herramientas/generar_teichi_hoja.py)
ORDEN_HOJA = [
    "quieto", "respirar",
    "caminar_1", "caminar_2", "caminar_3", "caminar_4",
    "tirar", "agachado", "brazos_arriba",
    "empujar", "correr_2",
]


def _par(imagen):
    """(mirando a la derecha, mirando a la izquierda)"""
    return imagen, pygame.transform.flip(imagen, True, False)


def sprites_teichi():
    """
    Los cuadros de la hoja de Teichi, agrandados. Todos los casilleros son
    del mismo tamano (apoyados abajo y centrados), asi no "salta" al cambiar
    de cuadro. Tirar y empujar miran a la derecha.
    """

    hoja = pygame.image.load(os.path.join(CARPETA_TEICHI, "teichi_hoja.png")).convert_alpha()
    ancho = hoja.get_width() // len(ORDEN_HOJA)
    alto = hoja.get_height()

    sprites = {}
    for i, nombre in enumerate(ORDEN_HOJA):
        cuadro = hoja.subsurface((i * ancho, 0, ancho, alto)).copy()
        cuadro = pygame.transform.scale(cuadro, (ancho * ESCALA_JEFE, alto * ESCALA_JEFE))
        sprites[nombre] = _par(cuadro)
    return sprites


def _cubo_base(ancho=30, alto=30, ojos="enojado", inclinado=0):
    """Cubo provisorio en pixel art (lo dibuja el juego)."""

    img = pygame.Surface((ancho + 2, alto + 2), pygame.SRCALPHA)
    pygame.draw.rect(img, NEGRO, (0, 0, ancho + 2, alto + 2))
    pygame.draw.rect(img, (150, 40, 50), (1, 1, ancho, alto))
    pygame.draw.rect(img, (190, 70, 80), (1, 1, ancho, 5))
    pygame.draw.rect(img, (190, 70, 80), (1, 1, 5, alto))
    pygame.draw.rect(img, (110, 24, 34), (1, alto - 4, ancho, 5))
    cx, cy = ancho // 2 + 1, alto // 2
    # Ojos
    for lado in (-1, 1):
        ox = cx + lado * 6 - 2
        pygame.draw.rect(img, BLANCO, (ox, cy - 4, 5, 6))
        pygame.draw.rect(img, NEGRO, (ox + (2 if lado < 0 else 1), cy - 2, 2, 3))
        if ojos == "enojado":
            pygame.draw.line(img, NEGRO, (ox - 1, cy - 6 + (0 if lado < 0 else 2)), (ox + 5, cy - 6 + (2 if lado < 0 else 0)), 2)
    # Boca
    pygame.draw.rect(img, NEGRO, (cx - 5, cy + 6, 10, 3))
    pygame.draw.rect(img, BLANCO, (cx - 4, cy + 6, 2, 2))
    pygame.draw.rect(img, BLANCO, (cx + 2, cy + 6, 2, 2))
    if inclinado:
        img = pygame.transform.rotate(img, inclinado)
    return img


def sprites_cubo():
    """Las mismas poses que Teichi, pero para el cubo provisorio."""

    piedra = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.rect(piedra, NEGRO, (0, 0, 10, 10))
    pygame.draw.rect(piedra, (140, 140, 150), (1, 1, 8, 8))

    tirar = pygame.Surface((32, 44), pygame.SRCALPHA)
    tirar.blit(_cubo_base(), (0, 12))
    tirar.blit(piedra, (2, 0))

    cuadros = {
        "quieto": _cubo_base(),
        "respirar": _cubo_base(31, 29),
        # Camina dando saltitos: se aplasta y se estira
        "caminar_1": _cubo_base(32, 27),
        "caminar_2": _cubo_base(),
        "caminar_3": _cubo_base(28, 32),
        "caminar_4": _cubo_base(),
        "tirar": tirar,
        "agachado": _cubo_base(40, 20),
        "brazos_arriba": _cubo_base(26, 38),
        "empujar": _cubo_base(inclinado=-14),
        "correr_2": _cubo_base(inclinado=-6),
    }

    escala = ESCALA_JEFE + 1
    sprites = {}
    for pose, img in cuadros.items():
        img = pygame.transform.scale(img, (img.get_width() * escala, img.get_height() * escala))
        sprites[pose] = _par(img)
    return sprites


# ==========================================================
# PIEDRAS Y ONDAS
# ==========================================================

def _imagen_piedra(cubo=False):
    img = pygame.Surface((12, 11), pygame.SRCALPHA)
    if cubo:
        pygame.draw.rect(img, NEGRO, (0, 0, 11, 11))
        pygame.draw.rect(img, (140, 140, 150), (1, 1, 9, 9))
        pygame.draw.rect(img, (180, 180, 190), (1, 1, 9, 2))
    else:
        pygame.draw.ellipse(img, NEGRO, (0, 0, 12, 11))
        pygame.draw.ellipse(img, (128, 126, 130), (1, 1, 10, 9))
        pygame.draw.rect(img, (170, 168, 172), (3, 2, 4, 2))
        pygame.draw.rect(img, (96, 94, 98), (6, 6, 3, 2))
    return pygame.transform.scale(img, (36, 33))


class Piedra:
    """
    vuela  -> la tiro el jefe: si te pega perdes una vida
    piso   -> quedo en el piso un rato: se agarra con E
    llevada-> la tenes arriba de la cabeza
    lanzada-> la tiraste: si le pega al jefe, lo marea
    """

    VIDA_EN_PISO = 5.0

    def __init__(self, imagen, x, y, vx, vy):
        self.imagen = imagen
        self.x, self.y, self.vx, self.vy = float(x), float(y), vx, vy
        self.estado = "vuela"
        self.t_piso = 0.0
        self.giro = 0.0
        self.terminada = False

    @property
    def rect(self):
        r = self.imagen.get_rect()
        r.center = (int(self.x), int(self.y))
        return r.inflate(-6, -6)

    def actualizar(self, dt, terreno):

        if self.estado in ("vuela", "lanzada"):
            self.vy += 1800 * dt
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.giro += 600 * dt * (1 if self.vx >= 0 else -1)
            if self.y + 16 >= PISO_Y and self.vy > 0:
                if terreno.hay_piso(self.x) and self.y < PISO_Y + 20:
                    self.y = PISO_Y - 16
                    if self.estado == "vuela":
                        self.estado = "piso"
                        self.t_piso = self.VIDA_EN_PISO
                    else:
                        self.terminada = True
                elif self.y > PISO_Y + 60:
                    self.terminada = True
            if self.x < -60 or self.x > terreno.ancho + 60:
                self.terminada = True

        elif self.estado == "piso":
            self.t_piso -= dt
            if self.t_piso <= 0:
                self.terminada = True

    def dibujar(self, pantalla, camara_x):
        if self.estado == "piso" and self.t_piso < 1.5 and int(self.t_piso * 10) % 2:
            return
        # Las que caen del techo (lluvia de piedras) marcan donde van a caer
        if self.estado == "vuela" and self.vx == 0:
            ancho = int(max(10, min(46, 46 - (PISO_Y - self.y) / 14)))
            sombra = pygame.Surface((ancho, 10), pygame.SRCALPHA)
            pygame.draw.ellipse(sombra, (0, 0, 0, 120), sombra.get_rect())
            pantalla.blit(sombra, sombra.get_rect(center=(int(self.x - camara_x), PISO_PANTALLA)))
        img = self.imagen
        if self.estado in ("vuela", "lanzada"):
            img = pygame.transform.rotate(img, self.giro)
        pantalla.blit(img, img.get_rect(center=(int(self.x - camara_x), int(self.y - CAMARA_Y))))


class Onda:
    """Onda del golpe al piso: corre por el piso, hay que saltarla."""

    def __init__(self, x, direccion, velocidad=380):
        self.x = float(x)
        self.dir = direccion
        self.vel = velocidad
        self.terminada = False
        self.t = 0.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x) - 22, PISO_Y - 30, 44, 30)

    def actualizar(self, dt, terreno):
        self.t += dt
        self.x += self.dir * self.vel * dt
        if not terreno.hay_piso(self.x) or self.x < 0 or self.x > terreno.ancho:
            self.terminada = True

    def dibujar(self, pantalla, camara_x):
        x = int(self.x - camara_x)
        y = PISO_PANTALLA
        for k in range(3):
            alto = 30 - k * 8 + int(math.sin(self.t * 30 + k) * 3)
            ancho = 16 + k * 10
            color = [(255, 240, 200), (255, 190, 90), (200, 120, 60)][k]
            pygame.draw.ellipse(pantalla, color, (x - ancho // 2 - self.dir * k * 10, y - alto, ancho, alto * 2), 0 if k == 0 else 3)
        for k in range(4):
            px = x - self.dir * (10 + k * 9)
            pygame.draw.rect(pantalla, (150, 140, 130), (px, y - 6 - (k * 5) % 14, 5, 5))


# ==========================================================
# EL JEFE
# ==========================================================

class Jefe:
    """
    El jefe tiene tres FASES segun la vida que le queda:

        FASE 1  tira piedras (de a una) y embiste
        FASE 2  ademas golpea el piso (ondas) y tira de a dos piedras
        FASE 3  ademas hace llover piedras del techo, tira de a tres, es mas
                rapido y llama ayudantes (gagambas) al empezar la fase

    Cuando cambia de fase avisa (self.fase_nueva) para que la pelea muestre
    el cartel y aparezcan los ayudantes.
    """

    def __init__(self, nombre, sprites, vida, arena, imagen_piedra, peligro="lava", frases_fase=None):

        self.nombre = nombre
        self.sprites = sprites
        self.vida = vida
        self.vida_max = vida
        self.arena = arena                   # (x_min, x_max) donde se mueve
        self.imagen_piedra = imagen_piedra
        self.peligro = peligro
        self.frases_fase = frases_fase or {}

        self.x = float(arena[1] - 300)
        self.y = float(PISO_Y)
        self.vx = 0.0
        self.vy = 0.0
        self.mira_der = False
        self.estado = "pausa"
        self.t = 0.0
        self.reloj = 0.0                     # para las animaciones
        self.t_suelta = -9.0                 # cuando solto la ultima piedra
        self.duracion = 1.2
        self.giro = 0.0
        self.piedras_por_tirar = 0
        self.ondas_nuevas = []
        self.piedras_nuevas = []
        self.temblor = 0.0
        self.textos = []          # (texto, x, y, t)
        self.fase_nueva = None    # numero de fase recien empezada
        self.y_techo = CAMARA_Y - 40

    # ---------- fases ----------

    def fase(self):
        parte = self.vida / self.vida_max
        if parte > 2 / 3:
            return 1
        if parte > 1 / 3:
            return 2
        return 3

    # ---------- apariencia ----------

    def pose(self):
        e = self.estado
        r = self.reloj
        if e == "pausa":
            return "caminar_%d" % (int(r * 8) % 4 + 1)
        if e == "tirar":
            return "empujar" if r - self.t_suelta < 0.25 else "tirar"
        if e == "golpe_preparar":
            return "agachado" if self.t < 0.18 else "brazos_arriba"
        if e in ("golpe_salto", "lluvia_preparar", "lluvia"):
            return "brazos_arriba"
        if e in ("embestir_preparar", "golpe_caida"):
            return "agachado"
        if e == "embestir":
            return "empujar" if int(r * 10) % 2 == 0 else "correr_2"
        if e == "mareado":
            return "respirar" if int(r * 3) % 2 else "quieto"
        return "quieto"

    def imagen(self):
        der, izq = self.sprites[self.pose()]
        return der if self.mira_der else izq

    def _caja_en_pantalla(self, img):
        """Rectangulo del dibujo (sin lo transparente) donde se dibuja."""
        caja = img.get_bounding_rect()
        return caja.move(int(self.x) - img.get_width() // 2, int(self.y) - img.get_height())

    def rect(self):
        caja = self._caja_en_pantalla(self.imagen())
        caja = caja.inflate(-int(caja.width * 0.25), -int(caja.height * 0.12))
        caja.bottom = int(self.y)
        if self.estado == "embestir":
            # Embistiendo va agachado: se lo puede saltar por arriba
            caja.height = int(caja.height * 0.55)
            caja.bottom = int(self.y)
        return caja

    @property
    def peligroso(self):
        # Recien golpeado (o volviendo al medio despues del golpe) no hace dano
        return self.estado not in ("mareado", "herido", "agarrado", "volando", "derrotado", "quemado", "volver")

    @property
    def mareado(self):
        return self.estado == "mareado"

    # ---------- maquina de estados ----------

    def _cambiar(self, estado, duracion=0.0):
        self.estado = estado
        self.t = 0.0
        self.duracion = duracion

    def furia(self):
        """0 con toda la vida, 1 con una sola."""
        return 1 - (self.vida - 1) / max(1, self.vida_max - 1)

    def marear(self, duracion=2.6):
        if self.estado in ("herido", "derrotado", "agarrado", "volando", "quemado"):
            return
        self._cambiar("mareado", duracion)
        self.vx = 0
        self.vy = 0
        self.y = PISO_Y

    def pegar(self, texto="¡AUCH!"):
        """Le saca una vida (y si cambia de fase, lo avisa)."""
        if self.estado in ("herido", "derrotado"):
            return
        fase_antes = self.fase()
        self.vida -= 1
        sonidos.reproducir("aplastar")
        self.textos.append([texto, self.x, self.y - 160, 0.0])
        if self.vida <= 0:
            self._cambiar("derrotado", 2.5)
            self.vx, self.vy = 0, -600
            return
        self._cambiar("herido", 1.1)
        if self.fase() != fase_antes:
            self.fase_nueva = self.fase()

    def actualizar(self, dt, jugador, terreno):

        self.t += dt
        self.reloj += dt
        self.temblor = max(0.0, self.temblor - dt)
        self.textos = [[tx, x, y - 50 * dt, t + dt] for tx, x, y, t in self.textos if t < 1.2]
        e = self.estado
        apurado = 1 + 0.25 * (self.fase() - 1) + 0.2 * self.furia()

        if e == "pausa":
            # Camina hacia el jugador (mas rapido si esta lejos)
            self.mira_der = jugador.rect.centerx > self.x
            lejos = abs(jugador.rect.centerx - self.x) > 500
            velocidad = (190 if lejos else 90) * apurado
            self.x += (1 if self.mira_der else -1) * velocidad * dt
            self.x = max(self.arena[0], min(self.arena[1], self.x))
            if self.t >= self.duracion:
                self._elegir_ataque(jugador)

        elif e == "tirar":
            self.mira_der = jugador.rect.centerx > self.x
            if self.t >= 0.55 / apurado and self.piedras_por_tirar > 0:
                self._tirar_piedra(jugador)
                self.piedras_por_tirar -= 1
                self.t = 0.2
            elif self.t >= 0.9 and self.piedras_por_tirar <= 0:
                self._cambiar("pausa", random.uniform(0.6, 1.1) / apurado)

        elif e == "golpe_preparar":
            if self.t >= 0.5 / apurado:
                self._cambiar("golpe_salto")
                self.vy = -820
                # Salta hacia el jugador (como mucho 650 por segundo)
                self.vx = max(-650, min(650, (jugador.rect.centerx - self.x) / 0.68))

        elif e == "golpe_salto":
            self.vy += 2400 * dt
            self.x += self.vx * dt
            self.x = max(self.arena[0], min(self.arena[1], self.x))
            self.y += self.vy * dt
            if self.y >= PISO_Y and self.vy > 0:
                self.y = PISO_Y
                self.vx = 0
                self.temblor = 0.35
                sonidos.reproducir("golpe")
                velocidad = 360 + 140 * self.furia()
                self.ondas_nuevas += [Onda(self.x - 30, -1, velocidad), Onda(self.x + 30, 1, velocidad)]
                self._cambiar("golpe_caida", 0.45)

        elif e == "golpe_caida":
            if self.t >= self.duracion:
                self._cambiar("pausa", random.uniform(0.5, 1.0) / apurado)

        elif e == "lluvia_preparar":
            if self.t >= 0.9 / apurado:
                self._cambiar("lluvia", 2.6)
                self.temblor = 0.3
                sonidos.reproducir("golpe")

        elif e == "lluvia":
            # Caen piedras del techo cerca del jugador (hay sombra en el piso)
            if int((self.t - dt) / 0.32) != int(self.t / 0.32):
                x = jugador.rect.centerx + random.uniform(-280, 280)
                x = max(self.arena[0] - 40, min(self.arena[1] + 40, x))
                self.piedras_nuevas.append(Piedra(self.imagen_piedra, x, self.y_techo, 0, 0))
            if self.t >= self.duracion:
                self._cambiar("pausa", 0.8 / apurado)

        elif e == "embestir_preparar":
            self.mira_der = jugador.rect.centerx > self.x
            if self.t >= 0.8 / apurado:
                self._cambiar("embestir")
                self.vx = (1 if self.mira_der else -1) * (520 + 160 * self.furia())

        elif e == "embestir":
            self.x += self.vx * dt
            if self.x <= self.arena[0] or self.x >= self.arena[1]:
                self.x = max(self.arena[0], min(self.arena[1], self.x))
                self.vx = 0
                self.temblor = 0.3
                sonidos.reproducir("golpe")
                self.marear(2.6 - 0.6 * self.furia())

        elif e == "mareado":
            if self.t >= self.duracion:
                self._cambiar("pausa", 0.4)

        elif e == "herido":
            if self.t >= self.duracion:
                # Salta al medio y sigue
                self._cambiar("volver")
                centro = (self.arena[0] + self.arena[1]) / 2
                self.vx = max(-900, min(900, (centro - self.x) / 0.8))
                self.vy = -900

        elif e == "volver":
            self.vy += 2250 * dt
            self.x += self.vx * dt
            self.y += self.vy * dt
            if self.y >= PISO_Y and self.vy > 0:
                self.y = PISO_Y
                self.vx = 0
                self.temblor = 0.25
                self._cambiar("pausa", 0.5)

        elif e == "quemado":
            # Salio de la lava (o de la bomba) gritando: vuelve al medio
            self.vy += 2250 * dt
            self.x += self.vx * dt
            self.y += self.vy * dt
            if self.y >= PISO_Y and self.vy > 0 and terreno.hay_piso(self.x):
                self.y = PISO_Y
                self.vx = 0
                self.pegar("¡QUEMA!" if self.peligro == "lava" else "¡BOOM!")

        elif e == "volando":
            self.vy += 2000 * dt
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.giro += 720 * dt * (1 if self.vx > 0 else -1)
            # Paredes de la sala
            if self.x < 30 or self.x > terreno.ancho - 30:
                self.x = max(30, min(terreno.ancho - 30, self.x))
                self.vx = 0
            en_peligro = self._en_peligro(terreno)
            if self.y >= PISO_Y and self.vy > 0:
                if en_peligro:
                    self._caer_en_peligro(terreno)
                else:
                    self.y = PISO_Y
                    self.vx = 0
                    self.giro = 0
                    self.temblor = 0.2
                    sonidos.reproducir("golpe")
                    self.marear(1.4)

        elif e == "derrotado":
            self.vy += 1600 * dt
            self.y = min(PISO_Y, self.y + self.vy * dt)

    def _en_peligro(self, terreno):
        if self.peligro == "lava":
            return not terreno.hay_piso(self.x)
        return self.x < self.arena[0] - 40 or self.x > self.arena[1] + 40

    def _caer_en_peligro(self, terreno):
        self.giro = 0
        sonidos.reproducir("golpe")
        self.temblor = 0.4
        centro = (self.arena[0] + self.arena[1]) / 2
        if self.peligro == "lava":
            self.y = PISO_Y + 10
        else:
            self.y = PISO_Y
        # Sale despedido hacia el medio
        self._cambiar("quemado")
        self.vx = max(-900, min(900, (centro - self.x) / 0.9))
        self.vy = -1150

    def _elegir_ataque(self, jugador):
        distancia = abs(jugador.rect.centerx - self.x)
        fase = self.fase()

        if distancia > 280:
            opciones = [("tirar", 45), ("embestir", 35)]
        else:
            opciones = [("tirar", 25), ("embestir", 45)]
        if fase >= 2:
            opciones.append(("golpe", 30 if distancia <= 280 else 20))
        if fase >= 3:
            opciones.append(("lluvia", 30))

        total = sum(p for _, p in opciones)
        r = random.uniform(0, total)
        for nombre, p in opciones:
            r -= p
            if r <= 0:
                break
        if nombre == "tirar":
            self.piedras_por_tirar = fase
            self._cambiar("tirar")
        elif nombre == "golpe":
            self._cambiar("golpe_preparar")
        elif nombre == "lluvia":
            self._cambiar("lluvia_preparar")
            self.textos.append(["¡LLUVIA DE PIEDRAS!", self.x, self.y - 180, 0.0])
        else:
            self._cambiar("embestir_preparar")

    def _tirar_piedra(self, jugador):
        caja = self._caja_en_pantalla(self.imagen())
        x0 = caja.centerx + (30 if self.mira_der else -30)
        y0 = caja.top + 20
        destino = jugador.rect.centerx + random.uniform(-60, 60)
        # Mas lejos, mas tiempo en el aire (asi no sale disparada)
        tiempo = max(0.75, min(1.5, abs(destino - x0) / 650)) * random.uniform(0.95, 1.1)
        vx = (destino - x0) / tiempo
        vy = ((PISO_Y - 16) - y0 - 0.5 * 1800 * tiempo * tiempo) / tiempo
        self.piedras_nuevas.append(Piedra(self.imagen_piedra, x0, y0, vx, vy))
        self.t_suelta = self.reloj
        sonidos.reproducir("salto")

    # ---------- dibujo ----------

    def dibujar(self, pantalla, camara_x, t, arriba_de=None):

        img = self.imagen()

        if self.estado == "agarrado" and arriba_de is not None:
            # Arriba de la cabeza del jugador, dado vuelta
            img = pygame.transform.rotate(pygame.transform.scale(img, (int(img.get_width() * 0.7), int(img.get_height() * 0.7))), 180 + math.sin(t * 12) * 10)
            rect = img.get_rect(midbottom=(arriba_de.centerx - camara_x, arriba_de.top - CAMARA_Y + 30))
            pantalla.blit(img, rect)
            return

        if self.estado == "mareado":
            # Se tambalea para los costados
            img = pygame.transform.rotate(img, math.sin(t * 6) * 7)

        if self.estado == "volando":
            img = pygame.transform.rotate(img, self.giro)

        if self.estado in ("herido", "quemado") and int(self.t * 16) % 2 == 0:
            img = img.copy()
            img.fill((255, 60, 40, 0), special_flags=pygame.BLEND_RGBA_MAX)

        if self.estado == "derrotado" and int(self.t * 10) % 2 == 0:
            return

        x = int(self.x - camara_x)
        y = int(self.y - CAMARA_Y)

        caja = img.get_bounding_rect()

        if self.estado != "volando" and self.y <= PISO_Y + 1:
            sombra = pygame.Surface((max(10, caja.width), 16), pygame.SRCALPHA)
            pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
            pantalla.blit(sombra, sombra.get_rect(center=(x, PISO_PANTALLA)))

        # El casillero va centrado y apoyado abajo (todos los cuadros iguales)
        arriba_img = y - img.get_height()
        pantalla.blit(img, (x - img.get_width() // 2, arriba_img))
        arriba = arriba_img + caja.top

        # "!" antes de embestir
        if self.estado == "embestir_preparar":
            arriba_signo = arriba - 20
            pygame.draw.rect(pantalla, NEGRO, (x - 7, arriba_signo - 36, 14, 28))
            pygame.draw.rect(pantalla, AMARILLO, (x - 5, arriba_signo - 34, 10, 24))
            pygame.draw.rect(pantalla, NEGRO, (x - 7, arriba_signo - 4, 14, 12))
            pygame.draw.rect(pantalla, AMARILLO, (x - 5, arriba_signo - 2, 10, 8))

        # Estrellitas de mareado
        if self.estado == "mareado":
            for k in range(4):
                a = t * 5 + k * math.pi / 2
                sx = x + int(math.cos(a) * 34)
                sy = arriba - 4 + int(math.sin(a) * 9)
                pygame.draw.rect(pantalla, AMARILLO, (sx - 1, sy - 5, 3, 11))
                pygame.draw.rect(pantalla, AMARILLO, (sx - 5, sy - 1, 11, 3))


# ==========================================================
# HUD
# ==========================================================

def _texto_sombra(pantalla, fuente, texto, color, **pos):
    sombra = fuente.render(texto, True, NEGRO)
    imagen = fuente.render(texto, True, color)
    rect = imagen.get_rect(**pos)
    pantalla.blit(sombra, rect.move(2, 2))
    pantalla.blit(imagen, rect)
    return rect


def dibujar_hud(pantalla, fuente, cabeza, vidas, puntos, nivel):

    x = 10
    if cabeza is not None:
        rect = cabeza.get_rect(topleft=(10, 10))
        pantalla.blit(cabeza, rect)
        x = rect.right + 12
        centro = rect.centery
    else:
        centro = 24
    _texto_sombra(pantalla, fuente, "VIDAS: " + str(vidas), BLANCO, midleft=(x, centro))
    _texto_sombra(pantalla, fuente, "PUNTOS: " + str(puntos), BLANCO, topright=(ANCHO - 12, 12))
    _texto_sombra(pantalla, fuente, "NIVEL " + str(nivel), BLANCO, midtop=(ANCHO // 2, 12))


def dibujar_vida_jefe(pantalla, fuente_chica, jefe):

    ancho = 300
    x = ANCHO // 2 - ancho // 2
    y = 74          # abajo del "NIVEL 30"
    _texto_sombra(pantalla, fuente_chica, jefe.nombre, (255, 200, 200), midbottom=(ANCHO // 2, y - 2))
    pygame.draw.rect(pantalla, NEGRO, (x - 4, y - 4, ancho + 8, 22))
    pygame.draw.rect(pantalla, (70, 20, 20), (x, y, ancho, 14))
    lleno = int(ancho * max(0, jefe.vida) / jefe.vida_max)
    pygame.draw.rect(pantalla, (230, 40, 40), (x, y, lleno, 14))
    pygame.draw.rect(pantalla, (255, 120, 110), (x, y, lleno, 4))
    for k in range(1, jefe.vida_max):
        sx = x + ancho * k // jefe.vida_max
        pygame.draw.line(pantalla, NEGRO, (sx, y), (sx, y + 13), 2)


def cartel(pantalla, fuente, texto, alfa=255, y=ALTO // 2 - 40, color=AMARILLO):
    imagen = fuente.render(texto, True, color)
    sombra = fuente.render(texto, True, NEGRO)
    if alfa < 255:
        imagen = imagen.copy()
        sombra = sombra.copy()
        imagen.set_alpha(alfa)
        sombra.set_alpha(alfa)
    rect = imagen.get_rect(center=(ANCHO // 2, y))
    for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3)):
        pantalla.blit(sombra, rect.move(dx, dy))
    pantalla.blit(imagen, rect)


# ==========================================================
# DIALOGO (Teichi antes y despues de la pelea)
# ==========================================================

def dialogo(pantalla, reloj, fuente_media, lineas, cabezas, dibujar_fondo):
    """
    lineas: [(nombre, texto)], cabezas: {nombre: (imagen, escala, color)}.
    dibujar_fondo(t) dibuja lo de atras. ENTER pasa, ESC saltea.
    """

    retratos = {n: Retrato(n, img) for n, (img, _, _) in cabezas.items()}
    partes = [(q, _partir_en_lineas(fuente_media, txt, TEXTO_ANCHO)) for q, txt in lineas]
    linea, letras, t = 0, 0.0, 0.0
    retratos[partes[0][0]].mandar_a(RETRATO_GRANDE.centerx, CUADRO.bottom - 14, cabezas[partes[0][0]][1], gris=False)

    while True:
        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt
        avanzar = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    sonidos.detener("teclado")
                    return
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                    avanzar = True
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                avanzar = True

        quien, texto = partes[linea]
        total = sum(len(p) for p in texto)
        letras = min(total, letras + 38 * dt)
        if avanzar:
            if letras < total:
                letras = total
            elif linea + 1 < len(partes):
                sonidos.reproducir("boton")
                linea += 1
                letras = 0.0
                nuevo = partes[linea][0]
                retratos[nuevo].mandar_a(RETRATO_GRANDE.centerx, CUADRO.bottom - 14, cabezas[nuevo][1], gris=False)
                continue
            else:
                sonidos.reproducir("boton")
                sonidos.detener("teclado")
                return

        escribiendo = letras < total
        if escribiendo:
            sonidos.reproducir_en_bucle("teclado")
        else:
            sonidos.detener("teclado")

        for r in retratos.values():
            r.actualizar(dt)

        dibujar_fondo(t)
        velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        velo.fill((0, 0, 0, 80))
        pantalla.blit(velo, (0, 0))
        _dibujar_cuadro(pantalla, fuente_media, quien, cabezas[quien][2])
        retratos[quien].dibujar(pantalla, int(abs(math.sin(t / 0.32 * math.pi)) * 3) if escribiendo else 0)
        restantes = int(letras)
        for k, parte in enumerate(texto):
            if restantes <= 0:
                break
            _dibujar_texto_con_sombra(pantalla, fuente_media, parte[:restantes], BLANCO, (TEXTO_X, TEXTO_Y + k * (fuente_media.get_height() - 4)))
            restantes -= len(parte)
        if not escribiendo:
            _dibujar_flechita(pantalla, t)
        pygame.display.flip()


# ==========================================================
# ENEMIGOS COMUNES (gagambas y hinchas) EN EL CASTILLO
# ==========================================================

def resolver_gagambas(jugador, enemigos, bottom_anterior):
    """Igual que en juego.py: pisarlos los aplasta, tocarlos te mata."""

    for enemigo in enemigos:
        if enemigo.aplastado or not jugador.rect.colliderect(enemigo.rect):
            continue
        if (
            jugador.vel_y > 0
            and bottom_anterior <= enemigo.rect.top + 18
            and enemigo.rect.top - jugador.rect.bottom <= 18
        ):
            enemigo.aplastar()
            sonidos.reproducir("aplastar")
            jugador.rect.bottom = enemigo.rect.top
            jugador.vel_y = J.SALTO_FUERZA * 0.55
            jugador.en_suelo = False
            return False
        if J.colision_por_pixeles(jugador, enemigo):
            return True
    return False


# ==========================================================
# NIVEL 30: EL CASTILLO
# ==========================================================

ANCHO_CASTILLO = 6200
X_PUERTA = 5920          # la puerta de la sala de Lord Teichi

# Tramos de piso (entre tramo y tramo hay lava)
PISOS_CASTILLO = [
    (0, 700), (830, 1300), (1500, 2100), (2420, 2900), (3020, 3500),
    (4000, 4600), (4730, 5200), (5360, ANCHO_CASTILLO),
]

# Plataformas sobre la lava y arriba de los pisos (x0, x1, y del mundo)
PLATAFORMAS_CASTILLO = [
    (1350, 1450, 700),
    (2150, 2250, 700), (2290, 2390, 640),
    (2560, 2760, 650),
    (3560, 3660, 700), (3720, 3820, 630), (3880, 3970, 700),
    (4200, 4380, 660),
    (5230, 5330, 690),
]

# Gagambas: (x, piso_y, rango)
GAGAMBAS_CASTILLO = [
    (1000, PISO_Y, 120), (1180, PISO_Y, 80), (1650, PISO_Y, 120), (1900, PISO_Y, 100),
    (2500, PISO_Y, 60), (2820, PISO_Y, 50), (3150, PISO_Y, 100), (3380, PISO_Y, 80),
    (4100, PISO_Y, 80), (4300, 660, 50), (4480, PISO_Y, 90), (4850, PISO_Y, 100),
    (5080, PISO_Y, 80), (5500, PISO_Y, 120), (5700, PISO_Y, 100),
]

# Hinchas que tiran botellas: (x, piso_y, rango)
HINCHAS_CASTILLO = [
    (1780, PISO_Y, 90), (2660, 650, 60), (3300, PISO_Y, 90), (4520, PISO_Y, 70),
    (4950, PISO_Y, 90), (5600, PISO_Y, 90),
]


# En el castillo Di Lolio (el hincha) tarda mas en cargar la lata
CARGA_LENTA_CASTILLO = 2.5

# Y los gagambas caminan mas despacio (en los otros niveles: 120)
VELOCIDAD_GAGAMBA_CASTILLO = 60


def _crear_enemigos_castillo(sprites):
    # Los gagambas del castillo son mas lentos (60 en vez de 120)
    enemigos = [J.Enemigo(x, sprites["enemigo"], rango, VELOCIDAD_GAGAMBA_CASTILLO, y) for x, y, rango in GAGAMBAS_CASTILLO]
    lanzadores = [J.HinchaLanzador(x, J.cargar_sprites_lanzador(), y, rango) for x, y, rango in HINCHAS_CASTILLO]
    for lanzador in lanzadores:
        lanzador.factor_carga = CARGA_LENTA_CASTILLO
    return enemigos, lanzadores


def _puerta(pantalla, x, fuente_chica, t):
    """Puerta grande de la sala del jefe (x de pantalla, centro)."""

    arriba = PISO_PANTALLA - 220
    pygame.draw.rect(pantalla, (30, 26, 34), (x - 90, arriba - 20, 180, 240))
    pygame.draw.ellipse(pantalla, (30, 26, 34), (x - 90, arriba - 80, 180, 130))
    pygame.draw.rect(pantalla, (90, 50, 24), (x - 74, arriba, 148, 220))
    pygame.draw.ellipse(pantalla, (90, 50, 24), (x - 74, arriba - 60, 148, 110))
    for k in range(-60, 70, 24):
        pygame.draw.line(pantalla, (60, 32, 14), (x + k, arriba - 30), (x + k, PISO_PANTALLA), 3)
    pygame.draw.circle(pantalla, (220, 180, 60), (x + 40, arriba + 120), 6)
    # Cartel
    texto = fuente_chica.render("SALA DE LORD TEICHI", True, (255, 220, 120))
    rect = texto.get_rect(midbottom=(x, arriba - 70))
    pygame.draw.rect(pantalla, NEGRO, rect.inflate(16, 10))
    pygame.draw.rect(pantalla, (200, 160, 40), rect.inflate(16, 10), 2)
    pantalla.blit(texto, rect)
    # Brillo que llama
    if int(t * 2) % 2 == 0:
        flecha = fuente_chica.render("ENTRA", True, BLANCO)
        pantalla.blit(flecha, flecha.get_rect(midbottom=(x, arriba - 100)))


def _castillo(pantalla, reloj, sprites, fuentes, cabeza, estado):
    """
    El castillo hasta la puerta. Devuelve "puerta", "menu" o "murio".
    estado: dict con vidas, puntos y nivel.
    """

    fuente_grande, fuente_media, fuente_chica = fuentes

    # El castillo usa una cancion de noche
    # La cancion del castillo se elige una vez: al morir se pausa y al
    # volver sigue desde donde quedo
    if "cancion_castillo" not in estado:
        estado["cancion_castillo"] = musica.cancion_de_nivel(30)
    musica.reproducir_cancion(estado["cancion_castillo"])

    terreno = TerrenoSimple(ANCHO_CASTILLO, PISOS_CASTILLO, PLATAFORMAS_CASTILLO, inicio_x=100)
    fondo = FondoCastillo(
        terreno, estado["cuadros"], fuente_media,
        sin_cuadros=(X_PUERTA - 60, X_PUERTA + 200)
    )
    jugador = J.Jugador(sprites, terreno)
    enemigos, lanzadores = _crear_enemigos_castillo(sprites)
    botellas = []
    bolas = []
    for x0, x1 in terreno.pozos():
        cuantas = 1 + (x1 - x0) // 220
        for k in range(cuantas):
            bolas.append(BolaLava(x0 + (x1 - x0) * (k + 1) / (cuantas + 1), len(bolas)))

    t = 0.0

    while True:

        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "menu"
            if evento.type == pygame.KEYDOWN and evento.key == cheats.TECLA:
                accion = _trucos(pantalla, reloj, estado)
                if accion is not None:
                    return accion

        teclas = pygame.key.get_pressed()
        bottom_anterior = jugador.rect.bottom
        jugador.mover(teclas, dt)
        jugador.actualizar_parpadeo(dt)
        fondo.actualizar(dt)

        for enemigo in enemigos:
            enemigo.mover(dt)
            enemigo.actualizar(dt)

        for lanzador in lanzadores:
            nueva = lanzador.actualizar(dt, jugador)
            if nueva is not None:
                botellas.append(nueva)

        for botella in botellas:
            botella.mover(dt, terreno)
        botellas = [b for b in botellas if not b.terminada and not b.fuera_del_nivel()]

        for bola in bolas:
            bola.actualizar(dt)

        camara_x = max(0, min(jugador.rect.centerx - ANCHO // 2, terreno.ancho - ANCHO))

        # --- muerte ---
        murio = resolver_gagambas(jugador, enemigos, bottom_anterior)
        murio = murio or J.resolver_lanzadores(jugador, lanzadores, bottom_anterior)
        murio = murio or J.resolver_botellas(jugador, botellas)
        murio = murio or any(b.activa and jugador.rect.colliderect(b.rect) for b in bolas)
        en_lava = jugador.rect.top > PISO_Y - 10
        murio = murio or en_lava

        enemigos = [e for e in enemigos if not (e.aplastado and e.tiempo_aplastado <= 0)]
        lanzadores = [l for l in lanzadores if not (l.aplastado and l.tiempo_aplastado <= 0)]

        if murio:
            musica.pausar()
            if en_lava:
                sonidos.reproducir("golpe")
            J.animacion_muerte(pantalla, reloj, jugador, sprites, camara_x, fondo, CAMARA_Y)
            return "murio"

        # --- la puerta ---
        if jugador.rect.centerx >= X_PUERTA:
            return "puerta"

        # --- dibujar ---
        fondo.dibujar(pantalla, camara_x)
        _puerta(pantalla, X_PUERTA - camara_x + 60, fuente_chica, t)

        for enemigo in enemigos:
            enemigo.dibujar(pantalla, camara_x, CAMARA_Y)
        for lanzador in lanzadores:
            lanzador.dibujar(pantalla, camara_x, CAMARA_Y)
        for botella in botellas:
            botella.dibujar(pantalla, camara_x, CAMARA_Y)

        jugador.dibujar(pantalla, camara_x, CAMARA_Y)

        for bola in bolas:
            bola.dibujar(pantalla, camara_x, t)

        dibujar_hud(pantalla, fuente_media, cabeza, estado["vidas"], estado["puntos"], estado["nivel"])

        if t < 3.5:
            alfa = int(255 * min(1.0, t / 0.4, (3.5 - t) / 0.6))
            cartel(pantalla, fuente_media, "EL CASTILLO DE LORD TEICHI", alfa, 150)
            cartel(pantalla, fuente_chica, "BURZACO - CUIDADO CON LA LAVA", alfa, 190, BLANCO)

        pygame.display.flip()


# ==========================================================
# PELEA CONTRA EL JEFE
# ==========================================================

# La arena de los jefes: tres pantallas de ancho, con plataformas para
# esquivar. La camara sigue al jugador.
ANCHO_ARENA = 2400

# Plataformas de la arena (x0, x1, y del mundo): se suben de un salto
PLATAFORMAS_ARENA = [
    (520, 740, 660),
    (1090, 1310, 650),
    (1660, 1880, 660),
]

# Donde esta la jaula de Mxroy en la sala de Teichi (x del mundo)
X_JAULA = ANCHO_ARENA - 330

# Vida de cada jefe (se divide en 3 fases)
VIDA_TEICHI = 6
VIDA_CUBO = 3

# Lo que grita cada jefe al empezar la fase 2 y la 3
FRASES_TEICHI = {
    2: "¡Ahora sí me enojaron, Broskis!",
    3: "¡Gagambas! ¡A ELLOS!",
}
FRASES_CUBO = {
    2: "¡CUBO ENOJADO!",
    3: "¡CUBO FURIOSO!",
}

# El jefe del nivel 15: un robot copia del personaje del jugador
FRASES_ROBOT = {
    2: "BIP BOP. ¡SISTEMAS AL 200%!",
    3: "¡MODO DESTRUCCION ACTIVADO!",
}

# Gagambas que llama el jefe al empezar la fase 3
AYUDANTES_FASE_3 = 3


def _robot(estado, sprites):
    """Los dibujos del robot (se arman una vez por nivel)."""
    if "robot" not in estado:
        estado["robot"] = sprites_robot(sprites)
    return estado["robot"]


def _armar_pelea(nivel, estado, sprites=None):
    """Arena, fondo y jefe de cada nivel."""

    if nivel == 30:
        # Sala de Lord Teichi: lava en los dos costados
        terreno = TerrenoSimple(ANCHO_ARENA, [(170, ANCHO_ARENA - 170)], PLATAFORMAS_ARENA, inicio_x=260)
        fondo = FondoCastillo(terreno, estado["cuadros"], None, separacion_cuadros=60, sala=True, semilla=31)
        jefe = Jefe("LORD TEICHI", sprites_teichi(), VIDA_TEICHI, (250, ANCHO_ARENA - 250),
                    _imagen_piedra(), "lava", FRASES_TEICHI)
    else:
        # La Bombonera: bombas en los costados
        terreno = TerrenoSimple(ANCHO_ARENA, [(0, ANCHO_ARENA)], PLATAFORMAS_ARENA, inicio_x=260)
        fondo = FondoBombonera(terreno)
        # El robot copia del personaje del jugador (del tamano del cubo)
        jefe = Jefe(nombre_robot(sprites), _robot(estado, sprites), VIDA_CUBO, (250, ANCHO_ARENA - 250),
                    _imagen_piedra(cubo=True), "bombas", FRASES_ROBOT)
    return terreno, fondo, jefe


# Bombas de la Bombonera (x del mundo) y hasta donde explotan
BOMBAS = (70, ANCHO_ARENA - 70)
ZONA_BOMBAS = 130


def _dibujar_bombas(pantalla, camara_x, t):
    """Bombas con mecha en los costados (Bombonera)."""
    for xb in BOMBAS:
        x = int(xb - camara_x)
        if x < -60 or x > ANCHO + 60:
            continue
        y = PISO_PANTALLA - 30
        pygame.draw.circle(pantalla, NEGRO, (x, y), 30)
        pygame.draw.circle(pantalla, (60, 60, 70), (x - 10, y - 10), 8)
        for k in range(8):
            a = k * math.pi / 4
            pygame.draw.line(pantalla, (40, 40, 40), (x + math.cos(a) * 28, y + math.sin(a) * 28), (x + math.cos(a) * 40, y + math.sin(a) * 40), 4)
        pygame.draw.line(pantalla, (180, 150, 100), (x, y - 30), (x + 8, y - 44), 3)
        if int(t * 8) % 2:
            pygame.draw.circle(pantalla, (255, 200, 60), (x + 8, y - 46), 5)


def _flecha_jefe(pantalla, jefe, camara_x, t):
    """Si el jefe no se ve, una flecha en el borde dice donde esta."""

    x = jefe.x - camara_x
    if -40 < x < ANCHO + 40:
        return
    izquierda = x < 0
    bx = 26 if izquierda else ANCHO - 26
    by = PISO_PANTALLA - 80 + int(math.sin(t * 6) * 4)
    punta = (bx - 16, by) if izquierda else (bx + 16, by)
    base = [(bx + 10, by - 16), (bx + 10, by + 16)] if izquierda else [(bx - 10, by - 16), (bx - 10, by + 16)]
    pygame.draw.polygon(pantalla, NEGRO, [punta] + base)
    pygame.draw.polygon(pantalla, ROJO, [(punta[0] + (3 if izquierda else -3), punta[1])] + [(b[0], b[1] + (3 if i == 0 else -3)) for i, b in enumerate(base)])


def _pelea(pantalla, reloj, sprites, fuentes, cabeza, estado):
    """Pelea contra el jefe. Devuelve "gano", "menu", "murio" (o los trucos)."""

    fuente_grande, fuente_media, fuente_chica = fuentes
    nivel = estado["nivel"]

    terreno, fondo, jefe = _armar_pelea(nivel, estado, sprites)
    jugador = J.Jugador(sprites, terreno)

    # La jaula del princesito Mxroy (en la sala de Teichi, a la derecha)
    mxroy = imagen_mxroy() if nivel == 30 else None
    if nivel == 30:
        estado["sala"] = (fondo, jefe.sprites)

    # --- cinematica antes de la pelea con Teichi (una vez por partida) ---
    if nivel == 30 and not escena_vista("presentacion_teichi"):
        marcar_escena_vista("presentacion_teichi")
        musica.pausar()
        escena_teichi_antes(pantalla, reloj, fuente_media, fondo, jefe.sprites, sprites, X_JAULA, PISO_PANTALLA)
        transicion.cerrar_circulo(pantalla, reloj)
        transicion.abrir_circulo()

    musica.reproducir_cancion("jefe_teichi" if nivel == 30 else "jefe_15")

    piedras = []
    ondas = []
    ayudantes = []             # gagambas que llama en la fase 3
    llevando = None            # None, una Piedra o "jefe"
    textos = []
    cartel_fase = [None, 0.0]  # (texto, tiempo) del cartel "FASE 2"
    camara = [0.0]
    t = 0.0

    def actualizar_camara():
        objetivo = max(0, min(jugador.rect.centerx - ANCHO // 2, terreno.ancho - ANCHO))
        camara[0] = objetivo

    def dibujar_todo(t_ext=0.0, con_jugador=True):
        temblor = (random.randint(-4, 4) if jefe.temblor > 0 else 0)
        cam = int(camara[0]) + temblor
        fondo.dibujar(pantalla, cam)
        if nivel == 15:
            _dibujar_bombas(pantalla, cam, t + t_ext)
        if mxroy is not None:
            dibujar_jaula(pantalla, X_JAULA - cam, PISO_PANTALLA, t + t_ext, mxroy)
        for onda in ondas:
            onda.dibujar(pantalla, cam)
        for p in piedras:
            if p.estado != "llevada":
                p.dibujar(pantalla, cam)
        for g in ayudantes:
            g.dibujar(pantalla, cam, CAMARA_Y)
        if jefe.estado != "agarrado":
            jefe.dibujar(pantalla, cam, t + t_ext)
        # En la animacion de muerte el jugador lo dibuja ella (si no, se ve
        # dos veces: uno muriendo y uno parado)
        if con_jugador:
            jugador.dibujar(pantalla, cam, CAMARA_Y)
            if llevando == "jefe":
                jefe.dibujar(pantalla, cam, t + t_ext, arriba_de=jugador.rect)
            elif isinstance(llevando, Piedra):
                img = llevando.imagen
                pantalla.blit(img, img.get_rect(midbottom=(jugador.rect.centerx - cam, jugador.rect.top - CAMARA_Y + 4)))
        _flecha_jefe(pantalla, jefe, cam, t + t_ext)
        for texto, x, y, tt in jefe.textos + textos:
            cartel(pantalla, fuente_media, texto, int(255 * max(0, 1 - tt / 1.2)), int(y - CAMARA_Y), ROJO)
        dibujar_hud(pantalla, fuente_media, cabeza, estado["vidas"], estado["puntos"], nivel)
        dibujar_vida_jefe(pantalla, fuente_chica, jefe)

    actualizar_camara()

    titulo = "¡PELEA!" if nivel == 30 else "¡%s!" % jefe.nombre

    while True:

        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt

        apreto_e = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return "menu"
                if evento.key == cheats.TECLA:
                    accion = _trucos(pantalla, reloj, estado)
                    if accion is not None:
                        return accion
                if evento.key in TECLAS_AGARRAR:
                    apreto_e = True

        teclas = pygame.key.get_pressed()
        bottom_anterior = jugador.rect.bottom
        x_antes = jugador.rect.x
        jugador.mover(teclas, dt)
        # Con el jefe a cuestas se camina mas lento
        if llevando == "jefe":
            jugador.rect.x = int(x_antes + (jugador.rect.x - x_antes) * 0.55)
        jugador.actualizar_parpadeo(dt)
        fondo.actualizar(dt)
        actualizar_camara()

        empieza = t > 1.4
        if empieza and jefe.estado not in ("agarrado",):
            jefe.actualizar(dt, jugador, terreno)

        # --- cambio de fase: cartel, frase y (en la 3) ayudantes ---
        if jefe.fase_nueva is not None:
            fase = jefe.fase_nueva
            jefe.fase_nueva = None
            cartel_fase[0] = "¡FASE %d!" % fase
            cartel_fase[1] = 0.0
            frase = jefe.frases_fase.get(fase)
            if frase:
                jefe.textos.append([frase, jefe.x, jefe.y - 230, -0.6])
            sonidos.reproducir("carta")
            if fase == 3:
                # Aparecen lejos del jugador (nunca encima)
                lugares = [x for x in range(jefe.arena[0], jefe.arena[1] - 60, 40)
                           if abs(x - jugador.rect.centerx) > 320]
                random.shuffle(lugares)
                elegidos = []
                for x in lugares:
                    if all(abs(x - e) > 260 for e in elegidos):
                        elegidos.append(x)
                    if len(elegidos) == AYUDANTES_FASE_3:
                        break
                for x in elegidos:
                    ayudantes.append(J.Enemigo(int(x), sprites["enemigo"], 130, 90, PISO_Y))

        piedras += jefe.piedras_nuevas
        jefe.piedras_nuevas = []
        ondas += jefe.ondas_nuevas
        jefe.ondas_nuevas = []

        for p in piedras:
            p.actualizar(dt, terreno)
        for o in ondas:
            o.actualizar(dt, terreno)
        for g in ayudantes:
            g.mover(dt)
            g.actualizar(dt)
        textos = [[tx, x, y - 50 * dt, tt + dt] for tx, x, y, tt in textos if tt < 1.2]
        cartel_fase[1] += dt

        # --- E: agarrar / tirar ---
        if apreto_e:
            if llevando == "jefe":
                direccion = 1 if jugador.mirando_derecha else -1
                jefe.estado = "volando"
                jefe.t = 0
                jefe.x = jugador.rect.centerx + direccion * 30
                jefe.y = jugador.rect.top - 20
                jefe.vx = 640 * direccion
                jefe.vy = -620
                llevando = None
                sonidos.reproducir("salto")
            elif isinstance(llevando, Piedra):
                direccion = 1 if jugador.mirando_derecha else -1
                llevando.estado = "lanzada"
                llevando.x = jugador.rect.centerx + direccion * 24
                llevando.y = jugador.rect.top - 10
                llevando.vx = 950 * direccion
                llevando.vy = -260
                llevando = None
                sonidos.reproducir("salto")
            elif jefe.mareado and jugador.rect.inflate(30, 10).colliderect(jefe.rect()):
                llevando = "jefe"
                jefe.estado = "agarrado"
                textos.append(["¡A REVOLEARLO!", jugador.rect.centerx, jugador.rect.top - 40, 0.0])
                sonidos.reproducir("boton")
            else:
                for p in piedras:
                    if p.estado == "piso" and jugador.rect.inflate(30, 20).colliderect(p.rect):
                        p.estado = "llevada"
                        llevando = p
                        sonidos.reproducir("boton")
                        break

        # Si el jefe que llevabas se solto solo (no deberia), se suelta
        if llevando == "jefe" and jefe.estado != "agarrado":
            llevando = None

        # --- piedras lanzadas contra el jefe (y contra los ayudantes) ---
        for p in piedras:
            if p.estado != "lanzada":
                continue
            if jefe.estado not in ("herido", "derrotado", "volando", "quemado", "agarrado") and p.rect.colliderect(jefe.rect()):
                p.terminada = True
                jefe.marear()
                jefe.textos.append(["¡MAREADO!", jefe.x, jefe.y - 170, 0.0])
                sonidos.reproducir("golpe")
                continue
            for g in ayudantes:
                if not g.aplastado and p.rect.colliderect(g.rect):
                    g.aplastar()
                    p.terminada = True
                    sonidos.reproducir("aplastar")
                    break

        piedras = [p for p in piedras if not p.terminada]
        ondas = [o for o in ondas if not o.terminada]

        # --- saltarle encima ---
        murio = False
        caja = jefe.rect()
        if jefe.estado not in ("derrotado", "agarrado") and jugador.rect.colliderect(caja):
            desde_arriba = jugador.vel_y > 0 and bottom_anterior <= caja.top + 24
            if desde_arriba:
                jugador.rect.bottom = caja.top
                jugador.vel_y = J.SALTO_FUERZA * 0.7
                jugador.en_suelo = False
                if jefe.mareado:
                    jefe.pegar()
                else:
                    sonidos.reproducir("aplastar")
            elif jefe.peligroso:
                murio = True

        # --- ayudantes (gagambas): pisarlos o esquivarlos ---
        murio = murio or resolver_gagambas(jugador, ayudantes, bottom_anterior)
        ayudantes = [g for g in ayudantes if not (g.aplastado and g.tiempo_aplastado <= 0)]

        # --- piedras en el aire y ondas ---
        for p in piedras:
            if p.estado == "vuela" and p.rect.colliderect(jugador.rect):
                murio = True
        for o in ondas:
            if o.rect.colliderect(jugador.rect) and jugador.rect.bottom > PISO_Y - 18:
                murio = True

        # --- lava o bombas ---
        en_lava = jugador.rect.top > PISO_Y - 10
        if nivel == 15 and (jugador.rect.left < BOMBAS[0] + ZONA_BOMBAS - 70 or jugador.rect.right > BOMBAS[1] - ZONA_BOMBAS + 70):
            murio = True
        murio = murio or en_lava

        if murio:
            if llevando == "jefe":
                jefe.marear(0.5)
                llevando = None
            musica.pausar()
            sonidos.reproducir("golpe")
            J.animacion_muerte(
                pantalla, reloj, jugador, sprites, int(camara[0]),
                _FondoPelea(lambda: dibujar_todo(con_jugador=False)), CAMARA_Y
            )
            return "murio"

        # --- gano ---
        if jefe.estado == "derrotado" and jefe.t >= jefe.duracion:
            _final_jefe(pantalla, reloj, fuentes, nivel, dibujar_todo, sprites, estado)
            return "gano"

        # --- dibujar ---
        dibujar_todo()

        if t < 1.8:
            cartel(pantalla, fuente_grande, titulo, int(255 * min(1.0, (1.8 - t) / 0.4)))
        else:
            # Donde estas (despues del cartel de la pelea)
            if nivel == 30:
                J.dibujar_cartel_lugar(pantalla, fuente_media, t - 1.8, "SALA DE LORD TEICHI", "BURZACO - CASTILLO", 150)
            else:
                J.dibujar_cartel_lugar(pantalla, fuente_media, t - 1.8, "LA BOMBONERA", "LA BOCA - BUENOS AIRES", 150)

        if cartel_fase[0] is not None and cartel_fase[1] < 2.0:
            alfa = int(255 * min(1.0, (2.0 - cartel_fase[1]) / 0.4))
            cartel(pantalla, fuente_grande, cartel_fase[0], alfa, 200)

        # Ayuda de la tecla E
        if t < 8 or jefe.mareado or any(p.estado == "piso" for p in piedras) or llevando is not None:
            ayuda = "E: TIRAR" if llevando is not None else "E: AGARRAR"
            _texto_sombra(pantalla, fuente_chica, ayuda, BLANCO, midbottom=(ANCHO // 2, ALTO - 10))

        pygame.display.flip()


def _trucos(pantalla, reloj, estado):
    """F10: menu de trucos. Devuelve "saltear", "ir" o None (seguir)."""

    truco = cheats.menu_cheats(pantalla, reloj, estado["vidas"], estado["nivel"])
    estado["vidas"] = truco["vidas"]
    estado["puntos"] = truco["puntos"]

    if truco["accion"] == "saltear":
        return "saltear"
    if truco["accion"] is not None:
        cheats.ir_al_nivel(truco["accion"][1])
        return "ir"
    return None


class _FondoPelea:
    """Para la animacion de muerte: dibuja la sala como esta (sin el
    jugador, que lo dibuja la animacion)."""

    def __init__(self, dibujar):
        self._dibujar = dibujar

    def dibujar(self, pantalla, camara_x=0, camara_y=0):
        self._dibujar()


def _final_jefe(pantalla, reloj, fuentes, nivel, dibujar_todo, sprites=None, estado=None):
    fuente_grande, fuente_media, fuente_chica = fuentes
    sonidos.reproducir("nivel_completo")

    if nivel == 30 and estado is not None and "sala" in estado:
        # El final: Teichi a la lava, la jaula, el trofeo y "continuara..."
        musica.detener()
        transicion.cerrar_circulo(pantalla, reloj)
        transicion.abrir_circulo()
        fondo, sprites_t = estado["sala"]
        escena_final(pantalla, reloj, fuente_media, fondo, sprites_t, sprites, X_JAULA, PISO_PANTALLA, 170)
        return

    if nivel == 15:
        # Cinematica: el robot destruido y Teichi por los parlantes
        musica.detener()
        transicion.cerrar_circulo(pantalla, reloj)
        transicion.abrir_circulo()
        escena_robot_destruido(pantalla, reloj, fuente_media, sprites, _robot(estado, sprites))
        return

    if nivel == 30:
        cabeza_t = pygame.image.load(os.path.join(CARPETA_TEICHI, "teichi cabeza.png")).convert_alpha()
        dialogo(
            pantalla, reloj, fuente_media,
            [("LORD TEICHI", "¡NOOO! ¿Cómo pudieron vencerme unos Compu Broskis tan diminutos...?")],
            {"LORD TEICHI": (cabeza_t, 6, (120, 30, 40))},
            lambda tt: dibujar_todo(tt),
        )
        mensajes = ["¡DERROTASTE A LORD TEICHI!", "¡RESCATASTE AL PRINCESITO MXROY!"]
    else:
        mensajes = ["¡JEFE DERROTADO!"]

    t = 0.0
    while t < 3.5:
        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE) and t > 1.0:
                t = 99
        dibujar_todo(t)
        velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        velo.fill((0, 0, 0, min(150, int(t * 200))))
        pantalla.blit(velo, (0, 0))
        for k, m in enumerate(mensajes):
            cartel(pantalla, fuente_media, m, min(255, int(t * 400)), ALTO // 2 - 30 + k * 50)
        pygame.display.flip()


# ==========================================================
# ENTRADA (la llama juego.jugar)
# ==========================================================

def jugar_jefe(pantalla, reloj, sprites, fuente_grande, fuente_media, cabeza=None, nivel=15):
    """
    Nivel 15 o 30. Devuelve lo mismo que juego.jugar: "mapa_victoria",
    "menu" o "personajes" (sin vidas).
    """

    fuente_chica = type(fuente_media)(2)
    fuentes = (fuente_grande, fuente_media, fuente_chica)

    estado = {
        "vidas": J.VIDAS_INICIALES + cargar_vidas_extra(),
        "puntos": cargar_puntos(),
        "nivel": nivel,
        "cuadros": cargar_cuadros() if nivel == 30 else [],
    }

    etapa = "castillo" if nivel == 30 else "jefe"

    # Antes de la primera pelea: el robot llega a la Bombonera (una vez por
    # partida)
    if nivel == 15 and not escena_vista("robot_llega"):
        marcar_escena_vista("robot_llega")
        musica.pausar()
        escena_robot_llega(pantalla, reloj, fuente_media, sprites, _robot(estado, sprites))
        transicion.cerrar_circulo(pantalla, reloj)
        transicion.abrir_circulo()

    while True:

        if etapa == "castillo":
            resultado = _castillo(pantalla, reloj, sprites, fuentes, cabeza, estado)
        else:
            resultado = _pelea(pantalla, reloj, sprites, fuentes, cabeza, estado)

        if resultado == "menu":
            return "menu"

        # Trucos (F10)
        if resultado == "saltear":
            cheats.saltear_nivel(nivel)
            return "mapa_victoria"

        if resultado == "ir":
            return "mapa"

        if resultado == "puerta":
            # Entra a la sala: si se muere adentro, vuelve a la sala
            transicion.cerrar_circulo(pantalla, reloj)
            transicion.abrir_circulo()
            etapa = "jefe"
            continue

        if resultado == "gano":
            completar_nivel(nivel)
            return "mapa_victoria"

        # murio
        sonidos.reproducir("perder_vida")
        estado["vidas"] -= 1
        gastar_vida_extra()

        if estado["vidas"] <= 0:
            musica.detener()
            reiniciar_progreso()
            J.pantalla_game_over(pantalla, reloj, fuente_media)
            return "personajes"

        transicion.cerrar_circulo(pantalla, reloj)
        transicion.abrir_circulo()
        J.pantalla_vidas(pantalla, reloj, sprites, estado["vidas"], fuente_media)
        transicion.cerrar_circulo(pantalla, reloj)
        transicion.abrir_circulo()

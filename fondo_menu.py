"""
Fondo animado del menu: el Obelisco en pixel art con nubes que se mueven
y carteles de publicidad con luz animada (como un "gif" hecho con codigo).

Capas, de atras para adelante:
    1. fondo_menu.png          -> imagen completa
    2. nubes                   -> solo se ven en el cielo (la capa 3 las tapa)
    3. fondo_menu_frente.png   -> obelisco, edificios y arboles (cielo transparente)
    4. carteles                -> brillo pulsante + barrido de luz sobre cada cartel
                                  (usa fondo_menu_carteles.png como mascara)

Uso en main.py:
    FONDO_MENU = FondoMenuAnimado(CARPETA, ANCHO, ALTO)
    ...
    FONDO_MENU.dibujar(pantalla)      # en lugar de pantalla.fill(CELESTE)

Las coordenadas de los carteles estan en pixeles de la imagen original
(1254 x 1254); la clase las convierte a pantalla.
"""

import math
import os
import random

import pygame


# ==========================================================
# CONFIGURACION
# ==========================================================

IMG_LADO = 1254          # la imagen original es de 1254 x 1254
RECORTE_Y = 98           # cuanto se corta de arriba (en px de la imagen)
                         # 98 deja justo la punta del obelisco

# ----------------------------------------------------------
# NUBES
# ----------------------------------------------------------

# (y en pantalla, ancho en celdas, alto en celdas, velocidad px/s)
NUBES = [
    (28, 34, 11, 7),
    (95, 26, 9, 11),
    (165, 40, 12, 5),
    (60, 18, 7, 15),
    (215, 22, 8, 9),
    (130, 16, 6, 13),
]
CELDA_NUBE = 3            # tamano de cada "pixel" de nube en pantalla

COLOR_NUBE = (255, 255, 255)
COLOR_NUBE_SOMBRA = (205, 226, 250)

# ----------------------------------------------------------
# CARTELES: caja (x0, y0, x1, y1) en px de la imagen original y
# parametros de la animacion:
#   pulso     = segundos que tarda en latir el brillo
#   barrido   = segundos entre barridos de luz (0 = sin barrido)
#   fase      = desfase para que no latan todos a la vez
#   parpadea  = True: se apaga un instante, como un neon
# ----------------------------------------------------------

CARTELES = [
    {"nombre": "hotel",    "caja": (47, 359, 155, 444),
     "pulso": 3.2, "barrido": 5.0, "fase": 0.0, "parpadea": False},
    {"nombre": "samsung",  "caja": (1126, 377, 1246, 486),
     "pulso": 2.6, "barrido": 4.2, "fase": 1.7, "parpadea": False},
    {"nombre": "rosa",     "caja": (1056, 477, 1106, 583),
     "pulso": 2.0, "barrido": 3.6, "fase": 0.9, "parpadea": False},
    {"nombre": "pantalla", "caja": (252, 550, 288, 713),
     "pulso": 1.6, "barrido": 3.0, "fase": 2.3, "parpadea": False},
    {"nombre": "inferior", "caja": (1107, 754, 1238, 796),
     "pulso": 2.4, "barrido": 0.0, "fase": 0.4, "parpadea": True},
]

BRILLO_BASE = 22          # opacidad minima del brillo (0-255)
BRILLO_PULSO = 26         # cuanto sube el brillo al latir
BRILLO_SUMA = 55          # cuanto se aclara el color del cartel
BARRIDO_ALPHA = 120       # opacidad maxima de la franja de luz
BARRIDO_ANCHO = 0.28      # ancho de la franja (fraccion del cartel)
BARRIDO_DURACION = 1.3    # segundos que tarda en cruzar el cartel


# ==========================================================
# ANIMACION DE CARTELES (sin pygame: solo numeros)
# ==========================================================

def estado_cartel(cartel, t):
    """(brillo 0-255, posicion del barrido 0..1 o None) en el instante t."""

    brillo = BRILLO_BASE + BRILLO_PULSO * (
        0.5 + 0.5 * math.sin(2 * math.pi * t / cartel["pulso"] + cartel["fase"])
    )

    if cartel["parpadea"]:

        # neon: de a ratos se apaga 2-3 veces seguidas
        ciclo = (t + cartel["fase"]) % 5.5

        if 4.2 < ciclo < 4.3 or 4.5 < ciclo < 4.58 or 4.8 < ciclo < 4.95:
            brillo = 0

    barrido = None

    if cartel["barrido"] > 0:

        ciclo = (t + cartel["fase"] * 0.6) % cartel["barrido"]

        if ciclo < BARRIDO_DURACION:
            barrido = ciclo / BARRIDO_DURACION

    return brillo, barrido


# ==========================================================
# SIMULACION DE NUBES (sin pygame: solo posiciones)
# ==========================================================

class SimulacionMenu:
    """Mueve las nubes."""

    def __init__(self, ancho_pantalla, semilla=7):

        self.azar = random.Random(semilla)
        self.ancho = ancho_pantalla

        # nubes: [x, y, ancho_celdas, alto_celdas, velocidad, forma]
        self.nubes = []

        for y, an, al, vel in NUBES:

            self.nubes.append([
                self.azar.uniform(-an * CELDA_NUBE, ancho_pantalla),
                y, an, al, vel,
                forma_nube(an, al, self.azar),
            ])

    def actualizar(self, dt):

        for nube in self.nubes:

            nube[0] += nube[4] * dt

            if nube[0] > self.ancho + 10:

                nube[0] = -nube[2] * CELDA_NUBE - self.azar.randint(0, 120)


def forma_nube(an, al, azar):
    """Matriz de celdas: 0 vacio, 1 nube, 2 nube con sombra.

    Son varias cupulas que se pisan, con la panza plana abajo."""

    celdas = [[0] * an for _ in range(al)]

    n = max(3, an // 5)
    cupulas = []

    for i in range(n):

        centro = an * (i + 0.5) / n + azar.uniform(-1, 1)
        radio_x = an / n * azar.uniform(0.85, 1.35)

        # las del medio son mas altas
        altura = al * (0.45 + 0.5 * math.sin(math.pi * (i + 0.5) / n))
        altura *= azar.uniform(0.8, 1.0)

        cupulas.append((centro, radio_x, altura))

    for y in range(al):
        for x in range(an):

            for cx, rx, ry in cupulas:

                if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - (al - 1)) / ry) ** 2 <= 1:

                    celdas[y][x] = 1
                    break

    # sombra: las 2 filas de abajo de cada columna
    for x in range(an):

        ultimas = [y for y in range(al) if celdas[y][x]]

        for y in ultimas[-2:]:
            celdas[y][x] = 2

    return celdas


# ==========================================================
# DIBUJO (pygame)
# ==========================================================

class FondoMenuAnimado:

    def __init__(self, carpeta, ancho, alto):

        ruta = os.path.join(carpeta, "assets", "fondos")

        self.ancho = ancho
        self.alto = alto

        self.factor = ancho / IMG_LADO
        lado = round(IMG_LADO * self.factor)
        self.recorte = min(round(RECORTE_Y * self.factor), lado - alto)

        ventana = pygame.Rect(0, self.recorte, ancho, alto)

        def cargar(nombre, alpha):

            img = pygame.image.load(os.path.join(ruta, nombre))
            img = img.convert_alpha() if alpha else img.convert()

            return pygame.transform.smoothscale(
                img, (lado, lado)
            ).subsurface(ventana).copy()

        self.fondo = cargar("fondo_menu.png", False)
        self.frente = cargar("fondo_menu_frente.png", True)
        carteles = cargar("fondo_menu_carteles.png", True)

        self.frente_rect = self.frente.get_bounding_rect()

        self.sim = SimulacionMenu(ancho)
        self.nubes_sup = self._crear_nubes()
        self.carteles = self._crear_carteles(carteles)

        self.t = 0.0
        self.ultimo = None

    # ------------------------------------------------------
    # NUBES
    # ------------------------------------------------------

    def _crear_nubes(self):

        superficies = []

        for nube in self.sim.nubes:

            celdas = nube[5]
            al, an = len(celdas), len(celdas[0])

            sup = pygame.Surface((an * CELDA_NUBE, al * CELDA_NUBE), pygame.SRCALPHA)

            for y, fila in enumerate(celdas):
                for x, v in enumerate(fila):

                    if v:
                        sup.fill(
                            COLOR_NUBE if v == 1 else COLOR_NUBE_SOMBRA,
                            (x * CELDA_NUBE, y * CELDA_NUBE, CELDA_NUBE, CELDA_NUBE),
                        )

            superficies.append(sup)

        return superficies

    # ------------------------------------------------------
    # CARTELES
    # ------------------------------------------------------

    def _crear_carteles(self, capa):
        """Por cada cartel: su posicion, una version aclarada y una mascara
        blanca para recortar la franja de luz."""

        lista = []

        for datos in CARTELES:

            x0, y0, x1, y1 = datos["caja"]

            rect = pygame.Rect(
                int(x0 * self.factor),
                int(y0 * self.factor) - self.recorte,
                math.ceil((x1 - x0) * self.factor) + 1,
                math.ceil((y1 - y0) * self.factor) + 1,
            ).clip(pygame.Rect(0, 0, self.ancho, self.alto))

            sup = capa.subsurface(rect).copy()

            # version aclarada: suma luz al color (el alpha no cambia)
            clara = sup.copy()
            clara.fill(
                (BRILLO_SUMA, BRILLO_SUMA, BRILLO_SUMA, 0),
                special_flags=pygame.BLEND_RGBA_ADD,
            )

            # mascara blanca con la forma del cartel
            mascara = sup.copy()
            mascara.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_ADD)

            # franja de luz: opaca en el centro, transparente en los bordes
            ancho_franja = max(4, int(rect.width * BARRIDO_ANCHO))
            franja = pygame.Surface((ancho_franja, rect.height), pygame.SRCALPHA)

            for x in range(ancho_franja):

                a = BARRIDO_ALPHA * (1 - abs(2 * (x + 0.5) / ancho_franja - 1))
                franja.fill((255, 255, 255, int(a)), (x, 0, 1, rect.height))

            lista.append({
                "datos": datos,
                "rect": rect,
                "clara": clara,
                "mascara": mascara,
                "franja": franja,
                "tmp": pygame.Surface(rect.size, pygame.SRCALPHA),
            })

        return lista

    def _dibujar_cartel(self, superficie, cartel):

        brillo, barrido = estado_cartel(cartel["datos"], self.t)

        rect = cartel["rect"]

        # 1) latido: la version aclarada con opacidad variable
        if brillo > 0:

            cartel["clara"].set_alpha(int(brillo))
            superficie.blit(cartel["clara"], rect)

        # 2) barrido: una franja de luz que cruza el cartel de lado a lado
        if barrido is not None:

            franja = cartel["franja"]
            x = int(-franja.get_width() + barrido * (rect.width + franja.get_width()))

            tmp = cartel["tmp"]
            tmp.fill((0, 0, 0, 0))
            tmp.blit(franja, (x, 0))
            tmp.blit(cartel["mascara"], (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            superficie.blit(tmp, rect)

    # ------------------------------------------------------
    # DIBUJO
    # ------------------------------------------------------

    def dibujar(self, superficie):

        # tiempo transcurrido (limitado por si el menu estuvo cerrado)
        ahora = pygame.time.get_ticks()
        dt = 0.016 if self.ultimo is None else min((ahora - self.ultimo) / 1000, 0.05)
        self.ultimo = ahora

        self.t += dt
        self.sim.actualizar(dt)

        # 1) fondo
        superficie.blit(self.fondo, (0, 0))

        # 2) nubes
        for nube, sup in zip(self.sim.nubes, self.nubes_sup):
            superficie.blit(sup, (round(nube[0]), nube[1]))

        # 3) obelisco, edificios y arboles por delante de las nubes
        superficie.blit(self.frente, self.frente_rect, self.frente_rect)

        # 4) luz animada de los carteles
        for cartel in self.carteles:
            self._dibujar_cartel(superficie, cartel)

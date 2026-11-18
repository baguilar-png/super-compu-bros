"""
Fondos pixel art de los niveles de Super Compu Bros.

Cada nivel es un barrio de Buenos Aires con tres pisos apilados: la calle
(abajo), los techos de una fila de edificios (en el medio) y el cielo con sus
nubes (arriba). A lo lejos se ven los monumentos del barrio. Se arma con
cuatro capas (assets/niveles/, generadas con herramientas/generar_techos.py),
de la mas lejana a la mas cercana:

    nivel_NN_cielo.png    cielo, sol o luna y nubes. Casi no se mueve.
    nivel_NN_lejos.png    ciudad lejana y los monumentos del barrio, con
                          bruma. Se mueve despacio.
    nivel_NN_medio.png    edificios del medio. Se mueve a media velocidad.
    nivel_NN_ciudad.png   la calle, los edificios y los techos por donde se
                          camina, pegados al nivel (se mueve igual que la
                          camara, tambien hacia arriba y abajo).

Cada capa se mueve mas despacio cuanto mas lejos esta (efecto de profundidad /
parallax). La velocidad sale sola del ancho de cada imagen: una capa que mide
justo lo que mide el nivel se mueve con la camara, y una mas angosta se mueve
proporcionalmente mas lento. Asi el principio y el final de cada capa siempre
coinciden con el principio y el final del nivel.

Cuando la camara sube y baja, las capas lejanas se mueven en vertical mas
despacio que las cercanas (tambien parallax). Y cuanto mas arriba se sube,
mas negro se pone el cielo y aparecen las estrellas (ver `oscuridad`). Las
nubes donde se camina se dibujan por codigo (pixel art generado al vuelo).

Los dibujos estan hechos con pixeles de 1 x 1 y se agrandan PX veces: cada
pixel de dibujo ocupa PX x PX pixeles de la pantalla.

Dia y noche: cada nivel es de dia (con sol: reflejos en los vidrios, rayos,
destellos que titilan y un resplandor con reflejos de lente) o de noche (con
luna, ventanas prendidas, postes de luz que alumbran, carteles de neon y luces
rojas de aviso que parpadean). Lo que se dibuja en las capas ya viene en las
imagenes; lo que se mueve (destellos, luz de los postes, balizas, el brillo del
sol y de la luna) se anota en nivel_NN_efectos.json y se anima aca, con el
mismo parallax que la capa donde esta. Si falta ese archivo, el fondo se ve
igual (solo quieto).

Si faltan las capas lejos y medio, igual anda (con el cielo y la ciudad). Y si
faltan las imagenes se usa un fondo simple (cielo celeste y edificios grises
con la forma de los techos), asi el juego nunca se rompe.
"""

import json
import math
import os
import random

import pygame

CARPETA = os.path.dirname(os.path.abspath(__file__))

CARPETA_NIVELES = os.path.join(CARPETA, "assets", "niveles")

TOTAL_FONDOS = 30

# Pixeles de pantalla por pixel de dibujo
PX = 3

# Capas, de la mas lejana a la mas cercana: (sufijo del archivo, tiene
# transparencia, cuanto se mueve en vertical respecto de la camara). El cielo
# es la unica que tapa toda la pantalla.
CAPAS = (
    ("cielo", False, 0.08),
    ("lejos", True, 0.30),
    ("medio", True, 0.60),
    ("ciudad", True, 1.00),
)

# Cielo cada vez mas negro: de OSCURO_DESDE_Y (altura del mundo donde
# empieza) a OSCURO_TOTAL_Y (negro del todo)
OSCURO_DESDE_Y = 60
OSCURO_TOTAL_Y = -1500

# Cuanto tapa la oscuridad como maximo (0 a 255) y de que color es
OSCURO_ALFA_MAX = 247
OSCURO_COLOR = (3, 4, 16)

# Estrellas: aparecen cuando la oscuridad pasa de ESTRELLAS_DESDE
ESTRELLAS = 150
ESTRELLAS_DESDE = 0.30

# Nubes (pixel art): cada pixel de dibujo mide PX, y la superficie donde se
# pisa queda NUBE_FILAS_ARRIBA filas abajo del borde de arriba del dibujo
NUBE_FILAS_ARRIBA = 6
NUBE_FILAS_CUERPO = 9
NUBE_COLOR_BORDE = (92, 126, 190)
NUBE_COLOR_LUZ = (255, 255, 255)
NUBE_COLOR_MEDIO = (226, 236, 252)
NUBE_COLOR_SOMBRA = (176, 198, 238)

# Nubes de noche: iluminadas por la luna (azules apagadas)
NUBE_NOCHE_BORDE = (34, 44, 98)
NUBE_NOCHE_LUZ = (126, 142, 206)
NUBE_NOCHE_MEDIO = (88, 104, 168)
NUBE_NOCHE_SOMBRA = (60, 72, 134)

# Niveles de noche: el texto del HUD se dibuja en blanco para que se lea y
# las nubes se ven a la luz de la luna
NIVELES_OSCUROS = (3, 6, 9, 12, 14, 15, 18, 21, 23, 25, 27, 30)

# Niveles que transcurren por dentro de un edificio (el 1: el Instituto Huergo).
# Son de un solo piso: la camara nunca sube, no hay nubes ni estrellas, y la
# capa cercana (las paredes hasta el cielorraso) tapa toda la pantalla.
NIVELES_INTERIOR = (1,)

INTERIOR_OSCURO_COLOR = (12, 9, 7)

# Destellos del sol en los vidrios: cuanto dura cada uno dentro de su ciclo
DESTELLO_DURACION = 0.30
DESTELLO_COLOR = (255, 252, 226)

# Luces rojas de aviso: parte del ciclo que estan prendidas
BALIZA_PRENDIDA = 0.45

# Resplandor del sol y de la luna (radio en pixeles de pantalla, color y
# cuanto suman) y reflejos de lente del sol: (a que fraccion del camino del
# sol al centro de la pantalla, radio en pixeles de dibujo, color, cuanto suman)
SOL_BRILLO = ((320, (255, 236, 180), 0.32), (110, (255, 250, 225), 0.42))
LUNA_BRILLO = ((250, (150, 175, 255), 0.30), (90, (220, 230, 255), 0.36))
REFLEJOS_LENTE = (
    (0.55, 3, (255, 214, 140), 0.16),
    (0.95, 5, (150, 220, 255), 0.10),
    (1.40, 3, (255, 190, 220), 0.14),
)


def numero_de_fondo(nivel):
    """Hay un fondo por nivel (1 a 30); pasado el 30 da la vuelta."""

    return ((max(1, int(nivel)) - 1) % TOTAL_FONDOS) + 1


class FondoNivel:

    def __init__(
        self,
        nivel,
        ancho_pantalla,
        alto_pantalla,
        suelo_y,
        nivel_ancho,
        color_cielo,
        color_suelo,
        terreno=None
    ):

        self.ancho = ancho_pantalla
        self.alto = alto_pantalla
        self.suelo_y = suelo_y
        self.nivel_ancho = nivel_ancho

        self.color_cielo = color_cielo
        self.color_suelo = color_suelo

        # Los techos (para el fondo simple, si faltan las imagenes)
        self.terreno = terreno

        self.numero = numero_de_fondo(nivel)

        self.oscuro = self.numero in NIVELES_OSCUROS

        # Por dentro de un edificio: sin nubes ni estrellas
        self.interior = self.numero in NIVELES_INTERIOR

        self._color_oscuro = INTERIOR_OSCURO_COLOR if self.interior else OSCURO_COLOR

        # Filas del dibujo de cada nube que quedan arriba de donde se pisa
        self._filas_arriba = NUBE_FILAS_ARRIBA

        # Luces animadas (destellos, postes, balizas, sol y luna): se leen de
        # nivel_NN_efectos.json (si falta, el fondo se ve igual pero quieto)
        self.efectos = None

        # Cuanto se mueve el cielo (para ubicar el sol y la luna)
        self._vel_cielo = 0.0

        self._ancho_cielo = 0

        # Resplandores ya hechos (se suman a lo que hay detras)
        self._resplandores = {}

        # Colores de las nubes: de dia blancas, de noche a la luz de la luna
        if self.oscuro:

            self._colores_nube = (
                NUBE_NOCHE_BORDE, NUBE_NOCHE_LUZ, NUBE_NOCHE_MEDIO, NUBE_NOCHE_SOMBRA
            )

        else:

            self._colores_nube = (
                NUBE_COLOR_BORDE, NUBE_COLOR_LUZ, NUBE_COLOR_MEDIO, NUBE_COLOR_SOMBRA
            )

        # Cada capa: [imagen, cuanto se mueve (0 a 1), fila desde donde hay
        # dibujo]. Solo se dibuja desde esa fila hacia abajo.
        self.capas = []

        self.cielo = None
        self.ciudad = None

        # Degradado negro del cielo (se arma la primera vez que se necesita),
        # estrellas y dibujos de nubes ya hechos
        self._degradado = None
        self._estrellas = None
        self._nubes = {}

        self._cargar()


    # ------------------------------------------------------
    # CARGA
    # ------------------------------------------------------

    def _cargar_capa(self, sufijo, transparente, vel_y):

        ruta = os.path.join(
            CARPETA_NIVELES,
            "nivel_{:02d}_{}.png".format(self.numero, sufijo)
        )

        imagen = pygame.image.load(ruta)

        # Se agranda una sola vez al cargar el nivel
        imagen = pygame.transform.scale(
            imagen,
            (imagen.get_width() * PX, imagen.get_height() * PX)
        )

        # convert() necesita que ya exista la ventana
        if pygame.display.get_surface() is not None:

            imagen = (
                imagen.convert_alpha() if transparente else imagen.convert()
            )

        # Cuanto se mueve: justo lo que hace falta para que el final de la
        # imagen coincida con el final del nivel
        recorrido = max(1, self.nivel_ancho - self.ancho)

        velocidad = max(
            0.0,
            min(1.0, (imagen.get_width() - self.ancho) / recorrido)
        )

        # Desde que fila hay algo dibujado (arriba no hace falta copiar)
        fila = 0

        if transparente:

            fila = min(imagen.get_bounding_rect().top, self.alto - 1)

        return [imagen, velocidad, fila, vel_y, sufijo]


    def _cargar(self):

        try:

            for sufijo, transparente, vel_y in CAPAS:

                try:

                    capa = self._cargar_capa(sufijo, transparente, vel_y)

                except (pygame.error, FileNotFoundError):

                    # Solo el cielo y la ciudad son obligatorios
                    if sufijo in ("cielo", "ciudad"):
                        raise

                    continue

                self.capas.append(capa)

                if sufijo == "cielo":
                    self.cielo = capa[0]
                    self._vel_cielo = capa[1]
                    self._ancho_cielo = capa[0].get_width()

                if sufijo == "ciudad":
                    self.ciudad = capa[0]

        except (pygame.error, FileNotFoundError):

            self.capas = []
            self.cielo = None
            self.ciudad = None

        self._cargar_efectos()


    def _cargar_efectos(self):
        """Lee las luces animadas del nivel (es opcional: sin el, todo queda quieto)."""

        ruta = os.path.join(
            CARPETA_NIVELES,
            "nivel_{:02d}_efectos.json".format(self.numero)
        )

        try:

            with open(ruta, encoding="utf-8") as archivo:

                datos = json.load(archivo)

            # que tenga la forma esperada
            if isinstance(datos.get("capas"), dict):

                self.efectos = datos

        except (OSError, ValueError, AttributeError):

            self.efectos = None


    @property
    def listo(self):

        return self.cielo is not None and self.ciudad is not None


    # ------------------------------------------------------
    # DIBUJO
    # ------------------------------------------------------

    def oscuridad(self, y_mundo):
        """
        Que tan negro esta el cielo a esa altura del mundo: 0.0 (normal, de la
        calle a los primeros pisos de nubes) a 1.0 (negro del todo, bien arriba).
        """

        t = (OSCURO_DESDE_Y - y_mundo) / (OSCURO_DESDE_Y - OSCURO_TOTAL_Y)

        return max(0.0, min(1.0, t))


    def _armar_degradado(self):
        """Una franja de OSCURO_COLOR, cada fila mas opaca cuanto mas arriba."""

        # Filas desde OSCURO_TOTAL_Y - alto hasta OSCURO_DESDE_Y
        self._degradado_arriba = OSCURO_TOTAL_Y - self.alto

        filas = OSCURO_DESDE_Y - self._degradado_arriba

        superficie = pygame.Surface((self.ancho, filas), pygame.SRCALPHA)

        for fila in range(filas):

            y_mundo = self._degradado_arriba + fila

            alfa = int(OSCURO_ALFA_MAX * self.oscuridad(y_mundo))

            superficie.fill(self._color_oscuro + (alfa,), (0, fila, self.ancho, 1))

        self._degradado = superficie


    def _dibujar_oscuridad(self, pantalla, camara_y):

        # Solo si arriba de la pantalla ya empieza a oscurecer
        if camara_y >= OSCURO_DESDE_Y:

            return

        if self._degradado is None:

            self._armar_degradado()

        # Filas del degradado que se ven (en alturas del mundo)
        desde = max(camara_y, self._degradado_arriba)

        hasta = min(camara_y + self.alto, OSCURO_DESDE_Y)

        if hasta > desde:

            pantalla.blit(
                self._degradado,
                (0, desde - camara_y),
                (0, desde - self._degradado_arriba, self.ancho, hasta - desde)
            )

        # Mas arriba de lo que llega el degradado: negro del todo
        if camara_y < self._degradado_arriba:

            alto = min(self.alto, self._degradado_arriba - camara_y)

            pantalla.fill(self._color_oscuro, (0, 0, self.ancho, alto))


    def _dibujar_estrellas(self, pantalla, camara_x, camara_y):

        # (por dentro no hay cielo: no hay estrellas)
        if self.interior:

            return

        if self.oscuridad(camara_y + self.alto) <= ESTRELLAS_DESDE:

            return

        if self._estrellas is None:

            azar = random.Random(7 * self.numero + 1)

            self._estrellas = [
                (
                    azar.randrange(self.ancho),
                    azar.randrange(self.alto),
                    azar.choice((2, 2, 3)),
                    azar.uniform(150, 255),
                    azar.uniform(0, 6.28)
                )
                for _ in range(ESTRELLAS)
            ]

        tiempo = pygame.time.get_ticks() / 1000.0

        for x, y, lado, brillo, fase in self._estrellas:

            sx = int(x - camara_x * 0.05) % self.ancho

            sy = int(y - camara_y * 0.15) % self.alto

            visible = (
                self.oscuridad(camara_y + sy) - ESTRELLAS_DESDE
            ) / (1.0 - ESTRELLAS_DESDE)

            if visible <= 0:

                continue

            titilar = 0.75 + 0.25 * math.sin(tiempo * 2.0 + fase)

            v = int(brillo * min(1.0, visible * 1.6) * titilar)

            pantalla.fill((v, v, min(255, v + 25)), (sx, sy, lado, lado))


    # ------------------------------------------------------
    # NUBES (pixel art hecho al vuelo)
    # ------------------------------------------------------

    def _sprite_nube(self, ancho):
        """
        El dibujo de una nube de `ancho` pixeles de pantalla (en cache). La
        superficie plana donde se pisa es la fila NUBE_FILAS_ARRIBA: arriba
        quedan los bultos (detras del personaje) y abajo la panza redonda.
        """

        columnas = max(6, round(ancho / PX))

        if columnas in self._nubes:

            return self._nubes[columnas]

        azar = random.Random(columnas * 31 + self.numero)

        filas = NUBE_FILAS_ARRIBA + NUBE_FILAS_CUERPO

        superficie = NUBE_FILAS_ARRIBA

        celdas = [[False] * columnas for _ in range(filas)]

        # Los bultos de arriba: pocos y redondos, lejos de las puntas
        bultos = []

        for _ in range(max(2, columnas // 11)):

            radio = azar.uniform(5.0, 9.0)

            centro = azar.uniform(radio + 3, max(radio + 4, columnas - radio - 3))

            bultos.append((centro, radio, azar.uniform(0.55, 1.0) * NUBE_FILAS_ARRIBA))

        # Ancho de cada gajo de la panza y donde empieza
        gajo = azar.uniform(7.0, 9.0)

        fase = azar.uniform(0, gajo)

        for col in range(columnas):

            x = col + 0.5

            u = x / columnas * 2 - 1

            # Panza: una lente (mas profunda al medio) con gajos redondos
            lente = (1 - abs(u) ** 2.4) ** 0.5

            onda = abs(math.sin(math.pi * (x + fase) / gajo))

            abajo = NUBE_FILAS_CUERPO * lente * (0.72 + 0.28 * onda)

            abajo = max(abajo, 1.2)

            arriba = 0.0

            for centro, radio, alto in bultos:

                d = abs(x - centro)

                if d < radio:

                    arriba = max(arriba, alto * math.sqrt(1 - (d / radio) ** 2))

            f0 = superficie - int(round(arriba))

            f1 = superficie + int(round(abajo)) - 1

            for f in range(max(0, f0), min(filas, f1 + 1)):

                celdas[f][col] = True

        imagen = pygame.Surface((columnas * PX, filas * PX), pygame.SRCALPHA)

        for f in range(filas):

            for col in range(columnas):

                if not celdas[f][col]:

                    continue

                vecinos = (
                    f == 0 or not celdas[f - 1][col],
                    f == filas - 1 or not celdas[f + 1][col],
                    col == 0 or not celdas[f][col - 1],
                    col == columnas - 1 or not celdas[f][col + 1],
                )

                if any(vecinos):

                    color = self._colores_nube[0]

                elif f <= superficie + 1:

                    color = self._colores_nube[1]

                elif f <= superficie + 3:

                    color = self._colores_nube[2]

                else:

                    color = self._colores_nube[3]

                imagen.fill(color, (col * PX, f * PX, PX, PX))

        self._nubes[columnas] = imagen

        return imagen


    def _dibujar_nubes(self, pantalla, camara_x, camara_y):

        if self.terreno is None:

            return

        for n in self.terreno.nubes:

            if n.x1 < camara_x - 10 or n.x0 > camara_x + self.ancho + 10:

                continue

            if n.y < camara_y - 40 - self._filas_arriba * PX or n.y > camara_y + self.alto + 40:

                continue

            imagen = self._sprite_nube(n.x1 - n.x0)

            pantalla.blit(
                imagen,
                (
                    int(n.x0 - camara_x),
                    int(n.y - camara_y) - self._filas_arriba * PX
                )
            )


    # ------------------------------------------------------
    # LUCES ANIMADAS (sol, luna, destellos, postes y balizas)
    # ------------------------------------------------------

    def _resplandor(self, radio, color, cuanto, pasos=None):
        """
        Una mancha de luz redonda (en escalones, como el resto del dibujo) para
        sumar a lo que hay detras: negro afuera, mas claro hacia el centro. Las
        grandes (sol, luna) llevan mas escalones para que no se noten los aros.
        """

        if pasos is None:

            pasos = max(8, min(26, radio // 11))

        # la intensidad cambia en cada cuadro (titilar): se redondea a escalones
        # de 0.05 para no armar una imagen nueva todo el tiempo
        cuanto = round(cuanto * 20) / 20.0

        clave = (radio, tuple(color), cuanto, pasos)

        sup = self._resplandores.get(clave)

        if sup is None:

            lado = radio * 2 + 1

            sup = pygame.Surface((lado, lado))

            sup.fill((0, 0, 0))

            for i in range(pasos):

                rad = int(radio * (1.0 - i / float(pasos)))

                if rad < 1:

                    break

                f = cuanto * ((i + 1) / float(pasos)) ** 1.7

                pygame.draw.circle(
                    sup,
                    tuple(min(255, int(c * f)) for c in color),
                    (radio, radio),
                    rad
                )

            if pygame.display.get_surface() is not None:

                sup = sup.convert()

            self._resplandores[clave] = sup

        return sup


    def _sumar_luz(self, pantalla, x, y, radio, color, cuanto):
        """Suma un resplandor centrado en (x, y)."""

        if cuanto < 0.03:

            return

        pantalla.blit(
            self._resplandor(radio, color, cuanto),
            (int(x) - radio, int(y) - radio),
            special_flags=pygame.BLEND_RGB_ADD
        )


    def _dibujar_efectos_capa(self, pantalla, nombre, x_capa, oy, tiempo):
        """
        Las luces animadas de una capa (se dibujan justo despues de ella, asi
        las capas de adelante las tapan): destellos del sol en los vidrios,
        luz de los postes y luces rojas que parpadean.
        """

        if self.efectos is None:

            return

        datos = self.efectos["capas"].get(nombre)

        if not datos:

            return

        ancho = self.ancho

        alto = self.alto

        # ---- destellos del sol: titilan, cada uno a su ritmo
        for ax, ay, tam, periodo, fase in datos.get("brillos", ()):

            sx = ax * PX - x_capa

            sy = ay * PX + oy

            if sx < -40 or sx > ancho + 40 or sy < -40 or sy > alto + 40:

                continue

            ciclo = (tiempo / periodo + fase) % 1.0

            if ciclo >= DESTELLO_DURACION:

                continue

            fuerza = math.sin(math.pi * ciclo / DESTELLO_DURACION)

            largo = int(round(tam * fuerza))

            if largo <= 0:

                continue

            pantalla.fill(DESTELLO_COLOR, (sx, sy, PX, PX))

            for k in range(1, largo + 1):

                for dx, dy in ((k, 0), (-k, 0), (0, k), (0, -k)):

                    pantalla.fill(
                        DESTELLO_COLOR,
                        (sx + dx * PX, sy + dy * PX, PX, PX)
                    )

            if largo >= 2:

                self._sumar_luz(
                    pantalla, sx + PX // 2, sy + PX // 2, 14,
                    (255, 244, 200), 0.55 * fuerza
                )

        # ---- postes de luz: un resplandor que se suma, con un leve titilar
        for ax, ay, radio, color, parpadea, fase in datos.get("lamparas", ()):

            sx = ax * PX - x_capa

            sy = ay * PX + oy

            r_px = radio * PX

            if sx < -r_px or sx > ancho + r_px or sy < -r_px or sy > alto + r_px:

                continue

            cuanto = 0.50 + 0.04 * math.sin(tiempo * 2.1 + fase * 40.0)

            # algunas lamparas estan fallando: se apagan a ratos
            if parpadea:

                onda = math.sin(tiempo * 23.0 + fase * 50.0) * math.sin(tiempo * 5.1 + fase * 9.0)

                if onda > 0.55:

                    cuanto *= 0.25

            self._sumar_luz(pantalla, sx + PX // 2, sy + PX // 2, r_px, color, cuanto)

        # ---- luces rojas de aviso: prenden y apagan
        for ax, ay, color, radio, periodo, fase in datos.get("balizas", ()):

            sx = ax * PX - x_capa

            sy = ay * PX + oy

            if sx < -30 or sx > ancho + 30 or sy < -30 or sy > alto + 30:

                continue

            if (tiempo / periodo + fase) % 1.0 >= BALIZA_PRENDIDA:

                continue

            pantalla.fill(tuple(color), (sx, sy, PX, PX))

            self._sumar_luz(
                pantalla, sx + PX // 2, sy + PX // 2, radio * PX, color, 0.60
            )


    def _luces(self, dibujar, *argumentos):
        """
        Dibuja las luces animadas. Si el archivo de efectos esta mal armado (por
        ejemplo, editado a mano) se apagan las luces animadas y el juego sigue.
        """

        if self.efectos is None:

            return

        try:

            dibujar(*argumentos)

        except (ValueError, TypeError, KeyError, IndexError):

            self.efectos = None


    def _disco_pixelado(self, radio, color, cuanto):
        """Disco de pixeles grandes (reflejo de lente), para sumar."""

        cuanto = round(cuanto * 40) / 40.0

        clave = ("disco", radio, tuple(color), cuanto)

        sup = self._resplandores.get(clave)

        if sup is None:

            lado = radio * 2 + 1

            chico = pygame.Surface((lado, lado))

            chico.fill((0, 0, 0))

            col = tuple(int(c * cuanto) for c in color)

            pygame.draw.circle(chico, col, (radio, radio), radio)

            sup = pygame.transform.scale(chico, (lado * PX, lado * PX))

            if pygame.display.get_surface() is not None:

                sup = sup.convert()

            self._resplandores[clave] = sup

        return sup


    def _dibujar_astro(self, pantalla, camara_x, camara_y, tiempo):
        """
        El brillo del sol (con reflejos de lente) o de la luna, sumado por encima
        de todo el fondo: el sol le da a los edificios y a las nubes. Se apaga a
        medida que se sube y el cielo se pone negro.
        """

        if self.efectos is None:

            return

        astro = self.efectos.get("astro")

        if not astro or self._ancho_cielo <= 0:

            return

        visible = 1.0 - min(1.0, self.oscuridad(camara_y + self.alto * 0.5) * 1.5)

        if visible <= 0.02:

            return

        x_cielo = max(0, min(int(camara_x * self._vel_cielo), self._ancho_cielo - self.ancho))

        sx = astro["x"] * PX + PX // 2 - x_cielo

        sy = astro["y"] * PX + PX // 2 - int(camara_y * CAPAS[0][2])

        if astro["tipo"] == "sol":

            pulso = 0.93 + 0.07 * math.sin(tiempo * 1.3)

            for radio, color, cuanto in SOL_BRILLO:

                self._sumar_luz(pantalla, sx, sy, radio, color, cuanto * pulso * visible)

            # reflejos de lente: sobre la recta del sol al centro de la pantalla
            if -60 < sx < self.ancho + 60 and -60 < sy < self.alto + 60:

                cx = self.ancho / 2.0

                cy = self.alto / 2.0

                for fraccion, radio, color, cuanto in REFLEJOS_LENTE:

                    disco = self._disco_pixelado(radio, color, cuanto * visible)

                    pantalla.blit(
                        disco,
                        (
                            int(sx + (cx - sx) * fraccion) - disco.get_width() // 2,
                            int(sy + (cy - sy) * fraccion) - disco.get_height() // 2
                        ),
                        special_flags=pygame.BLEND_RGB_ADD
                    )

        else:

            for radio, color, cuanto in LUNA_BRILLO:

                self._sumar_luz(pantalla, sx, sy, radio, color, cuanto * visible)


    # ------------------------------------------------------
    # DIBUJAR TODO
    # ------------------------------------------------------

    def dibujar(self, pantalla, camara_x, camara_y=0):

        camara_x = int(camara_x)

        camara_y = int(camara_y)

        if not self.listo:

            self._dibujar_simple(pantalla, camara_x, camara_y)

            self._dibujar_oscuridad(pantalla, camara_y)

            self._dibujar_nubes(pantalla, camara_x, camara_y)

            return

        tiempo = pygame.time.get_ticks() / 1000.0

        for imagen, velocidad, fila, vel_y, nombre in self.capas:

            x = int(camara_x * velocidad)

            x = max(0, min(x, imagen.get_width() - self.ancho))

            oy = -int(camara_y * vel_y)

            if imagen is self.cielo:

                # Si la imagen no llega a tapar la pantalla (subiendo o
                # bajando mucho) se estira el primer y el ultimo color
                if oy > 0:

                    pantalla.fill(imagen.get_at((0, 0)), (0, 0, self.ancho, oy))

                bajo = oy + imagen.get_height()

                if bajo < self.alto:

                    pantalla.fill(
                        imagen.get_at((0, imagen.get_height() - 1)),
                        (0, bajo, self.ancho, self.alto - bajo)
                    )

            if imagen is self.ciudad:

                # Antes de la ciudad: la oscuridad y las estrellas (que van
                # detras de los edificios)
                self._dibujar_oscuridad(pantalla, camara_y)

                self._dibujar_estrellas(pantalla, camara_x, camara_y)

            pantalla.blit(
                imagen,
                (0, oy + fila),
                (x, fila, self.ancho, imagen.get_height() - fila)
            )

            # luces animadas de esta capa (las de adelante las tapan)
            self._luces(self._dibujar_efectos_capa, pantalla, nombre, x, oy, tiempo)

        self._dibujar_nubes(pantalla, camara_x, camara_y)

        self._luces(self._dibujar_astro, pantalla, camara_x, camara_y, tiempo)


    def _dibujar_simple(self, pantalla, camara_x, camara_y=0):
        """El fondo de reserva, por si faltan las imagenes."""

        pantalla.fill(self.color_cielo)

        # Con techos: edificios grises con la forma de cada techo
        if self.terreno is not None:

            for e in self.terreno.edificios:

                if e.x1 < camara_x or e.x0 > camara_x + self.ancho:
                    continue

                gris = 150 - 18 * e.tier

                pygame.draw.rect(
                    pantalla,
                    (gris, gris, gris + 10),
                    (
                        e.x0 - camara_x,
                        e.y - camara_y,
                        e.x1 - e.x0,
                        self.terreno.calle_y - e.y
                    )
                )

                pygame.draw.rect(
                    pantalla,
                    (230, 230, 235),
                    (e.x0 - camara_x, e.y - camara_y, e.x1 - e.x0, 4)
                )

            for b in self.terreno.balcones:

                pygame.draw.rect(
                    pantalla,
                    (90, 70, 60),
                    (b.x0 - camara_x, b.y - camara_y, b.x1 - b.x0, 12)
                )

            # La calle y las escaleras
            pygame.draw.rect(
                pantalla,
                (70, 70, 76),
                (
                    0,
                    self.terreno.calle_y - camara_y,
                    self.ancho,
                    max(0, self.alto - (self.terreno.calle_y - camara_y))
                )
            )

            for esc in self.terreno.escaleras:

                pygame.draw.rect(
                    pantalla,
                    (170, 120, 60),
                    (
                        esc.x0 - camara_x,
                        esc.y_alto - camara_y,
                        esc.x1 - esc.x0,
                        esc.y_bajo - esc.y_alto
                    ),
                    3
                )

            return

        pygame.draw.rect(
            pantalla,
            self.color_suelo,
            (
                -camara_x,
                self.suelo_y,
                self.nivel_ancho,
                self.alto - self.suelo_y
            )
        )

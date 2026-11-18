import math
import os
import random
import sys

import pygame

import transicion
import sonidos
import cheats
import musica

from pixel_font import FuentePixel

from archivos import (
    cargar_puntos,
    guardar_puntos,
    cargar_bebidas,
    guardar_bebida,
    reiniciar_progreso,
    completar_nivel,
    cargar_vidas_extra,
    gastar_vida_extra,
    es_jefe,
    es_interior
)


from fondos_nivel import FondoNivel

from terreno import (
    Terreno,
    CALLE_Y,
    LIMITE_PLANO,
    TECHOS,
    VELOCIDAD_ESCALERA
)


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

ANCHO, ALTO = 800, 600

# Cada nivel mide el triple que antes (3200 x 3). Los items y los enemigos
# estan repartidos en consecuencia.
NIVEL_ANCHO = 9600

CELESTE = (135, 206, 235)
ROJO = (220, 20, 60)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (46, 204, 113)
VERDE_SUELO = (34, 139, 34)
DORADO = (255, 215, 0)

FPS = 60

TAM = 50

GRAVEDAD = 2880

SALTO_FUERZA = -960

VELOCIDAD_MOV = 420

SUELO_Y = ALTO - 60

META_X = NIVEL_ANCHO - 100

VIDAS_INICIALES = 3

# ----------------------------------------------------------
# GAGAMBAS (los bichos que caminan de un lado a otro)
# ----------------------------------------------------------

# Aparecen en los niveles 1 a 7. Del 8 en adelante ya no salen.
NIVEL_ULTIMO_GAGAMBA = 7

# Cuantos como maximo por nivel (se reparten por los techos)
GAGAMBAS_POR_NIVEL = 15

# ----------------------------------------------------------
# PELOTAS DE FUTBOL (enemigos que vienen volando desde la derecha)
# ----------------------------------------------------------

# Solo aparecen despues de este nivel (del 8 en adelante)
NIVEL_PELOTAS = 7

# 1.25 veces la velocidad del personaje
VELOCIDAD_PELOTA = VELOCIDAD_MOV * 1.25

ESCALA_PELOTA = 4

# Cada cuantos segundos sale una pelota (al azar entre los dos valores)
ESPERA_PELOTA_MIN = 1.5
ESPERA_PELOTA_MAX = 5.0

# Altura maxima que alcanza un salto: v^2 / (2 * g)
SALTO_MAXIMO = SALTO_FUERZA ** 2 / (2 * GRAVEDAD)

# Cuanto gira por segundo (grados)
GIRO_PELOTA = 900

# Pelota pisada: se cae y desaparece titilando
ESPERA_PELOTA_CAIDA = 0.45

TITILEO_PELOTA = 0.06


# ----------------------------------------------------------
# HINCHAS LANZADORES (enemigos que tiran botellas de Quilmes)
# ----------------------------------------------------------

# Aparecen desde este nivel (inclusive)
NIVEL_LANZADORES = 5

# Lugares donde pueden estar parados dentro de cada tercio del nivel (los
# gagambas estan en 500, 1100, 1700, 2300 y 2850 + 3200 y 6400). Nivel 5:
# 2 hinchas por tercio, cada nivel siguiente suma uno mas por tercio,
# hasta 4. Como el nivel mide el triple (9600), se repiten en los 3 tercios.
POSICIONES_LANZADORES = [800, 1400, 2000, 2600]

LARGO_TERCIO_NIVEL = 3200

ESCALA_LANZADOR = 2

# Fila de arriba del sprite (40x40) que esta vacia
RECORTE_LANZADOR = 8

ANCHO_HITBOX_LANZADOR = 44

# Patrulla: va y viene alrededor de su lugar
RANGO_LANZADOR = 90
VELOCIDAD_LANZADOR = 70
TIEMPO_PASO_LANZADOR = 0.14

# Si el jugador esta a menos de esta distancia (en x), tira
ALCANCE_LANZADOR = 460

# Segundos que dura cada pose del lanzamiento
TIEMPO_POSE_1 = 0.30
TIEMPO_POSE_2 = 0.25
TIEMPO_POSE_3 = 0.20
TIEMPO_PAUSA_LANZADOR = 0.35

# Segundos entre una botella y la siguiente (al azar)
ESPERA_LANZADOR_MIN = 1.8
ESPERA_LANZADOR_MAX = 3.0

# Botella de Quilmes
ESCALA_BOTELLA = 2
GRAVEDAD_BOTELLA = 1500
GIRO_BOTELLA = 540


# ----------------------------------------------------------
# FANTASMA (del nivel 10 en adelante; no en las arenas de jefe)
#
# Entra por la derecha volando hacia el jugador, a la altura de su cuerpo y
# un poquito levantado del piso: agacharse NO sirve, hay que saltar por
# encima. Si te toca no te saca vida, pero durante 2 segundos desaparece
# todo menos el mapa y los bordes de la pantalla se ponen grises.
# ----------------------------------------------------------

NIVEL_FANTASMA_DESDE = 10
NIVEL_FANTASMA_HASTA = 30

# Los dibujos son de 32 x 32: se agrandan al doble
ESCALA_FANTASMA = 2

VELOCIDAD_FANTASMA = 340

# Cada cuantos segundos sale un fantasma (al azar entre los dos valores)
ESPERA_FANTASMA_MIN = 3.0
ESPERA_FANTASMA_MAX = 6.0

# Segundos que dura cada cuadro de la animacion
TIEMPO_CUADRO_FANTASMA = 0.16

# Altura del borde de abajo del fantasma sobre el piso (en pixeles). Cada
# fantasma sale a una altura al azar entre estos dos valores y ademas flota
# subiendo y bajando FANTASMA_FLOTE. Se limita (ver crear_fantasma) para que
# siempre quede mas abajo que la cabeza del personaje agachado.
FANTASMA_ALTURA_MIN = 14
FANTASMA_ALTURA_MAX = 24
FANTASMA_FLOTE = 8
FANTASMA_PERIODO_FLOTE = 1.5

# Cuanto tiene que meterse el fantasma por debajo de la cabeza del personaje
# agachado, para que agacharse no alcance
FANTASMA_MARGEN_AGACHADO = 12

# Sombra en el piso: mas grande y mas oscura cuanto mas bajo vuela, mas chica
# y mas clara cuanto mas alto. Pegado al piso mide FANTASMA_SOMBRA_MAX veces el
# ancho del fantasma y a FANTASMA_SOMBRA_ALTURA_MIN pixeles (o mas) de altura
# ya mide FANTASMA_SOMBRA_MIN veces.
FANTASMA_SOMBRA_MAX = 1.30
FANTASMA_SOMBRA_MIN = 0.35
FANTASMA_SOMBRA_ALTURA_MIN = 45

# Efecto al tocarlo
DURACION_EFECTO_FANTASMA = 2.0

GRIS_BORDE_FANTASMA = (128, 128, 128)
GROSOR_BORDE_FANTASMA = 26            # banda gris solida
DEGRADE_BORDE_FANTASMA = 80           # despues se va aclarando hacia adentro

# Segundos que tardan en aparecer / desaparecer los bordes grises
ENTRADA_BORDE_FANTASMA = 0.12
SALIDA_BORDE_FANTASMA = 0.25

# ----------------------------------------------------------
# ENEMIGOS Y BEBIDAS POR PISO
#
#   calle  -> los enemigos mas flojos: gagambas (niveles 1 a 7) o hinchas
#   techos -> los de siempre (gagambas, hinchas, pelotas y fantasmas)
#   cielo  -> los mas fuertes: pelotas en todos los niveles y fantasmas
#             (del nivel 10 en adelante) el doble de seguido
# ----------------------------------------------------------

GAGAMBAS_CALLE = 8

# Hinchas en la calle (del nivel 8 en adelante, cuando ya no hay gagambas)
HINCHAS_CALLE_MIN = 3
HINCHAS_CALLE_MAX = 5

# En el cielo las pelotas salen mas seguido
ESPERA_PELOTA_CIELO_MIN = 1.0
ESPERA_PELOTA_CIELO_MAX = 3.0

# Y los fantasmas tambien
ESPERA_FANTASMA_CIELO_MIN = 1.5
ESPERA_FANTASMA_CIELO_MAX = 3.0

# (tipo, altura del centro sobre el piso). Las alturas altas obligan a saltar.
ITEMS_CALLE = [
    ("guinness", 45),
    ("guinness", 45),
    ("heineken", 45),
    ("guinness", 140),
    ("guinness", 45),
    ("heineken", 140),
]

# El cielo es opcional pero da premios: mas vidas que en los otros pisos
ITEMS_CIELO = [
    ("guinness", 50),
    ("heineken", 50),
    ("guinness", 50),
    ("heineken", 50),
    ("guinness", 50),
    ("heineken", 50),
]

# ----------------------------------------------------------
# CAMARA VERTICAL
#
# El nivel tiene tres pisos apilados: la calle (abajo), los techos (en el
# medio) y el cielo con sus nubes (arriba). La camara sube y baja suave segun
# el piso donde esta parado el jugador, sin moverse cuando salta.
# ----------------------------------------------------------

# Altura en pantalla de los pies cuando esta parado en la calle (igual que
# en los techos: asi el jugador se ve siempre a la misma altura)
PIES_CALLE_PANTALLA = 480

# Altura en pantalla de los pies cuando esta parado en una nube
PIES_NUBE_PANTALLA = 300

# Que tan rapido se acomoda la camara (1/segundos)
SUAVIZADO_CAMARA = 8.0

# Los pies nunca se salen de esta franja de la pantalla
PIES_MIN_PANTALLA = 90
PIES_MAX_PANTALLA = 560

# Cayendo mas rapido que esto la camara se adelanta para ver donde se cae
VELOCIDAD_CAIDA_CAMARA = 500
PIES_CAIDA_PANTALLA = 380

CARPETA = os.path.dirname(os.path.abspath(__file__))

VERDE_TEXTO = (80, 255, 120)


# ==========================================================
# ITEMS (HEINEKEN = +1 VIDA, GUINNESS = +500 PUNTOS)
# ==========================================================

ESCALA_ITEM = 3

# Subida y bajada tipo item de Minecraft
ITEM_AMPLITUD = 9          # pixeles que sube y baja
ITEM_PERIODO = 1.6         # segundos por ciclo completo

# Tiempo que titila en blanco el personaje al recoger un item
DURACION_PARPADEO = 2.0
VELOCIDAD_PARPADEO = 0.1   # segundos por cambio blanco / normal

PUNTOS_GUINNESS = 500

# (tipo, x, altura sobre el suelo del centro del item)
# Las alturas altas (mas de ~110) obligan a saltar.
POSICIONES_ITEMS = [
    # primer tercio (los de siempre)
    ("guinness", 300, 45),
    ("heineken", 820, 160),
    ("guinness", 1400, 45),
    ("heineken", 1900, 140),
    ("guinness", 2100, 170),
    ("guinness", 2600, 45),
    ("heineken", 3000, 45),

    # segundo tercio
    ("guinness", 3500, 45),
    ("heineken", 4100, 140),
    ("guinness", 4600, 170),
    ("heineken", 5100, 160),
    ("guinness", 5300, 45),
    ("guinness", 5800, 170),
    ("heineken", 6200, 45),

    # tercer tercio
    ("guinness", 6700, 45),
    ("heineken", 7300, 160),
    ("guinness", 7800, 45),
    ("heineken", 8300, 140),
    ("guinness", 8600, 170),
    ("guinness", 9000, 45),
    ("heineken", 9400, 45),
]


# ==========================================================
# JUGADOR
# ==========================================================

class Jugador:

    def __init__(self, sprites, terreno=None):

        self.sprites = sprites

        # Techos y balcones donde se camina (ver terreno.py). Sin terreno
        # (el tutorial) hay un solo piso plano en SUELO_Y.
        self.terreno = terreno

        ancho = sprites["ancho"]
        alto = sprites["alto"]

        # El techo (o piso) donde esta parado. Cuando salta o se cae sigue
        # valiendo el ultimo donde estuvo: las pelotas y los fantasmas
        # vuelan a la altura de ese techo.
        # El nivel arranca en la calle. Si el terreno no tiene calle (datos
        # viejos) se arranca en el primer techo.
        if terreno is not None and terreno.tiene_calle:

            self.apoyo_y = terreno.calle_y

        elif terreno is not None:

            self.apoyo_y = terreno.techo_en(100 + ancho // 2)

        else:

            self.apoyo_y = SUELO_Y

        # Posición inicial (casi siempre x = 100; el nivel 2 arranca en la
        # puerta del Huergo)
        self.rect = pygame.Rect(
            terreno.inicio_x if terreno is not None else 100,
            self.apoyo_y - alto,
            ancho,
            alto
        )

        # ==================================================
        # MÁSCARA INICIAL
        # ==================================================

        self.mask = pygame.mask.from_surface(
            sprites["idle_der"]
        )

        self.vel_y = 0

        self.en_suelo = True

        self.agachado = False

        # True = derecha
        # False = izquierda
        self.mirando_derecha = True

        self.moviendose = False

        self.frame_caminata = 0

        self.tiempo_animacion = 0

        # Segundos que le quedan al titileo blanco (items)
        self.tiempo_parpadeo = 0.0

        # Escalera de mano que esta trepando (o None) y su altura con decimales
        self.escalera = None

        self.altura_escalera = 0.0

        # Segundos hasta poder volver a agarrar una escalera (al soltarse)
        self.espera_escalera = 0.0

        # True hasta soltar las teclas de salto (al terminar de trepar no
        # sale saltando por seguir apretando arriba)
        self.bloquear_salto = False


    # ======================================================
    # TITILEO BLANCO (AL RECOGER UN ITEM)
    # ======================================================

    def iniciar_parpadeo(self):

        self.tiempo_parpadeo = DURACION_PARPADEO


    def actualizar_parpadeo(self, dt):

        if self.tiempo_parpadeo > 0:

            self.tiempo_parpadeo = max(
                0.0,
                self.tiempo_parpadeo - dt
            )


    def esta_en_blanco(self):

        if self.tiempo_parpadeo <= 0:

            return False

        transcurrido = (
            DURACION_PARPADEO
            - self.tiempo_parpadeo
        )

        # Alterna blanco / normal cada VELOCIDAD_PARPADEO
        return int(
            transcurrido / VELOCIDAD_PARPADEO
        ) % 2 == 0


    # ======================================================
    # OBTENER SPRITE ACTUAL
    # ======================================================

    def obtener_sprite_actual(self):

        # --------------------------------------------------
        # AGACHADO
        # --------------------------------------------------

        if self.agachado:

            if self.mirando_derecha:

                return self.sprites["agachado_der"]

            else:

                return self.sprites["agachado_izq"]


        # --------------------------------------------------
        # SALTO
        # --------------------------------------------------

        elif not self.en_suelo:

            if self.mirando_derecha:

                return self.sprites["saltar_der"]

            else:

                return self.sprites["saltar_izq"]


        # --------------------------------------------------
        # QUIETO
        # --------------------------------------------------

        elif not self.moviendose:

            if self.mirando_derecha:

                return self.sprites["idle_der"]

            else:

                return self.sprites["idle_izq"]


        # --------------------------------------------------
        # CAMINANDO
        # --------------------------------------------------

        else:

            if self.mirando_derecha:

                direccion = "caminar_der"

            else:

                direccion = "caminar_izq"

            return self.sprites[direccion][
                self.frame_caminata
            ]


    # ======================================================
    # ACTUALIZAR MÁSCARA
    # ======================================================

    def actualizar_mask(self):

        sprite = self.obtener_sprite_actual()

        self.mask = pygame.mask.from_surface(
            sprite
        )


    # ======================================================
    # MOVER JUGADOR
    # ======================================================

    # ======================================================
    # ESCALERAS DE MANO
    #
    #   - En la calle: arriba (W / flecha) cerca de una escalera la agarra.
    #   - En el techo, arriba de la escalera: abajo (S / flecha) la agarra.
    #   - Trepando: arriba y abajo se mueve; ESPACIO salta hacia afuera.
    #   - Al llegar al techo o a la calle se suelta sola.
    # ======================================================

    def _agarrar_escalera(self, esc):

        self.escalera = esc

        self.altura_escalera = float(self.rect.bottom)

        self.vel_y = 0

        self.en_suelo = True

        # Se para derecho (si estaba agachado)
        if self.agachado:

            piso = self.rect.bottom

            self.rect.height = self.sprites["alto"]

            self.rect.bottom = piso

            self.agachado = False

        self.rect.centerx = int(esc.x)

        self.bloquear_salto = True


    def _soltar_escalera(self, en_suelo, piso=None):

        if piso is not None:

            self.rect.bottom = int(piso)

            self.apoyo_y = piso

        self.escalera = None

        self.moviendose = False

        self.en_suelo = en_suelo

        self.vel_y = 0


    def _buscar_escalera(self, teclas):
        """Si hay que agarrar una escalera ahora, la agarra."""

        if self.espera_escalera > 0:

            return

        esc = self.terreno.escalera_cerca(self.rect.centerx)

        if esc is None:

            return

        arriba = teclas[pygame.K_UP] or teclas[pygame.K_w]

        abajo = teclas[pygame.K_DOWN] or teclas[pygame.K_s]

        bottom = self.rect.bottom

        if self.en_suelo:

            # Parado en la calle: arriba
            if arriba and bottom >= esc.y_bajo - 1:

                self._agarrar_escalera(esc)

            # Parado en el techo, justo arriba de la escalera: abajo
            elif abajo and abs(bottom - esc.y_alto) <= 1:

                self._agarrar_escalera(esc)

        # En el aire (saltando de la escalera, por ejemplo): se vuelve a
        # agarrar si esta a la altura de la escalera
        elif (arriba or abajo) and esc.y_alto + 20 < bottom < esc.y_bajo - 4:

            self._agarrar_escalera(esc)


    def _mover_en_escalera(self, teclas, dt):

        esc = self.escalera

        arriba = teclas[pygame.K_UP] or teclas[pygame.K_w]

        abajo = teclas[pygame.K_DOWN] or teclas[pygame.K_s]

        # ESPACIO: salta hacia afuera (suelta la escalera). Si la escalera
        # sube por delante de un edificio alto no se puede (se saldria del
        # cuerpo del edificio): hay que seguir trepando.
        if (
            teclas[pygame.K_SPACE]
            and not self.terreno.dentro_de_edificio(esc.x, self.rect.bottom - 2)
        ):

            self.escalera = None

            self.espera_escalera = 0.3

            self.vel_y = SALTO_FUERZA

            self.en_suelo = False

            self.moviendose = False

            sonidos.reproducir("salto")

            return

        direccion = 0

        if arriba and not abajo:

            direccion = -1

        elif abajo and not arriba:

            direccion = 1

        self.altura_escalera += direccion * VELOCIDAD_ESCALERA * dt

        self.rect.centerx = int(esc.x)

        self.moviendose = direccion != 0

        # Camina mientras trepa
        if self.moviendose:

            self.tiempo_animacion += dt

            if self.tiempo_animacion >= 0.1:

                self.tiempo_animacion -= 0.1

                self.frame_caminata = (self.frame_caminata + 1) % 3

        else:

            self.frame_caminata = 0

            self.tiempo_animacion = 0

        # Llego arriba: al techo
        if self.altura_escalera <= esc.y_alto:

            self.espera_escalera = 0.2

            self._soltar_escalera(True, esc.y_alto)

            self.bloquear_salto = True

            return

        # Llego abajo: a la calle
        if self.altura_escalera >= esc.y_bajo:

            self.espera_escalera = 0.2

            self._soltar_escalera(True, esc.y_bajo)

            self.bloquear_salto = True

            return

        self.rect.bottom = round(self.altura_escalera)

        # La camara y los enemigos siguen la altura a la que esta
        self.apoyo_y = self.rect.bottom


    def mover(self, teclas, dt):

        se_mueve = False

        x_antes = self.rect.x

        bottom_antes = self.rect.bottom

        self.espera_escalera = max(0.0, self.espera_escalera - dt)

        # --------------------------------------------------
        # ESCALERAS DE MANO
        # --------------------------------------------------

        if self.terreno is not None and self.terreno.escaleras:

            if self.escalera is None:

                self._buscar_escalera(teclas)

            if self.escalera is not None:

                self._mover_en_escalera(teclas, dt)

                self.actualizar_mask()

                return


        # ==================================================
        # AGACHARSE
        # ==================================================

        agachar = (
            teclas[pygame.K_DOWN]
            or teclas[pygame.K_s]
        ) and self.en_suelo

        if agachar != self.agachado:

            piso = self.rect.bottom

            if agachar:

                self.rect.height = (
                    self.sprites["alto_agachado"]
                )

            else:

                self.rect.height = (
                    self.sprites["alto"]
                )

            self.rect.bottom = piso

            self.agachado = agachar


        # ==================================================
        # MOVIMIENTO
        # ==================================================

        if not self.agachado:

            # ----------------------------------------------
            # IZQUIERDA
            # ----------------------------------------------

            if (
                teclas[pygame.K_LEFT]
                or teclas[pygame.K_a]
            ):

                self.rect.x -= (
                    VELOCIDAD_MOV * dt
                )

                # Mira hacia la izquierda
                self.mirando_derecha = False

                se_mueve = True


            # ----------------------------------------------
            # DERECHA
            # ----------------------------------------------

            if (
                teclas[pygame.K_RIGHT]
                or teclas[pygame.K_d]
            ):

                self.rect.x += (
                    VELOCIDAD_MOV * dt
                )

                # Mira hacia la derecha
                self.mirando_derecha = True

                se_mueve = True


        self.moviendose = se_mueve


        # ==================================================
        # ANIMACIÓN DE CAMINATA
        # ==================================================

        if se_mueve:

            self.tiempo_animacion += dt

            if self.tiempo_animacion >= 0.1:

                self.tiempo_animacion -= 0.1

                self.frame_caminata = (
                    self.frame_caminata + 1
                ) % 3

        else:

            self.frame_caminata = 0

            self.tiempo_animacion = 0


        # ==================================================
        # LÍMITES DEL NIVEL
        # ==================================================

        self.rect.left = max(
            0,
            self.rect.left
        )

        self.rect.right = min(
            self.terreno.ancho if self.terreno is not None else NIVEL_ANCHO,
            self.rect.right
        )


        # ==================================================
        # PAREDES DE LOS EDIFICIOS (solidas de costado)
        # ==================================================

        if self.terreno is not None:

            self.rect.x = self.terreno.resolver_x(
                self.rect,
                x_antes
            )


        # ==================================================
        # SALTO
        # ==================================================

        subir = teclas[pygame.K_UP] or teclas[pygame.K_w]

        # Despues de trepar, arriba no salta hasta soltar la tecla
        if not subir:

            self.bloquear_salto = False

        quiere_saltar = (
            teclas[pygame.K_SPACE]
            or (subir and not self.bloquear_salto)
        )

        if (
            quiere_saltar
            and self.en_suelo
            and not self.agachado
        ):

            self.vel_y = SALTO_FUERZA

            self.en_suelo = False

            sonidos.reproducir("salto")


        # ==================================================
        # GRAVEDAD
        # ==================================================

        self.vel_y += GRAVEDAD * dt

        self.rect.y += self.vel_y * dt


        # ==================================================
        # SUELO (el techo o balcon donde cae)
        # ==================================================

        if self.terreno is None:

            if self.rect.bottom >= SUELO_Y:

                self.rect.bottom = SUELO_Y

                self.vel_y = 0

                self.en_suelo = True

        else:

            apoyo = self.terreno.apoyo(
                self.rect.left,
                self.rect.right,
                bottom_antes,
                self.rect.bottom,
                self.vel_y
            )

            if apoyo is not None:

                self.rect.bottom = apoyo

                self.apoyo_y = apoyo

                self.vel_y = 0

                self.en_suelo = True

            else:

                # Sin nada abajo: esta en el aire (se cae de un borde)
                self.en_suelo = False


        # ==================================================
        # ACTUALIZAR MÁSCARA
        # ==================================================

        self.actualizar_mask()


    # ======================================================
    # DIBUJAR JUGADOR
    # ======================================================

    def dibujar(self, superficie, camara_x, camara_y=0):

        # --------------------------------------------------
        # AGACHADO
        # --------------------------------------------------

        if self.agachado:

            if self.mirando_derecha:

                sprite = self.sprites[
                    "agachado_der"
                ]

            else:

                sprite = self.sprites[
                    "agachado_izq"
                ]


        # --------------------------------------------------
        # SALTANDO
        # --------------------------------------------------

        elif not self.en_suelo:

            if self.mirando_derecha:

                sprite = self.sprites[
                    "saltar_der"
                ]

            else:

                sprite = self.sprites[
                    "saltar_izq"
                ]


        # --------------------------------------------------
        # QUIETO
        # --------------------------------------------------

        elif not self.moviendose:

            if self.mirando_derecha:

                sprite = self.sprites[
                    "idle_der"
                ]

            else:

                sprite = self.sprites[
                    "idle_izq"
                ]


        # --------------------------------------------------
        # CAMINANDO
        # --------------------------------------------------

        else:

            if self.mirando_derecha:

                direccion = "caminar_der"

            else:

                direccion = "caminar_izq"

            sprite = self.sprites[
                direccion
            ][self.frame_caminata]


        # --------------------------------------------------
        # TITILEO BLANCO
        # --------------------------------------------------

        if self.esta_en_blanco():

            sprite = silueta_blanca(sprite)


        # --------------------------------------------------
        # POSICIÓN DEL SPRITE
        # --------------------------------------------------

        destino = sprite.get_rect(
            midbottom=self.rect.move(
                -camara_x,
                -camara_y
            ).midbottom
        )


        # --------------------------------------------------
        # DIBUJAR
        # --------------------------------------------------

        superficie.blit(
            sprite,
            destino
        )


# ==========================================================
# SILUETA BLANCA (mismo dibujo, todo pintado de blanco)
# ==========================================================

_cache_siluetas = {}


def silueta_blanca(sprite):

    clave = id(sprite)

    if clave not in _cache_siluetas:

        _cache_siluetas[clave] = (
            pygame.mask.from_surface(sprite).to_surface(
                setcolor=(255, 255, 255, 255),
                unsetcolor=(0, 0, 0, 0)
            ),
            sprite
        )

    return _cache_siluetas[clave][0]


# ==========================================================
# TEXTO FLOTANTE (+1, +500)
# ==========================================================

class TextoFlotante:

    def __init__(self, texto, x, y, fuente, color, duracion=1.1):

        self.imagen = fuente.render(texto, True, color)

        self.sombra = fuente.render(texto, True, NEGRO)

        self.x = x

        self.y = y

        self.duracion = duracion

        self.tiempo = 0.0


    def actualizar(self, dt):

        self.tiempo += dt

        # Sube mientras dura
        self.y -= 55 * dt

        return self.tiempo < self.duracion


    def dibujar(self, superficie, camara_x, camara_y=0):

        # Se desvanece en el ultimo tramo
        restante = self.duracion - self.tiempo

        alfa = int(255 * max(0.0, min(1.0, restante / 0.35)))

        for imagen, desfase in (
            (self.sombra, 2),
            (self.imagen, 0)
        ):

            copia = imagen.copy()

            copia.set_alpha(alfa)

            rect = copia.get_rect(
                midbottom=(
                    int(self.x - camara_x) + desfase,
                    int(self.y - camara_y) + desfase
                )
            )

            superficie.blit(copia, rect)


# ==========================================================
# ITEM RECOGIBLE (HEINEKEN / GUINNESS)
# ==========================================================

class Item:

    def __init__(
        self,
        tipo,
        x,
        altura,
        sprite,
        nivel=1,
        suelo_y=SUELO_Y,
        id_x=None
    ):

        self.tipo = tipo

        # Id unico (se guarda en bebidas.txt al recogerlo). Lleva el
        # numero de nivel: cada nivel del mapa tiene sus propias bebidas.
        # `id_x` es la posicion de la plantilla (POSICIONES_ITEMS): el id
        # no cambia aunque el item se corra para quedar sobre un techo.
        self.id = "n" + str(nivel) + "_" + tipo + "_" + str(
            x if id_x is None else id_x
        )

        self.sprite = sprite

        self.x = x

        # y del techo (o piso) donde esta el item
        self.suelo_y = suelo_y

        # Altura base (centro del item) sobre el suelo
        self.altura = altura

        self.tiempo = (x % 7) * 0.23   # que no suban todos a la vez

        self.recogido = False

        self.rect = pygame.Rect(
            0,
            0,
            sprite.get_width(),
            sprite.get_height()
        )

        self.actualizar(0)


    def _oscilacion(self):

        # 0 = abajo del todo, 1 = arriba del todo (suave)
        fase = 2 * math.pi * self.tiempo / ITEM_PERIODO

        return (math.sin(fase) + 1) / 2


    def actualizar(self, dt):

        self.tiempo += dt

        centro_y = (
            self.suelo_y
            - self.altura
            - self._oscilacion() * ITEM_AMPLITUD * 2
        )

        self.rect.center = (
            int(self.x),
            int(centro_y)
        )


    def dibujar(self, superficie, camara_x, camara_y=0):

        # --------------------------------------------------
        # SOMBRA EN EL SUELO (mas chica y clara cuando sube)
        # --------------------------------------------------

        altura_real = self.suelo_y - self.rect.bottom

        distancia = max(0, altura_real)

        factor = max(0.45, 1.0 - distancia / 320)

        ancho = int(self.sprite.get_width() * 0.95 * factor)

        alto = max(4, int(ancho * 0.30))

        sombra = pygame.Surface(
            (ancho, alto),
            pygame.SRCALPHA
        )

        pygame.draw.ellipse(
            sombra,
            (0, 0, 0, int(105 * factor)),
            sombra.get_rect()
        )

        superficie.blit(
            sombra,
            sombra.get_rect(
                center=(
                    int(self.x - camara_x),
                    int(self.suelo_y + 7 - camara_y)
                )
            )
        )

        # --------------------------------------------------
        # ITEM
        # --------------------------------------------------

        superficie.blit(
            self.sprite,
            self.rect.move(-camara_x, -camara_y)
        )


_sprites_items = {}


def cargar_sprites_items():

    if not _sprites_items:

        for tipo, archivo in (
            ("heineken", "heineken.png"),
            ("guinness", "guiness.png")
        ):

            original = pygame.image.load(
                os.path.join(
                    CARPETA,
                    "assets",
                    "items",
                    archivo
                )
            ).convert_alpha()

            _sprites_items[tipo] = pygame.transform.scale(
                original,
                (
                    original.get_width() * ESCALA_ITEM,
                    original.get_height() * ESCALA_ITEM
                )
            )

    return _sprites_items


def crear_items(nivel=1, terreno=None):

    # Las arenas de jefe estan vacias: sin bebidas
    if es_jefe(nivel):

        return []

    sprites = cargar_sprites_items()

    # Adentro del Huergo no hay techos ni cielo: solo las bebidas del piso
    interior = terreno is not None and terreno.interior

    # Las bebidas que ya se recogieron en una partida anterior
    # (bebidas.txt) no vuelven a aparecer
    recogidas = cargar_bebidas()

    if interior:

        lugares = []

    # Sin terreno (piso plano): las posiciones de siempre
    elif terreno is None:

        lugares = [
            (tipo, x, altura, SUELO_Y, x)
            for tipo, x, altura in POSICIONES_ITEMS
        ]

    # Con techos: cada item se corre al techo que le toca (ver
    # Terreno.posiciones_items). El id sigue siendo el de la plantilla.
    else:

        lugares = [
            (tipo, nx, naltura, techo, x)
            for (tipo, x, _), (_, nx, naltura, techo)
            in zip(
                POSICIONES_ITEMS,
                terreno.posiciones_items(POSICIONES_ITEMS)
            )
        ]

    # La calle y el cielo tienen sus propias bebidas (ids "c0", "s0", ...)
    if terreno is not None and terreno.tiene_calle:

        for i, (tipo, x, altura, y) in enumerate(
            terreno.posiciones_items_calle(ITEMS_CALLE)
        ):

            lugares.append((tipo, x, altura, y, "c" + str(i)))

        for i, tipo, x, altura, y in terreno.posiciones_items_cielo(
            random, ITEMS_CIELO
        ):

            lugares.append((tipo, x, altura, y, "s" + str(i)))

    return [
        Item(tipo, x, altura, sprites[tipo], nivel, techo, id_x)
        for tipo, x, altura, techo, id_x in lugares
        if ("n" + str(nivel) + "_" + tipo + "_" + str(id_x)) not in recogidas
    ]


# ==========================================================
# ENEMIGO
# ==========================================================

# ==========================================================
# SOMBRA EN EL SUELO DE LOS ENEMIGOS
#
# Ovalo negro transparente (el mismo estilo que el de los items)
# pegado a los pies. Se dibuja ANTES del sprite para que quede abajo.
# ==========================================================

ALFA_SOMBRA_ENEMIGO = 120

# Cuanto sobresale la sombra por debajo de la linea del piso
BAJADA_SOMBRA_ENEMIGO = 3

_cache_sombras = {}


def dibujar_sombra_suelo(
    superficie,
    centro_x,
    ancho,
    alfa=ALFA_SOMBRA_ENEMIGO,
    suelo_y=SUELO_Y
):
    """Sombra ovalada en el piso (o techo), centrada en centro_x (en pantalla)."""

    ancho = max(8, int(ancho))

    clave = (ancho, alfa)

    if clave not in _cache_sombras:

        alto = max(5, int(ancho * 0.30))

        sombra = pygame.Surface((ancho, alto), pygame.SRCALPHA)

        pygame.draw.ellipse(sombra, (0, 0, 0, alfa), sombra.get_rect())

        _cache_sombras[clave] = sombra

    sombra = _cache_sombras[clave]

    superficie.blit(
        sombra,
        sombra.get_rect(
            center=(int(centro_x), suelo_y + BAJADA_SOMBRA_ENEMIGO)
        )
    )


class Enemigo:

    def __init__(
        self,
        x,
        sprite,
        rango=60,
        velocidad=120,
        suelo_y=SUELO_Y
    ):

        # y del techo (o piso) donde camina
        self.suelo_y = suelo_y

        self.rect = pygame.Rect(
            x,
            suelo_y - TAM,
            TAM,
            TAM
        )

        self.sprite_original = sprite

        self.sprite = sprite

        self.mask = pygame.mask.from_surface(
            self.sprite
        )

        self.x_inicial = x

        self.rango = rango

        self.vel_x = velocidad

        self.aplastado = False

        self.tiempo_aplastado = 0


    def mover(self, dt):

        if self.aplastado:

            return


        self.rect.x += (
            self.vel_x * dt
        )

        if (
            self.rect.x
            <= self.x_inicial - self.rango

            or

            self.rect.x
            >= self.x_inicial + self.rango
        ):

            self.vel_x *= -1


    def aplastar(self):

        if self.aplastado:

            return


        self.aplastado = True

        self.tiempo_aplastado = 0.45

        ancho = 60

        alto = 15

        self.sprite = pygame.transform.scale(
            self.sprite_original,
            (
                ancho,
                alto
            )
        )

        self.rect.width = ancho
        self.rect.height = alto

        self.rect.bottom = self.suelo_y

        self.mask = pygame.mask.from_surface(
            self.sprite
        )


    def actualizar(self, dt):

        if not self.aplastado:

            return True


        self.tiempo_aplastado -= dt

        return self.tiempo_aplastado > 0


    def dibujar(
        self,
        superficie,
        camara_x,
        camara_y=0
    ):

        destino = self.sprite.get_rect(
            midbottom=self.rect.move(
                -camara_x,
                -camara_y
            ).midbottom
        )

        # Sombra primero (aplastado queda una mancha mas finita)
        dibujar_sombra_suelo(
            superficie,
            destino.centerx,
            self.sprite.get_width() * (0.9 if self.aplastado else 1.0),
            ALFA_SOMBRA_ENEMIGO // 2 if self.aplastado else ALFA_SOMBRA_ENEMIGO,
            int(self.suelo_y - camara_y)
        )

        superficie.blit(
            self.sprite,
            destino
        )


# ==========================================================
# CREAR ENEMIGOS
# ==========================================================

def crear_enemigos(sprite, nivel=1, terreno=None, ocupados=None):
    """
    Gagambas del nivel: solo del 1 al 7 (NIVEL_ULTIMO_GAGAMBA). Con techos
    se reparten parejo, uno por techo (hasta GAGAMBAS_POR_NIVEL), sin pisar
    el tramo que usa un hincha (`ocupados`, ver crear_lanzadores).
    """

    if (
        nivel > NIVEL_ULTIMO_GAGAMBA
        or es_jefe(nivel)
        or es_interior(nivel)
    ):

        return []

    if terreno is not None:

        return [
            Enemigo(x, sprite, rango, 120, techo)
            for x, techo, rango in terreno.posiciones_gagambas(
                GAGAMBAS_POR_NIVEL,
                TAM,
                ocupados
            )
        ]

    # Piso plano (por si faltan los datos de los techos): 5 en cada tercio
    # del nivel (el nivel mide el triple que antes)
    posiciones = [
        500,
        1100,
        1700,
        2300,
        2850,

        3700,
        4300,
        4900,
        5500,
        6050,

        6900,
        7500,
        8100,
        8700,
        9250
    ]

    return [
        Enemigo(x, sprite)
        for x in posiciones
    ]


def crear_enemigos_calle(sprite, nivel, terreno):
    """Gagambas de la calle (niveles 1 a 7): los enemigos mas flojos."""

    if (
        nivel > NIVEL_ULTIMO_GAGAMBA
        or es_jefe(nivel)
        or es_interior(nivel)
        or terreno is None
        or not terreno.escaleras
    ):

        return []

    return [
        Enemigo(x, sprite, rango, 120, y)
        for x, y, rango in terreno.posiciones_gagambas_calle(
            GAGAMBAS_CALLE,
            TAM
        )
    ]


# ==========================================================
# PELOTAS DE FUTBOL
#
# Dos dibujos distintos; cada vez que sale una se elige uno al azar.
# Llegan desde la derecha en cualquier momento, a 1.25 veces la velocidad
# del personaje, y a una altura al azar entre el piso (el techo donde esta
# parado el jugador) y lo mas alto que se puede llegar saltando (nunca pasan
# por encima de un salto).
# Si se las toca desde arriba (cayendo sobre ellas) se caen y no pasa
# nada; de costado o desde abajo te sacan una vida.
# ==========================================================

_sprites_pelotas = []


def cargar_sprites_pelotas():

    if not _sprites_pelotas:

        for archivo in ("pelota_1.png", "pelota_2.png"):

            original = pygame.image.load(
                os.path.join(CARPETA, "assets", "enemigos", archivo)
            ).convert_alpha()

            recorte = original.subsurface(
                original.get_bounding_rect()
            ).copy()

            _sprites_pelotas.append(
                pygame.transform.scale(
                    recorte,
                    (
                        recorte.get_width() * ESCALA_PELOTA,
                        recorte.get_height() * ESCALA_PELOTA
                    )
                )
            )

    return _sprites_pelotas


class Pelota:

    def __init__(self, sprite, x, centro_y):

        self.sprite = sprite

        self.mask = pygame.mask.from_surface(sprite)

        self.rect = sprite.get_rect(center=(x, centro_y))

        # Posicion con decimales (el rect solo guarda enteros)
        self.x = float(self.rect.x)

        self.y = float(self.rect.y)

        self.angulo = random.uniform(0, 360)

        self.vel_x = -VELOCIDAD_PELOTA

        self.vel_y = 0.0

        # True cuando la pisaron: ya no lastima a nadie
        self.cayendo = False

        # Segundos que le quedan de titilar una vez que toco el piso
        self.espera_suelo = None


    def tirar(self):
        """El jugador la piso desde arriba: pierde fuerza y se cae."""

        self.cayendo = True

        self.vel_x *= 0.25

        self.vel_y = 0.0


    @property
    def terminada(self):
        """Ya se cayo, titilo y hay que sacarla."""

        return self.espera_suelo is not None and self.espera_suelo <= 0


    def mover(self, dt, terreno=None):

        if not self.cayendo:

            self.x += self.vel_x * dt

            self.rect.x = round(self.x)

            # Rueda hacia la izquierda
            self.angulo = (self.angulo + GIRO_PELOTA * dt) % 360

            return

        # ----- cayendo -----
        self.x += self.vel_x * dt

        base_antes = self.y + self.rect.height

        self.vel_y += GRAVEDAD * dt

        self.y += self.vel_y * dt

        self.angulo = (self.angulo + GIRO_PELOTA * 0.3 * dt) % 360

        # Donde cae: el piso, o el techo (o balcon) que tenga abajo
        if terreno is None:

            suelo = SUELO_Y

        else:

            suelo = terreno.superficie_bajo(
                self.x + self.rect.width / 2,
                base_antes
            )

            # Cayo por un costado de los edificios: no hay nada abajo
            if suelo is None and self.y > CALLE_Y + 200:

                suelo = self.y + self.rect.height

        if suelo is not None and self.y + self.rect.height >= suelo:

            self.y = suelo - self.rect.height

            self.vel_y = 0.0

            self.vel_x = 0.0

            if self.espera_suelo is None:

                self.espera_suelo = ESPERA_PELOTA_CAIDA

        if self.espera_suelo is not None:

            self.espera_suelo -= dt

        self.rect.x = round(self.x)

        self.rect.y = round(self.y)


    def salio_de_pantalla(self, camara_x):

        return self.rect.right < camara_x - 60


    def choca_pared(self, terreno):
        """True si entro en el cuerpo de un edificio (la pared la frena)."""

        return terreno is not None and terreno.choca_pared(self.rect)


    def dibujar(self, superficie, camara_x, camara_y=0):

        # Ya en el piso titila antes de desaparecer
        if (
            self.espera_suelo is not None
            and int(self.espera_suelo / TITILEO_PELOTA) % 2 == 0
        ):

            return

        # El giro se redondea de a 15 grados para que sea parejo
        girada = pygame.transform.rotate(
            self.sprite,
            round(self.angulo / 15) * 15
        )

        superficie.blit(
            girada,
            girada.get_rect(
                center=self.rect.move(-camara_x, -camara_y).center
            )
        )


def crear_pelota(camara_x, jugador, sprites, terreno=None):
    """
    Pelota nueva justo afuera del borde derecho de la pantalla.

    Altura al azar: la mas baja rueda por el techo donde esta el jugador y la
    mas alta es la que todavia toca al jugador en lo mas alto de su salto.
    Si hay un edificio mas alto en el camino (una pared entre el borde de la
    pantalla y el jugador) la pelota tiene que pasar por arriba de su techo;
    si no queda ninguna altura posible, no sale (devuelve None).
    """

    sprite = random.choice(sprites)

    alto = sprite.get_height()

    x_salida = camara_x + ANCHO + 10

    # El techo (o piso) donde esta parado el jugador
    piso = getattr(jugador, "apoyo_y", SUELO_Y)

    # Lo mas bajo que puede ir el borde de abajo de la pelota: el piso del
    # jugador, o el techo mas alto de los edificios que tiene que cruzar
    # (en el cielo no hay edificios en el camino: vuelan mas abajo)
    if terreno is not None and Terreno.zona(piso) != "cielo":

        piso = min(
            piso,
            terreno.techo_minimo(jugador.rect.centerx, x_salida)
        )

    # Cabeza del jugador en lo mas alto del salto
    tope_salto = (
        getattr(jugador, "apoyo_y", SUELO_Y)
        - jugador.sprites["alto"]
        - SALTO_MAXIMO
    )

    # Centro mas alto posible: la pelota queda a la altura de la cabeza
    # del jugador cuando salta lo maximo
    centro_alto = tope_salto + alto / 2

    centro_bajo = piso - alto / 2

    if centro_bajo < centro_alto:

        return None

    return Pelota(
        sprite,
        x_salida,
        random.uniform(centro_alto, centro_bajo)
    )


# ==========================================================
# HINCHAS LANZADORES + BOTELLAS DE QUILMES
#
# El hincha patrulla caminando. Cuando el jugador se acerca se frena,
# lo mira y hace el lanzamiento en 3 poses (la botella aparece en la
# mano, sube, y sale volando en la tercera). La botella sigue un arco
# hacia donde estaba el jugador: se esquiva moviendose o saltando.
#
#   - Pisarlo desde arriba lo aplasta (igual que a un gagamba).
#   - Tocarlo de costado, o que te pegue una botella, saca una vida.
# ==========================================================

_sprites_lanzador = {}


def _cargar_par(carpeta, nombre):
    """Devuelve (mirando a la derecha, mirando a la izquierda)."""

    original = pygame.image.load(
        os.path.join(carpeta, nombre)
    ).convert_alpha()

    recorte = original.subsurface(
        (
            0,
            RECORTE_LANZADOR,
            original.get_width(),
            original.get_height() - RECORTE_LANZADOR
        )
    ).copy()

    der = pygame.transform.scale(
        recorte,
        (
            recorte.get_width() * ESCALA_LANZADOR,
            recorte.get_height() * ESCALA_LANZADOR
        )
    )

    return der, pygame.transform.flip(der, True, False)


def cargar_sprites_lanzador():

    if not _sprites_lanzador:

        carpeta = os.path.join(CARPETA, "assets", "enemigos", "hincha")

        _sprites_lanzador["caminar"] = [
            _cargar_par(carpeta, "caminar_" + str(i) + ".png")
            for i in range(1, 5)
        ]

        _sprites_lanzador["lanzar"] = [
            _cargar_par(carpeta, "lanzar_" + str(i) + ".png")
            for i in range(1, 4)
        ]

        _sprites_lanzador["frente"] = _cargar_par(carpeta, "frente.png")

        botella = pygame.image.load(
            os.path.join(CARPETA, "assets", "enemigos", "quilmes.png")
        ).convert_alpha()

        _sprites_lanzador["botella"] = pygame.transform.scale(
            botella,
            (
                botella.get_width() * ESCALA_BOTELLA,
                botella.get_height() * ESCALA_BOTELLA
            )
        )

    return _sprites_lanzador


class Botella:

    def __init__(self, sprite, x, y, vel_x, vel_y):

        self.sprite = sprite

        self.x = float(x)

        self.y = float(y)

        self.vel_x = vel_x

        self.vel_y = vel_y

        self.angulo = 0.0

        # Giro hacia donde va
        self.giro = -GIRO_BOTELLA if vel_x >= 0 else GIRO_BOTELLA

        # Hitbox un poco mas chica que el dibujo (mas justo)
        lado = int(sprite.get_width() * 0.7)

        self.rect = pygame.Rect(0, 0, lado, lado)

        self.rect.center = (round(self.x), round(self.y))

        self.rota = False

        # Pedacitos de vidrio cuando se rompe
        self.pedazos = []

        self.tiempo_rota = 0.0


    def romper(self):

        if not self.rota:

            sonidos.reproducir("vidrio")

        self.rota = True

        self.tiempo_rota = 0.4

        colores = [
            (99, 194, 201),
            (184, 253, 255),
            (76, 147, 173),
            (255, 255, 255)
        ]

        for _ in range(9):

            self.pedazos.append(
                [
                    self.x,
                    self.y,
                    random.uniform(-220, 220),
                    random.uniform(-380, -120),
                    random.choice(colores)
                ]
            )


    @property
    def terminada(self):

        return self.rota and self.tiempo_rota <= 0


    def mover(self, dt, terreno=None):

        if self.rota:

            self.tiempo_rota -= dt

            for p in self.pedazos:

                p[3] += GRAVEDAD_BOTELLA * dt

                p[0] += p[2] * dt

                p[1] += p[3] * dt

            return

        base_antes = self.rect.bottom

        self.vel_y += GRAVEDAD_BOTELLA * dt

        self.x += self.vel_x * dt

        self.y += self.vel_y * dt

        self.angulo = (self.angulo + self.giro * dt) % 360

        self.rect.center = (round(self.x), round(self.y))

        # Toca el piso (o un techo / balcon): se rompe
        if terreno is None:

            suelo = SUELO_Y

        else:

            suelo = terreno.superficie_bajo(self.x, base_antes)

            # Se estrella contra la pared de un edificio
            if terreno.choca_pared(self.rect):

                self.romper()

                return

        if suelo is not None and self.rect.bottom >= suelo:

            self.y = suelo - self.rect.height / 2

            self.rect.center = (round(self.x), round(self.y))

            self.romper()


    def fuera_del_nivel(self):

        return (
            self.x < -80
            or self.x > NIVEL_ANCHO + 80
            or self.y > CALLE_Y + 200
        )


    def dibujar(self, superficie, camara_x, camara_y=0):

        if self.rota:

            for p in self.pedazos:

                pygame.draw.rect(
                    superficie,
                    p[4],
                    (round(p[0] - camara_x), round(p[1] - camara_y), 6, 6)
                )

            return

        girada = pygame.transform.rotate(
            self.sprite,
            round(self.angulo / 15) * 15
        )

        superficie.blit(
            girada,
            girada.get_rect(
                center=self.rect.move(-camara_x, -camara_y).center
            )
        )


class HinchaLanzador:

    def __init__(self, x, sprites, suelo_y=SUELO_Y, rango=RANGO_LANZADOR):

        self.sprites = sprites

        self.x = float(x)

        self.x_inicial = x

        # y del techo (o piso) donde patrulla y hasta donde camina
        self.suelo_y = suelo_y

        self.rango = rango

        alto = sprites["frente"][0].get_height()

        self.rect = pygame.Rect(0, 0, ANCHO_HITBOX_LANZADOR, alto)

        self.rect.midbottom = (x, suelo_y)

        # En que piso esta (calle, techos o cielo): solo le tira al jugador
        # si esta en el mismo
        self.zona = Terreno.zona(suelo_y)

        # Arranca mirando a la izquierda (el jugador viene de ese lado)
        self.mirando_derecha = False

        self.vel_x = -VELOCIDAD_LANZADOR

        # "patrulla" / "pose1" / "pose2" / "pose3" / "pausa"
        self.estado = "patrulla"

        self.tiempo_estado = 0.0

        self.frame_caminata = 0

        self.tiempo_paso = 0.0

        # Espera antes de poder tirar la primera botella
        self.espera = random.uniform(0.8, ESPERA_LANZADOR_MAX)

        # Cuanto mas tarda en cargar la lata (1 = normal). En el castillo
        # del nivel 30 es mas lento (ver jefes.py)
        self.factor_carga = 1.0

        self.aplastado = False

        self.tiempo_aplastado = 0.0

        self.sprite = self._sprite_actual()

        self.mask = pygame.mask.from_surface(self.sprite)


    # ------------------------------------------------------
    # SPRITE SEGUN LO QUE ESTA HACIENDO
    # ------------------------------------------------------

    def _par(self):

        if self.estado == "pose1":

            return self.sprites["lanzar"][0]

        if self.estado == "pose2":

            return self.sprites["lanzar"][1]

        if self.estado == "pose3":

            return self.sprites["lanzar"][2]

        if self.estado == "pausa":

            return self.sprites["frente"]

        return self.sprites["caminar"][self.frame_caminata]


    def _sprite_actual(self):

        par = self._par()

        return par[0] if self.mirando_derecha else par[1]


    def rect_sprite(self):

        return self.sprite.get_rect(midbottom=self.rect.midbottom)


    # ------------------------------------------------------
    # APLASTAR
    # ------------------------------------------------------

    def aplastar(self):

        if self.aplastado:

            return

        self.aplastado = True

        self.tiempo_aplastado = 0.45

        ancho = self.sprite.get_width()

        alto = 16

        self.sprite = pygame.transform.scale(self.sprite, (ancho, alto))

        self.rect.width = ANCHO_HITBOX_LANZADOR

        self.rect.height = alto

        self.rect.bottom = self.suelo_y

        self.mask = pygame.mask.from_surface(self.sprite)


    # ------------------------------------------------------
    # ACTUALIZAR (devuelve una Botella nueva o None)
    # ------------------------------------------------------

    def actualizar(self, dt, jugador):

        if self.aplastado:

            self.tiempo_aplastado -= dt

            return None

        botella = None

        self.tiempo_estado += dt

        self.espera = max(0.0, self.espera - dt)

        distancia = jugador.rect.centerx - self.rect.centerx

        # ----- patrulla -----
        if self.estado == "patrulla":

            self.x += self.vel_x * dt

            if self.x <= self.x_inicial - self.rango:

                self.vel_x = abs(self.vel_x)

            elif self.x >= self.x_inicial + self.rango:

                self.vel_x = -abs(self.vel_x)

            self.mirando_derecha = self.vel_x > 0

            self.rect.centerx = round(self.x)

            self.tiempo_paso += dt

            if self.tiempo_paso >= TIEMPO_PASO_LANZADOR:

                self.tiempo_paso = 0.0

                self.frame_caminata = (self.frame_caminata + 1) % 4

            # Ve al jugador cerca: se frena y lo mira
            if (
                self.espera <= 0
                and abs(distancia) <= ALCANCE_LANZADOR
                and Terreno.zona(
                    getattr(jugador, "apoyo_y", SUELO_Y)
                ) == self.zona
            ):

                self.estado = "pose1"

                self.tiempo_estado = 0.0

                self.mirando_derecha = distancia > 0

        # ----- lanzamiento -----
        elif self.estado == "pose1":

            if self.tiempo_estado >= TIEMPO_POSE_1 * self.factor_carga:

                self.estado = "pose2"

                self.tiempo_estado = 0.0

        elif self.estado == "pose2":

            if self.tiempo_estado >= TIEMPO_POSE_2 * self.factor_carga:

                self.estado = "pose3"

                self.tiempo_estado = 0.0

                botella = self._lanzar(jugador)

        elif self.estado == "pose3":

            if self.tiempo_estado >= TIEMPO_POSE_3:

                self.estado = "pausa"

                self.tiempo_estado = 0.0

        elif self.estado == "pausa":

            if self.tiempo_estado >= TIEMPO_PAUSA_LANZADOR:

                self.estado = "patrulla"

                self.tiempo_estado = 0.0

                self.espera = random.uniform(
                    ESPERA_LANZADOR_MIN,
                    ESPERA_LANZADOR_MAX
                ) * self.factor_carga

                # Sigue caminando para donde estaba mirando
                self.vel_x = (
                    VELOCIDAD_LANZADOR
                    if self.mirando_derecha
                    else -VELOCIDAD_LANZADOR
                )

        self.sprite = self._sprite_actual()

        self.mask = pygame.mask.from_surface(self.sprite)

        return botella


    # ------------------------------------------------------
    # LANZAR LA BOTELLA EN ARCO HACIA EL JUGADOR
    # ------------------------------------------------------

    def _lanzar(self, jugador):

        direccion = 1 if self.mirando_derecha else -1

        # Sale de la mano
        origen_x = self.rect.centerx + direccion * 40

        origen_y = self.rect.top + 24

        dx = jugador.rect.centerx - origen_x

        dy = jugador.rect.centery - origen_y

        # Tiempo de vuelo: mas lejos = mas tiempo (arco mas alto)
        tiempo = max(0.55, min(abs(dx) / 450.0, 1.15))

        vel_x = dx / tiempo

        vel_y = (dy - 0.5 * GRAVEDAD_BOTELLA * tiempo * tiempo) / tiempo

        return Botella(
            self.sprites["botella"],
            origen_x,
            origen_y,
            vel_x,
            vel_y
        )


    # ------------------------------------------------------
    # DIBUJAR
    # ------------------------------------------------------

    def dibujar(self, superficie, camara_x, camara_y=0):

        destino = self.sprite.get_rect(
            midbottom=self.rect.move(-camara_x, -camara_y).midbottom
        )

        # Sombra en el piso (queda fija aunque cambie la pose: el ancho
        # sale del hitbox, no del dibujo, que se estira al tirar)
        dibujar_sombra_suelo(
            superficie,
            self.rect.centerx - camara_x,
            self.rect.width * (1.1 if self.aplastado else 1.25),
            ALFA_SOMBRA_ENEMIGO // 2 if self.aplastado else ALFA_SOMBRA_ENEMIGO,
            int(self.suelo_y - camara_y)
        )

        superficie.blit(self.sprite, destino)

        # Botella en la mano mientras prepara el tiro
        if self.estado in ("pose1", "pose2") and not self.aplastado:

            direccion = 1 if self.mirando_derecha else -1

            botella = self.sprites["botella"]

            if self.estado == "pose2":

                botella = pygame.transform.rotate(botella, -direccion * 35)

            superficie.blit(
                botella,
                botella.get_rect(
                    center=(
                        self.rect.centerx - camara_x + direccion * 36,
                        self.rect.top - 2 - camara_y
                    )
                )
            )


def crear_lanzadores(nivel, terreno=None):
    """
    Hinchas del nivel: ninguno antes del 5, 2 por tercio en el 5, y uno mas
    por tercio en cada nivel siguiente (hasta 4 por tercio).

    Con techos, cada hincha se para en un techo ancho (el mas cercano al
    lugar de la lista) y patrulla sin salirse. Devuelve (hinchas, ocupados),
    donde `ocupados` dice que tramo de cada techo usa un hincha {edificio:
    (x_desde, x_hasta)}, para que los gagambas no se pongan encima.
    """

    if nivel < NIVEL_LANZADORES or es_jefe(nivel) or es_interior(nivel):

        return [], {}

    por_tercio = min(
        2 + (nivel - NIVEL_LANZADORES),
        len(POSICIONES_LANZADORES)
    )

    sprites = cargar_sprites_lanzador()

    objetivos = [
        x + tercio * LARGO_TERCIO_NIVEL
        for tercio in range(NIVEL_ANCHO // LARGO_TERCIO_NIVEL)
        for x in POSICIONES_LANZADORES[:por_tercio]
    ]

    if terreno is None:

        return [HinchaLanzador(x, sprites) for x in objetivos], {}

    lugares = terreno.posiciones_lanzadores(
        objetivos,
        RANGO_LANZADOR,
        ANCHO_HITBOX_LANZADOR
    )

    # Lo que ocupa cada techo: si hay dos hinchas, se unen sus tramos
    ocupados = {}

    for _, _, indice, (desde, hasta), _ in lugares:

        if indice in ocupados:

            desde = min(desde, ocupados[indice][0])

            hasta = max(hasta, ocupados[indice][1])

        ocupados[indice] = (desde, hasta)

    return (
        [
            HinchaLanzador(x, sprites, techo, rango)
            for x, techo, _, _, rango in lugares
        ],
        ocupados
    )


def crear_lanzadores_calle(nivel, terreno):
    """
    Hinchas de la calle: del nivel 8 en adelante (cuando ya no hay gagambas
    en la calle), entre 3 y 5.
    """

    if (
        nivel <= NIVEL_ULTIMO_GAGAMBA
        or es_jefe(nivel)
        or es_interior(nivel)
        or terreno is None
        or not terreno.escaleras
    ):

        return []

    cantidad = min(
        HINCHAS_CALLE_MIN + (nivel - NIVEL_ULTIMO_GAGAMBA - 1) // 2,
        HINCHAS_CALLE_MAX
    )

    sprites = cargar_sprites_lanzador()

    return [
        HinchaLanzador(x, sprites, y, rango)
        for x, y, _, rango in terreno.posiciones_lanzadores_calle(
            cantidad,
            ANCHO_HITBOX_LANZADOR,
            RANGO_LANZADOR
        )
    ]


def colision_lanzador(jugador, lanzador):

    if not jugador.rect.colliderect(lanzador.rect):

        return False

    caja = lanzador.rect_sprite()

    offset = (
        caja.x - jugador.rect.x,
        caja.y - jugador.rect.y
    )

    return jugador.mask.overlap(lanzador.mask, offset) is not None


def resolver_lanzadores(jugador, lanzadores, bottom_anterior):
    """
    Pisar al hincha desde arriba lo aplasta y el jugador rebota.
    Tocarlo de costado devuelve True (pierde una vida).
    """

    for lanzador in lanzadores:

        if lanzador.aplastado:

            continue

        if not jugador.rect.colliderect(lanzador.rect):

            continue

        esta_cayendo = jugador.vel_y > 0

        viene_desde_arriba = bottom_anterior <= lanzador.rect.top + 18

        esta_cerca = lanzador.rect.top - jugador.rect.bottom <= 18

        if esta_cayendo and viene_desde_arriba and esta_cerca:

            lanzador.aplastar()

            sonidos.reproducir("aplastar")

            jugador.rect.bottom = lanzador.rect.top

            jugador.vel_y = SALTO_FUERZA * 0.55

            jugador.en_suelo = False

            return False

        if colision_lanzador(jugador, lanzador):

            return True

    return False


def resolver_botellas(jugador, botellas):
    """True si una botella en el aire le pega al jugador."""

    for botella in botellas:

        if botella.rota:

            continue

        if not jugador.rect.colliderect(botella.rect):

            continue

        # Mascara del jugador contra la hitbox de la botella
        mascara_botella = pygame.mask.Mask(botella.rect.size, fill=True)

        offset = (
            botella.rect.x - jugador.rect.x,
            botella.rect.y - jugador.rect.y
        )

        if jugador.mask.overlap(mascara_botella, offset) is not None:

            botella.romper()

            return True

    return False



# ==========================================================
# COLISIÓN POR PÍXELES
# ==========================================================

def colision_por_pixeles(
    jugador,
    enemigo
):

    # ------------------------------------------------------
    # PRIMERA COMPROBACIÓN
    # ------------------------------------------------------

    if not jugador.rect.colliderect(
        enemigo.rect
    ):

        return False


    # ------------------------------------------------------
    # CALCULAR OFFSET
    # ------------------------------------------------------

    offset_x = int(
        enemigo.rect.x
        - jugador.rect.x
    )

    offset_y = int(
        enemigo.rect.y
        - jugador.rect.y
    )


    # ------------------------------------------------------
    # COMPROBAR PÍXELES
    # ------------------------------------------------------

    return jugador.mask.overlap(
        enemigo.mask,
        (
            offset_x,
            offset_y
        )
    ) is not None


# ==========================================================
# CHOQUE CON LAS PELOTAS
# ==========================================================

def resolver_pelotas(jugador, pelotas, bottom_anterior):
    """
    Revisa si el jugador toca alguna pelota.

        - Cayendo sobre ella desde arriba: la pelota se cae, el jugador
          rebota y no pasa nada (igual que al aplastar un enemigo).
        - De costado o desde abajo: devuelve True (pierde una vida).
    """

    for pelota in pelotas:

        if pelota.cayendo:

            continue

        if not jugador.rect.colliderect(pelota.rect):

            continue

        esta_cayendo = jugador.vel_y > 0

        viene_desde_arriba = bottom_anterior <= pelota.rect.top + 18

        esta_cerca = pelota.rect.top - jugador.rect.bottom <= 18

        if esta_cayendo and viene_desde_arriba and esta_cerca:

            pelota.tirar()

            sonidos.reproducir("aplastar")

            jugador.rect.bottom = pelota.rect.top

            jugador.vel_y = SALTO_FUERZA * 0.55

            jugador.en_suelo = False

            return False

        if colision_por_pixeles(jugador, pelota):

            return True

    return False


# ==========================================================
# FANTASMA (del nivel 10 en adelante)
#
#   - Vuela de derecha a izquierda, flotando un poco, a la altura del
#     cuerpo del jugador y levantado del piso: agacharse no lo evita, hay
#     que saltar.
#   - No se puede pisar ni sacarle vida a nadie: al tocarte empieza el
#     efecto (ver dibujar_bordes_grises y jugar): 2 segundos con todo
#     invisible menos el mapa.
#   - Tiene sombra en el piso que se achica y se aclara cuanto mas alto
#     esta, y crece y se oscurece cuando baja.
# ==========================================================

_sprites_fantasma = []

# Orden de los 3 cuadros: 1, 2, 3, 2, 1, 2, 3...
CUADROS_FANTASMA = (0, 1, 2, 1)


def cargar_sprites_fantasma():
    """Los 3 cuadros del fantasma, recortados todos igual (asi no saltan)."""

    if not _sprites_fantasma:

        originales = [
            pygame.image.load(
                os.path.join(
                    CARPETA, "assets", "enemigos", "fantasma",
                    "fantasma_" + str(i) + ".png"
                )
            ).convert_alpha()
            for i in (1, 2, 3)
        ]

        # Zona comun: todo lo que se ve en alguno de los 3 cuadros
        zona = originales[0].get_bounding_rect().unionall(
            [o.get_bounding_rect() for o in originales[1:]]
        )

        for original in originales:

            recorte = original.subsurface(zona).copy()

            _sprites_fantasma.append(
                pygame.transform.scale(
                    recorte,
                    (
                        recorte.get_width() * ESCALA_FANTASMA,
                        recorte.get_height() * ESCALA_FANTASMA
                    )
                )
            )

    return _sprites_fantasma


def dibujar_sombra_fantasma(
    superficie,
    centro_x,
    ancho,
    altura,
    suelo_y=SUELO_Y
):
    """
    Sombra del fantasma en el piso (o el techo que tiene abajo). `altura` son
    los pixeles que hay entre ese piso y el borde de abajo del fantasma:
    cuanto mas alto, mas chica y mas clara.
    """

    # 0.0 pegado al piso -> 1.0 muy arriba
    arriba = max(0.0, min(1.0, altura / FANTASMA_SOMBRA_ALTURA_MIN))

    escala = (
        FANTASMA_SOMBRA_MAX
        - arriba * (FANTASMA_SOMBRA_MAX - FANTASMA_SOMBRA_MIN)
    )

    alfa = ALFA_SOMBRA_ENEMIGO * (1.0 - 0.6 * arriba)

    # Se redondea (ancho de a 2 px, alfa de a 5) para no llenar la memoria
    # con una sombra distinta por cada pixel de altura
    dibujar_sombra_suelo(
        superficie,
        centro_x,
        round(ancho * escala / 2) * 2,
        round(alfa / 5) * 5,
        suelo_y
    )


# Cuanto sube o baja por segundo para seguir al techo donde esta el jugador
# (si el jugador cambio de techo mientras el fantasma cruzaba la pantalla)
VELOCIDAD_SEGUIR_FANTASMA = 220

# Deja de seguir cuando ya esta tan cerca del jugador (en x)
DISTANCIA_FIJA_FANTASMA = 120


class Fantasma:

    def __init__(self, sprites, x, altura_base, base_y=SUELO_Y):

        self.sprites = sprites

        self.masks = [pygame.mask.from_surface(s) for s in sprites]

        self.rect = sprites[0].get_rect()

        # Posicion con decimales (el rect solo guarda enteros)
        self.x = float(x)

        # y del techo (o piso) sobre el que vuela, y altura del borde de
        # abajo sobre el, sin contar el flote
        self.base_y = float(base_y)

        self.altura_base = altura_base

        self.altura = altura_base

        # Cada fantasma empieza en un punto distinto del subir y bajar
        self.fase = random.uniform(0, 2 * math.pi)

        self.tiempo = 0.0

        # True cuando ya te toco: no vuelve a empezar el efecto
        self.usado = False

        self.mover(0.0)


    @property
    def cuadro(self):

        return CUADROS_FANTASMA[
            int(self.tiempo / TIEMPO_CUADRO_FANTASMA)
            % len(CUADROS_FANTASMA)
        ]


    @property
    def mask(self):

        return self.masks[self.cuadro]


    def mover(self, dt, jugador=None):

        self.tiempo += dt

        self.x -= VELOCIDAD_FANTASMA * dt

        # Si el jugador paso a otro techo, el fantasma va subiendo o
        # bajando hacia el (hasta quedar cerca: ahi ya no cambia, asi se
        # puede esquivar)
        if (
            jugador is not None
            and self.x > jugador.rect.right + DISTANCIA_FIJA_FANTASMA
        ):

            destino = getattr(jugador, "apoyo_y", self.base_y)

            paso = VELOCIDAD_SEGUIR_FANTASMA * dt

            self.base_y += max(-paso, min(paso, destino - self.base_y))

        self.altura = self.altura_base + FANTASMA_FLOTE * math.sin(
            2 * math.pi * self.tiempo / FANTASMA_PERIODO_FLOTE + self.fase
        )

        self.rect.x = round(self.x)

        self.rect.bottom = round(self.base_y - self.altura)


    def salio_de_pantalla(self, camara_x):

        return self.rect.right < camara_x - 60


    def dibujar(self, superficie, camara_x, terreno=None, camara_y=0):

        destino = self.rect.move(-camara_x, -camara_y)

        # La sombra cae en el techo (o balcon) que tiene abajo. Si esta
        # metido adentro de un edificio (los fantasmas atraviesan las
        # paredes) no hay sombra.
        if terreno is None:

            suelo = SUELO_Y

        else:

            suelo = terreno.superficie_bajo(
                self.rect.centerx,
                self.rect.bottom
            )

        if suelo is not None and suelo - self.rect.bottom <= 260:

            dibujar_sombra_fantasma(
                superficie,
                destino.centerx,
                destino.width,
                suelo - self.rect.bottom,
                int(suelo - camara_y)
            )

        superficie.blit(
            self.sprites[self.cuadro],
            destino
        )


def crear_fantasma(camara_x, jugador, sprites):
    """
    Fantasma nuevo justo afuera del borde derecho de la pantalla.

    La altura es al azar pero siempre baja: el borde de abajo (incluso
    cuando flota lo mas arriba posible) queda mas abajo que la cabeza del
    personaje agachado, asi que agacharse no lo esquiva. Y el de arriba
    queda mucho mas abajo que lo mas alto del salto, asi que saltando si.
    """

    agachado = jugador.sprites["agachado_der"]

    # Altura de la cabeza del personaje agachado sobre el piso
    cabeza_agachado = agachado.get_height() - agachado.get_bounding_rect().top

    tope = (
        cabeza_agachado
        - FANTASMA_MARGEN_AGACHADO
        - FANTASMA_FLOTE
    )

    altura_max = max(FANTASMA_ALTURA_MIN, min(FANTASMA_ALTURA_MAX, tope))

    return Fantasma(
        sprites,
        camara_x + ANCHO + 10,
        random.uniform(FANTASMA_ALTURA_MIN, altura_max),
        getattr(jugador, "apoyo_y", SUELO_Y)
    )


def colision_visible(jugador, fantasma):
    """
    True si el dibujo del jugador (tal cual se ve en pantalla, parado,
    agachado o saltando) toca el dibujo del fantasma.
    """

    sprite = jugador.obtener_sprite_actual()

    # El sprite se dibuja centrado abajo del rect del jugador
    destino = sprite.get_rect(midbottom=jugador.rect.midbottom)

    if not destino.colliderect(fantasma.rect):

        return False

    return jugador.mask.overlap(
        fantasma.mask,
        (
            fantasma.rect.x - destino.x,
            fantasma.rect.y - destino.y
        )
    ) is not None


def resolver_fantasmas(jugador, fantasmas):
    """
    Revisa si el jugador toca algun fantasma que todavia no lo toco.

    Devuelve True si hay que empezar el efecto. Un fantasma toca una sola
    vez (queda `usado`): mientras te atraviesa no se repite.
    """

    toco = False

    for fantasma in fantasmas:

        if fantasma.usado:

            continue

        if colision_visible(jugador, fantasma):

            fantasma.usado = True

            toco = True

    return toco


# ==========================================================
# BORDES GRISES (efecto del fantasma)
#
# Marco gris en los 4 bordes de la pantalla: una banda solida que se va
# aclarando hacia adentro. Aparece y desaparece suavemente.
# ==========================================================

_borde_fantasma = None


def _crear_borde_fantasma():

    superficie = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    total = GROSOR_BORDE_FANTASMA + DEGRADE_BORDE_FANTASMA

    for d in range(total):

        if d < GROSOR_BORDE_FANTASMA:

            alfa = 255

        else:

            alfa = int(
                255 * (
                    1.0
                    - (d - GROSOR_BORDE_FANTASMA) / DEGRADE_BORDE_FANTASMA
                )
            )

        # Un anillo de 1 pixel, d pixeles hacia adentro del borde
        pygame.draw.rect(
            superficie,
            GRIS_BORDE_FANTASMA + (alfa,),
            (d, d, ANCHO - 2 * d, ALTO - 2 * d),
            1
        )

    return superficie


def dibujar_bordes_grises(pantalla, restante):
    """`restante`: segundos que le quedan al efecto (de 2.0 a 0)."""

    global _borde_fantasma

    if _borde_fantasma is None:

        _borde_fantasma = _crear_borde_fantasma()

    transcurrido = DURACION_EFECTO_FANTASMA - restante

    visibilidad = max(0.0, min(
        1.0,
        transcurrido / ENTRADA_BORDE_FANTASMA,
        restante / SALIDA_BORDE_FANTASMA
    ))

    _borde_fantasma.set_alpha(int(255 * visibilidad))

    pantalla.blit(_borde_fantasma, (0, 0))


# ==========================================================
# CAMARA VERTICAL
# ==========================================================

def objetivo_camara_y(jugador):
    """
    Hasta donde tiene que subir o bajar la camara (y del mundo que queda
    arriba de la pantalla), segun el piso donde esta parado el jugador:

      - calle: los pies quedan en PIES_CALLE_PANTALLA
      - techos: la camara no se mueve (0)
      - nubes: los pies quedan en PIES_NUBE_PANTALLA

    Saltar no la mueve (se usa el ultimo piso donde estuvo parado), pero si
    se esta cayendo desde muy arriba se adelanta para ver donde se cae.
    """

    apoyo = jugador.apoyo_y

    if apoyo > LIMITE_PLANO:

        objetivo = max(0.0, apoyo - PIES_CALLE_PANTALLA)

    elif apoyo >= TECHOS[2] - 20:

        objetivo = 0.0

    else:

        objetivo = apoyo - PIES_NUBE_PANTALLA

    # Solo si se esta cayendo MAS ABAJO del piso donde estaba (se cayo de un
    # techo o de una nube). En la bajada de un salto comun la camara queda
    # quieta: antes se movia y volvia en cada salto.
    if cayendo_a_otro_piso(jugador):

        objetivo = max(objetivo, jugador.rect.bottom - PIES_CAIDA_PANTALLA)

    return objetivo


def cayendo_a_otro_piso(jugador):
    """True si cae rapido y ya paso mas abajo del ultimo piso que piso."""

    return (
        not jugador.en_suelo
        and jugador.vel_y > VELOCIDAD_CAIDA_CAMARA
        and jugador.rect.bottom > jugador.apoyo_y + 4
    )


def actualizar_camara_y(camara_y, jugador, dt):
    """La camara se acomoda suave hacia el objetivo y no deja los pies fuera."""

    objetivo = objetivo_camara_y(jugador)

    ritmo = SUAVIZADO_CAMARA

    if cayendo_a_otro_piso(jugador):

        ritmo *= 2.5

    camara_y += (objetivo - camara_y) * min(1.0, ritmo * dt)

    bottom = jugador.rect.bottom

    return max(
        bottom - PIES_MAX_PANTALLA,
        min(bottom - PIES_MIN_PANTALLA, camara_y)
    )


# ==========================================================
# ANIMACIÓN DE MUERTE
# ==========================================================

def animacion_muerte(
    pantalla,
    reloj,
    jugador,
    sprites,
    camara_x,
    fondo=None,
    camara_y=0
):

    if jugador.mirando_derecha:

        sprite = sprites["idle_der"]

    else:

        sprite = sprites["idle_izq"]


    x = jugador.rect.centerx - camara_x

    y = jugador.rect.bottom - sprite.get_height() - camara_y

    velocidad_y = -900

    tiempo = 0

    duracion = 1.25


    while tiempo < duracion:

        dt = (
            reloj.tick(FPS)
            / 1000.0
        )

        dt = min(
            dt,
            0.05
        )

        tiempo += dt

        velocidad_y += GRAVEDAD * dt

        y += velocidad_y * dt


        if fondo is not None:

            fondo.dibujar(
                pantalla,
                camara_x,
                camara_y
            )

        else:

            pantalla.fill(
                CELESTE
            )


            pygame.draw.rect(
                pantalla,
                VERDE_SUELO,
                (
                    0,
                    SUELO_Y,
                    ANCHO,
                    ALTO - SUELO_Y
                )
            )


        pantalla.blit(
            sprite,
            (
                int(
                    x - sprite.get_width() / 2
                ),
                int(y)
            )
        )


        pygame.display.flip()


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


# ==========================================================
# PANTALLA DE VIDAS
# ==========================================================

def pantalla_vidas(
    pantalla,
    reloj,
    sprites,
    vidas,
    fuente_media
):

    duracion = 2.0

    tiempo = 0


    if sprites.get("idle_der"):

        sprite = sprites["idle_der"]

    else:

        sprite = sprites["idle_izq"]


    texto_vidas = fuente_media.render(
        "VIDAS: " + str(vidas),
        True,
        BLANCO
    )


    while tiempo < duracion:

        dt = (
            reloj.tick(FPS)
            / 1000.0
        )

        dt = min(
            dt,
            0.05
        )

        tiempo += dt


        pantalla.fill(
            NEGRO
        )


        destino_sprite = sprite.get_rect(
            center=(
                ANCHO // 2 - 100,
                ALTO // 2
            )
        )


        pantalla.blit(
            sprite,
            destino_sprite
        )


        pantalla.blit(
            texto_vidas,
            texto_vidas.get_rect(
                center=(
                    ANCHO // 2 + 120,
                    ALTO // 2
                )
            )
        )


        pygame.display.flip()


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


# ==========================================================
# GAME OVER: "HAS MUERTO" SOBRE EL CEMENTERIO DE CHACARITA
#
# Aparece de golpe (sin fundido de entrada), se queda un momento
# y se va desvaneciendo hasta quedar en negro.
# ==========================================================

ROJO_MUERTE = (225, 15, 15)

GAME_OVER_APARECE_SEG = 1.8     # cuanto se ve entera, de golpe
GAME_OVER_DESVANECE_SEG = 2.6   # cuanto tarda en irse a negro


def _texto_con_borde(fuente, texto, color, color_borde, grosor):
    """Texto pixel art con un borde de 'grosor' pixeles alrededor."""

    interior = fuente.render(texto, True, color)
    borde = fuente.render(texto, True, color_borde)

    w, h = interior.get_size()

    imagen = pygame.Surface(
        (w + grosor * 2, h + grosor * 2),
        pygame.SRCALPHA
    )

    for dx in range(-grosor, grosor + 1):

        for dy in range(-grosor, grosor + 1):

            imagen.blit(borde, (grosor + dx, grosor + dy))

    imagen.blit(interior, (grosor, grosor))

    return imagen


def _crear_escena_game_over(ancho, alto, fuente_media):

    # Fondo: la foto es 16:9 y la ventana 4:3, se ajusta a la altura
    # y se recorta el centro
    foto = pygame.image.load(
        os.path.join(
            CARPETA,
            "assets",
            "fondos",
            "game_over_chacarita.png"
        )
    ).convert()

    factor = alto / foto.get_height()

    foto = pygame.transform.smoothscale(
        foto,
        (round(foto.get_width() * factor), alto)
    )

    escena = pygame.Surface((ancho, alto))

    escena.blit(
        foto,
        ((ancho - foto.get_width()) // 2, 0)
    )

    # Textos
    fuente_titulo = FuentePixel(11)

    titulo = _texto_con_borde(
        fuente_titulo,
        "HAS MUERTO",
        ROJO_MUERTE,
        NEGRO,
        5
    )

    escena.blit(
        titulo,
        titulo.get_rect(center=(ancho // 2, alto // 2 - 40))
    )

    subtitulo = _texto_con_borde(
        fuente_media,
        "Ahora sos parte de Chacarita",
        BLANCO,
        NEGRO,
        3
    )

    escena.blit(
        subtitulo,
        subtitulo.get_rect(center=(ancho // 2, alto // 2 + 60))
    )

    return escena


def pantalla_game_over(pantalla, reloj, fuente_media):

    ancho, alto = pantalla.get_size()

    escena = _crear_escena_game_over(ancho, alto, fuente_media)

    tiempo = 0.0

    total = GAME_OVER_APARECE_SEG + GAME_OVER_DESVANECE_SEG

    while tiempo < total:

        # El primer frame ya se ve completo: aparece de golpe
        if tiempo <= GAME_OVER_APARECE_SEG:

            opacidad = 1.0

        else:

            opacidad = 1.0 - (
                (tiempo - GAME_OVER_APARECE_SEG)
                / GAME_OVER_DESVANECE_SEG
            )

        escena.set_alpha(int(255 * max(0.0, opacidad)))

        pantalla.fill(NEGRO)

        pantalla.blit(escena, (0, 0))

        pygame.display.flip()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

        tiempo += min(reloj.tick(FPS) / 1000.0, 0.05)

    pantalla.fill(NEGRO)

    pygame.display.flip()


# ==========================================================
# AVISO VERDE DEL HUD (+1 VIDA / +500 PUNTOS)
# ==========================================================

def dibujar_aviso(
    pantalla,
    fuente,
    texto,
    x,
    y,
    restante,
    derecha
):

    # restante: 1.0 recien aparecido -> 0.0 desaparece
    alfa = int(255 * max(0.0, min(1.0, restante / 0.3)))

    # Baja un poquito al aparecer
    y += int((1.0 - restante) * 6)

    for color, desfase in (
        (NEGRO, 2),
        (VERDE_TEXTO, 0)
    ):

        imagen = fuente.render(texto, True, color).copy()

        imagen.set_alpha(alfa)

        if derecha:

            rect = imagen.get_rect(
                topright=(x + desfase, y + desfase)
            )

        else:

            rect = imagen.get_rect(
                topleft=(x + desfase, y + desfase)
            )

        pantalla.blit(imagen, rect)


# ==========================================================
# JUGAR
# ==========================================================

# La bandera del final de los niveles (se saco; True para volver a ponerla)
MOSTRAR_BANDERA_META = False


def dibujar_meta(pantalla, terreno, camara_x, camara_y):
    """
    La meta: un mastil dorado con una bandera. Es alto: se ve desde la calle
    y desde los techos.
    """

    meta_x = terreno.meta_x

    x = meta_x - camara_x

    if x < -60 or x > ANCHO + 60:

        return

    base = terreno.calle_y if terreno.escaleras else terreno.techo_en(meta_x)

    punta = terreno.techo_en(meta_x) - 100

    pygame.draw.rect(
        pantalla,
        DORADO,
        (x, punta - camara_y, 15, base - punta)
    )

    # Bandera roja arriba
    pygame.draw.polygon(
        pantalla,
        ROJO,
        [
            (x + 15, punta - camara_y),
            (x + 15 + 46, punta - camara_y + 17),
            (x + 15, punta - camara_y + 34)
        ]
    )

    # Pie del mastil
    pygame.draw.rect(
        pantalla,
        (120, 90, 10),
        (x - 8, base - camara_y - 8, 31, 8)
    )


# ==========================================================
# CARTEL DE DONDE ESTAS (al empezar cada nivel)
# ==========================================================

DURACION_CARTEL_LUGAR = 3.5


def nombre_del_lugar(nivel):
    """("SAN TELMO", "BUENOS AIRES") segun el nivel (sale de mapa.py)."""

    from mapa import NIVELES_BUENOS_AIRES, NIVELES

    if not 1 <= nivel <= len(NIVELES):
        return None, None
    nombre = NIVELES[nivel - 1][0]
    zona = "BUENOS AIRES" if nivel <= len(NIVELES_BUENOS_AIRES) else "CONURBANO BONAERENSE"
    return nombre, zona


def dibujar_cartel_lugar(pantalla, fuente_media, t, titulo, subtitulo=None, y=150):
    """Cartel amarillo (con el texto chico abajo) que aparece y se va."""

    if t >= DURACION_CARTEL_LUGAR or not titulo:
        return
    alfa = int(255 * max(0.0, min(1.0, t / 0.4, (DURACION_CARTEL_LUGAR - t) / 0.6)))
    fuente_chica = type(fuente_media)(2)
    for fuente, texto, yy, color in (
        (fuente_media, titulo, y, (255, 220, 40)),
        (fuente_chica, subtitulo, y + 40, (255, 255, 255)),
    ):
        if not texto:
            continue
        imagen = fuente.render(texto, True, color).copy()
        sombra = fuente.render(texto, True, (0, 0, 0)).copy()
        imagen.set_alpha(alfa)
        sombra.set_alpha(alfa)
        rect = imagen.get_rect(center=(ANCHO // 2, yy))
        for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3)):
            pantalla.blit(sombra, rect.move(dx, dy))
        pantalla.blit(imagen, rect)


def jugar(
    pantalla,
    reloj,
    sprites,
    fuente_grande,
    fuente_media,
    cabeza=None,
    nivel=1
):

    # Niveles de jefe (15 y 30): los maneja jefes.py (el 30 es el castillo
    # de Lord Teichi, con lava y la pelea final)
    if es_jefe(nivel):

        from jefes import jugar_jefe

        return jugar_jefe(
            pantalla,
            reloj,
            sprites,
            fuente_grande,
            fuente_media,
            cabeza,
            nivel
        )

    # Cancion del nivel (de dia o de noche, ver musica.cancion_de_nivel)
    musica.reproducir_cancion(musica.cancion_de_nivel(nivel))

    # Los tres pisos del nivel (ver terreno.py): la calle, los techos de los
    # edificios y, arriba de todo, las nubes del cielo. Las nubes son
    # distintas cada vez que empieza el nivel.
    terreno = Terreno.cargar(nivel)

    terreno.generar_nubes(random.Random())

    jugador = Jugador(
        sprites,
        terreno
    )

    # Hinchas que tiran botellas de Quilmes (del nivel 5 en adelante, en los
    # techos; del 8 en adelante tambien en la calle)
    lanzadores, techos_hinchas = crear_lanzadores(nivel, terreno)

    lanzadores += crear_lanzadores_calle(nivel, terreno)

    # Gagambas: solo en los niveles 1 a 7, en los techos (o tramos de techo)
    # que no usan los hinchas, y en la calle
    enemigos = crear_enemigos(
        sprites["enemigo"],
        nivel,
        terreno,
        techos_hinchas
    )

    enemigos += crear_enemigos_calle(sprites["enemigo"], nivel, terreno)

    # Camara vertical: arranca ya en el piso donde empieza el jugador
    camara_y = objetivo_camara_y(jugador)

    # Las 3 vidas de cada nivel + las que se compraron en la tienda de
    # San Telmo y todavia no se usaron
    vidas = VIDAS_INICIALES + cargar_vidas_extra()

    # Los puntos vienen del archivo: se conservan al salir del juego
    # o volver al menu, y solo se borran al perder todas las vidas.
    puntos = cargar_puntos()

    items = crear_items(nivel, terreno)

    # Fondo pixel art del barrio (cielo, ciudad lejana con sus monumentos,
    # edificios del medio y los techos por donde se camina)
    fondo = FondoNivel(
        nivel,
        ANCHO,
        ALTO,
        SUELO_Y,
        terreno.ancho if terreno.interior else NIVEL_ANCHO,
        CELESTE,
        VERDE_SUELO,
        terreno
    )

    botellas = []

    # Pelotas de futbol (solo del nivel 8 en adelante)
    pelotas = []

    espera_pelota = random.uniform(ESPERA_PELOTA_MIN, ESPERA_PELOTA_MAX)

    # Fantasmas (del nivel 10 en adelante; las arenas de jefe estan vacias)
    hay_fantasmas = (
        NIVEL_FANTASMA_DESDE <= nivel <= NIVEL_FANTASMA_HASTA
        and not es_jefe(nivel)
        and not es_interior(nivel)
    )

    fantasmas = []

    espera_fantasma = random.uniform(
        ESPERA_FANTASMA_MIN,
        ESPERA_FANTASMA_MAX
    )

    # Segundos que le quedan al efecto de un fantasma (0 = sin efecto)
    efecto_fantasma = 0.0

    textos_flotantes = []

    # Segundos que le quedan a los avisos verdes del HUD
    aviso_vida = 0.0

    aviso_puntos = 0.0

    DURACION_AVISO = 1.6

    # En los niveles de noche (o cuando se sube al cielo oscuro) el fondo es
    # oscuro: texto blanco con sombra
    hud_oscuro = fondo.oscuro

    color_hud = BLANCO if hud_oscuro else NEGRO

    def sombra_hud(texto, rect):

        if hud_oscuro:

            pantalla.blit(
                fuente_media.render(texto, True, NEGRO),
                rect.move(2, 2)
            )


    # Cartel de donde estas (como en el castillo de Teichi)
    cartel_lugar, cartel_zona = nombre_del_lugar(nivel)
    tiempo_lugar = 0.0

    while True:

        # ==================================================
        # DELTA TIME
        # ==================================================

        dt = (
            reloj.tick(FPS)
            / 1000.0
        )

        dt = min(
            dt,
            0.05
        )

        tiempo_lugar += dt


        # ==================================================
        # EVENTOS
        # ==================================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if (
                evento.type == pygame.KEYDOWN
                and evento.key == pygame.K_ESCAPE
            ):

                return "menu"

            # F10: menu de trucos (vidas, puntos, saltear niveles)
            if (
                evento.type == pygame.KEYDOWN
                and evento.key == cheats.TECLA
            ):

                truco = cheats.menu_cheats(pantalla, reloj, vidas, nivel)

                vidas = truco["vidas"]

                puntos = truco["puntos"]

                if truco["accion"] == "saltear":

                    cheats.saltear_nivel(nivel)

                    return "mapa_victoria"

                if truco["accion"] is not None:

                    cheats.ir_al_nivel(truco["accion"][1])

                    return "mapa"


        # ==================================================
        # TECLAS
        # ==================================================

        teclas = pygame.key.get_pressed()


        # ==================================================
        # JUGADOR
        # ==================================================

        jugador_bottom_anterior = (
            jugador.rect.bottom
        )

        jugador.mover(
            teclas,
            dt
        )


        # ==================================================
        # ENEMIGOS
        # ==================================================

        for enemigo in enemigos:

            enemigo.mover(
                dt
            )

            enemigo.actualizar(
                dt
            )


        # ==================================================
        # HINCHAS LANZADORES Y BOTELLAS DE QUILMES
        # ==================================================

        for lanzador in lanzadores:

            botella_nueva = lanzador.actualizar(
                dt,
                jugador
            )

            if botella_nueva is not None:

                botellas.append(botella_nueva)

        for botella in botellas:

            botella.mover(dt, terreno)

        botellas = [
            b for b in botellas
            if not b.terminada
            and not b.fuera_del_nivel()
        ]


        # ==================================================
        # PELOTAS DE FUTBOL
        # ==================================================

        # En los techos salen del nivel 8 en adelante; en el cielo, en todos
        # los niveles y mas seguido; en la calle nunca.
        zona = Terreno.zona(jugador.apoyo_y)

        en_cielo = zona == "cielo"

        salen_pelotas = en_cielo or (nivel > NIVEL_PELOTAS and zona == "techos")

        if salen_pelotas or pelotas:

            camara_pelotas = max(
                0,
                min(
                    jugador.rect.centerx - ANCHO // 2,
                    terreno.ancho - ANCHO
                )
            )

            if salen_pelotas:

                espera_pelota -= dt

            if salen_pelotas and espera_pelota <= 0:

                pelota_nueva = crear_pelota(
                    camara_pelotas,
                    jugador,
                    cargar_sprites_pelotas(),
                    terreno
                )

                # Si hay una pared alta en el camino y no queda altura por
                # donde pasar, no sale y se vuelve a intentar enseguida
                if pelota_nueva is not None:

                    pelotas.append(pelota_nueva)

                    if en_cielo:

                        espera_pelota = random.uniform(
                            ESPERA_PELOTA_CIELO_MIN,
                            ESPERA_PELOTA_CIELO_MAX
                        )

                    else:

                        espera_pelota = random.uniform(
                            ESPERA_PELOTA_MIN,
                            ESPERA_PELOTA_MAX
                        )

                else:

                    espera_pelota = 0.5

            for pelota in pelotas:

                pelota.mover(dt, terreno)

            # Se van las que salen de la pantalla, las que ya se cayeron y
            # las que se estrellan contra la pared de un edificio
            pelotas = [
                p for p in pelotas
                if not p.salio_de_pantalla(camara_pelotas)
                and not p.terminada
                and (p.cayendo or not p.choca_pared(terreno))
            ]


        # ==================================================
        # FANTASMAS (del nivel 10 en adelante)
        # ==================================================

        if hay_fantasmas:

            camara_fantasmas = max(
                0,
                min(
                    jugador.rect.centerx - ANCHO // 2,
                    terreno.ancho - ANCHO
                )
            )

            # En la calle no hay fantasmas; en el cielo salen el doble de
            # seguido
            if zona != "calle":

                espera_fantasma -= dt

            if espera_fantasma <= 0 and zona != "calle":

                fantasmas.append(
                    crear_fantasma(
                        camara_fantasmas,
                        jugador,
                        cargar_sprites_fantasma()
                    )
                )

                if en_cielo:

                    espera_fantasma = random.uniform(
                        ESPERA_FANTASMA_CIELO_MIN,
                        ESPERA_FANTASMA_CIELO_MAX
                    )

                else:

                    espera_fantasma = random.uniform(
                        ESPERA_FANTASMA_MIN,
                        ESPERA_FANTASMA_MAX
                    )

            for fantasma in fantasmas:

                fantasma.mover(dt, jugador)

            fantasmas = [
                f for f in fantasmas
                if not f.salio_de_pantalla(camara_fantasmas)
            ]

            efecto_fantasma = max(0.0, efecto_fantasma - dt)

            # Tocar un fantasma no saca vida: empieza el efecto. Si ya
            # estaba en marcha no se reinicia (el fantasma igual queda
            # "usado" para que no empiece de nuevo apenas termine).
            if resolver_fantasmas(jugador, fantasmas):

                if efecto_fantasma <= 0:

                    efecto_fantasma = DURACION_EFECTO_FANTASMA


        # ==================================================
        # COLISIÓN
        # ==================================================

        murio = False


        for enemigo in enemigos:

            if enemigo.aplastado:

                continue


            if not jugador.rect.colliderect(
                enemigo.rect
            ):

                continue


            esta_cayendo = (
                jugador.vel_y > 0
            )


            diferencia_vertical = (
                enemigo.rect.top
                - jugador.rect.bottom
            )


            viene_desde_arriba = (
                jugador_bottom_anterior
                <= enemigo.rect.top + 18
            )


            esta_cerca_del_enemigo = (
                diferencia_vertical <= 18
            )


            if (
                esta_cayendo
                and viene_desde_arriba
                and esta_cerca_del_enemigo
            ):

                enemigo.aplastar()

                sonidos.reproducir("aplastar")

                jugador.rect.bottom = (
                    enemigo.rect.top
                )

                jugador.vel_y = (
                    SALTO_FUERZA * 0.55
                )

                jugador.en_suelo = False

                break


            if colision_por_pixeles(
                jugador,
                enemigo
            ):

                murio = True

                break


        # Hinchas: pisarlos desde arriba los aplasta, de costado
        # te saca una vida. Las botellas tambien.
        if not murio:

            murio = resolver_lanzadores(
                jugador,
                lanzadores,
                jugador_bottom_anterior
            )

        if not murio:

            murio = resolver_botellas(
                jugador,
                botellas
            )

        lanzadores = [
            l for l in lanzadores
            if not (
                l.aplastado
                and l.tiempo_aplastado <= 0
            )
        ]

        # Pelotas: pisarlas desde arriba las tira, tocarlas de costado
        # o desde abajo es perder una vida
        if not murio:

            murio = resolver_pelotas(
                jugador,
                pelotas,
                jugador_bottom_anterior
            )


        # ==================================================
        # ELIMINAR ENEMIGOS APLASTADOS
        # ==================================================

        enemigos = [
            enemigo
            for enemigo in enemigos
            if not (
                enemigo.aplastado
                and enemigo.tiempo_aplastado <= 0
            )
        ]


        # ==================================================
        # MUERTE
        # ==================================================

        if murio:

            # La cancion del nivel se pausa (sigue donde quedo al volver)
            musica.pausar()

            sonidos.reproducir("perder_vida")

            vidas -= 1

            # Si quedaba una vida comprada en la tienda, se gasta esa
            gastar_vida_extra()


            # ----------------------------------------------
            # CÁMARA ACTUAL
            # ----------------------------------------------

            camara_x = max(
                0,
                min(
                    jugador.rect.centerx
                    - ANCHO // 2,

                    terreno.ancho
                    - ANCHO
                )
            )


            # ----------------------------------------------
            # ANIMACIÓN DE MUERTE
            # ----------------------------------------------

            animacion_muerte(
                pantalla,
                reloj,
                jugador,
                sprites,
                camara_x,
                fondo,
                int(round(camara_y))
            )


            # ----------------------------------------------
            # SI NO QUEDAN VIDAS
            # ----------------------------------------------

            if vidas <= 0:

                musica.detener()

                # Sin vidas: recien ahi se borra todo (puntos.txt,
                # personajes.txt y bebidas.txt) y se vuelve a la
                # seleccion de personaje
                reiniciar_progreso()

                pantalla_game_over(
                    pantalla,
                    reloj,
                    fuente_media
                )

                return "personajes"


            # ----------------------------------------------
            # PANTALLA NEGRA
            #
            # Primero se cierra el círculo sobre el jugador (se sigue
            # viendo el nivel), y después se abre en la pantalla de
            # vidas. Al terminar se repite para volver al nivel.
            # ----------------------------------------------

            transicion.cerrar_circulo(
                pantalla,
                reloj,
                (
                    max(0, min(ANCHO, jugador.rect.centerx - camara_x)),
                    max(0, min(ALTO, jugador.rect.centery - int(round(camara_y))))
                )
            )

            transicion.abrir_circulo()

            pantalla_vidas(
                pantalla,
                reloj,
                sprites,
                vidas,
                fuente_media
            )

            transicion.cerrar_circulo(pantalla, reloj)

            transicion.abrir_circulo()

            # Vuelve el nivel: la cancion sigue desde donde se pauso
            musica.reanudar()


            # ----------------------------------------------
            # REINICIAR JUGADOR
            # ----------------------------------------------

            jugador = Jugador(
                sprites,
                terreno
            )


            # ----------------------------------------------
            # REINICIAR TODOS LOS GAGAMBAS
            # ----------------------------------------------

            lanzadores, techos_hinchas = crear_lanzadores(nivel, terreno)

            lanzadores += crear_lanzadores_calle(nivel, terreno)

            enemigos = crear_enemigos(
                sprites["enemigo"],
                nivel,
                terreno,
                techos_hinchas
            )

            enemigos += crear_enemigos_calle(sprites["enemigo"], nivel, terreno)

            camara_y = objetivo_camara_y(jugador)

            botellas = []

            pelotas = []

            espera_pelota = random.uniform(
                ESPERA_PELOTA_MIN,
                ESPERA_PELOTA_MAX
            )

            # Sin fantasmas y sin efecto al volver a empezar
            fantasmas = []

            efecto_fantasma = 0.0

            espera_fantasma = random.uniform(
                ESPERA_FANTASMA_MIN,
                ESPERA_FANTASMA_MAX
            )

            continue


        # ==================================================
        # ITEMS: HEINEKEN (+1 VIDA) / GUINNESS (+500 PUNTOS)
        # ==================================================

        jugador.actualizar_parpadeo(dt)

        for item in items:

            item.actualizar(dt)

            if item.recogido:

                continue

            if not jugador.rect.colliderect(item.rect):

                continue

            item.recogido = True

            # Queda anotada en bebidas.txt: no se puede volver a recoger
            guardar_bebida(item.id)

            jugador.iniciar_parpadeo()

            if item.tipo == "heineken":

                sonidos.reproducir("cerveza")

                vidas += 1

                aviso_vida = DURACION_AVISO

                texto_item = "+1"

            else:

                sonidos.reproducir("cerveza")

                puntos += PUNTOS_GUINNESS

                guardar_puntos(puntos)

                aviso_puntos = DURACION_AVISO

                texto_item = "+" + str(PUNTOS_GUINNESS)

            textos_flotantes.append(
                TextoFlotante(
                    texto_item,
                    item.rect.centerx,
                    item.rect.top,
                    fuente_media,
                    VERDE_TEXTO
                )
            )

        items = [i for i in items if not i.recogido]

        textos_flotantes = [
            t for t in textos_flotantes
            if t.actualizar(dt)
        ]

        aviso_vida = max(0.0, aviso_vida - dt)

        aviso_puntos = max(0.0, aviso_puntos - dt)


        # ==================================================
        # META
        # ==================================================

        if jugador.rect.x >= terreno.meta_x:

            # Nivel terminado: queda anotado y se vuelve al mapa, donde
            # el punto se vuelve negro y aparece el camino al siguiente
            completar_nivel(nivel)

            sonidos.reproducir("nivel_completo")

            return "mapa_victoria"


        # ==================================================
        # CÁMARA
        # ==================================================

        camara_x = max(
            0,
            min(
                jugador.rect.centerx
                - ANCHO // 2,

                terreno.ancho
                - ANCHO
            )
        )


        # Camara vertical (se acomoda suave segun el piso donde esta parado)
        camara_y = actualizar_camara_y(camara_y, jugador, dt)

        cam_y = int(round(camara_y))


        # ==================================================
        # FONDO
        # ==================================================

        # Cielo con parallax (cada vez mas negro cuanto mas arriba) + ciudad
        # (monumentos, calle y techos) + las nubes
        fondo.dibujar(
            pantalla,
            camara_x,
            cam_y
        )


        # ==================================================
        # META
        # ==================================================

        # (La bandera de la meta ya no se dibuja: el nivel termina igual al
        # llegar al final. Solo el tutorial tiene bandera.)
        if MOSTRAR_BANDERA_META:

            dibujar_meta(pantalla, terreno, camara_x, cam_y)


        # ==================================================
        # EFECTO DEL FANTASMA
        #
        # Durante 2 segundos no se dibuja nada mas que el mapa (el fondo
        # y la meta): ni jugador, ni items, ni enemigos, ni botellas, ni
        # pelotas, ni fantasmas, ni el HUD. El juego sigue corriendo
        # igual por detras. Los bordes de la pantalla quedan grises.
        # ==================================================

        if efecto_fantasma > 0:

            dibujar_bordes_grises(
                pantalla,
                efecto_fantasma
            )

            pygame.display.flip()

            continue


        # ==================================================
        # ITEMS
        # ==================================================

        for item in items:

            item.dibujar(
                pantalla,
                camara_x,
                cam_y
            )


        # ==================================================
        # ENEMIGOS
        # ==================================================

        for enemigo in enemigos:

            enemigo.dibujar(
                pantalla,
                camara_x,
                cam_y
            )

        for lanzador in lanzadores:

            lanzador.dibujar(
                pantalla,
                camara_x,
                cam_y
            )

        for botella in botellas:

            botella.dibujar(
                pantalla,
                camara_x,
                cam_y
            )

        for pelota in pelotas:

            pelota.dibujar(
                pantalla,
                camara_x,
                cam_y
            )


        # ==================================================
        # JUGADOR
        # ==================================================

        jugador.dibujar(
            pantalla,
            camara_x,
            cam_y
        )


        # ==================================================
        # FANTASMAS (arriba del jugador, se ve cuando te atraviesan)
        # ==================================================

        for fantasma in fantasmas:

            fantasma.dibujar(
                pantalla,
                camara_x,
                terreno,
                cam_y
            )


        # ==================================================
        # TEXTOS FLOTANTES (+1 / +500)
        # ==================================================

        for texto in textos_flotantes:

            texto.dibujar(
                pantalla,
                camara_x,
                cam_y
            )


        # ==================================================
        # HUD: CARA DEL PERSONAJE + VIDAS (arriba a la izquierda)
        # ==================================================

        hud_oscuro = fondo.oscuro or fondo.oscuridad(cam_y + 30) > 0.4

        color_hud = BLANCO if hud_oscuro else NEGRO

        texto_vidas = fuente_media.render(
            "VIDAS: " + str(vidas),
            True,
            color_hud
        )

        if cabeza is not None:

            rect_cabeza = cabeza.get_rect(
                topleft=(10, 10)
            )

            pantalla.blit(
                cabeza,
                rect_cabeza
            )

            x_texto = rect_cabeza.right + 12
            y_centro = rect_cabeza.centery

        else:

            x_texto = 10
            y_centro = 10 + texto_vidas.get_height() // 2

        rect_vidas = texto_vidas.get_rect(
            midleft=(
                x_texto,
                y_centro
            )
        )

        sombra_hud("VIDAS: " + str(vidas), rect_vidas)

        pantalla.blit(
            texto_vidas,
            rect_vidas
        )

        # "+1 VIDA" en verde, debajo del contador de vidas
        if aviso_vida > 0:

            dibujar_aviso(
                pantalla,
                fuente_media,
                "+1 VIDA",
                rect_vidas.left,
                rect_vidas.bottom + 8,
                aviso_vida / DURACION_AVISO,
                derecha=False
            )


        # ==================================================
        # HUD: CONTADOR DE PUNTOS (arriba a la derecha)
        # ==================================================

        texto_puntos = fuente_media.render(
            "PUNTOS: " + str(puntos),
            True,
            color_hud
        )

        rect_puntos = texto_puntos.get_rect(
            topright=(
                ANCHO - 12,
                12
            )
        )

        sombra_hud("PUNTOS: " + str(puntos), rect_puntos)

        pantalla.blit(
            texto_puntos,
            rect_puntos
        )

        # "+500 PUNTOS" en verde, debajo del contador de puntos
        if aviso_puntos > 0:

            dibujar_aviso(
                pantalla,
                fuente_media,
                "+" + str(PUNTOS_GUINNESS) + " PUNTOS",
                rect_puntos.right,
                rect_puntos.bottom + 8,
                aviso_puntos / DURACION_AVISO,
                derecha=True
            )


        # ==================================================
        # HUD: NUMERO DE NIVEL (arriba, en el centro)
        # ==================================================

        texto_nivel = fuente_media.render(
            "NIVEL " + str(nivel),
            True,
            color_hud
        )

        rect_nivel = texto_nivel.get_rect(
            midtop=(
                ANCHO // 2,
                12
            )
        )

        sombra_hud("NIVEL " + str(nivel), rect_nivel)

        pantalla.blit(
            texto_nivel,
            rect_nivel
        )


        # Cartel de donde estas
        dibujar_cartel_lugar(pantalla, fuente_media, tiempo_lugar, cartel_lugar, cartel_zona)


        # ==================================================
        # ACTUALIZAR PANTALLA
        # ==================================================

        pygame.display.flip()
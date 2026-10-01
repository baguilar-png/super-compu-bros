import math
import os
import sys

import pygame

from archivos import (
    cargar_puntos,
    guardar_puntos,
    cargar_bebidas,
    guardar_bebida,
    reiniciar_progreso
)


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

ANCHO, ALTO = 800, 600

NIVEL_ANCHO = 3200

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
    ("guinness", 300, 45),
    ("heineken", 820, 160),
    ("guinness", 1400, 45),
    ("heineken", 1900, 140),
    ("guinness", 2100, 170),
    ("guinness", 2600, 45),
    ("heineken", 3000, 45),
]


# ==========================================================
# JUGADOR
# ==========================================================

class Jugador:

    def __init__(self, sprites):

        self.sprites = sprites

        ancho = sprites["ancho"]
        alto = sprites["alto"]

        # Posición inicial
        self.rect = pygame.Rect(
            100,
            SUELO_Y - alto,
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

    def mover(self, teclas, dt):

        se_mueve = False


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
            NIVEL_ANCHO,
            self.rect.right
        )


        # ==================================================
        # SALTO
        # ==================================================

        if (
            teclas[pygame.K_SPACE]
            or teclas[pygame.K_UP]
            or teclas[pygame.K_w]
        ) and self.en_suelo and not self.agachado:

            self.vel_y = SALTO_FUERZA

            self.en_suelo = False


        # ==================================================
        # GRAVEDAD
        # ==================================================

        self.vel_y += GRAVEDAD * dt

        self.rect.y += self.vel_y * dt


        # ==================================================
        # SUELO
        # ==================================================

        if self.rect.bottom >= SUELO_Y:

            self.rect.bottom = SUELO_Y

            self.vel_y = 0

            self.en_suelo = True


        # ==================================================
        # ACTUALIZAR MÁSCARA
        # ==================================================

        self.actualizar_mask()


    # ======================================================
    # DIBUJAR JUGADOR
    # ======================================================

    def dibujar(self, superficie, camara_x):

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
                0
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


    def dibujar(self, superficie, camara_x):

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
                    int(self.y) + desfase
                )
            )

            superficie.blit(copia, rect)


# ==========================================================
# ITEM RECOGIBLE (HEINEKEN / GUINNESS)
# ==========================================================

class Item:

    def __init__(self, tipo, x, altura, sprite):

        self.tipo = tipo

        # Id unico (se guarda en bebidas.txt al recogerlo)
        self.id = tipo + "_" + str(x)

        self.sprite = sprite

        self.x = x

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
            SUELO_Y
            - self.altura
            - self._oscilacion() * ITEM_AMPLITUD * 2
        )

        self.rect.center = (
            int(self.x),
            int(centro_y)
        )


    def dibujar(self, superficie, camara_x):

        # --------------------------------------------------
        # SOMBRA EN EL SUELO (mas chica y clara cuando sube)
        # --------------------------------------------------

        altura_real = SUELO_Y - self.rect.bottom

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
                    SUELO_Y + 7
                )
            )
        )

        # --------------------------------------------------
        # ITEM
        # --------------------------------------------------

        superficie.blit(
            self.sprite,
            self.rect.move(-camara_x, 0)
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


def crear_items():

    sprites = cargar_sprites_items()

    # Las bebidas que ya se recogieron en una partida anterior
    # (bebidas.txt) no vuelven a aparecer
    recogidas = cargar_bebidas()

    return [
        Item(tipo, x, altura, sprites[tipo])
        for tipo, x, altura in POSICIONES_ITEMS
        if (tipo + "_" + str(x)) not in recogidas
    ]


# ==========================================================
# ENEMIGO
# ==========================================================

class Enemigo:

    def __init__(
        self,
        x,
        sprite,
        rango=60,
        velocidad=120
    ):

        self.rect = pygame.Rect(
            x,
            SUELO_Y - TAM,
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

        self.rect.bottom = SUELO_Y

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
        camara_x
    ):

        destino = self.sprite.get_rect(
            midbottom=self.rect.move(
                -camara_x,
                0
            ).midbottom
        )

        superficie.blit(
            self.sprite,
            destino
        )


# ==========================================================
# CREAR ENEMIGOS
# ==========================================================

def crear_enemigos(sprite):

    posiciones = [
        500,
        1100,
        1700,
        2300,
        2850
    ]

    return [
        Enemigo(x, sprite)
        for x in posiciones
    ]


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
# ANIMACIÓN DE MUERTE
# ==========================================================

def animacion_muerte(
    pantalla,
    reloj,
    jugador,
    sprites,
    camara_x
):

    if jugador.mirando_derecha:

        sprite = sprites["idle_der"]

    else:

        sprite = sprites["idle_izq"]


    x = jugador.rect.centerx - camara_x

    y = jugador.rect.bottom - sprite.get_height()

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
# PANTALLA DE VICTORIA
# ==========================================================

def pantalla_victoria(
    pantalla,
    reloj,
    fuente_grande,
    fuente_media
):

    texto = fuente_grande.render(
        "GANASTE!",
        True,
        BLANCO
    )

    sub = fuente_media.render(
        "Presiona ENTER para volver al menu",
        True,
        BLANCO
    )


    while True:

        pantalla.fill(
            VERDE
        )


        pantalla.blit(
            texto,
            texto.get_rect(
                center=(
                    ANCHO // 2,
                    ALTO // 2 - 40
                )
            )
        )


        pantalla.blit(
            sub,
            sub.get_rect(
                center=(
                    ANCHO // 2,
                    ALTO // 2 + 30
                )
            )
        )


        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()


            if (
                evento.type == pygame.KEYDOWN
                and evento.key == pygame.K_RETURN
            ):

                return "menu"


        pygame.display.flip()

        reloj.tick(FPS)


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

def jugar(
    pantalla,
    reloj,
    sprites,
    fuente_grande,
    fuente_media,
    cabeza=None
):

    jugador = Jugador(
        sprites
    )

    enemigos = crear_enemigos(
        sprites["enemigo"]
    )

    vidas = VIDAS_INICIALES

    # Los puntos vienen del archivo: se conservan al salir del juego
    # o volver al menu, y solo se borran al perder todas las vidas.
    puntos = cargar_puntos()

    items = crear_items()

    textos_flotantes = []

    # Segundos que le quedan a los avisos verdes del HUD
    aviso_vida = 0.0

    aviso_puntos = 0.0

    DURACION_AVISO = 1.6


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

            vidas -= 1


            # ----------------------------------------------
            # CÁMARA ACTUAL
            # ----------------------------------------------

            camara_x = max(
                0,
                min(
                    jugador.rect.centerx
                    - ANCHO // 2,

                    NIVEL_ANCHO
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
                camara_x
            )


            # ----------------------------------------------
            # SI NO QUEDAN VIDAS
            # ----------------------------------------------

            if vidas <= 0:

                # Sin vidas: recien ahi se borra todo (puntos.txt,
                # personajes.txt y bebidas.txt) y se vuelve a la
                # seleccion de personaje
                reiniciar_progreso()

                return "personajes"


            # ----------------------------------------------
            # PANTALLA NEGRA
            # ----------------------------------------------

            pantalla_vidas(
                pantalla,
                reloj,
                sprites,
                vidas,
                fuente_media
            )


            # ----------------------------------------------
            # REINICIAR JUGADOR
            # ----------------------------------------------

            jugador = Jugador(
                sprites
            )


            # ----------------------------------------------
            # REINICIAR TODOS LOS GAGAMBAS
            # ----------------------------------------------

            enemigos = crear_enemigos(
                sprites["enemigo"]
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

                vidas += 1

                aviso_vida = DURACION_AVISO

                texto_item = "+1"

            else:

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

        if jugador.rect.x >= META_X:

            return pantalla_victoria(
                pantalla,
                reloj,
                fuente_grande,
                fuente_media
            )


        # ==================================================
        # CÁMARA
        # ==================================================

        camara_x = max(
            0,
            min(
                jugador.rect.centerx
                - ANCHO // 2,

                NIVEL_ANCHO
                - ANCHO
            )
        )


        # ==================================================
        # FONDO
        # ==================================================

        pantalla.fill(
            CELESTE
        )


        # ==================================================
        # SUELO
        # ==================================================

        pygame.draw.rect(
            pantalla,
            VERDE_SUELO,
            (
                -camara_x,
                SUELO_Y,
                NIVEL_ANCHO,
                ALTO - SUELO_Y
            )
        )


        # ==================================================
        # META
        # ==================================================

        pygame.draw.rect(
            pantalla,
            DORADO,
            (
                META_X - camara_x,
                SUELO_Y - 100,
                15,
                100
            )
        )


        # ==================================================
        # ITEMS
        # ==================================================

        for item in items:

            item.dibujar(
                pantalla,
                camara_x
            )


        # ==================================================
        # ENEMIGOS
        # ==================================================

        for enemigo in enemigos:

            enemigo.dibujar(
                pantalla,
                camara_x
            )


        # ==================================================
        # JUGADOR
        # ==================================================

        jugador.dibujar(
            pantalla,
            camara_x
        )


        # ==================================================
        # TEXTOS FLOTANTES (+1 / +500)
        # ==================================================

        for texto in textos_flotantes:

            texto.dibujar(
                pantalla,
                camara_x
            )


        # ==================================================
        # HUD: CARA DEL PERSONAJE + VIDAS (arriba a la izquierda)
        # ==================================================

        texto_vidas = fuente_media.render(
            "VIDAS: " + str(vidas),
            True,
            NEGRO
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
            NEGRO
        )

        rect_puntos = texto_puntos.get_rect(
            topright=(
                ANCHO - 12,
                12
            )
        )

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
        # ACTUALIZAR PANTALLA
        # ==================================================

        pygame.display.flip()
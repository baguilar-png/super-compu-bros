import pygame
import sys


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

        self.sprite = sprite

        # Máscara de píxeles del enemigo
        self.mask = pygame.mask.from_surface(
            sprite
        )

        self.x_inicial = x

        self.rango = rango

        self.vel_x = velocidad


    def mover(self, dt):

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
# JUGAR
# ==========================================================

def jugar(
    pantalla,
    reloj,
    sprites,
    fuente_grande,
    fuente_media
):

    jugador = Jugador(
        sprites
    )

    enemigos = crear_enemigos(
        sprites["enemigo"]
    )


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


        # ==================================================
        # COLISIÓN
        # ==================================================

        if any(
            colision_por_pixeles(
                jugador,
                enemigo
            )
            for enemigo in enemigos
        ):

            jugador = Jugador(
                sprites
            )


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
        # INFORMACIÓN
        # ==================================================

        info = fuente_media.render(
            "ESC: menu | ABAJO/S: agacharse",
            True,
            NEGRO
        )

        pantalla.blit(
            info,
            (10, 10)
        )


        # ==================================================
        # ACTUALIZAR PANTALLA
        # ==================================================

        pygame.display.flip()
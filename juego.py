import pygame
import sys

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


class Jugador:
    def __init__(self, sprites):
        self.sprites = sprites
        ancho = sprites["ancho"]
        alto = sprites["alto"]
        self.rect = pygame.Rect(100, SUELO_Y - alto, ancho, alto)
        self.vel_y = 0
        self.en_suelo = True
        self.agachado = False
        self.mirando_derecha = True
        self.moviendose = False
        self.frame_caminata = 0
        self.tiempo_animacion = 0

    def mover(self, teclas, dt):
        se_mueve = False
        agachar = (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) and self.en_suelo
        if agachar != self.agachado:
            piso = self.rect.bottom
            self.rect.height = self.sprites["alto_agachado"] if agachar else self.sprites["alto"]
            self.rect.bottom = piso
            self.agachado = agachar

        if not self.agachado:
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                self.rect.x -= VELOCIDAD_MOV * dt
                self.mirando_derecha = True
                se_mueve = True
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                self.rect.x += VELOCIDAD_MOV * dt
                self.mirando_derecha = False
                se_mueve = True

        self.moviendose = se_mueve
        if se_mueve:
            self.tiempo_animacion += dt
            if self.tiempo_animacion >= 0.1:
                self.tiempo_animacion -= 0.1
                self.frame_caminata = (self.frame_caminata + 1) % 3
        else:
            self.frame_caminata = 0
            self.tiempo_animacion = 0
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(NIVEL_ANCHO, self.rect.right)

        if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP] or teclas[pygame.K_w]) and self.en_suelo and not self.agachado:
            self.vel_y = SALTO_FUERZA
            self.en_suelo = False

        self.vel_y += GRAVEDAD * dt
        self.rect.y += self.vel_y * dt
        if self.rect.bottom >= SUELO_Y:
            self.rect.bottom = SUELO_Y
            self.vel_y = 0
            self.en_suelo = True

    def dibujar(self, superficie, camara_x):
        if self.agachado:
            sprite = self.sprites["agachado_izq"] if self.mirando_derecha else self.sprites["agachado_der"]
        elif not self.en_suelo:
            sprite = self.sprites["saltar_izq"] if self.mirando_derecha else self.sprites["saltar_der"]
        elif not self.moviendose:
            sprite = self.sprites["idle_der"] if self.mirando_derecha else self.sprites["idle_izq"]
        else:
            direccion = "caminar_der" if self.mirando_derecha else "caminar_izq"
            sprite = self.sprites[direccion][self.frame_caminata]
        destino = sprite.get_rect(midbottom=self.rect.move(-camara_x, 0).midbottom)
        superficie.blit(sprite, destino)


class Enemigo:
    def __init__(self, x, sprite, rango=60, velocidad=120):
        self.rect = pygame.Rect(x, SUELO_Y - TAM, TAM, TAM)
        self.sprite = sprite
        self.x_inicial = x
        self.rango = rango
        self.vel_x = velocidad  # px/seg

    def mover(self, dt):
        self.rect.x += self.vel_x * dt
        if self.rect.x <= self.x_inicial - self.rango or self.rect.x >= self.x_inicial + self.rango:
            self.vel_x *= -1

    def dibujar(self, superficie, camara_x):
        destino = self.sprite.get_rect(midbottom=self.rect.move(-camara_x, 0).midbottom)
        superficie.blit(self.sprite, destino)


def crear_enemigos(sprite):
    posiciones = [500, 1100, 1700, 2300, 2850]
    return [Enemigo(x, sprite) for x in posiciones]


def pantalla_victoria(pantalla, reloj, fuente_grande, fuente_media):
    texto = fuente_grande.render("GANASTE!", True, BLANCO)
    sub = fuente_media.render("Presiona ENTER para volver al menu", True, BLANCO)
    while True:
        pantalla.fill(VERDE)
        pantalla.blit(texto, texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 40)))
        pantalla.blit(sub, sub.get_rect(center=(ANCHO // 2, ALTO // 2 + 30)))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return "menu"

        pygame.display.flip()
        reloj.tick(FPS)


def jugar(pantalla, reloj, sprites, fuente_grande, fuente_media):
    jugador = Jugador(sprites)
    enemigos = crear_enemigos(sprites["enemigo"])

    while True:
        dt = reloj.tick(FPS) / 1000.0
        dt = min(dt, 0.05)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return "menu"

        teclas = pygame.key.get_pressed()
        jugador.mover(teclas, dt)
        for enemigo in enemigos:
            enemigo.mover(dt)

        if any(jugador.rect.colliderect(e.rect) for e in enemigos):
            jugador = Jugador(sprites)

        if jugador.rect.x >= META_X:
            return pantalla_victoria(pantalla, reloj, fuente_grande, fuente_media)

        camara_x = max(0, min(jugador.rect.centerx - ANCHO // 2, NIVEL_ANCHO - ANCHO))

        pantalla.fill(CELESTE)
        pygame.draw.rect(pantalla, VERDE_SUELO, (-camara_x, SUELO_Y, NIVEL_ANCHO, ALTO - SUELO_Y))
        pygame.draw.rect(pantalla, DORADO, (META_X - camara_x, SUELO_Y - 100, 15, 100))

        for enemigo in enemigos:
            enemigo.dibujar(pantalla, camara_x)
        jugador.dibujar(pantalla, camara_x)

        info = fuente_media.render("ESC: menu | ABAJO/S: agacharse", True, NEGRO)
        pantalla.blit(info, (10, 10))

        pygame.display.flip()
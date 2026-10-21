"""
Pantalla de AJUSTES (el engranaje del menu).

Dos barras para subir y bajar el volumen:

    MUSICA    la cancion que suena de fondo (se oye cambiar en el momento)
    EFECTOS   los sonidos (agarrar una cerveza, saltar, pisar enemigos...);
              al soltar la barra suena una Guinness de muestra

Mouse: click o arrastrar sobre la barra, VOLVER para salir.
Teclado: ARRIBA / ABAJO eligen la barra, IZQUIERDA / DERECHA cambian el
volumen (de a 5), ESC o ENTER vuelven.

Lo elegido se guarda en ajustes.txt (ver ajustes.py).
"""

import math
import sys

import pygame

import ajustes
import sonidos


# ==========================================================
# COLORES (los mismos grises que los botones del menu)
# ==========================================================

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
DORADO = (255, 215, 0)

GRIS_BOTON = (180, 180, 180)
GRIS_BOTON_SOMBRA = (163, 163, 163)
GRIS_OSCURO = (70, 70, 70)

PANEL_FONDO = (58, 58, 58)
PANEL_LUZ = (112, 112, 112)
PANEL_SOMBRA = (34, 34, 34)

PISTA_FONDO = (28, 28, 28)

PASO_TECLADO = 5


# ==========================================================
# ENGRANAJE (dibujado pixel por pixel, 15 x 15)
# ==========================================================

N_ENGRANAJE = 15


def _forma_engranaje():
    """Matriz de booleanos: 4 dientes anchos, 4 diagonales y un agujero."""

    c = N_ENGRANAJE // 2

    forma = []

    for y in range(N_ENGRANAJE):

        fila = []

        for x in range(N_ENGRANAJE):

            dx, dy = abs(x - c), abs(y - c)

            r = math.hypot(dx, dy)

            lleno = r <= 5.2

            # dientes de arriba, abajo, izquierda y derecha
            lleno = lleno or (dx <= 1 and dy <= c)
            lleno = lleno or (dy <= 1 and dx <= c)

            # dientes de las diagonales (cuadraditos de 2 x 2)
            lleno = lleno or (4 <= dx <= 5 and 4 <= dy <= 5)

            fila.append(lleno and r > 2.8)

        forma.append(fila)

    return forma


def crear_engranaje(escala=3):
    """
    Devuelve (normal, hover): el engranaje gris con borde oscuro y el mismo
    con el borde blanco (igual que se ponen blancos los botones del menu).

    El borde va por FUERA de la forma (1 pixel de dibujo), asi el cuerpo
    queda todo gris y se lee bien aunque sea chico.
    """

    forma = _forma_engranaje()

    n = N_ENGRANAJE + 2

    def lleno(x, y):

        x -= 1
        y -= 1

        return (
            0 <= x < N_ENGRANAJE
            and 0 <= y < N_ENGRANAJE
            and forma[y][x]
        )

    resultado = []

    for color_borde in (GRIS_OSCURO, BLANCO):

        chico = pygame.Surface((n, n), pygame.SRCALPHA)

        for y in range(n):

            for x in range(n):

                if lleno(x, y):

                    # luz arriba a la izquierda, sombra abajo a la derecha
                    chico.set_at(
                        (x, y),
                        GRIS_BOTON if x + y < n - 1 else GRIS_BOTON_SOMBRA
                    )

                elif (
                    lleno(x - 1, y)
                    or lleno(x + 1, y)
                    or lleno(x, y - 1)
                    or lleno(x, y + 1)
                ):

                    chico.set_at((x, y), color_borde)

        resultado.append(
            pygame.transform.scale(chico, (n * escala, n * escala))
        )

    return tuple(resultado)


# ==========================================================
# BARRA DE VOLUMEN
# ==========================================================

class Barra:

    def __init__(self, nombre, centro_y, rect_pista, leer, fijar, es_efecto):

        self.nombre = nombre

        self.centro_y = centro_y

        self.pista = rect_pista

        self.leer = leer

        self.fijar = fijar

        self.es_efecto = es_efecto

    def zona(self):
        """Donde se puede hacer click (un poco mas grande que la barra)."""

        return self.pista.inflate(30, 34)

    def x_manija(self):

        return self.pista.left + round(self.leer() / 100 * self.pista.width)

    def valor_en(self, x):

        return round((x - self.pista.left) / self.pista.width * 100)

    def dibujar(self, superficie, fuente, activa, hover, foco):

        # Nombre (dorado si es la barra elegida con el teclado)
        color = DORADO if foco else BLANCO

        texto = fuente.render(self.nombre, True, color)

        sombra = fuente.render(self.nombre, True, NEGRO)

        pos = texto.get_rect(midleft=(self.pista.left - 190, self.centro_y))

        superficie.blit(sombra, pos.move(3, 3))
        superficie.blit(texto, pos)

        # Pista: fondo oscuro con borde, y la parte llena en dorado
        pygame.draw.rect(superficie, NEGRO, self.pista.inflate(6, 6))

        pygame.draw.rect(superficie, PISTA_FONDO, self.pista)

        lleno = self.pista.copy()

        lleno.width = self.x_manija() - self.pista.left

        if lleno.width > 0:

            pygame.draw.rect(superficie, DORADO, lleno)

            pygame.draw.rect(
                superficie,
                (255, 240, 150),
                (lleno.left, lleno.top, lleno.width, 3)
            )

        # Manija: bloque gris con borde oscuro (blanco al apuntarla)
        manija = pygame.Rect(0, 0, 16, 34)

        manija.center = (self.x_manija(), self.centro_y)

        borde = BLANCO if (hover or activa) else GRIS_OSCURO

        pygame.draw.rect(superficie, borde, manija)

        pygame.draw.rect(superficie, GRIS_BOTON, manija.inflate(-6, -6))

        pygame.draw.rect(
            superficie,
            GRIS_BOTON_SOMBRA,
            (manija.left + 3, manija.centery, manija.width - 6, manija.height // 2 - 3)
        )

        # Porcentaje a la derecha
        porcentaje = fuente.render("%d%%" % self.leer(), True, color)

        sombra_p = fuente.render("%d%%" % self.leer(), True, NEGRO)

        pos_p = porcentaje.get_rect(midright=(self.pista.right + 100, self.centro_y))

        superficie.blit(sombra_p, pos_p.move(3, 3))
        superficie.blit(porcentaje, pos_p)


# ==========================================================
# LA PANTALLA
# ==========================================================

def abrir(
    pantalla,
    reloj,
    dibujar_fondo,
    fuente_titulo,
    fuente_texto,
    fuente_chica,
    fps=60
):
    """
    Muestra los ajustes encima del fondo del menu hasta que se vuelve.

    dibujar_fondo -> funcion sin argumentos que dibuja el fondo del menu
    """

    ancho, alto = pantalla.get_size()

    sonidos.reproducir("click")

    # Panel
    panel = pygame.Rect(0, 0, 600, 390)

    panel.center = (ancho // 2, alto // 2 - 30)

    # Barras (la pista queda a la derecha del nombre)
    x_pista = panel.left + 250

    ancho_pista = 220

    barras = [
        Barra(
            "MUSICA",
            panel.top + 135,
            pygame.Rect(x_pista, panel.top + 135 - 8, ancho_pista, 16),
            lambda: ajustes.musica,
            ajustes.fijar_musica,
            False
        ),
        Barra(
            "EFECTOS",
            panel.top + 210,
            pygame.Rect(x_pista, panel.top + 210 - 8, ancho_pista, 16),
            lambda: ajustes.efectos,
            ajustes.fijar_efectos,
            True
        ),
    ]

    # El boton VOLVER (mismo estilo que los del menu)
    boton_volver = pygame.Rect(0, 0, 220, 52)

    boton_volver.midtop = (panel.centerx, panel.top + 268)

    foco = 0               # 0 y 1: las barras, 2: el boton VOLVER

    arrastrando = None

    velo = pygame.Surface((ancho, alto), pygame.SRCALPHA)

    velo.fill((0, 0, 0, 150))

    while True:

        mouse = pygame.mouse.get_pos()

        # --------------------------------------------------
        # EVENTOS
        # --------------------------------------------------

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER):

                    sonidos.reproducir("click")

                    return

                if evento.key in (pygame.K_UP, pygame.K_w):

                    foco = (foco - 1) % 3

                if evento.key in (pygame.K_DOWN, pygame.K_s):

                    foco = (foco + 1) % 3

                if foco < 2 and evento.key in (
                    pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d
                ):

                    barra = barras[foco]

                    signo = (
                        -1
                        if evento.key in (pygame.K_LEFT, pygame.K_a)
                        else 1
                    )

                    barra.fijar(barra.leer() + signo * PASO_TECLADO)

                    if barra.es_efecto:

                        sonidos.reproducir("guinness")

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if boton_volver.collidepoint(evento.pos):

                    sonidos.reproducir("click")

                    return

                for i, barra in enumerate(barras):

                    if barra.zona().collidepoint(evento.pos):

                        arrastrando = barra

                        foco = i

                        barra.fijar(barra.valor_en(evento.pos[0]))

            if evento.type == pygame.MOUSEMOTION and arrastrando is not None:

                arrastrando.fijar(arrastrando.valor_en(evento.pos[0]))

            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:

                # Al soltar la barra de efectos suena una muestra
                if arrastrando is not None and arrastrando.es_efecto:

                    sonidos.reproducir("guinness")

                arrastrando = None

        # --------------------------------------------------
        # DIBUJO
        # --------------------------------------------------

        dibujar_fondo()

        pantalla.blit(velo, (0, 0))

        # Panel con borde en relieve
        pygame.draw.rect(pantalla, NEGRO, panel.inflate(8, 8))

        pygame.draw.rect(pantalla, PANEL_FONDO, panel)

        pygame.draw.rect(pantalla, PANEL_LUZ, (panel.left, panel.top, panel.width, 4))
        pygame.draw.rect(pantalla, PANEL_LUZ, (panel.left, panel.top, 4, panel.height))
        pygame.draw.rect(pantalla, PANEL_SOMBRA, (panel.left, panel.bottom - 4, panel.width, 4))
        pygame.draw.rect(pantalla, PANEL_SOMBRA, (panel.right - 4, panel.top, 4, panel.height))

        # Titulo
        titulo = fuente_titulo.render("AJUSTES", True, BLANCO)

        sombra_t = fuente_titulo.render("AJUSTES", True, NEGRO)

        pos_t = titulo.get_rect(midtop=(panel.centerx, panel.top + 22))

        pantalla.blit(sombra_t, pos_t.move(4, 4))
        pantalla.blit(titulo, pos_t)

        # Barras
        for i, barra in enumerate(barras):

            barra.dibujar(
                pantalla,
                fuente_texto,
                arrastrando is barra,
                barra.zona().collidepoint(mouse),
                foco == i
            )

        # Boton VOLVER: al apuntarlo (o elegirlo con el teclado) las
        # letras y el borde se ponen blancos, igual que en el menu
        resaltado = boton_volver.collidepoint(mouse) or foco == 2

        color_borde = BLANCO if resaltado else GRIS_OSCURO

        pygame.draw.rect(pantalla, color_borde, boton_volver)

        pygame.draw.rect(pantalla, GRIS_BOTON, boton_volver.inflate(-8, -8))

        pygame.draw.rect(
            pantalla,
            GRIS_BOTON_SOMBRA,
            (
                boton_volver.left + 4,
                boton_volver.centery + 6,
                boton_volver.width - 8,
                boton_volver.height // 2 - 10
            )
        )

        texto_volver = fuente_texto.render("VOLVER", True, color_borde)

        pantalla.blit(
            texto_volver,
            texto_volver.get_rect(center=boton_volver.center)
        )

        # Pista de teclas
        pista = fuente_chica.render(
            "FLECHAS: CAMBIAR   ESC: VOLVER",
            True,
            (210, 210, 210)
        )

        pantalla.blit(
            pista,
            pista.get_rect(midbottom=(panel.centerx, panel.bottom - 14))
        )

        pygame.display.flip()

        reloj.tick(fps)

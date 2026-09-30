import pygame
import sys
import os

FPS = 60

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS_CLARO = (190, 190, 190)

# Duraciones en segundos
DURACION_APARECER = 1.6   # de negro a la imagen completa
DURACION_MANTENER = 1.6   # imagen quieta
DURACION_DESAPARECER = 1.0  # de la imagen a negro



def _cargar_imagen(nombre):
    """
    Carga una imagen de assets/fondos, la recorta al dibujo (sin el margen
    transparente) y pasa a blanco sus píxeles negros para que se vea sobre
    el fondo negro. Los demás colores (el verde de la S) no se tocan.
    """

    ruta = os.path.join("assets", "fondos", nombre)

    imagen = pygame.image.load(ruta).convert_alpha()
    imagen = imagen.subsurface(imagen.get_bounding_rect()).copy()

    for x in range(imagen.get_width()):
        for y in range(imagen.get_height()):
            r, g, b, a = imagen.get_at((x, y))

            if a > 0 and r < 40 and g < 40 and b < 40:
                imagen.set_at((x, y), (255, 255, 255, a))

    return imagen


def _crear_diapositiva_productores(ancho, alto, fuente_grande, fuente_media):
    """Primera diapositiva: "presentado por..." y debajo el logo de BS Corp."""

    diapositiva = pygame.Surface((ancho, alto))
    diapositiva.fill(NEGRO)

    presentado = _cargar_imagen("presentado_por.png")
    bs_corp = _cargar_imagen("logo_bs.png")

    # Espacio entre las dos imágenes, en píxeles del arte original
    separacion = 5

    alto_total = (
        presentado.get_height() + separacion + bs_corp.get_height()
    )

    # Escala entera para no deformar el pixel art
    escala = max(1, min(
        (ancho * 7 // 10) // max(presentado.get_width(), bs_corp.get_width()),
        (alto * 6 // 10) // alto_total
    ))

    presentado = pygame.transform.scale(
        presentado,
        (presentado.get_width() * escala, presentado.get_height() * escala)
    )

    bs_corp = pygame.transform.scale(
        bs_corp,
        (bs_corp.get_width() * escala, bs_corp.get_height() * escala)
    )

    separacion *= escala

    # Una imagen arriba de la otra, centradas en la pantalla
    y_inicio = (
        alto - (presentado.get_height() + separacion + bs_corp.get_height())
    ) // 2

    diapositiva.blit(
        presentado,
        presentado.get_rect(midtop=(ancho // 2, y_inicio))
    )

    diapositiva.blit(
        bs_corp,
        bs_corp.get_rect(
            midtop=(
                ancho // 2,
                y_inicio + presentado.get_height() + separacion
            )
        )
    )

    return diapositiva


def _crear_diapositiva_logo(ancho, alto, logo):
    """Diapositiva con fondo negro y el logo del juego."""

    diapositiva = pygame.Surface((ancho, alto))
    diapositiva.fill(NEGRO)

    diapositiva.blit(
        logo,
        logo.get_rect(center=(ancho // 2, alto // 2))
    )

    return diapositiva


def _mostrar_diapositiva(pantalla, reloj, diapositiva):
    """
    Muestra una diapositiva: sale del negro, se mantiene y vuelve al negro.
    Devuelve cuando termina o cuando el jugador la saltea
    (ENTER, ESPACIO, ESC o click).
    """

    total = DURACION_APARECER + DURACION_MANTENER + DURACION_DESAPARECER
    tiempo = 0.0

    while tiempo < total:

        dt = reloj.tick(FPS) / 1000.0
        tiempo += dt

        # --------------------------------------------------
        # EVENTOS
        # --------------------------------------------------

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                return

            if evento.type == pygame.KEYDOWN:
                if evento.key in (
                    pygame.K_RETURN,
                    pygame.K_SPACE,
                    pygame.K_ESCAPE
                ):
                    return

        # --------------------------------------------------
        # OPACIDAD SEGÚN LA FASE
        # --------------------------------------------------

        if tiempo < DURACION_APARECER:
            opacidad = tiempo / DURACION_APARECER

        elif tiempo < DURACION_APARECER + DURACION_MANTENER:
            opacidad = 1.0

        else:
            restante = total - tiempo
            opacidad = restante / DURACION_DESAPARECER

        opacidad = max(0.0, min(1.0, opacidad))

        # --------------------------------------------------
        # DIBUJAR
        # --------------------------------------------------

        pantalla.fill(NEGRO)

        diapositiva.set_alpha(int(255 * opacidad))
        pantalla.blit(diapositiva, (0, 0))

        pygame.display.flip()


def pantallas_intro(pantalla, reloj, ancho, alto, logo, fuente_grande, fuente_media):
    """Dos pantallas negras que se aclaran, como una presentación."""

    diapositivas = [
        _crear_diapositiva_productores(
            ancho,
            alto,
            fuente_grande,
            fuente_media
        ),
        _crear_diapositiva_logo(
            ancho,
            alto,
            logo
        ),
    ]

    for diapositiva in diapositivas:
        _mostrar_diapositiva(pantalla, reloj, diapositiva)

    # Pequeña pausa en negro antes de pasar a la elección de personajes
    pantalla.fill(NEGRO)
    pygame.display.flip()
    pygame.time.wait(300)

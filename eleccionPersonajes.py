import pygame
import sys


FPS = 60

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
VERDE = (46, 204, 113)
CELESTE = (135, 206, 235)


def seleccionar_personaje(
    pantalla,
    reloj,
    ancho,
    alto,
    personajes,
    fuente_grande,
    fuente_media
):
    seleccionado = 0

    while True:
        pantalla.fill(CELESTE)

        # ==============================================
        # TÍTULO
        # ==============================================

        titulo = fuente_grande.render(
            "SELECCIONAR PERSONAJE",
            True,
            BLANCO
        )

        pantalla.blit(
            titulo,
            titulo.get_rect(center=(ancho // 2, 70))
        )

        # ==============================================
        # PERSONAJES
        # ==============================================

        cantidad = len(personajes)

        espacio = 150

        inicio_x = ancho // 2 - ((cantidad - 1) * espacio) // 2

        for i, personaje in enumerate(personajes):

            x = inicio_x + i * espacio
            y = 300

            # Caja del personaje
            rect = pygame.Rect(
                x - 65,
                y - 110,
                130,
                220
            )

            if i == seleccionado:
                pygame.draw.rect(
                    pantalla,
                    VERDE,
                    rect,
                    6,
                    border_radius=12
                )
            else:
                pygame.draw.rect(
                    pantalla,
                    GRIS,
                    rect,
                    3,
                    border_radius=12
                )

            # Sprite
            sprite = personaje["preview"]

            sprite_rect = sprite.get_rect(
                center=(x, y - 20)
            )

            pantalla.blit(sprite, sprite_rect)

            # Nombre
            nombre = fuente_media.render(
                personaje["nombre"],
                True,
                NEGRO
            )

            pantalla.blit(
                nombre,
                nombre.get_rect(
                    center=(x, y + 75)
                )
            )

        # ==============================================
        # CONTROLES
        # ==============================================

        controles = fuente_media.render(
            "<  >   Elegir       ENTER   Seleccionar",
            True,
            NEGRO
        )

        pantalla.blit(
            controles,
            controles.get_rect(
                center=(ancho // 2, alto - 50)
            )
        )

        # ==============================================
        # EVENTOS
        # ==============================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_LEFT:
                    seleccionado -= 1

                    if seleccionado < 0:
                        seleccionado = len(personajes) - 1

                elif evento.key == pygame.K_RIGHT:
                    seleccionado += 1

                    if seleccionado >= len(personajes):
                        seleccionado = 0

                elif evento.key == pygame.K_RETURN:
                    return personajes[seleccionado]["sprites"]

                elif evento.key == pygame.K_ESCAPE:
                    return None

        pygame.display.flip()
        reloj.tick(FPS)
import pygame
import sys

FPS = 60

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
VERDE = (46, 204, 113)


def dibujar_boton(superficie, texto, rect, color_fondo, color_texto, fuente):
    pygame.draw.rect(superficie, color_fondo, rect, border_radius=12)
    pygame.draw.rect(superficie, NEGRO, rect, 3, border_radius=12)
    render = fuente.render(texto, True, color_texto)
    superficie.blit(render, render.get_rect(center=rect.center))


def pantalla_instrucciones(pantalla, reloj, ancho, alto, color_fondo, fuente_grande, fuente_media):
    boton_volver = pygame.Rect(ancho // 2 - 110, alto - 100, 220, 65)

    lineas = [
        "FLECHAS o A / D: moverse",
        "ESPACIO, ARRIBA o W: saltar",
        "ABAJO o S: agacharse",
        "Llega a la bandera dorada para ganar",
        "Esquiva a los enemigos rojos",
        "ESC: volver al menu en cualquier momento",
    ]

    while True:
        pantalla.fill(color_fondo)

        titulo = fuente_grande.render("INSTRUCCIONES", True, BLANCO)
        pantalla.blit(titulo, titulo.get_rect(center=(ancho // 2, 90)))

        for i, linea in enumerate(lineas):
            render = fuente_media.render(linea, True, NEGRO)
            pantalla.blit(render, render.get_rect(center=(ancho // 2, 190 + i * 55)))

        mouse_pos = pygame.mouse.get_pos()
        color_boton = VERDE if boton_volver.collidepoint(mouse_pos) else GRIS
        dibujar_boton(pantalla, "VOLVER", boton_volver, color_boton, BLANCO, fuente_media)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    return "menu"
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return "menu"

        pygame.display.flip()
        reloj.tick(FPS)

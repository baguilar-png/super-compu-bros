import pygame
import sys
import os

from juego import jugar
from instrucciones import pantalla_instrucciones

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Super Compu Bros MVP")


CELESTE = (135, 206, 235)
ROJO = (220, 20, 60)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (100, 100, 100)
VERDE = (46, 204, 113)

reloj = pygame.time.Clock()
FPS = 60
fuente_grande = pygame.font.SysFont("Arial", 60, bold=True)
fuente_media = pygame.font.SysFont("Arial", 36)

CARPETA = os.path.dirname(os.path.abspath(__file__))

ESCALA_SPRITE = 3
_sprite_original = pygame.image.load(os.path.join(CARPETA, "assets/personajes/benja.png")).convert_alpha()

JUG_ANCHO = _sprite_original.get_width() * ESCALA_SPRITE
JUG_ALTO = _sprite_original.get_height() * ESCALA_SPRITE
JUG_ALTO_AGACHADO = JUG_ALTO // 2

SPRITE_DER = pygame.transform.scale(_sprite_original, (JUG_ANCHO, JUG_ALTO))
SPRITE_IZQ = pygame.transform.flip(SPRITE_DER, True, False)
SPRITE_AGACHADO_DER = pygame.transform.scale(_sprite_original, (JUG_ANCHO, JUG_ALTO_AGACHADO))
SPRITE_AGACHADO_IZQ = pygame.transform.flip(SPRITE_AGACHADO_DER, True, False)

sprites = {
    "der": SPRITE_DER,
    "izq": SPRITE_IZQ,
    "agachado_der": SPRITE_AGACHADO_DER,
    "agachado_izq": SPRITE_AGACHADO_IZQ,
    "ancho": JUG_ANCHO,
    "alto": JUG_ALTO,
    "alto_agachado": JUG_ALTO_AGACHADO,
}

_logo_original = pygame.image.load(os.path.join(CARPETA, "assets/fondos/logo.png")).convert_alpha()
ESCALA_LOGO = 3
LOGO = pygame.transform.scale(
    _logo_original,
    (_logo_original.get_width() * ESCALA_LOGO, _logo_original.get_height() * ESCALA_LOGO),
)

_play_original = pygame.image.load(os.path.join(CARPETA, "assets/fondos/play.png")).convert_alpha()
PLAY_BUTTON = pygame.transform.scale(_play_original, (150, 150))


def dibujar_boton(superficie, texto, rect, color_fondo, color_texto, fuente):
    pygame.draw.rect(superficie, color_fondo, rect, border_radius=12)
    pygame.draw.rect(superficie, NEGRO, rect, 3, border_radius=12)
    render = fuente.render(texto, True, color_texto)
    superficie.blit(render, render.get_rect(center=rect.center))


def menu():
    boton_play = pygame.Rect(ANCHO // 2 - 100, 260, 200, 65)
    boton_instrucciones = pygame.Rect(ANCHO // 2 - 100, 345, 200, 65)
    boton_exit = pygame.Rect(ANCHO // 2 - 100, 430, 200, 65)

    while True:
        pantalla.fill(CELESTE)
        pantalla.blit(LOGO, LOGO.get_rect(center=(ANCHO // 2, 140)))

        mouse_pos = pygame.mouse.get_pos()
        color_instrucciones = VERDE if boton_instrucciones.collidepoint(mouse_pos) else GRIS
        color_exit = ROJO if boton_exit.collidepoint(mouse_pos) else GRIS
        pantalla.blit(PLAY_BUTTON, PLAY_BUTTON.get_rect(center=boton_play.center))
        dibujar_boton(pantalla, "INSTRUCCIONES", boton_instrucciones, color_instrucciones, BLANCO, pygame.font.SysFont("Arial", 22))
        dibujar_boton(pantalla, "EXIT", boton_exit, color_exit, BLANCO, fuente_media)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_play.collidepoint(evento.pos):
                    return "jugar"
                if boton_instrucciones.collidepoint(evento.pos):
                    return "instrucciones"
                if boton_exit.collidepoint(evento.pos):
                    pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if evento.key == pygame.K_RETURN:
                    return "jugar"

        pygame.display.flip()
        reloj.tick(FPS)


def main():
    estado = "menu"
    while True:
        if estado == "menu":
            estado = menu()
        elif estado == "jugar":
            estado = jugar(pantalla, reloj, sprites, fuente_grande, fuente_media)
        elif estado == "instrucciones":
            estado = pantalla_instrucciones(pantalla, reloj, ANCHO, ALTO, CELESTE, fuente_grande, fuente_media)


if __name__ == "__main__":
    main()

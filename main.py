import pygame
import sys
import os

from juego import jugar
from instrucciones import pantalla_instrucciones
from eleccionPersonajes import seleccionar_personaje
from intro import pantallas_intro


# ==========================================================
# INICIALIZAR PYGAME
# ==========================================================

pygame.init()


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

ANCHO, ALTO = 800, 600

pantalla = pygame.display.set_mode(
    (ANCHO, ALTO)
)

pygame.display.set_caption(
    "Super Compu Bros MVP"
)


# ==========================================================
# COLORES
# ==========================================================

CELESTE = (135, 206, 235)
ROJO = (220, 20, 60)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (100, 100, 100)
VERDE = (46, 204, 113)


# ==========================================================
# RELOJ Y FUENTES
# ==========================================================

reloj = pygame.time.Clock()

FPS = 60

fuente_grande = pygame.font.SysFont(
    "Arial",
    60,
    bold=True
)

fuente_media = pygame.font.SysFont(
    "Arial",
    36
)


# ==========================================================
# CARPETAS
# ==========================================================

CARPETA = os.path.dirname(
    os.path.abspath(__file__)
)


# ==========================================================
# ESCALAS
# ==========================================================

ESCALA_SPRITE = 2


# ==========================================================
# CARGAR SPRITE
# ==========================================================

def cargar_sprite(ruta):

    original = pygame.image.load(
        os.path.join(CARPETA, ruta)
    ).convert_alpha()

    return pygame.transform.scale(
        original,
        (
            original.get_width() * ESCALA_SPRITE,
            original.get_height() * ESCALA_SPRITE
        )
    )


# ==========================================================
# CREAR SPRITES DE PERSONAJE
#
# TODOS LOS ARCHIVOS ORIGINALES MIRAN HACIA LA DERECHA.
# LAS VERSIONES IZQUIERDAS SE CREAN AUTOMÁTICAMENTE.
# ==========================================================

def crear_sprites_personaje(
    carpeta,
    nombre_idle,
    nombre_agachado,
    nombre_saltando,
    nombre_frame1,
    nombre_frame2,
    nombre_frame3
):

    ruta_base = os.path.join(
        "assets",
        "personajes",
        carpeta
    )

    # ------------------------------------------------------
    # SPRITES ORIGINALES: DERECHA
    # ------------------------------------------------------

    idle_der = cargar_sprite(
        os.path.join(
            ruta_base,
            nombre_idle
        )
    )

    agachado_der = cargar_sprite(
        os.path.join(
            ruta_base,
            nombre_agachado
        )
    )

    saltar_der = cargar_sprite(
        os.path.join(
            ruta_base,
            nombre_saltando
        )
    )

    frame1_der = cargar_sprite(
        os.path.join(
            ruta_base,
            nombre_frame1
        )
    )

    frame2_der = cargar_sprite(
        os.path.join(
            ruta_base,
            nombre_frame2
        )
    )

    frame3_der = cargar_sprite(
        os.path.join(
            ruta_base,
            nombre_frame3
        )
    )

    # ------------------------------------------------------
    # SPRITES ESPEJADOS: IZQUIERDA
    # ------------------------------------------------------

    idle_izq = pygame.transform.flip(
        idle_der,
        True,
        False
    )

    agachado_izq = pygame.transform.flip(
        agachado_der,
        True,
        False
    )

    saltar_izq = pygame.transform.flip(
        saltar_der,
        True,
        False
    )

    frame1_izq = pygame.transform.flip(
        frame1_der,
        True,
        False
    )

    frame2_izq = pygame.transform.flip(
        frame2_der,
        True,
        False
    )

    frame3_izq = pygame.transform.flip(
        frame3_der,
        True,
        False
    )

    # ------------------------------------------------------
    # DEVOLVER SPRITES
    # ------------------------------------------------------

    return {
        "idle_der": idle_der,
        "idle_izq": idle_izq,

        "agachado_der": agachado_der,
        "agachado_izq": agachado_izq,

        "saltar_der": saltar_der,
        "saltar_izq": saltar_izq,

        "caminar_der": [
            frame1_der,
            frame2_der,
            frame3_der
        ],

        "caminar_izq": [
            frame1_izq,
            frame2_izq,
            frame3_izq
        ],

        "ancho": idle_der.get_width(),
        "alto": idle_der.get_height(),
        "alto_agachado": agachado_der.get_height()
    }


# ==========================================================
# CREAR PERSONAJOS
# ==========================================================

personajes = []


# ----------------------------------------------------------
# BAUTO
# ----------------------------------------------------------

sprites_bauto = crear_sprites_personaje(
    "BAUTO",

    "bauto final.png",
    "bauto agachado.png",
    "bauto saltando.png",

    "bauto frame 1.png",
    "bauto frame 2.png",
    "bauto frame 3.png"
)

_play_original = pygame.image.load(os.path.join(CARPETA, "assets/fondos/play.png")).convert_alpha()
PLAY_BUTTON = pygame.transform.scale(_play_original, (200, 65))
_instrucciones_original = pygame.image.load(os.path.join(CARPETA, "assets/fondos/instrucciones.png")).convert_alpha()
INSTRUCCIONES_BUTTON = pygame.transform.scale(_instrucciones_original, (200, 65))
_exit_original = pygame.image.load(os.path.join(CARPETA, "assets/fondos/exit.png")).convert_alpha()
EXIT_BUTTON = pygame.transform.scale(_exit_original, (150, 150))
personajes.append({
    "nombre": "BAUTO",
    "preview": sprites_bauto["idle_der"],
    "sprites": sprites_bauto
})


# ----------------------------------------------------------
# BENJA
# ----------------------------------------------------------

sprites_benja = crear_sprites_personaje(
    "BENJA",

    "benja.png",
    "Benja agachado.png",
    "Benja saltando.png",

    "Benja frame 1.png",
    "Benja frame 2.png",
    "Benja frame 3.png"
)

personajes.append({
    "nombre": "BENJA",
    "preview": sprites_benja["idle_der"],
    "sprites": sprites_benja
})


# ----------------------------------------------------------
# CASTRO
# ----------------------------------------------------------

sprites_castro = crear_sprites_personaje(
    "CASTRO",

    "castro final.png",
    "castro agachado.png",
    "castro saltando.png",

    "castro frame 1.png",
    "castro frame 2.png",
    "castro frame 3.png"
)

personajes.append({
    "nombre": "CASTRO",
    "preview": sprites_castro["idle_der"],
    "sprites": sprites_castro
})


# ----------------------------------------------------------
# POSHO
# ----------------------------------------------------------

sprites_posho = crear_sprites_personaje(
    "POSHO",

    "Posho final.png",
    "Posho agachado.png",
    "Posho saltando.png",

    "Posho Frame 1.png",
    "Posho Frame 2.png",
    "Posho Frame 3.png"
)

personajes.append({
    "nombre": "POSHO",
    "preview": sprites_posho["idle_der"],
    "sprites": sprites_posho
})


# ----------------------------------------------------------
# THIAGO
# ----------------------------------------------------------

sprites_thiago = crear_sprites_personaje(
    "THIAGO",

    "thiago final.png",
    "thiago agachado.png",
    "thiago saltando.png",

    "thiago frame 1.png",
    "thiago frame 2.png",
    "thiago frame 3.png"
)

personajes.append({
    "nombre": "THIAGO",
    "preview": sprites_thiago["idle_der"],
    "sprites": sprites_thiago
})


# ==========================================================
# ENEMIGO GAGAMBA
# ==========================================================

sprite_gagamba = cargar_sprite(
    os.path.join(
        "assets",
        "personajes",
        "gagamba.png"
    )
)

sprite_gagamba = pygame.transform.scale(
    sprite_gagamba,
    (50, 42)
)


# Agregar el enemigo a todos los personajes
for personaje in personajes:

    personaje["sprites"]["enemigo"] = sprite_gagamba


# ==========================================================
# LOGO
# ==========================================================

_logo_original = pygame.image.load(
    os.path.join(
        CARPETA,
        "assets",
        "fondos",
        "logo.png"
    )
).convert_alpha()

ESCALA_LOGO = 3

LOGO = pygame.transform.scale(
    _logo_original,
    (
        _logo_original.get_width() * ESCALA_LOGO,
        _logo_original.get_height() * ESCALA_LOGO
    )
)


# El png del logo tiene espacio transparente a la izquierda;
# se lo descuenta para que el dibujo quede pegado al margen.
LOGO_MARGEN_TRANSPARENTE = LOGO.get_bounding_rect().left


# ==========================================================
# BOTÓN PLAY
# ==========================================================

_play_original = pygame.image.load(
    os.path.join(
        CARPETA,
        "assets",
        "fondos",
        "play.png"
    )
).convert_alpha()

PLAY_BUTTON = pygame.transform.scale(
    _play_original,
    (200, 65)
)


# ==========================================================
# DIBUJAR BOTÓN DE TEXTO
# ==========================================================

def dibujar_boton(
    superficie,
    texto,
    rect,
    color_fondo,
    color_texto,
    fuente
):

    pygame.draw.rect(
        superficie,
        color_fondo,
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        superficie,
        NEGRO,
        rect,
        3,
        border_radius=12
    )

    render = fuente.render(
        texto,
        True,
        color_texto
    )

    superficie.blit(
        render,
        render.get_rect(
            center=rect.center
        )
    )


# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================

MARGEN_IZQ = 60

ALTO_HOTBAR = 80

GRIS_HOTBAR = (90, 90, 90)
GRIS_HOTBAR_OSCURO = (55, 55, 55)
GRIS_SLOT = (130, 130, 130)


def dibujar_hotbar(superficie, sprites_elegidos):
    """Bloque gris inferior con un slot por personaje (estilo hotbar)."""

    y_barra = ALTO - ALTO_HOTBAR

    # Bloque gris con borde superior
    pygame.draw.rect(
        superficie,
        GRIS_HOTBAR,
        (0, y_barra, ANCHO, ALTO_HOTBAR)
    )

    pygame.draw.line(
        superficie,
        GRIS_HOTBAR_OSCURO,
        (0, y_barra),
        (ANCHO, y_barra),
        4
    )

    # Slots
    tam_slot = 64
    separacion = 8
    y_slot = y_barra + (ALTO_HOTBAR - tam_slot) // 2

    for i, personaje in enumerate(personajes):

        x_slot = MARGEN_IZQ + i * (tam_slot + separacion)

        rect_slot = pygame.Rect(x_slot, y_slot, tam_slot, tam_slot)

        es_elegido = personaje["sprites"] is sprites_elegidos

        pygame.draw.rect(superficie, GRIS_SLOT, rect_slot)

        pygame.draw.rect(
            superficie,
            BLANCO if es_elegido else GRIS_HOTBAR_OSCURO,
            rect_slot,
            4 if es_elegido else 3
        )

        # Sprite del personaje (se achica si no entra en el slot)
        sprite = personaje["preview"]

        maximo = tam_slot - 12

        if sprite.get_width() > maximo or sprite.get_height() > maximo:

            factor = min(
                maximo / sprite.get_width(),
                maximo / sprite.get_height()
            )

            sprite = pygame.transform.scale(
                sprite,
                (
                    int(sprite.get_width() * factor),
                    int(sprite.get_height() * factor)
                )
            )

        superficie.blit(
            sprite,
            sprite.get_rect(center=rect_slot.center)
        )

    # Pista a la derecha de la barra
    pista = pygame.font.SysFont("Arial", 20).render(
        "C: cambiar personaje",
        True,
        BLANCO
    )

    superficie.blit(
        pista,
        pista.get_rect(
            midright=(ANCHO - MARGEN_IZQ, y_barra + ALTO_HOTBAR // 2)
        )
    )


def menu(sprites_elegidos=None):

    boton_play = pygame.Rect(
        MARGEN_IZQ,
        250,
        200,
        65
    )

    boton_instrucciones = pygame.Rect(
        MARGEN_IZQ,
        325,
        200,
        65
    )

    boton_exit = pygame.Rect(
        MARGEN_IZQ,
        400,
        200,
        65
    )

    while True:

        pantalla.fill(
            CELESTE
        )

        # --------------------------------------------------
        # LOGO
        # --------------------------------------------------

        pantalla.blit(
            LOGO,
            LOGO.get_rect(
                midleft=(
                    MARGEN_IZQ - LOGO_MARGEN_TRANSPARENTE,
                    125
                )
            )
        )

        # --------------------------------------------------
        # MOUSE
        # --------------------------------------------------

        mouse_pos = pygame.mouse.get_pos()
        color_instrucciones = VERDE if boton_instrucciones.collidepoint(mouse_pos) else GRIS
        color_exit = ROJO if boton_exit.collidepoint(mouse_pos) else GRIS
        pantalla.blit(PLAY_BUTTON, PLAY_BUTTON.get_rect(center=boton_play.center))
        pantalla.blit(INSTRUCCIONES_BUTTON, INSTRUCCIONES_BUTTON.get_rect(center=boton_instrucciones.center))
        pantalla.blit(EXIT_BUTTON, EXIT_BUTTON.get_rect(center=boton_exit.center))

        color_instrucciones = (
            VERDE
            if boton_instrucciones.collidepoint(mouse_pos)
            else GRIS
        )

        color_exit = (
            ROJO
            if boton_exit.collidepoint(mouse_pos)
            else GRIS
        )

        # --------------------------------------------------
        # BOTÓN PLAY
        # --------------------------------------------------

        pantalla.blit(
            PLAY_BUTTON,
            PLAY_BUTTON.get_rect(
                center=boton_play.center
            )
        )

        # --------------------------------------------------
        # BOTÓN INSTRUCCIONES
        # --------------------------------------------------

        dibujar_boton(
            pantalla,
            "INSTRUCCIONES",
            boton_instrucciones,
            color_instrucciones,
            BLANCO,
            pygame.font.SysFont(
                "Arial",
                22
            )
        )

        # --------------------------------------------------
        # BOTÓN EXIT
        # --------------------------------------------------

        dibujar_boton(
            pantalla,
            "EXIT",
            boton_exit,
            color_exit,
            BLANCO,
            fuente_media
        )

        # --------------------------------------------------
        # HOTBAR
        # --------------------------------------------------

        dibujar_hotbar(pantalla, sprites_elegidos)

        # --------------------------------------------------
        # EVENTOS
        # --------------------------------------------------

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            # ----------------------------------------------
            # CLICK DEL MOUSE
            # ----------------------------------------------

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if boton_play.collidepoint(evento.pos):

                    return "jugar"

                if boton_instrucciones.collidepoint(evento.pos):

                    return "instrucciones"

                if boton_exit.collidepoint(evento.pos):

                    pygame.quit()
                    sys.exit()

            # ----------------------------------------------
            # TECLADO
            # ----------------------------------------------

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

                if evento.key == pygame.K_RETURN:

                    return "jugar"

                if evento.key == pygame.K_c:

                    return "personajes"

        pygame.display.flip()

        reloj.tick(FPS)


# ==========================================================
# FUNCIÓN PRINCIPAL
# ==========================================================

def main():

    estado = "intro"

    sprites_elegidos = None

    while True:

        # --------------------------------------------------
        # INTRO: DOS PANTALLAS NEGRAS QUE SE ACLARAN
        # --------------------------------------------------

        if estado == "intro":

            pantallas_intro(
                pantalla,
                reloj,
                ANCHO,
                ALTO,
                LOGO,
                fuente_grande,
                fuente_media
            )

            estado = "personajes"

        # --------------------------------------------------
        # SELECCIÓN DE PERSONAJE (ANTES DEL MENÚ)
        # --------------------------------------------------

        elif estado == "personajes":

            elegido = seleccionar_personaje(
                pantalla,
                reloj,
                ANCHO,
                ALTO,
                personajes,
                fuente_grande,
                fuente_media
            )

            if elegido is None:

                # ESC en la selección: si ya había un personaje
                # elegido se vuelve al menú, si no se sale del juego
                if sprites_elegidos is None:

                    pygame.quit()
                    sys.exit()

            else:

                sprites_elegidos = elegido

            estado = "menu"

        # --------------------------------------------------
        # MENÚ
        # --------------------------------------------------

        elif estado == "menu":

            estado = menu(sprites_elegidos)

        # --------------------------------------------------
        # JUGAR CON EL PERSONAJE ELEGIDO
        # --------------------------------------------------

        elif estado == "jugar":

            estado = jugar(
                pantalla,
                reloj,
                sprites_elegidos,
                fuente_grande,
                fuente_media
            )

        # --------------------------------------------------
        # INSTRUCCIONES
        # --------------------------------------------------

        elif estado == "instrucciones":

            estado = pantalla_instrucciones(
                pantalla,
                reloj,
                ANCHO,
                ALTO,
                CELESTE,
                fuente_grande,
                fuente_media
            )


# ==========================================================
# EJECUTAR
# ==========================================================

if __name__ == "__main__":

    main()
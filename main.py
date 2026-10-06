import pygame
import sys
import os
import math

from juego import jugar
from mapa import pantalla_mapa
from instrucciones import pantalla_instrucciones
from eleccionPersonajes import seleccionar_personaje
from intro import pantallas_intro
from pixel_font import FuentePixel
from fondo_menu import FondoMenuAnimado
import transicion
import musica
from archivos import (
    cargar_personaje,
    guardar_personaje,
    cargar_mapa
)


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
    "Super Compu Bros Alpha 1.000.2"
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

# Fuentes pixel art (la cifra es el tamano de cada pixel de la letra)
fuente_grande = FuentePixel(6)
fuente_media = FuentePixel(3)
fuente_chica = FuentePixel(2)


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


# Cabeza para la hotbar (imagen solo de la cabeza, escala 3)
ESCALA_CABEZA = 3


def cargar_cabeza(ruta):

    original = pygame.image.load(
        os.path.join(CARPETA, ruta)
    ).convert_alpha()

    return pygame.transform.scale(
        original,
        (
            original.get_width() * ESCALA_CABEZA,
            original.get_height() * ESCALA_CABEZA
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

_exit_original = pygame.image.load(os.path.join(CARPETA, "assets/fondos/exit.png")).convert_alpha()
EXIT_BUTTON = pygame.transform.scale(_exit_original, (150, 150))
personajes.append({
    "nombre": "BAUTO",
    "preview": sprites_bauto["idle_der"],
    "seleccion": cargar_sprite("assets/personajes/BAUTO/bauto frente.png"),
    "cabeza": cargar_cabeza("assets/personajes/BAUTO/bauto cabeza.png"),
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
    "seleccion": cargar_sprite("assets/personajes/BENJA/benja frente.png"),
    "cabeza": cargar_cabeza("assets/personajes/BENJA/benja cabeza.png"),
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
    "seleccion": cargar_sprite("assets/personajes/CASTRO/castro frente.png"),
    "cabeza": cargar_cabeza("assets/personajes/CASTRO/castro cabeza.png"),
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
    "seleccion": cargar_sprite("assets/personajes/POSHO/posho frente.png"),
    "cabeza": cargar_cabeza("assets/personajes/POSHO/Posho cabeza.png"),
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
    "seleccion": cargar_sprite("assets/personajes/THIAGO/thiago frente.png"),
    "cabeza": cargar_cabeza("assets/personajes/THIAGO/thiago cabeza.png"),
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
# BOTONES PIXEL ART (PLAY e INSTRUCCIONES)
#
# Los png tienen mucho espacio transparente alrededor, así que se
# recortan al borde real del botón y se escalan por un entero
# (para que los píxeles queden nítidos).
#
# Hover: las letras y el borde se ponen blancos.
# Click: sigue en blanco y "respira" 2 veces; recién después
#        se ejecuta la acción del botón.
# ==========================================================

# Los tres botones (PLAY, INSTRUCCIONES y EXIT) tienen la misma altura.
# Se toma la que ya tenía INSTRUCCIONES (9 px de dibujo x 5).
ALTO_BOTON = 45

# Animación al apretar: "respira" 2 veces
RESPIROS = 2
DURACION_RESPIRO_MS = 180
AGRANDE = 0.12

# Duración total de la animación
DURACION_ANIMACION_MS = RESPIROS * DURACION_RESPIRO_MS


def recortar(superficie):
    """Recorta el espacio transparente que rodea al dibujo."""

    return superficie.subsurface(
        superficie.get_bounding_rect()
    ).copy()


def hacer_blanco(superficie):
    """
    Devuelve una copia con las letras y el borde (gris oscuro)
    en blanco. El cuerpo gris del botón se mantiene.
    """

    copia = superficie.copy()

    for x in range(copia.get_width()):

        for y in range(copia.get_height()):

            r, g, b, a = copia.get_at((x, y))

            if a > 0 and r <= 120:

                copia.set_at((x, y), (255, 255, 255, a))

    return copia


def hacer_todo_blanco(superficie):
    """Devuelve una copia con TODO el botón en blanco (silueta)."""

    copia = superficie.copy()

    for x in range(copia.get_width()):

        for y in range(copia.get_height()):

            a = copia.get_at((x, y)).a

            if a > 0:

                copia.set_at((x, y), (255, 255, 255, a))

    return copia


class BotonPixel:

    def __init__(self, archivo, alto, x_izq, y_centro):

        original = recortar(
            pygame.image.load(
                os.path.join(
                    CARPETA,
                    "assets",
                    "fondos",
                    archivo
                )
            ).convert_alpha()
        )

        # Se escala para que todos los botones midan lo mismo de alto
        escala = alto / original.get_height()

        self.tamano = (
            round(original.get_width() * escala),
            alto
        )

        self.normal = pygame.transform.scale(
            original,
            self.tamano
        )

        self.blanco = pygame.transform.scale(
            hacer_blanco(original),
            self.tamano
        )

        # Mientras respira, el botón entero se vuelve blanco
        self.todo_blanco = pygame.transform.scale(
            hacer_todo_blanco(original),
            self.tamano
        )

        # Alineado a la izquierda con el resto del menú
        self.rect = pygame.Rect(0, 0, *self.tamano)

        self.rect.midleft = (x_izq, y_centro)

    def dibujar(self, superficie, hover, t_click):
        """
        hover   -> True si el mouse está encima (se pone blanco)
        t_click -> ms desde que se apretó, o None si no se apretó
        """

        if t_click is None:

            imagen = self.blanco if hover else self.normal

        else:

            # Apretado: todo blanco y respirando (agranda y achica)
            fase = (t_click / DURACION_RESPIRO_MS) % 1.0

            escala = 1 + AGRANDE * math.sin(math.pi * fase)

            imagen = pygame.transform.scale(
                self.todo_blanco,
                (
                    int(self.tamano[0] * escala),
                    int(self.tamano[1] * escala)
                )
            )

        superficie.blit(
            imagen,
            imagen.get_rect(center=self.rect.center)
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

_cubo_original = recortar(
    pygame.image.load(
        os.path.join(
            CARPETA,
            "assets",
            "fondos",
            "cubo.png"
        )
    ).convert_alpha()
)

ESCALA_CUBO = 3

CUBO = pygame.transform.scale(
    _cubo_original,
    (
        _cubo_original.get_width() * ESCALA_CUBO,
        _cubo_original.get_height() * ESCALA_CUBO
    )
)


# Fondo de la seleccion de personajes (la imagen es 16:9, la ventana
# 4:3: se ajusta a la altura y se recorta el centro)
_fondo_original = pygame.image.load(
    os.path.join(
        CARPETA,
        "assets",
        "fondos",
        "fondo_seleccion.png"
    )
).convert()

_factor_fondo = ALTO / _fondo_original.get_height()

_fondo_escalado = pygame.transform.smoothscale(
    _fondo_original,
    (
        round(_fondo_original.get_width() * _factor_fondo),
        ALTO
    )
)

FONDO_SELECCION = _fondo_escalado.subsurface(
    (
        (_fondo_escalado.get_width() - ANCHO) // 2,
        0,
        ANCHO,
        ALTO
    )
).copy()


# Fondo animado del menu (Obelisco con nubes y autos en movimiento)
FONDO_MENU = FondoMenuAnimado(CARPETA, ANCHO, ALTO)


# Hot bar nueva (hot_bar.png): se recorta la parte transparente de
# arriba y se estira al ancho de la ventana sin suavizar (pixel art)
_hotbar_original = recortar(
    pygame.image.load(
        os.path.join(
            CARPETA,
            "assets",
            "fondos",
            "hot_bar.png"
        )
    ).convert_alpha()
)

HOTBAR_IMAGEN = pygame.transform.scale(
    _hotbar_original,
    (ANCHO, ALTO_HOTBAR)
)


def dibujar_hotbar(superficie, sprites_elegidos):
    """Barra inferior (imagen) con un slot por personaje (estilo hotbar)."""

    y_barra = ALTO - ALTO_HOTBAR

    superficie.blit(HOTBAR_IMAGEN, (0, y_barra))

    # Slots
    tam_slot = 64
    separacion = 8
    y_slot = y_barra + (ALTO_HOTBAR - tam_slot) // 2

    for i, personaje in enumerate(personajes):

        x_slot = MARGEN_IZQ + i * (tam_slot + separacion)

        rect_slot = pygame.Rect(x_slot, y_slot, tam_slot, tam_slot)

        es_elegido = personaje["sprites"] is sprites_elegidos

        # El cubo reemplaza al cuadrado gris
        rect_cubo = CUBO.get_rect(center=rect_slot.center)

        superficie.blit(CUBO, rect_cubo)

        # El personaje elegido se marca con un borde blanco
        if es_elegido:

            pygame.draw.rect(
                superficie,
                BLANCO,
                rect_cubo.inflate(6, 6),
                3
            )

        # Sprite del personaje (se achica si no entra en el slot)
        sprite = personaje.get("cabeza", personaje["preview"])

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
    pista = fuente_chica.render(
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


BOTON_PLAY = BotonPixel(
    "boton_jugar.png",
    ALTO_BOTON,
    MARGEN_IZQ,
    295
)

BOTON_INSTRUCCIONES = BotonPixel(
    "boton_instrucciones.png",
    ALTO_BOTON,
    MARGEN_IZQ,
    365
)

BOTON_EXIT = BotonPixel(
    "boton_salir.png",
    ALTO_BOTON,
    MARGEN_IZQ,
    435
)


def menu(sprites_elegidos=None):

    # Botón que se apretó ("jugar" / "instrucciones") y en qué
    # momento (ms); None = todavía no se apretó ninguno
    accion_click = None
    inicio_click = None

    while True:

        FONDO_MENU.dibujar(pantalla)

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

        # --------------------------------------------------
        # BOTONES PLAY E INSTRUCCIONES
        # --------------------------------------------------

        t_click = (
            None
            if inicio_click is None
            else pygame.time.get_ticks() - inicio_click
        )

        # Mientras respira uno, el otro no reacciona al mouse
        libre = accion_click is None

        BOTON_PLAY.dibujar(
            pantalla,
            libre and BOTON_PLAY.rect.collidepoint(mouse_pos),
            t_click if accion_click == "jugar" else None
        )

        BOTON_INSTRUCCIONES.dibujar(
            pantalla,
            libre and BOTON_INSTRUCCIONES.rect.collidepoint(mouse_pos),
            t_click if accion_click == "instrucciones" else None
        )

        BOTON_EXIT.dibujar(
            pantalla,
            libre and BOTON_EXIT.rect.collidepoint(mouse_pos),
            t_click if accion_click == "salir" else None
        )

        # Terminaron los 2 respiros -> recién ahí se ejecuta la acción
        if t_click is not None and t_click >= DURACION_ANIMACION_MS:

            return accion_click

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

                if accion_click is not None:

                    continue

                if BOTON_PLAY.rect.collidepoint(evento.pos):

                    accion_click = "jugar"
                    inicio_click = pygame.time.get_ticks()

                    continue

                if BOTON_INSTRUCCIONES.rect.collidepoint(evento.pos):

                    accion_click = "instrucciones"
                    inicio_click = pygame.time.get_ticks()

                    continue

                if BOTON_EXIT.rect.collidepoint(evento.pos):

                    accion_click = "salir"
                    inicio_click = pygame.time.get_ticks()

                    continue

            # ----------------------------------------------
            # TECLADO
            # ----------------------------------------------

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:

                    pygame.quit()
                    sys.exit()

                if accion_click is not None:

                    continue

                if evento.key == pygame.K_RETURN:

                    accion_click = "jugar"
                    inicio_click = pygame.time.get_ticks()

                    continue

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

    # Pantalla que se mostró en la vuelta anterior (para la transición)
    estado_mostrado = None

    while True:

        # --------------------------------------------------
        # TRANSICIÓN DE CÍRCULO ENTRE PANTALLAS
        #
        # Primero se CIERRA el círculo sobre la pantalla en la que
        # estabas (sigue viéndose el menú / nivel / mapa de antes) y
        # después se ABRE sobre la pantalla nueva.
        # Desde la intro solo se abre (la intro termina en negro).
        # --------------------------------------------------

        if estado_mostrado is not None:

            if estado_mostrado != "intro":

                transicion.cerrar_circulo(pantalla, reloj)

            transicion.abrir_circulo()

        estado_mostrado = estado

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

            # Si hay un personaje guardado (personajes.txt) se va
            # directo al menu, si no se elige
            guardado = cargar_personaje()

            for personaje in personajes:

                if personaje["nombre"] == guardado:
                    sprites_elegidos = personaje["sprites"]

            estado = "menu" if sprites_elegidos is not None else "personajes"

        # --------------------------------------------------
        # SELECCIÓN DE PERSONAJE (ANTES DEL MENÚ)
        # --------------------------------------------------

        elif estado == "personajes":

            musica.reproducir(musica.MUSICA_SELECCION)

            elegido = seleccionar_personaje(
                pantalla,
                reloj,
                ANCHO,
                ALTO,
                personajes,
                fuente_grande,
                fuente_media,
                FONDO_SELECCION
            )

            if elegido is None:

                # ESC en la selección: si ya había un personaje
                # elegido se vuelve al menú, si no se sale del juego
                if sprites_elegidos is None:

                    pygame.quit()
                    sys.exit()

            else:

                sprites_elegidos = elegido

                # Se guarda el personaje elegido en personajes.txt
                for personaje in personajes:

                    if personaje["sprites"] is elegido:
                        guardar_personaje(personaje["nombre"])

            estado = "menu"

        # --------------------------------------------------
        # MENÚ
        # --------------------------------------------------

        elif estado == "menu":

            musica.reproducir(musica.MUSICA_MENU)

            estado = menu(sprites_elegidos)

            if estado == "salir":

                # El círculo se cierra y recién ahí se cierra el juego
                transicion.cerrar_circulo(pantalla, reloj)

                pygame.quit()
                sys.exit()

            # La primera vez (ningun nivel completado) PLAY entra directo
            # al nivel 1; el mapa de Buenos Aires aparece recien despues
            # de pasar el primer nivel
            if estado == "jugar" and cargar_mapa()[0] > 0:

                estado = "mapa"

        # --------------------------------------------------
        # MAPA DE BUENOS AIRES (15 NIVELES, LA BOCA -> LA BOCA)
        # --------------------------------------------------

        elif estado in ("mapa", "mapa_victoria"):

            musica.detener()

            # "mapa_victoria": se viene de terminar un nivel, el punto
            # se vuelve negro y salen los puntitos al siguiente
            estado = pantalla_mapa(
                pantalla,
                reloj,
                sprites_elegidos,
                animar_completado=(estado == "mapa_victoria")
            )

        # --------------------------------------------------
        # JUGAR CON EL PERSONAJE ELEGIDO
        # --------------------------------------------------

        elif estado == "jugar":

            musica.detener()

            # Cara del personaje en uso (para el HUD de vidas)
            cabeza_elegida = None

            for personaje in personajes:

                if personaje["sprites"] is sprites_elegidos:
                    cabeza_elegida = personaje.get("cabeza")

            # Nivel que toca jugar (los completados + 1)
            nivel_actual = cargar_mapa()[0] + 1

            estado = jugar(
                pantalla,
                reloj,
                sprites_elegidos,
                fuente_grande,
                fuente_media,
                cabeza_elegida,
                nivel_actual
            )

            # Perdio todas las vidas: hay que elegir personaje de nuevo
            if estado == "personajes":

                sprites_elegidos = None

        # --------------------------------------------------
        # INSTRUCCIONES
        # --------------------------------------------------

        elif estado == "instrucciones":

            musica.reproducir(musica.MUSICA_MENU)

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
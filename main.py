import pygame
import sys
import os
import math

from juego import jugar
from mapa import pantalla_mapa
from tutorial import jugar_tutorial
from eleccionPersonajes import seleccionar_personaje
from intro import pantallas_intro
from historia import escena_historia
from escena_dilolio import escena_dilolio
from escena_fantasma import escena_fantasma
from escenas_carlitos import llamada_carlitos
from pixel_font import FuentePixel
from fondo_menu import FondoMenuAnimado
import transicion
import musica
import sonidos
import pantalla_ajustes
import archivos
import partidas
from archivos import (
    ultima_partida,
    usar_partida,
    cargar_personaje,
    guardar_personaje,
    cargar_mapa,
    historia_vista,
    marcar_historia_vista,
    escena_dilolio_vista,
    escena_vista,
    marcar_escena_vista,
    marcar_escena_dilolio_vista,
    CARLITOS_PERDIDO,
    CARLITOS_ENCONTRADO,
    cargar_carlitos,
    guardar_carlitos
)


# ==========================================================
# INICIALIZAR PYGAME
# ==========================================================

pygame.init()

# VERSION SIN SONIDO: se apaga el audio
try:
    pygame.mixer.quit()
except pygame.error:
    pass


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

ANCHO, ALTO = 800, 600

# Ventana normal, agrandable, pantalla completa o sin bordes (se elige en
# AJUSTES; ver ventana.py)
import ventana
from archivos import cargar_modo_ventana

pantalla = ventana.aplicar(cargar_modo_ventana())


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
# ASPECTO HISTORICO DE CADA PERSONAJE
#
# No son personajes aparte: al elegir uno (BENJA, por ejemplo) aparece
# una pantalla para elegir su aspecto, NORMAL o HISTORICO. El historico
# vive en assets/personajes/<NOMBRE>/historico/ (sus poses de caminar,
# salto, etc. se generan con herramientas/generar_historicos.py).
# ==========================================================

# Nombre con el que aparece cada aspecto historico (si no figura aca
# se usa "<NOMBRE> HISTORICO")
NOMBRES_HISTORICOS = {
    "BENJA": "BENJUCHIS HISTORICO"
}

for personaje in personajes:

    nombre = personaje["nombre"]

    carpeta_historico = os.path.join(nombre, "historico")

    sprites_historico = crear_sprites_personaje(
        carpeta_historico,
        "final.png",
        "agachado.png",
        "saltando.png",
        "frame_1.png",
        "frame_2.png",
        "frame_3.png"
    )

    ruta_historico = os.path.join(
        "assets", "personajes", nombre, "historico"
    )

    personaje["historico"] = {
        "nombre": NOMBRES_HISTORICOS.get(
            nombre,
            nombre + " HISTORICO"
        ),
        "preview": sprites_historico["idle_der"],
        "seleccion": cargar_sprite(
            os.path.join(ruta_historico, "frente.png")
        ),
        "cabeza": cargar_cabeza(
            os.path.join(ruta_historico, "cabeza.png")
        ),
        "sprites": sprites_historico
    }


# Datos extra en cada juego de sprites: el nombre del personaje y su dibujo
# de frente (los usa el robot del jefe del nivel 15, ver escenas_robot.py)
for personaje in personajes:

    for aspecto in (personaje, personaje["historico"]):

        aspecto["sprites"]["nombre"] = personaje["nombre"]

        aspecto["sprites"]["frente"] = aspecto["seleccion"]


def buscar_aspecto(sprites):
    """
    Dado el diccionario de sprites en uso, devuelve (personaje, aspecto)
    donde aspecto es el propio personaje (normal) o su "historico".
    Devuelve (None, None) si no se encuentra.
    """

    for personaje in personajes:

        for aspecto in (personaje, personaje["historico"]):

            if aspecto["sprites"] is sprites:

                return personaje, aspecto

    return None, None


def nombre_para_guardar(sprites):
    """Texto que se guarda en personajes.txt: BENJA o BENJA:HISTORICO."""

    personaje, aspecto = buscar_aspecto(sprites)

    if personaje is None:

        return None

    if aspecto is personaje:

        return personaje["nombre"]

    return personaje["nombre"] + ":HISTORICO"


def sprites_guardados(texto):
    """Operacion inversa de nombre_para_guardar (None si no existe)."""

    if not texto:

        return None

    nombre, _, aspecto = texto.partition(":")

    for personaje in personajes:

        if personaje["nombre"] == nombre:

            if aspecto == "HISTORICO":

                return personaje["historico"]["sprites"]

            return personaje["sprites"]

    return None


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

    personaje["historico"]["sprites"]["enemigo"] = sprite_gagamba


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

        # El personaje cuenta como elegido con cualquiera de sus aspectos;
        # en el slot se ve la cabeza del aspecto que esta en uso
        aspecto = personaje

        if personaje["historico"]["sprites"] is sprites_elegidos:

            aspecto = personaje["historico"]

        es_elegido = aspecto["sprites"] is sprites_elegidos

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
        sprite = aspecto.get("cabeza", aspecto["preview"])

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

# Al tocar JUGAR: NUEVA PARTIDA / CARGAR PARTIDA / VOLVER
BOTON_NUEVA = BotonPixel(
    "boton_nueva_partida.png",
    ALTO_BOTON,
    MARGEN_IZQ,
    295
)

BOTON_CARGAR = BotonPixel(
    "boton_cargar_partida.png",
    ALTO_BOTON,
    MARGEN_IZQ,
    365
)

BOTON_VOLVER = BotonPixel(
    "boton_volver.png",
    ALTO_BOTON,
    MARGEN_IZQ,
    435
)


# ==========================================================
# ENGRANAJE DE AJUSTES (arriba a la derecha del menu)
#
# Se comporta como los otros botones: se pone blanco al apuntarlo y
# "respira" al apretarlo; despues se abre la pantalla de ajustes
# (volumen de la musica y de los efectos).
# ==========================================================

class BotonEngranaje(BotonPixel):

    def __init__(self, derecha, arriba):

        self.normal, self.blanco = pantalla_ajustes.crear_engranaje(3)

        self.todo_blanco = hacer_todo_blanco(self.normal)

        self.tamano = self.normal.get_size()

        self.rect = pygame.Rect((0, 0), self.tamano)

        self.rect.topright = (derecha, arriba)


BOTON_AJUSTES = BotonEngranaje(ANCHO - 24, 24)

# Titulo de la pantalla de ajustes
fuente_titulo_ajustes = FuentePixel(5)


def abrir_ajustes():
    """Pantalla de ajustes encima del fondo animado del menu."""

    global pantalla

    pantalla_ajustes.abrir(
        pantalla,
        reloj,
        lambda: FONDO_MENU.dibujar(pygame.display.get_surface()),
        fuente_titulo_ajustes,
        fuente_media,
        fuente_chica,
        FPS
    )

    # Si se cambio el modo de la ventana, la pantalla es otra
    pantalla = pygame.display.get_surface()


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

        BOTON_AJUSTES.dibujar(
            pantalla,
            libre and BOTON_AJUSTES.rect.collidepoint(mouse_pos),
            t_click if accion_click == "ajustes" else None
        )

        # Terminaron los 2 respiros -> recién ahí se ejecuta la acción
        if t_click is not None and t_click >= DURACION_ANIMACION_MS:

            if accion_click == "ajustes":

                # Los ajustes se abren encima del menu y al volver
                # el menu sigue como estaba
                accion_click = None
                inicio_click = None

                abrir_ajustes()

                continue

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
                    sonidos.reproducir("boton")

                    continue

                if BOTON_INSTRUCCIONES.rect.collidepoint(evento.pos):

                    accion_click = "instrucciones"
                    inicio_click = pygame.time.get_ticks()
                    sonidos.reproducir("boton")

                    continue

                if BOTON_EXIT.rect.collidepoint(evento.pos):

                    accion_click = "salir"
                    inicio_click = pygame.time.get_ticks()
                    sonidos.reproducir("boton")

                    continue

                if BOTON_AJUSTES.rect.collidepoint(evento.pos):

                    accion_click = "ajustes"
                    inicio_click = pygame.time.get_ticks()
                    sonidos.reproducir("boton")

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
                    sonidos.reproducir("boton")

                    continue

                if evento.key == pygame.K_c:

                    return "personajes"

        pygame.display.flip()

        reloj.tick(FPS)


def dibujar_menu_quieto(sprites_elegidos=None, con_barra=True):
    """Fondo del menu con el logo (para las pantallas de partidas)."""

    FONDO_MENU.dibujar(pantalla)

    pantalla.blit(
        LOGO,
        LOGO.get_rect(midleft=(MARGEN_IZQ - LOGO_MARGEN_TRANSPARENTE, 125))
    )

    if con_barra:

        dibujar_hotbar(pantalla, sprites_elegidos)


def menu_partidas(sprites_elegidos=None):
    """
    Lo que aparece al tocar JUGAR: NUEVA PARTIDA, CARGAR PARTIDA y VOLVER.
    Devuelve "nueva", "cargar" o "volver".
    """

    botones = [
        ("nueva", BOTON_NUEVA),
        ("cargar", BOTON_CARGAR),
        ("volver", BOTON_VOLVER),
    ]

    accion_click = None
    inicio_click = None
    elegido = 0

    while True:

        dibujar_menu_quieto(sprites_elegidos)

        mouse_pos = pygame.mouse.get_pos()

        t_click = (
            None
            if inicio_click is None
            else pygame.time.get_ticks() - inicio_click
        )

        libre = accion_click is None

        for i, (accion, boton) in enumerate(botones):

            if libre and boton.rect.collidepoint(mouse_pos):

                elegido = i

            boton.dibujar(
                pantalla,
                libre and i == elegido,
                t_click if accion_click == accion else None
            )

        if t_click is not None and t_click >= DURACION_ANIMACION_MS:

            return accion_click

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if accion_click is not None:

                continue

            if evento.type == pygame.MOUSEBUTTONDOWN:

                for accion, boton in botones:

                    if boton.rect.collidepoint(evento.pos):

                        accion_click = accion
                        inicio_click = pygame.time.get_ticks()
                        sonidos.reproducir("boton")

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:

                    return "volver"

                if evento.key in (pygame.K_UP, pygame.K_w):

                    elegido = (elegido - 1) % len(botones)

                if evento.key in (pygame.K_DOWN, pygame.K_s):

                    elegido = (elegido + 1) % len(botones)

                if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):

                    accion_click = botones[elegido][0]
                    inicio_click = pygame.time.get_ticks()
                    sonidos.reproducir("boton")

        pygame.display.flip()

        reloj.tick(FPS)


# Nivel antes del cual aparece la presentacion de Di Lolio
NIVEL_DILOLIO = 5

# Nivel antes del cual aparece la escena del FantasmaCastro (el primero con
# fantasma, ver NIVEL_FANTASMA_DESDE en juego.py)
NIVEL_FANTASMA_CASTRO = 10

# Al pasar este nivel un Compu Bro llama a los demas: encontro a Carlitos
NIVEL_LLAMADA_CARLITOS = 8


# ==========================================================
# FUNCIÓN PRINCIPAL
# ==========================================================

def main():

    estado = "intro"

    sprites_elegidos = None

    # A donde se va despues de elegir personaje ("menu" o "empezar")
    despues_de_elegir = "menu"

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

        # Entre el menu y NUEVA/CARGAR PARTIDA no hay transicion (es el
        # mismo fondo: solo cambian los botones)
        sin_transicion = {estado_mostrado, estado} <= {"menu", "partidas"}

        if estado_mostrado is not None and not sin_transicion:

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

            # Se deja en uso la ultima partida que se jugo (solo para ver
            # su personaje abajo): para jugar igual hay que elegirla con
            # CARGAR PARTIDA (y su contrasena)
            numero = ultima_partida()

            if numero is not None:

                usar_partida(numero)

                sprites_elegidos = sprites_guardados(cargar_personaje())

            estado = "menu"

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

                # ESC en la selección: se vuelve al menú
                estado = "menu"

            else:

                sprites_elegidos = elegido

                # Se guarda el personaje (y su aspecto) en personajes.txt
                # de la partida en uso
                guardar_personaje(nombre_para_guardar(elegido))

                # Partida nueva (o despues de perder): arranca a jugar
                estado = despues_de_elegir

            despues_de_elegir = "menu"

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

            # JUGAR: NUEVA PARTIDA o CARGAR PARTIDA
            if estado == "jugar":

                estado = "partidas"

            # C (cambiar personaje) solo con una partida en uso
            if estado == "personajes" and archivos.partida_actual is None:

                estado = "menu"

        # --------------------------------------------------
        # NUEVA PARTIDA / CARGAR PARTIDA
        # --------------------------------------------------

        elif estado == "partidas":

            eleccion = menu_partidas(sprites_elegidos)

            fondo = lambda: dibujar_menu_quieto(sprites_elegidos, con_barra=False)

            if eleccion == "nueva":

                if partidas.nueva_partida(pantalla, reloj, fondo):

                    # Partida nueva: se elige personaje y arranca
                    sprites_elegidos = None
                    despues_de_elegir = "empezar"
                    estado = "personajes"

                else:

                    estado = "partidas"

            elif eleccion == "cargar":

                if partidas.cargar_partida(pantalla, reloj, fondo):

                    sprites_elegidos = sprites_guardados(cargar_personaje())

                    if sprites_elegidos is None:

                        despues_de_elegir = "empezar"
                        estado = "personajes"

                    else:

                        estado = "empezar"

                else:

                    estado = "partidas"

            else:

                estado = "menu"

        # --------------------------------------------------
        # EMPEZAR LA PARTIDA EN USO
        # --------------------------------------------------

        elif estado == "empezar":

            # Al empezar la partida aparece la escena de la historia
            # (IKI avisa que se llevaron al princesito Mxroy), una vez
            # por partida
            if not historia_vista():

                estado = "historia"

            # Sin niveles completados se entra directo al nivel 1 (el
            # Instituto Huergo); el mapa aparece despues del primero
            elif cargar_mapa()[0] > 0:

                estado = "mapa"

            else:

                estado = "jugar"

            # (sin transicion extra: la pantalla no cambio)
            estado_mostrado = "intro"

        # --------------------------------------------------
        # HISTORIA (SOLO LA PRIMERA VEZ QUE SE TOCA PLAY)
        # --------------------------------------------------

        elif estado == "historia":

            # En las cinematicas la cancion del nivel se pausa
            musica.pausar()

            escena_historia(
                pantalla,
                reloj,
                fuente_grande,
                fuente_media
            )

            # Vista (o salteada con ESC): no vuelve a aparecer
            marcar_historia_vista()

            estado = "mapa" if cargar_mapa()[0] > 0 else "jugar"

        # --------------------------------------------------
        # MAPAS (30 NIVELES: BUENOS AIRES 1-15 Y CONURBANO 16-30)
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

            # Nivel 8 salteado desde el mapa con los trucos (F10): igual
            # aparece la llamada de Carlitos
            if (
                estado == "mapa_victoria"
                and cargar_mapa()[0] == NIVEL_LLAMADA_CARLITOS
                and cargar_carlitos() == CARLITOS_PERDIDO
            ):

                estado = "llamada_carlitos"

            # Despues de pasar el nivel 4, antes de entrar al 5, aparece
            # la presentacion de Di Lolio (una sola vez)
            if (
                estado == "jugar"
                and cargar_mapa()[0] + 1 == NIVEL_DILOLIO
                and not escena_dilolio_vista()
            ):

                estado = "dilolio"

            # Antes del primer nivel con fantasma: el FantasmaCastro (una
            # vez por partida)
            if (
                estado == "jugar"
                and cargar_mapa()[0] + 1 == NIVEL_FANTASMA_CASTRO
                and not escena_vista("fantasma_castro")
            ):

                estado = "fantasma_castro"

        # --------------------------------------------------
        # ESCENA DEL FANTASMA CASTRO (ANTES DEL NIVEL 10)
        # --------------------------------------------------

        elif estado == "fantasma_castro":

            # En las cinematicas la cancion del nivel se pausa
            musica.pausar()

            escena_fantasma(
                pantalla,
                reloj,
                fuente_grande,
                fuente_media
            )

            marcar_escena_vista("fantasma_castro")

            estado = "jugar"

        # --------------------------------------------------
        # PRESENTACION DE DI LOLIO (ANTES DEL NIVEL 5)
        # --------------------------------------------------

        elif estado == "dilolio":

            # En las cinematicas la cancion del nivel se pausa
            musica.pausar()

            escena_dilolio(
                pantalla,
                reloj,
                fuente_grande,
                fuente_media
            )

            marcar_escena_dilolio_vista()

            estado = "jugar"

        # --------------------------------------------------
        # JUGAR CON EL PERSONAJE ELEGIDO
        # --------------------------------------------------

        elif estado == "jugar":

            musica.detener()

            # Cara del personaje (y aspecto) en uso, para el HUD de vidas
            _, aspecto_en_uso = buscar_aspecto(sprites_elegidos)

            cabeza_elegida = (
                aspecto_en_uso.get("cabeza")
                if aspecto_en_uso is not None
                else None
            )

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
            # (y la partida vuelve a empezar, con sus cinematicas)
            if estado == "personajes":

                sprites_elegidos = None

                despues_de_elegir = "empezar"

            # Paso el nivel 8: llamada de Carlitos antes de volver al mapa
            if (
                estado == "mapa_victoria"
                and cargar_mapa()[0] == NIVEL_LLAMADA_CARLITOS
                and cargar_carlitos() == CARLITOS_PERDIDO
            ):

                estado = "llamada_carlitos"

        # --------------------------------------------------
        # LLAMADA: UN COMPU BRO ENCONTRO A CARLITOS (NIVEL 8)
        # --------------------------------------------------

        elif estado == "llamada_carlitos":

            # En las cinematicas la cancion del nivel se pausa
            musica.pausar()

            personaje_en_uso, aspecto_en_uso = buscar_aspecto(sprites_elegidos)

            llamada_carlitos(
                pantalla,
                reloj,
                fuente_grande,
                fuente_media,
                jugador=(
                    personaje_en_uso["nombre"]
                    if personaje_en_uso is not None
                    else "BENJA"
                ),
                historico=(
                    personaje_en_uso is not None
                    and aspecto_en_uso is not personaje_en_uso
                )
            )

            # Carlitos aparece en el mapa
            guardar_carlitos(CARLITOS_ENCONTRADO)

            estado = "mapa_victoria"

        # --------------------------------------------------
        # INSTRUCCIONES
        # --------------------------------------------------

        elif estado == "instrucciones":

            # El boton INSTRUCCIONES lleva al nivel tutorial (con el
            # personaje y aspecto elegidos). Al llegar a la bandera
            # gris, o con ESC, se vuelve al menu.
            estado = jugar_tutorial(
                pantalla,
                reloj,
                sprites_elegidos or personajes[0]["sprites"],
                fuente_grande,
                fuente_media
            )


# ==========================================================
# EJECUTAR
# ==========================================================

if __name__ == "__main__":

    main()
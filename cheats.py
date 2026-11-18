"""
MENU DE TRUCOS (cheats): se abre con F10 adentro de un nivel (tambien en
los jefes y en el castillo) o en el mapa. El juego queda en pausa mientras
esta abierto.

    VIDAS          <- / ->  sacar o sumar una vida
    PUNTOS         <- / ->  100 menos o 100 mas (con SHIFT: de a 1000)
    SALTEAR NIVEL  ENTER: da por pasado el nivel (en el mapa: el proximo)
    IR AL NIVEL    <- / -> elegir el nivel, ENTER para ir
    VOLVER         ENTER, F10 o ESC: cierra el menu

Flechas arriba / abajo (o W / S) para elegir, o el mouse.

Adentro de un nivel las vidas son las de ese nivel. En el mapa se cambian
las vidas extra (las que se compran en la tienda), que se suman al empezar
cada nivel.
"""

import sys

import pygame

import sonidos
from archivos import (
    TOTAL_NIVELES,
    cargar_mapa,
    cargar_puntos,
    cargar_vidas_extra,
    completar_nivel,
    guardar_mapa,
    guardar_puntos,
    guardar_vidas_extra,
)

TECLA = pygame.K_F10

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AMARILLO = (255, 214, 64)
VERDE = (90, 230, 120)
GRIS = (150, 150, 165)

FPS = 60

VIDAS_MAX = 99


def _fuente(escala):
    from pixel_font import FuentePixel
    return FuentePixel(escala)


def menu_cheats(pantalla, reloj, vidas=None, nivel=None, vidas_base=0):
    """
    Muestra el menu encima de lo que hay en pantalla.

    vidas:      vidas actuales del nivel (None = estamos en el mapa: se
                cambian las vidas extra)
    nivel:      nivel que se esta jugando (None = el mapa)
    vidas_base: en el mapa, cuantas vidas tiene un nivel sin las extra (se
                muestran sumadas)

    Devuelve un dict:
        "vidas":  las vidas que quedaron (en un nivel)
        "puntos": los puntos que quedaron (ya guardados)
        "accion": None, "saltear" o ("ir", numero_de_nivel)
    """

    fuente = _fuente(3)
    fuente_titulo = _fuente(4)
    fuente_chica = _fuente(2)

    en_mapa = vidas is None
    if en_mapa:
        vidas = vidas_base + cargar_vidas_extra()
        minimo_vidas = vidas_base
    else:
        minimo_vidas = 1

    puntos = cargar_puntos()
    completados = cargar_mapa()[0]
    destino = nivel if nivel is not None else min(completados + 1, TOTAL_NIVELES)

    opciones = ["VIDAS", "PUNTOS", "SALTEAR", "IR", "VOLVER"]
    elegida = 0
    fondo = pantalla.copy()
    velo = pygame.Surface(pantalla.get_size(), pygame.SRCALPHA)
    velo.fill((0, 0, 0, 170))
    ancho, alto = pantalla.get_size()

    panel = pygame.Rect(0, 0, 560, 430)
    panel.center = (ancho // 2, alto // 2)

    def rect_opcion(i):
        return pygame.Rect(panel.x + 30, panel.y + 90 + i * 56, panel.width - 60, 46)

    def texto_opcion(nombre):
        if nombre == "VIDAS":
            return "VIDAS:  < %d >" % vidas
        if nombre == "PUNTOS":
            return "PUNTOS:  < %d >" % puntos
        if nombre == "SALTEAR":
            if nivel is not None:
                return "SALTEAR ESTE NIVEL (%d)" % nivel
            if completados >= TOTAL_NIVELES:
                return "SALTEAR NIVEL (no quedan)"
            return "SALTEAR EL NIVEL %d" % (completados + 1)
        if nombre == "IR":
            return "IR AL NIVEL:  < %d >" % destino
        return "VOLVER"

    sonidos.reproducir("boton")

    def cambiar(direccion, mucho):
        nonlocal vidas, puntos, destino
        nombre = opciones[elegida]
        if nombre == "VIDAS":
            vidas = max(minimo_vidas, min(VIDAS_MAX, vidas + direccion))
        elif nombre == "PUNTOS":
            puntos = max(0, puntos + direccion * (1000 if mucho else 100))
        elif nombre == "IR":
            destino = (destino - 1 + direccion) % TOTAL_NIVELES + 1
        else:
            return
        sonidos.reproducir("boton")

    def terminar(accion=None):
        guardar_puntos(puntos)
        if en_mapa:
            guardar_vidas_extra(vidas - vidas_base)
        return {"vidas": vidas, "puntos": puntos, "accion": accion}

    def activar():
        nombre = opciones[elegida]
        if nombre == "VOLVER":
            return terminar()
        if nombre == "SALTEAR":
            if nivel is None and completados >= TOTAL_NIVELES:
                return None
            sonidos.reproducir("nivel_completo")
            return terminar("saltear")
        if nombre == "IR":
            sonidos.reproducir("boton")
            return terminar(("ir", destino))
        return None

    while True:

        reloj.tick(FPS)
        mucho = bool(pygame.key.get_mods() & pygame.KMOD_SHIFT)

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key in (TECLA, pygame.K_ESCAPE):
                    return terminar()
                if evento.key in (pygame.K_UP, pygame.K_w):
                    elegida = (elegida - 1) % len(opciones)
                if evento.key in (pygame.K_DOWN, pygame.K_s):
                    elegida = (elegida + 1) % len(opciones)
                if evento.key in (pygame.K_LEFT, pygame.K_a):
                    cambiar(-1, mucho)
                if evento.key in (pygame.K_RIGHT, pygame.K_d):
                    cambiar(1, mucho)
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                    resultado = activar()
                    if resultado is not None:
                        return resultado

            if evento.type == pygame.MOUSEMOTION:
                for i in range(len(opciones)):
                    if rect_opcion(i).collidepoint(evento.pos):
                        elegida = i

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button in (1, 3, 4, 5):
                for i in range(len(opciones)):
                    rect = rect_opcion(i)
                    if not rect.collidepoint(evento.pos):
                        continue
                    elegida = i
                    if evento.button == 4:
                        cambiar(1, mucho)
                    elif evento.button == 5:
                        cambiar(-1, mucho)
                    elif opciones[i] in ("VIDAS", "PUNTOS", "IR") and evento.button == 1 and evento.pos[0] < rect.centerx - 60:
                        cambiar(-1, mucho)
                    elif opciones[i] in ("VIDAS", "PUNTOS", "IR") and evento.button == 1 and evento.pos[0] > rect.centerx + 60:
                        cambiar(1, mucho)
                    elif evento.button == 1:
                        resultado = activar()
                        if resultado is not None:
                            return resultado

        # --------------------------------------------------
        # DIBUJAR
        # --------------------------------------------------

        pantalla.blit(fondo, (0, 0))
        pantalla.blit(velo, (0, 0))

        pygame.draw.rect(pantalla, NEGRO, panel.inflate(10, 10))
        pygame.draw.rect(pantalla, (30, 26, 50), panel)
        pygame.draw.rect(pantalla, AMARILLO, panel, 4)

        titulo = fuente_titulo.render("MENU DE TRUCOS", True, AMARILLO)
        pantalla.blit(titulo, titulo.get_rect(midtop=(panel.centerx, panel.y + 22)))

        for i, nombre in enumerate(opciones):
            rect = rect_opcion(i)
            activa = i == elegida
            pygame.draw.rect(pantalla, (70, 60, 110) if activa else (44, 38, 70), rect)
            pygame.draw.rect(pantalla, AMARILLO if activa else GRIS, rect, 3)
            texto = fuente.render(texto_opcion(nombre), True, BLANCO if activa else (210, 210, 220))
            pantalla.blit(texto, texto.get_rect(center=(rect.centerx, rect.centery + 2)))

        if opciones[elegida] in ("VIDAS", "PUNTOS", "IR"):
            ayuda = "<- / -> cambiar" + ("   (SHIFT: de a 1000)" if opciones[elegida] == "PUNTOS" else "") + ("   ENTER: ir" if opciones[elegida] == "IR" else "")
        else:
            ayuda = "ENTER: elegir"
        ayuda += "   F10 / ESC: cerrar"
        imagen = fuente_chica.render(ayuda, True, GRIS)
        pantalla.blit(imagen, imagen.get_rect(midbottom=(panel.centerx, panel.bottom - 8)))

        pygame.display.flip()


def ir_al_nivel(numero):
    """Deja el mapa listo para jugar el nivel `numero` (1 a 30)."""

    numero = max(1, min(TOTAL_NIVELES, int(numero)))
    guardar_mapa(numero - 1, None, None, [])


def saltear_nivel(nivel):
    """Da por pasado el nivel (lo mismo que llegar a la meta)."""

    completar_nivel(nivel)

import math
import sys

import pygame

from pixel_font import FuentePixel


FPS = 60

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (100, 100, 100)
GRIS_OSCURO = (70, 70, 70)
GRIS_CLARO = (180, 180, 180)
CELESTE = (135, 206, 235)


# ==========================================================
# AJUSTES DEL MENÚ DE SELECCIÓN
# ==========================================================

# Escala EXTRA sobre los sprites (que ya vienen x2)
ESCALA_ELEGIDO = 3.0      # el que está en el centro (de frente)
ESCALA_FONDO = 2.0        # los que quedan atrás (sprite común)

SEPARACION = 145          # distancia horizontal entre personajes
Y_SUELO_ELEGIDO = 430     # "piso" del personaje elegido
Y_SUELO_FONDO = 395       # los de atrás están más arriba (más lejos)

OSCURECER_FONDO = 130     # 255 = sin oscurecer

# Respiración del elegido (estilo selección de skins de Bedrock)
PERIODO_RESPIRO_MS = 2400
RESPIRO_ALTO = 0.035
RESPIRO_ANCHO = 0.012

# Qué tan rápido se desliza al cambiar de personaje (0 a 1)
SUAVIDAD = 0.18


def _oscurecer(superficie, valor):
    """Copia del sprite multiplicada por un gris (más oscuro)."""

    copia = superficie.copy()

    copia.fill(
        (valor, valor, valor, 255),
        special_flags=pygame.BLEND_RGBA_MULT
    )

    return copia


def _flecha(superficie, centro, lado, hover):
    """Flecha en pantalla. lado = -1 (izquierda) o 1 (derecha)."""

    cx, cy = centro

    puntos = [
        (cx + lado * 22, cy),
        (cx - lado * 14, cy - 30),
        (cx - lado * 14, cy + 30),
    ]

    pygame.draw.polygon(
        superficie,
        BLANCO if hover else GRIS_CLARO,
        puntos
    )

    pygame.draw.polygon(
        superficie,
        GRIS_OSCURO,
        puntos,
        4
    )

    # Zona de click
    return pygame.Rect(cx - 40, cy - 45, 80, 90)


def seleccionar_personaje(
    pantalla,
    reloj,
    ancho,
    alto,
    personajes,
    fuente_grande,
    fuente_media,
    fondo=None
):
    cantidad = len(personajes)

    # Con fondo de imagen los textos van en blanco (el piso es oscuro)
    color_texto = NEGRO if fondo is None else BLANCO


    objetivo = 0          # personaje elegido (contador sin límite)
    posicion = 0.0        # posición animada (se desliza hacia objetivo)

    fuente_titulo = FuentePixel(5)

    cx = ancho // 2

    while True:

        if fondo is not None:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(CELESTE)

        mouse_pos = pygame.mouse.get_pos()

        posicion += (objetivo - posicion) * SUAVIDAD

        if abs(objetivo - posicion) < 0.001:
            posicion = float(objetivo)

        # ==============================================
        # TÍTULO
        # ==============================================

        titulo = fuente_titulo.render(
            "SELECCIONAR PERSONAJE",
            True,
            BLANCO
        )

        pantalla.blit(
            titulo,
            titulo.get_rect(center=(cx, 60))
        )

        # ==============================================
        # PERSONAJES
        # ==============================================

        # Offset de cada personaje respecto al centro (circular)
        offsets = []

        for i in range(cantidad):

            d = (i - posicion + cantidad / 2) % cantidad - cantidad / 2

            offsets.append((abs(d), i, d))

        # Primero los más lejanos, al final el del centro
        offsets.sort(reverse=True)

        rects_click = {}

        t_ms = pygame.time.get_ticks()

        onda = math.sin(2 * math.pi * t_ms / PERIODO_RESPIRO_MS)

        for dist, i, d in offsets:

            personaje = personajes[i]

            cerca = min(dist, 1.0)          # 0 = centro, 1 = atrás

            x = cx + d * SEPARACION

            y_suelo = (
                Y_SUELO_ELEGIDO
                + (Y_SUELO_FONDO - Y_SUELO_ELEGIDO) * cerca
            )

            de_frente = dist < 0.5

            base = (
                personaje.get("seleccion", personaje["preview"])
                if de_frente
                else personaje["preview"]
            )

            factor = (
                ESCALA_ELEGIDO
                + (ESCALA_FONDO - ESCALA_ELEGIDO) * cerca
            )

            # Respiración: solo el que está en el centro
            peso = 1.0 - cerca

            factor_x = factor * (1 - RESPIRO_ANCHO * onda * peso)
            factor_y = factor * (1 + RESPIRO_ALTO * onda * peso)

            tam = (
                max(1, round(base.get_width() * factor_x)),
                max(1, round(base.get_height() * factor_y))
            )

            sprite = pygame.transform.scale(base, tam)

            # Más oscuro cuanto más atrás
            valor = round(255 - (255 - OSCURECER_FONDO) * cerca)

            if valor < 255:
                sprite = _oscurecer(sprite, valor)

            # Sombra en el piso
            ancho_sombra = int(sprite.get_width() * 0.9)

            sombra = pygame.Surface((ancho_sombra, 22), pygame.SRCALPHA)

            pygame.draw.ellipse(
                sombra,
                (0, 0, 0, int(70 - 25 * cerca)),
                sombra.get_rect()
            )

            pantalla.blit(
                sombra,
                sombra.get_rect(center=(x, y_suelo))
            )

            # Anclado en los pies (así respira sin "flotar")
            rect = sprite.get_rect(midbottom=(x, y_suelo + 4))

            pantalla.blit(sprite, rect)

            rects_click[i] = rect

        # Nombre del elegido
        indice_actual = round(posicion) % cantidad

        nombre = fuente_grande.render(
            personajes[indice_actual]["nombre"],
            True,
            color_texto
        )

        if nombre.get_width() > ancho - 260:

            nombre = pygame.transform.scale(
                nombre,
                (
                    ancho - 260,
                    round(nombre.get_height() * (ancho - 260) / nombre.get_width())
                )
            )

        pantalla.blit(
            nombre,
            nombre.get_rect(center=(cx, 495))
        )

        # ==============================================
        # FLECHAS EN PANTALLA
        # ==============================================

        rect_izq = _flecha(pantalla, (42, 300), -1, False)
        rect_der = _flecha(pantalla, (ancho - 42, 300), 1, False)

        if rect_izq.collidepoint(mouse_pos):
            _flecha(pantalla, (42, 300), -1, True)

        if rect_der.collidepoint(mouse_pos):
            _flecha(pantalla, (ancho - 42, 300), 1, True)

        # ==============================================
        # CONTROLES
        # ==============================================

        controles = fuente_media.render(
            "<  >   Elegir       ENTER   Seleccionar",
            True,
            color_texto
        )

        pantalla.blit(
            controles,
            controles.get_rect(center=(cx, alto - 40))
        )

        # ==============================================
        # EVENTOS
        # ==============================================

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key in (pygame.K_LEFT, pygame.K_a):
                    objetivo -= 1

                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    objetivo += 1

                elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return personajes[indice_actual]["sprites"]

                elif evento.key == pygame.K_ESCAPE:
                    return None

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if rect_izq.collidepoint(evento.pos):
                    objetivo -= 1

                elif rect_der.collidepoint(evento.pos):
                    objetivo += 1

                else:

                    # Click en un personaje: el del centro se elige,
                    # los de atrás pasan al centro
                    for i, rect in rects_click.items():

                        if rect.collidepoint(evento.pos):

                            if i == indice_actual:
                                return personajes[i]["sprites"]

                            d = (i - objetivo + cantidad / 2) % cantidad - cantidad / 2

                            objetivo += round(d)

                            break

        pygame.display.flip()
        reloj.tick(FPS)

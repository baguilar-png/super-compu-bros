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


# ==========================================================
# PERSONAJES HISTORICOS BLOQUEADOS
#
# Los aspectos historicos se ven como una silueta negra con un candado
# hasta terminar la mision de Carlitos (el reencuentro con Iki).
# ==========================================================

def historicos_desbloqueados():
    try:
        from archivos import historicos_desbloqueados as desbloqueados
        return desbloqueados()
    except Exception:
        return True


_siluetas = {}


def _silueta(imagen):
    """El mismo dibujo, todo negro (se calcula una vez por imagen)."""

    clave = id(imagen)

    if clave not in _siluetas:

        negra = pygame.Surface(imagen.get_size(), pygame.SRCALPHA)

        for y in range(imagen.get_height()):
            for x in range(imagen.get_width()):
                a = imagen.get_at((x, y))[3]
                if a:
                    negra.set_at((x, y), (12, 12, 16, a))

        _siluetas[clave] = (imagen, negra)

    return _siluetas[clave][1]


def _candado(superficie, centro, escala):
    """Candado pixel art (escala = tamano de cada pixel)."""

    u = max(2, int(escala))
    cx, cy = centro
    x0 = cx - 5 * u
    y0 = cy - 6 * u

    # Arco
    for rx, ry, rw, rh in ((2, 0, 6, 1), (1, 1, 1, 4), (8, 1, 1, 4)):
        pygame.draw.rect(superficie, NEGRO, (x0 + (rx - 1) * u, y0 + (ry - 1) * u, (rw + 2) * u, (rh + 2) * u))
    for rx, ry, rw, rh in ((2, 0, 6, 1), (1, 1, 1, 4), (8, 1, 1, 4)):
        pygame.draw.rect(superficie, (200, 200, 210), (x0 + rx * u, y0 + ry * u, rw * u, rh * u))

    # Cuerpo
    pygame.draw.rect(superficie, NEGRO, (x0 - u, y0 + 4 * u, 12 * u, 9 * u))
    pygame.draw.rect(superficie, (240, 196, 40), (x0, y0 + 5 * u, 10 * u, 7 * u))
    pygame.draw.rect(superficie, (255, 230, 120), (x0, y0 + 5 * u, 10 * u, u))
    pygame.draw.rect(superficie, (190, 140, 20), (x0, y0 + 11 * u, 10 * u, u))

    # Cerradura
    pygame.draw.rect(superficie, NEGRO, (x0 + 4 * u, y0 + 7 * u, 2 * u, 2 * u))
    pygame.draw.rect(superficie, NEGRO, (x0 + 4.5 * u, y0 + 9 * u, u, 2 * u))


# ==========================================================
# CARRUSEL (lo usan la seleccion de personaje y la de aspecto)
#
# El del centro esta adelante, de frente, grande y respirando; los otros
# quedan atras, de costado, mas chicos y mas oscuros. Se deslizan.
# ==========================================================

def _distancia(i, posicion, cantidad, circular):

    if circular:
        return (i - posicion + cantidad / 2) % cantidad - cantidad / 2

    return i - posicion


def _dibujar_carrusel(pantalla, cx, items, posicion, circular, separacion=SEPARACION):
    """
    items: [{"frente": imagen, "costado": imagen, "bloqueado": bool}]
    Devuelve {indice: rect} para los clicks.
    """

    cantidad = len(items)

    orden = []

    for i in range(cantidad):

        d = _distancia(i, posicion, cantidad, circular)

        orden.append((abs(d), i, d))

    # Primero los mas lejanos, al final el del centro
    orden.sort(reverse=True)

    onda = math.sin(2 * math.pi * pygame.time.get_ticks() / PERIODO_RESPIRO_MS)

    rects = {}

    for dist, i, d in orden:

        item = items[i]

        cerca = min(dist, 1.0)          # 0 = centro, 1 = atras

        x = cx + d * separacion

        y_suelo = Y_SUELO_ELEGIDO + (Y_SUELO_FONDO - Y_SUELO_ELEGIDO) * cerca

        de_frente = dist < 0.5

        base = item["frente"] if de_frente else item["costado"]

        if item.get("bloqueado"):
            base = _silueta(base)

        factor = ESCALA_ELEGIDO + (ESCALA_FONDO - ESCALA_ELEGIDO) * cerca

        # Respiracion: solo el que esta en el centro
        peso = 1.0 - cerca

        tam = (
            max(1, round(base.get_width() * factor * (1 - RESPIRO_ANCHO * onda * peso))),
            max(1, round(base.get_height() * factor * (1 + RESPIRO_ALTO * onda * peso)))
        )

        sprite = pygame.transform.scale(base, tam)

        # Mas oscuro cuanto mas atras
        valor = round(255 - (255 - OSCURECER_FONDO) * cerca)

        if valor < 255 and not item.get("bloqueado"):
            sprite = _oscurecer(sprite, valor)

        # Sombra en el piso
        sombra = pygame.Surface((int(sprite.get_width() * 0.9), 22), pygame.SRCALPHA)

        pygame.draw.ellipse(sombra, (0, 0, 0, int(70 - 25 * cerca)), sombra.get_rect())

        pantalla.blit(sombra, sombra.get_rect(center=(x, y_suelo)))

        # Anclado en los pies (asi respira sin "flotar")
        rect = sprite.get_rect(midbottom=(x, y_suelo + 4))

        pantalla.blit(sprite, rect)

        if item.get("bloqueado"):
            _candado(pantalla, rect.center, factor * 1.3)

        rects[i] = rect

    return rects


def _texto_grande(pantalla, fuente, texto, color, centro, ancho_max):

    imagen = fuente.render(texto, True, color)

    if imagen.get_width() > ancho_max:

        imagen = pygame.transform.scale(
            imagen,
            (ancho_max, round(imagen.get_height() * ancho_max / imagen.get_width()))
        )

    pantalla.blit(imagen, imagen.get_rect(center=centro))


# ==========================================================
# ELEGIR ASPECTO (NORMAL / HISTORICO)
#
# Aparece al elegir un personaje. Cada personaje tiene su aspecto normal
# (el propio diccionario del personaje) y, si tiene la clave "historico",
# ese aspecto. Igual que la seleccion de personaje: el del centro respira
# y los dos se deslizan.
# ==========================================================

def elegir_aspecto(
    pantalla,
    reloj,
    ancho,
    alto,
    personaje,
    fuente_media,
    fondo=None,
    fuente_grande=None
):
    """
    Devuelve el aspecto elegido (el propio personaje si es el normal, o
    personaje["historico"]), o None si se apreto ESC para volver.
    """

    aspectos = [personaje]

    if personaje.get("historico") is not None:

        aspectos.append(personaje["historico"])

    # Sin aspectos extra no hay nada que elegir
    if len(aspectos) == 1:

        return personaje

    bloqueado = not historicos_desbloqueados()

    nombres = ["NORMAL", "???" if bloqueado else personaje["historico"]["nombre"]]

    items = [
        {
            "frente": a.get("seleccion", a["preview"]),
            "costado": a["preview"],
            "bloqueado": bloqueado and k == 1,
        }
        for k, a in enumerate(aspectos)
    ]

    fuente_titulo = FuentePixel(5)

    fuente_nombre = fuente_grande or FuentePixel(6)

    color_texto = NEGRO if fondo is None else BLANCO

    cx = ancho // 2

    separacion = 230

    objetivo = 0

    posicion = 0.0

    aviso = 0.0     # tiempo que queda mostrando "BLOQUEADO"

    while True:

        dt = reloj.tick(FPS) / 1000.0

        aviso = max(0.0, aviso - dt)

        if fondo is not None:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(CELESTE)

        mouse_pos = pygame.mouse.get_pos()

        posicion += (objetivo - posicion) * SUAVIDAD

        if abs(objetivo - posicion) < 0.001:
            posicion = float(objetivo)

        # ----- titulo -----
        titulo = fuente_titulo.render("ELEGIR ASPECTO", True, BLANCO)

        pantalla.blit(titulo, titulo.get_rect(center=(cx, 60)))

        subtitulo = fuente_media.render(personaje["nombre"], True, BLANCO)

        pantalla.blit(subtitulo, subtitulo.get_rect(center=(cx, 108)))

        # ----- aspectos -----
        rects_click = _dibujar_carrusel(pantalla, cx, items, posicion, False, separacion)

        indice_actual = int(round(posicion))

        _texto_grande(pantalla, fuente_nombre, nombres[indice_actual], color_texto, (cx, 495), ancho - 260)

        if items[indice_actual]["bloqueado"]:

            pista = fuente_media.render("TERMINA LA MISION DE CARLITOS", True, (255, 214, 64) if aviso else BLANCO)

            pantalla.blit(pista, pista.get_rect(center=(cx, 535)))

        # ----- flechas -----
        hay_izq = objetivo > 0
        hay_der = objetivo < len(aspectos) - 1

        rect_izq = _flecha(pantalla, (42, 300), -1, False) if hay_izq else pygame.Rect(0, 0, 0, 0)
        rect_der = _flecha(pantalla, (ancho - 42, 300), 1, False) if hay_der else pygame.Rect(0, 0, 0, 0)

        if hay_izq and rect_izq.collidepoint(mouse_pos):
            _flecha(pantalla, (42, 300), -1, True)

        if hay_der and rect_der.collidepoint(mouse_pos):
            _flecha(pantalla, (ancho - 42, 300), 1, True)

        # ----- controles -----
        controles = fuente_media.render(
            "<  >  Elegir     ENTER  Listo     ESC  Volver",
            True,
            color_texto
        )

        pantalla.blit(controles, controles.get_rect(center=(cx, alto - 30)))

        # ----- eventos -----
        def confirmar(i):
            nonlocal aviso
            if items[i]["bloqueado"]:
                aviso = 1.2
                try:
                    import sonidos
                    sonidos.reproducir("golpe")
                except Exception:
                    pass
                return None
            return aspectos[i]

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key in (pygame.K_LEFT, pygame.K_a):
                    objetivo = max(0, objetivo - 1)

                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    objetivo = min(len(aspectos) - 1, objetivo + 1)

                elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    elegido = confirmar(indice_actual)
                    if elegido is not None:
                        return elegido

                elif evento.key == pygame.K_ESCAPE:
                    return None

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if hay_izq and rect_izq.collidepoint(evento.pos):
                    objetivo -= 1

                elif hay_der and rect_der.collidepoint(evento.pos):
                    objetivo += 1

                else:

                    for i, rect in rects_click.items():

                        if rect.collidepoint(evento.pos):

                            # Click en el del centro: se confirma
                            if i == indice_actual:
                                elegido = confirmar(i)
                                if elegido is not None:
                                    return elegido
                            else:
                                objetivo = i

                            break

        pygame.display.flip()


# ==========================================================
# SELECCIONAR PERSONAJE
# ==========================================================

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

    objetivo = 0          # personaje elegido (contador sin limite)
    posicion = 0.0        # posicion animada (se desliza hacia objetivo)

    fuente_titulo = FuentePixel(5)

    cx = ancho // 2

    items = [
        {"frente": p.get("seleccion", p["preview"]), "costado": p["preview"]}
        for p in personajes
    ]

    def aspecto_de(i):
        return elegir_aspecto(
            pantalla, reloj, ancho, alto, personajes[i],
            fuente_media, fondo, fuente_grande
        )

    while True:

        if fondo is not None:
            pantalla.blit(fondo, (0, 0))
        else:
            pantalla.fill(CELESTE)

        mouse_pos = pygame.mouse.get_pos()

        posicion += (objetivo - posicion) * SUAVIDAD

        if abs(objetivo - posicion) < 0.001:
            posicion = float(objetivo)

        # ----- titulo -----
        titulo = fuente_titulo.render("SELECCIONAR PERSONAJE", True, BLANCO)

        pantalla.blit(titulo, titulo.get_rect(center=(cx, 60)))

        # ----- personajes -----
        rects_click = _dibujar_carrusel(pantalla, cx, items, posicion, True)

        indice_actual = round(posicion) % cantidad

        _texto_grande(pantalla, fuente_grande, personajes[indice_actual]["nombre"], color_texto, (cx, 495), ancho - 260)

        # ----- flechas -----
        rect_izq = _flecha(pantalla, (42, 300), -1, False)
        rect_der = _flecha(pantalla, (ancho - 42, 300), 1, False)

        if rect_izq.collidepoint(mouse_pos):
            _flecha(pantalla, (42, 300), -1, True)

        if rect_der.collidepoint(mouse_pos):
            _flecha(pantalla, (ancho - 42, 300), 1, True)

        # ----- controles -----
        controles = fuente_media.render(
            "<  >   Elegir       ENTER   Seleccionar",
            True,
            color_texto
        )

        pantalla.blit(controles, controles.get_rect(center=(cx, alto - 40)))

        # ----- eventos -----
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

                    # Al elegir un personaje se elige tambien su aspecto
                    aspecto = aspecto_de(indice_actual)

                    if aspecto is not None:
                        return aspecto["sprites"]

                elif evento.key == pygame.K_ESCAPE:
                    return None

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if rect_izq.collidepoint(evento.pos):
                    objetivo -= 1

                elif rect_der.collidepoint(evento.pos):
                    objetivo += 1

                else:

                    # Click en un personaje: el del centro se elige,
                    # los de atras pasan al centro
                    for i, rect in rects_click.items():

                        if rect.collidepoint(evento.pos):

                            if i == indice_actual:

                                aspecto = aspecto_de(i)

                                if aspecto is not None:
                                    return aspecto["sprites"]

                                break

                            d = (i - objetivo + cantidad / 2) % cantidad - cantidad / 2

                            objetivo += round(d)

                            break

        pygame.display.flip()
        reloj.tick(FPS)

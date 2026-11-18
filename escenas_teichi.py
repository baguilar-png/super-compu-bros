"""
Cinematicas de LORD TEICHI (nivel 30) y el FINAL del juego.

    escena_teichi_antes()   en la sala del castillo, antes de la pelea:
                            "Nunca crei que llegarian a este punto..."; saca
                            la foto de los Compu Bros ("¿Estos son
                            ustedes?"), se rie, y la camara se desliza hasta
                            la jaula del princesito Mxroy, que pide ayuda
    escena_final()          despues de ganarle: Teichi se cae a la lava
                            ("¡NOOOOOOOOO!"), hace un pulgar para arriba antes
                            de hundirse, se rompe la jaula, Mxroy agradece,
                            y despues: el trofeo, "volvieron a ser 6",
                            "continuara en..." y el logo de SUPER COMPU BROS 2

ENTER / ESPACIO / click pasan el texto (y adelantan las animaciones), ESC
saltea.
"""

import math
import random
import sys

import pygame

import sonidos
from historia import (
    BLANCO,
    CUADRO,
    FPS,
    NEGRO,
    TEXTO_ANCHO,
    TEXTO_X,
    TEXTO_Y,
    Retrato,
    _cargar,
    _dibujar_cuadro,
    _dibujar_flechita,
    _dibujar_signo,
    _dibujar_texto_con_sombra,
    _escalar,
    _partir_en_lineas,
)

ANCHO, ALTO = 800, 600

LETRAS_POR_SEGUNDO = 38

COLOR_TEICHI = (120, 30, 40)
COLOR_MXROY = (130, 50, 160)
AMARILLO = (255, 214, 64)

# La sala se ve mas arriba que en la pelea, asi el cuadro de texto no tapa
SUBIR = 110

ESCALA_MXROY = 2           # igual que el jugador en la pelea
RUTA_MXROY = "assets/personajes/MXROY/frente.png"
# La foto que saca Teichi antes de la pelea ("¿Estos son ustedes?")
RUTA_FOTO = "assets/historia/foto_teichi.png"


# ==========================================================
# JAULA DE MXROY (tambien se ve en la pelea)
# ==========================================================

def imagen_mxroy():
    return _escalar(_cargar(RUTA_MXROY), ESCALA_MXROY)


def caminar_mxroy(escala=ESCALA_MXROY, a_la_izquierda=True):
    """Poses de caminar de Mxroy (salen del molde de Bauto, como las de Iki)."""
    poses = []
    for k in (1, 2, 3, 2):
        img = _escalar(_cargar("assets/personajes/MXROY/frame_%d.png" % k), escala)
        poses.append(pygame.transform.flip(img, True, False) if a_la_izquierda else img)
    return poses


def dibujar_jaula(superficie, x, piso, t, mxroy, rota=False, saltar=False):
    """Jaula de hierro con el princesito adentro. x: centro, piso: base."""

    ancho, alto = 96, 124
    base = pygame.Rect(0, 0, ancho + 16, 14)
    base.midbottom = (x, piso)

    # Mxroy adentro (saltando y moviendose de los nervios). Con la jaula
    # rota, a Mxroy lo dibuja la escena (sale caminando)
    if mxroy is not None:
        salto = int(abs(math.sin(t * 7)) * 8) if saltar else 0
        vaiven = int(math.sin(t * 3) * 3)
        superficie.blit(mxroy, mxroy.get_rect(midbottom=(x + vaiven, base.top - salto)))

    if rota:
        pygame.draw.rect(superficie, NEGRO, base.inflate(4, 4))
        pygame.draw.rect(superficie, (70, 70, 80), base)
        return

    techo = pygame.Rect(0, 0, ancho + 16, 14)
    techo.midbottom = (x, base.top - alto)
    for r in (base, techo):
        pygame.draw.rect(superficie, NEGRO, r.inflate(4, 4))
        pygame.draw.rect(superficie, (70, 70, 80), r)
        pygame.draw.line(superficie, (130, 130, 145), r.topleft, r.topright, 2)
    # Cadena hasta el techo
    for cy in range(techo.top - 260, techo.top, 12):
        pygame.draw.ellipse(superficie, (90, 90, 100), (x - 4, cy, 8, 12), 2)
    # Barrotes
    for k in range(6):
        bx = techo.left + 6 + k * (ancho + 4) // 5
        pygame.draw.rect(superficie, NEGRO, (bx - 3, techo.bottom, 7, alto))
        pygame.draw.rect(superficie, (96, 96, 110), (bx - 2, techo.bottom, 5, alto))
        pygame.draw.line(superficie, (150, 150, 165), (bx - 1, techo.bottom), (bx - 1, base.top), 1)
    # Candado dorado
    candado = pygame.Rect(0, 0, 22, 18)
    candado.center = (x, base.top - alto // 2)
    pygame.draw.circle(superficie, NEGRO, (candado.centerx, candado.top), 9, 4)
    pygame.draw.rect(superficie, NEGRO, candado.inflate(4, 4))
    pygame.draw.rect(superficie, (240, 196, 40), candado)
    pygame.draw.rect(superficie, NEGRO, (candado.centerx - 2, candado.centery - 3, 4, 7))


# ==========================================================
# DIBUJOS SUELTOS
# ==========================================================

def _pulgar(superficie, x, y, escala=3):
    """Mano con el pulgar para arriba (y el brazo para abajo)."""
    e = escala
    piel = (234, 172, 124)
    sombra = (196, 128, 88)
    # (x, y, ancho, alto) en pixeles del dibujo, con (0,0) arriba a la izquierda
    partes = [
        (2, 0, 2, 4),     # pulgar
        (0, 4, 7, 5),     # puno
        (1, 9, 5, 12),    # brazo
    ]
    for px, py, w, h in partes:
        pygame.draw.rect(superficie, NEGRO, (x + (px - 1) * e, y + (py - 1) * e, (w + 2) * e, (h + 2) * e))
    for px, py, w, h in partes:
        pygame.draw.rect(superficie, piel, (x + px * e, y + py * e, w * e, h * e))
    # Dedos (rayitas) y sombra
    for k in range(3):
        pygame.draw.rect(superficie, sombra, (x + 4 * e, y + (5 + k * 1.3) * e, 3 * e, max(1, e // 2)))
    pygame.draw.rect(superficie, sombra, (x + 1 * e, y + 9 * e, 1 * e, 12 * e))


def _trofeo(superficie, cx, cy, escala=8, brillo=0.0):
    """Copa dorada pixel art (13x16) centrada en (cx, cy)."""
    DIBUJO = [
        "..#########..",
        "##.ooooooo.##",
        "#.#oOOoooo#.#",
        "#.#oOoooooo#.#",
        ".##ooooooo##.",
        "...#ooooo#...",
        "....#ooo#....",
        ".....#o#.....",
        ".....#o#.....",
        "....#ooo#....",
        "...#######...",
        "..#ooooooo#..",
        "..#ddddddd#..",
        "..#########..",
    ]
    e = escala
    w = max(len(f) for f in DIBUJO)
    x0 = cx - w * e // 2
    y0 = cy - len(DIBUJO) * e // 2
    colores = {
        "#": (60, 36, 0),
        "o": (246, 196, 40),
        "O": (255, 246, 190),
        "d": (190, 130, 20),
        ".": None,
    }
    for fy, fila in enumerate(DIBUJO):
        for fx, c in enumerate(fila):
            color = colores.get(c)
            if color:
                pygame.draw.rect(superficie, color, (x0 + fx * e, y0 + fy * e, e, e))
    # Estrella en la copa
    sx, sy = cx, y0 + 3 * e
    pygame.draw.polygon(superficie, (255, 255, 255), [
        (sx, sy - e), (sx + e // 2, sy - e // 3), (sx + e, sy - e // 4), (sx + e // 2, sy + e // 4),
        (sx + e * 2 // 3, sy + e), (sx, sy + e // 2), (sx - e * 2 // 3, sy + e), (sx - e // 2, sy + e // 4),
        (sx - e, sy - e // 4), (sx - e // 2, sy - e // 3)])
    # Destellos
    if brillo > 0:
        for k in range(6):
            a = brillo * 2 + k * math.pi / 3
            r = w * e * 0.75
            px = cx + int(math.cos(a) * r)
            py = cy + int(math.sin(a) * r * 0.8)
            pygame.draw.rect(superficie, (255, 240, 160), (px - 2, py - 8, 4, 16))
            pygame.draw.rect(superficie, (255, 240, 160), (px - 8, py - 2, 16, 4))


def _silueta_cabeza(imagen):
    return imagen


class _Particula:

    def __init__(self, x, y, vx, vy, color, tam, vida, gravedad=1000, giro=False):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.color, self.tam, self.vida = color, tam, vida
        self.gravedad = gravedad
        self.alto = tam * (5 if giro else 1)

    def actualizar(self, dt):
        self.vida -= dt
        self.vy += self.gravedad * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, NEGRO, (int(self.x) - 1, int(self.y) - 1, self.tam + 2, self.alto + 2))
        pygame.draw.rect(superficie, self.color, (int(self.x), int(self.y), self.tam, self.alto))


# ==========================================================
# MOTOR DE LAS ESCENAS (guion con dialogos y animaciones)
# ==========================================================

def _correr_guion(pantalla, reloj, fuente_media, pasos, retratos, dibujar, al_empezar=None, avisos=None):
    """
    pasos: ("dice", quien, texto) o ("hace", accion, duracion).
    retratos: {quien: (imagen, escala, color)}.
    dibujar(lienzo, accion, progreso, t, dt, quien_habla, escribiendo)
    Devuelve False si se apreto ESC.
    """

    avisos = avisos or {}
    retr = {q: Retrato(q, img) for q, (img, _, _) in retratos.items()}
    lineas = []
    for paso in pasos:
        if paso[0] == "dice":
            lineas.append(("dice", paso[1], _partir_en_lineas(fuente_media, paso[2], TEXTO_ANCHO)))
        else:
            lineas.append(paso)

    lienzo = pygame.Surface((ANCHO, ALTO))
    chica = type(fuente_media)(2)
    banco = []
    hablando = None
    letras = 0.0
    total = 0
    t = 0.0
    t_paso = 0.0
    t_dialogo = 0.0
    indice = -1

    def empezar(i):
        nonlocal indice, t_paso, letras, total, hablando, t_dialogo
        indice = i
        t_paso = 0.0
        if i >= len(lineas):
            return
        paso = lineas[i]
        if paso[0] == "hace":
            if al_empezar:
                al_empezar(paso[1])
            return
        quien = paso[1]
        if i == 0 or lineas[i - 1][0] != "dice":
            t_dialogo = t
        letras = 0.0
        total = sum(len(p) for p in paso[2])
        if quien != hablando:
            if hablando is not None and hablando not in banco:
                banco.append(hablando)
            if quien in banco:
                banco.remove(quien)
            hablando = quien
            retr[quien].mandar_a(CUADRO.x + 112, CUADRO.bottom - 14, retratos[quien][1], gris=False)
            x = CUADRO.right - 10
            for nombre in banco[-3:]:
                ancho = retr[nombre].color.get_width() * 2
                retr[nombre].mandar_a(x - ancho // 2, CUADRO.y - 12, 2, gris=True)
                x -= ancho + 10

    empezar(0)

    try:
        while indice < len(lineas):

            dt = min(reloj.tick(FPS) / 1000.0, 0.05)
            t += dt
            t_paso += dt

            avanzar = False
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return False
                    if evento.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                        avanzar = True
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    avanzar = True

            paso = lineas[indice]

            if paso[0] == "dice":
                if letras < total:
                    letras = min(total, letras + LETRAS_POR_SEGUNDO * dt)
                if avanzar:
                    if letras < total:
                        letras = total
                    else:
                        sonidos.reproducir("boton")
                        empezar(indice + 1)
                        continue
                accion, progreso = None, 0.0
            else:
                accion, duracion = paso[1], paso[2]
                if avanzar:
                    t_paso = duracion
                progreso = min(1.0, t_paso / duracion) if duracion else 1.0
                if t_paso >= duracion:
                    dibujar(lienzo, accion, 1.0, t, dt, None, False)
                    empezar(indice + 1)
                    continue

            escribiendo = paso[0] == "dice" and letras < total
            if escribiendo:
                sonidos.reproducir_en_bucle("teclado")
            else:
                sonidos.detener("teclado")

            for r in retr.values():
                r.actualizar(dt)

            quien = paso[1] if paso[0] == "dice" else None
            dibujar(lienzo, accion, progreso, t, dt, quien, escribiendo)
            pantalla.blit(lienzo, (0, 0))

            if paso[0] == "dice":
                partes = paso[2]
                velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
                velo.fill((0, 0, 0, int(90 * min(1.0, (t - t_dialogo) / 0.25))))
                pantalla.blit(velo, (0, 0))
                _dibujar_cuadro(pantalla, fuente_media, quien, retratos[quien][2])
                for nombre in banco[-3:]:
                    retr[nombre].dibujar(pantalla)
                salto = int(abs(math.sin(t / 0.32 * math.pi)) * 3) if escribiendo else 0
                retr[quien].dibujar(pantalla, salto)
                restantes = int(letras)
                alto_linea = fuente_media.get_height() - 4
                for k, parte in enumerate(partes):
                    if restantes <= 0:
                        break
                    _dibujar_texto_con_sombra(pantalla, fuente_media, parte[:restantes], BLANCO,
                                              (TEXTO_X, TEXTO_Y + k * alto_linea))
                    restantes -= len(parte)
                if not escribiendo:
                    _dibujar_flechita(pantalla, t)
                if quien in avisos:
                    imagen = chica.render(avisos[quien], True, (200, 200, 220))
                    pantalla.blit(imagen, imagen.get_rect(bottomleft=(TEXTO_X + 240, CUADRO.y + 2)))

            ayuda = chica.render("ESC: saltear", True, (230, 230, 230))
            pantalla.blit(ayuda, ayuda.get_rect(topright=(ANCHO - 10, 8)))
            pygame.display.flip()
    finally:
        sonidos.detener("teclado")

    return True


_tmp_sala = []


def _dibujar_sala(lienzo, fondo, camara_x):
    """La sala del castillo corrida para arriba (abajo se repite el piso)."""
    if not _tmp_sala:
        _tmp_sala.append(pygame.Surface((ANCHO, ALTO)))
    tmp = _tmp_sala[0]
    fondo.dibujar(tmp, int(camara_x))
    lienzo.blit(tmp, (0, -SUBIR))
    alto_tira = 60
    y = ALTO - SUBIR
    while y < ALTO:
        lienzo.blit(tmp, (0, y), (0, ALTO - alto_tira, ANCHO, alto_tira))
        y += alto_tira


def _sombra(superficie, x, y, ancho):
    s = pygame.Surface((ancho, 14), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 0, 0, 100), s.get_rect())
    superficie.blit(s, s.get_rect(center=(int(x), int(y))))


def _fundido(pantalla, alfa):
    if alfa <= 0:
        return
    negro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    negro.fill((0, 0, 0, int(255 * max(0.0, min(1.0, alfa)))))
    pantalla.blit(negro, (0, 0))


def _retrato_jugador(sprites_jugador):
    frente = sprites_jugador.get("frente") or sprites_jugador["idle_der"]
    return pygame.transform.scale(frente, (frente.get_width() // 2, frente.get_height() // 2))


# ==========================================================
# ANTES DE LA PELEA
# ==========================================================

def escena_teichi_antes(pantalla, reloj, fuente_media, fondo, sprites_teichi, sprites_jugador, x_jaula, piso_pantalla):
    """
    fondo: el de la sala (FondoCastillo). x_jaula: x de la jaula en la sala.
    piso_pantalla: y del piso en la pelea (jefes.PISO_PANTALLA).
    """

    piso = piso_pantalla - SUBIR
    mxroy = imagen_mxroy()
    foto = _cargar(RUTA_FOTO)
    # Se agranda sin deformarla (la foto puede no ser cuadrada)
    proporcion = foto.get_height() / foto.get_width()
    ANCHO_FOTO = 360
    foto_grande = pygame.transform.smoothscale(foto, (ANCHO_FOTO, int(ANCHO_FOTO * proporcion)))
    foto_chica = pygame.transform.smoothscale(foto, (40, int(40 * proporcion)))
    jugador = sprites_jugador["idle_der"]

    X_JUGADOR = 260
    X_TEICHI = 640
    camara = {"x": 0.0, "desde": 0.0}
    estado = {"foto": 0.0, "risa": False}
    cam_final = x_jaula - ANCHO // 2

    def al_empezar(accion):
        if accion == "deslizar":
            camara["desde"] = camara["x"]
            sonidos.reproducir("salto")
        if accion == "sacar_foto":
            sonidos.reproducir("carta")
        if accion == "risa":
            estado["risa"] = True

    def dibujar(lienzo, accion, p, t, dt, quien, escribiendo):
        fondo.actualizar(dt)

        if accion == "deslizar":
            # Se desliza suave hasta la jaula
            k = p * p * (3 - 2 * p)
            camara["x"] = camara["desde"] + (cam_final - camara["desde"]) * k
        cam = camara["x"]

        if accion == "sacar_foto":
            estado["foto"] = p
        elif accion == "guardar_foto":
            estado["foto"] = 1 - p

        _dibujar_sala(lienzo, fondo, cam)

        # Jaula con Mxroy (salta y grita cuando habla)
        dibujar_jaula(lienzo, x_jaula - cam, piso, t, mxroy, saltar=(quien == "MXROY" or accion == "deslizar"))

        # Jugador
        _sombra(lienzo, X_JUGADOR - cam, piso, jugador.get_width())
        lienzo.blit(jugador, jugador.get_rect(midbottom=(int(X_JUGADOR - cam), piso)))

        # Teichi: respira; cuando habla salta un poquito; levanta la foto; se rie
        if estado["foto"] > 0.05:
            pose = "tirar"
        elif estado["risa"] and quien == "LORD TEICHI":
            pose = "brazos_arriba" if int(t * 6) % 2 else "quieto"
        else:
            pose = "respirar" if int(t * 1.6) % 2 else "quieto"
        img = sprites_teichi[pose][1]       # mira a la izquierda
        salto = int(abs(math.sin(t / 0.32 * math.pi)) * 5) if (quien == "LORD TEICHI" and escribiendo) else 0
        _sombra(lienzo, X_TEICHI - cam, piso, 110)
        rect = img.get_rect(midbottom=(int(X_TEICHI - cam), piso - salto))
        lienzo.blit(img, rect)
        if estado["foto"] > 0.05:
            lienzo.blit(foto_chica, foto_chica.get_rect(center=(rect.right - 34, rect.top + 30)))

        # Risa: "JA JA JA" alrededor
        if estado["risa"] and quien == "LORD TEICHI" and escribiendo:
            for k in range(3):
                fase = (t * 1.5 + k / 3) % 1.0
                _dibujar_signo(lienzo, fuente_media, "JA", AMARILLO,
                               rect.centerx + (k - 1) * 60, int(rect.top - 10 - fase * 50))

        # La foto grande en el medio de la pantalla
        if estado["foto"] > 0.01:
            f = estado["foto"]
            escala = 0.4 + 0.6 * f
            img_foto = pygame.transform.smoothscale(
                foto_grande, (int(foto_grande.get_width() * escala), int(foto_grande.get_height() * escala)))
            marco = img_foto.get_rect(center=(ANCHO // 2, int(200 + (1 - f) * 120)))
            pygame.draw.rect(lienzo, NEGRO, marco.inflate(22, 22))
            pygame.draw.rect(lienzo, BLANCO, marco.inflate(16, 16))
            lienzo.blit(img_foto, marco)

    pasos = [
        ("dice", "LORD TEICHI", "Nunca creí que llegarían a este punto."),
        ("dice", "LORD TEICHI", "Pero hoy tengo la ventaja de casa y..."),
        ("hace", "sacar_foto", 0.9),
        ("dice", "LORD TEICHI", "¿Estos son ustedes?"),
        ("hace", "guardar_foto", 0.6),
        ("hace", "risa", 0.01),
        ("dice", "LORD TEICHI", "JAJAJAJAJA."),
        ("dice", "LORD TEICHI", "Esto será muuuy fácil."),
        ("hace", "deslizar", 2.6),
        ("dice", "MXROY", "¡AYUDA! ¡Compu Bros, sáquenme de acá!"),
        ("hace", "fin", 0.8),
    ]

    retratos = {
        "LORD TEICHI": (_cargar("assets/personajes/TEICHI/teichi cabeza.png"), 6, COLOR_TEICHI),
        "MXROY": (_cargar(RUTA_MXROY), 6, COLOR_MXROY),
    }

    def dibujar_con_fin(lienzo, accion, p, t, dt, quien, escribiendo):
        dibujar(lienzo, accion, p, t, dt, quien, escribiendo)
        if accion == "fin":
            _fundido(lienzo, p)

    _correr_guion(pantalla, reloj, fuente_media, pasos, retratos, dibujar_con_fin, al_empezar)


# ==========================================================
# DESPUES DE LA PELEA: EL FINAL
# ==========================================================

def escena_final(pantalla, reloj, fuente_media, fondo, sprites_teichi, sprites_jugador, x_jaula, piso_pantalla, borde_lava):
    """
    borde_lava: x donde empieza el piso de la sala (a la izquierda es lava).
    """

    piso = piso_pantalla - SUBIR
    lava_y = piso + 16
    mxroy = imagen_mxroy()
    jugador = sprites_jugador["idle_der"]
    caminar = sprites_jugador["caminar_der"]
    nombre_jugador = sprites_jugador.get("nombre", "COMPU BRO")

    X_TEICHI_INICIO = borde_lava + 70
    X_TEICHI_LAVA = borde_lava - 80
    X_JUGADOR = borde_lava + 330
    X_JUGADOR_JAULA = x_jaula - 200

    mxroy_camina = caminar_mxroy()
    mxroy_quieto = imagen_mxroy()

    s = {
        "mxroy_x": float(x_jaula),
        "cam": 0.0,
        "teichi_x": float(X_TEICHI_INICIO),
        "teichi_y": float(piso),
        "hundido": 0.0,         # cuanto se hundio (px)
        "en_lava": False,
        "pulgar": 0.0,          # cuanto se ve la mano (px)
        "jugador_x": float(X_JUGADOR),
        "jaula_rota": False,
        "particulas": [],
        "burbujas": [],
        "grito": 0.0,
        "temblor": 0.0,
    }
    cam_jaula = x_jaula - ANCHO // 2 - 60

    def al_empezar(accion):
        if accion == "cae":
            sonidos.reproducir("salto")
            s["grito"] = 2.6
        if accion == "romper":
            s["jaula_rota"] = True
            s["temblor"] = 0.4
            sonidos.reproducir("explosion")
            for _ in range(28):
                a = random.uniform(-math.pi, 0)
                v = random.uniform(250, 600)
                s["particulas"].append(_Particula(
                    x_jaula + random.uniform(-60, 60), piso - random.uniform(20, 160),
                    math.cos(a) * v, math.sin(a) * v,
                    random.choice([(96, 96, 110), (130, 130, 145), (70, 70, 80)]),
                    5, 1.6, giro=True))
            s["particulas"].append(_Particula(x_jaula, piso - 84, 120, -380, (240, 196, 40), 14, 1.6))
        if accion == "pulgar":
            sonidos.reproducir("boton")

    def dibujar(lienzo, accion, p, t, dt, quien, escribiendo):
        fondo.actualizar(dt)
        s["grito"] = max(0.0, s["grito"] - dt)
        s["temblor"] = max(0.0, s["temblor"] - dt)

        # --- Teichi se cae a la lava ---
        if accion == "tambalea":
            s["teichi_x"] = X_TEICHI_INICIO - 40 * p + math.sin(t * 14) * 5
        elif accion == "cae":
            x0 = X_TEICHI_INICIO - 40
            s["teichi_x"] = x0 + (X_TEICHI_LAVA - x0) * p
            # Salto en arco hacia la lava
            s["teichi_y"] = piso - math.sin(p * math.pi) * 90 + p * 30
            if p >= 0.99 and not s["en_lava"]:
                s["en_lava"] = True
        elif accion == "hundir_1":
            s["hundido"] = 30 + 50 * p
        elif accion == "hundir_2":
            s["hundido"] = 80 + 70 * p
            s["pulgar"] = 60 * min(1.0, p * 2)
        elif accion == "pulgar":
            s["hundido"] = 150 + 20 * p
        elif accion == "hundir_3":
            s["pulgar"] = 60 * (1 - p)
            s["hundido"] = 170 + 40 * p

        if s["en_lava"] and accion != "cae":
            s["teichi_y"] = lava_y + s["hundido"] - 30
            if random.random() < 0.3:
                s["burbujas"].append([s["teichi_x"] + random.uniform(-50, 50), lava_y + 6, random.uniform(3, 7), 0.6])

        # --- Camara: va hasta la jaula ---
        if accion == "ir_jaula":
            k = p * p * (3 - 2 * p)
            s["cam"] = cam_jaula * k
            s["jugador_x"] = X_JUGADOR + (X_JUGADOR_JAULA - X_JUGADOR) * k

        cam = s["cam"] + (random.randint(-5, 5) if s["temblor"] > 0 else 0)

        _dibujar_sala(lienzo, fondo, cam)

        # Teichi (antes de hundirse del todo)
        if s["hundido"] < 200 or not s["en_lava"]:
            if not s["en_lava"]:
                pose = "brazos_arriba" if accion == "cae" else ("agachado" if int(t * 3) % 2 else "quieto")
            else:
                pose = "brazos_arriba"
            img = sprites_teichi[pose][1]
            rect = img.get_rect(midbottom=(int(s["teichi_x"] - cam), int(s["teichi_y"])))
            if s["en_lava"]:
                # Solo se ve lo que esta arriba de la lava
                visible = max(0, lava_y + 8 - rect.top)
                if visible > 0:
                    lienzo.blit(img, rect.topleft, (0, 0, img.get_width(), visible))
            else:
                if accion != "cae":
                    _sombra(lienzo, rect.centerx, piso, 110)
                lienzo.blit(img, rect)

        # Pulgar para arriba saliendo de la lava
        if s["pulgar"] > 1:
            mano = pygame.Surface((30, 90), pygame.SRCALPHA)
            _pulgar(mano, 4, 4, 3)
            alto_visible = int(s["pulgar"])
            mx = int(s["teichi_x"] - cam) + 10
            lienzo.blit(mano, (mx, lava_y + 8 - alto_visible), (0, 0, 30, alto_visible))

        for b in s["burbujas"]:
            b[1] -= 30 * dt
            b[3] -= dt
            pygame.draw.circle(lienzo, (255, 200, 80), (int(b[0] - cam), int(b[1])), int(b[2]))
        s["burbujas"] = [b for b in s["burbujas"] if b[3] > 0]

        # Jaula
        if accion == "mxroy_sale":
            s["mxroy_x"] = x_jaula + (X_JUGADOR_JAULA + 110 - x_jaula) * p
        dibujar_jaula(lienzo, x_jaula - cam, piso, t, None if s["jaula_rota"] else mxroy, rota=s["jaula_rota"],
                      saltar=(quien == "MXROY"))
        if s["jaula_rota"]:
            # Mxroy libre: sale caminando hasta el jugador (y salta cuando habla)
            if accion == "mxroy_sale":
                img_m = mxroy_camina[int(t * 8) % len(mxroy_camina)]
            else:
                img_m = mxroy_quieto
            salto_m = int(abs(math.sin(t * 7)) * 8) if (quien == "MXROY" or accion == "festejo") else 0
            _sombra(lienzo, s["mxroy_x"] - cam, piso, img_m.get_width())
            lienzo.blit(img_m, img_m.get_rect(midbottom=(int(s["mxroy_x"] - cam), piso - salto_m)))

        # Jugador (camina hasta la jaula)
        img = caminar[int(t * 8) % len(caminar)] if accion == "ir_jaula" else jugador
        _sombra(lienzo, s["jugador_x"] - cam, piso, img.get_width())
        lienzo.blit(img, img.get_rect(midbottom=(int(s["jugador_x"] - cam), piso)))

        for q in s["particulas"]:
            q.actualizar(dt)
            if q.vida > 0:
                q.x -= 0  # (se mueven en coordenadas del mundo)
                pygame.draw.rect(lienzo, NEGRO, (int(q.x - cam) - 1, int(q.y) - 1, q.tam + 2, q.alto + 2))
                pygame.draw.rect(lienzo, q.color, (int(q.x - cam), int(q.y), q.tam, q.alto))
        s["particulas"] = [q for q in s["particulas"] if q.vida > 0]

        # El grito, grande arriba
        if s["grito"] > 0:
            grande = type(fuente_media)(6)
            temblor = random.randint(-3, 3)
            _dibujar_signo(lienzo, grande, "¡NOOOOOOOOO!", (255, 80, 60), ANCHO // 2 + temblor, 150)

        if accion == "fin":
            _fundido(lienzo, p)

    pasos = [
        ("hace", "tambalea", 1.4),
        ("hace", "cae", 1.1),
        ("hace", "hundir_1", 1.4),
        ("dice", "LORD TEICHI", "Volveré más fuerte la próxima vez..."),
        ("hace", "hundir_2", 1.6),
        ("hace", "pulgar", 1.6),
        ("hace", "hundir_3", 1.2),
        ("hace", "pausa", 1.0),
        ("hace", "ir_jaula", 3.0),
        ("hace", "romper", 1.2),
        ("hace", "mxroy_sale", 1.6),
        ("hace", "festejo", 0.8),
        ("dice", "MXROY", "¡Gracias, Compu Bros! Gracias por todo el esfuerzo."),
        ("dice", nombre_jugador, "Quedate tranquilo, vos sabés que te queremos mucho."),
        ("hace", "fin", 1.0),
    ]

    retratos = {
        "LORD TEICHI": (_cargar("assets/personajes/TEICHI/teichi cabeza.png"), 6, COLOR_TEICHI),
        "MXROY": (_cargar(RUTA_MXROY), 6, COLOR_MXROY),
        nombre_jugador: (_retrato_jugador(sprites_jugador), 6, (40, 70, 170)),
    }

    _correr_guion(pantalla, reloj, fuente_media, pasos, retratos, dibujar, al_empezar)

    _pantallas_finales(pantalla, reloj, fuente_media)


# ==========================================================
# PANTALLAS NEGRAS DEL FINAL
# ==========================================================

def _esperar(pantalla, reloj, dibujar, minimo=1.2, maximo=7.0):
    """Muestra dibujar(t) hasta ENTER (despues de 'minimo') o 'maximo'."""
    t = 0.0
    salida = None
    while True:
        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER, pygame.K_ESCAPE):
                if t > minimo and salida is None:
                    salida = t
            if evento.type == pygame.MOUSEBUTTONDOWN and t > minimo and salida is None:
                salida = t
        if salida is None and t > maximo:
            salida = t
        pantalla.fill(NEGRO)
        dibujar(pantalla, t)
        _fundido(pantalla, max(1 - t / 0.6, 0) if salida is None else (t - salida) / 0.6)
        pygame.display.flip()
        if salida is not None and t - salida >= 0.6:
            return


def _texto_centrado(pantalla, fuente, texto, color, y):
    imagen = fuente.render(texto, True, color)
    if imagen.get_width() > ANCHO - 40:
        imagen = pygame.transform.scale(imagen, (ANCHO - 40, int(imagen.get_height() * (ANCHO - 40) / imagen.get_width())))
    pantalla.blit(imagen, imagen.get_rect(center=(ANCHO // 2, y)))


def _pantallas_finales(pantalla, reloj, fuente_media):

    grande = type(fuente_media)(5)
    media = fuente_media

    # 1) El trofeo
    sonidos.reproducir("nivel_completo")

    def trofeo(p, t):
        rebote = int(abs(math.sin(t * 2.2)) * 10)
        _trofeo(p, ANCHO // 2, 250 - rebote, 12, brillo=t)
        _texto_centrado(p, grande, "¡SALVASTE A MXROY!", AMARILLO, 440)
        _texto_centrado(p, media, "SOS UN VERDADERO COMPU BRO", BLANCO, 500)

    _esperar(pantalla, reloj, trofeo, 1.5, 8.0)

    # 2) El grupo volvio a estar completo: los bros, Mxroy e Iki
    cabezas = []
    for ruta in (
        "assets/personajes/BAUTO/bauto cabeza.png",
        "assets/personajes/BENJA/benja cabeza.png",
        "assets/personajes/CASTRO/castro cabeza.png",
        "assets/personajes/POSHO/Posho cabeza.png",
        "assets/personajes/THIAGO/thiago cabeza.png",
        "assets/personajes/MXROY/cabeza.png",
        "assets/personajes/IKI/cabeza.png",
    ):
        try:
            cabezas.append(_escalar(_cargar(ruta), 4))
        except (pygame.error, FileNotFoundError):
            pass

    def completo(p, t):
        _texto_centrado(p, media, "POR FIN EL GRUPO", BLANCO, 170)
        _texto_centrado(p, media, "VOLVIÓ A ESTAR COMPLETO", BLANCO, 215)
        ancho_total = sum(c.get_width() for c in cabezas) + 16 * (len(cabezas) - 1)
        x = ANCHO // 2 - ancho_total // 2
        for k, c in enumerate(cabezas):
            # Aparecen de a una
            if t > 0.4 + k * 0.25:
                salto = int(abs(math.sin(t * 3 + k)) * 6)
                p.blit(c, (x, 330 - c.get_height() - salto))
            x += c.get_width() + 16

    _esperar(pantalla, reloj, completo, 2.6, 8.0)

    # 3) Cinematica: se llevan a Iki
    escena_secuestro_iki(pantalla, reloj, fuente_media)

    # 4) "Continuara en..." y el logo con el 2
    try:
        logo = _cargar("assets/fondos/logo_2.png")
        logo = pygame.transform.scale(logo, (logo.get_width() * 5, logo.get_height() * 5))
    except (pygame.error, FileNotFoundError):
        logo = grande.render("SUPER COMPU BROS 2", True, AMARILLO)

    azar = random.Random(4)
    estrellas = [(azar.randrange(ANCHO), azar.randrange(ALTO), azar.random()) for _ in range(90)]

    def logo_2(p, t):
        p.fill((8, 10, 30))
        for x, y, f in estrellas:
            if (t * 1.5 + f) % 1.0 < 0.8:
                pygame.draw.rect(p, (220, 220, 255), (x, y, 2, 2))
        _texto_centrado(p, grande, "CONTINUARÁ EN...", AMARILLO, 110)
        if t > 1.0:
            escala = min(1.0, 0.6 + (t - 1.0) * 0.8)
            img = pygame.transform.scale(logo, (int(logo.get_width() * escala), int(logo.get_height() * escala)))
            p.blit(img, img.get_rect(center=(ANCHO // 2, ALTO // 2 + 40)))

    sonidos.reproducir("carta")
    _esperar(pantalla, reloj, logo_2, 3.0, 12.0)


# ==========================================================
# SE LLEVAN A IKI (el gancho para SUPER COMPU BROS 2)
# ==========================================================

ORDEN_GRUPO = ["BAUTO", "BENJA", "CASTRO", "MXROY", "POSHO", "THIAGO", "IKI"]


def escena_secuestro_iki(pantalla, reloj, fuente_media):
    """
    Todos juntos en el pasillo del Huergo festejando. Se corta la luz, en
    la oscuridad aparecen dos ojos rojos y se oye a Iki gritar mientras lo
    arrastran. Vuelve la luz: Iki no esta y cae una nota.
    """

    from historia import PERSONAJES, PISO_Y, ESCALA_ESCENA, _cargar_fondo, _dibujar_globo

    fondo = _cargar_fondo(ANCHO, ALTO)
    globo = type(fuente_media)(2)
    signo = type(fuente_media)(4)

    rutas = {n: PERSONAJES[n][0] for n in ORDEN_GRUPO if n in PERSONAJES}
    rutas["MXROY"] = RUTA_MXROY
    frente = {n: _cargar(r) for n, r in rutas.items()}
    en_escena = {n: _escalar(img, ESCALA_ESCENA) for n, img in frente.items()}
    xs = {n: 75 + k * 108 for k, n in enumerate(ORDEN_GRUPO)}

    s = {"iki_x": float(xs["IKI"]), "iki_esta": True, "nota_y": None, "luz": 1.0, "sorpresa": 0.0, "ojos": 0.0}

    def al_empezar(accion):
        if accion == "apagon":
            sonidos.reproducir("golpe")
        if accion == "arrastre":
            sonidos.reproducir("fantasma")
        if accion == "luz":
            s["iki_esta"] = False
            s["sorpresa"] = 2.0
            sonidos.reproducir("boton")
        if accion == "nota":
            s["nota_y"] = -40.0
            sonidos.reproducir("carta")

    def dibujar(lienzo, accion, p, t, dt, quien, escribiendo):
        s["sorpresa"] = max(0.0, s["sorpresa"] - dt)

        if accion == "apagon":
            # La luz titila y se corta
            s["luz"] = 0.0 if p > 0.7 else (0.25 if int(t * 14) % 2 else 1.0)
            s["ojos"] = max(0.0, (p - 0.75) / 0.25)
        elif accion == "arrastre":
            s["luz"] = 0.0
            s["iki_x"] = xs["IKI"] + 260 * p * p
        elif accion == "luz":
            s["luz"] = min(1.0, p * 2)
            s["ojos"] = 0.0
        if accion == "nota" and s["nota_y"] is not None:
            s["nota_y"] = -40 + (PISO_Y - 10 + 40) * p

        lienzo.blit(fondo, (0, 0))

        for nombre in ORDEN_GRUPO:
            if nombre == "IKI" and not s["iki_esta"]:
                continue
            img = en_escena[nombre]
            x = s["iki_x"] if nombre == "IKI" else xs[nombre]
            salto = 0
            if accion == "festejo" or (accion is None and quien is None):
                salto = int(abs(math.sin(t * 6 + xs[nombre] * 0.01)) * 10)
            elif quien == nombre and escribiendo:
                salto = int(abs(math.sin(t / 0.32 * math.pi)) * 7)
            _sombra(lienzo, x, PISO_Y - 1, 70)
            rect = img.get_rect(midbottom=(int(x), PISO_Y - salto))
            lienzo.blit(img, rect)
            if s["sorpresa"] > 0 and nombre != "IKI":
                _dibujar_signo(lienzo, signo, "!", AMARILLO, rect.centerx, rect.top - 6)

        if accion == "festejo":
            _dibujar_globo(lienzo, globo, xs["BENJA"], PISO_Y - 110, "¡VAMOS!")
            _dibujar_globo(lienzo, globo, xs["POSHO"], PISO_Y - 110, "¡AGUANTE!")

        # La nota en el piso, donde estaba Iki
        if s["nota_y"] is not None:
            nx = xs["IKI"] + math.sin(t * 5) * (8 if accion == "nota" else 0)
            nota = pygame.Rect(0, 0, 34, 24)
            nota.center = (int(nx), int(s["nota_y"]))
            pygame.draw.rect(lienzo, NEGRO, nota.inflate(4, 4))
            pygame.draw.rect(lienzo, (236, 220, 178), nota)
            for k in range(3):
                pygame.draw.line(lienzo, (120, 90, 60), (nota.x + 5, nota.y + 6 + k * 6), (nota.right - 6, nota.y + 6 + k * 6), 2)

        # Oscuridad
        if s["luz"] < 1.0:
            negro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            negro.fill((0, 0, 0, int(245 * (1 - s["luz"]))))
            lienzo.blit(negro, (0, 0))

        # Ojos rojos en la oscuridad y el grito de Iki
        if s["ojos"] > 0 or accion == "arrastre":
            ox = int(s["iki_x"] + 60)
            oy = PISO_Y - 110
            for dx in (-14, 14):
                pygame.draw.rect(lienzo, (255, 30, 30), (ox + dx - 5, oy, 10, 6))
                pygame.draw.rect(lienzo, (255, 200, 200), (ox + dx - 2, oy + 1, 3, 3))
        if accion == "arrastre":
            # Iki, apenas una silueta que se lleva la oscuridad
            img = en_escena["IKI"].copy()
            img.fill((40, 40, 50, 255), special_flags=pygame.BLEND_RGBA_MULT)
            lienzo.blit(img, img.get_rect(midbottom=(int(s["iki_x"]), PISO_Y)))
            _dibujar_signo(lienzo, signo, "¡AAAAAH!", BLANCO, min(ANCHO - 150, int(s["iki_x"]) - 30), PISO_Y - 120)

        if accion == "fin":
            _fundido(lienzo, p)

    pasos = [
        ("hace", "festejo", 2.0),
        ("dice", "IKI", "¡Por fin estamos todos juntos otra vez!"),
        ("dice", "MXROY", "Gracias por rescatarme, chicos. Los extrañé un montón."),
        ("dice", "BENJA", "¡Esto hay que festejarlo!"),
        ("hace", "apagon", 1.6),
        ("hace", "arrastre", 1.6),
        ("hace", "luz", 0.8),
        ("dice", "MXROY", "¿Y... Iki?"),
        ("hace", "nota", 1.2),
        ("dice", "THIAGO", "Hay una nota... \"Si quieren volver a ver a Iki, vengan a buscarlo. Att: ???\""),
        ("dice", "CASTRO", "¡No puede ser! ¡Otra vez no!"),
        ("dice", "BAUTO", "¡Vamos, Compu Bros! ¡A rescatar a Iki!"),
        ("hace", "fin", 1.0),
    ]

    retratos = {n: (frente[n], 6, PERSONAJES[n][1]) for n in ORDEN_GRUPO if n in PERSONAJES}
    retratos["MXROY"] = (frente["MXROY"], 6, COLOR_MXROY)

    _correr_guion(pantalla, reloj, fuente_media, pasos, retratos, dibujar, al_empezar)

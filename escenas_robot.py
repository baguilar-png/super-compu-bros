"""
El ROBOT del nivel 15 (La Bombonera) y sus dos cinematicas.

El jefe del nivel 15 es un robot copia del personaje que estas usando (del
tamano del cubo): ROBO-BENJA, ROBO-CASTRO... Sus dibujos se arman solos a
partir de los sprites del jugador (sprites_robot): la piel pasa a metal, la
ropa y el pelo quedan metalizados, los ojos se prenden en rojo y le sale una
antena.

    escena_robot_llega()      antes de la pelea: el robot llega volando a la
                              Bombonera y Lord Teichi cuenta (por los
                              parlantes del estadio) que quiere hacer con el
    escena_robot_destruido()  despues de ganar: el robot destruido en la
                              cancha y Teichi por los parlantes

ENTER / ESPACIO / click pasan el texto, ESC saltea.
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
    _partir_en_lineas,
)

ANCHO, ALTO = 800, 600

# El cubo media 32 de alto x4: el robot (35 x4) es del mismo tamano
ESCALA_ROBOT = 4

COLOR_TEICHI = (120, 30, 40)
COLOR_ROBOT = (70, 90, 120)
OJO_ROJO = (255, 40, 40)

LETRAS_POR_SEGUNDO = 38


def nombre_robot(sprites_jugador):
    return "ROBO-" + str(sprites_jugador.get("nombre", "BRO"))


# ==========================================================
# DIBUJOS DEL ROBOT
# ==========================================================

def _luz(r, g, b):
    return 0.3 * r + 0.59 * g + 0.11 * b


def _es_piel(r, g, b):
    return r >= 150 and g >= 90 and r > g > b and r - b >= 40


def _robotizar(imagen):
    """
    Pasa un sprite (tamano original, sin agrandar) a robot. Devuelve una
    imagen un poco mas alta: arriba va la antena.
    """

    caja = imagen.get_bounding_rect()
    imagen = imagen.subsurface(caja).copy()
    w, h = imagen.get_size()

    piel = [[False] * h for _ in range(w)]
    oscuro = [[False] * h for _ in range(w)]
    for x in range(w):
        for y in range(h):
            r, g, b, a = imagen.get_at((x, y))
            if a:
                piel[x][y] = _es_piel(r, g, b)
                oscuro[x][y] = _luz(r, g, b) < 60

    ALTO_ANTENA = 5
    robot = pygame.Surface((w, h + ALTO_ANTENA), pygame.SRCALPHA)

    alto_cabeza = int(h * 0.45)

    for x in range(w):
        for y in range(h):
            r, g, b, a = imagen.get_at((x, y))
            if not a:
                continue
            v = _luz(r, g, b)
            if oscuro[x][y]:
                # Pupilas (oscuro rodeado de piel, en la cara): luces rojas
                vecinos_piel = sum(
                    1 for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
                    if 0 <= x + dx < w and 0 <= y + dy < h and piel[x + dx][y + dy]
                )
                if y < alto_cabeza and vecinos_piel >= 3:
                    color = (150, 0, 0)
                else:
                    color = (18, 20, 28)
            elif y < alto_cabeza and r > 215 and g > 215 and b > 215 and any(
                0 <= x + dx < w and 0 <= y + dy < h and piel[x + dx][y + dy]
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
            ):
                # Lo blanco de los ojos: luces rojas
                color = OJO_ROJO
            elif piel[x][y]:
                # Piel: acero
                color = (int(v * 0.70 + 50), int(v * 0.74 + 55), int(v * 0.80 + 62))
            elif r > 215 and g > 215 and b > 215:
                color = (222, 230, 242)
            else:
                # Ropa y pelo: el mismo color, metalizado (un poco gris y azulado)
                color = (
                    int(r * 0.62 + v * 0.30 + 8),
                    int(g * 0.62 + v * 0.30 + 12),
                    int(b * 0.62 + v * 0.30 + 22),
                )
            color = tuple(max(0, min(255, c)) for c in color)
            robot.set_at((x, y + ALTO_ANTENA), color + (a,))

    # Remaches en el borde de la cara (cada 3 pixeles de piel del borde)
    for y in range(1, alto_cabeza):
        fila = [x for x in range(w) if piel[x][y]]
        if fila and y % 3 == 0:
            for x in (fila[0], fila[-1]):
                robot.set_at((x, y + ALTO_ANTENA), (90, 96, 110, 255))

    # Antena arriba de la cabeza
    arriba = [x for x in range(w) if imagen.get_at((x, 0))[3]]
    cx = arriba[len(arriba) // 2] if arriba else w // 2
    for y in range(1, ALTO_ANTENA):
        robot.set_at((cx, y), (18, 20, 28, 255))
    for dx, dy in ((-1, 0), (0, 0), (-1, -1), (0, -1)):
        if 0 <= cx + dx < w:
            robot.set_at((cx + dx, 1 + dy if 1 + dy >= 0 else 0), OJO_ROJO + (255,))

    return robot


def _original(imagen):
    """Los sprites del juego estan agrandados x2: vuelve al tamano original."""
    return pygame.transform.scale(imagen, (max(1, imagen.get_width() // 2), max(1, imagen.get_height() // 2)))


def _agrandar(imagen, escala=ESCALA_ROBOT):
    return pygame.transform.scale(imagen, (imagen.get_width() * escala, imagen.get_height() * escala))


def sprites_robot(sprites_jugador):
    """
    Las mismas poses que Teichi y el cubo (ver jefes.Jefe.pose), armadas con
    los dibujos del personaje del jugador. Devuelve {pose: (der, izq)}.
    """

    caminar = sprites_jugador["caminar_der"]
    quieto = _robotizar(_original(sprites_jugador["idle_der"]))
    paso_1 = _robotizar(_original(caminar[0]))
    paso_2 = _robotizar(_original(caminar[1]))
    paso_3 = _robotizar(_original(caminar[2 % len(caminar)]))
    salto = _robotizar(_original(sprites_jugador["saltar_der"]))
    agachado = _robotizar(_original(sprites_jugador["agachado_der"]))

    respirar = pygame.transform.scale(quieto, (quieto.get_width() + 1, quieto.get_height() - 1))

    cuadros = {
        "quieto": quieto,
        "respirar": respirar,
        "caminar_1": paso_1,
        "caminar_2": paso_2,
        "caminar_3": paso_3,
        "caminar_4": paso_2,
        "tirar": salto,
        "agachado": agachado,
        "brazos_arriba": salto,
        "empujar": pygame.transform.rotate(paso_2, -12),
        "correr_2": pygame.transform.rotate(paso_3, -8),
    }

    sprites = {}
    for pose, img in cuadros.items():
        grande = _agrandar(img)
        sprites[pose] = (grande, pygame.transform.flip(grande, True, False))
    return sprites


def frente_robot(sprites_jugador):
    """El robot de frente (tamano original), para el retrato."""
    frente = sprites_jugador.get("frente")
    if frente is None:
        return _robotizar(_original(sprites_jugador["idle_der"]))
    return _robotizar(_original(frente))


def _silueta(imagen):
    negra = imagen.copy()
    for x in range(negra.get_width()):
        for y in range(negra.get_height()):
            a = negra.get_at((x, y))[3]
            if a:
                negra.set_at((x, y), (8, 8, 12, a))
    return negra


# ==========================================================
# DIALOGO (como el de las otras escenas)
# ==========================================================

class _Dialogo:
    """Cuadro de texto con retrato grande; los que ya hablaron, al costado."""

    def __init__(self, fuente, lineas, retratos, escalas, colores, avisos=None):
        self.fuente = fuente
        self.lineas = [(q, _partir_en_lineas(fuente, txt, TEXTO_ANCHO)) for q, txt in lineas]
        self.retratos = retratos
        self.escalas = escalas
        self.colores = colores
        self.avisos = avisos or {}
        self.indice = -1
        self.letras = 0.0
        self.total = 0
        self.hablando = None
        self.banco = []
        self.t0 = 0.0

    @property
    def escribiendo(self):
        return 0 <= self.indice < len(self.lineas) and self.letras < self.total

    @property
    def activo(self):
        return 0 <= self.indice < len(self.lineas)

    def empezar(self, t):
        self.t0 = t
        self._pasar(0)

    def _pasar(self, i):
        self.indice = i
        if i >= len(self.lineas):
            return
        quien, partes = self.lineas[i]
        self.letras = 0.0
        self.total = sum(len(p) for p in partes)
        if quien != self.hablando:
            if self.hablando is not None and self.hablando not in self.banco:
                self.banco.append(self.hablando)
            if quien in self.banco:
                self.banco.remove(quien)
            self.hablando = quien
            self.retratos[quien].mandar_a(CUADRO.x + 112, CUADRO.bottom - 14, self.escalas[quien], gris=False)
            x = CUADRO.right - 10
            for nombre in self.banco[-3:]:
                ancho = self.retratos[nombre].color.get_width() * 2
                self.retratos[nombre].mandar_a(x - ancho // 2, CUADRO.y - 12, 2, gris=True)
                x -= ancho + 10

    def actualizar(self, dt, avanzar):
        """True cuando se termino el dialogo."""
        for r in self.retratos.values():
            r.actualizar(dt)
        if not self.activo:
            return self.indice >= len(self.lineas)
        if self.letras < self.total:
            self.letras = min(self.total, self.letras + LETRAS_POR_SEGUNDO * dt)
        if avanzar:
            if self.letras < self.total:
                self.letras = self.total
            else:
                sonidos.reproducir("boton")
                self._pasar(self.indice + 1)
        if self.escribiendo:
            sonidos.reproducir_en_bucle("teclado")
        else:
            sonidos.detener("teclado")
        return self.indice >= len(self.lineas)

    def dibujar(self, pantalla, t):
        if not self.activo:
            return
        quien, partes = self.lineas[self.indice]
        velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        velo.fill((0, 0, 0, int(90 * min(1.0, (t - self.t0) / 0.25))))
        pantalla.blit(velo, (0, 0))
        _dibujar_cuadro(pantalla, self.fuente, quien, self.colores[quien])
        for nombre in self.banco[-3:]:
            self.retratos[nombre].dibujar(pantalla)
        salto = int(abs(math.sin(t / 0.32 * math.pi)) * 3) if self.escribiendo else 0
        self.retratos[quien].dibujar(pantalla, salto)
        restantes = int(self.letras)
        alto_linea = self.fuente.get_height() - 4
        for k, parte in enumerate(partes):
            if restantes <= 0:
                break
            _dibujar_texto_con_sombra(pantalla, self.fuente, parte[:restantes], BLANCO,
                                      (TEXTO_X, TEXTO_Y + k * alto_linea))
            restantes -= len(parte)
        if not self.escribiendo:
            _dibujar_flechita(pantalla, t)
        aviso = self.avisos.get(quien)
        if aviso:
            chica = type(self.fuente)(2)
            imagen = chica.render(aviso, True, (200, 200, 220))
            pantalla.blit(imagen, imagen.get_rect(bottomleft=(TEXTO_X + 240, CUADRO.y + 2)))


# ==========================================================
# LA BOMBONERA (fondo, parlantes, particulas)
# ==========================================================

# En las cinematicas la cancha se ve mas arriba que en la pelea, asi el
# cuadro de texto no tapa a nadie
SUBIR_CANCHA = 100


def _bombonera():
    import jefes
    terreno = jefes.TerrenoSimple(ANCHO, [(0, ANCHO)], [], inicio_x=100)
    return jefes.FondoBombonera(terreno), jefes.PISO_PANTALLA - SUBIR_CANCHA


_estadio_tmp = []


def _dibujar_estadio(lienzo, fondo):
    """La Bombonera corrida para arriba; abajo se repite el pasto."""
    if not _estadio_tmp:
        _estadio_tmp.append(pygame.Surface((ANCHO, ALTO)))
    tmp = _estadio_tmp[0]
    fondo.dibujar(tmp)
    lienzo.blit(tmp, (0, -SUBIR_CANCHA))
    alto_pasto = 70
    y = ALTO - SUBIR_CANCHA
    while y < ALTO:
        lienzo.blit(tmp, (0, y), (0, ALTO - alto_pasto, ANCHO, alto_pasto))
        y += alto_pasto


def _dibujar_parlantes(pantalla, t, hablando):
    """Parlantes colgados de las torres de luz; con ondas si Teichi habla."""
    for x in (60, 620):
        caja = pygame.Rect(0, 0, 40, 34)
        caja.midtop = (x, 22)
        pygame.draw.line(pantalla, (40, 40, 46), (x, 0), (x, 22), 3)
        pygame.draw.rect(pantalla, NEGRO, caja.inflate(6, 6))
        pygame.draw.rect(pantalla, (50, 50, 58), caja)
        for k in range(2):
            pygame.draw.circle(pantalla, (20, 20, 24), (caja.centerx, caja.top + 9 + k * 16), 7)
            pygame.draw.circle(pantalla, (90, 90, 100), (caja.centerx, caja.top + 9 + k * 16), 3)
        if hablando:
            for k in range(3):
                fase = (t * 3 + k * 0.33) % 1.0
                radio = int(18 + fase * 40)
                alfa = int(220 * (1 - fase))
                onda = pygame.Surface((radio * 2 + 4, radio * 2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(onda, (255, 230, 120, alfa), (radio + 2, radio + 2), radio, 3)
                pantalla.blit(onda, onda.get_rect(center=caja.center))


class _Particula:

    def __init__(self, x, y, vx, vy, color, tam, vida, gravedad=900, piso=None):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.color, self.tam, self.vida = color, tam, vida
        self.gravedad, self.piso = gravedad, piso

    def actualizar(self, dt):
        self.vida -= dt
        self.vy += self.gravedad * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.piso is not None and self.y > self.piso:
            self.y = self.piso
            self.vy = 0
            self.vx *= 0.5

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, (int(self.x), int(self.y), self.tam, self.tam))


def _eventos():
    """(avanzar, salir)"""
    avanzar = False
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return False, True
            if evento.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                avanzar = True
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            avanzar = True
    return avanzar, False


def _cabeza_teichi():
    return _silueta(_cargar("assets/personajes/TEICHI/teichi cabeza.png"))


# ==========================================================
# ANTES DE LA PELEA: EL ROBOT LLEGA A LA BOMBONERA
# ==========================================================

def escena_robot_llega(pantalla, reloj, fuente_media, sprites_jugador, robot=None):
    try:
        _llega(pantalla, reloj, fuente_media, sprites_jugador, robot or sprites_robot(sprites_jugador))
    finally:
        sonidos.detener("teclado")


def _llega(pantalla, reloj, fuente_media, sprites_jugador, robot):

    fondo, piso = _bombonera()
    nombre = sprites_jugador.get("nombre", "BRO")
    robo = nombre_robot(sprites_jugador)
    fuente_signo = type(fuente_media)(3)

    retratos = {
        "LORD TEICHI": Retrato("LORD TEICHI", _cabeza_teichi()),
        robo: Retrato(robo, frente_robot(sprites_jugador)),
    }
    dialogo = _Dialogo(
        fuente_media,
        [
            ("LORD TEICHI", "Bienvenido a la Bombonera, %s." % robo),
            ("LORD TEICHI", "Te construí copiando a %s tornillo por tornillo." % nombre),
            ("LORD TEICHI", "Cuando lleguen esos diminutos Compu Broskis, los vas a aplastar uno por uno."),
            ("LORD TEICHI", "Y después vas a ocupar el lugar de %s... ¡y nadie va a rescatar al princesito Mxroy!" % nombre),
            (robo, "BIP BOP. ORDEN RECIBIDA. DESTRUIR A LOS COMPU BROSKIS."),
        ],
        retratos,
        {"LORD TEICHI": 6, robo: 6},
        {"LORD TEICHI": COLOR_TEICHI, robo: COLOR_ROBOT},
        {"LORD TEICHI": "(por los parlantes)"},
    )

    ESPERA = 1.2        # estadio vacio
    BAJADA = 2.4        # el robot baja volando
    x = ANCHO // 2
    y_inicio = -60.0
    y_robot = y_inicio
    aterrizo = False
    t = 0.0
    temblor = 0.0
    polvo = []
    t_fin = None
    lienzo = pygame.Surface((ANCHO, ALTO))

    while True:
        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt
        temblor = max(0.0, temblor - dt)
        avanzar, salir = _eventos()
        if salir:
            return

        # --- el robot baja con los cohetes prendidos ---
        if not aterrizo:
            if avanzar:
                t = max(t, ESPERA + BAJADA)
                avanzar = False
            p = max(0.0, min(1.0, (t - ESPERA) / BAJADA))
            # Frena al llegar (ease out)
            y_robot = y_inicio + (piso - y_inicio) * (1 - (1 - p) ** 3)
            if p >= 1.0:
                aterrizo = True
                y_robot = piso
                temblor = 0.5
                sonidos.reproducir("golpe")
                for _ in range(40):
                    lado = random.choice((-1, 1))
                    polvo.append(_Particula(x + lado * random.uniform(10, 60), piso - 4,
                                            lado * random.uniform(60, 260), random.uniform(-220, -40),
                                            random.choice([(150, 130, 100), (120, 110, 90), (70, 150, 70)]),
                                            random.choice((4, 6)), random.uniform(0.6, 1.3), piso=piso - 3))
        t_aterrizo = ESPERA + BAJADA

        if aterrizo and dialogo.indice < 0:
            # Un ratito parado ("BIP BOP") y arranca a hablar Teichi
            if t > t_aterrizo + 1.4 or (avanzar and t > t_aterrizo + 0.3):
                avanzar = False
                dialogo.empezar(t)
        elif dialogo.indice >= 0:
            if dialogo.actualizar(dt, avanzar) and t_fin is None:
                t_fin = t

        if t_fin is not None and t - t_fin > 0.8:
            return

        for q in polvo:
            q.actualizar(dt)
        polvo = [q for q in polvo if q.vida > 0]
        fondo.actualizar(dt)

        # --- dibujar ---
        _dibujar_estadio(lienzo, fondo)
        hablando_teichi = dialogo.activo and dialogo.hablando == "LORD TEICHI" and dialogo.escribiendo
        _dibujar_parlantes(lienzo, t, hablando_teichi)

        if aterrizo:
            sombra = pygame.Surface((120, 18), pygame.SRCALPHA)
            pygame.draw.ellipse(sombra, (0, 0, 0, 110), sombra.get_rect())
            lienzo.blit(sombra, sombra.get_rect(center=(x, piso)))

        # Pose: bajando con los brazos arriba; al aterrizar se agacha y se para
        if not aterrizo:
            pose = "brazos_arriba"
        elif t - t_aterrizo < 0.35:
            pose = "agachado"
        elif dialogo.activo and dialogo.hablando != "LORD TEICHI" and dialogo.escribiendo:
            pose = "brazos_arriba" if int(t * 4) % 2 else "quieto"
        else:
            pose = "respirar" if int(t * 1.5) % 2 else "quieto"
        img = robot[pose][0]
        rect = img.get_rect(midbottom=(x, int(y_robot)))

        # Fuego de los cohetes de los pies
        if not aterrizo and t > ESPERA - 0.2:
            for lado in (-1, 1):
                fx = rect.centerx + lado * 18
                largo = random.randint(30, 52)
                pygame.draw.polygon(lienzo, (255, 140, 30), [(fx - 12, rect.bottom - 4), (fx + 12, rect.bottom - 4), (fx, rect.bottom + largo)])
                pygame.draw.polygon(lienzo, (255, 230, 90), [(fx - 6, rect.bottom - 4), (fx + 6, rect.bottom - 4), (fx, rect.bottom + largo * 0.6)])
        lienzo.blit(img, rect)

        if aterrizo and 0.4 < t - t_aterrizo < 1.4:
            _dibujar_signo(lienzo, fuente_signo, "BIP BOP", (255, 80, 80), x, rect.top - 8)

        for q in polvo:
            q.dibujar(lienzo)

        dx = random.randint(-6, 6) if temblor > 0 else 0
        dy = random.randint(-4, 4) if temblor > 0 else 0
        pantalla.fill(NEGRO)
        pantalla.blit(lienzo, (dx, dy))

        # Aparece de a poco al principio y se va a negro al final
        if t < 0.6 or t_fin is not None:
            alfa = (1 - t / 0.6) if t_fin is None else min(1.0, (t - t_fin) / 0.8)
            negro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            negro.fill((0, 0, 0, int(255 * max(0.0, min(1.0, alfa)))))
            pantalla.blit(negro, (0, 0))

        dialogo.dibujar(pantalla, t)
        _ayuda(pantalla, fuente_media)
        pygame.display.flip()


def _ayuda(pantalla, fuente_media):
    chica = type(fuente_media)(2)
    imagen = chica.render("ESC: saltear", True, (230, 230, 230))
    pantalla.blit(imagen, imagen.get_rect(topright=(ANCHO - 10, 8)))


# ==========================================================
# DESPUES DE LA PELEA: EL ROBOT DESTRUIDO
# ==========================================================

def escena_robot_destruido(pantalla, reloj, fuente_media, sprites_jugador, robot=None):
    try:
        _destruido(pantalla, reloj, fuente_media, sprites_jugador, robot or sprites_robot(sprites_jugador))
    finally:
        sonidos.detener("teclado")


def _destruido(pantalla, reloj, fuente_media, sprites_jugador, robot):

    fondo, piso = _bombonera()

    retratos = {"LORD TEICHI": Retrato("LORD TEICHI", _cabeza_teichi())}
    dialogo = _Dialogo(
        fuente_media,
        [
            ("LORD TEICHI", "No creía que fueran a lograrlo."),
            ("LORD TEICHI", "NOS VEMOS EN BURZACO DIMINUTOS COMPU BROSKIS."),
        ],
        retratos,
        {"LORD TEICHI": 6},
        {"LORD TEICHI": COLOR_TEICHI},
        {"LORD TEICHI": "(por los parlantes)"},
    )

    # El robot tirado en la cancha, oscurecido y de costado
    tirado = pygame.transform.rotate(robot["agachado"][0], 90)
    tirado = tirado.copy()
    tirado.fill((150, 150, 150, 255), special_flags=pygame.BLEND_RGBA_MULT)
    x_robot = 470

    # Pedazos sueltos (tornillos, tuercas y chapas)
    azar = random.Random(15)
    pedazos = []
    for _ in range(14):
        pedazos.append((
            x_robot + azar.uniform(-170, 170),
            piso - azar.choice((4, 6, 8)),
            azar.choice((6, 8, 10, 12)),
            azar.choice([(150, 156, 170), (110, 116, 130), (200, 206, 220), (60, 64, 76)]),
        ))

    jugador = sprites_jugador["idle_der"]
    x_jugador = 210

    chispas = []
    humo = []
    t = 0.0
    t_fin = None
    lienzo = pygame.Surface((ANCHO, ALTO))
    INICIO = 1.6

    while True:
        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt
        avanzar, salir = _eventos()
        if salir:
            return

        if not dialogo.activo and dialogo.indice < 0:
            if t > INICIO or avanzar:
                avanzar = False
                dialogo.empezar(t)
        else:
            if dialogo.actualizar(dt, avanzar) and t_fin is None:
                t_fin = t

        if t_fin is not None and t - t_fin > 1.0:
            return

        # Chispas y humo que salen del robot
        if random.random() < 0.35:
            for _ in range(random.randint(2, 5)):
                chispas.append(_Particula(x_robot + random.uniform(-30, 30), piso - random.uniform(20, 60),
                                          random.uniform(-160, 160), random.uniform(-260, -80),
                                          random.choice([(255, 230, 80), (255, 170, 40), (255, 255, 200)]),
                                          3, random.uniform(0.25, 0.5), gravedad=800))
        if random.random() < 0.12:
            humo.append([x_robot + random.uniform(-40, 40), piso - 50, random.uniform(10, 18), 2.0])
        for q in chispas:
            q.actualizar(dt)
        chispas = [q for q in chispas if q.vida > 0]
        for h in humo:
            h[1] -= 35 * dt
            h[0] += 8 * dt
            h[2] += 12 * dt
            h[3] -= dt
        humo = [h for h in humo if h[3] > 0]
        fondo.actualizar(dt)

        # --- dibujar ---
        _dibujar_estadio(lienzo, fondo)
        hablando = dialogo.activo and dialogo.escribiendo
        _dibujar_parlantes(lienzo, t, hablando)

        for px, py, tam, color in pedazos:
            pygame.draw.rect(lienzo, NEGRO, (int(px) - 1, int(py) - 1, tam + 2, tam + 2))
            pygame.draw.rect(lienzo, color, (int(px), int(py), tam, tam))

        sombra = pygame.Surface((tirado.get_width() + 20, 18), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 110), sombra.get_rect())
        lienzo.blit(sombra, sombra.get_rect(center=(x_robot, piso)))
        lienzo.blit(tirado, tirado.get_rect(midbottom=(x_robot, piso + 4)))

        for hx, hy, radio, vida in humo:
            nube = pygame.Surface((int(radio * 2) + 2, int(radio * 2) + 2), pygame.SRCALPHA)
            pygame.draw.circle(nube, (90, 90, 96, int(150 * min(1.0, vida))), (int(radio) + 1, int(radio) + 1), int(radio))
            lienzo.blit(nube, (int(hx - radio), int(hy - radio)))
        for q in chispas:
            q.dibujar(lienzo)

        # El jugador, parado al costado mirando al robot (y despues arriba,
        # a los parlantes)
        sombra = pygame.Surface((jugador.get_width(), 10), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
        lienzo.blit(sombra, sombra.get_rect(center=(x_jugador, piso)))
        lienzo.blit(jugador, jugador.get_rect(midbottom=(x_jugador, piso)))

        pantalla.blit(lienzo, (0, 0))

        if t < 0.6 or t_fin is not None:
            alfa = (1 - t / 0.6) if t_fin is None else min(1.0, (t - t_fin) / 1.0)
            negro = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            negro.fill((0, 0, 0, int(255 * max(0.0, min(1.0, alfa)))))
            pantalla.blit(negro, (0, 0))

        dialogo.dibujar(pantalla, t)
        _ayuda(pantalla, fuente_media)
        pygame.display.flip()

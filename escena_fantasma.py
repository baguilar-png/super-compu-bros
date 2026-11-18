"""
Escena del FANTASMA CASTRO (antes del nivel 10, el primero con fantasma).

Aparece una vez por partida (si perdes todas las vidas se vuelve a ver).

    1. Los cinco Compu Bros en la calle de Once.
    2. Castro se empieza a sentir mal: se pone verde, vomita, se infla y
       EXPLOTA. Del humo sale el FantasmaCastro, que se va volando.
    3. A Benja le suena el celular: es Lord Teichi, que dice que ahora el
       FantasmaCastro lo controla el y que va a ser un enemigo nuevo.
    4. Castro sale de un edificio como si nada (el que exploto era un clon):
       "¿por que estan tan palidos?" - "¡vos explotaste recien!" - "nono, les
       estaba mostrando mis biceps a unas damiselas".

ENTER / ESPACIO / click pasan el texto (y adelantan las animaciones), ESC
saltea la escena. Los dialogos son como los de historia.py: el que habla se
ve grande y cuando deja de hablar se achica, se pone gris y va al costado.
"""

import math
import random
import sys

import pygame

import sonidos
from escena_dilolio import _dibujar_celular, _dibujar_ring
from historia import (
    BLANCO,
    CUADRO,
    FPS,
    NEGRO,
    PERSONAJES,
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


# ==========================================================
# GUION
#
# ("dice", quien, texto)   una linea de dialogo
# ("hace", accion)         una animacion (ver ACCIONES)
# ==========================================================

GUION = [
    ("hace", "charla"),
    ("hace", "mareo"),
    ("dice", "CASTRO_MAL", "Chicos... no me siento muy bien..."),
    ("dice", "BENJA", "¿Qué te pasa, Castro? Estás todo verde."),
    ("dice", "CASTRO_MAL", "Creo que el chori de la esquina me cayó mal... ¡BLAAARGH!"),
    ("hace", "vomito"),
    ("dice", "POSHO", "¡Qué asco, Castro!"),
    ("dice", "CASTRO_MAL", "Esperen... me siento... muy... INFLADO..."),
    ("hace", "inflar"),
    ("hace", "explosion"),
    ("dice", "THIAGO", "¡¿CASTRO EXPLOTÓ?!"),
    ("hace", "fantasma"),
    ("dice", "BAUTO", "¡Y ahora es un fantasma!"),
    ("hace", "fantasma_se_va"),
    ("hace", "telefono"),
    ("dice", "LORD TEICHI", "Jejeje... ¿Les gustó el espectáculo, diminutos Compu Broskis?"),
    ("dice", "LORD TEICHI", "Ahora el FantasmaCastro está bajo mi control."),
    ("dice", "LORD TEICHI", "Va a ser su nuevo enemigo. ¡Que lo disfruten!"),
    ("hace", "colgar"),
    ("hace", "puerta"),
    ("dice", "CASTRO", "Ey, ¿qué pasó? ¿Por qué están tan pálidos?"),
    ("dice", "COMPU BROS", "¡VOS EXPLOTASTE RECIÉN!"),
    ("dice", "CASTRO", "Nono, les estaba mostrando mis bíceps a unas damiselas."),
    ("dice", "BENJA", "Entonces... el que explotó era un clon."),
    ("hace", "fin"),
]

# Cuanto dura cada animacion (segundos). ENTER la adelanta.
ACCIONES = {
    "charla": 2.2,
    "mareo": 1.2,
    "vomito": 1.8,
    "inflar": 1.8,
    "explosion": 1.8,
    "fantasma": 2.0,
    "fantasma_se_va": 1.3,
    "telefono": 2.6,
    "colgar": 0.7,
    "puerta": 3.2,
    "fin": 1.0,
}

# Nombre que se ve en el cartel y color del cartel
NOMBRES = {
    "CASTRO_MAL": ("CASTRO", (60, 150, 60)),
    "COMPU BROS": ("COMPU BROS", (90, 90, 110)),
    "LORD TEICHI": ("LORD TEICHI", (120, 30, 40)),
}

LETRAS_POR_SEGUNDO = 38


# ==========================================================
# MEDIDAS
# ==========================================================

NIVEL_FONDO = 10            # la calle de Once
CAMARA_X = 2050
CAMARA_Y = 400            # la vereda queda arriba del cuadro de texto

ESCALA = 3                  # sprites en la calle (30x32 -> 90x96)
X_BROS = {"BAUTO": 130, "BENJA": 240, "CASTRO": 350, "POSHO": 460, "THIAGO": 570}
X_PUERTA = 700

ESCALA_FANTASMA = 3
ESCALA_RETRATO = 6
ESCALA_TEICHI = 6
ESCALA_GRUPO = 5
ESCALA_BANCO = 2

RETRATO_X = CUADRO.x + 112
RETRATO_BASE = CUADRO.bottom - 14

VERDE = (110, 200, 80)


# ==========================================================
# AYUDAS DE DIBUJO
# ==========================================================

def _tenida(imagen, color, sumar=False):
    """Copia teñida pixel por pixel (multiplicando o sumando el color)."""
    copia = imagen.copy()
    for x in range(copia.get_width()):
        for y in range(copia.get_height()):
            r, g, b, a = copia.get_at((x, y))
            if not a:
                continue
            if sumar:
                nuevo = (min(255, r + color[0]), min(255, g + color[1]), min(255, b + color[2]), a)
            else:
                nuevo = (r * color[0] // 255, g * color[1] // 255, b * color[2] // 255, a)
            copia.set_at((x, y), nuevo)
    return copia


def _silueta(imagen):
    negra = imagen.copy()
    for x in range(negra.get_width()):
        for y in range(negra.get_height()):
            a = negra.get_at((x, y))[3]
            if a:
                negra.set_at((x, y), (8, 8, 12, a))
    return negra


def _fondo(ancho, alto):
    """La calle de Once (el fondo del nivel 10), quieta."""

    lienzo = pygame.Surface((ancho, alto))
    lienzo.fill((120, 170, 220))
    piso_y = 474
    try:
        import juego as J
        from terreno import Terreno

        terreno = Terreno.cargar(NIVEL_FONDO)
        fondo = J.FondoNivel(NIVEL_FONDO, ancho, alto, J.SUELO_Y, J.NIVEL_ANCHO, J.CELESTE, J.VERDE_SUELO, terreno)
        fondo.dibujar(lienzo, CAMARA_X, CAMARA_Y)
        piso_y = terreno.calle_y - CAMARA_Y
        # Abajo de la calle se repite la franja del asfalto hasta el borde
        franja = lienzo.subsurface((0, piso_y + 20, ancho, 60)).copy()
        y = piso_y + 80
        while y < alto:
            lienzo.blit(franja, (0, y))
            y += 60
    except Exception:
        pygame.draw.rect(lienzo, (90, 90, 100), (0, piso_y, ancho, alto - piso_y))
    return lienzo, piso_y


def _grupo(cabezas):
    """Las caras de cuatro Compu Bros juntas, de a dos (para "COMPU BROS")."""
    w = max(c.get_width() for c in cabezas)
    h = max(c.get_height() for c in cabezas)
    imagen = pygame.Surface((w * 2 + 2, h * 2 + 1), pygame.SRCALPHA)
    for k, c in enumerate(cabezas):
        imagen.blit(c, ((k % 2) * (w + 2), (k // 2) * (h + 1)))
    return imagen


def _dibujar_puerta(pantalla, x, piso_y, apertura):
    """Puerta de madera en la pared del edificio. apertura: 0 a 1."""

    ancho, alto = 56, 92
    marco = pygame.Rect(0, 0, ancho + 12, alto + 8)
    marco.midbottom = (x, piso_y - 6)
    pygame.draw.rect(pantalla, NEGRO, marco.inflate(6, 6))
    pygame.draw.rect(pantalla, (150, 120, 90), marco)
    hueco = pygame.Rect(0, 0, ancho, alto)
    hueco.midbottom = (x, piso_y - 6)
    pygame.draw.rect(pantalla, (20, 16, 22), hueco)
    # La hoja de la puerta se va angostando al abrirse (gira hacia adentro)
    hoja = hueco.copy()
    hoja.width = max(4, int(ancho * (1 - apertura)))
    pygame.draw.rect(pantalla, (110, 64, 34), hoja)
    pygame.draw.rect(pantalla, (80, 44, 22), hoja, 3)
    if hoja.width > 14:
        pygame.draw.rect(pantalla, (240, 200, 60), (hoja.right - 12, hoja.centery, 5, 5))
    # Escalon
    pygame.draw.rect(pantalla, (120, 120, 128), (marco.x - 4, piso_y - 8, marco.width + 8, 8))


class Particula:

    def __init__(self, x, y, vx, vy, color, tam, vida, gravedad=1100, piso=None):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.color = color
        self.tam = tam
        self.vida = vida
        self.gravedad = gravedad
        self.piso = piso
        self.quieta = False

    def actualizar(self, dt):
        self.vida -= dt
        if self.quieta:
            return
        self.vy += self.gravedad * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.piso is not None and self.y >= self.piso:
            self.y = self.piso
            self.vx *= 0.3
            self.vy = 0
            self.quieta = True

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, (int(self.x), int(self.y), self.tam, self.tam))


# ==========================================================
# ESCENA
# ==========================================================

def escena_fantasma(pantalla, reloj, fuente_grande, fuente_media, jugador=None):
    """Muestra la escena. Vuelve al terminar o con ESC."""

    try:
        _escena(pantalla, reloj, fuente_media)
    finally:
        sonidos.detener("telefono")
        sonidos.detener("teclado")


def _escena(pantalla, reloj, fuente_media):

    ancho, alto = pantalla.get_size()
    fuente_chica = type(fuente_media)(2)
    fuente_signo = type(fuente_media)(4)

    fondo, piso_y = _fondo(ancho, alto)
    lienzo = pygame.Surface((ancho, alto))

    # ----- sprites -----
    frente = {}
    for nombre in X_BROS:
        frente[nombre] = _cargar(PERSONAJES[nombre][0])
    en_calle = {n: _escalar(img, ESCALA) for n, img in frente.items()}
    palidos = {n: _tenida(img, (110, 110, 110), sumar=True) for n, img in en_calle.items()}
    castro_verde = _tenida(en_calle["CASTRO"], (150, 255, 140))
    castro_rojo = _tenida(en_calle["CASTRO"], (255, 120, 120))

    castro_caminando = []
    for k in (1, 2, 3, 2):
        img = _escalar(_cargar("assets/personajes/CASTRO/castro frame %d.png" % k), ESCALA)
        castro_caminando.append(pygame.transform.flip(img, True, False))

    fantasma = [
        _escalar(_cargar("assets/enemigos/fantasma/fantasma_%d.png" % k), ESCALA_FANTASMA)
        for k in (1, 2, 3)
    ]

    # ----- retratos -----
    cabezas = {
        n: _cargar("assets/personajes/%s/%s cabeza.png" % (n, n.lower() if n != "POSHO" else "Posho"))
        for n in X_BROS
    }
    imagenes_retrato = {n: frente[n] for n in X_BROS}
    imagenes_retrato["CASTRO_MAL"] = _tenida(frente["CASTRO"], (150, 255, 140))
    imagenes_retrato["LORD TEICHI"] = _silueta(_cargar("assets/personajes/TEICHI/teichi cabeza.png"))
    imagenes_retrato["COMPU BROS"] = _grupo([cabezas[n] for n in ("BAUTO", "BENJA", "POSHO", "THIAGO")])
    escalas = {n: ESCALA_RETRATO for n in imagenes_retrato}
    escalas["LORD TEICHI"] = ESCALA_TEICHI
    escalas["COMPU BROS"] = ESCALA_GRUPO
    retratos = {n: Retrato(n, img) for n, img in imagenes_retrato.items()}

    def nombre_y_color(quien):
        if quien in NOMBRES:
            return NOMBRES[quien]
        return quien, PERSONAJES[quien][1]

    guion = []
    for paso in GUION:
        if paso[0] == "dice":
            guion.append(("dice", paso[1], _partir_en_lineas(fuente_media, paso[2], TEXTO_ANCHO)))
        else:
            guion.append(paso)

    # ----- estado -----
    paso = -1
    t_paso = 0.0
    letras = 0.0
    total_letras = 0
    banco = []
    hablando = None
    t = 0.0
    temblor = 0.0
    flash = 0.0

    castro = "normal"           # normal, verde, inflado, no_esta, vuelve
    escala_castro = 1.0
    x_castro = float(X_BROS["CASTRO"])
    charco = 0.0                # tamano del vomito en el piso
    particulas = []
    humo = []                   # [x, y, radio, vida]
    fantasma_pos = None         # [x, y, alfa]
    sono = False
    atendio = False
    son_palidos = False
    puerta = 0.0
    sorpresa = 0.0              # "!" sobre los bros
    t_dialogo = 0.0

    def pasar_a_linea(quien, partes):
        nonlocal letras, total_letras, hablando
        letras = 0.0
        total_letras = sum(len(p) for p in partes)
        if quien == hablando:
            return
        if hablando is not None and hablando not in banco:
            banco.append(hablando)
        if quien in banco:
            banco.remove(quien)
        hablando = quien
        retratos[quien].mandar_a(RETRATO_X, RETRATO_BASE, escalas[quien], gris=False)
        x = CUADRO.right - 10
        for nombre in banco[-3:]:
            ancho_chico = retratos[nombre].color.get_width() * ESCALA_BANCO
            retratos[nombre].mandar_a(x - ancho_chico // 2, CUADRO.y - 12, ESCALA_BANCO, gris=True)
            x -= ancho_chico + 10

    def empezar_paso(indice):
        nonlocal paso, t_paso, castro, sono, atendio, son_palidos, sorpresa, fantasma_pos, flash, temblor, t_dialogo, x_castro
        paso = indice
        t_paso = 0.0
        if paso >= len(guion):
            return
        tipo = guion[paso][0]
        if tipo == "dice":
            if not (paso > 0 and guion[paso - 1][0] == "dice"):
                t_dialogo = t
            pasar_a_linea(guion[paso][1], guion[paso][2])
            return
        accion = guion[paso][1]
        if accion == "mareo":
            castro = "verde"
            sorpresa = 0.0
        elif accion == "vomito":
            sonidos.reproducir("vomito")
        elif accion == "inflar":
            castro = "inflado"
            sorpresa = 9.0
        elif accion == "explosion":
            castro = "no_esta"
            sonidos.reproducir("explosion")
            flash = 1.0
            temblor = 0.7
            cx = X_BROS["CASTRO"]
            cy = piso_y - 50
            colores = [(210, 40, 40), (240, 240, 240), (230, 190, 150), (40, 30, 30), (120, 200, 80)]
            for _ in range(70):
                a = random.uniform(0, 2 * math.pi)
                v = random.uniform(150, 650)
                particulas.append(Particula(cx, cy, math.cos(a) * v, math.sin(a) * v - 250,
                                            random.choice(colores), random.choice((4, 6, 8)),
                                            random.uniform(1.5, 3.0), piso=piso_y - 4))
            for _ in range(14):
                humo.append([cx + random.uniform(-50, 50), cy + random.uniform(-50, 30),
                             random.uniform(18, 34), random.uniform(1.6, 2.6)])
            sorpresa = 9.0
        elif accion == "fantasma":
            fantasma_pos = [float(X_BROS["CASTRO"]), float(piso_y - 60), 0.0]
            sonidos.reproducir("fantasma")
        elif accion == "telefono":
            sono = True
            sorpresa = 0.0
            sonidos.reproducir_en_bucle("telefono")
        elif accion == "colgar":
            sonidos.reproducir("boton")
            atendio = False
            sono = False
        elif accion == "puerta":
            son_palidos = True
            castro = "vuelve"
            x_castro = float(X_PUERTA)
            sorpresa = 0.0

    def terminar_accion():
        """ENTER durante una animacion: se adelanta al final."""
        nonlocal t_paso
        t_paso = ACCIONES[guion[paso][1]]

    empezar_paso(0)

    while True:

        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt
        t_paso += dt
        temblor = max(0.0, temblor - dt)
        flash = max(0.0, flash - dt * 2.5)
        sorpresa = max(0.0, sorpresa - dt)

        avanzar = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                    avanzar = True
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                avanzar = True

        if paso >= len(guion):
            return

        tipo = guion[paso][0]

        # --------------------------------------------------
        # AVANCE DEL GUION
        # --------------------------------------------------

        if tipo == "dice":
            if letras < total_letras:
                letras = min(total_letras, letras + LETRAS_POR_SEGUNDO * dt)
            if avanzar:
                if letras < total_letras:
                    letras = total_letras
                else:
                    sonidos.reproducir("boton")
                    empezar_paso(paso + 1)
                    continue
        else:
            accion = guion[paso][1]
            if avanzar:
                terminar_accion()
            # El telefono atiende al final del ring
            if accion == "telefono" and t_paso >= ACCIONES["telefono"] and not atendio:
                atendio = True
                sonidos.detener("telefono")
                sonidos.reproducir("boton")
            if accion == "fin" and t_paso >= ACCIONES["fin"]:
                return
            if t_paso >= ACCIONES[accion]:
                if accion == "fantasma_se_va":
                    fantasma_pos = None
                if accion == "vomito":
                    charco = max(charco, 1.0)
                empezar_paso(paso + 1)
                continue

        escribiendo = tipo == "dice" and letras < total_letras
        if escribiendo:
            sonidos.reproducir_en_bucle("teclado")
        else:
            sonidos.detener("teclado")

        accion = guion[paso][1] if tipo == "hace" else None
        p = min(1.0, t_paso / ACCIONES[accion]) if accion else 0.0

        # Vomito: chorro verde que cae adelante de Castro
        if accion == "vomito" and 0.15 < t_paso < 1.4:
            boca_y = piso_y - 60
            for _ in range(4):
                particulas.append(Particula(
                    X_BROS["CASTRO"] + random.uniform(-6, 6), boca_y,
                    random.uniform(-40, 90), random.uniform(-160, 10),
                    random.choice([(120, 190, 60), (150, 210, 70), (100, 160, 40)]),
                    random.choice((4, 6)), 1.4, piso=piso_y - 4))
            charco = min(1.0, charco + dt * 0.8)

        for q in particulas:
            q.actualizar(dt)
        particulas = [q for q in particulas if q.vida > 0]
        for h in humo:
            h[2] += 30 * dt
            h[1] -= 22 * dt
            h[3] -= dt
        humo = [h for h in humo if h[3] > 0]

        # Fantasma: sube flotando y despues se va volando
        if fantasma_pos is not None:
            if accion == "fantasma":
                fantasma_pos[1] = piso_y - 60 - 110 * min(1.0, t_paso / 1.2)
                fantasma_pos[2] = min(1.0, t_paso / 0.6)
            elif accion == "fantasma_se_va":
                fantasma_pos[0] += 380 * dt
                fantasma_pos[1] -= 300 * dt

        # Castro vuelve: sale por la puerta y camina hasta su lugar
        if accion == "puerta":
            puerta = min(1.0, t_paso / 0.5) if t_paso < 2.8 else max(0.0, 1 - (t_paso - 2.8) / 0.4)
            if t_paso > 0.6:
                x_castro = X_PUERTA - (X_PUERTA - X_BROS["CASTRO"]) * min(1.0, (t_paso - 0.6) / 1.8)
            if t_paso > 2.4 and sorpresa <= 0:
                sorpresa = 1.2
        if castro == "vuelve" and accion != "puerta":
            x_castro = float(X_BROS["CASTRO"])

        for r in retratos.values():
            r.actualizar(dt)

        # --------------------------------------------------
        # DIBUJAR (en un lienzo, para poder sacudirlo)
        # --------------------------------------------------

        lienzo.blit(fondo, (0, 0))

        # Puerta (siempre esta: es la del edificio de donde sale Castro)
        _dibujar_puerta(lienzo, X_PUERTA, piso_y, puerta)

        # Charco de vomito
        if charco > 0:
            w = int(30 + 70 * charco)
            pygame.draw.ellipse(lienzo, (90, 150, 40), (X_BROS["CASTRO"] + 10 - w // 2, piso_y - 9, w, 12))
            pygame.draw.ellipse(lienzo, (130, 190, 60), (X_BROS["CASTRO"] + 14 - w // 3, piso_y - 7, w * 2 // 3, 6))

        quien_habla = hablando if tipo == "dice" else None

        def dibujar_castro():
            nonlocal escala_castro
            if castro in ("normal", "verde", "inflado", "vuelve"):
                x = x_castro
                if castro == "verde":
                    img = castro_verde
                    x += math.sin(t * 9) * 3          # se tambalea
                    if accion == "vomito" and 0.1 < t_paso < 1.4:
                        img = pygame.transform.rotate(castro_verde, -8)
                elif castro == "inflado":
                    escala_castro = 1 + 0.7 * p * p
                    base = castro_rojo if int(t * 12) % 2 and p > 0.4 else castro_verde
                    img = pygame.transform.scale(base, (int(base.get_width() * escala_castro), int(base.get_height() * escala_castro)))
                    x += random.uniform(-1, 1) * 5 * p
                elif castro == "vuelve" and accion == "puerta" and 0.6 < t_paso < 2.4:
                    img = castro_caminando[int(t * 8) % len(castro_caminando)]
                else:
                    img = en_calle["CASTRO"]
                salto = 0
                if escribiendo and quien_habla in ("CASTRO", "CASTRO_MAL"):
                    salto = int(abs(math.sin(t / 0.32 * math.pi)) * 7)
                sombra = pygame.Surface((max(40, img.get_width() - 20), 12), pygame.SRCALPHA)
                pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
                lienzo.blit(sombra, sombra.get_rect(center=(int(x), piso_y - 1)))
                # Mientras sale por la puerta, se ve solo lo que esta afuera
                rect = img.get_rect(midbottom=(int(x), piso_y - salto))
                lienzo.blit(img, rect)

                # Gotitas de sudor
                if castro == "verde" and int(t * 3) % 2 == 0:
                    pygame.draw.rect(lienzo, (140, 200, 255), (rect.right - 22, rect.top + 18, 5, 8))
                    pygame.draw.rect(lienzo, (140, 200, 255), (rect.left + 18, rect.top + 26, 5, 8))


        # Castro (cuando sale de la puerta camina por atras de los demas)
        castro_atras = castro == "vuelve" and accion == "puerta"
        if castro_atras:
            dibujar_castro()

        for nombre, x in X_BROS.items():

            if nombre == "CASTRO":
                continue

            img = palidos[nombre] if son_palidos else en_calle[nombre]
            salto = 0
            if escribiendo and (quien_habla == nombre or quien_habla == "COMPU BROS"):
                salto = int(abs(math.sin(t / 0.32 * math.pi)) * 7)
            # Chiquito vaiven, como charlando
            elif accion == "charla":
                salto = int(abs(math.sin(t * 3 + x)) * 3)
            # Benja con el celular
            sombra = pygame.Surface((70, 12), pygame.SRCALPHA)
            pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
            lienzo.blit(sombra, (x - 35, piso_y - 7))
            rect = img.get_rect(midbottom=(x, piso_y - salto))
            lienzo.blit(img, rect)

            if nombre == "BENJA":
                if sono and not atendio:
                    _dibujar_ring(lienzo, fuente_media, rect.right + 20, rect.top + 50, t)
                elif atendio:
                    _dibujar_celular(lienzo, rect.right - 26, rect.top + 26, 3)

            if sorpresa > 0:
                _dibujar_signo(lienzo, fuente_signo, "!", (255, 214, 64), x, rect.top - 6)

        if not castro_atras:
            dibujar_castro()

        # Particulas (vomito y pedazos de la explosion)
        for q in particulas:
            q.dibujar(lienzo)

        # Humo
        for hx, hy, radio, vida in humo:
            nube = pygame.Surface((int(radio * 2) + 2, int(radio * 2) + 2), pygame.SRCALPHA)
            pygame.draw.circle(nube, (200, 200, 200, int(200 * min(1.0, vida))), (int(radio) + 1, int(radio) + 1), int(radio))
            lienzo.blit(nube, (int(hx - radio), int(hy - radio)))

        # FantasmaCastro
        if fantasma_pos is not None:
            img = fantasma[int(t / 0.16) % len(fantasma)].copy()
            img.set_alpha(int(255 * fantasma_pos[2]))
            flote = math.sin(t * 4) * 6
            lienzo.blit(img, img.get_rect(center=(int(fantasma_pos[0]), int(fantasma_pos[1] + flote))))
            if accion == "fantasma" and t_paso > 0.8:
                _dibujar_signo(lienzo, fuente_media, "UUUUH", BLANCO, int(fantasma_pos[0]) + 70, int(fantasma_pos[1]) - 40)

        # --------------------------------------------------
        # A PANTALLA (con sacudida y destello)
        # --------------------------------------------------

        dx = random.randint(-8, 8) if temblor > 0 else 0
        dy = random.randint(-6, 6) if temblor > 0 else 0
        pantalla.fill(NEGRO)
        pantalla.blit(lienzo, (dx, dy))

        if flash > 0:
            blanco = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            blanco.fill((255, 255, 255, int(255 * min(1.0, flash))))
            pantalla.blit(blanco, (0, 0))

        if accion == "fin":
            negro = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            negro.fill((0, 0, 0, int(255 * p)))
            pantalla.blit(negro, (0, 0))

        # --------------------------------------------------
        # DIALOGO
        # --------------------------------------------------

        if tipo == "dice":

            quien, partes = guion[paso][1], guion[paso][2]
            nombre_cartel, color = nombre_y_color(quien)

            velo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            velo.fill((0, 0, 0, int(90 * min(1.0, (t - t_dialogo) / 0.25))))
            pantalla.blit(velo, (0, 0))

            _dibujar_cuadro(pantalla, fuente_media, nombre_cartel, color)

            for nombre in banco[-3:]:
                retratos[nombre].dibujar(pantalla)

            salto_retrato = int(abs(math.sin(t / 0.32 * math.pi)) * 3) if escribiendo else 0
            retratos[quien].dibujar(pantalla, salto_retrato)

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

            if quien == "LORD TEICHI":
                aviso = fuente_chica.render("(por telefono)", True, (200, 200, 220))
                pantalla.blit(aviso, aviso.get_rect(bottomleft=(TEXTO_X + 240, CUADRO.y + 2)))

        ayuda = fuente_chica.render("ESC: saltear", True, (230, 230, 230))
        pantalla.blit(ayuda, ayuda.get_rect(topright=(ancho - 10, 8)))

        pygame.display.flip()

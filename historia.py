"""
Escena de la historia: aparece la PRIMERA vez que se toca JUGAR.

    1. Los cinco Compu Bros estan en el pasillo del Huergo charlando
       (suben y bajan, como si hablaran).
    2. A los 3 segundos entra IKI corriendo y les avisa que se llevaron
       al princesito Mxroy.
    3. Dialogo tipo juego de rol: el que habla se ve GRANDE en el cuadro
       de texto; cuando deja de hablar se achica, se pone gris y se va a
       un costado (arriba a la derecha del cuadro), y el que sigue pasa
       a estar grande.
    4. IKI muestra la carta que dejo el secuestrador (con la foto de
       assets/historia/carta_foto.png y la silueta de
       assets/historia/silueta.png).

Controles: ENTER / ESPACIO / click pasan el texto (si el texto se esta
escribiendo, lo completan). ESC saltea la escena entera.

Despues de verla (o saltearla) se guarda historia.txt y no vuelve a
aparecer (ver archivos.py).

El dialogo esta en DIALOGO, mas abajo: se puede cambiar el texto, el
orden o quien habla sin tocar nada mas.
"""

import math
import os
import sys

import pygame

import sonidos


CARPETA = os.path.dirname(os.path.abspath(__file__))

FPS = 60

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 214, 64)


# ==========================================================
# PERSONAJES DE LA ESCENA
# ==========================================================

# nombre -> (ruta del sprite de frente, color del cartel con el nombre)
PERSONAJES = {
    "BAUTO": ("assets/personajes/BAUTO/bauto frente.png", (200, 60, 70)),
    "BENJA": ("assets/personajes/BENJA/benja frente.png", (40, 70, 170)),
    "CASTRO": ("assets/personajes/CASTRO/castro frente.png", (210, 40, 40)),
    "POSHO": ("assets/personajes/POSHO/posho frente.png", (150, 40, 60)),
    "THIAGO": ("assets/personajes/THIAGO/thiago frente.png", (40, 110, 210)),
    # Iki de frente (lo arma herramientas/generar_desde_bauto.py con el
    # molde de Bauto; su dibujo original es iki frente.png)
    "IKI": ("assets/personajes/IKI/frente.png", (30, 130, 70)),
}

# Los cinco Compu Bros, de izquierda a derecha en el pasillo
COMPU_BROS = ["BAUTO", "BENJA", "CASTRO", "POSHO", "THIAGO"]


# ==========================================================
# DIALOGO (quien habla, que dice)
# ==========================================================

# ("CARTA", None) es el momento en que se muestra la carta (ver CARTA).

DIALOGO = [
    ("IKI", "¡COMPU BROS! ¡COMPU BROS! ¡Tengo que contarles algo terrible!"),
    ("BENJA", "Tranqui, Iki. Respirá... ¿Qué pasó?"),
    ("IKI", "¡Se llevaron al princesito Mxroy!"),
    ("CASTRO", "¿¡QUÉ!? ¿Quién se lo llevó?"),
    ("IKI", "Estaba chismeando con sus amigas mientras los demás jugaban al fútbol y desapareció."),
    ("POSHO", "¿Y nadie vio nada?"),
    ("THIAGO", "¿No dejaron ninguna pista?"),
    ("IKI", "Lo único que quedó es esta carta."),
    ("CARTA", None),
    ("BAUTO", "¡Vamos, Compu Bros! ¡A rescatar al princesito Mxroy!"),
]


# ==========================================================
# LA CARTA DEL SECUESTRADOR
# ==========================================================

CARTA_SALUDO = "Diminutos Compu Broskis."

CARTA_CUERPO = (
    "Hoy bajo este lecho reclamo el alma del princesito Mxroy, si ustedes "
    "quiereis recuperarle, tendreis que buscarme en la Tierra donde todo es "
    "próspero todavia se monta al caballo y fue el primer monumento a la "
    "bandera de Argentina, ya sabes de que hablo."
)

CARTA_PD = "PD: Sois unos maricones"

CARTA_FIRMA = ["Att: Lord Teichi de las", "Tinieblas Tenebrosas VIII"]

# Foto que aparece al lado de la PD
CARTA_FOTO = "assets/historia/carta_foto.png"

# Silueta misteriosa (pixel art, fondo transparente) abajo de la PD
CARTA_SILUETA = "assets/historia/silueta.png"


# ==========================================================
# TIEMPOS (en segundos)
# ==========================================================

DURACION_CHARLA = 3.0       # los bros charlando antes de que entre IKI
DURACION_ENTRADA = 0.9      # IKI cruzando la pantalla
PAUSA_SORPRESA = 0.6        # el "!" sobre los bros antes del dialogo
LETRAS_POR_SEGUNDO = 38     # velocidad a la que se escribe el texto
VELOCIDAD_RETRATOS = 12.0   # que tan rapido se mueven/achican los retratos


# ==========================================================
# MEDIDAS DE LA PANTALLA (800 x 600)
# ==========================================================

ESCALA_ESCENA = 3           # sprites en el pasillo (30x32 -> 90x96)
PISO_Y = 352                # donde apoyan los pies en el pasillo
X_BROS = [130, 235, 340, 445, 550]
X_IKI = 690

ALTURA_SALTITO = 7          # cuanto suben al "hablar"
PERIODO_SALTITO = 0.32      # segundos de cada subida y bajada

CUADRO = pygame.Rect(16, 436, 768, 150)     # el cuadro de texto

ESCALA_GRANDE = 6           # el que habla (30x32 -> 180x192)
ESCALA_CHICA = 2            # los que ya hablaron (60x64), grises

# Retrato grande: los pies apoyados adentro del cuadro, a la izquierda
RETRATO_GRANDE = pygame.Rect(0, 0, 30 * ESCALA_GRANDE, 32 * ESCALA_GRANDE)
RETRATO_GRANDE.midbottom = (CUADRO.x + 112, CUADRO.bottom - 8)

TEXTO_X = CUADRO.x + 220
TEXTO_Y = CUADRO.y + 22
TEXTO_ANCHO = CUADRO.right - 44 - TEXTO_X

# Fila de los que ya hablaron: arriba del cuadro, contra la derecha
SEPARACION_BANCO = 66


# ==========================================================
# IMAGENES
# ==========================================================

def _cargar(ruta):

    return pygame.image.load(os.path.join(CARPETA, ruta)).convert_alpha()


def _en_gris(imagen):
    """Copia en escala de grises y un poco mas oscura."""

    gris = imagen.copy()

    for x in range(gris.get_width()):
        for y in range(gris.get_height()):
            r, g, b, a = gris.get_at((x, y))
            if a:
                v = int((r * 0.3 + g * 0.59 + b * 0.11) * 0.62)
                gris.set_at((x, y), (v, v, v, a))

    return gris


def _escalar(imagen, escala):

    return pygame.transform.scale(
        imagen,
        (imagen.get_width() * escala, imagen.get_height() * escala)
    )


def _cargar_fondo(ancho, alto):
    """
    El pasillo del Instituto Huergo (la capa de adelante del nivel 1),
    recortado cerca del SALON DE ACTOS y agrandado. Abajo se repite el
    piso hasta llenar la pantalla.
    """

    pantalla_fondo = pygame.Surface((ancho, alto))
    pantalla_fondo.fill((24, 20, 32))

    try:
        capa = _cargar("assets/niveles/nivel_01_ciudad.png")
    except (pygame.error, FileNotFoundError):
        return pantalla_fondo

    recorte = pygame.Rect(1150, 95, 400, 217)
    recorte = recorte.clip(capa.get_rect())

    pasillo = pygame.Surface(recorte.size)
    pasillo.fill((40, 34, 48))
    pasillo.blit(capa, (0, 0), recorte)
    pasillo = _escalar(pasillo, 2)

    x = (ancho - pasillo.get_width()) // 2
    pantalla_fondo.blit(pasillo, (x, 0))

    # Piso: se repite la franja de abajo del pasillo
    alto_piso = 90
    franja = pygame.Rect(0, pasillo.get_height() - alto_piso, pasillo.get_width(), alto_piso)
    y = pasillo.get_height()
    while y < alto:
        pantalla_fondo.blit(pasillo, (x, y), franja)
        y += alto_piso

    return pantalla_fondo


# ==========================================================
# TEXTO
# ==========================================================

def _partir_en_lineas(fuente, texto, ancho_max):
    """Corta el texto en lineas que entran en ancho_max."""

    lineas = []
    actual = ""

    for palabra in texto.split(" "):
        prueba = palabra if not actual else actual + " " + palabra
        if fuente.size(prueba)[0] <= ancho_max or not actual:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra

    if actual:
        lineas.append(actual)

    return lineas


def _dibujar_texto_con_sombra(pantalla, fuente, texto, color, pos):

    pantalla.blit(fuente.render(texto, True, NEGRO), (pos[0] + 2, pos[1] + 2))
    pantalla.blit(fuente.render(texto, True, color), pos)


# ==========================================================
# RETRATOS (el que habla grande, los demas chicos y grises)
# ==========================================================

class Retrato:

    def __init__(self, nombre, imagen):

        self.nombre = nombre
        self.color = imagen
        self.gris = _en_gris(imagen)

        # Posicion y tamano que se ven (se acercan solos al objetivo)
        self.rect = [0.0, 0.0, 0.0, 0.0]     # centro x, base y, ancho, alto
        self.cuanto_gris = 0.0
        self.visible = False

        self.objetivo = [0.0, 0.0, 0.0, 0.0]
        self.objetivo_gris = 0.0

    def mandar_a(self, centro_x, base_y, escala, gris):

        ancho = self.color.get_width() * escala
        alto = self.color.get_height() * escala

        self.objetivo = [float(centro_x), float(base_y), float(ancho), float(alto)]
        self.objetivo_gris = 1.0 if gris else 0.0

        if not self.visible:
            # Aparece por primera vez: crece desde su lugar, sin color gris
            self.rect = [float(centro_x), float(base_y), 0.0, 0.0]
            self.cuanto_gris = self.objetivo_gris
            self.visible = True

    def actualizar(self, dt):

        k = 1.0 - math.exp(-VELOCIDAD_RETRATOS * dt)

        for i in range(4):
            self.rect[i] += (self.objetivo[i] - self.rect[i]) * k

        self.cuanto_gris += (self.objetivo_gris - self.cuanto_gris) * k

    def dibujar(self, pantalla, saltito=0):

        if not self.visible:
            return

        ancho = int(round(self.rect[2]))
        alto = int(round(self.rect[3]))

        if ancho < 2 or alto < 2:
            return

        x = int(round(self.rect[0] - ancho / 2))
        y = int(round(self.rect[1] - alto)) - saltito

        gris = pygame.transform.scale(self.gris, (ancho, alto))
        color = pygame.transform.scale(self.color, (ancho, alto))

        # Mezcla entre el gris y el color segun cuanto_gris
        if self.cuanto_gris > 0.01:
            pantalla.blit(gris, (x, y))

        if self.cuanto_gris < 0.99:
            color.set_alpha(int(255 * (1.0 - self.cuanto_gris)))
            pantalla.blit(color, (x, y))


# ==========================================================
# DIBUJO DE LA ESCENA
# ==========================================================

def _saltito(t, fase):
    """Altura del "estoy hablando": sube y baja rapido."""

    return int(abs(math.sin((t / PERIODO_SALTITO + fase) * math.pi)) * ALTURA_SALTITO)


def _dibujar_globo(pantalla, fuente, centro_x, base_y, texto):
    """Globito de dialogo chiquito arriba de la cabeza."""

    imagen = fuente.render(texto, True, NEGRO)
    rect = imagen.get_rect()
    rect.inflate_ip(14, -6)
    rect.midbottom = (centro_x + 18, base_y)

    pygame.draw.rect(pantalla, BLANCO, rect)
    pygame.draw.rect(pantalla, NEGRO, rect, 3)

    # Colita del globo
    pygame.draw.polygon(
        pantalla,
        BLANCO,
        [(rect.x + 10, rect.bottom - 3), (rect.x + 22, rect.bottom - 3), (rect.x + 8, rect.bottom + 9)]
    )
    pygame.draw.line(pantalla, NEGRO, (rect.x + 10, rect.bottom - 1), (rect.x + 8, rect.bottom + 9), 3)
    pygame.draw.line(pantalla, NEGRO, (rect.x + 22, rect.bottom - 1), (rect.x + 8, rect.bottom + 9), 3)

    pantalla.blit(imagen, imagen.get_rect(center=(rect.centerx, rect.centery + 1)))


def _dibujar_sombra(pantalla, centro_x, ancho):

    sombra = pygame.Surface((ancho, 12), pygame.SRCALPHA)
    pygame.draw.ellipse(sombra, (0, 0, 0, 90), sombra.get_rect())
    pantalla.blit(sombra, (centro_x - ancho // 2, PISO_Y - 7))


def _dibujar_signo(pantalla, fuente, texto, color, centro_x, base_y):
    """Signo de sorpresa ("!") con sombra, arriba de una cabeza."""

    sombra = fuente.render(texto, True, NEGRO)
    imagen = fuente.render(texto, True, color)
    rect = imagen.get_rect(midbottom=(centro_x, base_y))

    for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3)):
        pantalla.blit(sombra, (rect.x + dx, rect.y + dy))

    pantalla.blit(imagen, rect)


def _dibujar_cuadro(pantalla, fuente_nombre, nombre, color_nombre):

    # Borde doble pixelado: negro afuera, blanco, y el fondo azul oscuro
    pygame.draw.rect(pantalla, NEGRO, CUADRO.inflate(8, 8))
    pygame.draw.rect(pantalla, BLANCO, CUADRO)
    pygame.draw.rect(pantalla, (18, 22, 58), CUADRO.inflate(-10, -10))

    # Panel del retrato (un poco mas claro)
    panel = pygame.Rect(CUADRO.x + 14, CUADRO.y + 14, 196, CUADRO.height - 28)
    pygame.draw.rect(pantalla, (36, 44, 98), panel)
    pygame.draw.rect(pantalla, (70, 84, 160), panel, 3)

    # Cartel con el nombre, encima del borde del cuadro
    imagen = fuente_nombre.render(nombre, True, BLANCO)
    cartel = imagen.get_rect()
    cartel.inflate_ip(24, -4)
    cartel.bottomleft = (TEXTO_X - 6, CUADRO.y + 10)

    pygame.draw.rect(pantalla, NEGRO, cartel.inflate(8, 8))
    pygame.draw.rect(pantalla, color_nombre, cartel)
    pygame.draw.rect(pantalla, BLANCO, cartel, 3)

    _dibujar_texto_con_sombra(
        pantalla,
        fuente_nombre,
        nombre,
        BLANCO,
        imagen.get_rect(center=(cartel.centerx, cartel.centery + 1)).topleft
    )


def _dibujar_flechita(pantalla, t):
    """Triangulo que titila abajo a la derecha: "apreta para seguir"."""

    if int(t * 2.5) % 2:
        return

    x = CUADRO.right - 30
    y = CUADRO.bottom - 24 + int(math.sin(t * 6) * 2)

    pygame.draw.polygon(pantalla, NEGRO, [(x - 8, y - 3), (x + 10, y - 3), (x + 1, y + 9)])
    pygame.draw.polygon(pantalla, AMARILLO, [(x - 7, y - 5), (x + 7, y - 5), (x, y + 5)])


# ==========================================================
# CARTA
# ==========================================================

PAPEL = (236, 220, 178)
PAPEL_OSCURO = (196, 168, 112)
TINTA = (58, 34, 22)
TINTA_ROJA = (140, 20, 20)

HOJA = pygame.Rect(40, 24, 720, 552)


def _armar_carta(fuente):
    """Dibuja la carta completa (papel, texto y foto) en una Surface."""

    hoja = pygame.Surface(HOJA.size, pygame.SRCALPHA)
    hoja.fill((0, 0, 0, 0))

    papel = hoja.get_rect()
    pygame.draw.rect(hoja, NEGRO, papel)
    pygame.draw.rect(hoja, PAPEL_OSCURO, papel.inflate(-8, -8))
    pygame.draw.rect(hoja, PAPEL, papel.inflate(-20, -20))

    # Esquinas "gastadas"
    for x, y in ((4, 4), (papel.right - 20, 4), (4, papel.bottom - 20), (papel.right - 20, papel.bottom - 20)):
        pygame.draw.rect(hoja, PAPEL_OSCURO, (x, y, 16, 16))

    margen = 40
    ancho_texto = papel.width - margen * 2
    alto_linea = fuente.get_height() - 2
    y = 36

    hoja.blit(fuente.render(CARTA_SALUDO, True, TINTA), (margen, y))
    y += alto_linea + 12

    for linea in _partir_en_lineas(fuente, CARTA_CUERPO, ancho_texto):
        hoja.blit(fuente.render(linea, True, TINTA), (margen, y))
        y += alto_linea

    y += 18

    # Abajo: PD y firma a la izquierda, la foto a la derecha
    lado_foto = papel.bottom - 28 - y
    lado_foto = max(120, min(lado_foto, 300))
    x_foto = papel.right - margen - lado_foto
    ancho_izq = x_foto - margen - 20

    y_izq = y + 10
    for linea in _partir_en_lineas(fuente, CARTA_PD, ancho_izq):
        hoja.blit(fuente.render(linea, True, TINTA_ROJA), (margen, y_izq))
        y_izq += alto_linea

    # Flechita de la PD a la foto
    flecha_y = y_izq - alto_linea // 2
    pygame.draw.line(hoja, TINTA_ROJA, (margen + 10, flecha_y + 18), (x_foto - 14, flecha_y + 18), 3)
    pygame.draw.polygon(
        hoja,
        TINTA_ROJA,
        [(x_foto - 6, flecha_y + 18), (x_foto - 18, flecha_y + 11), (x_foto - 18, flecha_y + 25)]
    )

    y_firma = papel.bottom - 34 - alto_linea * len(CARTA_FIRMA)
    for k, linea in enumerate(CARTA_FIRMA):
        hoja.blit(fuente.render(linea, True, TINTA), (margen, y_firma + k * alto_linea))

    # Silueta: entre la PD y la firma, a la izquierda, lo mas grande
    # posible sin deformar los pixeles
    try:
        silueta = _cargar(CARTA_SILUETA)

        arriba = flecha_y + 36
        abajo = y_firma - 10
        escala = int(min(
            (abajo - arriba) / silueta.get_height(),
            ancho_izq / silueta.get_width()
        ))

        if escala >= 1:
            silueta = _escalar(silueta, escala)
            hoja.blit(
                silueta,
                silueta.get_rect(midbottom=(margen + ancho_izq // 2, abajo))
            )

    except (pygame.error, FileNotFoundError):
        pass

    try:
        foto = _cargar(CARTA_FOTO)
        try:
            foto = pygame.transform.smoothscale(foto, (lado_foto, lado_foto))
        except (ValueError, pygame.error):
            foto = pygame.transform.scale(foto, (lado_foto, lado_foto))

        marco = pygame.Rect(x_foto, y, lado_foto, lado_foto)
        pygame.draw.rect(hoja, NEGRO, marco.inflate(12, 12))
        pygame.draw.rect(hoja, BLANCO, marco.inflate(6, 6))
        hoja.blit(foto, marco)

    except (pygame.error, FileNotFoundError):
        pass

    return hoja


def _dibujar_carta(pantalla, hoja, aparicion, t):
    """La carta entra desde abajo; aparicion va de 0 a 1."""

    ancho, alto = pantalla.get_size()

    velo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    velo.fill((0, 0, 0, int(170 * aparicion)))
    pantalla.blit(velo, (0, 0))

    suave = 1 - (1 - aparicion) ** 3
    y = int(HOJA.y + (alto - HOJA.y) * (1 - suave))
    pantalla.blit(hoja, (HOJA.x, y))

    if aparicion >= 1.0 and not int(t * 2.5) % 2:
        x = HOJA.right - 28
        y_flecha = HOJA.bottom - 22 + int(math.sin(t * 6) * 2)
        pygame.draw.polygon(pantalla, NEGRO, [(x - 8, y_flecha - 3), (x + 10, y_flecha - 3), (x + 1, y_flecha + 9)])
        pygame.draw.polygon(pantalla, TINTA_ROJA, [(x - 7, y_flecha - 5), (x + 7, y_flecha - 5), (x, y_flecha + 5)])


# ==========================================================
# ESCENA
# ==========================================================

def escena_historia(pantalla, reloj, fuente_grande, fuente_media):
    """
    Muestra la escena completa. Vuelve cuando termina el dialogo o
    cuando el jugador aprieta ESC.
    """

    try:
        _escena(pantalla, reloj, fuente_grande, fuente_media)
    finally:
        # Que el teclado no siga sonando despues de la escena
        sonidos.detener("teclado")


def _escena(pantalla, reloj, fuente_grande, fuente_media):

    ancho, alto = pantalla.get_size()

    fuente_texto = fuente_media
    fuente_nombre = fuente_media
    fuente_globo = type(fuente_media)(2)

    fuente_signo = type(fuente_media)(4)

    fondo = _cargar_fondo(ancho, alto)

    hoja_carta = _armar_carta(type(fuente_media)(2))
    t_carta = None          # cuando aparecio la carta (None = no esta)

    sprites = {}
    for nombre, (ruta, _) in PERSONAJES.items():
        try:
            sprites[nombre] = _cargar(ruta)
        except (pygame.error, FileNotFoundError):
            # Si falta el dibujo (por ejemplo IKI) se usa el de BENJA
            sprites[nombre] = _cargar(PERSONAJES["BENJA"][0])

    en_escena = {nombre: _escalar(sprites[nombre], ESCALA_ESCENA) for nombre in sprites}

    # Iki entra caminando desde la derecha: sus poses de caminar dadas
    # vuelta (miran a la izquierda). Las genera herramientas/generar_historicos.py
    iki_caminando = []
    try:
        for archivo in ("frame_1.png", "frame_2.png", "frame_3.png", "frame_2.png"):
            imagen = _escalar(_cargar("assets/personajes/IKI/" + archivo), ESCALA_ESCENA)
            iki_caminando.append(pygame.transform.flip(imagen, True, False))
    except (pygame.error, FileNotFoundError):
        iki_caminando = []

    retratos = {nombre: Retrato(nombre, sprites[nombre]) for nombre in sprites}

    # Los que ya hablaron, en el orden en que se fueron al costado
    banco = []
    hablando = None

    # Lineas ya cortadas para que entren en el cuadro
    lineas_dialogo = [
        (quien, _partir_en_lineas(fuente_texto, texto, TEXTO_ANCHO) if texto else [])
        for quien, texto in DIALOGO
    ]

    linea = -1              # cual del DIALOGO se esta mostrando
    letras = 0.0            # cuantas letras ya se escribieron
    total_letras = 0

    t = 0.0
    t_dialogo = None        # cuando arranco el dialogo
    musica_bajada = False

    def pasar_a(indice):
        nonlocal linea, letras, total_letras, hablando, t_carta

        linea = indice
        letras = 0.0
        quien, partes = lineas_dialogo[linea]
        total_letras = sum(len(p) for p in partes)

        # La carta no es un personaje: se muestra encima de todo y el que
        # hablaba (IKI) queda grande abajo
        if quien == "CARTA":
            t_carta = t
            sonidos.detener("teclado")
            sonidos.reproducir("carta")
            return

        t_carta = None

        if quien != hablando:

            # El que hablaba se achica, se pone gris y va al costado
            if hablando is not None and hablando not in banco:
                banco.append(hablando)

            # El nuevo sale del costado (si estaba) y pasa a estar grande
            if quien in banco:
                banco.remove(quien)

            hablando = quien

            retratos[quien].mandar_a(
                RETRATO_GRANDE.centerx,
                RETRATO_GRANDE.bottom,
                ESCALA_GRANDE,
                gris=False
            )

            for i, nombre in enumerate(banco):
                retratos[nombre].mandar_a(
                    CUADRO.right - 34 - i * SEPARACION_BANCO,
                    CUADRO.y - 10,
                    ESCALA_CHICA,
                    gris=True
                )

    while True:

        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        t += dt

        # --------------------------------------------------
        # EVENTOS
        # --------------------------------------------------

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

        # --------------------------------------------------
        # FASES
        # --------------------------------------------------

        t_entrada = DURACION_CHARLA
        t_llego = t_entrada + DURACION_ENTRADA
        t_hablar = t_llego + PAUSA_SORPRESA

        # Cuando entra IKI se va apagando la musica del menu
        if t >= t_entrada and not musica_bajada:
            musica_bajada = True
            try:
                pygame.mixer.music.fadeout(900)
            except pygame.error:
                pass

        # Antes del dialogo, apretar adelanta la escena hasta que entra IKI
        if avanzar and linea < 0:
            if t < t_entrada:
                t = t_entrada
            elif t < t_hablar:
                t = t_hablar
            avanzar = False

        if linea < 0 and t >= t_hablar:
            t_dialogo = t
            pasar_a(0)

        if linea >= 0:

            if letras < total_letras:
                letras = min(total_letras, letras + LETRAS_POR_SEGUNDO * dt)

            if avanzar and t_carta is not None and t - t_carta < 0.45:
                # Mientras la carta entra, apretar no la saca
                avanzar = False

            if avanzar:
                if letras < total_letras:
                    letras = total_letras
                elif linea + 1 < len(lineas_dialogo):
                    sonidos.reproducir("boton")
                    pasar_a(linea + 1)
                else:
                    sonidos.reproducir("boton")
                    return

        for retrato in retratos.values():
            retrato.actualizar(dt)

        # --------------------------------------------------
        # DIBUJAR EL PASILLO
        # --------------------------------------------------

        pantalla.blit(fondo, (0, 0))

        escribiendo = linea >= 0 and letras < total_letras

        # Sonido de teclado mientras se escribe el dialogo
        if escribiendo:
            sonidos.reproducir_en_bucle("teclado")
        else:
            sonidos.detener("teclado")

        for i, nombre in enumerate(COMPU_BROS):

            if t < t_entrada:
                # Charlando: todos suben y bajan, cada uno a su ritmo
                salto = _saltito(t, i * 0.37)
            elif linea >= 0 and nombre == hablando and escribiendo:
                salto = _saltito(t, 0)
            else:
                salto = 0

            imagen = en_escena[nombre]
            _dibujar_sombra(pantalla, X_BROS[i], 64)
            pantalla.blit(imagen, imagen.get_rect(midbottom=(X_BROS[i], PISO_Y - salto)))

            # Globitos de charla, uno distinto cada tanto
            if t < t_entrada and int(t * 1.6 + i * 1.7) % 3 == 0:
                _dibujar_globo(
                    pantalla,
                    fuente_globo,
                    X_BROS[i],
                    PISO_Y - imagen.get_height() - 6,
                    "..." if i % 2 else "bla"
                )

            # Sorpresa cuando llega IKI
            if t_llego <= t < t_hablar + 0.5:
                _dibujar_signo(
                    pantalla,
                    fuente_signo,
                    "!",
                    AMARILLO,
                    X_BROS[i],
                    PISO_Y - imagen.get_height() + 6
                )

        # IKI entra corriendo desde la derecha
        if t >= t_entrada:

            avance = min(1.0, (t - t_entrada) / DURACION_ENTRADA)
            avance = 1 - (1 - avance) ** 2          # frena al llegar
            x_iki = int(ancho + 80 + (X_IKI - ancho - 80) * avance)

            if avance < 1.0 and iki_caminando:
                salto = -4      # las poses de caminar tienen otro lienzo
            elif avance < 1.0:
                salto = int(abs(math.sin(t * 18)) * 10)    # corriendo
            elif linea >= 0 and hablando == "IKI" and escribiendo:
                salto = _saltito(t, 0)
            else:
                salto = 0

            imagen = en_escena["IKI"]
            if avance < 1.0 and iki_caminando:
                imagen = iki_caminando[int(t * 12) % len(iki_caminando)]
            _dibujar_sombra(pantalla, x_iki, 64)
            pantalla.blit(imagen, imagen.get_rect(midbottom=(x_iki, PISO_Y - salto)))

            # "!!" sobre IKI mientras llega
            if t < t_hablar:
                _dibujar_signo(
                    pantalla,
                    fuente_signo,
                    "!!",
                    (255, 80, 80),
                    x_iki,
                    PISO_Y - imagen.get_height() + 6 - salto
                )

        # --------------------------------------------------
        # DIALOGO
        # --------------------------------------------------

        if linea >= 0:

            # El pasillo se oscurece un poco para que se lea el dialogo
            velo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            aparicion = min(1.0, (t - t_dialogo) / 0.25)
            velo.fill((0, 0, 0, int(90 * aparicion)))
            pantalla.blit(velo, (0, 0))

            quien, partes = lineas_dialogo[linea]

            if quien == "CARTA":
                # Abajo sigue IKI (el ultimo que hablo) con el cuadro vacio
                quien, partes = hablando, []

            _dibujar_cuadro(pantalla, fuente_nombre, quien, PERSONAJES[quien][1])

            # Los que ya hablaron (chicos y grises, al costado)
            for nombre in banco:
                retratos[nombre].dibujar(pantalla)

            # El que habla, grande (sube y baja mientras se escribe)
            salto = _saltito(t, 0) // 2 if escribiendo else 0
            retratos[quien].dibujar(pantalla, salto)

            # Texto que se va escribiendo
            restantes = int(letras)
            alto_linea = fuente_texto.get_height() - 4
            for k, parte in enumerate(partes):
                if restantes <= 0:
                    break
                visible = parte[:restantes]
                restantes -= len(parte)
                _dibujar_texto_con_sombra(
                    pantalla,
                    fuente_texto,
                    visible,
                    BLANCO,
                    (TEXTO_X, TEXTO_Y + k * alto_linea)
                )

            if not escribiendo and t_carta is None:
                _dibujar_flechita(pantalla, t)

            if t_carta is not None:
                _dibujar_carta(pantalla, hoja_carta, min(1.0, (t - t_carta) / 0.45), t)

        # Ayuda chiquita arriba a la derecha
        ayuda = fuente_globo.render("ESC: saltear", True, (230, 230, 230))
        pantalla.blit(ayuda, ayuda.get_rect(topright=(ancho - 10, 8)))

        pygame.display.flip()

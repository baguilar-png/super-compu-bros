"""
NIVEL 2 - SAN TELMO

    El nivel arranca en la puerta de entrada del Instituto Huergo (de donde se
    sale en el nivel 1) y sigue por San Telmo. De fondo se ven edificios de la
    zona (dibujados de memoria, aproximados):

    * Facultad de Ingenieria de la UBA (Paseo Colon 850, el "Edificio
      Paseo Colon": bloque de piedra con un gran portico de columnas)
    * Escuela Industrial Otto Krause (Paseo Colon 650, escuela tecnica)
    * Mercado de San Telmo (1897, estructura de hierro, gran cupula central)
    * Iglesia Ortodoxa Rusa de la Santisima Trinidad (Parque Lezama,
      cupulas azules en forma de cebolla)
    * Museo Historico Nacional (Parque Lezama, la vieja quinta de la
      barranca)
    * Iglesia de San Pedro Gonzalez Telmo (dos torres con azulejos blancos)
"""

from pixelart import *  # noqa: F401,F403
from monumentos._comunes import cartel_nombre, ventana_fila


# ==========================================================
# MERCADO DE SAN TELMO
# ==========================================================

def mercado_san_telmo():

    ancho = 186
    alto = 112

    l = Lienzo(ancho, alto)

    base = alto - 1

    crema = rgb("#e6d6a4")
    rojo = rgb("#a9472f")
    hierro = rgb("#5f7f7c")

    # --- cupula central de hierro y vidrio (se ve detras de la fachada) ---
    cx = 93

    cupula(l, cx, base - 62, 30, 28, hierro, costillas=7,
           c_luz=rgb("#9fc2bc"), c_sombra=rgb("#46605e"), linterna=True)

    # paneles de vidrio entre las costillas
    for k in range(-24, 25, 8):

        for dy in range(6, 24, 6):

            x = cx + k

            if abs(k) < 30 * math.sqrt(max(0, 1 - (dy / 28) ** 2)) - 3:
                l.rect(x - 2, base - 62 - dy, x + 2, base - 62 - dy, VIDRIO_LUZ)

    l.rect(cx, base - 100, cx, base - 92, rgb("#3a3a3a"))
    l.rect(cx + 1, base - 100, cx + 4, base - 98, CELESTE_ARG)

    # --- cuerpo central del frente ---
    x0, x1 = 28, 158

    volumen(l, x0, base - 62, x1, base, crema, 1, 3)

    # franjas de ladrillo rojo
    l.rect(x0, base - 62, x1, base - 59, rojo)
    l.rect(x0, base - 62, x1, base - 62, luz(rojo, 0.25))
    l.rect(x0, base - 36, x1, base - 34, rojo)

    # cartel del mercado
    texto = "MERCADO DE SAN TELMO"

    w = ancho_texto(texto)

    sx = cx - w // 2

    l.rect(sx - 4, base - 58, sx + w + 3, base - 46, rgb("#1f4a38"))
    l.marco(sx - 4, base - 58, sx + w + 3, base - 46, ORO)

    l.texto(sx, base - 56, texto, BLANCO)

    # portal central con arco
    ventana_arco(l, 78, base - 6, 108, 37, VIDRIO, rojo)

    for x in range(81, 107, 5):
        l.rect(x, base - 40, x, base - 6, VIDRIO_OSC)

    l.rect(79, base - 26, 107, base - 26, VIDRIO_OSC)

    # puerta con escalones de marmol
    l.rect(88, base - 14, 98, base - 7, rgb("#3a2a22"))

    for i in range(3):
        l.rect(76 - i * 2, base - 6 + i * 2, 110 + i * 2, base - 5 + i * 2,
               rgb("#e9e4d6") if i % 2 == 0 else rgb("#cfc9bb"))

    # arcos a los costados (puestos)
    for lado in (-1, 1):

        for k in range(3):

            ax = cx + lado * (38 + k * 15) - 4

            ventana_arco(l, ax, base - 6, ax + 8, 26, VIDRIO, rojo)

            # toldo
            for j in range(0, 12, 3):
                l.rect(ax - 1 + j, base - 32, ax + 1 + j, base - 29,
                       [ROJO, BLANCO][(j // 3) % 2])

    # --- alas bajas ---
    for (a0, a1) in ((4, 27), (159, 182)):

        volumen(l, a0, base - 40, a1, base, crema, 1, 2)

        l.rect(a0, base - 40, a1, base - 38, rojo)

        for x in range(a0 + 4, a1 - 5, 9):

            ventana_arco(l, x, base - 8, x + 4, 18, VIDRIO, rojo)

    # farolitos de hierro en la entrada
    for x in (74, 112):

        l.rect(x, base - 20, x, base - 7, rgb("#2c3a3a"))
        l.rect(x - 1, base - 24, x + 1, base - 21, rgb("#f4e7a3"))

    return l


# ==========================================================
# IGLESIA ORTODOXA RUSA
# ==========================================================

def iglesia_rusa():

    ancho = 112
    alto = 140

    l = Lienzo(ancho, alto)

    base = alto - 1

    muro = rgb("#efe9dc")
    azul = rgb("#2f8fcc")
    azul_osc = rgb("#1f5f9c")

    cx = 56

    # --- cupulas de atras (las dos de los costados, mas altas que el cuerpo) ---
    for dx in (-31, 31):

        l.rect(cx + dx - 6, base - 70, cx + dx + 6, base - 46, muro)
        l.rect(cx + dx - 6, base - 70, cx + dx - 6, base - 46, luz(muro, 0.1))
        l.rect(cx + dx + 4, base - 70, cx + dx + 6, base - 46, sombra(muro, 0.85))
        l.rect(cx + dx - 2, base - 66, cx + dx + 1, base - 56, azul_osc)

        cebolla(l, cx + dx, base - 70, 18, 20, azul, estrellas=ORO)

    # --- tambor central y gran cupula ---
    l.rect(cx - 13, base - 100, cx + 13, base - 46, muro)
    l.rect(cx - 13, base - 100, cx - 13, base - 46, luz(muro, 0.1))
    l.rect(cx + 9, base - 100, cx + 13, base - 46, sombra(muro, 0.85))

    for dx in (-8, -2, 4):
        l.rect(cx + dx, base - 96, cx + dx + 2, base - 84, azul_osc)
        l.px(cx + dx, base - 96, azul)

    l.rect(cx - 14, base - 102, cx + 14, base - 100, azul_osc)

    cebolla(l, cx, base - 102, 30, 30, azul, estrellas=ORO)

    # --- cuerpo bajo ---
    volumen(l, 14, base - 46, 98, base, muro, 1, 3)

    l.rect(14, base - 46, 98, base - 43, azul_osc)
    l.rect(14, base - 46, 98, base - 46, azul)

    # ventanas con arco
    for x in (20, 30, 76, 86):

        ventana_arco(l, x, base - 8, x + 4, 22, azul_osc, muro)

        l.px(x + 1, base - 24, azul)

    # --- porche de entrada ---
    volumen(l, 40, base - 36, 72, base, muro, 1, 2)

    l.poly([(38, base - 36), (56, base - 52), (74, base - 36)], azul_osc)
    l.poly([(41, base - 37), (56, base - 49), (71, base - 37)], muro)

    l.rect(51, base - 49, 61, base - 47, azul)

    # arco de la puerta y cruz
    l.arco(49, base, 63, 26, rgb("#6a4a2a"))
    l.arco(51, base - 1, 61, 22, rgb("#8a6a3a"))

    l.rect(56, base - 44, 56, base - 40, ORO)
    l.rect(54, base - 43, 58, base - 43, ORO)

    # escalones
    for i in range(3):
        l.rect(44 - i * 2, base - 2 + i, 68 + i * 2, base - 2 + i, rgb("#cfc9bb"))

    return l


# ==========================================================
# SAN PEDRO TELMO
# ==========================================================

def _torre_telmo(l, cx, base):

    muro = rgb("#efe5cb")

    # cuerpo cubico
    volumen(l, cx - 11, base - 66, cx + 11, base, muro, 1, 3)

    l.rect(cx - 12, base - 68, cx + 12, base - 66, luz(muro, 0.3))

    # ventana de campanario
    ventana_arco(l, cx - 4, base - 40, cx + 4, 14, rgb("#2a3550"), rgb("#bfae86"))
    ventana_arco(l, cx - 3, base - 14, cx + 3, 10, rgb("#2a3550"), rgb("#bfae86"))

    # primer octogono
    volumen(l, cx - 8, base - 86, cx + 8, base - 68, muro, 1, 2)

    for x in (cx - 5, cx + 1):
        ventana_arco(l, x, base - 72, x + 3, 10, rgb("#2a3550"), rgb("#bfae86"))

    l.rect(cx - 9, base - 88, cx + 9, base - 86, rgb("#c9b78b"))

    # segundo octogono
    volumen(l, cx - 6, base - 102, cx + 6, base - 88, muro, 1, 2)

    l.rect(cx - 2, base - 98, cx + 1, base - 91, rgb("#2a3550"))

    l.rect(cx - 7, base - 104, cx + 7, base - 102, rgb("#c9b78b"))

    # azulejos blancos y azules en los remates
    for x in range(cx - 6, cx + 6, 2):
        l.px(x, base - 100, rgb("#6b8fd0"))

    # cupulita con linterna y cruz
    cupula(l, cx, base - 104, 7, 9, rgb("#7a8aa0"), costillas=2)

    l.rect(cx, base - 118, cx, base - 112, ORO)
    l.rect(cx - 2, base - 116, cx + 2, base - 116, ORO)


def san_pedro_telmo():

    ancho = 112
    alto = 130

    l = Lienzo(ancho, alto)

    base = alto - 1

    muro = rgb("#efe5cb")

    # cupula del crucero (atras)
    cupula(l, 56, base - 74, 17, 15, rgb("#8a97a8"), costillas=5, linterna=True, remate=ORO)

    l.rect(40, base - 90, 72, base - 74, muro)

    # torres
    _torre_telmo(l, 20, base)
    _torre_telmo(l, ancho - 21, base)

    # cuerpo central de la fachada
    volumen(l, 32, base - 76, ancho - 33, base, muro, 1, 3)

    # frontis curvo del remate
    l.poly([(32, base - 76), (56, base - 90), (ancho - 33, base - 76)], muro)
    l.linea(32, base - 76, 56, base - 90, luz(muro, 0.3))

    l.rect(51, base - 86, 61, base - 80, rgb("#2a3550"))

    # nicho con San Pedro Telmo
    l.arco(48, base - 40, 64, 22, rgb("#c9b78b"))
    l.arco(50, base - 41, 62, 19, rgb("#7a6a52"))

    figura(l, 56, base - 42, 14, rgb("#f4efe0"), pose="brazo_der", falda=True)

    # inscripcion
    l.rect(40, base - 62, 72, base - 62, rgb("#c9b78b"))

    for x in range(41, 72, 2):
        l.px(x, base - 58, rgb("#b0a074"))

    # portal con arco y puerta
    l.arco(47, base, 65, 30, rgb("#c9b78b"))
    l.arco(49, base - 1, 63, 26, rgb("#5a3a22"))

    l.rect(56, base - 24, 56, base - 1, rgb("#3a2518"))

    # puertas laterales
    for x in (36, 70):

        ventana_arco(l, x, base - 6, x + 5, 20, rgb("#5a3a22"), rgb("#c9b78b"))

    # ventanas del medio
    for x in (36, 70):

        ventana_arco(l, x, base - 38, x + 5, 12, rgb("#2a3550"), rgb("#c9b78b"))

    # escalinata de marmol
    for i in range(4):
        l.rect(40 - i * 2, base - 3 + i, 72 + i * 2, base - 3 + i,
               rgb("#e9e4d6") if i % 2 == 0 else rgb("#cfc9bb"))

    return l


# ==========================================================
# FACULTAD DE INGENIERIA (UBA)
# ==========================================================

def facultad_ingenieria():

    ancho = 188
    alto = 118

    l = Lienzo(ancho, alto)

    base = alto - 1

    piedra = rgb("#d9d2bf")
    gris = rgb("#b9b4a6")

    cx = ancho // 2

    # alas laterales
    for (a, b) in ((4, 62), (ancho - 63, ancho - 5)):

        volumen(l, a, base - 66, b, base, piedra, 1, 3)

        l.rect(a - 1, base - 69, b + 1, base - 66, gris)

        ventana_fila(l, a + 6, b - 5, base - 46, 5, 14, 6, VIDRIO, rgb("#efe9d8"))
        ventana_fila(l, a + 6, b - 5, base - 14, 5, 14, 6, VIDRIO, rgb("#efe9d8"))

        l.rect(a, base - 30, b, base - 29, gris)

    # cuerpo central, mas alto, con el gran portico
    volumen(l, 58, base - 82, ancho - 59, base, piedra, 1, 3)

    l.rect(56, base - 86, ancho - 57, base - 82, gris)

    # remate con estatuas
    for x in range(64, ancho - 62, 14):

        l.rect(x, base - 94, x + 3, base - 86, sombra(piedra, 0.85))

    # el portico: columnas altas y arquitrabe
    l.rect(62, base - 74, ancho - 63, base - 70, luz(piedra, 0.25))

    columnas(l, 70, ancho - 71, base - 70, base - 8, 8, 6, rgb("#efe9d8"))

    # entrada oscura entre las columnas
    l.rect(cx - 10, base - 52, cx + 10, base - 8, rgb("#3a3a46"))
    l.rect(cx - 10, base - 52, cx + 10, base - 50, VIDRIO)

    # escalinata ancha
    for i in range(5):

        l.rect(60 - i * 2, base - 6 + i, ancho - 61 + i * 2, base - 6 + i,
               rgb("#e9e4d6") if i % 2 == 0 else rgb("#cfc9bb"))

    # bandera
    bandera(l, cx, base - 94, 14, 10, 6)

    cartel_nombre(l, cx, base - 66, "INGENIERIA", rgb("#7a1f2a"))

    return l


# ==========================================================
# ESCUELA INDUSTRIAL OTTO KRAUSE
# ==========================================================

def escuela_otto_krause():

    ancho = 168
    alto = 112

    l = Lienzo(ancho, alto)

    base = alto - 1

    ladrillo = rgb("#b5603f")
    crema = rgb("#eadcb8")

    cx = ancho // 2

    # alas de ladrillo con ventanas de arco
    for (a, b) in ((4, 56), (ancho - 57, ancho - 5)):

        ladrillos(l, a, base - 50, b, base, ladrillo)

        l.rect(a - 1, base - 53, b + 1, base - 50, crema)

        ventana_fila(l, a + 5, b - 4, base - 28, 7, 15, 6, VIDRIO, crema, arco=True)

        l.rect(a - 1, base - 5, b + 1, base - 4, crema)

    # techos de las alas
    for (a, b) in ((2, 58), (ancho - 59, ancho - 3)):

        l.poly([(a, base - 53), (a + 8, base - 64), (b - 8, base - 64), (b, base - 53)], rgb("#5f6a78"))

    # cuerpo central con frontis
    volumen(l, 52, base - 70, ancho - 53, base, crema, 1, 3)

    fronton(l, 50, ancho - 51, base - 70, 18, crema, rgb("#cfc09c"), rgb("#f4ecd6"))

    # ojo de buey y cartel en el frontis
    l.circulo(cx, base - 80, 4, rgb("#4a4038"))
    l.circulo(cx, base - 80, 3, rgb("#f4f1e8"))

    # columnas de la entrada
    columnas(l, 62, ancho - 63, base - 60, base - 6, 4, 5, rgb("#f4ecd6"))

    l.arco(cx - 7, base - 5, cx + 7, 34, rgb("#3a2a22"))

    ventana_fila(l, 58, 70, base - 20, 5, 14, 6, VIDRIO, rgb("#cfc09c"))
    ventana_fila(l, ancho - 71, ancho - 59, base - 20, 5, 14, 6, VIDRIO, rgb("#cfc09c"))

    for i in range(4):

        l.rect(54 - i * 2, base - 3 + i, ancho - 55 + i * 2, base - 3 + i,
               rgb("#e9e4d6") if i % 2 == 0 else rgb("#cfc9bb"))

    # bandera en el mastil
    bandera(l, cx, base - 88, 16, 10, 6)

    cartel_nombre(l, cx, base - 56, "OTTO KRAUSE", rgb("#1f3f78"))

    return l


# ==========================================================
# MUSEO HISTORICO NACIONAL (PARQUE LEZAMA)
# ==========================================================

def museo_historico_nacional():

    ancho = 150
    alto = 108

    l = Lienzo(ancho, alto)

    base = alto - 1

    ocre = rgb("#e0c07a")
    blanco = rgb("#f4ecd6")
    teja = rgb("#a9472f")

    # palmeras y arboles del parque
    arbol(l, 8, base - 1, 80, "palmera", seed=5)
    arbol(l, ancho - 8, base - 1, 76, "palmera", seed=6)

    cx = ancho // 2

    # planta alta
    volumen(l, 22, base - 66, ancho - 23, base - 30, ocre, 1, 3)

    # techo de teja a cuatro aguas
    l.poly([(16, base - 65), (32, base - 82), (ancho - 33, base - 82), (ancho - 17, base - 65)], teja)
    l.rect(16, base - 66, ancho - 17, base - 64, sombra(teja, 0.7))

    for y in range(base - 80, base - 66, 3):

        l.rect(32 - (base - 80 - y) // 1 + 0, y, ancho - 33 + (base - 80 - y) // 1, y, sombra(teja, 0.84))

    # ventanas de la planta alta, con persianas
    ventana_fila(l, 30, ancho - 31, base - 40, 7, 14, 9, VIDRIO, blanco)

    # planta baja con galeria de arcos
    volumen(l, 22, base - 30, ancho - 23, base, ocre, 1, 3)

    for x in range(28, ancho - 30, 14):

        l.arco(x, base - 1, x + 8, 22, blanco)
        l.arco(x + 1, base - 1, x + 7, 19, rgb("#2a3550"))

    # balcon corrido
    balcon(l, 20, ancho - 21, base - 32, rgb("#2c3a3a"), 3)

    # portico central con escalera y frontis chico
    volumen(l, cx - 14, base - 58, cx + 14, base - 30, blanco, 1, 2)

    fronton(l, cx - 15, cx + 15, base - 58, 10, blanco, rgb("#cfc4a8"), rgb("#f4ecd6"))

    columnas(l, cx - 10, cx + 10, base - 56, base - 31, 3, 3, blanco)

    # escalera de la barranca
    for i in range(5):

        l.rect(cx - 16 - i * 2, base - 6 + i, cx + 16 + i * 2, base - 6 + i,
               rgb("#e9e4d6") if i % 2 == 0 else rgb("#cfc9bb"))

    bandera(l, cx, base - 82, 14, 9, 6)

    cartel_nombre(l, cx, base - 27, "MUSEO", rgb("#1f3f78"))

    return l


MONUMENTOS = [
    dict(id="facultad_ingenieria", nombre="Facultad de Ingenieria (UBA)", fn=facultad_ingenieria),
    dict(id="escuela_otto_krause", nombre="Escuela Industrial Otto Krause", fn=escuela_otto_krause),
    dict(id="mercado_san_telmo", nombre="Mercado de San Telmo", fn=mercado_san_telmo),
    dict(id="iglesia_rusa", nombre="Catedral Ortodoxa Rusa (Parque Lezama)", fn=iglesia_rusa),
    dict(id="san_pedro_telmo", nombre="Iglesia de San Pedro Gonzalez Telmo", fn=san_pedro_telmo),
    dict(id="museo_historico_nacional", nombre="Museo Historico Nacional", fn=museo_historico_nacional),
]

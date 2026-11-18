"""
NIVEL 15 - LA BOMBONERA (JEFE)

    En la arena del jefe se ven de fondo La Bombonera y Caminito. El resto de
    los dibujos de La Boca (Puente Transbordador, Usina del Arte y el Tren
    del Roca) quedan disponibles. El Puente Nicolas Avellaneda se dibuja aca
    pero se usa en el nivel 20 (Avellaneda).

    * La Bombonera (estadio Alberto J. Armando, Brandsen 805): paredon azul,
      franja amarilla de travesanos en cruz, modulo central con el escudo y
      las tribunas azul - amarillo - azul (dibujada mirando una foto aerea)
    * Puente Nicolas Avellaneda (puente levadizo sobre el Riachuelo, 1940)
    * Tren del Ferrocarril Roca (las vias rodean la cancha)
"""

from pixelart import *  # noqa: F401,F403
from monumentos.la_boca import caminito, transbordador, usina_del_arte  # noqa: F401


# ==========================================================
# LA BOMBONERA
# ==========================================================

def bombonera():
    """
    La Bombonera vista de frente, como en las fotos: paredon azul con la
    franja amarilla de travesanos en diagonal, el modulo central con el
    escudo y, detras, las tribunas (azul - amarillo - azul) con el techo.
    """

    ancho = 272
    alto = 150

    l = Lienzo(ancho, alto)

    base = alto - 1

    cx = ancho // 2

    azul = AZUL_BOCA
    azul_osc = sombra(AZUL_BOCA, 0.62)
    azul_med = luz(AZUL_BOCA, 0.12)
    azul_luz = luz(AZUL_BOCA, 0.42)
    amarillo = AMARILLO_BOCA
    amarillo_osc = sombra(AMARILLO_BOCA, 0.78)
    cemento = rgb("#a4a9b1")
    cemento_osc = rgb("#7d838c")
    blanco = BLANCO

    r = random.Random(15)

    x_ini = 3
    x_fin = ancho - 4

    # ------------------------------------------------------
    # TRIBUNAS DE ATRAS (azul abajo - amarillo - azul arriba)
    # cada piso es un trapecio: se achica hacia arriba
    # ------------------------------------------------------

    def tribuna(y0, y1, in0, in1, c, c_fila, flecos=0):
        """Trapecio de y0 (arriba) a y1 (abajo); in0 / in1 = cuanto se
        mete desde cada borde arriba / abajo."""

        for y in range(y0, y1 + 1):

            t = (y - y0) / max(1, (y1 - y0))

            ent = in0 + (in1 - in0) * t

            a = round(x_ini + ent)
            b = round(x_fin - ent)

            l.rect(a, y, b, y, c)

            # fila de asientos cada 3 pixeles
            if (y - y0) % 3 == 2:

                l.rect(a, y, b, y, c_fila)

        # pasillos (escaleras) que bajan cada 17 pixeles
        for x in range(x_ini + 34, x_fin - 30, 17):

            for y in range(y0, y1 + 1):

                t = (y - y0) / max(1, (y1 - y0))

                ent = in0 + (in1 - in0) * t

                if x_ini + ent + 1 < x < x_fin - ent - 1:

                    l.px(x, y, c_fila)
                    l.px(x + 1, y, c_fila)

    y_rim = base - 94          # borde de arriba del paredon

    # piso de arriba (azul), de en medio (amarillo) y de abajo (azul)
    tribuna(y_rim - 56, y_rim - 40, 22, 18, azul_med, azul)
    tribuna(y_rim - 39, y_rim - 25, 18, 14, amarillo, amarillo_osc)
    tribuna(y_rim - 24, y_rim - 1, 14, 8, azul, azul_osc)

    # baranda de cada cambio de piso
    for yb, ent in ((y_rim - 39, 18), (y_rim - 24, 14)):

        l.rect(x_ini + ent, yb, x_fin - ent, yb, blanco)

    # techo: borde claro con la panza azul abajo y luces
    y_t = y_rim - 60

    l.rect(x_ini + 18, y_t, x_fin - 18, y_t + 3, cemento)
    l.rect(x_ini + 18, y_t, x_fin - 18, y_t, blanco)
    l.rect(x_ini + 18, y_t + 3, x_fin - 18, y_t + 3, cemento_osc)

    for x in range(x_ini + 26, x_fin - 24, 12):

        l.rect(x, y_t + 1, x + 2, y_t + 2, rgb("#fff3a8"))

    # tablero electronico del costado izquierdo
    l.rect(x_ini + 6, y_rim - 44, x_ini + 30, y_rim, azul_osc)
    l.rect(x_ini + 6, y_rim - 44, x_ini + 30, y_rim - 44, azul_luz)
    l.rect(x_ini + 9, y_rim - 40, x_ini + 27, y_rim - 26, rgb("#10131c"))
    l.rect(x_ini + 10, y_rim - 39, x_ini + 26, y_rim - 38, rgb("#2b3550"))

    for k in range(4):

        l.rect(x_ini + 12 + k * 4, y_rim - 34, x_ini + 13 + k * 4, y_rim - 31, amarillo)

    # ------------------------------------------------------
    # PAREDON EXTERIOR
    # ------------------------------------------------------

    # cemento de la vereda
    l.rect(x_ini - 2, base - 2, x_fin + 2, base, cemento)
    l.rect(x_ini - 2, base - 2, x_fin + 2, base - 2, luz(cemento, 0.3))

    # pared de arriba (azul liso con nervios)
    l.rect(x_ini, y_rim, x_fin, base - 62, azul)
    l.rect(x_ini, y_rim, x_fin, y_rim + 1, azul_luz)
    l.rect(x_ini, y_rim + 2, x_fin, y_rim + 2, azul_osc)

    # pared de abajo
    l.rect(x_ini, base - 33, x_fin, base - 3, azul)

    # franja amarilla: fondo oscuro + travesanos en cruz (enrejado)
    # (como en la foto)
    y_a0 = base - 62
    y_a1 = base - 34

    l.rect(x_ini, y_a0, x_fin, y_a1, azul_osc)

    def travesanos(x0, x1, sentido, periodo=13, grosor=8, giro=24):

        for y in range(y_a0 + 2, y_a1 - 1):

            t = (y - (y_a0 + 2)) / (y_a1 - 1 - (y_a0 + 2))

            desplaza = sentido * (t - 0.5) * giro

            for k in range(-4, (x1 - x0) // periodo + 5):

                a = round(x0 + k * periodo + desplaza)
                b = a + grosor - 1

                aa = max(x0, a)
                bb = min(x1, b)

                if aa > bb:
                    continue

                l.rect(aa, y, bb, y, amarillo)

                if b <= x1:
                    l.px(b, y, amarillo_osc)

    for sentido in (+1, -1):

        travesanos(x_ini, cx - 25, sentido, periodo=19, grosor=5, giro=26)
        travesanos(cx + 25, x_fin, sentido, periodo=19, grosor=5, giro=26)

    # rieles amarillos de arriba y de abajo de la franja
    l.rect(x_ini, y_a0, x_fin, y_a0 + 1, amarillo)
    l.rect(x_ini, y_a1 - 1, x_fin, y_a1, amarillo)
    l.rect(x_ini, y_a1, x_fin, y_a1, amarillo_osc)

    # nervios (columnas) del paredon
    for x in range(x_ini + 10, x_fin - 4, 22):

        if abs(x - cx) < 28:
            continue

        l.rect(x, y_rim + 3, x + 1, y_a0 - 1, azul_med)
        l.rect(x, y_a1 + 1, x + 1, base - 3, azul_med)

    # ventanitas de la pared de arriba
    for x in range(x_ini + 14, x_fin - 10, 22):

        if abs(x + 5 - cx) < 30:
            continue

        l.rect(x, y_rim + 8, x + 10, y_rim + 14, azul_osc)
        l.rect(x, y_rim + 8, x + 10, y_rim + 8, sombra(AZUL_BOCA, 0.45))

    # rejas / respiraderos de la pared de abajo
    for x in range(x_ini + 6, x_fin - 6, 11):

        if abs(x + 2 - cx) < 30:
            continue

        l.rect(x, base - 26, x + 3, base - 12, azul_osc)

        for yy in range(base - 25, base - 12, 3):

            l.rect(x, yy, x + 3, yy, sombra(AZUL_BOCA, 0.45))

    # puertas de acceso (tornos)
    for x in (34, 86, 172, 226):

        l.arco(x, base - 3, x + 11, 17, rgb("#0a0f2a"))

        l.arco(x + 2, base - 3, x + 9, 14, rgb("#1a2a6a"))

        for k in (4, 6, 8):

            l.rect(x + k - 1, base - 11, x + k - 1, base - 4, rgb("#9aa0b0"))

    # ------------------------------------------------------
    # MODULO CENTRAL (mas alto) con el escudo
    # ------------------------------------------------------

    mx0 = cx - 24
    mx1 = cx + 24

    y_m = y_rim - 14

    l.rect(mx0, y_m, mx1, base - 3, azul_med)
    l.rect(mx0, y_m, mx1, y_m + 1, azul_luz)
    l.rect(mx0, y_m, mx0, base - 3, azul_luz)
    l.rect(mx1, y_m + 2, mx1, base - 3, azul_osc)

    # la franja amarilla sigue de lado a lado
    l.rect(mx0, y_a0, mx1, y_a0 + 1, amarillo)
    l.rect(mx0, y_a1 - 1, mx1, y_a1, amarillo)
    l.rect(mx0 + 3, y_a0 + 2, mx1 - 3, y_a1 - 2, azul_osc)

    for x in range(mx0 + 5, mx1 - 4, 6):

        l.rect(x, y_a0 + 2, x + 1, y_a1 - 2, amarillo_osc)

    # ventanal del modulo (arriba)
    l.rect(mx0 + 6, y_m + 6, mx1 - 6, y_m + 9, azul_osc)

    # escudo (azul con franja amarilla y borde blanco)
    ex = cx
    ey = y_a0 - 31

    escudo = [(ex - 10, ey), (ex + 10, ey), (ex + 10, ey + 14), (ex, ey + 25), (ex - 10, ey + 14)]

    l.poly(escudo, blanco)

    interior = [(ex - 8, ey + 2), (ex + 8, ey + 2), (ex + 8, ey + 13), (ex, ey + 22), (ex - 8, ey + 13)]

    l.poly(interior, azul)

    l.rect(ex - 8, ey + 8, ex + 8, ey + 14, amarillo)

    # estrellitas del escudo
    for dx in (-5, -1, 3):

        l.rect(ex + dx, ey + 4, ex + dx + 1, ey + 5, blanco)

    # entrada central
    l.arco(cx - 9, base - 3, cx + 9, 26, rgb("#0a0f2a"))
    l.arco(cx - 7, base - 3, cx + 7, 23, rgb("#1a2a6a"))

    for k in range(-5, 6, 3):

        l.rect(cx + k, base - 18, cx + k, base - 4, rgb("#9aa0b0"))

    # cartel con el nombre sobre la franja del modulo
    texto = "BOCA"

    w = ancho_texto(texto, 1)

    l.rect(cx - w // 2 - 3, y_a0 + 9, cx + w // 2 + 2, y_a0 + 19, azul_osc)
    l.marco(cx - w // 2 - 3, y_a0 + 9, cx + w // 2 + 2, y_a0 + 19, amarillo)
    l.texto(cx - w // 2, y_a0 + 11, texto, amarillo, 1)

    return l


# ==========================================================
# PUENTE NICOLAS AVELLANEDA
# ==========================================================

def puente_avellaneda():

    ancho = 232
    alto = 138

    l = Lienzo(ancho, alto)

    base = alto - 1

    acero = rgb("#7f9bb8")
    oscuro = rgb("#4a6280")
    brillo = rgb("#c4d6e8")

    # agua del Riachuelo
    agua_dibujo(l, 0, base - 20, ancho - 1, base - 5, rgb("#5f7a58"), seed=9)

    # muelle del frente
    l.rect(0, base - 6, ancho - 1, base, rgb("#8d8a84"))
    l.rect(0, base - 6, ancho - 1, base - 6, rgb("#b4b0a8"))

    for x in range(3, ancho, 9):
        l.rect(x, base - 5, x, base, rgb("#6c6a66"))

    y_f = base - 30

    # accesos fijos (izquierda y derecha)
    l.rect(0, y_f, 52, y_f + 5, oscuro)
    l.rect(0, y_f, 52, y_f, brillo)
    l.rect(ancho - 53, y_f, ancho - 1, y_f + 5, oscuro)
    l.rect(ancho - 53, y_f, ancho - 1, y_f, brillo)

    # reticulado bajo el tablero
    for x in range(0, 52, 6):
        l.linea(x, y_f + 5, x + 6, y_f + 14, oscuro)

    for x in range(ancho - 53, ancho, 6):
        l.linea(x + 6, y_f + 5, x, y_f + 14, oscuro)

    # pilas de hormigon
    for x in (40, ancho - 44):
        l.rect(x, y_f + 6, x + 6, base - 6, rgb("#c9c5bb"))
        l.rect(x + 4, y_f + 6, x + 6, base - 6, rgb("#a8a498"))

    # torres reticuladas de elevacion
    def torre(x):

        l.rect(x - 8, 8, x + 8, 14, oscuro)
        l.rect(x - 8, 8, x + 8, 8, brillo)

        for pata in (x - 8, x + 6):
            l.rect(pata, 14, pata + 2, base - 6, acero)
            l.rect(pata, 14, pata, base - 6, brillo)

        for y in range(16, base - 10, 14):

            l.linea(x - 6, y, x + 6, y + 14, oscuro)
            l.linea(x + 6, y, x - 6, y + 14, oscuro)
            l.rect(x - 6, y + 14, x + 6, y + 14, acero)

        # sala de maquinas
        l.rect(x - 11, 0, x + 11, 8, rgb("#dfe6ee"))
        l.rect(x - 11, 0, x + 11, 0, rgb("#ffffff"))
        l.rect(x - 9, 2, x - 4, 5, VIDRIO)
        l.rect(x + 4, 2, x + 9, 5, VIDRIO)

    torre(58)
    torre(ancho - 62)

    # tramo levadizo (esta levantado hasta la mitad)
    y_l = base - 78

    l.rect(66, y_l, ancho - 71, y_l + 5, rgb("#b7c8d8"))
    l.rect(66, y_l, ancho - 71, y_l, rgb("#ffffff"))
    l.rect(66, y_l + 5, ancho - 71, y_l + 5, oscuro)

    for x in range(66, ancho - 71, 8):
        l.linea(x, y_l + 5, x + 8, y_l + 14, oscuro)
        l.linea(x + 8, y_l + 5, x, y_l + 14, oscuro)

    # cables de elevacion
    for x in (72, 90):
        l.rect(x, 14, x, y_l, rgb("#2a2f38"))

    for x in (ancho - 90, ancho - 76):
        l.rect(x, 14, x, y_l, rgb("#2a2f38"))

    # contrapesos
    l.rect(52, 36, 56, 52, rgb("#8a8a86"))
    l.rect(ancho - 66, 36, ancho - 62, 52, rgb("#8a8a86"))

    # vehiculos en el tablero fijo
    l.rect(14, y_f - 8, 28, y_f - 1, rgb("#e7c22b"))
    l.rect(16, y_f - 11, 24, y_f - 8, rgb("#e7c22b"))
    l.rect(17, y_f - 10, 23, y_f - 8, VIDRIO_LUZ)

    l.rect(ancho - 38, y_f - 9, ancho - 12, y_f - 1, rgb("#2f64b8"))
    l.rect(ancho - 38, y_f - 9, ancho - 12, y_f - 9, luz(rgb("#2f64b8"), 0.3))

    # lancha en el rio
    l.poly([(110, base - 12), (150, base - 12), (146, base - 6), (114, base - 6)], rgb("#c0392b"))
    l.rect(120, base - 20, 136, base - 12, rgb("#f4f1e8"))
    l.rect(124, base - 18, 132, base - 15, VIDRIO)
    l.rect(128, base - 30, 128, base - 20, rgb("#3a3a3a"))

    return l


# ==========================================================
# TREN DEL ROCA
# ==========================================================

def tren_roca():

    ancho = 256
    alto = 86

    l = Lienzo(ancho, alto)

    base = alto - 1

    hormigon = rgb("#9a9a94")
    oscuro = rgb("#6a6a66")

    # terraplen / muro de contencion con murales
    y_v = base - 34

    l.rect(0, y_v, ancho - 1, base, hormigon)
    l.rect(0, y_v, ancho - 1, y_v, luz(hormigon, 0.35))
    l.rect(0, y_v + 1, ancho - 1, y_v + 3, oscuro)

    for x in range(0, ancho, 20):
        l.rect(x, y_v + 4, x, base, sombra(hormigon, 0.88))

    # grafitis / murales en Boca
    for i, x in enumerate(range(8, ancho - 30, 52)):

        l.rect(x, y_v + 8, x + 36, y_v + 28, AZUL_BOCA)
        l.rect(x, y_v + 15, x + 36, y_v + 20, AMARILLO_BOCA)
        l.rect(x + 14, y_v + 9, x + 22, y_v + 27, rgb("#f4f1e8") if i % 2 else rgb("#e0405a"))

    # columnas del tendido electrico (catenaria)
    for x in (40, 126, 212):

        l.rect(x, y_v - 40, x + 1, y_v, rgb("#4a4f58"))
        l.rect(x - 6, y_v - 38, x + 7, y_v - 36, rgb("#4a4f58"))

    l.rect(0, y_v - 38, ancho - 1, y_v - 38, rgb("#2a2f38"))
    l.rect(0, y_v - 34, ancho - 1, y_v - 34, rgb("#2a2f38"))

    # el tren: tres coches
    for k in range(3):

        x0 = 14 + k * 78

        carro = rgb("#e8e6df")

        l.rect(x0, y_v - 24, x0 + 74, y_v - 1, carro)
        l.rect(x0, y_v - 24, x0 + 74, y_v - 24, rgb("#ffffff"))
        l.rect(x0, y_v - 3, x0 + 74, y_v - 1, rgb("#4a4f58"))

        # franja celeste
        l.rect(x0, y_v - 12, x0 + 74, y_v - 8, rgb("#3a8fd8"))

        # ventanas
        for x in range(x0 + 4, x0 + 70, 10):

            l.rect(x, y_v - 21, x + 6, y_v - 14, VIDRIO)
            l.px(x, y_v - 21, VIDRIO_LUZ)

        # puertas
        for x in (x0 + 22, x0 + 52):
            l.rect(x, y_v - 21, x + 4, y_v - 3, rgb("#c8c6bd"))

        # ruedas / bogies
        for x in (x0 + 8, x0 + 62):
            l.rect(x, y_v, x + 8, y_v + 1, rgb("#1f1a24"))

        # pantografo en el primer y ultimo coche
        if k in (0, 2):

            l.linea(x0 + 36, y_v - 24, x0 + 28, y_v - 31, rgb("#2a2f38"))
            l.linea(x0 + 28, y_v - 31, x0 + 44, y_v - 36, rgb("#2a2f38"))

    # frente del tren con faros (a la derecha)
    l.rect(ancho - 8, y_v - 22, ancho - 4, y_v - 3, rgb("#e0944f"))
    l.rect(ancho - 7, y_v - 18, ancho - 5, y_v - 16, rgb("#fff6b0"))

    # semaforo ferroviario
    l.rect(ancho - 22, y_v - 30, ancho - 21, y_v, rgb("#2a2f38"))
    l.rect(ancho - 25, y_v - 38, ancho - 18, y_v - 30, rgb("#1a1a24"))
    l.px(ancho - 23, y_v - 36, rgb("#e0405a"))
    l.px(ancho - 23, y_v - 33, rgb("#3fd070"))

    return l


MONUMENTOS = [
    dict(id="bombonera", nombre="La Bombonera", fn=bombonera),
    dict(id="tren_roca", nombre="Tren del Ferrocarril Roca", fn=tren_roca),
    dict(id="caminito", nombre="Caminito", fn=caminito),
    dict(id="transbordador", nombre="Puente Transbordador Nicolas Avellaneda", fn=transbordador),
    dict(id="usina_del_arte", nombre="Usina del Arte", fn=usina_del_arte),
]

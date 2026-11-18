"""
Efectos de luz de los fondos: el reflejo del sol (niveles de dia) y las luces
de la noche (ventanas prendidas, postes de luz, balizas).

Todo se dibuja con pixel art sobre las capas (lo usa generar_techos.py) y,
ademas, se anota en nivel_NN_efectos.json lo que el juego anima en vivo
(fondos_nivel.py): los destellos del sol, la luz de las farolas y las luces
rojas que parpadean.

Las posiciones del json estan en pixeles de dibujo de cada capa (no del
mundo): el juego las mueve con el mismo parallax que la capa.
"""

import math

import numpy as np
from PIL import Image

from pixelart import mezcla, luz

import generar_niveles as G


# ----------------------------------------------------------
# Que sale en el json
# ----------------------------------------------------------

CAPAS_EFECTOS = ("ciudad", "medio", "lejos")


class Efectos:
    """Lo que el juego anima en vivo (posiciones en pixeles de dibujo)."""

    def __init__(self, azar):

        self.azar = azar

        self.capas = {
            c: dict(brillos=[], lamparas=[], balizas=[]) for c in CAPAS_EFECTOS
        }

        self.astro = None

    def brillo(self, capa, x, y, tam=3):
        """Destello del sol en un vidrio: titila con su propio ritmo."""

        r = self.azar

        self.capas[capa]["brillos"].append(
            [int(x), int(y), int(tam), round(r.uniform(1.8, 3.6), 2), round(r.random(), 3)]
        )

    def lampara(self, capa, x, y, radio, color, parpadea=False):
        """Luz de un poste: un resplandor que se suma a lo que hay detras."""

        r = self.azar

        self.capas[capa]["lamparas"].append(
            [int(x), int(y), int(radio), [int(c) for c in color[:3]],
             1 if parpadea else 0, round(r.random(), 3)]
        )

    def baliza(self, capa, x, y, color=(255, 60, 50), radio=6):
        """Luz de aviso (antenas, torres): prende y apaga."""

        r = self.azar

        self.capas[capa]["balizas"].append(
            [int(x), int(y), [int(c) for c in color[:3]], int(radio),
             round(r.uniform(1.4, 2.6), 2), round(r.random(), 3)]
        )

    def astro_en_cielo(self, tipo, x, y, radio, color):

        self.astro = dict(
            tipo=tipo, x=int(x), y=int(y), r=int(radio),
            color=[int(c) for c in color[:3]]
        )

    def a_dict(self):

        return dict(astro=self.astro, capas=self.capas)


# ----------------------------------------------------------
# Ventanas (vidrios) de una capa
# ----------------------------------------------------------

class Ventanas:
    """Los vidrios de una capa, uno por uno (cada ventana es una etiqueta)."""

    def __init__(self, l):

        a = np.array(l.im)

        mask = np.zeros(a.shape[:2], bool)

        for c in G.VIDRIOS:

            mask |= np.all(a[..., :3] == np.array(c), axis=-1) & (a[..., 3] > 0)

        self.mask = mask

        self.lab, self.n = G.etiquetar_ventanas(mask)

        n = self.n

        ys, xs = np.nonzero(self.lab)

        ids = self.lab[ys, xs]

        self.x0 = np.full(n + 1, 1 << 30, np.int64)
        self.y0 = np.full(n + 1, 1 << 30, np.int64)
        self.x1 = np.full(n + 1, -1, np.int64)
        self.y1 = np.full(n + 1, -1, np.int64)

        np.minimum.at(self.x0, ids, xs)
        np.minimum.at(self.y0, ids, ys)
        np.maximum.at(self.x1, ids, xs)
        np.maximum.at(self.y1, ids, ys)

    def caja(self, i):

        return int(self.x0[i]), int(self.y0[i]), int(self.x1[i]), int(self.y1[i])


def _guardar(l, a):

    l.im = Image.fromarray(a, "RGBA")

    from PIL import ImageDraw

    l.d = ImageDraw.Draw(l.im)


# ==========================================================
# DIA: REFLEJO DEL SOL
# ==========================================================

SOL_BLANCO = (255, 250, 226)


def lado_del_sol(cfg):
    """
    De que lado le pega el sol a los edificios ("der" o "izq"): el sol se ve
    en la mitad derecha de la pantalla si esta lejos del principio del
    cielo y en la izquierda si esta cerca. Sale de la configuracion.
    """

    if "sol_lado" in cfg:

        return cfg["sol_lado"]

    sx = cfg.get("sol", (0, 0, 0, ""))[0]

    return "der" if sx > 520 else "izq"


def reflejos_en_ventanas(l, prob, azar, color_cielo, lado, ef=None, capa="ciudad",
                         max_brillos=0, ventanas=None):
    """
    Vidrios que reflejan el sol: franjas diagonales de cielo y de luz, y algunos
    ventanales que dan directo al sol y brillan casi blancos. De los que
    brillan salen los destellos que titilan en el juego.
    """

    v = ventanas or Ventanas(l)

    if v.n == 0:

        return

    a = np.array(l.im)

    cielo_reflejado = np.array(mezcla(color_cielo, (255, 255, 255), 0.5), np.float32)

    blanco = np.array(SOL_BLANCO, np.float32)

    # "/" si el sol viene de la derecha, "\" si viene de la izquierda
    giro = 1 if lado == "der" else -1

    candidatos = []

    for i in range(1, v.n + 1):

        if azar.random() >= prob:

            continue

        x0, y0, x1, y1 = v.caja(i)

        sub = v.lab[y0:y1 + 1, x0:x1 + 1] == i

        yy, xx = np.nonzero(sub)

        if len(yy) < 4:

            continue

        pix = a[y0 + yy, x0 + xx, :3].astype(np.float32)

        directo = azar.random() < 0.20

        if directo:

            out = pix * 0.16 + blanco * 0.84

            # el borde de abajo, un poco menos brillante (marco del vidrio)
            candidatos.append((x1 if lado == "der" else x0, y0))

        else:

            t = (xx + giro * yy + azar.randint(0, 5)) % 6

            reflejo = pix * 0.45 + cielo_reflejado * 0.55

            out = np.where((t <= 1)[:, None], pix * 0.10 + blanco * 0.90, reflejo)

            out = np.where((t == 2)[:, None], pix * 0.50 + blanco * 0.50, out)

        a[y0 + yy, x0 + xx, :3] = np.clip(out, 0, 255).astype(np.uint8)

    _guardar(l, a)

    if ef is not None and max_brillos:

        azar.shuffle(candidatos)

        for x, y in candidatos[:max_brillos]:

            ef.brillo(capa, x, y, 3)


def brillo_de_calle(capa, azar, ef, filas, ancho, color_sol=SOL_BLANCO):
    """
    El sol en la calle: rayitas claras sobre el asfalto (como si estuviera
    recien lavado), baldosas que brillan y algunos destellos.
    filas = (fila_fachada, fila_calle, alto)
    """

    fila_fachada, fila_calle, alto = filas

    im = capa.im

    # asfalto
    for _ in range(ancho // 20):

        x = azar.randrange(ancho - 14)

        y = azar.randint(fila_calle + 8, alto - 5)

        largo = azar.randint(4, 11)

        for dx in range(largo):

            actual = im.getpixel((x + dx, y))[:3]

            capa.px(x + dx, y, mezcla(actual, color_sol, 0.34 if dx not in (0, largo - 1) else 0.18))

    # baldosas de la vereda y el cordon
    for _ in range(ancho // 16):

        x = azar.randrange(ancho)

        y = azar.randint(fila_fachada + 3, fila_calle + 1)

        actual = im.getpixel((x, y))[:3]

        capa.px(x, y, luz(actual, 0.28))

    if ef is not None:

        for _ in range(40):

            x = azar.randrange(30, ancho - 30)

            y = azar.choice((fila_calle + 3, azar.randint(fila_calle + 9, alto - 8)))

            ef.brillo("ciudad", x, y, 2)


def luz_de_borde(l, color, t, lado):
    """
    El sol de costado: el borde de arriba de cada silueta (y el que da al sol)
    se aclara con el color de la luz.
    """

    a = np.array(l.im)

    op = a[..., 3] > 0

    arriba = np.zeros_like(op)
    arriba[0] = op[0]
    arriba[1:] = op[1:] & ~op[:-1]

    lateral = np.zeros_like(op)

    if lado == "der":

        lateral[:, -1] = op[:, -1]
        lateral[:, :-1] = op[:, :-1] & ~op[:, 1:]

    else:

        lateral[:, 0] = op[:, 0]
        lateral[:, 1:] = op[:, 1:] & ~op[:, :-1]

    for m, k in ((arriba, t), (lateral, t * 0.7)):

        c = np.array(color, np.float32)

        a[m, :3] = np.clip(a[m, :3].astype(np.float32) * (1 - k) + c * k, 0, 255).astype(np.uint8)

    _guardar(l, a)


def rayos_de_sol(l, cx, cy, color, largo, cantidad, azar):
    """Rayos finos que salen del sol (transparentes, en tres escalones)."""

    ov = Image.new("RGBA", l.im.size, (0, 0, 0, 0))

    from PIL import ImageDraw

    d = ImageDraw.Draw(ov)

    base = azar.uniform(0, math.pi)

    for k in range(cantidad):

        ang = base + 2 * math.pi * k / cantidad

        ancho = 0.045 if k % 2 == 0 else 0.028

        largo_k = largo * (1.0 if k % 2 == 0 else 0.7)

        for esc, alfa in ((1.0, 20), (0.68, 20), (0.36, 24)):

            p1 = (cx + math.cos(ang - ancho) * largo_k * esc, cy + math.sin(ang - ancho) * largo_k * esc)
            p2 = (cx + math.cos(ang + ancho) * largo_k * esc, cy + math.sin(ang + ancho) * largo_k * esc)

            d.polygon([(cx, cy), p1, p2], fill=tuple(color[:3]) + (alfa,))

    l.im.alpha_composite(ov)

    l.d = ImageDraw.Draw(l.im)


# ==========================================================
# NOCHE: VENTANAS PRENDIDAS
# ==========================================================

AMARILLO = (255, 224, 128)
CLARO = (255, 240, 176)
NARANJA = (255, 186, 96)
BLANCO_FRIO = (214, 236, 255)
TELE = (140, 184, 255)
ROSA = (255, 120, 200)
CELESTE = (90, 230, 255)
VIOLETA = (190, 150, 255)

# (color, peso) de las luces de las ventanas segun el barrio
PALETAS_LUCES = {
    "calida": [(AMARILLO, 60), (CLARO, 12), (NARANJA, 20), (BLANCO_FRIO, 4), (TELE, 4)],
    "fria": [(CLARO, 26), (BLANCO_FRIO, 34), (AMARILLO, 18), (TELE, 14), (NARANJA, 8)],
    "neon": [(AMARILLO, 52), (ROSA, 10), (CELESTE, 10), (NARANJA, 16), (VIOLETA, 12)],
    "sodio": [(NARANJA, 44), (AMARILLO, 34), (CLARO, 12), (TELE, 10)],
}


def elegir_ventanas(l, prob, azar):
    """
    Que ventanas se prenden (antes de teñir la capa: los vidrios se buscan por
    su color). Devuelve las ventanas y un arreglo de bool por etiqueta.
    """

    v = Ventanas(l)

    prender = np.zeros(v.n + 1, bool)

    for i in range(1, v.n + 1):

        prender[i] = azar.random() < prob

    return v, prender


def _color_pesos(opciones, azar):

    total = sum(p for _, p in opciones)

    t = azar.uniform(0, total)

    for c, p in opciones:

        t -= p

        if t <= 0:

            return c

    return opciones[0][0]


def prender_ventanas(l, v, prender, azar, paleta="calida", brillo=0.22):
    """
    Pinta de luz las ventanas elegidas (cada una con su color), con un reflejo
    arriba y un resplandor de un pixel alrededor.
    """

    opciones = PALETAS_LUCES[paleta]

    colores = np.zeros((v.n + 1, 3), np.uint8)

    for i in range(1, v.n + 1):

        if prender[i]:

            colores[i] = _color_pesos(opciones, azar)

    a = np.array(l.im)

    pix = prender[v.lab] & v.mask

    if not pix.any():

        return

    lab = np.where(pix, v.lab, 0)

    # resplandor alrededor (solo donde hay dibujo y no es otra ventana prendida)
    ya = pix.copy()

    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):

        vecino = np.zeros_like(lab)

        ys = slice(max(0, dy), lab.shape[0] + min(0, dy))
        yd = slice(max(0, -dy), lab.shape[0] + min(0, -dy))
        xs = slice(max(0, dx), lab.shape[1] + min(0, dx))
        xd = slice(max(0, -dx), lab.shape[1] + min(0, -dx))

        vecino[yd, xd] = lab[ys, xs]

        nuevo = (vecino > 0) & ~ya & (a[..., 3] > 0)

        c = colores[vecino[nuevo]].astype(np.float32)

        a[nuevo, :3] = np.clip(a[nuevo, :3].astype(np.float32) * (1 - brillo) + c * brillo, 0, 255).astype(np.uint8)

        ya |= nuevo

    # los vidrios prendidos
    a[pix, :3] = colores[v.lab[pix]]

    # un brillo en el borde de arriba de cada ventana
    sup = np.zeros_like(pix)
    sup[1:] = pix[1:] & ~pix[:-1]

    alto = colores[v.lab[sup]].astype(np.float32)

    a[sup, :3] = np.clip(alto * 0.5 + 255 * 0.5, 0, 255).astype(np.uint8)

    _guardar(l, a)


# ==========================================================
# NOCHE: POSTES DE LUZ
# ==========================================================

def _componer(l, img, x, y):
    """Pega una imagen RGBA (arreglo) en (x, y), recortando lo que se sale."""

    x = int(x)
    y = int(y)

    im = Image.fromarray(img, "RGBA")

    sx0 = max(0, -x)
    sy0 = max(0, -y)
    sx1 = min(im.width, l.w - x)
    sy1 = min(im.height, l.h - y)

    if sx1 > sx0 and sy1 > sy0:

        l.im.alpha_composite(im.crop((sx0, sy0, sx1, sy1)), (x + sx0, y + sy0))

        from PIL import ImageDraw

        l.d = ImageDraw.Draw(l.im)


def cono_de_luz(l, cx, y_cabeza, y_suelo, ancho_suelo, color, alfa):
    """La luz que cae de la lampara: un cono que se abre hacia el suelo."""

    alto = int(y_suelo - y_cabeza)

    ancho = int(ancho_suelo)

    if alto < 4:

        return

    yy, xx = np.mgrid[0:alto + 1, 0:ancho + 1]

    mitad = ancho / 2.0

    abierto = mitad * (yy / float(alto)) + 1.5

    dist = np.abs(xx - mitad)

    dentro = dist <= abierto

    a = alfa * (1.0 - 0.60 * yy / alto) * (1.0 - 0.55 * (dist / abierto) ** 2)

    a = np.where(dentro, a, 0)

    a = (np.round(a / 7.0) * 7.0).astype(np.uint8)

    img = np.zeros((alto + 1, ancho + 1, 4), np.uint8)

    img[..., 0], img[..., 1], img[..., 2] = color

    img[..., 3] = a

    _componer(l, img, cx - ancho // 2, y_cabeza)


def charco_de_luz(l, cx, cy, rx, ry, color, alfa):
    """Mancha de luz en el piso (una elipse que se apaga hacia los bordes)."""

    yy, xx = np.mgrid[-ry:ry + 1, -rx:rx + 1]

    d = np.sqrt((xx / float(rx)) ** 2 + (yy / float(ry)) ** 2)

    a = np.clip(1.0 - d, 0, 1) ** 1.2 * alfa

    a = (np.round(a / 7.0) * 7.0).astype(np.uint8)

    img = np.zeros((2 * ry + 1, 2 * rx + 1, 4), np.uint8)

    img[..., 0], img[..., 1], img[..., 2] = color

    img[..., 3] = a

    _componer(l, img, cx - rx, cy - ry)


def reflejo_en_asfalto(l, cx, y0, largo, color, alfa):
    """La luz del poste reflejada en el asfalto: una columna que se va apagando."""

    for k in range(largo):

        a = int(alfa * (1 - k / float(largo)) ** 1.4)

        a = (a // 7) * 7

        if a <= 0:

            continue

        ancho = 1 if k < largo * 0.5 else 2

        img = np.zeros((1, ancho * 2 + 1, 4), np.uint8)

        img[..., 0], img[..., 1], img[..., 2] = color

        img[0, :, 3] = a

        img[0, 0, 3] = a // 2

        img[0, -1, 3] = a // 2

        _componer(l, img, cx - ancho, y0 + k)


def antena_con_baliza(l, x, y, ef, capa, color=(255, 70, 60)):
    """Una luz roja en la punta de una antena (se apaga y prende en el juego)."""

    l.px(x, y, color)

    if ef is not None:

        ef.baliza(capa, x, y, color, 5)


def luminaria_azotea(l, x, y_base, alto, color_luz, ef, capa):
    """Poste de luz chico en un techo (como las luminarias de las terrazas)."""

    poste = (44, 50, 58)

    l.rect(x, y_base - alto, x, y_base, poste)

    l.rect(x - 1, y_base - 1, x + 1, y_base, poste)

    l.rect(x - 2, y_base - alto - 2, x + 2, y_base - alto - 1, mezcla(color_luz, (255, 255, 255), 0.55))

    l.rect(x - 2, y_base - alto - 3, x + 2, y_base - alto - 3, poste)

    if ef is not None:

        ef.lampara(capa, x, y_base - alto - 2, 14, color_luz)


def letrero_neon(l, x, y, ancho, color, ef=None, capa="medio"):
    """Cartel luminoso (neon) con su resplandor."""

    centro = mezcla(color, (255, 255, 255), 0.55)

    l.rect(x, y, x + ancho - 1, y + 2, color)

    l.rect(x + 1, y + 1, x + ancho - 2, y + 1, centro)

    # resplandor alrededor
    alto = 3

    rad = ancho // 2 + 4

    yy, xx = np.mgrid[-5:alto + 5, -rad:ancho + rad]

    dx = np.maximum(np.maximum(-xx, xx - (ancho - 1)), 0)

    dy = np.maximum(np.maximum(-yy, yy - (alto - 1)), 0)

    d = np.sqrt(dx ** 2 + (dy * 1.6) ** 2)

    a = np.clip(1.0 - d / 6.0, 0, 1) ** 1.5 * 90

    a = (np.round(a / 10.0) * 10.0).astype(np.uint8)

    img = np.zeros(a.shape + (4,), np.uint8)

    img[..., 0], img[..., 1], img[..., 2] = color

    img[..., 3] = a

    # el letrero en si no se tapa
    img[5:5 + alto, rad:rad + ancho, 3] = 0

    _componer(l, img, x - rad, y - 5)

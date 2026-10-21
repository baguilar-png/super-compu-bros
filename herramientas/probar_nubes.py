"""
Prueba que las nubes aleatorias del cielo SIEMPRE se pueden alcanzar y que el
cielo se puede recorrer de punta a punta (se puede ganar el nivel por las
nubes).

Las nubes se generan al empezar cada nivel (Terreno.generar_nubes):

  - El piso 0 es una "autopista": nubes desde el primer techo grande hasta la
    meta, a la misma altura, con huecos al azar. Hay una sobre cada techo
    grande (por ahi se sube).
  - Arriba se apilan mas pisos: cada nube se apoya en una "padre" del piso de
    abajo con la que se solapa.

Este script simula con la fisica real del juego (gravedad, fuerza de salto,
velocidad) y comprueba tres cosas:

  1. De cada techo grande se llega a su nube de entrada (salto vertical).
  2. De cada nube de arriba se llega desde su padre (salto vertical parado en
     el solape), y entre dos nubes vecinas de la autopista se cruza el hueco
     saltando hacia la derecha.
  3. Hay una RUTA: un buscador (mejor primero) prueba saltos y caidas, con la
     fisica real y contando las nubes que atajan el salto, desde la primera
     nube de entrada hasta la meta.

Uso (desde la carpeta del juego):

    python herramientas/probar_nubes.py              # los 15 niveles, 4 semillas
    python herramientas/probar_nubes.py 3 8 12       # solo esos niveles
    python herramientas/probar_nubes.py -s 10        # 10 semillas por nivel

Las constantes de fisica de abajo tienen que coincidir con las de juego.py
(GRAVEDAD, SALTO_FUERZA, VELOCIDAD_MOV y el tamano del jugador).
"""

import argparse
import collections
import heapq
import os
import random
import statistics
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import terreno as T
from terreno import Terreno

DT = 1 / 60
GRAVEDAD = 2880
SALTO_FUERZA = -960
VELOCIDAD_MOV = 420
ANCHO_J = 32
ALTO_J = 54

# Donde esta la meta (igual que META_X de juego.py)
META_X = T.NIVEL_ANCHO - 100

# Frames que se mantiene la direccion en un salto (None = hasta caer)
HOLDS = [None, 4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 38, 46, 56]
HOLDS_RUTA = [None, 6, 10, 14, 18, 24, 30, 38, 48]


class Rapido:
    """Busca el apoyo de un jugador que cae (nubes y techos de edificios altos)."""

    def __init__(self, terreno):
        self.t = terreno
        self.cubetas = collections.defaultdict(list)
        for n in terreno.nubes:
            for c in range(int(n.x0 // 200) - 1, int(n.x1 // 200) + 2):
                self.cubetas[c].append(n)
        self.grandes = [e for e in terreno.edificios if e.tier == 2]

    def apoyo_obj(self, izq, der, bottom_antes, bottom, vel_y):
        """La nube (o techo) donde aterriza, o None si sigue en el aire."""
        if vel_y < 0:
            return None
        mejor = None
        vistos = set()
        for c in range(int(izq // 200), int(der // 200) + 1):
            for n in self.cubetas.get(c, ()):
                if id(n) in vistos:
                    continue
                vistos.add(id(n))
                if (
                    der - T.MARGEN_APOYO_BALCON > n.x0
                    and izq + T.MARGEN_APOYO_BALCON < n.x1
                    and bottom_antes <= n.y + 1
                    and bottom >= n.y
                ):
                    if mejor is None or n.y < mejor.y:
                        mejor = n
        for e in self.grandes:
            if (
                der - T.MARGEN_APOYO > e.x0
                and izq + T.MARGEN_APOYO < e.x1
                and bottom_antes <= e.y + 1
                and bottom >= e.y
            ):
                if mejor is None or e.y < mejor.y:
                    mejor = e
        return mejor

    def apoyo(self, izq, der, bottom_antes, bottom, vel_y):
        o = self.apoyo_obj(izq, der, bottom_antes, bottom, vel_y)
        return None if o is None else o.y


def simular(r, x, bottom, vel_y, d, hold):
    """
    Un salto (vel_y = SALTO_FUERZA) o una caida (vel_y = 0) desde el
    rectangulo con el borde izquierdo en x y los pies en `bottom`. `d` es la
    direccion (-1, 0, 1) y `hold` los frames que se mantiene (None = hasta
    caer). Devuelve (objeto_donde_aterriza, x) o None.
    """
    y = bottom - ALTO_J
    rx = x
    for f in range(170):
        bottom_antes = y + ALTO_J
        if hold is None or f < hold:
            rx = int(rx + d * VELOCIDAD_MOV * DT)
        vel_y += GRAVEDAD * DT
        y = int(y + vel_y * DT)
        ap = r.apoyo_obj(rx, rx + ANCHO_J, bottom_antes, y + ALTO_J, vel_y)
        if ap is not None:
            return ap, rx
        if y + ALTO_J > 900:
            return None
    return None


def salto(r, x, bottom, d, hold):
    """Como `simular` con un salto; devuelve (y_apoyo, x) o None."""
    res = simular(r, x, bottom, SALTO_FUERZA, d, hold)
    return None if res is None else (res[0].y, res[1])


# ----------------------------------------------------------
# 1 y 2: de donde se llega a cada nube
# ----------------------------------------------------------

def salto_lateral_ok(r, a, b):
    """Hay algun salto parado en la nube `a` que aterriza en la nube `b`?"""
    d = 1 if b.centro > a.centro else -1
    xs = list(range(int(a.x0 - 26) + 1, int(a.x1 - 6), 2))
    if d > 0:
        xs.reverse()
    for hold in HOLDS:
        for x in xs:
            res = salto(r, x, a.y, d, hold)
            if res and res[0] == b.y and b.x0 <= res[1] + ANCHO_J / 2 < b.x1:
                return True
    return False


def probar(n, semilla):
    """Devuelve (terreno, pruebas hechas, lista de problemas)."""
    t = Terreno.cargar(n)
    t.generar_nubes(random.Random(semilla * 977 + n))
    r = Rapido(t)
    malas = []
    total = 0

    # el piso 0 llega hasta la meta, sin huecos imposibles (se cruzan hacia
    # la derecha, que es hacia donde se gana)
    p0 = sorted((c for c in t.nubes if c.piso == 0), key=lambda c: c.x0)
    if not p0:
        malas.append("sin nubes en el piso 0")
        return t, total, malas
    if p0[-1].x1 < META_X + 40:
        malas.append(("la autopista no llega a la meta", round(p0[-1].x1)))

    for a, b in zip(p0, p0[1:]):
        total += 1
        hueco = b.x0 - a.x1
        if not T.NUBE_HUECO_MIN - 1e-6 <= hueco <= T.NUBE_HUECO_MAX + 1e-6:
            malas.append(("hueco fuera de rango", round(a.x1), round(hueco)))
        if not salto_lateral_ok(r, a, b):
            malas.append(("no se cruza el hueco", round(a.x1), round(hueco)))

    for h in t.nubes:
        p = h.padre
        if p is None:
            malas.append((round(h.x0), round(h.y), "sin padre"))
            continue
        if isinstance(p, T.Nube) and p.piso == h.piso:
            continue   # relleno de la autopista: ya probado arriba
        ov0 = max(h.x0, p.x0)
        ov1 = min(h.x1, p.x1)
        # un salto vertical con el jugador entero dentro del solape: algun
        # punto del solape tiene que llevar a la nube hija
        for izq in range(int(ov0) + 1, int(ov1) - ANCHO_J, 6):
            total += 1
            res = salto(r, izq, p.y, 0, 0)
            if not res or res[0] != h.y or not (h.x0 <= res[1] + 16 < h.x1):
                malas.append((round(h.x0), round(h.y), h.piso, izq, res))
                break
    return t, total, malas


# ----------------------------------------------------------
# 3: una ruta de punta a punta, con la fisica real
# ----------------------------------------------------------

def movimientos(r, c, robusto=True):
    """
    Todos los saltos y caidas que se pueden hacer desde la nube `c`, a otra
    nube. Devuelve {id(destino): (destino, x_salida, direccion, frames, tipo)}
    (uno por destino). Con `robusto` el movimiento tiene que dar el mismo
    resultado saliendo 3 px a cada lado (un jugador no clava el pixel).
    """
    res = {}

    def intentar(x, bottom, vel_y, d, hold, tipo):
        sal = simular(r, x, bottom, vel_y, d, hold)
        if sal is None or not isinstance(sal[0], T.Nube) or sal[0] is c:
            return
        dest, rx = sal
        if id(dest) in res:
            return
        if robusto:
            for dx in (-3, 3):
                o = simular(r, x + dx, bottom, vel_y, d, hold)
                if o is None or o[0] is not dest:
                    return
        res[id(dest)] = (dest, x, d, hold, tipo)

    xs = list(range(int(c.x0 - 26) + 4, int(c.x1 - 6) - 3, 14))

    for x in xs:
        for d in (1, -1):
            for hold in HOLDS_RUTA:
                intentar(x, c.y, SALTO_FUERZA, d, hold, "salto")
        intentar(x, c.y, SALTO_FUERZA, 0, 0, "salto")

    # caerse por un borde caminando (queda en el aire sin tocar nada abajo)
    intentar(int(c.x1 - 6), c.y, 0, 1, None, "caida")
    intentar(int(c.x0 - 26), c.y, 0, -1, None, "caida")
    intentar(int(c.x1 - 6), c.y, 0, 0, 0, "caida")
    intentar(int(c.x0 - 26), c.y, 0, 0, 0, "caida")

    return res


def ruta_cielo(t, desde=None, robusto=True, r=None, cache=None):
    """
    Busca (mejor primero, siempre hacia la derecha) un camino de nube en nube
    desde `desde` (por defecto la primera nube del piso 0) hasta una nube que
    llegue a la meta. Devuelve (camino, expandidas) con camino = lista de
    (nube_origen, x_salida, direccion, frames, tipo, nube_destino), o
    (None, expandidas) si no hay.
    """
    r = r or Rapido(t)
    cache = {} if cache is None else cache
    if desde is None:
        desde = min((c for c in t.nubes if c.piso == 0), key=lambda c: c.x0)

    def llega(c):
        return c.x1 > META_X + 10

    orden = 0
    cola = [(-desde.centro, orden, desde)]
    vino = {id(desde): None}
    expandidas = 0

    while cola:
        _, _, c = heapq.heappop(cola)
        if llega(c):
            camino = []
            k = id(c)
            while vino[k] is not None:
                prev, paso = vino[k]
                camino.append((prev, paso[1], paso[2], paso[3], paso[4], paso[0]))
                k = id(prev)
            camino.reverse()
            return camino, expandidas
        expandidas += 1
        if id(c) not in cache:
            cache[id(c)] = movimientos(r, c, robusto)
        for k, paso in cache[id(c)].items():
            if k in vino:
                continue
            vino[k] = (c, paso)
            orden += 1
            heapq.heappush(cola, (-paso[0].centro, orden, paso[0]))
    return None, expandidas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("niveles", nargs="*", type=int, help="niveles a probar (por defecto los 15)")
    ap.add_argument("-s", "--semillas", type=int, default=4, help="semillas por nivel (por defecto 4)")
    args = ap.parse_args()

    niveles = args.niveles or list(range(1, 16))
    t0 = time.time()
    cantidades = []
    fallas = 0
    for n in niveles:
        for semilla in range(args.semillas):
            t, total, malas = probar(n, semilla)
            cantidades.append(len(t.nubes))
            pisos = max(c.piso for c in t.nubes) + 1
            camino, expandidas = ruta_cielo(t)
            if camino is None:
                malas.append("no hay ruta hasta la meta")
            fallas += len(malas)
            print(
                "nivel %2d semilla %d: %3d nubes, %2d pisos, %4d pruebas, ruta de %2d saltos (%3d nubes vistas), %d malas %s (%.0fs)"
                % (n, semilla, len(t.nubes), pisos, total, len(camino or []), expandidas, len(malas), malas[:2], time.time() - t0),
                flush=True,
            )
    print("nubes por nivel: min %d, mediana %d, max %d" % (min(cantidades), statistics.median(cantidades), max(cantidades)))
    print("TODAS ALCANZABLES Y HAY RUTA HASTA LA META" if fallas == 0 else "HAY PROBLEMAS: %d" % fallas)
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())

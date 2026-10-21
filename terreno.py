"""
Terreno de los niveles: tres pisos apilados a lo largo de todo el nivel.

  - LA CALLE (abajo de todo, y = CALLE_Y): ahi arranca el nivel y estan los
    enemigos mas flojos. La calle esta libre de punta a punta (se puede ganar
    el nivel caminando por ella). Hay escaleras de mano (ESCALERAS) en los
    edificios chicos para subir a los techos.
  - LOS TECHOS (en el medio): el personaje camina sobre los techos de una fila
    de edificios pegados unos a otros. Hay edificios chicos, medianos y
    grandes (tres alturas de techo), asi que a veces hay que subir o bajar:

      * Un techo que esta a menos de un salto (SALTO_ESCALON) sobre el que
        pisas se alcanza saltando.
      * Los edificios grandes que quedan mas de un salto arriba de su vecino
        tienen BALCONES pegados a la pared (plataformas de un solo sentido:
        se entra desde abajo y se pisa desde arriba) que sirven de escalones.
      * Bajar es facil: se camina hasta el borde y se cae al techo de al lado.
      * Las paredes de los edificios son solidas de costado, pero solo para
        el que esta en el piso de los techos: en la calle los edificios son
        el fondo, se pasa por adelante.

  - EL CIELO (arriba): NUBES, plataformas de un solo sentido que se generan al
    azar cada vez que empieza el nivel (generar_nubes), siempre de modo que se
    pueda llegar a todas saltando. Se sube desde los techos grandes. Cuanto mas
    alto, mas oscuro el cielo. Si te caes de una nube caes al techo (o a la
    calle) que haya abajo.

El dibujo (assets/niveles/nivel_NN_ciudad.png) y los datos de colision
(assets/niveles/nivel_NN_terreno.json) los genera juntos
herramientas/generar_techos.py, asi nunca se desacomodan.

Todas las medidas son en pixeles del mundo (el nivel mide 9600 de ancho y la
ventana 800 x 600; la camara tambien se mueve para arriba y para abajo).
Este archivo no necesita pygame: recibe rectangulos de pygame (o cualquier
cosa con .x, .width y .bottom).
"""

import json
import os

CARPETA = os.path.dirname(os.path.abspath(__file__))

CARPETA_NIVELES = os.path.join(CARPETA, "assets", "niveles")

NIVEL_ANCHO = 9600

# Pixeles de pantalla por pixel de dibujo
PX = 3

# ----------------------------------------------------------
# ALTURAS
# ----------------------------------------------------------

# y de pantalla de la superficie de cada altura de techo: chico, mediano y
# grande. Cada escalon mide 108 (36 pixeles de dibujo).
TECHOS = (480, 372, 264)

# Lo mas alto que se llega saltando son 160 px. Con esto queda margen.
SALTO_ESCALON = 111

# Balcones (plataformas pegadas a la pared de un edificio grande)
ANCHO_BALCON = 108
GROSOR_BALCON = 12

# ----------------------------------------------------------
# LOS TRES PISOS
# ----------------------------------------------------------

# y de la calle (3 escalones de 108 abajo del techo de los edificios chicos)
CALLE_Y = 804

# Plano de los techos: si los pies estan mas abajo que esto (con margen) se
# esta en la calle o en una escalera, y las paredes de los edificios no
# frenan (son el fondo). Desde los techos grandes hacia arriba esta el cielo.
LIMITE_PLANO = TECHOS[0] + 2

# Escaleras de mano: de la calle al techo de un edificio chico
ANCHO_ESCALERA = 36
AGARRE_ESCALERA = 22          # a que distancia del centro se las agarra
VELOCIDAD_ESCALERA = 230      # px por segundo al trepar

# Nubes
NUBE_ANCHOS = (108, 144, 180)
NUBE_Y0 = 156                 # primer piso: un escalon sobre los techos grandes
NUBE_PISOS = 17
NUBE_PASO = (88, 100)         # distancia entre pisos: menos que un salto (160),
                              # pero dos pisos juntos son mas que un salto, asi
                              # un salto nunca "se pasa" a la nube de arriba
NUBE_JITTER = 4               # cuanto se desvia cada nube de la altura del piso
NUBE_SOLAPE = 64              # cuanto tiene que tapar una nube a la de abajo
                              # (el jugador mide 32: entra parado en el solape)
NUBE_SEPARACION = 40          # hueco minimo entre dos nubes del mismo piso
NUBE_PROB_SEGUNDA = 0.45      # chance de que una nube tenga dos nubes encima
NUBE_MARGEN = 30

# La "autopista": el primer piso de nubes cubre todo el ancho del nivel, con
# huecos al azar entre HUECO_MIN y HUECO_MAX (un salto cruza hasta ~290)
NUBE_HUECO_MIN = NUBE_SEPARACION
NUBE_HUECO_MAX = 150
NUBE_ANCHO_MIN = 70           # lo mas angosta que puede quedar una nube

# Anchos de las nubes de relleno de la autopista (mas anchas = mas lugar para
# nubes encima)
NUBE_ANCHOS_AUTOPISTA = (108, 144, 144, 180, 180)

# Zona de aterrizaje de cada nube de la autopista: desde NUBE_ATERRIZAJE_ANTES
# antes de su borde izquierdo hasta NUBE_ATERRIZAJE_DESPUES despues. Ninguna
# nube del piso 1 tapa esa zona, porque el piso 1 esta a menos de un salto
# (160) de la autopista y atajaria el salto: el jugador no podria caer sobre la
# nube. Asi de cada nube de la autopista siempre se cruza a la siguiente.
NUBE_ATERRIZAJE_ANTES = 40
NUBE_ATERRIZAJE_DESPUES = 70

# ----------------------------------------------------------
# FISICA
# ----------------------------------------------------------

# Si los pies estan a esta distancia (o menos) por debajo del techo se
# considera que esta parado encima, no contra la pared
TOLERANCIA_PARED = 2

# Cuanto tiene que quedar apoyado el rectangulo del jugador sobre un techo
# (a cada lado) para no caerse
MARGEN_APOYO = 8
MARGEN_APOYO_BALCON = 6

# Margen que se deja a los costados del techo para poner enemigos e items
MARGEN_BORDE = 30

# Tramo del techo, justo despues de subir de uno mas bajo, donde no se pone
# ningun enemigo (ahi aterriza el jugador)
ZONA_ATERRIZAJE = 170

# Tramo antes de una pared mas alta (el jugador se frena y salta ahi)
ZONA_SALTO = 100

# Items: lugar que se les deja al borde del techo y distancia minima entre
# dos items del mismo techo
MARGEN_ITEM = 40
ESPACIO_ITEMS = 90

# Tramo del techo, a cada lado de una escalera, donde no se pone nada
ZONA_ESCALERA = 90

# Calle: donde no se ponen enemigos (antes de la primera escalera arranca el
# jugador), y cuanto se deja libre alrededor de las escaleras
CALLE_INICIO_LIBRE = 520
CALLE_LIBRE_ESCALERA = 130
CALLE_FIN_LIBRE = 420


class Edificio:
    """Un edificio: x0..x1 es su ancho y `y` la superficie de su techo."""

    __slots__ = ("x0", "x1", "y", "tier", "estilo", "indice")

    def __init__(self, x0, x1, y, tier, estilo, indice):

        self.x0 = x0
        self.x1 = x1
        self.y = y
        self.tier = tier
        self.estilo = estilo
        self.indice = indice

    @property
    def ancho(self):

        return self.x1 - self.x0

    @property
    def centro(self):

        return (self.x0 + self.x1) / 2


class Balcon:
    """
    Plataforma de un solo sentido pegada a la pared de un edificio grande.
    `lado` es "izq" o "der": de que lado del edificio sale. `y` es la
    superficie donde se pisa.
    """

    __slots__ = ("x0", "x1", "y", "lado", "edificio")

    def __init__(self, x0, x1, y, lado, edificio):

        self.x0 = x0
        self.x1 = x1
        self.y = y
        self.lado = lado
        self.edificio = edificio


class Escalera:
    """
    Escalera de mano pegada a la fachada de un edificio chico: va de la
    calle (CALLE_Y) hasta su techo (`y_alto`). `x` es el centro.
    """

    __slots__ = ("x", "y_alto", "y_bajo", "edificio")

    def __init__(self, x, y_alto, edificio, y_bajo=CALLE_Y):

        self.x = x
        self.y_alto = y_alto
        self.y_bajo = y_bajo
        self.edificio = edificio

    @property
    def x0(self):

        return self.x - ANCHO_ESCALERA // 2

    @property
    def x1(self):

        return self.x + ANCHO_ESCALERA // 2


class Nube:
    """
    Plataforma de un solo sentido en el cielo: x0..x1 es donde se pisa y `y`
    la superficie. `piso` es el nivel de altura (0 = el mas bajo).
    """

    __slots__ = ("x0", "x1", "y", "piso", "padre")

    def __init__(self, x0, x1, y, piso=0, padre=None):

        self.x0 = x0
        self.x1 = x1
        self.y = y
        self.piso = piso

        # De donde se llega a esta nube (otra Nube, o el Edificio de abajo en
        # el primer piso). Sirve para probar que se puede llegar.
        self.padre = padre

    @property
    def ancho(self):

        return self.x1 - self.x0

    @property
    def centro(self):

        return (self.x0 + self.x1) / 2


class Terreno:

    def __init__(
        self,
        edificios,
        balcones,
        nivel=0,
        escaleras=None
    ):

        self.nivel = nivel

        self.edificios = edificios

        self.balcones = balcones

        self.escaleras = escaleras or []

        # Se llenan con generar_nubes() al empezar el nivel
        self.nubes = []

        self.calle_y = CALLE_Y

    # ------------------------------------------------------
    # CARGA
    # ------------------------------------------------------

    @classmethod
    def desde_dict(cls, datos):

        edificios = [
            Edificio(e["x0"], e["x1"], e["y"], e["tier"], e["estilo"], i)
            for i, e in enumerate(datos["edificios"])
        ]

        balcones = [
            Balcon(b["x0"], b["x1"], b["y"], b["lado"], b["edificio"])
            for b in datos.get("balcones", [])
        ]

        escaleras = [
            Escalera(e["x"], e["y"], e["edificio"])
            for e in datos.get("escaleras", [])
        ]

        return cls(
            edificios,
            balcones,
            datos.get("nivel", 0),
            escaleras
        )

    @classmethod
    def plano(cls, nivel=0):
        """Un solo techo largo (como el piso de antes). Sirve de reserva."""

        return cls(
            [Edificio(0, NIVEL_ANCHO, TECHOS[0], 0, "casa_baja", 0)],
            [],
            nivel
        )

    @classmethod
    def cargar(cls, nivel):
        """
        Lee assets/niveles/nivel_NN_terreno.json. Si falta o esta roto
        devuelve un terreno plano, asi el juego nunca se rompe.
        """

        # El mapa da la vuelta: el nivel 16 usa el terreno del 1, etc.
        numero = ((max(1, int(nivel)) - 1) % 15) + 1

        ruta = os.path.join(
            CARPETA_NIVELES,
            "nivel_{:02d}_terreno.json".format(numero)
        )

        try:

            with open(ruta, "r", encoding="utf-8") as f:

                return cls.desde_dict(json.load(f))

        except (OSError, ValueError, KeyError, TypeError):

            return cls.plano(nivel)

    # ------------------------------------------------------
    # CONSULTAS
    # ------------------------------------------------------

    def edificio_en(self, x):
        """El edificio que esta en la columna x (el ultimo si se pasa)."""

        for e in self.edificios:

            if e.x0 <= x < e.x1:

                return e

        return self.edificios[-1] if x >= 0 else self.edificios[0]

    def techo_en(self, x):
        """y de la superficie del techo en la columna x."""

        return self.edificio_en(x).y

    @staticmethod
    def zona(y):
        """
        En que piso esta algo cuyos pies (o cuyo piso de apoyo) estan en y:
        "calle", "techos" o "cielo".
        """

        if y > LIMITE_PLANO:

            return "calle"

        if y < TECHOS[2] - 20:

            return "cielo"

        return "techos"

    def escalera_cerca(self, x):
        """La escalera que se puede agarrar parado en la columna x, o None."""

        for esc in self.escaleras:

            if abs(x - esc.x) <= AGARRE_ESCALERA:

                return esc

        return None

    def nube_en(self, x, y_ref):
        """La nube mas alta bajo y_ref en la columna x, o None."""

        mejor = None

        for n in self.nubes:

            if n.x0 <= x < n.x1 and n.y >= y_ref - 1:

                if mejor is None or n.y < mejor.y:

                    mejor = n

        return mejor

    def superficie_bajo(self, x, y_ref, margen=1):
        """
        y de la primera superficie (techo, balcon, nube o calle) que hay en la
        columna x a la altura y_ref o mas abajo. None si no hay ninguna. La
        calle solo cuenta para lo que ya esta en el piso de la calle (los
        techos son macizos hasta ahi, y de adentro no se cae).
        """

        mejor = None

        for e in self.edificios:

            if e.x0 <= x < e.x1 and e.y >= y_ref - margen:

                if mejor is None or e.y < mejor:

                    mejor = e.y

        for b in self.balcones:

            if b.x0 <= x < b.x1 and b.y >= y_ref - margen:

                if mejor is None or b.y < mejor:

                    mejor = b.y

        for n in self.nubes:

            if n.x0 <= x < n.x1 and n.y >= y_ref - margen:

                if mejor is None or n.y < mejor:

                    mejor = n.y

        if mejor is None and y_ref >= LIMITE_PLANO - margen:

            mejor = self.calle_y if y_ref <= self.calle_y + margen else None

        return mejor

    def dentro_de_edificio(self, x, y):
        """
        True si el punto esta metido adentro del cuerpo de un edificio, en el
        piso de los techos (en la calle los edificios son el fondo).
        """

        e = self.edificio_en(x)

        return e.y < y <= LIMITE_PLANO

    def techo_minimo(self, x_a, x_b):
        """
        y del techo mas alto (el numero mas chico) de todos los edificios
        que hay entre x_a y x_b. Sirve para saber por donde puede pasar algo
        que vuela de un lado al otro.
        """

        izq, der = (x_a, x_b) if x_a <= x_b else (x_b, x_a)

        return min(
            (e.y for e in self.edificios if e.x1 > izq and e.x0 < der),
            default=TECHOS[0]
        )

    def choca_pared(self, rect, tolerancia=4):
        """
        True si el rectangulo (de algo que vuela: pelota, botella) se metio
        en el cuerpo de un edificio (si esta en el piso de los techos), o sea
        que lo frena la pared. En la calle no hay paredes.
        """

        if rect.bottom <= LIMITE_PLANO:

            for e in self.edificios:

                if rect.right > e.x0 and rect.x < e.x1:

                    if rect.bottom > e.y + tolerancia:

                        return True

        return False

    # ------------------------------------------------------
    # FISICA
    # ------------------------------------------------------

    @staticmethod
    def _empujar(x, ancho, x_antes, x0, x1, centro):
        """Saca el rectangulo [x, x + ancho] de la pared [x0, x1]."""

        if x_antes + ancho <= x0 + 1:

            # venia por la izquierda
            return x0 - ancho

        if x_antes >= x1 - 1:

            # venia por la derecha
            return x1

        # ya estaba adentro (no deberia pasar): afuera por el lado mas cercano
        if x + ancho / 2 < centro:

            return x0 - ancho

        return x1

    def resolver_x(self, rect, x_antes):
        """
        Las paredes son solidas. Devuelve la x donde queda el rectangulo
        despues de moverse horizontalmente (x_antes era donde estaba).

        Los edificios frenan solo en el piso de los techos; en la calle no hay
        nada que frene (se camina de punta a punta).
        """

        x = rect.x

        ancho = rect.width

        if rect.bottom <= LIMITE_PLANO:

            for e in self.edificios:

                # Parado encima del techo (o saltando por arriba): no choca
                if rect.bottom <= e.y + TOLERANCIA_PARED:

                    continue

                if x + ancho > e.x0 and x < e.x1:

                    x = self._empujar(x, ancho, x_antes, e.x0, e.x1, e.centro)

        return x

    def apoyo(self, izq, der, bottom_antes, bottom, vel_y):
        """
        y del techo, balcon, nube o calle donde aterriza un rectangulo que se
        movio verticalmente, o None si sigue en el aire.

        izq y der son los bordes del rectangulo; bottom_antes y bottom, la
        parte de abajo antes y despues de moverse. Solo se aterriza cayendo
        (o parado) y desde arriba.
        """

        if vel_y < 0:

            return None

        mejor = None

        for e in self.edificios:

            if (
                der - MARGEN_APOYO > e.x0
                and izq + MARGEN_APOYO < e.x1
                and bottom_antes <= e.y + 1
                and bottom >= e.y
            ):

                if mejor is None or e.y < mejor:

                    mejor = e.y

        for b in self.balcones:

            if (
                der - MARGEN_APOYO_BALCON > b.x0
                and izq + MARGEN_APOYO_BALCON < b.x1
                and bottom_antes <= b.y + 1
                and bottom >= b.y
            ):

                if mejor is None or b.y < mejor:

                    mejor = b.y

        for n in self.nubes:

            if (
                der - MARGEN_APOYO_BALCON > n.x0
                and izq + MARGEN_APOYO_BALCON < n.x1
                and bottom_antes <= n.y + 1
                and bottom >= n.y
            ):

                if mejor is None or n.y < mejor:

                    mejor = n.y

        # La calle: abajo de todo y en todo el ancho del nivel
        if mejor is None and bottom_antes <= self.calle_y + 1 and bottom >= self.calle_y:

            mejor = self.calle_y

        return mejor

    # ------------------------------------------------------
    # CIELO: NUBES AL AZAR (siempre se puede llegar)
    # ------------------------------------------------------

    def generar_nubes(self, rng, pisos=NUBE_PISOS):
        """
        Arma las nubes del nivel con el generador `rng` (random.Random). Es
        distinto cada vez que empieza el nivel, pero siempre se puede llegar
        a todas las nubes:

          - El primer piso es una AUTOPISTA: una fila de nubes desde el primer
            techo grande hasta el borde derecho del nivel (hasta la meta), con
            huecos al azar que se cruzan de un salto. Se sube a ella desde
            cualquier techo grande, porque hay una nube un escalon (108) arriba
            de cada uno, tapando al menos NUBE_SOLAPE del techo. Asi el cielo
            se puede recorrer entero y ganar el nivel sin bajar.
          - Las nubes del piso 1 (a menos de un salto de la autopista) no
            tapan la zona de aterrizaje de las nubes de la autopista, para
            que nunca atajen el salto de una a la otra.
          - Cada nube de un piso de arriba se apoya en una "padre" del piso
            de abajo: queda a menos de un salto de altura y tapa al menos
            NUBE_SOLAPE de ella. Parado en esa parte comun, un salto casi
            vertical aterriza en la hija.
          - Entre dos pisos hay mas de la mitad de un salto: el pico del salto
            desde una nube nunca llega al piso de arriba de la hija, asi que
            ninguna otra nube intercepta ese salto.

        Algunas nubes no tienen ninguna encima (cadenas que terminan) y otras
        tienen dos (el camino se bifurca). herramientas/probar_nubes.py prueba
        con la fisica real que de cada padre se llega a sus hijas.
        """

        nubes = []

        entradas = []

        for e in self.edificios:

            if e.tier != 2:

                continue

            ancho = rng.choice(NUBE_ANCHOS)

            margen = min(70, max(20, (e.ancho - 60) / 2))

            centro = rng.uniform(e.x0 + margen, e.x1 - margen)

            x0 = max(NUBE_MARGEN, centro - ancho / 2)

            x1 = min(NIVEL_ANCHO - NUBE_MARGEN, x0 + ancho)

            entradas.append(Nube(x0, x1, NUBE_Y0, 0, e))

        piso0 = self._autopista(rng, entradas)

        nubes.extend(piso0)

        # Lugares del piso 1 donde no puede haber nubes (ver NUBE_ATERRIZAJE_*)
        zonas = [
            (n.x0 - NUBE_ATERRIZAJE_ANTES, n.x0 + NUBE_ATERRIZAJE_DESPUES)
            for n in piso0
        ]

        anterior = piso0

        # Maximo de nubes por piso de arriba (que el cielo no se llene de
        # nubes): parejo con la cantidad de edificios grandes
        tope = max(12, len(entradas) * 2)

        y_base = NUBE_Y0

        for piso in range(1, pisos):

            y_base -= rng.randint(*NUBE_PASO)

            actual = []

            padres = list(anterior)

            rng.shuffle(padres)

            for padre in padres:

                hijas = 1

                if rng.random() < NUBE_PROB_SEGUNDA:

                    hijas = 2

                for _ in range(hijas):

                    if len(actual) >= tope:

                        break

                    hija = self._nube_sobre(
                        rng, padre, piso, y_base, actual,
                        intentos=40 if piso == 1 else 14,
                        prohibidas=zonas if piso == 1 else ()
                    )

                    if hija is not None:

                        actual.append(hija)

            # Si ninguna entro, se fuerza una sobre una nube de abajo (para
            # que el cielo no se corte)
            if not actual:

                for padre in padres:

                    hija = self._nube_sobre(
                        rng, padre, piso, y_base, actual, 60,
                        prohibidas=zonas if piso == 1 else ()
                    )

                    if hija is not None:

                        actual.append(hija)

                        break

            if not actual:

                break

            actual.sort(key=lambda n: n.x0)

            nubes.extend(actual)

            anterior = actual

        self.nubes = nubes

        return nubes

    def _autopista(self, rng, entradas):
        """
        El piso 0 de nubes: las `entradas` (una sobre cada techo grande, por
        donde se sube) unidas por nubes de relleno, desde la primera entrada
        hasta el borde derecho del nivel (la meta). Entre dos nubes vecinas
        queda un hueco al azar de
        NUBE_HUECO_MIN a NUBE_HUECO_MAX (siempre saltable). Todas quedan a la
        misma altura (NUBE_Y0), asi que de cada una se llega a la siguiente
        con un salto hacia el costado. `padre` de una de relleno es la
        vecina de la izquierda, de la que se llega a ella.
        Devuelve la lista ordenada de izquierda a derecha.
        """

        limite_izq = NUBE_MARGEN

        limite_der = NIVEL_ANCHO - NUBE_MARGEN

        # 1) las entradas, sin pisarse (si dos quedan muy cerca se corre la
        # de la derecha, o se saca si ya no tapa su techo)
        ruta = []

        for e in sorted(entradas, key=lambda n: n.x0):

            if ruta and e.x0 < ruta[-1].x1 + NUBE_HUECO_MIN:

                e.x0 = ruta[-1].x1 + NUBE_HUECO_MIN

                techo = e.padre

                if (
                    e.x1 - e.x0 < NUBE_ANCHO_MIN
                    or min(e.x1, techo.x1) - max(e.x0, techo.x0) < NUBE_SOLAPE
                ):

                    continue

            ruta.append(e)

        if not ruta:

            return []

        # 2) relleno entre cada par de entradas
        completa = [ruta[0]]

        for sig in ruta[1:]:

            ant = completa[-1]

            cursor = ant.x1

            while sig.x0 - cursor > NUBE_HUECO_MAX:

                restante = sig.x0 - cursor

                hueco = rng.uniform(NUBE_HUECO_MIN, NUBE_HUECO_MAX)

                ancho = rng.choice(NUBE_ANCHOS_AUTOPISTA)

                # lo que sobra despues de esta nube tiene que ser un hueco
                # valido (si no, se achica la nube)
                if restante - hueco - ancho < NUBE_HUECO_MIN:

                    ancho = restante - hueco - NUBE_HUECO_MIN

                    if ancho < NUBE_ANCHO_MIN:

                        hueco = NUBE_HUECO_MIN

                        ancho = restante - 2 * NUBE_HUECO_MIN

                x0 = cursor + hueco

                completa.append(Nube(x0, x0 + ancho, NUBE_Y0, 0, completa[-1]))

                cursor = x0 + ancho

            completa.append(sig)

        # 3) hacia la derecha de la ultima entrada, hasta el borde (la meta
        # esta casi al final del nivel)
        cursor = completa[-1].x1

        while limite_der - cursor > 0:

            restante = limite_der - cursor

            if restante < NUBE_HUECO_MIN + NUBE_ANCHO_MIN:

                # no entra otra nube: se alarga la ultima hasta el borde
                completa[-1].x1 = limite_der

                break

            hueco = rng.uniform(NUBE_HUECO_MIN, min(NUBE_HUECO_MAX, restante - NUBE_ANCHO_MIN))

            ancho = rng.choice(NUBE_ANCHOS_AUTOPISTA)

            x0 = cursor + hueco

            x1 = x0 + ancho

            # la nube que llegaria a menos de un hueco del borde llega al borde
            if limite_der - x1 < NUBE_HUECO_MIN + NUBE_ANCHO_MIN:

                x1 = limite_der

            completa.append(Nube(x0, x1, NUBE_Y0, 0, completa[-1]))

            cursor = x1

        completa.sort(key=lambda n: n.x0)

        return completa

    @staticmethod
    def _hueco(a, b):
        """Hueco horizontal (borde a borde) entre dos nubes; 0 si se tocan."""

        return max(0.0, max(a.x0, b.x0) - min(a.x1, b.x1))

    def _nube_sobre(self, rng, padre, piso, y_base, actual, intentos=14, prohibidas=()):
        """
        Una nube nueva del piso `piso` apoyada en `padre`: tapa al menos
        NUBE_SOLAPE de ella y deja NUBE_SEPARACION de hueco con las otras
        nubes del piso (`actual`). No se mete en ninguno de los tramos
        (x_desde, x_hasta) de `prohibidas`. None si no se pudo acomodar.
        """

        for _ in range(intentos):

            ancho = rng.choice(NUBE_ANCHOS)

            desde = padre.x0 - ancho + NUBE_SOLAPE

            hasta = padre.x1 - NUBE_SOLAPE

            if hasta < desde:

                continue

            # Tramos de x0 posibles, sin las zonas prohibidas
            tramos = [(desde, hasta)]

            for a_, b_ in prohibidas:

                nuevos = []

                for lo, hi in tramos:

                    if hi <= a_ - ancho or lo >= b_:

                        nuevos.append((lo, hi))

                        continue

                    if lo < a_ - ancho:

                        nuevos.append((lo, a_ - ancho))

                    if hi > b_:

                        nuevos.append((b_, hi))

                tramos = nuevos

            tramos = [(lo, hi) for lo, hi in tramos if hi >= lo]

            if not tramos:

                continue

            lo, hi = rng.choices(
                tramos, weights=[max(1.0, h - l) for l, h in tramos]
            )[0]

            x0 = rng.uniform(lo, hi)

            x0 = max(NUBE_MARGEN, min(NIVEL_ANCHO - NUBE_MARGEN - ancho, x0))

            x1 = x0 + ancho

            if min(x1, padre.x1) - max(x0, padre.x0) < NUBE_SOLAPE:

                continue

            if any(
                x0 < o.x1 + NUBE_SEPARACION and x1 > o.x0 - NUBE_SEPARACION
                for o in actual
            ):

                continue

            if any(x0 < b and x1 > a for a, b in prohibidas):

                continue

            y = y_base + rng.randint(-NUBE_JITTER, NUBE_JITTER)

            return Nube(x0, x1, y, piso, padre)

        return None

    # ------------------------------------------------------
    # DONDE PONER COSAS (items y enemigos)
    # ------------------------------------------------------

    def zona_libre(self, edificio):
        """
        (x_min, x_max) del techo donde se pueden poner enemigos e items: se
        dejan afuera los bordes, los balcones de los edificios de al lado y
        dos tramos para que el jugador no caiga o salte justo encima de un
        enemigo:

          - despues de subir (si el vecino de la izquierda es mas bajo),
            donde se aterriza al subir;
          - antes de la pared que hay que saltar (si el vecino de la derecha
            es mas alto).
        """

        x0 = edificio.x0 + MARGEN_BORDE

        x1 = edificio.x1 - MARGEN_BORDE

        i = edificio.indice

        if i > 0 and self.edificios[i - 1].y > edificio.y:

            x0 = edificio.x0 + ZONA_ATERRIZAJE

        if i + 1 < len(self.edificios) and self.edificios[i + 1].y < edificio.y:

            x1 = edificio.x1 - ZONA_SALTO

        for b in self.balcones:

            if b.edificio == edificio.indice:

                continue

            if b.x1 > edificio.x0 and b.x0 < edificio.x1:

                if b.lado == "izq":

                    x1 = min(x1, b.x0 - 6)

                else:

                    x0 = max(x0, b.x1 + 6)

        # La escalera que sale a este techo: se deja libre un tramo de cada
        # lado y se usa el lado que queda mas ancho
        for esc in self.escaleras:

            if esc.edificio != edificio.indice:

                continue

            izq = (x0, min(x1, esc.x - ZONA_ESCALERA))

            der = (max(x0, esc.x + ZONA_ESCALERA), x1)

            x0, x1 = izq if izq[1] - izq[0] >= der[1] - der[0] else der

        return x0, x1

    def _elegibles(self, ancho_necesario, reservados=None):
        """
        Lugares donde entra algo de `ancho_necesario` de ancho: una lista de
        (edificio, x_min, x_max) con los tramos libres de cada techo (menos
        el primero y el ultimo). `reservados` es {indice de edificio: (x0, x1)}
        con lo que ya ocupa otra cosa (un hincha, por ejemplo).
        """

        reservados = reservados or {}

        resultado = []

        for e in self.edificios[1:-1]:

            a, b = self.zona_libre(e)

            tramos = [(a, b)]

            if e.indice in reservados:

                r0, r1 = reservados[e.indice]

                tramos = [(a, min(b, r0)), (max(a, r1), b)]

            for ta, tb in tramos:

                if tb - ta >= ancho_necesario:

                    resultado.append((e, ta, tb))

        return resultado

    def posiciones_lanzadores(
        self,
        objetivos,
        rango_max,
        ancho_hitbox,
        ancho_doble=520
    ):
        """
        Para cada x objetivo busca el techo con lugar mas cercano y devuelve
        [(x_centro, y_techo, indice_edificio, (x_desde, x_hasta), rango)].

        El hincha patrulla `rango` para cada lado (hasta `rango_max`, menos si
        el techo es angosto). En un techo ancho (`ancho_doble` o mas de zona
        libre) entran dos hinchas, cada uno de su lado. `(x_desde, x_hasta)`
        es lo que ocupa.
        """

        minimo = ancho_hitbox + 70

        capacidad = {}

        zonas = {}

        for e in self.edificios[1:-1]:

            a, b = self.zona_libre(e)

            if b - a >= minimo:

                zonas[e.indice] = (e, a, b)

                capacidad[e.indice] = 2 if b - a >= ancho_doble else 1

        puestos = {}

        resultado = []

        for objetivo in objetivos:

            candidatos = [
                zonas[k] for k in zonas
                if len(puestos.get(k, [])) < capacidad[k]
            ]

            if not candidatos:

                break

            e, a, b = min(
                candidatos,
                key=lambda c: (
                    abs(c[0].centro - objetivo)
                    + 400 * len(puestos.get(c[0].indice, []))
                )
            )

            usados = puestos.setdefault(e.indice, [])

            usados.append(objetivo)

            if capacidad[e.indice] == 1:

                desde, hasta = a, b

            else:

                mitad = (b - a) / 2

                # el primero va del lado izquierdo, el segundo del derecho
                if len(usados) == 1:
                    desde, hasta = a, a + mitad
                else:
                    desde, hasta = a + mitad, b

            rango = max(0, min(rango_max, (hasta - desde - ancho_hitbox) / 2 - 12))

            resultado.append((
                (desde + hasta) / 2, e.y, e.indice, (desde, hasta), rango
            ))

        return resultado

    def posiciones_gagambas(
        self,
        maximo,
        ancho_enemigo,
        reservados=None,
        ancho_necesario=210,
        ancho_doble=440
    ):
        """
        Hasta `maximo` gagambas repartidos parejo a lo largo del nivel (en
        los tramos que no usan los `reservados`). Un gagamba por techo; si no
        alcanzan los techos, en los mas anchos (`ancho_doble` o mas) caminan
        dos, uno de cada lado.

        Devuelve [(x_inicial, y_techo, rango)]: x_inicial es el costado
        izquierdo del gagamba y `rango` cuanto camina para cada lado.
        """

        # un solo tramo por techo: el mas ancho
        mejores = {}

        for e, a, b in self._elegibles(ancho_necesario, reservados):

            if e.indice not in mejores or b - a > mejores[e.indice][2] - mejores[e.indice][1]:

                mejores[e.indice] = (e, a, b)

        simples = [mejores[k] for k in sorted(mejores)]

        lugares = []

        for e, a, b in simples:

            lugares.append((e, (a + b) / 2, min(60, (b - a - ancho_enemigo) / 2)))

        # si faltan, se agrega un segundo en los techos anchos
        if len(lugares) < maximo:

            for e, a, b in simples:

                if b - a >= ancho_doble and len(lugares) < maximo:

                    cuarto = (b - a) / 4

                    # el que ya estaba pasa a la izquierda y se suma uno a la derecha
                    for k, (e2, centro, rango) in enumerate(lugares):

                        if e2 is e:

                            lugares[k] = (e, a + cuarto, min(60, cuarto - ancho_enemigo / 2 - 6))

                    lugares.append((e, b - cuarto, min(60, cuarto - ancho_enemigo / 2 - 6)))

        lugares.sort(key=lambda l: l[1])

        if len(lugares) > maximo:

            paso = len(lugares) / maximo

            lugares = [lugares[int(i * paso)] for i in range(maximo)]

        return [
            (centro - ancho_enemigo / 2, e.y, max(0, rango))
            for e, centro, rango in lugares
        ]

    def posiciones_items(self, plantilla):
        """
        `plantilla` es la lista de siempre [(tipo, x, altura)] (21 items,
        7 por tercio). Cada uno se corre al techo libre mas cercano a su lugar
        de siempre, con la misma altura (los de arriba siguen obligando a
        saltar). Si caen varios en el mismo techo se reparten parejo, a no
        menos de ESPACIO_ITEMS uno del otro.

        Devuelve [(tipo, x, altura, y_techo)] en el mismo orden.
        """

        techos = []

        for e in self.edificios:

            a, b = self.zona_libre(e)

            a += MARGEN_ITEM

            b -= MARGEN_ITEM

            if b < a:

                continue

            capacidad = int((b - a) // ESPACIO_ITEMS) + 1

            techos.append([e, a, b, capacidad, []])

        for indice, (tipo, x, altura) in enumerate(plantilla):

            libres = [t for t in techos if len(t[4]) < t[3]]

            t = min(
                libres,
                key=lambda t: abs(x - max(t[1], min(t[2], x)))
            )

            t[4].append((x, indice))

        resultado = [None] * len(plantilla)

        for e, a, b, _, lista in techos:

            lista.sort()

            n = len(lista)

            for k, (x, indice) in enumerate(lista):

                if n == 1:

                    px = max(a, min(b, x))

                else:

                    px = a + (b - a) * k / (n - 1)

                tipo, _, altura = plantilla[indice]

                resultado[indice] = (tipo, int(px), altura, e.y)

        return resultado

    # ------------------------------------------------------
    # CALLE: enemigos y bebidas
    # ------------------------------------------------------

    def tramos_calle(self, desde=CALLE_INICIO_LIBRE, hasta=None):
        """
        Tramos de la calle donde se pueden poner cosas: sin el arranque, sin
        el final, y sin el alrededor de las escaleras. Devuelve
        [(x0, x1)] ordenados.
        """

        hasta = NIVEL_ANCHO - CALLE_FIN_LIBRE if hasta is None else hasta

        prohibidos = []

        for esc in self.escaleras:

            prohibidos.append((esc.x - CALLE_LIBRE_ESCALERA, esc.x + CALLE_LIBRE_ESCALERA))

        prohibidos.sort()

        tramos = []

        x = desde

        for a, b in prohibidos:

            if a > x:

                tramos.append((x, min(a, hasta)))

            x = max(x, b)

        if x < hasta:

            tramos.append((x, hasta))

        return [(a, b) for a, b in tramos if b > a]

    def _repartir_en_tramos(self, cantidad, tramos, ancho_min, reservados=None):
        """
        `cantidad` lugares repartidos parejo a lo largo de los tramos
        (cada uno con al menos `ancho_min` de ancho). Devuelve
        [(x_desde, x_hasta)]: lo que ocupa cada uno.
        """

        utiles = [(a, b) for a, b in tramos if b - a >= ancho_min]

        total = sum(b - a for a, b in utiles)

        if not utiles or cantidad <= 0:

            return []

        lugares = []

        for i in range(cantidad):

            objetivo = (i + 0.5) * total / cantidad

            acumulado = 0

            for a, b in utiles:

                if objetivo <= acumulado + (b - a):

                    centro = a + (objetivo - acumulado)

                    mitad = ancho_min / 2

                    centro = max(a + mitad, min(b - mitad, centro))

                    lugares.append((centro - mitad, centro + mitad))

                    break

                acumulado += b - a

        # que no se pisen (puede pasar si hay pocos tramos): se saltea el que pisa
        resultado = []

        for d, h in lugares:

            if all(h <= d2 - 20 or d >= h2 + 20 for d2, h2 in resultado):

                resultado.append((d, h))

        return resultado

    def posiciones_gagambas_calle(self, maximo, ancho_enemigo, rango_max=70):
        """
        Hasta `maximo` gagambas repartidos parejo por la calle. Devuelve
        [(x_inicial, y_calle, rango)] (x_inicial es el costado izquierdo).
        """

        ancho = ancho_enemigo + 2 * rango_max

        lugares = self._repartir_en_tramos(
            maximo, self.tramos_calle(), ancho
        )

        return [
            (d + rango_max, self.calle_y, rango_max)
            for d, h in lugares
        ]

    def posiciones_lanzadores_calle(self, cantidad, ancho_hitbox, rango_max):
        """
        Hinchas en la calle: [(x_centro, y_calle, (desde, hasta), rango)].
        """

        ancho = ancho_hitbox + 2 * rango_max

        lugares = self._repartir_en_tramos(
            cantidad, self.tramos_calle(), ancho
        )

        return [
            ((d + h) / 2, self.calle_y, (d, h), rango_max)
            for d, h in lugares
        ]

    def posiciones_items_calle(self, tipos):
        """
        Bebidas sobre la calle, repartidas parejo. `tipos` es la lista de
        [(tipo, altura)]. Devuelve [(tipo, x, altura, y_calle)] (x entero).
        """

        lugares = self._repartir_en_tramos(
            len(tipos), self.tramos_calle(CALLE_INICIO_LIBRE - 200), ESPACIO_ITEMS
        )

        return [
            (tipo, int((d + h) / 2), altura, self.calle_y)
            for (tipo, altura), (d, h) in zip(tipos, lugares)
        ]

    def posiciones_items_cielo(self, rng, tipos):
        """
        Bebidas sobre las nubes de mas arriba, una por cada tramo del nivel
        (en lugares distintos de cada vez). `tipos` es [(tipo, altura)].
        Devuelve [(indice, tipo, x, altura, y_nube)]: `indice` es el lugar
        en `tipos` (no cambia aunque las nubes sean distintas cada vez).
        """

        if not self.nubes or not tipos:

            return []

        pisos = max(n.piso for n in self.nubes)

        altas = [n for n in self.nubes if n.piso >= max(1, pisos // 2)]

        cantidad = len(tipos)

        resultado = []

        usadas = set()

        for i, (tipo, altura) in enumerate(tipos):

            a = i * NIVEL_ANCHO / cantidad

            b = (i + 1) * NIVEL_ANCHO / cantidad

            sector = [n for n in altas if a <= n.centro < b and id(n) not in usadas]

            if not sector:

                sector = [n for n in self.nubes if a <= n.centro < b and id(n) not in usadas]

            # Sin nubes en ese tramo del nivel: las mas cercanas que queden
            if not sector:

                centro = (a + b) / 2

                libres = [n for n in altas if id(n) not in usadas] or [
                    n for n in self.nubes if id(n) not in usadas
                ]

                libres.sort(key=lambda n: abs(n.centro - centro))

                sector = libres[:3]

            if not sector:

                continue

            # las mas altas del sector
            sector.sort(key=lambda n: n.y)

            n = rng.choice(sector[: max(1, len(sector) // 3)])

            usadas.add(id(n))

            resultado.append((i, tipo, int(n.centro), altura, n.y))

        return resultado

    def _ancho_libre(self, e):

        a, b = self.zona_libre(e)

        return b - a

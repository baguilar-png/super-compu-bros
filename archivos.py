"""
Persistencia de datos del juego (todo en archivos .txt al lado del juego).

    puntos.txt      -> puntos acumulados (un numero)
    personajes.txt  -> nombre del personaje elegido
    bebidas.txt     -> una bebida por linea, las que ya se recogieron
                       (asi no se pueden farmear puntos ni vidas)
    nivel.txt       -> progreso en los mapas (niveles 1 a 15 en Buenos Aires
                       y 16 a 30 en el conurbano): niveles completados,
                       donde esta parado el personaje y por que puntitos
                       del camino ya paso (los negros)
    tienda.txt      -> existe si ya se entro a la tienda de San Telmo
                       (sirve para sacar los signos de exclamacion)
    mision.txt      -> existe si ya se entro a la mision de San Telmo
    mision_completa.txt -> existe si ya se termino la mision de Iki (el
                       recuerdo de Bolivar): su cara no aparece mas en el
                       mapa. Se borra al perder y al dar la vuelta
                       (sirve para sacar los signos de exclamacion)
    vidas_extra.txt -> vidas compradas en la tienda que todavia no se
                       usaron (se suman a las 3 de cada nivel)
    ajustes.txt     -> volumen de la musica y de los efectos (0 a 100).
                       NO se borra nunca: es una preferencia, no progreso
    historia.txt    -> existe si ya se vio la escena de la historia (la que
                       aparece al empezar la partida). Se borra al perder
                       todas las vidas: se vuelve a ver
    escena_dilolio.txt -> existe si ya se vio la presentacion de Di Lolio
                       (antes del nivel 5). Se borra al perder
    historicos.txt  -> existe si ya se termino la mision de Carlitos: los
                       personajes historicos estan desbloqueados (no se
                       borra al perder)
    carlitos.txt    -> que paso con Carlitos, el perro: 1 = un Compu Bro
                       lo encontro (llamada despues del nivel 8) y esta en
                       el mapa; 2 = ya fue el reencuentro y se escapo.
                       Es progreso: se borra al perder y al dar la vuelta

PARTIDAS: hay 6 casillas. Todos los archivos de progreso de arriba (todos
menos ajustes.txt) van en la carpeta de cada partida:

    partidas/partida_1/ ... partidas/partida_6/
        partida.txt  -> nombre de la partida y la contrasena (guardada
                        "picada" con sha256, no se ve a simple vista)
        vistas.txt   -> cinematicas ya vistas en esta partida (una por
                        linea). Se borra al perder todas las vidas: las
                        cinematicas se vuelven a ver en su momento
    ultima_partida.txt (en la carpeta del juego) -> la ultima que se jugo

usar_partida(n) elige la casilla: desde ahi todas las funciones de este
archivo leen y escriben en la carpeta de esa partida.

Todo sobrevive a: ESC, cerrar la ventana y cerrar el programa.
Todo se borra junto SOLO cuando el jugador pierde todas las vidas
(ver reiniciar_progreso).
"""

import hashlib
import os
import shutil

CARPETA = os.path.dirname(os.path.abspath(__file__))

# Los ajustes son del juego (no de una partida)
RUTA_AJUSTES = os.path.join(CARPETA, "ajustes.txt")

# ----------------------------------------------------------
# PARTIDAS (6 casillas)
# ----------------------------------------------------------

CANTIDAD_PARTIDAS = 6

CARPETA_PARTIDAS = os.path.join(CARPETA, "partidas")

RUTA_ULTIMA_PARTIDA = os.path.join(CARPETA, "ultima_partida.txt")

# Archivos de progreso (cada partida tiene los suyos)
ARCHIVOS_PARTIDA = {
    "RUTA_PUNTOS": "puntos.txt",
    "RUTA_PERSONAJE": "personajes.txt",
    "RUTA_BEBIDAS": "bebidas.txt",
    "RUTA_NIVEL": "nivel.txt",
    "RUTA_TIENDA": "tienda.txt",
    "RUTA_MISION": "mision.txt",
    "RUTA_MISION_COMPLETA": "mision_completa.txt",
    "RUTA_VIDAS_EXTRA": "vidas_extra.txt",
    "RUTA_HISTORIA": "historia.txt",
    "RUTA_ESCENA_DILOLIO": "escena_dilolio.txt",
    "RUTA_CARLITOS": "carlitos.txt",
    "RUTA_VISTAS": "vistas.txt",
    "RUTA_HISTORICOS": "historicos.txt",
}

# Partida en uso (1 a 6), o None si todavia no se eligio ninguna
partida_actual = None


def carpeta_partida(numero):
    return os.path.join(CARPETA_PARTIDAS, "partida_%d" % int(numero))


def _poner_rutas(carpeta):
    for variable, archivo in ARCHIVOS_PARTIDA.items():
        globals()[variable] = os.path.join(carpeta, archivo)


def usar_partida(numero):
    """Desde ahora todo se lee y se guarda en la partida 'numero'."""

    global partida_actual

    partida_actual = int(numero)
    os.makedirs(carpeta_partida(numero), exist_ok=True)
    _poner_rutas(carpeta_partida(numero))
    _escribir(RUTA_ULTIMA_PARTIDA, "%d\n" % partida_actual)


# Sin partida elegida las rutas apuntan a una carpeta que no existe
# (no se lee nada y nada se guarda hasta elegir una)
_poner_rutas(os.path.join(CARPETA_PARTIDAS, "_sin_partida"))

# Estados de Carlitos (carlitos.txt)
CARLITOS_PERDIDO = 0        # todavia nadie lo encontro
CARLITOS_ENCONTRADO = 1     # esta en el mapa esperando el reencuentro
CARLITOS_ESCAPO = 2         # ya fue el reencuentro: se escapo otra vez

# Cantidad de niveles del juego. Son dos mapas de 15 niveles cada uno:
#   niveles 1 a 15   Buenos Aires (del Instituto Huergo a La Bombonera)
#   niveles 16 a 30  el conurbano (de Moron a Burzaco)
NIVELES_POR_MAPA = 15

TOTAL_NIVELES = 30

# Los ultimos niveles de cada mapa son peleas contra un jefe (por ahora son
# arenas vacias: sin enemigos ni items)
NIVELES_JEFE = (15, 30)


def es_jefe(nivel):
    """True si el nivel es una pelea de jefe (el 15 y el 30)."""

    return int(nivel) in NIVELES_JEFE


# El nivel 1 transcurre adentro del Instituto Huergo: es mas corto que los
# demas, tiene un solo piso (no se puede subir a ningun techo) y no tiene
# enemigos
NIVELES_INTERIOR = (1,)


def es_interior(nivel):
    """True si el nivel pasa adentro de un edificio (el 1, el Huergo)."""

    return int(nivel) in NIVELES_INTERIOR


def mapa_del_nivel(nivel):
    """Que mapa le toca a un nivel: 0 (niveles 1 a 15) o 1 (niveles 16 a 30)."""

    return (max(1, int(nivel)) - 1) // NIVELES_POR_MAPA


# ==========================================================
# AYUDAS
# ==========================================================

def _leer(ruta):
    """Texto del archivo, o None si no existe / no se puede leer."""

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read()

    except OSError:
        return None


def _escribir(ruta, texto):

    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(texto)

    except OSError:
        pass


def _borrar(ruta):

    try:
        os.remove(ruta)

    except OSError:
        pass


# ==========================================================
# PUNTOS
# ==========================================================

def cargar_puntos():
    """Puntos guardados (0 si no hay archivo o esta roto)."""

    texto = _leer(RUTA_PUNTOS)

    try:
        return max(0, int(texto.strip()))

    except (AttributeError, ValueError):
        return 0


def guardar_puntos(puntos):

    _escribir(RUTA_PUNTOS, str(int(puntos)) + "\n")


# ==========================================================
# PERSONAJE ELEGIDO
# ==========================================================

def cargar_personaje():
    """Nombre del personaje guardado, o None si hay que elegir."""

    texto = _leer(RUTA_PERSONAJE)

    if texto is None:
        return None

    nombre = texto.strip()

    return nombre or None


def guardar_personaje(nombre):

    _escribir(RUTA_PERSONAJE, str(nombre) + "\n")


# ==========================================================
# BEBIDAS YA RECOGIDAS
# ==========================================================

def cargar_bebidas():
    """Conjunto con los ids de las bebidas ya recogidas."""

    texto = _leer(RUTA_BEBIDAS)

    if texto is None:
        return set()

    return {linea.strip() for linea in texto.splitlines() if linea.strip()}


def guardar_bebida(id_bebida):
    """Agrega una bebida al txt (se guarda en el momento de recogerla)."""

    bebidas = cargar_bebidas()

    bebidas.add(id_bebida)

    _escribir(RUTA_BEBIDAS, "\n".join(sorted(bebidas)) + "\n")


# ==========================================================
# PROGRESO EN EL MAPA
# ==========================================================

def cargar_mapa():
    """
    (niveles_completados, x, y, tocados) guardados.

    x, y     -> donde quedo parado el personaje en el mapa (coordenadas de
                la imagen original); None si todavia no hay posicion
    tocados  -> puntitos del camino actual por los que ya paso (negros)
    Si no hay archivo (o esta roto) se empieza de cero.
    """

    texto = _leer(RUTA_NIVEL)

    try:
        lineas = texto.splitlines()

        completados, x, y = lineas[0].split()[:3]

        completados = max(0, min(TOTAL_NIVELES, int(completados)))

        x = None if x == "-" else float(x)
        y = None if y == "-" else float(y)

        tocados = []

        if len(lineas) > 1:

            tocados = [
                int(n) for n in lineas[1].split(",") if n.strip()
            ]

        return completados, x, y, tocados

    except (AttributeError, IndexError, ValueError):
        return 0, None, None, []


def guardar_mapa(completados, x, y, tocados):

    _escribir(
        RUTA_NIVEL,
        "%d %s %s\n%s\n" % (
            completados,
            "-" if x is None else "%.1f" % x,
            "-" if y is None else "%.1f" % y,
            ",".join(str(n) for n in sorted(tocados))
        )
    )


def completar_nivel(nivel):
    """
    Se llego a la meta del nivel (1 a 30). Se suma a los completados, el
    personaje queda donde estaba y el camino al siguiente arranca limpio.
    """

    completados, x, y, _ = cargar_mapa()

    if nivel > completados:

        guardar_mapa(min(nivel, TOTAL_NIVELES), x, y, [])


def tienda_visitada():
    """True si ya se entro alguna vez a la tienda de San Telmo."""

    return _leer(RUTA_TIENDA) is not None


def marcar_tienda_visitada():

    _escribir(RUTA_TIENDA, "1\n")


def mision_visitada():
    """True si ya se entro alguna vez a la mision de San Telmo."""

    return _leer(RUTA_MISION) is not None


def marcar_mision_visitada():

    _escribir(RUTA_MISION, "1\n")


def mision_completada():
    """True si ya se termino la mision de Iki (no aparece mas en el mapa)."""

    return _leer(RUTA_MISION_COMPLETA) is not None


def marcar_mision_completada():

    _escribir(RUTA_MISION_COMPLETA, "1\n")


def historia_vista():
    """True si ya se vio la escena de la historia (IKI y el princesito)."""

    return _leer(RUTA_HISTORIA) is not None


def marcar_historia_vista():

    _escribir(RUTA_HISTORIA, "1\n")


def escena_dilolio_vista():
    """True si ya se vio la presentacion de Di Lolio (antes del nivel 6)."""

    return _leer(RUTA_ESCENA_DILOLIO) is not None


def marcar_escena_dilolio_vista():

    _escribir(RUTA_ESCENA_DILOLIO, "1\n")


def escena_vista(nombre):
    """True si en esta partida ya se vio la cinematica 'nombre'."""

    texto = _leer(RUTA_VISTAS) or ""
    return nombre in {linea.strip() for linea in texto.splitlines()}


def marcar_escena_vista(nombre):

    if partida_actual is None or escena_vista(nombre):
        return
    texto = _leer(RUTA_VISTAS) or ""
    _escribir(RUTA_VISTAS, texto + nombre + "\n")


def cargar_carlitos():
    """Estado de Carlitos (CARLITOS_PERDIDO, _ENCONTRADO o _ESCAPO)."""

    try:
        return int((_leer(RUTA_CARLITOS) or "0").strip())
    except ValueError:
        return CARLITOS_PERDIDO


def guardar_carlitos(estado):

    _escribir(RUTA_CARLITOS, "%d\n" % int(estado))

    # Termino la mision de Carlitos (el reencuentro): se desbloquean los
    # personajes historicos en esta partida (para siempre: no se borra al
    # perder)
    if int(estado) == CARLITOS_ESCAPO:

        _escribir(RUTA_HISTORICOS, "1\n")


def historicos_desbloqueados():
    """True si en esta partida ya se termino la mision de Carlitos."""

    return _leer(RUTA_HISTORICOS) is not None


def cargar_vidas_extra():
    """Vidas compradas en la tienda que todavia no se usaron."""

    texto = _leer(RUTA_VIDAS_EXTRA)

    try:
        return max(0, int(texto.strip()))

    except (AttributeError, ValueError):
        return 0


def guardar_vidas_extra(cantidad):

    _escribir(RUTA_VIDAS_EXTRA, str(max(0, int(cantidad))) + "\n")


def gastar_vida_extra():
    """Se perdio una vida: si quedaba una extra comprada, se usa esa."""

    cantidad = cargar_vidas_extra()

    if cantidad > 0:

        guardar_vidas_extra(cantidad - 1)


def nueva_vuelta():
    """
    Se terminaron los 30 niveles: el mapa y las bebidas se borran para
    poder volver a jugar desde el Instituto Huergo (puntos y personaje se
    conservan).
    """

    _borrar(RUTA_NIVEL)
    _borrar(RUTA_BEBIDAS)
    _borrar(RUTA_TIENDA)
    _borrar(RUTA_MISION)
    _borrar(RUTA_MISION_COMPLETA)
    _borrar(RUTA_CARLITOS)


# ==========================================================
# AJUSTES (VOLUMEN)
# ==========================================================

VOLUMEN_POR_DEFECTO = 100


def cargar_ajustes():
    """
    (volumen_musica, volumen_efectos), cada uno de 0 a 100.
    Si no hay archivo (o esta roto) los dos van al maximo.
    """

    texto = _leer(RUTA_AJUSTES)

    try:
        musica, efectos = texto.split()[:2]

        return (
            max(0, min(100, int(musica))),
            max(0, min(100, int(efectos)))
        )

    except (AttributeError, ValueError):
        return VOLUMEN_POR_DEFECTO, VOLUMEN_POR_DEFECTO


def guardar_ajustes(musica, efectos, modo_ventana=None):
    """
    Guarda los volumenes. El modo de la ventana va en el mismo archivo
    (tercer dato): si no se pasa, se conserva el que estaba.
    """

    if modo_ventana is None:

        modo_ventana = cargar_modo_ventana()

    _escribir(
        RUTA_AJUSTES,
        "%d %d %s\n" % (
            max(0, min(100, int(musica))),
            max(0, min(100, int(efectos))),
            modo_ventana
        )
    )


def cargar_modo_ventana():
    """Modo de la ventana guardado (ver ventana.py): "normal" si no hay."""

    texto = _leer(RUTA_AJUSTES)

    try:
        return texto.split()[2]

    except (AttributeError, IndexError):
        return "normal"


def guardar_modo_ventana(modo):

    musica, efectos = cargar_ajustes()

    guardar_ajustes(musica, efectos, modo)


# ==========================================================
# GAME OVER
# ==========================================================

def reiniciar_progreso():
    """
    Se pierden todas las vidas: se borran puntos, personaje y bebidas
    recogidas. La proxima partida empieza de cero y hay que elegir
    personaje de nuevo.
    """

    _borrar(RUTA_PUNTOS)
    _borrar(RUTA_PERSONAJE)
    _borrar(RUTA_BEBIDAS)
    _borrar(RUTA_NIVEL)
    _borrar(RUTA_TIENDA)
    _borrar(RUTA_MISION)
    _borrar(RUTA_MISION_COMPLETA)
    _borrar(RUTA_VIDAS_EXTRA)
    _borrar(RUTA_CARLITOS)

    # Las cinematicas se vuelven a ver (cada una en su momento)
    _borrar(RUTA_HISTORIA)
    _borrar(RUTA_ESCENA_DILOLIO)
    _borrar(RUTA_VISTAS)


# ==========================================================
# CASILLAS DE PARTIDA (NUEVA / CARGAR)
# ==========================================================

def _picar(contrasena):
    """La contrasena no se guarda tal cual: se guarda su sha256."""

    return hashlib.sha256(("compu bros|" + contrasena).encode("utf-8")).hexdigest()


def info_partida(numero):
    """
    {"numero", "nombre", "nivel", "con_contrasena"} de la casilla, o None
    si esta vacia. "nivel" es el que toca jugar (1 a 30).
    """

    texto = _leer(os.path.join(carpeta_partida(numero), "partida.txt"))
    if texto is None:
        return None
    lineas = texto.splitlines() + ["", ""]
    nombre = lineas[0].strip() or "PARTIDA %d" % numero
    picada = lineas[1].strip()

    nivel_txt = _leer(os.path.join(carpeta_partida(numero), "nivel.txt"))
    try:
        completados = int(nivel_txt.split()[0])
    except (AttributeError, IndexError, ValueError):
        completados = 0

    return {
        "numero": numero,
        "nombre": nombre,
        "nivel": max(1, min(TOTAL_NIVELES, completados + 1)),
        "con_contrasena": bool(picada),
    }


def info_partidas():
    """Las 6 casillas (None en las vacias)."""

    return [info_partida(n) for n in range(1, CANTIDAD_PARTIDAS + 1)]


def contrasena_correcta(numero, contrasena):

    texto = _leer(os.path.join(carpeta_partida(numero), "partida.txt"))
    if texto is None:
        return False
    lineas = texto.splitlines() + ["", ""]
    picada = lineas[1].strip()
    return not picada or picada == _picar(contrasena)


def crear_partida(numero, nombre, contrasena):
    """Partida nueva en la casilla (si habia otra, se pisa)."""

    carpeta = carpeta_partida(numero)
    shutil.rmtree(carpeta, ignore_errors=True)
    os.makedirs(carpeta, exist_ok=True)
    _escribir(
        os.path.join(carpeta, "partida.txt"),
        "%s\n%s\n" % (nombre.strip(), _picar(contrasena) if contrasena else "")
    )
    usar_partida(numero)


def ultima_partida():
    """Numero de la ultima partida que se jugo (si todavia existe)."""

    try:
        numero = int((_leer(RUTA_ULTIMA_PARTIDA) or "").strip())
    except ValueError:
        return None
    if 1 <= numero <= CANTIDAD_PARTIDAS and info_partida(numero) is not None:
        return numero
    return None


def _pasar_progreso_viejo():
    """
    Antes habia una sola partida, con los archivos sueltos en la carpeta
    del juego. Si estan, se mueven a la casilla 1 ("MI PARTIDA", sin
    contrasena) para no perder el progreso.
    """

    viejos = [a for a in ARCHIVOS_PARTIDA.values() if os.path.exists(os.path.join(CARPETA, a))]
    if not viejos:
        return
    if any(info_partida(n) is not None for n in range(1, CANTIDAD_PARTIDAS + 1)):
        return
    carpeta = carpeta_partida(1)
    os.makedirs(carpeta, exist_ok=True)
    for archivo in viejos:
        try:
            shutil.move(os.path.join(CARPETA, archivo), os.path.join(carpeta, archivo))
        except OSError:
            pass
    _escribir(os.path.join(carpeta, "partida.txt"), "MI PARTIDA\n\n")
    _escribir(RUTA_ULTIMA_PARTIDA, "1\n")


_pasar_progreso_viejo()

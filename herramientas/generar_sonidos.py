"""
Genera los efectos de sonido del juego (estilo chiptune) en assets/sonidos/.

No hace falta ningun programa de audio: los sonidos se calculan con onditas
cuadradas, de sierra y ruido, y se guardan como .wav (16 bits, mono).

    python herramientas/generar_sonidos.py            # los hace todos
    python herramientas/generar_sonidos.py salto      # solo algunos

Si se quiere usar un sonido propio alcanza con reemplazar el .wav (mono o
estereo, el volumen lo ajusta el juego). Hace falta:  pip install numpy

Sonidos:
    click       boton del menu / ajustes
    salto       el personaje salta
    aplastar    se pisa a un gagamba, un hincha o una pelota
    golpe       se pierde una vida
    guinness    se agarra una Guinness (+500 puntos)
    heineken    se agarra una Heineken (+1 vida)
    vidrio      se rompe una botella
    meta        se llega al final del nivel / a la bandera del tutorial
"""

import os
import sys
import wave

import numpy as np

CARPETA_JUEGO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_SALIDA = os.path.join(CARPETA_JUEGO, "assets", "sonidos")

HZ = 22050


# ==========================================================
# ONDAS
# ==========================================================

def tiempo(segundos):
    return np.arange(int(HZ * segundos)) / HZ


def cuadrada(frecuencia, ciclo=0.5):
    """frecuencia: numero o arreglo (barrido) en Hz."""

    fase = np.cumsum(frecuencia / HZ) if np.ndim(frecuencia) else None

    if fase is None:
        raise ValueError("usar barrer() o nota()")

    return np.where((fase % 1.0) < ciclo, 1.0, -1.0)


def sierra(frecuencia):

    fase = np.cumsum(frecuencia / HZ)

    return 2.0 * (fase % 1.0) - 1.0


def seno(frecuencia):

    fase = np.cumsum(frecuencia / HZ)

    return np.sin(2 * np.pi * fase)


def ruido(segundos, semilla=1):

    return np.random.RandomState(semilla).uniform(-1, 1, int(HZ * segundos))


def barrer(f0, f1, segundos, curva=1.0):
    """Frecuencia que va de f0 a f1 (curva > 1 = cambia rapido al final)."""

    x = np.linspace(0, 1, int(HZ * segundos)) ** curva

    return f0 + (f1 - f0) * x


def envolvente(n, ataque=0.004, caida=1.0, potencia=2.0):
    """Sube rapido y se apaga de a poco (caida = fraccion que dura)."""

    t = np.linspace(0, 1, n)

    a = np.minimum(1.0, t / max(1e-6, ataque * HZ / max(n, 1)))

    d = np.clip(1.0 - t / caida, 0, 1) ** potencia

    return a * d


def nota(frecuencia, segundos, onda="cuadrada", volumen=1.0, caida=1.0,
         potencia=1.6):

    f = np.full(int(HZ * segundos), float(frecuencia))

    if onda == "cuadrada":
        y = cuadrada(f, 0.5)
    elif onda == "pulso":
        y = cuadrada(f, 0.25)
    elif onda == "sierra":
        y = sierra(f)
    else:
        y = seno(f)

    return y * envolvente(len(y), caida=caida, potencia=potencia) * volumen


def silencio(segundos):

    return np.zeros(int(HZ * segundos))


def mezclar(*pistas):
    """Suma pistas de distinto largo (arrancan juntas)."""

    n = max(len(p) for p in pistas)

    salida = np.zeros(n)

    for p in pistas:
        salida[:len(p)] += p

    return salida


def secuencia(*partes):

    return np.concatenate(partes)


def pasa_altos(y, corte=2000):
    """Filtro simple: deja los agudos (suena a vidrio / chasquido)."""

    rc = 1.0 / (2 * np.pi * corte)
    alfa = rc / (rc + 1.0 / HZ)

    salida = np.zeros_like(y)

    for i in range(1, len(y)):
        salida[i] = alfa * (salida[i - 1] + y[i] - y[i - 1])

    return salida


# ==========================================================
# LOS SONIDOS
# ==========================================================

def s_click():

    return mezclar(
        nota(1040, 0.045, "cuadrada", 0.7, potencia=2.5),
        nota(520, 0.05, "pulso", 0.35, potencia=2.5),
    )


def s_salto():

    f = barrer(260, 720, 0.16, curva=0.7)

    y = cuadrada(f, 0.35)

    return y * envolvente(len(y), caida=1.0, potencia=1.4) * 0.8


def s_aplastar():

    # "plop" que baja + un chasquido corto
    f = barrer(520, 110, 0.13, curva=0.6)

    cuerpo = cuadrada(f, 0.5) * envolvente(len(f), potencia=1.8) * 0.85

    chasquido = ruido(0.04, 3) * envolvente(int(HZ * 0.04), potencia=3) * 0.55

    return mezclar(cuerpo, chasquido)


def s_golpe():

    # buzzer grave que cae
    f = barrer(330, 70, 0.34, curva=0.8)

    cuerpo = sierra(f) * envolvente(len(f), caida=1.0, potencia=1.2) * 0.8

    f2 = barrer(165, 55, 0.34, curva=0.8)

    sub = cuadrada(f2, 0.5) * envolvente(len(f2), potencia=1.4) * 0.45

    golpe = ruido(0.08, 5) * envolvente(int(HZ * 0.08), potencia=2.5) * 0.7

    return mezclar(cuerpo, sub, golpe)


def s_guinness():

    # moneda: dos notas agudas (Si - Mi)
    return secuencia(
        nota(988, 0.07, "cuadrada", 0.7, caida=1.0, potencia=0.8),
        nota(1319, 0.30, "cuadrada", 0.7, caida=1.0, potencia=1.8),
    )


def s_heineken():

    # "vida extra": arpegio que sube
    notas = [659, 784, 1319, 1047, 1175, 1568]

    partes = []

    for i, hz in enumerate(notas):

        ultimo = i == len(notas) - 1

        partes.append(
            nota(hz, 0.32 if ultimo else 0.075, "cuadrada", 0.65,
                 caida=1.0, potencia=0.9 if not ultimo else 1.8)
        )

    return secuencia(*partes)


def s_vidrio():

    # estallido de vidrio: ruido agudo + cascabelitos
    n = int(HZ * 0.38)

    estallido = pasa_altos(ruido(0.38, 7), 2500) * envolvente(n, potencia=2.4) * 1.4

    pings = [np.zeros(n)]

    azar = np.random.RandomState(11)

    for k in range(7):

        inicio = int(HZ * azar.uniform(0.0, 0.20))

        hz = azar.choice([2093, 2637, 3136, 3520, 4186])

        ping = nota(hz, 0.12, "seno", 0.32, potencia=2.2)

        p = np.zeros(n)

        p[inicio:inicio + len(ping)] = ping[:max(0, n - inicio)]

        pings.append(p)

    return mezclar(estallido, *pings)


def s_meta():

    # fanfarria corta (Do - Mi - Sol - Do)
    return secuencia(
        nota(523, 0.11, "cuadrada", 0.65, potencia=0.8),
        nota(659, 0.11, "cuadrada", 0.65, potencia=0.8),
        nota(784, 0.11, "cuadrada", 0.65, potencia=0.8),
        mezclar(
            nota(1047, 0.55, "cuadrada", 0.55, potencia=1.6),
            nota(523, 0.55, "pulso", 0.30, potencia=1.6),
        ),
    )


SONIDOS = {
    "click": s_click,
    "salto": s_salto,
    "aplastar": s_aplastar,
    "golpe": s_golpe,
    "guinness": s_guinness,
    "heineken": s_heineken,
    "vidrio": s_vidrio,
    "meta": s_meta,
}


# ==========================================================
# GUARDAR
# ==========================================================

def guardar(nombre, y):

    # sin chasquidos al principio ni al final y sin pasarse de volumen
    y = np.asarray(y, dtype=np.float64)

    pico = np.max(np.abs(y)) or 1.0

    y = y / pico * 0.8

    fade = int(HZ * 0.004)

    y[:fade] *= np.linspace(0, 1, fade)
    y[-fade:] *= np.linspace(1, 0, fade)

    datos = (y * 32767).astype("<i2")

    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    ruta = os.path.join(CARPETA_SALIDA, nombre + ".wav")

    with wave.open(ruta, "wb") as w:

        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(HZ)
        w.writeframes(datos.tobytes())

    return ruta, len(y) / HZ


def main():

    pedidos = sys.argv[1:] or list(SONIDOS)

    for nombre in pedidos:

        if nombre not in SONIDOS:
            print("no existe el sonido:", nombre, "(hay:", ", ".join(SONIDOS) + ")")
            continue

        ruta, duracion = guardar(nombre, SONIDOS[nombre]())

        print("%-9s %.2f s  %s" % (nombre, duracion, os.path.relpath(ruta, CARPETA_JUEGO)))


if __name__ == "__main__":

    main()

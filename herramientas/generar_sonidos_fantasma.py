"""
Sonidos de la escena del FantasmaCastro (8 bits, sintetizados):
    vomito.wav     arcada + chorro
    explosion.wav  la explosion de Castro
    fantasma.wav   "uuuuh" del fantasma que se va volando

Uso: python herramientas/generar_sonidos_fantasma.py
"""

import math
import os
import random
import struct
import wave

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "assets", "sonidos")
FR = 22050


def guardar(nombre, muestras):
    with wave.open(os.path.join(SALIDA, nombre), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(FR)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, m)) * 30000)) for m in muestras))


def vomito():
    azar = random.Random(3)
    m = []
    # Arcada: tono grave que baja ("hrrk")
    n = int(FR * 0.35)
    for i in range(n):
        t = i / FR
        f = 140 - 60 * t / 0.35
        cuadrada = 1 if math.sin(2 * math.pi * f * t) > 0 else -1
        m.append(0.45 * cuadrada * (1 - i / n) + 0.15 * (azar.random() * 2 - 1))
    m += [0.0] * int(FR * 0.05)
    # Chorro: ruido filtrado que gorgotea
    n = int(FR * 0.9)
    previo = 0.0
    for i in range(n):
        t = i / FR
        ruido = azar.random() * 2 - 1
        previo = previo * 0.85 + ruido * 0.15
        gorgoteo = 0.5 + 0.5 * math.sin(2 * math.pi * 11 * t)
        env = min(1.0, t / 0.05) * (1 - i / n) ** 0.6
        m.append(1.6 * previo * gorgoteo * env)
    return m


def explosion():
    azar = random.Random(9)
    m = []
    n = int(FR * 1.4)
    previo = 0.0
    paso = 1
    retenido = 0.0
    for i in range(n):
        t = i / FR
        # Ruido "8 bits": se repite cada tantas muestras (mas grave al final)
        paso = 2 + int(t * 14)
        if i % paso == 0:
            retenido = azar.random() * 2 - 1
        previo = previo * 0.6 + retenido * 0.4
        golpe = math.sin(2 * math.pi * (60 - 30 * t) * t) * max(0, 1 - t / 0.3)
        env = math.exp(-t * 2.6)
        m.append(0.9 * previo * env + 0.6 * golpe)
    return m


def fantasma():
    m = []
    n = int(FR * 1.1)
    for i in range(n):
        t = i / FR
        f = 420 + 160 * math.sin(2 * math.pi * 1.2 * t) + 5 * math.sin(2 * math.pi * 7 * t) * 10
        env = min(1.0, t / 0.15) * min(1.0, (n - i) / (FR * 0.3))
        triangular = 2 * abs(2 * ((f * t) % 1) - 1) - 1
        m.append(0.35 * triangular * env)
    return m


if __name__ == "__main__":
    guardar("vomito.wav", vomito())
    guardar("explosion.wav", explosion())
    guardar("fantasma.wav", fantasma())
    print("listo")

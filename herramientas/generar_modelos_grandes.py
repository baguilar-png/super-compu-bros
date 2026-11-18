"""
Modelos GRANDES de los Compu Bros (del tamano de Lord Teichi).

NO los usa el juego: quedan en la carpeta modelos/ para mirarlos, editarlos
o usarlos mas adelante (por ejemplo en escenas, portadas o un jefe).

Agranda cada sprite al doble con Scale2x (suaviza las diagonales en vez de
hacer cuadrados de 2x2) y lo recorta. Tambien arma modelos/vista_previa.png
con todos juntos al lado de Teichi.

Uso (desde la carpeta del juego):
    python herramientas/generar_modelos_grandes.py
"""

import os

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSONAJES = os.path.join(RAIZ, "assets", "personajes")
SALIDA = os.path.join(RAIZ, "modelos")

BROS = ["BAUTO", "BENJA", "CASTRO", "POSHO", "THIAGO"]

# Pose -> como termina el nombre del archivo original (sin mayusculas)
POSES = [
    ("frente", "frente.png"),
    ("caminar_1", "frame 1.png"),
    ("caminar_2", "frame 2.png"),
    ("caminar_3", "frame 3.png"),
    ("saltando", "saltando.png"),
    ("agachado", "agachado.png"),
    ("costado", "final.png"),
    ("cabeza", "cabeza.png"),
]


def scale2x(img):
    """Scale2x / EPX: duplica el tamano manteniendo el estilo pixel art."""

    img = img.convert("RGBA")
    w, h = img.size
    src = img.load()
    out = Image.new("RGBA", (w * 2, h * 2))
    dst = out.load()

    def px(x, y):
        x = min(max(x, 0), w - 1)
        y = min(max(y, 0), h - 1)
        return src[x, y]

    for y in range(h):
        for x in range(w):
            p = src[x, y]
            a, b, c, d = px(x, y - 1), px(x + 1, y), px(x - 1, y), px(x, y + 1)
            e0 = e1 = e2 = e3 = p
            if c == a and c != d and a != b:
                e0 = a
            if a == b and a != c and b != d:
                e1 = b
            if d == c and d != b and c != a:
                e2 = c
            if b == d and b != a and d != c:
                e3 = d
            dst[2 * x, 2 * y] = e0
            dst[2 * x + 1, 2 * y] = e1
            dst[2 * x, 2 * y + 1] = e2
            dst[2 * x + 1, 2 * y + 1] = e3
    return out


def buscar(carpeta, final):
    for nombre in sorted(os.listdir(carpeta)):
        bajo = nombre.lower()
        if bajo.endswith(final) and not (final == "frente.png" and bajo == "iki frente.png"):
            return os.path.join(carpeta, nombre)
    return None


def main():
    os.makedirs(SALIDA, exist_ok=True)
    frentes = []

    for bro in BROS:
        carpeta = os.path.join(PERSONAJES, bro)
        destino = os.path.join(SALIDA, bro)
        os.makedirs(destino, exist_ok=True)
        for pose, final in POSES:
            ruta = buscar(carpeta, final)
            if ruta is None:
                continue
            img = Image.open(ruta).convert("RGBA")
            caja = img.getbbox()
            if caja:
                img = img.crop(caja)
            grande = scale2x(img)
            grande.save(os.path.join(destino, pose + ".png"))
            if pose == "frente":
                frentes.append(grande)

    # Vista previa: los 5 al lado de Teichi, agrandada x4 para verla bien
    teichi = Image.open(os.path.join(PERSONAJES, "TEICHI", "quieto.png")).convert("RGBA")
    todos = frentes + [teichi]
    alto = max(i.height for i in todos) + 4
    ancho = sum(i.width + 6 for i in todos) + 6
    vista = Image.new("RGBA", (ancho, alto), (90, 140, 200, 255))
    x = 6
    for i in todos:
        vista.alpha_composite(i, (x, alto - 2 - i.height))
        x += i.width + 6
    vista = vista.resize((ancho * 4, alto * 4), Image.NEAREST)
    vista.save(os.path.join(SALIDA, "vista_previa.png"))
    print("Modelos en", SALIDA)


if __name__ == "__main__":
    main()

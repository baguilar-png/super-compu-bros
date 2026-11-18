"""
Arma la HOJA DE SPRITES (spritesheet) de LORD TEICHI a partir de sus 5
poses (assets/personajes/TEICHI/*.png), para que se mueva fluido como los
Compu Bros:

    quieto, respirar           parado (respira: el cuerpo baja 1 pixel)
    caminar_1 ... caminar_4    camina: levanta un pie, apoya, levanta el
                               otro, apoya (con el cuerpo subiendo y bajando)
    tirar                      con la piedra arriba de la cabeza
    agachado, brazos_arriba    para el golpe al piso
    empujar, correr_2          la embestida (dos pasos)

Todas las poses van en una sola imagen, una al lado de la otra, en
casilleros del mismo tamano y apoyadas abajo y centradas:

    assets/personajes/TEICHI/teichi_hoja.png

El orden es ORDEN (abajo); jefes.py usa el mismo orden para cortarla.
Tambien se guarda cada cuadro suelto en assets/personajes/TEICHI/hoja/.

Uso, desde la carpeta del juego:

    python herramientas/generar_teichi_hoja.py
"""

import os

from PIL import Image

CARPETA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEICHI = os.path.join(CARPETA, "assets", "personajes", "TEICHI")

ORDEN = [
    "quieto", "respirar",
    "caminar_1", "caminar_2", "caminar_3", "caminar_4",
    "tirar", "agachado", "brazos_arriba",
    "empujar", "correr_2",
]

# Filas donde empiezan las piernas y columna que separa la pierna izquierda
# de la derecha (en el dibujo quieto y en el de empujar)
PIERNAS_QUIETO = (37, 23)
PIERNAS_EMPUJAR = (33, 20)


def _mover(img, caja, dx, dy):
    """Mueve un pedazo de la imagen (caja = x0, y0, x1, y1)."""
    pedazo = img.crop(caja)
    salida = img.copy()
    salida.paste((0, 0, 0, 0), caja)
    salida.alpha_composite(pedazo, (caja[0] + dx, caja[1] + dy))
    return salida


def _cuerpo_abajo(img, fila_piernas, cuanto=1):
    """Baja el cuerpo (de las piernas para arriba) unos pixeles."""
    ancho, _ = img.size
    return _mover(img, (0, 0, ancho, fila_piernas), 0, cuanto)


def _levantar_pie(img, fila, desde, hasta, cuanto=2):
    """Levanta una pierna (de la fila de las piernas para abajo)."""
    _, alto = img.size
    return _mover(img, (desde, fila, hasta, alto), 0, -cuanto)


def generar():

    poses = {
        n: Image.open(os.path.join(TEICHI, n + ".png")).convert("RGBA")
        for n in ("quieto", "tirar", "empujar", "brazos_arriba", "agachado")
    }

    quieto = poses["quieto"]
    fila, medio = PIERNAS_QUIETO
    ancho_q = quieto.width

    cuadros = {
        "quieto": quieto,
        "respirar": _cuerpo_abajo(quieto, fila),
        # Pie izquierdo arriba, apoya (cuerpo abajo), pie derecho arriba, apoya
        "caminar_1": _levantar_pie(quieto, fila, 0, medio),
        "caminar_2": _cuerpo_abajo(quieto, fila),
        "caminar_3": _levantar_pie(quieto, fila, medio, ancho_q),
        "caminar_4": _cuerpo_abajo(quieto, fila),
        "tirar": poses["tirar"],
        "agachado": poses["agachado"],
        "brazos_arriba": poses["brazos_arriba"],
        "empujar": poses["empujar"],
    }

    fila_e, medio_e = PIERNAS_EMPUJAR
    empujar = poses["empujar"]
    cuadros["correr_2"] = _cuerpo_abajo(
        _levantar_pie(empujar, fila_e, 0, medio_e, 3), fila_e
    )

    # Casilleros del mismo tamano: el ancho y el alto mas grandes
    ancho = max(c.width for c in cuadros.values())
    alto = max(c.height for c in cuadros.values())

    hoja = Image.new("RGBA", (ancho * len(ORDEN), alto), (0, 0, 0, 0))
    os.makedirs(os.path.join(TEICHI, "hoja"), exist_ok=True)

    for i, nombre in enumerate(ORDEN):
        cuadro = cuadros[nombre]
        x = i * ancho + (ancho - cuadro.width) // 2
        y = alto - cuadro.height
        hoja.alpha_composite(cuadro, (x, y))
        cuadro.save(os.path.join(TEICHI, "hoja", nombre + ".png"))

    hoja.save(os.path.join(TEICHI, "teichi_hoja.png"))
    print("Hoja:", hoja.size, "casilleros de", (ancho, alto))


if __name__ == "__main__":
    generar()

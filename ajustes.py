"""
Ajustes del juego: volumen de la musica y de los efectos.

Cada volumen es un numero entero de 0 a 100 (100 = como sonaba antes).
Se guardan en ajustes.txt apenas se cambian, asi que sobreviven a cerrar el
juego (y NO se borran cuando se pierden todas las vidas).

    import ajustes
    ajustes.musica            # 0 a 100
    ajustes.efectos           # 0 a 100
    ajustes.fijar_musica(40)  # cambia, guarda y se oye en el momento
    ajustes.fijar_efectos(40)
"""

from archivos import cargar_ajustes, guardar_ajustes

musica, efectos = cargar_ajustes()


def _limitar(valor):

    return max(0, min(100, int(round(valor))))


def factor_musica():
    """0.0 a 1.0 (se multiplica por el volumen base de la musica)."""

    return musica / 100.0


def factor_efectos():
    """0.0 a 1.0 (se multiplica por el volumen base de cada efecto)."""

    return efectos / 100.0


def fijar_musica(valor):
    """Cambia el volumen de la musica: se oye en el momento y se guarda."""

    global musica

    valor = _limitar(valor)

    if valor == musica:

        return

    musica = valor

    guardar_ajustes(musica, efectos)

    # La musica que esta sonando cambia de volumen sin cortarse
    import musica as modulo_musica

    modulo_musica.aplicar_volumen()


def fijar_efectos(valor):
    """Cambia el volumen de los efectos y se guarda."""

    global efectos

    valor = _limitar(valor)

    if valor == efectos:

        return

    efectos = valor

    guardar_ajustes(musica, efectos)

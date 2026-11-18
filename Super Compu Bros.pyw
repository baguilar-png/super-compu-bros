"""
Abre el juego sin la ventana negra de la consola (en Windows, los .pyw se
abren con pythonw). Es lo que abre el acceso directo.
"""

import os
import runpy
import sys

CARPETA = os.path.dirname(os.path.abspath(__file__))

os.chdir(CARPETA)
sys.path.insert(0, CARPETA)

runpy.run_path(os.path.join(CARPETA, "main.py"), run_name="__main__")

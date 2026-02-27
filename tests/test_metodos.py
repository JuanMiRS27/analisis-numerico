from metodos.biseccion import biseccion
from metodos.falsa_posicion import falsa_posicion
from metodos.punto_fijo import punto_fijo
from metodos.newton import newton_raphson
from metodos.secante import secante

from funciones.definiciones import (
    funcion_biseccion,
    funcion_falsa_posicion,
    g_punto_fijo,
    funcion_newton,
    derivada_newton,
    funcion_secante
)

def test_biseccion():
    f_test = lambda x: x**2 - 4   # raíz en x = 2
    resultados = biseccion(f_test, 0, 5, 1e-6, 100)
    assert len(resultados) > 0
    assert abs(resultados[-1]["f_c"]) < 1e-6


def test_falsa_posicion():
    resultados = falsa_posicion(funcion_falsa_posicion, 2, 4, 1e-7, 100)
    assert len(resultados) > 0
    assert abs(resultados[-1]["f_c"]) < 1e-6


def test_punto_fijo():
    resultados = punto_fijo(g_punto_fijo, 1.0, 1e-8, 100)
    assert len(resultados) > 0
    ultimo_error = resultados[-1]["error_abs"]
    assert ultimo_error < 1e-6


def test_newton():
    resultados = newton_raphson(funcion_newton, derivada_newton, 2.5, 1e-10, 100)
    assert len(resultados) > 0
    assert abs(resultados[-1]["f_x"]) < 1e-6

def test_secante():
    resultados = secante(funcion_secante, 0.5, 1.0, 1e-9, 100)
    assert len(resultados) > 0
    assert abs(funcion_secante(resultados[-1]["x_next"])) < 1e-6
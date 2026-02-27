import numpy as np

# ===== EJERCICIO 1: BISECCIÓN =====
def funcion_biseccion(lam: float) -> float:
    return 2.5 + 0.8 * lam**2 - 3.2 * lam + np.log(lam + 1)


# ===== EJERCICIO 2: FALSA POSICIÓN =====
def funcion_falsa_posicion(x: float) -> float:
    return x**3 - 6*x**2 + 11*x - 6.5


# ===== EJERCICIO 3: PUNTO FIJO =====
def g_punto_fijo(x: float) -> float:
    return 0.5 * np.cos(x) + 1.5


def derivada_g_punto_fijo(x: float) -> float:
    return -0.5 * np.sin(x)


# ===== EJERCICIO 4: NEWTON =====
def funcion_newton(n: float) -> float:
    return n**3 - 8*n**2 + 20*n - 16


def derivada_newton(n: float) -> float:
    return 3*n**2 - 16*n + 20


# ===== EJERCICIO 5: SECANTE =====
def funcion_secante(x: float) -> float:
    return x * np.exp(-x / 2) - 0.3


def derivada_secante(x: float) -> float:
    return np.exp(-x / 2) * (1 - x / 2)


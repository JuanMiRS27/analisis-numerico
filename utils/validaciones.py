from typing import Callable

def validar_intervalo(f: Callable[[float], float], a: float, b: float) -> None:
    if a >= b:
        raise ValueError("El valor 'a' debe ser menor que 'b'.")

    fa = f(a)
    fb = f(b)

    if fa * fb >= 0:
        raise ValueError("El intervalo no encierra una raíz (no hay cambio de signo).")


def validar_tolerancia(tol: float) -> None:
    if tol <= 0:
        raise ValueError("La tolerancia debe ser un número positivo.")


def validar_max_iter(max_iter: int) -> None:
    if max_iter <= 0:
        raise ValueError("El número máximo de iteraciones debe ser mayor que cero.")


def validar_valor_inicial(x0: float) -> None:
    if not isinstance(x0, (int, float)):
        raise ValueError("El valor inicial debe ser numérico.")


def validar_dos_valores_iniciales(x0: float, x1: float) -> None:
    if not isinstance(x0, (int, float)) or not isinstance(x1, (int, float)):
        raise ValueError("Los valores iniciales deben ser numéricos.")
    if x0 == x1:
        raise ValueError("Los dos valores iniciales no pueden ser iguales.")


def validar_derivada_no_cero(df: Callable[[float], float], x: float) -> None:
    if df(x) == 0:
        raise ZeroDivisionError("La derivada es cero en el punto inicial. Newton falla.")


def validar_convergencia_punto_fijo(
    dg: Callable[[float], float],
    x: float
) -> None:
    valor = abs(dg(x))
    if valor >= 1:
        raise ValueError(
            f"La condición de convergencia no se cumple: |g'(x)| = {valor} ≥ 1"
        )
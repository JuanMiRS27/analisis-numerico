from typing import Callable, List, Dict

def falsa_posicion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float,
    max_iter: int
) -> List[Dict]:

    if f(a) * f(b) >= 0:
        raise ValueError("El intervalo no encierra una raíz.")

    resultados = []
    c_anterior = None

    for n in range(1, max_iter + 1):
        fa = f(a)
        fb = f(b)

        if fb - fa == 0:
            raise ZeroDivisionError("División por cero en falsa posición.")

        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)

        if c_anterior is None:
            error_abs = None
            error_rel = None
        else:
            error_abs = abs(c - c_anterior)
            error_rel = error_abs / abs(c)

        resultados.append({
            "iteracion": n,
            "a": a,
            "b": b,
            "c": c,
            "f_c": fc,
            "error_abs": error_abs,
            "error_rel": error_rel
        })

        if abs(fc) < tol or (error_abs is not None and error_abs < tol):
            break

        if fa * fc < 0:
            b = c
        else:
            a = c

        c_anterior = c

    return resultados
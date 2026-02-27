from typing import Callable, List, Dict

def biseccion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float,
    max_iter: int
) -> List[Dict]:

    if f(a) * f(b) >= 0:
        raise ValueError("El intervalo no encierra una raíz (no hay cambio de signo).")

    resultados = []
    c_anterior = None

    for n in range(1, max_iter + 1):
        c = (a + b) / 2
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

        if f(a) * fc < 0:
            b = c
        else:
            a = c

        c_anterior = c

    return resultados
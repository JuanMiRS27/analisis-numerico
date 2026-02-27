from typing import Callable, List, Dict

def punto_fijo(
    g: Callable[[float], float],
    x0: float,
    tol: float,
    max_iter: int
) -> List[Dict]:

    resultados = []
    x_actual = x0

    for n in range(1, max_iter + 1):
        x_siguiente = g(x_actual)
        error_abs = abs(x_siguiente - x_actual)
        error_rel = error_abs / abs(x_siguiente) if x_siguiente != 0 else None

        resultados.append({
            "iteracion": n,
            "x_n": x_actual,
            "g_x": x_siguiente,
            "error_abs": error_abs,
            "error_rel": error_rel
        })

        if error_abs < tol:
            break

        x_actual = x_siguiente

    return resultados
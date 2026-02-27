from typing import Callable, List, Dict

def secante(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tol: float,
    max_iter: int
) -> List[Dict]:

    resultados = []
    x_anterior = x0
    x_actual = x1

    for n in range(1, max_iter + 1):
        f_x0 = f(x_anterior)
        f_x1 = f(x_actual)

        if f_x1 - f_x0 == 0:
            raise ZeroDivisionError("División por cero en secante.")

        x_siguiente = x_actual - f_x1 * (x_actual - x_anterior) / (f_x1 - f_x0)
        error_abs = abs(x_siguiente - x_actual)
        error_rel = error_abs / abs(x_siguiente)

        resultados.append({
            "iteracion": n,
            "x_n_1": x_anterior,
            "x_n": x_actual,
            "f_x_n_1": f_x0,
            "f_x_n": f_x1,
            "x_next": x_siguiente,
            "error_abs": error_abs,
            "error_rel": error_rel
        })

        if error_abs < tol:
            break

        x_anterior, x_actual = x_actual, x_siguiente

    return resultados
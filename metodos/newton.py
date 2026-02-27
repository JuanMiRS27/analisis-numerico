from typing import Callable, List, Dict

def newton_raphson(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    tol: float,
    max_iter: int
) -> List[Dict]:

    resultados = []
    x_actual = x0

    for n in range(1, max_iter + 1):
        f_x = f(x_actual)
        df_x = df(x_actual)

        if df_x == 0:
            raise ZeroDivisionError("Derivada cero. Newton falla.")

        x_siguiente = x_actual - f_x / df_x
        error_abs = abs(x_siguiente - x_actual)
        error_rel = error_abs / abs(x_siguiente)

        resultados.append({
            "iteracion": n,
            "x_n": x_actual,
            "f_x": f_x,
            "df_x": df_x,
            "x_next": x_siguiente,
            "error_abs": error_abs,
            "error_rel": error_rel
        })

        if error_abs < tol:
            break

        x_actual = x_siguiente

    return resultados
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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


class App:
    def __init__(self, parent):
        self.root = parent

        # ===== Parámetros =====
        frame_inputs = ttk.LabelFrame(self.root, text="Parámetros")
        frame_inputs.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        ttk.Label(frame_inputs, text="Método:").grid(row=0, column=0, sticky="w")
        self.combo_metodo = ttk.Combobox(
            frame_inputs,
            values=["Bisección", "Falsa Posición", "Punto Fijo", "Newton-Raphson", "Secante"],
            state="readonly"
        )
        self.combo_metodo.current(0)
        self.combo_metodo.grid(row=0, column=1, pady=5)
        self.combo_metodo.bind("<<ComboboxSelected>>", self.actualizar_campos)

        ttk.Label(frame_inputs, text="a / x0:").grid(row=1, column=0, sticky="w")
        self.entry_a = ttk.Entry(frame_inputs)
        self.entry_a.grid(row=1, column=1)

        ttk.Label(frame_inputs, text="b / x1:").grid(row=2, column=0, sticky="w")
        self.entry_b = ttk.Entry(frame_inputs)
        self.entry_b.grid(row=2, column=1)

        ttk.Label(frame_inputs, text="Tolerancia:").grid(row=3, column=0, sticky="w")
        self.entry_tol = ttk.Entry(frame_inputs)
        self.entry_tol.insert(0, "1e-6")
        self.entry_tol.grid(row=3, column=1)

        ttk.Label(frame_inputs, text="Max iter:").grid(row=4, column=0, sticky="w")
        self.entry_iter = ttk.Entry(frame_inputs)
        self.entry_iter.insert(0, "100")
        self.entry_iter.grid(row=4, column=1)

        ttk.Button(frame_inputs, text="Calcular", command=self.calcular).grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Button(frame_inputs, text="Limpiar", command=self.limpiar).grid(row=6, column=0, columnspan=2, pady=5)

        # ===== Tabla =====
        frame_tabla = ttk.LabelFrame(self.root, text="Iteraciones")
        frame_tabla.grid(row=0, column=1, padx=10, pady=10)

        columnas = ("n", "x_n", "x_prev", "f_x", "error_abs", "error_rel")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)
        for col, txt in zip(columnas, ["n", "x_n", "x_{n-1}", "f(x_n)", "Error abs", "Error rel (%)"]):
            self.tabla.heading(col, text=txt)
            self.tabla.column(col, width=110, anchor="center")
        self.tabla.pack()

        # ===== Gráfica principal =====
        frame_grafica = ttk.LabelFrame(self.root, text="Función y Convergencia")
        frame_grafica.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.fig = Figure(figsize=(7, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_grafica)
        self.canvas.get_tk_widget().pack()

        # ===== Gráfica de error =====
        frame_error = ttk.LabelFrame(self.root, text="Convergencia del Error (escala log)")
        frame_error.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.fig_err = Figure(figsize=(7, 3), dpi=100)
        self.ax_err = self.fig_err.add_subplot(111)
        self.canvas_err = FigureCanvasTkAgg(self.fig_err, master=frame_error)
        self.canvas_err.get_tk_widget().pack()

        # ===== Resultados finales =====
        frame_resultados = ttk.LabelFrame(self.root, text="Resultados finales")
        frame_resultados.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.lbl_raiz = ttk.Label(frame_resultados, text="Raíz aproximada: -")
        self.lbl_iters = ttk.Label(frame_resultados, text="Iteraciones: -")
        self.lbl_error = ttk.Label(frame_resultados, text="Error final: -")
        self.lbl_tiempo = ttk.Label(frame_resultados, text="Tiempo: -")
        self.lbl_estado = ttk.Label(frame_resultados, text="Estado: -")

        self.lbl_raiz.grid(row=0, column=0, padx=10, sticky="w")
        self.lbl_iters.grid(row=0, column=1, padx=10, sticky="w")
        self.lbl_error.grid(row=0, column=2, padx=10, sticky="w")
        self.lbl_tiempo.grid(row=1, column=0, padx=10, sticky="w")
        self.lbl_estado.grid(row=1, column=1, columnspan=2, padx=10, sticky="w")

        self.actualizar_campos()

    def actualizar_campos(self, event=None):
        metodo = self.combo_metodo.get()
        self.entry_b.config(state="normal")
        if metodo in ["Punto Fijo", "Newton-Raphson"]:
            self.entry_b.delete(0, tk.END)
            self.entry_b.config(state="disabled")

    def calcular(self):
        inicio = time.perf_counter()
        try:
            metodo = self.combo_metodo.get()
            tol = float(self.entry_tol.get())
            max_iter = int(self.entry_iter.get())

            if metodo == "Bisección":
                a = float(self.entry_a.get())
                b = float(self.entry_b.get())
                resultados = biseccion(funcion_biseccion, a, b, tol, max_iter)
                xs = [r["c"] for r in resultados]
                fxs = [r["f_c"] for r in resultados]
                fplot = funcion_biseccion

            elif metodo == "Falsa Posición":
                a = float(self.entry_a.get())
                b = float(self.entry_b.get())
                resultados = falsa_posicion(funcion_falsa_posicion, a, b, tol, max_iter)
                xs = [r["c"] for r in resultados]
                fxs = [r["f_c"] for r in resultados]
                fplot = funcion_falsa_posicion

            elif metodo == "Punto Fijo":
                x0 = float(self.entry_a.get())
                resultados = punto_fijo(g_punto_fijo, x0, tol, max_iter)
                xs = [r["x_n"] for r in resultados]
                fxs = [funcion_newton(x) for x in xs]
                fplot = lambda x: g_punto_fijo(x) - x

            elif metodo == "Newton-Raphson":
                x0 = float(self.entry_a.get())
                resultados = newton_raphson(funcion_newton, derivada_newton, x0, tol, max_iter)
                xs = [r["x_n"] for r in resultados]
                fxs = [r["f_x"] for r in resultados]
                fplot = funcion_newton

            elif metodo == "Secante":
                x0 = float(self.entry_a.get())
                x1 = float(self.entry_b.get())
                resultados = secante(funcion_secante, x0, x1, tol, max_iter)
                xs = [r["x_next"] for r in resultados]
                fxs = [funcion_secante(x) for x in xs]
                fplot = funcion_secante

            # Tabla + errores
            for fila in self.tabla.get_children():
                self.tabla.delete(fila)

            errores = []
            x_prev = None
            for i, x_n in enumerate(xs, start=1):
                if x_prev is None:
                    err_abs = ""
                    err_rel = ""
                    x_prev_show = ""
                else:
                    err_abs = abs(x_n - x_prev)
                    err_rel = abs((x_n - x_prev) / x_n) * 100 if x_n != 0 else 0
                    x_prev_show = f"{x_prev:.6f}"
                    errores.append(err_abs)

                self.tabla.insert("", tk.END, values=(
                    i, f"{x_n:.6f}", x_prev_show,
                    f"{fxs[i-1]:.6e}",
                    "" if err_abs == "" else f"{err_abs:.3e}",
                    "" if err_rel == "" else f"{err_rel:.3f}"
                ))
                x_prev = x_n

            # ===== Gráfica 1 =====
            self.ax.clear()
            x_plot = np.linspace(min(xs) - 1, max(xs) + 1, 400)
            y_plot = [fplot(x) for x in x_plot]
            self.ax.axhline(0)
            self.ax.plot(x_plot, y_plot, label="f(x)")
            self.ax.plot(xs, fxs, "o-", label="Iteraciones")
            self.ax.plot(xs[-1], fxs[-1], "s", markersize=10, label="Raíz final")
            self.ax.set_title(f"{metodo} - Función y Convergencia")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("f(x)")
            self.ax.legend()
            self.canvas.draw()

            # Tangentes, secantes, cobweb
            if metodo == "Newton-Raphson":
                for x in xs[:-1]:
                    y = funcion_newton(x)
                    m = derivada_newton(x)
                    xt = np.linspace(x - 1, x + 1, 50)
                    yt = m * (xt - x) + y
                    self.ax.plot(xt, yt, "--", alpha=0.6)
                self.canvas.draw()

            elif metodo == "Secante":
                for i in range(len(xs) - 1):
                    x0, x1 = xs[i], xs[i + 1]
                    y0, y1 = funcion_secante(x0), funcion_secante(x1)
                    xt = np.linspace(x0, x1, 50)
                    yt = y0 + (y1 - y0) * (xt - x0) / (x1 - x0)
                    self.ax.plot(xt, yt, "--", alpha=0.6)
                self.canvas.draw()

            elif metodo == "Punto Fijo":
                self.ax.clear()
                x_plot = np.linspace(min(xs) - 1, max(xs) + 1, 400)
                self.ax.plot(x_plot, x_plot, "k--", label="y = x")
                self.ax.plot(x_plot, [g_punto_fijo(x) for x in x_plot], label="y = g(x)")
                for i in range(len(xs) - 1):
                    self.ax.plot([xs[i], xs[i]], [xs[i], xs[i + 1]], "r-")
                    self.ax.plot([xs[i], xs[i + 1]], [xs[i + 1], xs[i + 1]], "r-")
                self.ax.legend()
                self.ax.set_title("Punto Fijo - Cobweb")
                self.canvas.draw()

            # ===== Gráfica 2: Error =====
            self.ax_err.clear()
            if errores:
                self.ax_err.semilogy(range(1, len(errores) + 1), errores, marker="o")
            self.ax_err.set_xlabel("Iteración")
            self.ax_err.set_ylabel("Error abs (log)")
            self.ax_err.set_title("Convergencia del Error")
            self.canvas_err.draw()

            fin = time.perf_counter()
            self.lbl_raiz.config(text=f"Raíz aproximada: {xs[-1]:.8f}")
            self.lbl_iters.config(text=f"Iteraciones: {len(xs)}")
            self.lbl_error.config(text=f"Error final: {errores[-1]:.3e}" if errores else "Error final: -")
            self.lbl_tiempo.config(text=f"Tiempo: {(fin - inicio)*1000:.2f} ms")
            self.lbl_estado.config(text="Estado: Convergencia exitosa ✅")

        except Exception as e:
            fin = time.perf_counter()
            self.lbl_estado.config(text=f"Estado: Fallo ❌ ({e})")
            self.lbl_tiempo.config(text=f"Tiempo: {(fin - inicio)*1000:.2f} ms")
            messagebox.showerror("Error", str(e))

    def limpiar(self):
        self.entry_a.delete(0, tk.END)
        self.entry_b.config(state="normal")
        self.entry_b.delete(0, tk.END)
        self.entry_tol.delete(0, tk.END)
        self.entry_tol.insert(0, "1e-6")
        self.entry_iter.delete(0, tk.END)
        self.entry_iter.insert(0, "100")

        self.combo_metodo.current(0)
        self.actualizar_campos()

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        self.ax.clear()
        self.canvas.draw()
        self.ax_err.clear()
        self.canvas_err.draw()

        self.lbl_raiz.config(text="Raíz aproximada: -")
        self.lbl_iters.config(text="Iteraciones: -")
        self.lbl_error.config(text="Error final: -")
        self.lbl_tiempo.config(text="Tiempo: -")
        self.lbl_estado.config(text="Estado: -")
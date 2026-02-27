import tkinter as tk
from tkinter import ttk
from interfaz.gui_principal import App

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Métodos Numéricos")

    # Canvas + Scrollbar
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    app = App(scrollable_frame)
    root.mainloop()
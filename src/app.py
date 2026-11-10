import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk

import numpy as np
import sounddevice as sd

from src.core.clasificador import METRICAS, analizar
from src.core.entrenamiento import cargar_modelo
from src.core.espectro import FS, N_PUNTOS

UMBRAL_RMS = 1e-3   
NOMBRES = {"hombre": "HOMBRE", "mujer": "MUJER"}

class App:
    def __init__(self, raiz, clases, medias, desviaciones, palabra):
        self.raiz = raiz
        self.clases = clases
        self.medias = medias
        self.desviaciones = desviaciones
        self.palabra = palabra
        self.cola = queue.Queue()
        self.ultima_senal = None  

        raiz.title("Reconocimiento de género por banco de filtros")

        barra = ttk.Frame(raiz, padding=8)
        barra.pack(fill="x")
        self.btn_grabar = ttk.Button(barra, text="Grabar 2 s y clasificar", command=self.grabar)
        self.btn_grabar.pack(side="left")
        ttk.Label(barra, text="Distancia:").pack(side="left", padx=(16, 4))
        self.metrica = tk.StringVar(value="Euclidiana")
        combo = ttk.Combobox(barra, textvariable=self.metrica, values=list(METRICAS),
                             state="readonly", width=24)
        combo.pack(side="left")
        combo.bind("<<ComboboxSelected>>", lambda _e: self.reclasificar())

        ttk.Label(raiz, text=f"Palabra a decir: «{palabra}»",
                  font=("Segoe UI", 14)).pack(pady=(10, 0))
        self.lbl_resultado = ttk.Label(raiz, text="—", font=("Segoe UI", 40, "bold"),
                                       anchor="center")
        self.lbl_resultado.pack(fill="x", pady=(4, 0))
        self.lbl_estado = ttk.Label(raiz, text="Pulsa «Grabar» y di la palabra.", anchor="center")
        self.lbl_estado.pack(fill="x")
        self.lbl_detalle = ttk.Label(raiz, text="", font=("Consolas", 10), justify="left")
        self.lbl_detalle.pack(padx=16, pady=10)

    # ------------------------------------------------------------------ micrófono
    def grabar(self):
        self.btn_grabar.config(state="disabled")
        self.lbl_estado.config(text=f"Grabando 2 s… di «{self.palabra}» ahora")
        threading.Thread(target=self._capturar, daemon=True).start()
        self.raiz.after(100, self._revisar_cola)

    def _capturar(self):
        try:
            audio = sd.rec(N_PUNTOS, samplerate=FS, channels=1, dtype="float32")
            sd.wait()
            self.cola.put(("ok", audio[:, 0].astype(np.float64)))
        except Exception as e:
            self.cola.put(("error", str(e)))

    def _revisar_cola(self):
        try:
            tipo, dato = self.cola.get_nowait()
        except queue.Empty:
            self.raiz.after(100, self._revisar_cola)
            return
        self.btn_grabar.config(state="normal")
        if tipo == "error":
            self.lbl_estado.config(text="Error al grabar")
            messagebox.showerror("Micrófono", f"No se pudo grabar:\n{dato}")
            return
        self._procesar(dato)

    # ------------------------------------------------------------------ análisis
    def _procesar(self, senal):
        self.ultima_senal = senal
        rms = float(np.sqrt(np.mean(senal ** 2)))
        try:
            res = analizar(senal, self.clases, self.medias, self.desviaciones,
                           self.metrica.get())
        except Exception as e:
            messagebox.showerror("Análisis", str(e))
            return

        d = np.sort(res["distancias"])
        margen = (d[1] - d[0]) / d[1] if d[1] > 0 else 0.0
        self.lbl_resultado.config(text=NOMBRES.get(res["clase"], res["clase"]))
        estado = f"RMS = {rms:.4f}  |  margen sobre la 2.ª clase: {margen:.0%}"
        if rms < UMBRAL_RMS:
            estado += "  |  ATENCIÓN: señal muy débil (¿micrófono silenciado o muy lejos?)"
        self.lbl_estado.config(text=estado)

        lineas = ["Distancia a cada clase (menor = más parecida):"]
        lineas += [f"  {c:<8} {x:10.4f}" for c, x in zip(self.clases, res["distancias"])]
        lineas += ["", "Energía por sub-banda de la captura:",
                   "  " + "  ".join(f"B{i + 1}={e:.4f}" for i, e in enumerate(res["vector"]))]
        self.lbl_detalle.config(text="\n".join(lineas))

    def reclasificar(self):
        if self.ultima_senal is not None:
            self._procesar(self.ultima_senal)

def iniciar_app():
    raiz = tk.Tk()
    try:
        clases, medias, desviaciones, palabra = cargar_modelo()
    except Exception as e:
        messagebox.showerror(
            "Modelo",
            f"No se pudo cargar el modelo:\n{e}\n\n"
            "Ejecuta primero:  python -m src.core.entrenamiento")
        raiz.destroy()
        return
    App(raiz, clases, medias, desviaciones, palabra)
    raiz.mainloop()

if __name__ == "__main__":
    iniciar_app()
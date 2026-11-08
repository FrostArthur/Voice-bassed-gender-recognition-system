import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sounddevice as sd
import os

# Importar los módulos previamente creados
from config import FS, DURACION_GRABACION, PALABRA, MODEL_PATH
from preprocesamiento import normalizar_audio
from banco_filtros import extraer_caracteristicas
from clasificador import clasificar_minima_distancia

class ReconocedorVozGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconocimiento Automático de Género")
        self.root.geometry("450x350")
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(False, False)

        # Verificar si el modelo existe antes de iniciar
        if not os.path.exists(MODEL_PATH):
            messagebox.showwarning(
                "Modelo no encontrado", 
                "No se encontró el modelo entrenado. Por favor, ejecuta 'entrenar.py' primero."
            )

        self.crear_widgets()

    def crear_widgets(self):
        # Título
        titulo = tk.Label(
            self.root, 
            text="Sistema de Reconocimiento de Género", 
            font=("Helvetica", 14, "bold"), 
            bg="#f0f4f8", 
            fg="#333"
        )
        titulo.pack(pady=20)

        # Instrucciones
        instrucciones = tk.Label(
            self.root, 
            text=f"Presiona el botón y di la palabra: '{PALABRA.upper()}'", 
            font=("Helvetica", 11), 
            bg="#f0f4f8"
        )
        instrucciones.pack(pady=10)

        # Estado de la grabación
        self.lbl_estado = tk.Label(
            self.root, 
            text="Estado: Esperando...", 
            font=("Helvetica", 10, "italic"), 
            bg="#f0f4f8", 
            fg="#666"
        )
        self.lbl_estado.pack(pady=10)

        # Botón de grabación
        self.btn_grabar = tk.Button(
            self.root, 
            text="🎤 Iniciar Grabación", 
            font=("Helvetica", 12, "bold"), 
            bg="#4CAF50", 
            fg="white", 
            activebackground="#45a049",
            activeforeground="white",
            relief="raised",
            padx=20,
            pady=10,
            command=self.iniciar_grabacion_thread
        )
        self.btn_grabar.pack(pady=20)

        # Resultado
        self.lbl_resultado = tk.Label(
            self.root, 
            text="-", 
            font=("Helvetica", 18, "bold"), 
            bg="#f0f4f8", 
            fg="#1f77b4"
        )
        self.lbl_resultado.pack(pady=20)

    def iniciar_grabacion_thread(self):
        # Deshabilitar botón durante la grabación
        self.btn_grabar.config(state=tk.DISABLED, bg="#cccccc")
        self.lbl_resultado.config(text="-")
        
        # Iniciar un hilo separado para no congelar la interfaz gráfica
        hilo = threading.Thread(target=self.proceso_grabacion_reconocimiento)
        hilo.start()

    def proceso_grabacion_reconocimiento(self):
        try:
            # 1. Captura en tiempo real
            self.lbl_estado.config(text=f"Grabando ({DURACION_GRABACION}s)... ¡Habla ahora!", fg="#d9534f")
            grabacion = sd.rec(int(DURACION_GRABACION * FS), samplerate=FS, channels=1, dtype='float32')
            sd.wait() # Esperar a que termine la captura del micrófono
            
            # 2. Procesamiento
            self.lbl_estado.config(text="Procesando señal...", fg="#f0ad4e")
            audio_signal = grabacion.flatten()
            audio_signal = normalizar_audio(audio_signal)
            
            # 3. Extracción de energía promedio y desviación en las subbandas
            caracteristicas = extraer_caracteristicas(audio_signal)
            
            # 4. Clasificación
            genero, distancia = clasificar_minima_distancia(caracteristicas, MODEL_PATH)
            
            # 5. Mostrar Resultado
            color = "#007acc" if genero == "hombre" else "#d81b60"
            self.lbl_resultado.config(text=f"VOZ DE {genero.upper()}", fg=color)
            self.lbl_estado.config(text=f"Completado. (Distancia: {distancia:.2f})", fg="#5cb85c")

        except Exception as e:
            self.lbl_estado.config(text="Error en el procesamiento.", fg="red")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
            
        finally:
            # Reactivar botón
            self.btn_grabar.config(state=tk.NORMAL, bg="#4CAF50")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReconocedorVozGUI(root)
    root.mainloop()
"""Parámetros compartidos por la descarga, el entrenamiento y el tiempo real.

También lo usa descargar_voces.py (FS, N y RUTA_GRABACIONES).
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

# ----------------------------- señal -----------------------------
FS = 44100                 # MSWC es de 16 kHz; la voz casi no pasa de 8 kHz
DURACION = 2               # segundos: igual que el proyecto de aves
N = FS * DURACION          # muestras por audio (FFT de N puntos, 0,5 Hz por bin)

# ----------------------------- datos -----------------------------
PALABRA = "trabajo"        # debe coincidir con --palabra de descargar_voces.py
CLASES = ("hombre", "mujer")
RUTA_GRABACIONES = str(RAIZ / "data" / "grabaciones")   # data/ está en .gitignore
RUTA_MODELO = RAIZ / "models" / "modelo_genero.json"

# ----------------------------- banco de filtros -----------------------------
# Puntos de corte en Hz. 4 cortes -> 5 sub-bandas (el laboratorio permite 2 a 5).
#   0-150    : fundamental típica de voz masculina (85-155 Hz)
#   150-300  : fundamental típica de voz femenina (165-255 Hz)
#   300-1000 : primer formante
#   1000-3000: segundo y tercer formante
#   3000-8000: fricativas / brillo
CORTES_HZ = (150, 300, 600, 1200)

# ----------------------------- preprocesado -----------------------------
VENTANA_MM = 5             # filtro de media móvil (igual que el proyecto)
UMBRAL_COMPUERTA = 0.1     # tramas de 20 ms con RMS < 10 % del máximo se ponen en 0
NORMALIZAR_ENERGIAS = True # vector de energías relativo (suma 1): no depende del volumen
"""Parámetros compartidos por la descarga, el entrenamiento y el tiempo real."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

# ----------------------------- señal -----------------------------
FS = 44100                 # frecuencia de muestreo (Hz)
DURACION = 2               # segundos por audio
N = FS * DURACION          # 88200 muestras -> FFT de N puntos, 0,5 Hz por bin (k = 2f)

# ----------------------------- datos -----------------------------
PALABRA = "trabajo"        # palabra del comando de voz
CLASES = ("hombre", "mujer")
RUTA_GRABACIONES = str(RAIZ / "data" / "grabaciones")
RUTA_MODELO = RAIZ / "models" / "modelo_genero.json"

# ----------------------------- banco de filtros -----------------------------
# Puntos de corte en Hz, tomados de los cruces de los espectros promedio
# ||H(k)||m y ||M(k)||m. 4 cortes -> 5 sub-bandas (el laboratorio permite 2 a 5).
#   0-100    : debajo de la fundamental
#   100-171  : fundamental masculina (||H|| > ||M||)
#   171-250  : fundamental femenina  (||M|| > ||H||)
#   250-600  : primer formante
#   600-...  : resto del espectro (hasta k = N-1)
CORTES_HZ = (100, 171, 250, 600)

# ----------------------------- preprocesado -----------------------------
VENTANA_MM = 5             # orden M del filtro de media móvil (peine)

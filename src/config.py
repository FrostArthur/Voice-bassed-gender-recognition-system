import os

# Configuración general del sistema
FS = 44100              # Frecuencia de muestreo
PALABRA = "hola"        # Palabra seleccionada para el comando de voz
NUM_SUBBANDAS = 4       # Entre 2 y 5 subbandas requeridas
DURACION_GRABACION = 2  # Segundos de captura en tiempo real

# Cortes en Hz para las subbandas donde la voz difiere por género
BANDAS = [(50, 150), (150, 300), (300, 600), (600, 1200)]

# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_PATH = os.path.join(BASE_DIR, "models", "modelo_genero.json")
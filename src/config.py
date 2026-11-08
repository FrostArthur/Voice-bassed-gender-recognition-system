import os

# Configuración general del sistema
FS = 44100             
PALABRA = "pasabandas"       
NUM_SUBBANDAS = 4       
DURACION_GRABACION = 2  

BANDAS = [(50, 150), (150, 300), (300, 600), (600, 1200)]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_PATH = os.path.join(BASE_DIR, "models", "modelo_genero.json")
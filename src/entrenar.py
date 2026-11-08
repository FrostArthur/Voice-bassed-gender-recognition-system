import os
import glob
import json
import numpy as np
from scipy.io import wavfile
from config import DATA_DIR, MODEL_PATH
from preprocesamiento import normalizar_audio
from banco_filtros import extraer_caracteristicas

def entrenar_modelo():
    """
    Lee las grabaciones diversas, extrae características y guarda 
    los vectores promedio (centroides) en formato JSON legible.
    """
    clases = ['hombre', 'mujer']
    centroides = {}
    
    print("Iniciando extracción de características...")
    for clase in clases:
        ruta = os.path.join(DATA_DIR, clase, "*.wav")
        archivos = glob.glob(ruta)
        
        caracteristicas_clase = []
        
        for archivo in archivos:
            fs, audio = wavfile.read(archivo)
            audio = normalizar_audio(audio)
            feats = extraer_caracteristicas(audio)
            caracteristicas_clase.append(feats)
            
        if caracteristicas_clase:
            # Promedio de todas las grabaciones para crear el vector representativo (centroide)
            centroide = np.mean(caracteristicas_clase, axis=0).tolist()
            centroides[clase] = centroide
            print(f"[{clase}] Entrenado con {len(archivos)} audios.")
        else:
            print(f"ADVERTENCIA: No hay audios en {ruta}")
            centroides[clase] = [0.0] * 8 # Fallback
            
    # Guardar vectores en JSON (legible)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, 'w') as f:
        json.dump(centroides, f, indent=4)
        
    print(f"Modelo guardado exitosamente en: {MODEL_PATH}")

if __name__ == "__main__":
    entrenar_modelo()
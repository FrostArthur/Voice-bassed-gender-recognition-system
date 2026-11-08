import os
import glob
from scipy.io import wavfile
from config import DATA_DIR, MODEL_PATH
from preprocesamiento import normalizar_audio
from banco_filtros import extraer_caracteristicas
from clasificador import clasificar_minima_distancia

def evaluar_sistema():
    clases = ['hombre', 'mujer']
    aciertos = 0
    total = 0
    
    for clase in clases:
        archivos = glob.glob(os.path.join(DATA_DIR, clase, "*.wav"))
        for archivo in archivos:
            fs, audio = wavfile.read(archivo)
            audio = normalizar_audio(audio)
            caracteristicas = extraer_caracteristicas(audio)
            
            prediccion, _ = clasificar_minima_distancia(caracteristicas, MODEL_PATH)
            
            if prediccion == clase:
                aciertos += 1
            total += 1
            
    if total > 0:
        precision = (aciertos / total) * 100
        error = 100 - precision
        print(f"Total evaluados: {total}")
        print(f"Precisión: {precision:.2f}%")
        print(f"Margen de error: {error:.2f}%")
        
        if error <= 5.0:
            print("ÉXITO: Se cumple el margen de error máximo del 5%.")
        else:
            print("ADVERTENCIA: El margen de error supera el 5%. Se necesitan más grabaciones diversas.")
    else:
        print("No hay datos para evaluar.")

if __name__ == "__main__":
    evaluar_sistema()
import os
import glob
import numpy as np
from scipy.io import wavfile

def recortar_voz_activa(carpeta_origen, carpeta_destino, duracion_segundos=2):
    os.makedirs(carpeta_destino, exist_ok=True)
    archivos = glob.glob(os.path.join(carpeta_origen, "*.wav"))
    
    if not archivos:
        print(f"No se encontraron archivos .wav en {carpeta_origen}")
        return

    print(f"Procesando {len(archivos)} archivos de {carpeta_origen} con detección de voz...")
    
    for archivo in archivos:
        try:
            fs, audio = wavfile.read(archivo)
            muestras_requeridas = int(fs * duracion_segundos)
            
            if len(audio.shape) > 1:
                audio = audio[:, 0]
                
            max_amplitud = np.max(np.abs(audio))
            umbral = max_amplitud * 0.1 
            
            indices_activos = np.where(np.abs(audio) > umbral)[0]
            
            if len(indices_activos) > 0:
                inicio_voz = indices_activos[0] 
            else:
                inicio_voz = 0 # 
                
            fin_voz = inicio_voz + muestras_requeridas
            
            if fin_voz <= len(audio):
                audio_procesado = audio[inicio_voz:fin_voz]
            else:
                audio_recortado = audio[inicio_voz:]
                ceros_faltantes = np.zeros(muestras_requeridas - len(audio_recortado), dtype=audio.dtype)
                audio_procesado = np.concatenate((audio_recortado, ceros_faltantes))
                
            nombre_archivo = os.path.basename(archivo)
            ruta_guardado = os.path.join(carpeta_destino, nombre_archivo)
            wavfile.write(ruta_guardado, fs, audio_procesado)
            
        except Exception as e:
            print(f"Error procesando el archivo {archivo}: {e}")
            
    print(f"Audios guardados en: {carpeta_destino}\n")

if __name__ == "__main__":
    recortar_voz_activa("audios/hombre", "data/hombre", duracion_segundos=2)
    recortar_voz_activa("audios/mujer", "data/mujer", duracion_segundos=2)
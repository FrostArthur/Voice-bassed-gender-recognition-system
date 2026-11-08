import sounddevice as sd
from config import FS, DURACION_GRABACION, PALABRA, MODEL_PATH
from preprocesamiento import normalizar_audio
from banco_filtros import extraer_caracteristicas
from clasificador import clasificar_minima_distancia

def capturar_y_reconocer():
    print(f"\n--- Reconocimiento en Tiempo Real ---")
    print(f"Pronuncia la palabra '{PALABRA}'...")
    
    grabacion = sd.rec(int(DURACION_GRABACION * FS), samplerate=FS, channels=1, dtype='float32')
    sd.wait() 
    print("Grabación procesando...")
    
    audio_signal = grabacion.flatten()
    audio_signal = normalizar_audio(audio_signal)
    
    caracteristicas = extraer_caracteristicas(audio_signal)
    
    genero, distancia = clasificar_minima_distancia(caracteristicas, MODEL_PATH)
    
    print(f">>> GÉNERO DETECTADO: {genero.upper()} (Distancia: {distancia:.4f})")

if __name__ == "__main__":
    print("Sistema Automático de Reconocimiento de Género")
    while True:
        opcion = input("Presiona ENTER para hablar o 'q' para salir: ")
        if opcion.lower() == 'q':
            break
        capturar_y_reconocer()
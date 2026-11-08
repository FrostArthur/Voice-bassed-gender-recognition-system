import numpy as np
from scipy.signal import butter, lfilter
from config import BANDAS, FS

def apply_bandpass_filter(data, lowcut, highcut, fs, order=5):
    """Aplica un filtro pasa banda."""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

def extraer_caracteristicas(audio_signal):
    """
    Pasa la señal por el banco de filtros y calcula la energía promedio 
    y desviación promedio para cada subbanda.
    """
    features = []
    
    for low, high in BANDAS:
        # Filtrado de la subbanda
        senal_filtrada = apply_bandpass_filter(audio_signal, low, high, FS)
        
        # Cálculo de la energía
        energia = senal_filtrada ** 2
        
        # Estimación de la energía promedio y desviación promedio
        avg_energia = np.mean(energia)
        std_energia = np.std(energia)
        
        features.extend([avg_energia, std_energia])
        
    return features
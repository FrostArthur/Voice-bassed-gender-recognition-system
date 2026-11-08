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
    features = []
    
    for low, high in BANDAS:
        # Filtrado de la subbanda
        senal_filtrada = apply_bandpass_filter(audio_signal, low, high, FS)
        
        energia = senal_filtrada ** 2
        
        avg_energia = np.mean(energia)
        std_energia = np.std(energia)
        
        features.extend([avg_energia, std_energia])
        
    return features
import numpy as np
from scipy.signal import butter, sosfilt
from config import BANDAS, FS

def apply_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    
    sos = butter(order, [low, high], btype='band', output='sos')
    
    return sosfilt(sos, data)

def extraer_caracteristicas(audio_signal):
    features = []

    audio_signal = audio_signal + np.random.normal(0, 1e-10, len(audio_signal))
    
    for low, high in BANDAS:
        senal_filtrada = apply_bandpass_filter(audio_signal, low, high, FS)
        
        energia = senal_filtrada ** 2
        
        avg_energia = np.mean(energia)
        std_energia = np.std(energia)
        
        if np.isnan(avg_energia): avg_energia = 0.0
        if np.isnan(std_energia): std_energia = 0.0
            
        features.extend([avg_energia, std_energia])
        
    return features
import numpy as np

def normalizar_audio(audio):
    """
    Convierte a mono si es estéreo y normaliza la amplitud.
    """
    if len(audio.shape) > 1:
        audio = audio[:, 0]
    
    # Prevenir división por cero
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val
        
    return audio
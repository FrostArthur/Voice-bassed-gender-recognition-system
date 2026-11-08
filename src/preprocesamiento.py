import numpy as np

def normalizar_audio(audio):
    if len(audio.shape) > 1:
        audio = audio[:, 0]
    
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val
        
    return audio
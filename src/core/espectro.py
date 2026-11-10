import numpy as np

import config

N_PUNTOS = config.N
FS = config.FS

def calcularEspectro(audio):
    assert len(audio) == N_PUNTOS, f"El audio debe tener {N_PUNTOS} muestras ({config.DURACION} s)"
    return np.abs(np.fft.fft(audio))
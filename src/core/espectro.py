import numpy as np

import config

N_PUNTOS = config.N
FS = config.FS


# Espectro de un audio: ||X(k)|| = |FFT de N puntos|
def calcularEspectro(audio):
    assert len(audio) == N_PUNTOS, f"El audio debe tener {N_PUNTOS} muestras ({config.DURACION} s)"
    return np.abs(np.fft.fft(audio))


# Espectro promedio de una clase: ||X(k)||m = (1/R) * sum_r ||X_r(k)||
def EspectroPromedio(lista_audios):
    return np.mean([calcularEspectro(audio) for audio in lista_audios], axis=0)

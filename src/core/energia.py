import numpy as np

import config

N_PUNTOS = config.N
FS = config.FS

# Bin de cada corte: k = f * N / fs  (con N = 88200 y fs = 44100, k = 2f)
PUNTOS_CORTE = [int(round(f * N_PUNTOS / FS)) for f in config.CORTES_HZ]
LIMITES = [0, *PUNTOS_CORTE, N_PUNTOS // 2]          # el espectro completo, k = 0 ... N-1
N_BANDAS = len(LIMITES) - 1

assert 2 <= N_BANDAS <= 5, "El laboratorio exige entre 2 y 5 sub-bandas"
assert all(a < b for a, b in zip(LIMITES[:-1], LIMITES[1:])), "Cortes fuera de orden"


# Vector de la sub-banda b (bins k_b ... k_{b+1}-1, N_b = k_{b+1} - k_b bins):
#   energía promedio            E_b = (1/N_b) * sum ||X(k)||^2
#   desviación promedio energías D_b = (1/N_b) * sum | ||X(k)||^2 - E_b |
def obtenerVectorEnergias(espectro):
    energias, desviaciones = [], []
    for a, b in zip(LIMITES[:-1], LIMITES[1:]):
        potencia = espectro[a:b] ** 2
        e = np.mean(potencia)
        energias.append(e)
        desviaciones.append(np.mean(np.abs(potencia - e)))
    return np.array(energias + desviaciones)     # [E_1..E_B, D_1..D_B]

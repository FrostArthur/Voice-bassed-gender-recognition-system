import numpy as np

import config

N_PUNTOS = config.N
FS = config.FS

PUNTOS_CORTE = [int(round(f * N_PUNTOS / FS)) for f in config.CORTES_HZ]
LIMITES = [0, *PUNTOS_CORTE, N_PUNTOS // 2]     
N_BANDAS = len(LIMITES) - 1

assert 2 <= N_BANDAS <= 5, "El laboratorio exige entre 2 y 5 sub-bandas"
assert all(a < b for a, b in zip(LIMITES[:-1], LIMITES[1:])), "Cortes fuera de orden"

def obtenerVectorEnergias(espectro):
    energias = np.array([np.mean(espectro[a:b] ** 2)
                         for a, b in zip(LIMITES[:-1], LIMITES[1:])])
    if config.NORMALIZAR_ENERGIAS:
        total = energias.sum()
        if total > 0:
            energias = energias / total
    return energias
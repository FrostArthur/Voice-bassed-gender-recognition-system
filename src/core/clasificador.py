import numpy as np

from src.core.entrenamiento import vector_de_audio
from src.core.espectro import N_PUNTOS

METRICAS = {
    "Euclidiana": lambda medias, desv, v: np.linalg.norm(medias - v, axis=1),
    "Resta absoluta": lambda medias, desv, v: np.abs(medias - v).sum(axis=1),
    "Euclidiana ponderada (σ)": lambda medias, desv, v:
        np.linalg.norm((medias - v) / np.maximum(desv, 1e-9), axis=1),
}


def analizar(senal, clases, medias, desviaciones, metrica="Euclidiana"):
    senal = np.asarray(senal, dtype=np.float64)
    if senal.ndim == 2:
        senal = senal.mean(axis=1)
    if len(senal) != N_PUNTOS:
        raise ValueError(f"La señal debe tener {N_PUNTOS} muestras, tiene {len(senal)}")

    vector = vector_de_audio(senal)
    distancias = METRICAS[metrica](medias, desviaciones, vector)
    return {
        "clase": clases[int(np.argmin(distancias))],
        "distancias": distancias,
        "vector": vector,
    }
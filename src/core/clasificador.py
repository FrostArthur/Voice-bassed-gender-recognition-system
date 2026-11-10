"""Clasificador por mínima distancia (fase de tiempo real)."""
import numpy as np

from src.core.energia import obtenerVectorEnergias
from src.core.entrenamiento import preprocesar
from src.core.espectro import N_PUNTOS, calcularEspectro

# Distancias entre el vector de la captura y el de cada clase
METRICAS = {
    "Resta absoluta": lambda vectores, v: np.abs(vectores - v).sum(axis=1),
    "Euclidiana": lambda vectores, v: np.linalg.norm(vectores - v, axis=1),
}


def analizar(senal, clases, vectores, metrica="Resta absoluta"):
    senal = np.asarray(senal, dtype=np.float64)
    if senal.ndim == 2:
        senal = senal.mean(axis=1)
    if len(senal) != N_PUNTOS:
        raise ValueError(f"La señal debe tener {N_PUNTOS} muestras, tiene {len(senal)}")

    vector = obtenerVectorEnergias(calcularEspectro(preprocesar(senal)))
    distancias = METRICAS[metrica](vectores, vector)
    return {
        "clase": clases[int(np.argmin(distancias))],     # c = argmin d(E_x, E_c)
        "distancias": distancias,
        "vector": vector,
    }

"""Fase de entrenamiento: genera models/modelo_genero.json

Ejecutar desde la raíz del proyecto:
    python -m src.core.entrenamiento
"""
import json
from pathlib import Path

import numpy as np
import soundfile as sf

import config
from src.core.energia import LIMITES, N_BANDAS, PUNTOS_CORTE, obtenerVectorEnergias
from src.core.espectro import FS, N_PUNTOS, EspectroPromedio, calcularEspectro
from src.scripts.filtro_media_movil import aplicar_filtro_media_movil


# MISMO preprocesado para entrenamiento y tiempo real:
# mono -> normalizar por el pico -> media móvil
def preprocesar(audio):
    audio = np.asarray(audio, dtype=np.float64)
    if audio.ndim == 2:
        audio = audio.mean(axis=1)
    pico = np.max(np.abs(audio))
    if pico > 0:
        audio = audio / pico
    return aplicar_filtro_media_movil(audio, config.VENTANA_MM)


def cargar_audios(clase):
    archivos = sorted((Path(config.RUTA_GRABACIONES) / clase).glob("*.wav"))
    if not archivos:
        raise FileNotFoundError(
            f"No hay WAV en {Path(config.RUTA_GRABACIONES) / clase}. "
            "Ejecuta primero descargar_voces.py")
    audios = []
    for archivo in archivos:
        audio, fs = sf.read(archivo)
        if fs != FS:
            raise ValueError(f"{archivo.name}: fs={fs} Hz, se esperaba {FS} Hz")
        if audio.ndim == 2:
            audio = audio.mean(axis=1)
        if len(audio) < N_PUNTOS:
            audio = np.pad(audio, (0, N_PUNTOS - len(audio)))
        audios.append(preprocesar(audio[:N_PUNTOS]))
    return audios


# Por cada clase: espectro promedio ||X(k)||m -> vector de energías por sub-banda
def entrenar():
    vectores, conteos = [], []
    for clase in config.CLASES:
        audios = cargar_audios(clase)
        vector = obtenerVectorEnergias(EspectroPromedio(audios))
        vectores.append(vector)
        conteos.append(len(audios))
        print(f"{clase}: {len(audios)} audios")
        print(f"   energía promedio      : {np.round(vector[:N_BANDAS], 4)}")
        print(f"   desviación promedio   : {np.round(vector[N_BANDAS:], 4)}")
    guardar_modelo(vectores, conteos)


def guardar_modelo(vectores, conteos):
    config.RUTA_MODELO.parent.mkdir(parents=True, exist_ok=True)
    modelo = {
        "palabra": config.PALABRA,
        "fs": FS,
        "n_puntos": N_PUNTOS,
        "ventana_media_movil": config.VENTANA_MM,
        "subbandas": [
            {
                "banda": i + 1,
                "bin_inicio": a,
                "bin_fin": b,
                "hz_inicio": a * FS / N_PUNTOS,
                "hz_fin": b * FS / N_PUNTOS,
            }
            for i, (a, b) in enumerate(zip(LIMITES[:-1], LIMITES[1:]))
        ],
        "puntos_corte": list(PUNTOS_CORTE),
        "n_audios": {c: n for c, n in zip(config.CLASES, conteos)},
        "energia_promedio": {c: [float(x) for x in v[:N_BANDAS]]
                             for c, v in zip(config.CLASES, vectores)},
        "desviacion_promedio": {c: [float(x) for x in v[N_BANDAS:]]
                                for c, v in zip(config.CLASES, vectores)},
    }
    with open(config.RUTA_MODELO, "w", encoding="utf-8") as f:
        json.dump(modelo, f, indent=2, ensure_ascii=False)
    print(f"Modelo guardado en {config.RUTA_MODELO}")


# ----------------------------- Tiempo real -----------------------------
def cargar_modelo(ruta=config.RUTA_MODELO):
    with open(ruta, encoding="utf-8") as f:
        d = json.load(f)
    if d["fs"] != FS or d["n_puntos"] != N_PUNTOS:
        raise ValueError("El modelo se entrenó con otra fs o longitud de señal")
    if tuple(d["puntos_corte"]) != tuple(PUNTOS_CORTE):
        raise ValueError("Los puntos de corte del modelo no coinciden con config.py")
    clases = list(d["energia_promedio"].keys())
    vectores = np.array([d["energia_promedio"][c] + d["desviacion_promedio"][c]
                         for c in clases])
    return clases, vectores, d.get("palabra", config.PALABRA)


if __name__ == "__main__":
    entrenar()

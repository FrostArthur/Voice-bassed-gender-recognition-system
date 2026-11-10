import json
from pathlib import Path

import numpy as np
import soundfile as sf

import config
from src.core.energia import LIMITES, PUNTOS_CORTE, N_BANDAS, obtenerVectorEnergias
from src.core.espectro import FS, N_PUNTOS, calcularEspectro
from src.scripts.filtro_media_movil import aplicar_filtro_media_movil


def _compuerta(audio):
    largo = int(0.02 * FS)
    n_tramas = len(audio) // largo
    if n_tramas == 0:
        return audio
    tramas = audio[:n_tramas * largo].reshape(n_tramas, largo)
    rms = np.sqrt(np.mean(tramas ** 2, axis=1))
    if rms.max() == 0:
        return audio
    activa = rms >= config.UMBRAL_COMPUERTA * rms.max()
    mascara = np.repeat(activa, largo)
    salida = audio.copy()
    salida[:n_tramas * largo][~mascara] = 0.0
    return salida


def preprocesar(audio):
    audio = np.asarray(audio, dtype=np.float64)
    if audio.ndim == 2:
        audio = audio.mean(axis=1)
    audio = audio - audio.mean()
    audio = _compuerta(audio)
    pico = np.max(np.abs(audio))
    if pico > 0:
        audio = audio / pico
    return aplicar_filtro_media_movil(audio, config.VENTANA_MM)


def vector_de_audio(audio):
    return obtenerVectorEnergias(calcularEspectro(preprocesar(audio)))


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
        audios.append(audio[:N_PUNTOS])
    return audios


def entrenar():
    medias, desviaciones, conteos = [], [], []
    for clase in config.CLASES:
        audios = cargar_audios(clase)
        vectores = np.array([vector_de_audio(a) for a in audios])   
        media = vectores.mean(axis=0)
        desv = vectores.std(axis=0)
        medias.append(media)
        desviaciones.append(desv)
        conteos.append(len(audios))
        print(f"{clase}: {len(audios)} audios")
        print(f"   energía promedio : {np.round(media, 4)}")
        print(f"   desviación       : {np.round(desv, 4)}")
    guardar_modelo(medias, desviaciones, conteos)


def guardar_modelo(medias, desviaciones, conteos):
    config.RUTA_MODELO.parent.mkdir(parents=True, exist_ok=True)
    modelo = {
        "palabra": config.PALABRA,
        "fs": FS,
        "n_puntos": N_PUNTOS,
        "ventana_media_movil": config.VENTANA_MM,
        "normalizar_energias": config.NORMALIZAR_ENERGIAS,
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
        "energia_promedio": {c: [float(e) for e in v] for c, v in zip(config.CLASES, medias)},
        "desviacion_energia": {c: [float(e) for e in v] for c, v in zip(config.CLASES, desviaciones)},
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
    if d["normalizar_energias"] != config.NORMALIZAR_ENERGIAS:
        raise ValueError("El modelo se entrenó con otra opción NORMALIZAR_ENERGIAS")
    clases = list(d["energia_promedio"].keys())
    medias = np.array([d["energia_promedio"][c] for c in clases])
    desviaciones = np.array([d["desviacion_energia"][c] for c in clases])
    return clases, medias, desviaciones, d.get("palabra", config.PALABRA)


if __name__ == "__main__":
    entrenar()
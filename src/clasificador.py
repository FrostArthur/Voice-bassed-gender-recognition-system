import numpy as np
import json

def calcular_distancia_euclidiana(vec1, vec2):
    return np.linalg.norm(np.array(vec1) - np.array(vec2))

def clasificar_minima_distancia(caracteristicas, modelo_path):
    with open(modelo_path, 'r') as f:
        modelo = json.load(f)
        
    dist_hombre = calcular_distancia_euclidiana(caracteristicas, modelo["hombre"])
    dist_mujer = calcular_distancia_euclidiana(caracteristicas, modelo["mujer"])
    
    if dist_hombre < dist_mujer:
        return "hombre", dist_hombre
    else:
        return "mujer", dist_mujer
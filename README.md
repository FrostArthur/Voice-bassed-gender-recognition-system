# Reconocimiento de género por voz mediante banco de filtros
## 1. Descripción
Sistema desarrollado en **Python** que reconoce el **género del hablante (voz de hombre / voz de mujer)** a partir de un **comando de voz** (una palabra previamente seleccionada), con un **margen de error máximo del 5 %**.
 
La clasificación se basa en la técnica de **análisis por banco de filtros**: el espectro de la señal se divide en subbandas y, para cada una, se calculan estadísticos de energía que forman un vector característico. Este vector se compara contra los vectores de referencia de cada clase obtenidos en la fase de entrenamiento.
 
El sistema opera en dos fases:
 
1. **Entrenamiento (offline):** a partir de un banco de grabaciones diverso se calculan los vectores característicos de cada clase y se guardan en un modelo.
2. **Reconocimiento en tiempo real:** con el micrófono activado se captura el comando de voz, se extrae su vector característico y se clasifica el género.

## 2. Requisitos
| Requisito | Cómo se cumple |
|---|---|
| Lenguaje Python o Matlab | Python |
| Clases: voz hombre y voz mujer | `hombre`, `mujer` |
| Palabra seleccionada como comando | `PALABRA = "..."` _(completar)_ |
| Error máximo del 5 % | Evaluado sobre un conjunto de prueba (ver sección 7) |
| Banco de filtros con 2 a 5 subbandas | `N_SUBBANDAS = ...` _(completar, entre 2 y 5)_ |
| Por subbanda: energía promedio y desviación promedio de energías | Vector de características de 2·N valores |
| Captura en tiempo real con micrófono | `src/app.py` |
| Fuentes muy diversas (diferentes personas) | Banco de grabaciones de múltiples hablantes (ver sección 5) |
 
## 3. Metodología
 
1. **Adquisición:** grabaciones de la palabra seleccionada, a frecuencia de muestreo `fs` fija _(ej. 44100 Hz)_ y duración uniforme.
2. **Preprocesamiento:** conversión a mono, normalización de amplitud, recorte de silencios y, si se requiere, filtro de suavizado (media móvil).
3. **Análisis espectral:** FFT de cada grabación y espectro promedio por clase.
4. **Definición de subbandas:** a partir de los espectros promedio de hombre y mujer se eligen los puntos de corte del banco de filtros (mínimo 2, máximo 5 subbandas).
5. **Vector de características:** para cada subbanda _k_ se calculan
   - la **energía promedio** `E_k`
   - la **desviación promedio de energías** `σ_k`
   obteniendo el vector `[E_1, σ_1, E_2, σ_2, ..., E_N, σ_N]`.
6. **Modelo por clase:** promedio de los vectores de todas las grabaciones de cada clase.
7. **Clasificación:** mínima distancia (euclidiana o diferencia absoluta) entre el vector de la señal capturada y los vectores de `hombre` y `mujer`.
## 4. Estructura del repositorio
 
```
.
├── README.md
├── requirements.txt
├── .gitignore
├── data/                  # Grabaciones (NO se sube al repositorio)
│   ├── hombre/
│   └── mujer/
├── models/
│   └── modelo_genero.json # Vectores de energía por clase (legible)
├── src/
│   ├── config.py          # fs, palabra, número de subbandas, cortes
│   ├── preprocesamiento.py
│   ├── banco_filtros.py   # Subbandas, energía y desviación promedio
│   ├── entrenar.py        # Fase de entrenamiento
│   ├── evaluar.py         # Cálculo del error sobre el conjunto de prueba
│   ├── clasificador.py    # Clasificación por mínima distancia
│   └── app.py             # Reconocimiento en tiempo real (micrófono)
├── docs/
│   └── informe.pdf
└── figuras/               # Espectros promedio, subbandas, matriz de confusión
```
 
> Ajusta los nombres de archivos a lo que realmente tenga el repositorio.
 
## 5. Banco de grabaciones
 
Para que el sistema generalice, las grabaciones deben provenir de **muchas personas distintas** (diferentes edades, timbres y entornos de grabación), con una cantidad equilibrada entre hombres y mujeres.
 
- **Palabra grabada:** _(completar)_
- **Número de hablantes:** _(completar)_ hombres y _(completar)_ mujeres
- **Grabaciones por clase:** _(completar)_
- **Formato:** `.wav`, mono, `fs` = _(completar)_ Hz
- **Fuentes:** compañeros, familiares, conocidos y/o bases de datos públicas de voz _(completar)_
La carpeta `data/` está en `.gitignore`; cada integrante debe contar con las grabaciones localmente (o descargarlas desde _enlace a la carpeta compartida_).
 
Separar los hablantes entre **entrenamiento** y **prueba** (una persona no debe aparecer en ambos conjuntos) para que el cálculo del error sea honesto.
 
## 6. Instalación y uso
 
### Instalación
 
```bash
git clone <url-del-repositorio>
cd <nombre-del-repositorio>
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
 
Dependencias sugeridas (`requirements.txt`):
 
```
numpy
scipy
matplotlib
sounddevice
soundfile
```
 
### Orden de ejecución
 
1. **Colocar las grabaciones** en `data/hombre/` y `data/mujer/`.
2. **Entrenar el modelo:**
```bash
   python src/entrenar.py
```
   Genera `models/modelo_genero.json` y las gráficas de espectros promedio y subbandas.
3. **Evaluar el error:**
```bash
   python src/evaluar.py
```
   Debe reportar un error **≤ 5 %** sobre el conjunto de prueba.
4. **Ejecutar el reconocimiento en tiempo real:**
```bash
   python src/app.py
```
   Con el micrófono activado, pronunciar la palabra seleccionada; el sistema mostrará el género reconocido.

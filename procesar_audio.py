import librosa
import numpy as np

# Cargar la señal de audio
audio_path = 'prueba.wav'
y, sr = librosa.load(audio_path)

# Calcular autocorrelación
def autocorrelation(signal):
    result = np.correlate(signal, signal, mode='full')
    return result[result.size // 2:]

# Calcular los valores requeridos
def calculate_correlation_features(y, sr):
    frame_length = int(0.03 * sr)  # 30ms por frame
    hop_length = int(0.01 * sr)    # Desplazamiento de 10ms
    frames = librosa.util.frame(y, frame_length=frame_length, hop_length=hop_length).T
    r0_values, r1norm_values, rmaxnorm_values = [], [], []

    for frame in frames:
        r = autocorrelation(frame)
        r0 = r[0]
        if r0 == 0:  # Evitar división por cero
            r0_values.append(0)
            r1norm_values.append(0)
            rmaxnorm_values.append(0)
            continue

        # Calcular r0, r1norm y rmaxnorm
        r1norm = r[1] / r0
        secondary_max = np.argmax(r[1:]) + 1  # Máximo secundario
        rmaxnorm = r[secondary_max] / r0

        r0_values.append(r0)
        r1norm_values.append(r1norm)
        rmaxnorm_values.append(rmaxnorm)

    return r0_values, r1norm_values, rmaxnorm_values

# Calcular características
r0, r1norm, rmaxnorm = calculate_correlation_features(y, sr)

# Guardar los resultados en archivos separados
output_files = {
    "r0.txt": r0,
    "r1norm.txt": r1norm,
    "rmaxnorm.txt": rmaxnorm
}

# Guardar en archivos
for filename, data in output_files.items():
    with open(filename, 'w') as f:
        f.write("\n".join(map(str, data)) + "\n")
    print(f"Resultados guardados en {filename}")

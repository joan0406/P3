import numpy as np
import matplotlib.pyplot as plt
import wave

# Archivo del segmento de audio
fitxer_audio = "segmento.wav"

# Abrimos el archivo de audio
with wave.open(fitxer_audio, 'rb') as fitxer_wav:
    n_frames = fitxer_wav.getnframes()
    frame_rate = fitxer_wav.getframerate()  # Frecuencia de muestreo
    datos_audio = fitxer_wav.readframes(n_frames)
    senyal_audio = np.frombuffer(datos_audio, dtype=np.int16)

# Eje temporal
temps = np.linspace(0, n_frames / frame_rate, num=n_frames)

# Autocorrelación para detectar el período de pitch
auto_corr = np.correlate(senyal_audio, senyal_audio, mode='full')
auto_corr = auto_corr[len(auto_corr) // 2:]  # Segunda mitad (simétrica)
peak_idx = np.argmax(auto_corr[1:]) + 1  # Ignoramos el primer máximo en cero
pitch_period = peak_idx / frame_rate  # Convertimos el índice a tiempo (s)

# Gráficos
plt.figure(figsize=(12, 6))

# Subplot 1: Señal temporal
plt.subplot(2, 1, 1)
plt.plot(temps, senyal_audio, label="Señal Temporal", color="blue")
plt.axvline(x=pitch_period, color='red', linestyle='--',
            label=f"Período Pitch: {pitch_period * 1000:.2f} ms")
plt.title("Señal Temporal y Período de Pitch")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.legend()
plt.grid()

# Subplot 2: Autocorrelación
plt.subplot(2, 1, 2)
lags = np.arange(len(auto_corr)) / frame_rate
plt.plot(lags, auto_corr, label="Autocorrelación", color="orange")
plt.axvline(x=pitch_period, color='red', linestyle='--',
            label=f"Primer Máximo Secundario: {pitch_period * 1000:.2f} ms")
plt.title("Autocorrelación de la Señal")
plt.xlabel("Retraso (s)")
plt.ylabel("Autocorrelación")
plt.legend()
plt.grid()

# Ajustar diseño y mostrar
plt.tight_layout()
plt.savefig("segment_autoco_plot.png")
plt.show()
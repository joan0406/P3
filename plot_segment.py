import numpy as np
import matplotlib.pyplot as plt
import wave

# Archivo del segmento de audio
audio_file = "segmento.wav"

# Abrimos el archivo de audio
with wave.open(audio_file, 'rb') as wav_file:
    n_frames = wav_file.getnframes()
    frame_rate = wav_file.getframerate()
    audio_data = wav_file.readframes(n_frames)
    audio_signal = np.frombuffer(audio_data, dtype=np.int16)

# Normalizar la señal para su análisis
audio_signal = audio_signal / np.max(np.abs(audio_signal))

# Eje temporal
time = np.linspace(0, n_frames / frame_rate, num=n_frames)

# Autocorrelación usando numpy.correlate()
auto_corr = np.correlate(audio_signal, audio_signal, mode='full')
auto_corr = auto_corr[len(auto_corr) // 2:]  # Solo parte positiva
auto_corr_norm = auto_corr / np.max(auto_corr)  # Normalización

# Detectar el primer máximo después del origen
origin = 0
while auto_corr_norm[origin] == np.max(auto_corr_norm):
    origin += 1

# Detectar el primer máximo
first_peak_idx = origin + np.argmax(auto_corr_norm[origin:])

# Detectar el segundo máximo después del primer pico
second_peak_idx = first_peak_idx + np.argmax(auto_corr_norm[first_peak_idx + 1:])

# Convertimos índice a tiempo para el segundo pico
pitch_period_2 = second_peak_idx / frame_rate  # Convertimos índice a tiempo

# Graficar señal y autocorrelación
plt.figure(figsize=(14, 7))

# Señal temporal
plt.subplot(2, 1, 1)
plt.plot(time, audio_signal, label="Señal Temporal", color="blue")
plt.title("Señal Temporal")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid()

# Autocorrelación
plt.subplot(2, 1, 2)
lags = np.arange(0, len(auto_corr_norm)) / frame_rate
plt.plot(lags, auto_corr_norm, label="Autocorrelación", color="green")
plt.axvline(x=pitch_period_2, color='orange', linestyle='--', label=f"Segundo Pico: {pitch_period_2*1000:.2f} ms")
plt.title("Autocorrelación de la Señal")
plt.xlabel("Desplazamiento (s)")
plt.ylabel("Amplitud Normalizada")
plt.legend()
plt.grid()

# Ajustar diseño y guardar
plt.tight_layout()
plt.savefig("autocorrelation_with_second_peak_corrected.png")
plt.show()
import numpy as np
import matplotlib.pyplot as plt

# Carga los datos exportados
signal = np.loadtxt('signal_data.txt')
autocorr = np.loadtxt('autocorrelation_data.txt')

# Configuración del tiempo (asumiendo 30 ms y frecuencia de muestreo de 16 kHz)
sampling_freq = 16000  # Ajusta según tu configuración
time = np.linspace(0, 30e-3, int(30e-3 * sampling_freq))  # Primeros 30 ms

# Crea los subplots
plt.figure(figsize=(10, 6))

# Señal temporal
plt.subplot(2, 1, 1)
plt.plot(time, signal[:len(time)], label='Señal temporal')
plt.axvline(x=time[np.argmax(autocorr[1:]) + 1], color='r', linestyle='--', label='Periodo Pitch')
plt.title("Señal Temporal")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.legend()
plt.grid()

# Autocorrelación
plt.subplot(2, 1, 2)
plt.plot(autocorr, label='Autocorrelación')
plt.axvline(x=np.argmax(autocorr[1:]) + 1, color='r', linestyle='--', label='Primer Máximo Secundario')
plt.title("Autocorrelación")
plt.xlabel("Lag")
plt.ylabel("Amplitud")
plt.legend()
plt.grid()

# Muestra la gráfica
plt.tight_layout()
plt.show()
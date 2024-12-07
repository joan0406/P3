import wave
import numpy as np

# Abrir el archivo de audio
input_file = "prueba.wav"
output_file = "segmento.wav"

# Definir el inicio y duración en segundos
start_time = 2.375  # Segundo donde empieza el segmento
duration = 0.03     # Duración del segmento en segundos (30 ms)

with wave.open(input_file, 'rb') as wav_file:
    # Obtener parámetros del archivo
    n_channels = wav_file.getnchannels()
    sample_width = wav_file.getsampwidth()
    frame_rate = wav_file.getframerate()
    n_frames = wav_file.getnframes()

    print(f"Frame rate: {frame_rate} Hz, Total frames: {n_frames}")

    # Calcular el inicio y el número de frames a leer
    start_frame = int(start_time * frame_rate)
    num_frames = int(duration * frame_rate)

    # Posicionarse en el inicio del segmento
    wav_file.setpos(start_frame)

    # Leer el segmento de audio
    frames = wav_file.readframes(num_frames)

# Guardar el segmento en un nuevo archivo
with wave.open(output_file, 'wb') as segment:
    segment.setnchannels(n_channels)
    segment.setsampwidth(sample_width)
    segment.setframerate(frame_rate)
    segment.writeframes(frames)

print(f"Segmento de {duration} segundos guardado en {output_file}")
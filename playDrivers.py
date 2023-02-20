# reproductor simple co eleccion de driver de salida

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs


devs = sd.query_devices()
print("\n",devs)

dev = int(input("Device: "))
sd.default.device = dev

print("\n\nUsing output: ",devs[sd.default.device[0]]['name'])

# abrimos wav y recogemos frecMuestreo (SRATE) y el array de muestras
data, SRATE = sf.read('ex1.wav')


# informacion de wav
print("\n\nOriginal wav ",SRATE)
print("  Sample rate ",SRATE)
print("  Sample format: ",data.dtype)
print("  Num channels: ",len(data.shape))
print("  Len: ",data.shape[0])



# bajamos volumen
data = data * 0.5

# a reproducir!
sd.play(data, SRATE)

# bloqueamos la ejecución para dejar que suene
sd.wait()

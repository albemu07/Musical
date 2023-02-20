# Grabacion de un archivo de audio 'q' para terminar

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
SRATE = 44100


# abrimos stream de entrada (InpuStream)
stream = sd.InputStream(samplerate=SRATE, blocksize=CHUNK, dtype="float32", channels=1)

# arrancamos stream
stream.start()


print("* grabando")
print("* pulsa q para termninar")

# buffer para acumular grabación.
# (0,1): con un canal (1), vacio (de tamaño 0)
buffer = np.empty((0, 1), dtype="float32")

# bucle de grabación
kb = kbhit.KBHit()
c = ' '
while c != 'q': 
    bloque, _check = stream.read(CHUNK)  # recogida de samples en array numpy    
    # read devuelve un par (samples,bool)
    buffer = np.append(buffer,bloque) # en bloque[0] están los samples
    if kb.kbhit(): c = kb.getch()

stream.stop() 
print("* grabacion terminada")

print('Quieres reproducir [S/n]? ',end='')
# bloqueamos ejecucion para recoger respuesta
while not kb.kbhit(): 
    True

# reproducción del buffer adquirido
c = kb.getch()
if c!='n':
    sd.play(buffer, SRATE)
    sd.wait()

# volcado a un archivo wav, utilizando la librería soundfile 
sf.write("rec.wav", buffer, SRATE)

stream.stop()
stream.close()
kb.set_normal_term()


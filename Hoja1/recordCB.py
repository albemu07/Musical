# basic/record0.py Grabacion de un archivo de audio 'q' para terminar
import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
CHANNELS = 1
SRATE = 44100


# buffer para acumular grabación.
# (0,1): con un canal (1), vacio (de tamaño 0)
buffer = np.empty((0, 1), dtype="float32")
def callback(indata, frames, time, status):
    global buffer
    buffer = np.append(buffer,indata)



# stream de entrada con callBack
stream = sd.InputStream(
    samplerate=SRATE, dtype="float32",
    channels=CHANNELS,
    blocksize=CHUNK, 
    callback=callback)


# arrancamos stream
stream.start()


print("* grabando")
print("* pulsa q para termninar")

# bucle para grabacion 
kb = kbhit.KBHit()
c = ' '
while c != 'q': 
    if kb.kbhit(): 
        c = kb.getch()
        print(c)


stream.stop() 
stream.close()
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

kb.set_normal_term()

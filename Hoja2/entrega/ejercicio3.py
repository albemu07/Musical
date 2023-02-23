import numpy as np
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit
# creacion de una ventana de pygame
import pygame
from pygame.locals import *
WIDTH = 640 # ancho y alto de la ventana de PyGame
HEIGHT = 480

CHUNK = 1024
SRATE = 44100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theremin")
...
# obtencion de la posicion del raton
for event in pygame.event.get():
    if event.type == pygame.MOUSEMOTION:
        mouseX, mouseY = event.pos
pygame.quit()


# abrimos stream de salida
# el tipo del stream por defecto es float64. Procesamos con esta resolución
# y convertimos a float32 al escribir en el stream
stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
stream.start()

# tabla de ondas -> se copia la tabla cíclicamente hasta rellenenar un CHUNK
def synthWaveTable(wavetable, frame):
    samples = np.zeros(CHUNK)
    t = frame % len(wavetable)
    for i in range(CHUNK):
        samples[i] = wavetable[t]
        t = (t+1) % len(wavetable)
    return samples
# tabla de ondas para un seno de 800 Hz: se almacena un ciclo
frec = 800
waveTable = np.sin(2*np.pi*frec*np.arange(SRATE/frec)/SRATE)
frame = 0

while True:
    samples = synthWaveTable(waveTable,frame)
    stream.write(np.float32(0.5*samples))
    frame += CHUNK
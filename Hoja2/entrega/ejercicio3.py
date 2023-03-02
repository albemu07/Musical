import numpy as np
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
# creacion de una ventana de pygame
import pygame
import wavetable2
from pygame.locals import *
WIDTH = 640 # ancho y alto de la ventana de PyGame
HEIGHT = 480

SRATE = 44100      
CHUNK = 64

def main():
    
    # abrimos stream de salida
    # el tipo del stream por defecto es float64. Procesamos con esta resolución
    # y convertimos a float32 al escribir en el stream
    stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
    stream.start()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Theremin")

    # tabla de ondas para un seno de 800 Hz: se almacena un ciclo
    frec = 800
    frame = 0
    vol = 1.0
    mouseX = 0 
    mouseY = 0
    waveTable = wavetable2.OscWaveTable(frec, vol, SRATE)

    while True:
        # obtencion de la posicion del raton
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos
        newFrec = mouseX / WIDTH * (1000 - 100) + 100
        newVol = mouseY /HEIGHT 
        if (newFrec != frec):
            wavetable2.OscWaveTable.setFrec(waveTable, newFrec)
            frec = newFrec
        if (newVol != vol):
            wavetable2.OscWaveTable.setVol(waveTable, newVol)
            vol = newVol
        samples = wavetable2.OscWaveTable.getChunk(waveTable)
        stream.write(np.float32(0.5*samples))
        frame += CHUNK

main()
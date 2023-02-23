import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante
import matplotlib.pyplot as plt

CHUNK = 1024
SRATE = 44100

last = 0

# informacion de wav)
print("\n\nInfo del wav ",SRATE)
print("  Sample rate ",SRATE)


# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)  # num de canales

# arrancamos stream
stream.start()

def oscChuck(frec,vol):
    global last # var global
    data = vol*np.sin(2*np.pi*(np.arange(CHUNK))*frec/SRATE)
    last += CHUNK # actualizamos ultimo generado
    return np.float32(data)

def sqrChunk(frec, vol):
    global last
    x = np.full((int)(CHUNK* frec / SRATE / 2), 1)
    x2 = np.concatenate((x, -x))
    last += CHUNK
    return np.float32(vol * x2)


kb = kbhit.KBHit()
c= ' '

vol = 1.0
frec = 440
print('\n\nProcessing chunks: ',end='')

# termina con 'q' o cuando no queden samples
end = False # será true cuando el chunk esté vacio

while c!= 'q' and not(end)>0: 
    # nuevo bloque. Si tiene menos de CHUNK samples coge los que quedan
    bloque = oscChuck(frec,vol)
    plt.plot(oscChuck(frec,vol))

    plt.show()
    # lo pasamos al stream
    stream.write(bloque) # escribimos al stream

    # modificación de volumen 
    if kb.kbhit():
        c = kb.getch()
        if (c=='v'): vol= max(0,vol-0.05)
        elif (c=='V'): vol= min(1,vol+0.05)
        if (c=='f'): frec = max(0, frec - 1)
        elif (c=='F'): frec = frec + 1
        print("Vol: ",vol, " Frec: ", frec) 

    print('.',end='')

print('end')

stream.stop()
stream.close()
kb.set_normal_term()
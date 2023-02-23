#  sintesis aditiva con tabla de armonicos y volumenes
import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

SRATE = 44100  # sampling rate, Hz, must be integer
CHUNK = 1024   # tamaño del chunk

# contador de frames. se incrementa cada vez que se procesa un bloque
frame = 0

# frecuencia dada, volumen, frame inicial (para evitar pops)
def osc(frec,vol):
    return np.float32(vol*np.sin(2*np.pi*(np.arange(CHUNK)+frame)*frec/SRATE))
    

# abrimos stream de salida
# el tipo del stream por defecto es float64. Procesamos con esta resolución
# y convertimos a float32 al escribir en el stream
stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
stream.start()

frec = 440  # frec base
step = 5    # variacion de la frecuencia base
vols = [0.3, 0.2, 0.15, 0.15, 0.1, 0.1]  # vols de los armónicos

kb = kbhit.KBHit()
c = ' '
print("[F/f] subir/bajar frecuencia")
while True:
    # lista de armónicos multiplos de la frec base
    arms = [frec*(i+1) for i in range(len(vols))]

    samples = np.zeros(CHUNK) 
   
    for i in range(len(arms)):        
        samples = samples+osc(arms[i],vols[i])

    stream.write(np.float32(0.5*samples))

    if kb.kbhit():
        c = kb.getch()
        if c =='q': break
        elif c=='F': frec=frec+step
        elif c=='f': frec=frec-step
        print("\n\nFrecs:")
        for i in range(len(arms)): print(f"F{i}: {arms[i]} v{i}: {vols[i]}   ",end='')
    frame += CHUNK

stream.stop()

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit           # para lectura de teclas no bloqueante


CHUNK = 1024
SRATE = 44100

def filterLP(bloq, prev, alpha):
    # Aplicar el filtro paso bajo
    bloque_lp = np.copy(bloq)
    bloque_lp[0] = prev + alpha * (bloque_lp[0] - prev)
    for i in range(1, CHUNK):
        bloque_lp[i] = bloque_lp[i-1] + alpha * (bloque_lp[i] - bloque_lp[i-1])
    new_prev = bloque_lp[CHUNK-1]
    return bloque_lp, new_prev

# abrimos stream de salida
stream = sd.OutputStream(
samplerate = SRATE,            # frec muestreo 
blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
channels   = 1)  # num de canales

stream.start()
kb = kbhit.KBHit()

# Calcular los valores de alpha para los filtros LP y HP
alpha_lp = 2    #np.exp(-2*np.pi*f1/SRATE)
alpha_hp = 1/2 

# Inicializar la variable previa
prev_lp = 0
prev_hp = 0

c = ' '
frame = 0

vol = 1.0

data, samplerate = sf.read("piano.wav")
# Aplicar el filtro paso banda
while c != 'q':
    # Obtener el bloque de datos
    bloque = np.copy(data[frame*CHUNK:(frame+1)*CHUNK])
    if len(bloque)==0: 
        break

    bloque, prev_lp = filterLP(bloque, prev_lp, alpha_lp)
    
    if kb.kbhit():
            c = kb.getch()
            if (c=='v'): vol= max(0,vol-0.05)
            elif (c=='V'): vol= min(1,vol+0.05)

    stream.write(np.float32(bloque*vol))

    frame += 1
    # Usar bloque_hp como la señal filtrada
    # Hacer algo con los datos filtrados
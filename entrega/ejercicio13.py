import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit           # para lectura de teclas no bloqueante


CHUNK = 1024
SRATE = 44100
#COMO LO HACE JAIME 

alpha = 1
prev = 0
while c!= 'q':
bloque = np.copy(data[frame*CHUNK:(frame+1)*CHUNK])
bloque[0] = prev + alpha * (bloque[0]-prev)
for i in range(1,CHUNK):
bloque[i] = bloque[i-1] + alpha * (bloque[i]-bloque[i-1])
prev = bloque[CHUNK-1]

#COMO LO HAGO YO 

# abrimos stream de salida
stream = sd.OutputStream(
samplerate = SRATE,            # frec muestreo 
blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
channels   = 1)  # num de canales

stream.start()
kb = kbhit.KBHit()

# Definir los parámetros del filtro
fc = 1000 # Frecuencia central
bw = 500 # Ancho de banda
Q = fc / bw # Factor de calidad

# Calcular las frecuencias de corte del filtro paso bajo y paso alto
f1 = fc / Q
f2 = fc * Q

# Calcular los valores de alpha para los filtros LP y HP
alpha_lp = np.exp(-2*np.pi*f1/SRATE)
alpha_hp = np.exp(-2*np.pi*f2/SRATE)

# Inicializar la variable previa
prev_lp = 0
prev_hp = 0


c = ' '
# Aplicar el filtro paso banda
while c != 'q':
    # Obtener el bloque de datos
    bloque = np.copy(data[frame*CHUNK:(frame+1)*CHUNK])
    
    # Aplicar el filtro paso bajo
    bloque_lp = np.copy(bloque)
    bloque_lp[0] = prev_lp + alpha_lp * (bloque_lp[0] - prev_lp)
    for i in range(1, CHUNK):
        bloque_lp[i] = bloque_lp[i-1] + alpha_lp * (bloque_lp[i] - bloque_lp[i-1])
    prev_lp = bloque_lp[CHUNK-1]
    
    # Aplicar el filtro paso alto
    bloque_hp = np.copy(bloque_lp)
    bloque_hp[0] = prev_hp + alpha_hp * (bloque_hp[0] - prev_hp)
    for i in range(1, CHUNK):
        bloque_hp[i] = alpha_hp * (bloque_hp[i-1] + bloque_lp[i] - bloque_lp[i-1])
    prev_hp = bloque_hp[CHUNK-1]
    
    if kb.kbhit():
            c = kb.getch()
            if (c=='v'): vol= max(0,vol-0.05)
            elif (c=='V'): vol= min(1,vol+0.05)

    # Usar bloque_hp como la señal filtrada
    # Hacer algo con los datos filtrados
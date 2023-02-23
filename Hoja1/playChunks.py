# reproductor con Chunks

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024

# leemos wav en array numpy (data)
# por defecto lee float64 (no soportado por portAudio) 
# podemos hacer directamente la conversion a float32
data, SRATE = sf.read('ex1.wav',dtype="float32")


# informacion de wav)
print("\n\nInfo del wav ",SRATE)
print("  Sample rate ",SRATE)
print("  Sample format: ",data.dtype)
print("  Num channels: ",len(data.shape))
print("  Len: ",data.shape[0])


# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = len(data.shape))  # num de canales

# arrancamos stream
stream.start()

vol = 1.0

kb = kbhit.KBHit()
c= ' '

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
numBloque = 0 # contador de bloques/chunks

vol = 1.0
print('\n\nProcessing chunks: ',end='')

# termina con 'q' o cuando no queden samples
end = False # será true cuando el chunk esté vacio

while c!= 'q' and not(end)>0: 
    # nuevo bloque. Si tiene menos de CHUNK samples coge los que quedan
    bloque = data[numBloque*CHUNK : (numBloque+1)*CHUNK]
    if bloque.shape[0]==0: # bloque vacio: terminamos
        end=True
    else:
        bloque *= vol
        # lo pasamos al stream
        stream.write(bloque) # escribimos al stream

        # modificación de volumen 
        if kb.kbhit():
            c = kb.getch()
            if (c=='v'): vol= max(0,vol-0.05)
            elif (c=='V'): vol= min(1,vol+0.05)
            print("Vol: ",vol)

        numBloque += 1
        print('.',end='')

print('end')

stream.stop()
stream.close()
kb.set_normal_term()
